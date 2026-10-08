"""
Q3 — Document Intelligence Pipeline — Streamlit UI
Classifies documents, extracts fields with per-field confidence scores,
flags low-confidence fields, and generates structured JSON output.
"""

import streamlit as st
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from extractor import (
    run_pipeline,
    classify_document,
    extract_fields,
    generate_flagging_report,
    CONFIDENCE_THRESHOLD,
    EXTRACTED_DATA,
    DOC_REGISTRY,
)

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🔍 Document Intelligence Pipeline",
    page_icon="🔍",
    layout="wide",
)

# ─── Paths ────────────────────────────────────────────────────────────────────
Q3_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Question 1 & 3 (Files to use)",
    "Question 3",
)

# ─── Helpers ──────────────────────────────────────────────────────────────────
def confidence_color(c: float) -> str:
    if c >= 0.90:
        return "🟢"
    elif c >= CONFIDENCE_THRESHOLD:
        return "🟡"
    else:
        return "🔴"


def render_fields_table(fields: dict):
    rows = []
    for field, info in fields.items():
        icon = confidence_color(info["confidence"])
        flag = "⚠️ FLAG" if info["confidence"] < CONFIDENCE_THRESHOLD else ""
        rows.append({
            "Field": field.replace("_", " ").title(),
            "Extracted Value": info["value"] or "(not found)",
            "Confidence": f"{info['confidence']:.0%}",
            "Status": f"{icon} {flag}".strip(),
        })
    import pandas as pd
    return pd.DataFrame(rows)


# ─── UI ───────────────────────────────────────────────────────────────────────
st.title("🔍 Document Intelligence Pipeline")
st.caption(
    "Classifies documents → Extracts fields → Assigns per-field confidence scores → "
    "Flags low-confidence fields for human review."
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    threshold_display = st.slider(
        "Confidence Threshold",
        min_value=0.5, max_value=0.95, value=CONFIDENCE_THRESHOLD, step=0.05,
        help="Fields below this threshold are flagged for human review.",
    )
    st.markdown("---")
    st.markdown(f"**Documents folder:**")
    st.code(Q3_FOLDER, language=None)
    st.markdown("**Legend:**")
    st.markdown("🟢 High confidence (≥ 90%)")
    st.markdown("🟡 Acceptable (≥ threshold)")
    st.markdown("🔴 Flagged (< threshold)")

# Run pipeline
with st.spinner("Running pipeline on all 10 documents…"):
    pipeline_output = run_pipeline(Q3_FOLDER)

summary = pipeline_output["pipeline_summary"]
documents = pipeline_output["documents"]
flagging = pipeline_output["flagging_report"]

# ── Summary metrics ───────────────────────────────────────────────────────────
st.header("📊 Pipeline Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Documents", summary["total_documents"])
col2.metric("Printed Documents", summary["printed_documents"])
col3.metric("Handwritten Documents", summary["handwritten_documents"])
col4.metric("Flagged Fields", flagging["total_flagged_fields"])

st.markdown("---")

# ── Per-document results ──────────────────────────────────────────────────────
st.header("📄 Per-Document Extraction Results")

for doc in documents:
    fname = doc["filename"]
    doc_type = doc["doc_type"]
    hw_label = "✍️ Handwritten" if doc["is_handwritten_dominant"] else "🖨️ Printed"
    flagged_in_doc = sum(
        1 for f in doc["fields"].values() if f["confidence"] < threshold_display
    )
    flag_badge = f" — ⚠️ {flagged_in_doc} field(s) flagged" if flagged_in_doc else ""

    with st.expander(f"**{fname}** — {doc_type} ({hw_label}){flag_badge}", expanded=False):
        col_a, col_b = st.columns([2, 1])
        with col_a:
            if doc["fields"]:
                import pandas as pd
                df_table = render_fields_table(doc["fields"])
                st.dataframe(df_table, width="stretch", hide_index=True)
            else:
                st.warning("No fields extracted.")

        with col_b:
            # Try to display the image
            img_path = Path(Q3_FOLDER) / fname
            if img_path.exists() and fname.lower().endswith((".png", ".jpg", ".jpeg")):
                st.image(str(img_path), caption=fname, width="stretch")

        if doc.get("document_notes"):
            st.info(f"📝 **Notes:** {doc['document_notes']}")

st.markdown("---")

# ── Flagging report ───────────────────────────────────────────────────────────
st.header("⚠️ Flagging Report")
st.markdown(
    f"**Confidence Threshold:** {threshold_display:.0%}  \n"
    f"**Rationale:** {flagging['threshold_rationale']}"
)

if flagging["flagged_items"]:
    import pandas as pd
    flag_rows = []
    for item in flagging["flagged_items"]:
        if item["confidence"] < threshold_display:
            flag_rows.append({
                "File": item["filename"],
                "Document Type": item["doc_type"],
                "Field": item["field"].replace("_", " ").title(),
                "Extracted Value": item["extracted_value"],
                "Confidence": f"{item['confidence']:.0%}",
                "Flag Reason": item["flag_reason"],
            })
    if flag_rows:
        st.dataframe(pd.DataFrame(flag_rows), width="stretch", hide_index=True)
    else:
        st.success("No fields flagged at the current threshold.")
else:
    st.success("No fields flagged.")

st.markdown("---")

# ── Methodology note ─────────────────────────────────────────────────────────
st.header("📋 Methodology Note")
with st.expander("Handwritten vs Printed Text Handling + Failure Cases", expanded=True):
    st.markdown(pipeline_output["methodology_note"].replace("\n", "  \n"))

st.markdown("---")

# ── JSON output ──────────────────────────────────────────────────────────────
st.header("📥 Full JSON Output")
st.caption("Structured extraction output per document, suitable for downstream processing.")

# Download button
json_str = json.dumps(pipeline_output, indent=2, ensure_ascii=False)
st.download_button(
    label="⬇️ Download Full JSON",
    data=json_str,
    file_name="document_extraction_output.json",
    mime="application/json",
)

with st.expander("View JSON", expanded=False):
    st.code(json_str, language="json")
