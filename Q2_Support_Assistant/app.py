"""
Q2 — Document-Aware Support Assistant
A multi-turn Streamlit chat assistant that:
  • Uses a knowledge base built from the provided documents
  • Maintains session context (remembers what was asked)
  • Avoids repeating information already shared
  • Handles topic switches gracefully
  • Cites the specific document section in each response
  • Uses Google Gemini API (via REST — no extra package needed)
"""

import streamlit as st
import re
import sys
import os
import requests

sys.path.insert(0, os.path.dirname(__file__))
from knowledge_base import search_kb, KNOWLEDGE_BASE

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📄 Document Support Assistant",
    page_icon="📄",
    layout="wide",
)


# ─── Gemini API call ─────────────────────────────────────────────────────────
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
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1200},
    }
    if system_text:
        payload["systemInstruction"] = {"parts": [{"text": system_text}]}

    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text}")
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


# ─── System prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a knowledgeable support assistant with access to a curated knowledge base.

Your knowledge base covers:
1. Inventory records for 46 technology products (laptops, monitors, keyboards, gaming gear, etc.)
2. HDFC Life Insurance documents for a customer named Ashok, including:
   - Proposal / Customer Declaration Form
   - Assignment Request Form
   - Suitability Profiler Declaration
   - Multiple Policies Consent Form
   - Moral Hazard Questionnaire
   - Benefit Illustration Declaration
   - FATCA Annexure Form
   - NACH/ECS Bank Mandate
   - Identity documents: PAN Card, Aadhaar Card, Passport, Driving Licence

Rules you MUST follow:
1. CITE your source in every response using the format: [Source: <doc_id> – <title>, Section: <section>]
2. If you already covered information in a previous turn, do NOT repeat it. Say "As mentioned earlier..." instead.
3. If the user switches topics, acknowledge the switch and answer cleanly.
4. If information is not in the context provided, say so — do NOT hallucinate.
5. Keep answers focused. Use bullet points for multi-part answers.

The relevant knowledge base chunks will be provided as context before the user's question.
"""


# ─── Context builder ──────────────────────────────────────────────────────────
def build_context_block(chunks: list) -> str:
    if not chunks:
        return "No directly relevant document chunks found."
    lines = []
    for c in chunks:
        lines.append(f"[{c['doc_id']}] {c['title']} — {c['section']}:\n{c['content']}")
    return "\n\n".join(lines)


# ─── Main agent turn ──────────────────────────────────────────────────────────
def agent_turn(user_msg: str, history: list, already_cited: set, api_key: str) -> tuple:
    chunks = search_kb(user_msg, top_k=4)
    context = build_context_block(chunks)

    covered_summary = ""
    if already_cited:
        covered_summary = (
            f"\n\nTopics/documents already discussed: {', '.join(sorted(already_cited))}. "
            "Do not repeat information from these unless the user explicitly asks."
        )

    augmented_user = (
        f"[Retrieved Context]\n{context}\n"
        f"{covered_summary}\n\n"
        f"[User Question]\n{user_msg}"
    )

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history
        + [{"role": "user", "content": augmented_user}]
    )

    reply = call_gemini(messages, api_key)

    new_cited = set(already_cited)
    for chunk in chunks:
        if chunk["doc_id"].lower() in reply.lower() or chunk["title"][:15].lower() in reply.lower():
            new_cited.add(chunk["doc_id"])

    return reply, new_cited


# ─── UI ───────────────────────────────────────────────────────────────────────
st.title("📄 Document-Aware Support Assistant")
st.caption("Powered by Google Gemini · Cites sources · Remembers context · No repetition")

with st.sidebar:
    st.header("⚙️ Configuration")
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        st.success("✅ GEMINI_API_KEY loaded from environment")
        api_key = env_key
    else:
        api_key = st.text_input("Gemini API Key", type="password", key="gemini_key")
        st.caption("Or set GEMINI_API_KEY as an environment variable")

    st.markdown("---")
    st.markdown("**Knowledge Base Documents:**")
    unique_titles = list(dict.fromkeys(e["title"] for e in KNOWLEDGE_BASE))
    for t in unique_titles:
        st.markdown(f"• {t}")

    st.markdown("---")
    st.markdown("**Suggested conversation (10+ turns):**")
    suggestions = [
        "What products are in the inventory?",
        "Which items have the highest total cost value?",
        "Tell me about Ashok's insurance policy.",
        "What is the sum assured on the policy?",
        "Who is the assignee on the assignment form?",
        "What are the nominee details from the Moral Hazard Questionnaire?",
        "What bank details are on the ECS mandate?",
        "What does FATCA say about Ashok's tax residency?",
        "Summarise all of Ashok's identity documents.",
        "Which products have hand-in-stock below 25 units?",
        "What is the reason for the policy assignment?",
        "What did Ashok declare in the suitability profiler?",
    ]
    for s in suggestions:
        if st.button(s, key=f"sug_{s[:20]}"):
            st.session_state["prefill"] = s

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "cited" not in st.session_state:
    st.session_state.cited = set()
if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0

# Display existing conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.turn_count > 0:
    st.sidebar.markdown(f"**Conversation turns:** {st.session_state.turn_count}")

# Input
prefill = st.session_state.pop("prefill", None)
user_input = st.chat_input("Ask about the documents or inventory data…") or prefill

if user_input:
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar or set GEMINI_API_KEY env var.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and composing answer…"):
            try:
                reply, new_cited = agent_turn(
                    user_input,
                    st.session_state.history,
                    st.session_state.cited,
                    api_key,
                )
                st.session_state.cited = new_cited
            except Exception as e:
                reply = f"❌ Error: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": reply})
    st.session_state.turn_count += 1
    st.rerun()

# Welcome message
if not st.session_state.messages:
    st.info(
        "👋 Hi! I'm your document-aware support assistant. "
        "I have access to inventory records and a full set of HDFC Life insurance documents for Ashok. "
        "Ask me anything — I'll cite my source every time and won't repeat myself!"
    )
