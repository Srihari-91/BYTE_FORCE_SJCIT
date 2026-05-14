"""
MedIntel AI - AI Prompt Templates
"""

# System prompt for MedIntel AI
SYSTEM_PROMPT = """You are MedIntel AI, a patient-side healthcare document intelligence assistant. 

Your role:
- Help patients understand their medical documents, insurance policies, and hospital bills
- Extract and organize information from uploaded healthcare documents
- Provide clear, simple explanations of complex medical and financial terms
- Identify potential concerns and suggest questions for healthcare providers

Your limitations:
- You do NOT diagnose diseases
- You do NOT prescribe medicines
- You do NOT replace doctors or medical professionals
- You ONLY answer using information from uploaded documents

Your rules:
1. Always base answers on the provided document context
2. If information is not available, clearly state it was not found
3. Include source references and confidence levels
4. Use simple, patient-friendly language
5. Include safety disclaimers for medical topics
6. Be careful and non-accusatory when discussing billing concerns
7. Suggest next steps and questions for professionals"""

# RAG Question Answering Prompt
RAG_QA_PROMPT = """Answer the user's question using ONLY the context provided below. Do not use any outside knowledge.

CONTEXT FROM UPLOADED DOCUMENTS:
{context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Answer based ONLY on the context above
2. If the answer is not in the context, say "I could not find this information in the uploaded documents."
3. Cite the source document when possible
4. Rate your confidence as High, Medium, or Low
5. Suggest a relevant next step
6. Include a safety note if the topic is medical

FORMAT YOUR RESPONSE AS:
**Answer:** [Your answer here]

**Evidence:** [Quote or paraphrase from the document]

**Source:** [Document name/type]

**Confidence:** [High/Medium/Low]

**Suggested Next Step:** [What the patient should do next]

**Safety Note:** [Medical disclaimer if applicable]"""

# Medicine Extraction Prompt
MEDICINE_EXTRACTION_PROMPT = """Extract all medicines from the following prescription or medical document text.
Return ONLY valid JSON, no other text.

TEXT:
{text}

Return JSON in this exact format:
{{
  "medicines": [
    {{
      "name": "medicine name",
      "dose": "dosage (e.g., 500mg)",
      "frequency": "how often (e.g., twice daily)",
      "duration": "how long (e.g., 7 days)",
      "instructions": "special instructions (e.g., after food)",
      "source_snippet": "exact text from document"
    }}
  ]
}}

If no medicines found, return: {{"medicines": []}}"""

# Lab Value Extraction Prompt
LAB_EXTRACTION_PROMPT = """Extract all lab test results from the following medical report text.
Return ONLY valid JSON, no other text.

TEXT:
{text}

Return JSON in this exact format:
{{
  "lab_values": [
    {{
      "test_name": "name of the test",
      "value": "numeric value",
      "unit": "unit of measurement",
      "reference_range": "normal range if mentioned",
      "status": "Normal/High/Low if mentioned",
      "date": "test date if found",
      "source_snippet": "exact text from document"
    }}
  ]
}}

Common tests to look for: Hemoglobin, HbA1c, Glucose, Cholesterol, LDL, HDL, Triglycerides, Creatinine, Urea, SGPT, SGOT, TSH, WBC, Platelets, RBC, Bilirubin, etc.

If no lab values found, return: {{"lab_values": []}}"""

# Insurance Clause Extraction Prompt
INSURANCE_EXTRACTION_PROMPT = """Extract all important insurance policy clauses from the following document text.
Return ONLY valid JSON, no other text.

TEXT:
{text}

Return JSON in this exact format:
{{
  "clauses": [
    {{
      "clause_type": "waiting_period|room_rent_cap|copay|sublimit|exclusion|pre_existing_disease|claim_condition|network_hospital|other",
      "clause_text": "exact text from policy",
      "simple_meaning": "what this means in simple language",
      "financial_risk": "potential financial impact on patient",
      "severity": "Low|Medium|High",
      "question_to_ask": "question patient should ask insurer"
    }}
  ],
  "policy_summary": {{
    "sum_insured": "coverage amount if found",
    "policy_type": "individual/family floater/etc",
    "insurer_name": "insurance company name",
    "policy_number": "policy number if found"
  }}
}}

Key clauses to look for:
- Waiting periods (initial, specific diseases)
- Room rent caps (% of sum insured or fixed amount)
- Co-payment requirements
- Sub-limits on specific treatments
- Exclusions (permanent and temporary)
- Pre-existing disease clauses
- Network hospital requirements
- Claim process conditions

If no clauses found, return: {{"clauses": [], "policy_summary": {{}}}}"""

# Hospital Bill Extraction Prompt
BILL_EXTRACTION_PROMPT = """Extract all line items from the following hospital bill text.
Return ONLY valid JSON, no other text.

TEXT:
{text}

Return JSON in this exact format:
{{
  "bill_items": [
    {{
      "item_name": "name of the item/service",
      "category": "room|diagnostic|medicine|consumable|consultation|procedure|nursing|other",
      "quantity": "number of units",
      "unit_price": "price per unit (number only)",
      "total_amount": "total amount (number only)",
      "date": "date of service if found",
      "source_snippet": "exact text from bill"
    }}
  ],
  "bill_summary": {{
    "hospital_name": "hospital name",
    "patient_name": "patient name",
    "admission_date": "admission date",
    "discharge_date": "discharge date",
    "estimated_amount": "initial estimate if mentioned",
    "final_amount": "total bill amount",
    "deposit_paid": "advance deposit if mentioned",
    "balance_due": "remaining amount"
  }}
}}

Look for:
- Room charges (General ward, Private room, ICU)
- Diagnostic tests (X-ray, MRI, CT scan, blood tests, ECG)
- Medicines and pharmacy charges
- Consumables (gloves, syringes, IV sets)
- Doctor consultation fees
- Procedure/surgery charges
- Nursing charges
- Miscellaneous charges

If no items found, return: {{"bill_items": [], "bill_summary": {{}}}}"""

# Bill Risk Explanation Prompt
BILL_RISK_EXPLANATION_PROMPT = """You are a patient financial advisor. Explain these hospital bill concerns in simple, patient-friendly language.

IMPORTANT: 
- Do NOT accuse the hospital of fraud or wrongdoing
- Use careful language like "possible", "unusual", "may need verification", "worth asking about"
- Be helpful, not alarming
- Suggest polite questions to ask the billing department

FLAGGED ITEMS:
{flags}

BILL CONTEXT:
{bill_summary}

Provide your response in this format:

**Summary:** [Brief overview of concerns]

**Items to Review:**
[For each flagged item, explain why it was flagged and what question to ask]

**Suggested Questions for Billing Desk:**
[List of polite, specific questions]

**Important Note:** [Remind patient this is automated analysis and actual verification is needed]"""

# Discharge Summary Extraction Prompt
DISCHARGE_EXTRACTION_PROMPT = """Extract key medical information from this discharge summary.
Return ONLY valid JSON, no other text.

TEXT:
{text}

Return JSON in this exact format:
{{
  "patient_info": {{
    "name": "patient name",
    "age": "age",
    "gender": "gender",
    "admission_date": "date",
    "discharge_date": "date",
    "hospital": "hospital name"
  }},
  "diagnoses": [
    {{
      "diagnosis": "diagnosis name",
      "type": "primary|secondary",
      "icd_code": "code if mentioned"
    }}
  ],
  "procedures": [
    {{
      "procedure": "procedure name",
      "date": "date if mentioned"
    }}
  ],
  "medications_at_discharge": [
    {{
      "name": "medicine name",
      "dose": "dosage",
      "frequency": "how often",
      "duration": "how long"
    }}
  ],
  "follow_up": {{
    "instructions": "follow-up instructions",
    "next_visit": "next appointment date"
  }},
  "key_findings": ["list of important findings"]
}}

If information not found, use null for that field."""

# Doctor Summary Generation Prompt
DOCTOR_SUMMARY_PROMPT = """Generate a concise, professional summary for a doctor consultation based on the patient's uploaded documents and extracted information.

EXTRACTED INFORMATION:
{extracted_data}

Create a summary in this format:

**PATIENT HEALTH SUMMARY FOR DOCTOR CONSULTATION**

**Documents Reviewed:** [List of document types]

**Current Medications:**
[List all medicines with dosage]

**Recent Diagnoses:**
[List diagnoses from documents]

**Key Lab Results:**
[List abnormal or notable values]

**Insurance Coverage Notes:**
[Any relevant coverage limitations]

**Billing Concerns:**
[Any notable billing issues to discuss]

**Questions for Doctor:**
[Generate 3-5 relevant questions based on the documents]

**Important Dates:**
[Follow-up appointments, medication review dates]

---
*This summary was generated from uploaded documents and should be verified by the healthcare provider.*"""

# Patient Summary Prompt
PATIENT_SUMMARY_PROMPT = """Generate a simple, easy-to-understand health summary for the patient based on their uploaded documents.

EXTRACTED INFORMATION:
{extracted_data}

Create a friendly summary:

**YOUR HEALTH SUMMARY**

**What Documents We Reviewed:**
[Simple list]

**Your Current Medicines:**
[List with simple instructions]

**Your Recent Test Results:**
[Key values with simple explanations]

**Things to Remember:**
[Important points from documents]

**Insurance Points to Know:**
[Key coverage information]

**Questions You Might Want to Ask Your Doctor:**
[3-4 helpful questions]

**Questions for Your Insurance Company:**
[If applicable]

**Questions for Hospital Billing:**
[If applicable]

---
*Remember: This summary is based on your documents. Always consult your doctor for medical advice.*"""

# Lab Trend Analysis Prompt
LAB_TREND_ANALYSIS_PROMPT = """Analyze these lab test results and identify trends.

LAB VALUES OVER TIME:
{lab_data}

REFERENCE RANGES:
{reference_ranges}

Provide analysis:

**Lab Trend Analysis**

**Tests Analyzed:** [List of tests]

**Trends Identified:**
[For each test with multiple values, describe if improving, worsening, or stable]

**Values Outside Normal Range:**
[List any concerning values]

**Simple Explanation:**
[What these trends might mean in simple terms - without diagnosing]

**Suggested Discussion Points with Doctor:**
[Questions to ask about these results]

**Safety Note:** These trends are for informational purposes. Interpretation should be done by your healthcare provider."""

# Document Classification Prompt
DOCUMENT_CLASSIFICATION_PROMPT = """Classify this medical document into one of these categories:
- Prescription
- Lab Report
- Discharge Summary
- Insurance Policy
- Claim Document
- Hospital Bill
- Medical Certificate
- Other

TEXT:
{text}

Return ONLY the category name, nothing else."""
