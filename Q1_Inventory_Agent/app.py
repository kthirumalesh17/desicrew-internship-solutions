"""
Q1 — Inventory Data Agent
A Streamlit chat interface that:
  • Loads the inventory Excel sheet
  • Writes & executes Python/pandas code to answer questions
  • Looks up definitions via a search tool (Wikipedia REST API)
  • Summarises findings in plain English
  • Uses Google Gemini API (via REST — no extra package needed)
"""

import streamlit as st
import pandas as pd
import io
import traceback
import contextlib
import re
import requests
import os

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="📦 Inventory Data Agent", page_icon="📦", layout="wide")

# ─── Load the dataset ──────────────────────────────────────────────────────────
EXCEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Question 1 & 3 (Files to use)",
    "Question 1",
    "Inventory-Records-Sample-Data.xlsx",
)

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    raw = pd.read_excel(path, header=None)
    header_row = None
    for i, row in raw.iterrows():
        if any("Product ID" in str(c) for c in row.values):
            header_row = i
            break
    if header_row is None:
        raise ValueError("Cannot find header row in Excel file.")
    df = pd.read_excel(path, header=header_row)
    df = df.dropna(how="all").dropna(axis=1, how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return df


# ─── Gemini API call ──────────────────────────────────────────────────────────
def call_gemini(messages: list, api_key: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-3.1-flash-lite:generateContent?key=" + api_key
    )
    contents = []
    system_text = ""
    for msg in messages:
        if msg["role"] == "system":
            system_text = msg["content"]
        elif msg["role"] == "user":
            contents.append({"role": "user", "parts": [{"text": msg["content"]}]})
        elif msg["role"] == "assistant":
            contents.append({"role": "model", "parts": [{"text": msg["content"]}]})

    payload = {
        "contents": contents,
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1500},
    }
    if system_text:
        payload["systemInstruction"] = {"parts": [{"text": system_text}]}

    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text}")
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


# ─── Code execution sandbox ───────────────────────────────────────────────────
def safe_exec(code: str, df: pd.DataFrame) -> str:
    buf = io.StringIO()
    local_ns = {"df": df, "pd": pd}
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {"__builtins__": __builtins__}, local_ns)  # noqa: S102
        output = buf.getvalue()
        return output.strip() if output.strip() else "(no output produced)"
    except Exception:
        return f"❌ Code execution error:\n{traceback.format_exc()}"


# ─── Wikipedia search ─────────────────────────────────────────────────────────
def wikipedia_search(query: str) -> str:
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(query)
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json().get("extract", "No summary available.")
        return f"Wikipedia returned HTTP {r.status_code}."
    except Exception as e:
        return f"Search failed: {e}"


# ─── System prompt ────────────────────────────────────────────────────────────
def build_system_prompt(df: pd.DataFrame) -> str:
    schema = ", ".join(df.columns.tolist())
    sample = df.head(3).to_string(index=False)
    return f"""You are an expert inventory data analyst agent.

The user has loaded an inventory Excel dataset into a pandas DataFrame called `df`.

Dataset schema (column names):
{schema}

First 3 rows:
{sample}

Your job:
1. Understand the user's question.
2. If it requires data analysis, write Python/pandas code that computes the answer.
   - Wrap runnable code in a ```python ... ``` block.
   - Use `print()` to output results.
   - `df` and `pd` are already in scope — do NOT import them again.
3. If the question is about a concept or definition (e.g. "what is COGS?"), use
   [SEARCH: your search query] in your response.
4. Always end with a plain-English summary of your findings.

Rules:
- Be concise and accurate.
- Never hallucinate data values — only state what the code output confirms.
"""


# ─── Agent turn ───────────────────────────────────────────────────────────────
def agent_turn(user_msg: str, history: list, df: pd.DataFrame, api_key: str) -> str:
    system = build_system_prompt(df)
    messages = [{"role": "system", "content": system}] + history + [
        {"role": "user", "content": user_msg}
    ]

    response = call_gemini(messages, api_key)

    code_blocks = re.findall(r"```python\s*(.*?)```", response, re.DOTALL)
    execution_outputs = []
    for block in code_blocks:
        out = safe_exec(block.strip(), df)
        execution_outputs.append(out)

    search_results = []
    for query in re.findall(r"\[SEARCH:\s*(.*?)\]", response):
        result = wikipedia_search(query.strip())
        search_results.append(f"**Search result for '{query}':**\n{result}")

    if execution_outputs or search_results:
        synthesis_content = response + "\n\n"
        if execution_outputs:
            synthesis_content += "**Code output:**\n" + "\n---\n".join(execution_outputs)
        if search_results:
            synthesis_content += "\n\n" + "\n\n".join(search_results)

        messages.append({"role": "assistant", "content": synthesis_content})
        messages.append({
            "role": "user",
            "content": (
                "Based on the code output and/or search results above, "
                "provide a clear, concise plain-English summary. "
                "Include the exact numbers/values from the output."
            ),
        })
        final = call_gemini(messages, api_key)
        return synthesis_content + "\n\n---\n### 📋 Summary\n" + final

    return response


# ─── UI ───────────────────────────────────────────────────────────────────────
st.title("📦 Inventory Data Agent")
st.caption("Powered by Google Gemini · Ask questions about your inventory data in plain English.")

with st.sidebar:
    st.header("⚙️ Configuration")

    # Read from env var first, fallback to sidebar input
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        st.success("✅ GEMINI_API_KEY loaded from environment")
        api_key = env_key
    else:
        api_key = st.text_input("Gemini API Key", type="password")
        st.caption("Or set GEMINI_API_KEY as an environment variable")

    st.markdown("---")
    st.markdown("**Example questions:**")
    examples = [
        "Which product has the highest total cost?",
        "What is the average cost price per unit?",
        "List all products with hand-in-stock below 30.",
        "What does COGS mean?",
        "Which 5 products sold the most units?",
        "Total inventory value across all products?",
        "Which products have a purchase/stock-in greater than 20?",
        "What is the turnover ratio for Laptop?",
    ]
    for ex in examples:
        if st.button(ex, key=ex):
            st.session_state["prefill"] = ex

# Load data
try:
    df = load_data(EXCEL_PATH)
    with st.sidebar:
        st.markdown("---")
        st.success(f"✅ Dataset loaded: {len(df)} products")
        st.dataframe(df, height=300)
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prefill = st.session_state.pop("prefill", None)
user_input = st.chat_input("Ask a question about the inventory data…") or prefill

if user_input:
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar or set GEMINI_API_KEY env var.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                reply = agent_turn(user_input, st.session_state.history, df, api_key)
            except Exception as e:
                reply = f"❌ Error: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": reply})
