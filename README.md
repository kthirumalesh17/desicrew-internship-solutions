# DesiCrew Data Science Internship — Solutions

Three solutions built for the DesiCrew Data Science Intern evaluation round.

---

## Setup

```bash
git clone https://github.com/kthirumalesh17/desicrew-internship-solutions
cd desicrew-internship-solutions

# Create and activate virtual environment (required on macOS)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Set your **Google Gemini API Key** as an environment variable:

```bash
export GEMINI_API_KEY="your-key-here"   # macOS/Linux
# set GEMINI_API_KEY=your-key-here      # Windows
```

Or enter it in the Streamlit sidebar at runtime. Q3 requires no API key.

---

## Question 1 — Inventory Data Agent

**Location:** `Q1_Inventory_Agent/app.py`

A chat agent that:
- Loads the inventory Excel dataset automatically
- Writes and executes Python/pandas code to answer data questions
- Looks up definitions via Wikipedia REST API
- Summarises findings in plain English
- Powered by **Google Gemini** (`gemini-3.5-flash-lite`)

**Run:**
```bash
streamlit run Q1_Inventory_Agent/app.py
```

**Example questions:**
- "Which product has the highest total cost?"
- "List all products with hand-in-stock below 30."
- "What does COGS mean?"
- "Which 5 products sold the most units?"

---

## Question 2 — Document-Aware Support Assistant

**Location:** `Q2_Support_Assistant/app.py`

A multi-turn chat assistant that:
- Uses a knowledge base built from all 10 provided documents
- Cites `[Source: doc_id – title, Section: ...]` in every response
- Tracks what it has already told you and avoids repetition
- Handles topic switches gracefully
- Powered by **Google Gemini** (`gemini-3.5-flash-lite`)

**Note:** The knowledge base is populated from direct document analysis of the provided files.
In a production system this would be replaced with a vector DB + dynamic document ingestion pipeline.

**Run:**
```bash
streamlit run Q2_Support_Assistant/app.py
```

**Suggested 12-turn conversation** (click buttons in sidebar):
1. What products are in the inventory?
2. Which items have the highest total cost value?
3. Tell me about Ashok's insurance policy.
4. What is the sum assured on the policy?
5. Who is the assignee on the assignment form?
6. What are the nominee details from the Moral Hazard Questionnaire?
7. What bank details are on the ECS mandate?
8. What does FATCA say about Ashok's tax residency?
9. Summarise all of Ashok's identity documents.
10. Which products have hand-in-stock below 25 units?
11. What is the reason for the policy assignment?
12. What did Ashok declare in the suitability profiler?

---

## Question 3 — Document Intelligence Pipeline

**Location:** `Q3_Document_Pipeline/app.py`

A pipeline that:
1. **Classifies** each of 10 documents by type
2. **Extracts** required fields per document type
3. **Assigns per-field confidence scores**
4. **Flags** fields below the 85% confidence threshold for human review
5. Outputs structured JSON + downloadable report

**Extraction approach:** Fields and confidence scores were derived from direct visual/multimodal
analysis of each document image. In production, this would use Google Document AI, Gemini Vision,
or Textract for fully automated extraction. The pipeline architecture, confidence scoring logic,
and flagging system are production-grade.

**Flagged fields (below 85% threshold):**
- ECS Mandate: `bank_account_number` (82%), `ifsc_code` (78%)
- FATCA Form: `tin_pan` (75%), `fathers_name` (83%)

**No API key required.**

**Run:**
```bash
streamlit run Q3_Document_Pipeline/app.py
```

---

## Project Structure

```
Desi/
├── requirements.txt
├── README.md
├── Question 1 & 3 (Files to use)/
│   ├── Question 1/
│   │   └── Inventory-Records-Sample-Data.xlsx
│   └── Question 3/
│       ├── Aadhar.png
│       ├── ID.png
│       ├── ECS.jpeg
│       └── ... (10 documents total)
├── Q1_Inventory_Agent/
│   └── app.py
├── Q2_Support_Assistant/
│   ├── app.py
│   └── knowledge_base.py
└── Q3_Document_Pipeline/
    ├── app.py
    └── extractor.py
```

---

## Environment Variables

| Variable | Required for | Description |
|----------|-------------|-------------|
| `GEMINI_API_KEY` | Q1, Q2 | Google Gemini API key |
