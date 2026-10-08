"""
Knowledge base for Q2 — built from the documents provided in the context.
Each entry has: doc_id, title, section, content.
This simulates a RAG knowledge base without requiring external vector stores.
"""

KNOWLEDGE_BASE = [
    # ── Inventory / Business data (from Q1 Excel) ────────────────────────────
    {
        "doc_id": "INV-001",
        "title": "Inventory Records – Product Catalogue",
        "section": "Electronics – High Value",
        "content": (
            "The inventory contains 46 product SKUs from P101 to P146. "
            "High-value products include: Laptop (P101, cost $1,200/unit, 60 units in stock), "
            "Smartphone (P105, cost $900/unit, 80 units), Tablet (P106, cost $700/unit, 55 units), "
            "Monitor (P102, cost $500/unit, 50 units), and Graphics Card (P122, cost $600/unit, 49 units). "
            "Total inventory cost for Laptops is $72,000 and for Smartphones is also $72,000."
        ),
    },
    {
        "doc_id": "INV-002",
        "title": "Inventory Records – Stock Movement",
        "section": "Purchase and Sales Summary",
        "content": (
            "Across all 46 products, total opening stock was approximately 1,615 units. "
            "Total stock purchased/received was around 680 units. "
            "Total units sold were around 310 units. "
            "Products with highest units sold: Smartphone (20), Laptop (10), Monitor (5 — low), "
            "Router (12), Wireless Earbuds (7). "
            "Products with lowest hand-in-stock: Gaming Chair (19 units, P120), "
            "External DVD Drive (17 units, P136), WiFi Adapter (23 units, P135)."
        ),
    },
    {
        "doc_id": "INV-003",
        "title": "Inventory Records – Cost Analysis",
        "section": "Total Inventory Value",
        "content": (
            "The total cost value across all products in hand-in-stock is substantial. "
            "Top total cost products: Laptop ($72,000), Smartphone ($72,000), Tablet ($38,500), "
            "Monitor ($25,000), Graphics Card ($29,400), Gaming Monitor ($11,600), CPU ($13,300). "
            "Lowest total cost items: Thermal Paste (P133, $250), Mouse Pad (P132, $580), "
            "Printer Cable (P137, $145), Anti-Glare Screen Protector (P141, $280)."
        ),
    },
    # ── HDFC Life Insurance Documents (from Q3 set) ──────────────────────────
    {
        "doc_id": "PROP-001",
        "title": "HDFC Life – Proposal / Customer Declaration Form",
        "section": "Policy Details",
        "content": (
            "Application/Proposal Form Number: 1500137601025. "
            "Name of Life Assured / Proposed Policyholder: Ashok. "
            "Type of Plan: Savings. "
            "Name of Insurance Plan: HDFC Life Sanjay Pay Advantage. "
            "Premium Payable (INR): 50,000. "
            "Frequency: Annual. "
            "Premium Paying Term: 12 Years. "
            "Sum Assured (INR): 630,000. "
            "Signed on 26/04/2026 at West Bihar."
        ),
    },
    {
        "doc_id": "PROP-002",
        "title": "HDFC Life – Proposal Form",
        "section": "Customer Declarations",
        "content": (
            "The Customer Declaration form contains two declaration sections. "
            "The first section ('I/We declare that') covers: truthfulness of statements, "
            "submission of original documents, notification of changes, premium payment from legal sources, "
            "and compliance with Prevention of Money Laundering Act 2002. "
            "The second section ('I/We agree and understand') covers: company risk on proposal, "
            "right to accept or reject, initial deposit adjustments, medical examination consent, "
            "and communication consent including WhatsApp and VoIP."
        ),
    },
    {
        "doc_id": "ASSIGN-001",
        "title": "HDFC Life – Assignment Request Form",
        "section": "Assignor / Assignee Details",
        "content": (
            "Assignment Request Form for Policy 1500137601025. "
            "Assignor: Ashok. Insurance Plan: HDFC Life Sanjay Pay Advantage. "
            "Assignee: HDFC Bank, West Bihar. Assignee Type: Company. "
            "Relationship of Assignee to Assignor: Creditor. "
            "Reason for Assignment: Loan Protection. "
            "Proof of Assignment: Loan Sanction Letter. "
            "Assignment is not subject to any condition (treated as Absolute). "
            "Date: 26/04/2026. Place: West Bihar."
        ),
    },
    {
        "doc_id": "ASSIGN-002",
        "title": "HDFC Life – Assignment Request Form",
        "section": "Policy Endorsement",
        "content": (
            "Endorsement on the Policy document: Ashok, in consideration of Loan Protection, "
            "assigns in favour of HDFC Bank (Assignee, related as Creditor) all rights, title and interest "
            "in Insurance Policy 1500137601025 granted by HDFC Life. "
            "Dated 26 day of APR 2026. Witness: Rajesh, West Bihar. "
            "Important notes: Assignment cancels existing nominations; requires original Policy bond; "
            "taxes deducted at source per Income-tax Act 1961."
        ),
    },
    {
        "doc_id": "SUIT-001",
        "title": "HDFC Life – Suitability Profiler Declaration",
        "section": "Customer Suitability Declaration",
        "content": (
            "Application/Proposal Form Number: 1500137601025. "
            "Name of Life Assured / Proposed Policyholder: Ashok. "
            "Declaration: Product recommendation by HDFC Life was derived based on inputs and information "
            "provided by Ashok via the Suitability Profiler. Ashok confirms the product is suitable "
            "for their insurance needs and financial objectives. "
            "Name of Agent/SP: Ramesh Kumar. "
            "Date: 26/04/2026. Place: West Bihar."
        ),
    },
    {
        "doc_id": "SPLIT-001",
        "title": "HDFC Life – Split & Multiple Policies Customer Consent Form",
        "section": "Multiple Policy Consent",
        "content": (
            "Proposer/Life Assured Name: Ashok. "
            "Ashok confirms taking multiple policies from HDFC Life Insurance in the last six months. "
            "Reason for buying multiple policies (checked): Financial Planning "
            "(viz. payout on different life stages, different payment terms, etc.). "
            "Other options not selected: Different investment/protection needs, "
            "Separate policy purchased for different beneficiary, Others. "
            "Date: 26/04/2026. Place: West Bihar."
        ),
    },
    {
        "doc_id": "MHQ-001",
        "title": "HDFC Life – Moral Hazard Questionnaire",
        "section": "Application & Nominee Details",
        "content": (
            "Application No.: 1500137601025. "
            "Name of the Life to be Assured: Ashok. "
            "Family dependents: Father – No, Mother – No, Spouse – No, Children – No. "
            "Nominee relationship: Nephew. "
            "Nominee is not financially dependent on Ashok. "
            "Reason for not choosing immediate family: Love and affection. "
            "Date: 26/04/2026 (handwritten). Place: West Bihar."
        ),
    },
    {
        "doc_id": "BENILL-001",
        "title": "HDFC Life – Benefit Illustration Declaration",
        "section": "Policy Benefit Illustration",
        "content": (
            "Application/Proposal Form Number: 1500137601025. "
            "Name of Life Assured / Proposed Policyholder: Ashok. "
            "Benefit Illustration is intended to show year-wise premiums payable and benefits under the policy. "
            "Guaranteed benefits will be clearly marked. Variable benefits use two assumed future investment "
            "return rates: 8% p.a. and 4% p.a. These are not guarantees. "
            "Annualised Premium excludes: underwriting extra premium, frequency loadings, rider premiums, "
            "Goods & Service Tax. "
            "Policyholder (Ashok) confirms reading and understanding terms/conditions and risks. "
            "Date: 26/04/2026. Place: West Bihar."
        ),
    },
    {
        "doc_id": "FATCA-001",
        "title": "HDFC Life – FATCA Annexure Form",
        "section": "FATCA / CRS Compliance",
        "content": (
            "Form reference: NRMP 52492101362 / CANA. "
            "Policy No.: 1500137601025. "
            "Tax residency: India only (checkbox ticked for 'Only India'). "
            "TIN/Functional Equivalent: BPQPD3051R. Issuing country: India. Documents provided: PAN card. "
            "Father's Name: Arjun Das Kumar. Spouse's Name: Greetha. "
            "Place of Birth: West Bihar. Country of Birth: India. "
            "Nationality: Indian. Occupation: Salaried. "
            "Signed by Ashok. Date: 25/04/2026 (handwritten). Place: West Bihar."
        ),
    },
    {
        "doc_id": "ECS-001",
        "title": "HDFC Life – NACH Mandate Instruction (ECS)",
        "section": "Bank Mandate Details",
        "content": (
            "NACH/ECS Mandate for HDFC Life premium collection. "
            "Bank Account Number: 31004258 91112 (handwritten). "
            "Bank Name: State Bank of India. "
            "IFSC Code: SBIN0271112 (handwritten). "
            "Amount in figures: ₹50,000. Amount in words: Fifty Thousand Only. "
            "Frequency: Monthly (ticked). Debit Type: Fixed Amount. "
            "Reference No. 1 (Application/Policy No.): 1500137601025. "
            "Date of mandate: 26/01/2026. "
            "Account holder name as in bank records: Ashok."
        ),
    },
    {
        "doc_id": "PAN-001",
        "title": "PAN Card – Ashok",
        "section": "Identity Document",
        "content": (
            "PAN Card issued by Income Tax Department, Government of India. "
            "PAN Number: ABCDE1234F. "
            "Full Name: MR. ASHOK. "
            "Father's Name: S/O KUMAR. "
            "Date of Birth: 18/12/1979. "
            "Note: This is a sample/demonstration PAN card."
        ),
    },
    {
        "doc_id": "AADHAAR-001",
        "title": "Aadhaar Card – Ashok",
        "section": "Identity Document",
        "content": (
            "Aadhaar Card issued by Unique Identification Authority of India (UIDAI). "
            "Name: Mr. Ashok. "
            "Date of Birth: 18/12/1979. "
            "Gender: Male. "
            "Aadhaar Number: 1234 5678 9012. "
            "Address: S/O Kumar, Kataia, West Bihar, India – 841543. "
            "Enrollment No.: 1234/56789/12345. "
            "Date of Issue: 01/01/2015. "
            "Note: Sample/dummy Aadhaar card for demonstration purposes only."
        ),
    },
    {
        "doc_id": "PASSPORT-001",
        "title": "Passport – Ashok",
        "section": "Identity Document",
        "content": (
            "Republic of India Passport. "
            "Passport Number: X1234567. "
            "Type: P. Country Code: IND. "
            "Surname: ASHOK. Given Name: MR. ASHOK. "
            "Nationality: INDIAN. "
            "Date of Birth: 18/12/1979. Sex: M. "
            "Place of Birth: WEST BIHAR. "
            "Father's Name: KUMAR. "
            "Address: S/O KUMAR, KATAIA, WEST BIHAR, INDIA – 841543. "
            "Date of Issue: 01/01/2020. Date of Expiry: 01/01/2030. "
            "Place of Issue: PATNA. "
            "MRZ Line 2: X1234567<7IND7912185M3001010<<<<<<<<<<<<<<08. "
            "Note: Sample passport for demonstration purposes only."
        ),
    },
    {
        "doc_id": "DL-001",
        "title": "Driving Licence – Ashok",
        "section": "Identity Document",
        "content": (
            "Indian Union Driving Licence – Maharashtra State. "
            "DL Number: MH12 2021 0001234. "
            "Name: MR. ASHOK. "
            "S/W/D of: KUMAR. "
            "DOB: 18/12/1979. Blood Group: B+. "
            "Address: S/O Kumar, Kataia, West Bihar, India – 841543. "
            "Date of Issue (DOI): 15/06/2021. "
            "Valid Till: 14/06/2041. "
            "Licencing Authority: RTO, Gaya. "
            "Vehicle classes: MCWG (valid till 14/06/2041), LMV (valid till 14/06/2041), "
            "HMV (valid till 14/06/2041)."
        ),
    },
]

def search_kb(query: str, top_k: int = 3) -> list[dict]:
    """
    Simple keyword-based retrieval from the knowledge base.
    Returns top_k most relevant chunks.
    """
    query_lower = query.lower()
    scores = []
    for entry in KNOWLEDGE_BASE:
        text = (entry["title"] + " " + entry["section"] + " " + entry["content"]).lower()
        # Count keyword overlaps
        words = set(re.split(r'\W+', query_lower))
        hits = sum(1 for w in words if w and len(w) > 2 and w in text)
        scores.append((hits, entry))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scores[:top_k] if _ > 0]


import re  # noqa: E402 (needed in module scope)
