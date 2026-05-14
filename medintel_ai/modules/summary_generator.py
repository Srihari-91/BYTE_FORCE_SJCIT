"""
MedIntel AI - Summary Generator
"""
from typing import Dict, List, Optional
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modules.llm_client import call_llm, check_llm_available
from modules.database import (
    get_all_documents, get_all_medicines, get_all_lab_values,
    get_all_insurance_risks, get_all_bill_risks, get_statistics
)
from utils.prompts import DOCTOR_SUMMARY_PROMPT, PATIENT_SUMMARY_PROMPT
from utils.safety import MEDICAL_DISCLAIMER, SAFETY_FOOTER


def generate_patient_summary() -> str:
    """
    Generate a patient-friendly summary.
    
    Returns:
        Summary text
    """
    # Gather all data
    data = gather_all_data()
    
    if not check_llm_available():
        return generate_simple_summary(data)
    
    # Format data for LLM
    data_text = format_data_for_prompt(data)
    
    prompt = PATIENT_SUMMARY_PROMPT.format(extracted_data=data_text)
    
    summary = call_llm(prompt)
    
    # Add safety note
    summary += "\n\n" + SAFETY_FOOTER
    
    return summary


def generate_doctor_summary() -> str:
    """
    Generate a professional summary for doctor consultation.
    
    Returns:
        Summary text
    """
    data = gather_all_data()
    
    if not check_llm_available():
        return generate_professional_summary(data)
    
    data_text = format_data_for_prompt(data)
    
    prompt = DOCTOR_SUMMARY_PROMPT.format(extracted_data=data_text)
    
    summary = call_llm(prompt)
    
    return summary


def generate_insurance_summary() -> str:
    """
    Generate summary for insurance-related findings.
    
    Returns:
        Summary text
    """
    risks = get_all_insurance_risks()
    
    if not risks:
        return "No insurance documents have been analyzed yet."
    
    summary = "## Insurance Policy Summary\n\n"
    
    # Group by severity
    high_risk = [r for r in risks if r.get('severity') == 'High']
    medium_risk = [r for r in risks if r.get('severity') == 'Medium']
    low_risk = [r for r in risks if r.get('severity') == 'Low']
    
    if high_risk:
        summary += "### ⚠️ High Priority Clauses\n\n"
        for risk in high_risk[:5]:
            summary += f"**{risk.get('clause_type', 'Unknown')}**\n"
            summary += f"- {risk.get('simple_meaning', 'No explanation available')}\n"
            summary += f"- Financial Risk: {risk.get('financial_risk', 'Unknown')}\n\n"
    
    if medium_risk:
        summary += "### ⚡ Medium Priority Clauses\n\n"
        for risk in medium_risk[:5]:
            summary += f"**{risk.get('clause_type', 'Unknown')}**\n"
            summary += f"- {risk.get('simple_meaning', 'No explanation available')}\n\n"
    
    # Questions to ask
    questions = set()
    for risk in risks:
        if risk.get('question_to_ask'):
            questions.add(risk['question_to_ask'])
    
    if questions:
        summary += "### 📋 Questions for Your Insurer\n\n"
        for i, q in enumerate(list(questions)[:8], 1):
            summary += f"{i}. {q}\n"
    
    summary += "\n\n---\n*This summary is based on AI analysis. Verify all information with your insurance provider.*"
    
    return summary


def generate_billing_summary() -> str:
    """
    Generate summary for billing-related findings.
    
    Returns:
        Summary text
    """
    risks = get_all_bill_risks()
    
    if not risks:
        return "No hospital bills have been analyzed yet."
    
    summary = "## Hospital Bill Analysis Summary\n\n"
    
    # Calculate totals
    total_flagged = sum(r.get('amount', 0) for r in risks)
    
    summary += f"**Items Flagged for Review:** {len(risks)}\n"
    summary += f"**Total Amount in Question:** ₹{total_flagged:,.2f}\n\n"
    
    # Group by severity
    high_risk = [r for r in risks if r.get('severity') == 'High']
    medium_risk = [r for r in risks if r.get('severity') == 'Medium']
    
    if high_risk:
        summary += "### 🔴 High Priority Items\n\n"
        for risk in high_risk[:5]:
            summary += f"- **{risk.get('item_name', 'Unknown')}** (₹{risk.get('amount', 0):,.0f})\n"
            summary += f"  {risk.get('reason', '')}\n\n"
    
    if medium_risk:
        summary += "### 🟡 Medium Priority Items\n\n"
        for risk in medium_risk[:5]:
            summary += f"- **{risk.get('item_name', 'Unknown')}** (₹{risk.get('amount', 0):,.0f})\n"
            summary += f"  {risk.get('reason', '')}\n\n"
    
    # Questions
    questions = set()
    for risk in risks:
        if risk.get('suggested_question'):
            questions.add(risk['suggested_question'])
    
    if questions:
        summary += "### 📋 Questions for Billing Desk\n\n"
        for i, q in enumerate(list(questions)[:6], 1):
            summary += f"{i}. {q}\n"
    
    summary += "\n\n---\n*This is an automated analysis. Please verify all concerns with the hospital billing department.*"
    
    return summary


def generate_questions_to_ask() -> Dict[str, List[str]]:
    """
    Generate categorized questions to ask healthcare providers.
    
    Returns:
        Dictionary of questions by category
    """
    questions = {
        'doctor': [],
        'insurer': [],
        'hospital_billing': [],
        'pharmacy': []
    }
    
    # Get all data
    medicines = get_all_medicines()
    lab_values = get_all_lab_values()
    insurance_risks = get_all_insurance_risks()
    bill_risks = get_all_bill_risks()
    
    # Doctor questions based on medicines and labs
    if medicines:
        med_names = list(set(m.get('name', '') for m in medicines if m.get('name')))[:5]
        questions['doctor'].append(f"I'm currently taking: {', '.join(med_names)}. Are there any interactions I should know about?")
    
    abnormal_labs = [l for l in lab_values if l.get('status') in ['high', 'low']]
    if abnormal_labs:
        for lab in abnormal_labs[:3]:
            questions['doctor'].append(f"My {lab.get('test_name', 'test')} was {lab.get('status', 'abnormal')}. What does this mean for my health?")
    
    questions['doctor'].append("Based on my records, are there any preventive measures I should take?")
    
    # Insurer questions
    for risk in insurance_risks:
        if risk.get('question_to_ask'):
            questions['insurer'].append(risk['question_to_ask'])
    questions['insurer'] = list(set(questions['insurer']))[:6]
    
    # Billing questions
    for risk in bill_risks:
        if risk.get('suggested_question'):
            questions['hospital_billing'].append(risk['suggested_question'])
    questions['hospital_billing'] = list(set(questions['hospital_billing']))[:6]
    
    if not questions['hospital_billing']:
        questions['hospital_billing'].append("Can I have a detailed itemized bill?")
    
    # Pharmacy questions
    if medicines:
        questions['pharmacy'].append("Are there generic alternatives available for my medicines?")
        questions['pharmacy'].append("Are there any special storage requirements for my medications?")
    
    return questions


def generate_final_case_summary() -> str:
    """
    Generate comprehensive final case summary.
    
    Returns:
        Complete summary
    """
    data = gather_all_data()
    stats = get_statistics()
    
    summary = f"""
# MedIntel AI - Complete Health Summary
Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}

---

## Overview

| Metric | Count |
|--------|-------|
| Documents Analyzed | {stats.get('total_documents', 0)} |
| Medical Facts Extracted | {stats.get('total_entities', 0)} |
| Lab Values Recorded | {stats.get('total_lab_values', 0)} |
| Insurance Clauses Found | {stats.get('total_insurance_risks', 0)} |
| Billing Items Reviewed | {stats.get('total_bill_risks', 0)} |
| Medicines Identified | {stats.get('total_medicines', 0)} |

---

## Documents Processed

"""
    
    for doc in data['documents'][:10]:
        summary += f"- **{doc.get('filename', 'Unknown')}** ({doc.get('document_type', 'Unknown')}) - {doc.get('upload_time', '')}\n"
    
    summary += "\n---\n\n## Current Medications\n\n"
    
    if data['medicines']:
        for med in data['medicines'][:10]:
            summary += f"- **{med.get('name', 'Unknown')}** {med.get('dose', '')} - {med.get('frequency', '')}\n"
    else:
        summary += "*No medications found in uploaded documents*\n"
    
    summary += "\n---\n\n## Lab Values Summary\n\n"
    
    if data['lab_values']:
        abnormal = [l for l in data['lab_values'] if l.get('status') in ['high', 'low']]
        if abnormal:
            summary += "### Values Outside Normal Range\n\n"
            for lab in abnormal[:10]:
                summary += f"- **{lab.get('test_name', 'Unknown')}**: {lab.get('value', '')} {lab.get('unit', '')} ({lab.get('status', '').upper()})\n"
        else:
            summary += "*All recorded values are within normal range*\n"
    else:
        summary += "*No lab values found in uploaded documents*\n"
    
    summary += "\n---\n\n## Insurance Considerations\n\n"
    
    if data['insurance_risks']:
        high_risk = [r for r in data['insurance_risks'] if r.get('severity') == 'High']
        if high_risk:
            summary += "### Key Clauses to Remember\n\n"
            for risk in high_risk[:5]:
                summary += f"- **{risk.get('clause_type', 'Unknown')}**: {risk.get('simple_meaning', '')}\n"
        else:
            summary += "*No high-risk insurance clauses identified*\n"
    else:
        summary += "*No insurance documents analyzed*\n"
    
    summary += "\n---\n\n## Billing Observations\n\n"
    
    if data['bill_risks']:
        summary += f"Found {len(data['bill_risks'])} items that may need verification.\n\n"
        for risk in data['bill_risks'][:5]:
            summary += f"- **{risk.get('item_name', 'Unknown')}**: {risk.get('reason', '')}\n"
    else:
        summary += "*No billing concerns identified*\n"
    
    summary += f"""
---

## Important Reminders

1. This summary is generated by AI and should be verified with healthcare professionals
2. Always consult your doctor before making medical decisions
3. Verify insurance claims with your insurer
4. Discuss billing concerns politely with the hospital

---

{MEDICAL_DISCLAIMER}

---

*Generated by MedIntel AI - Your Medical Memory, Insurance Decoder, and Hospital Bill Watchdog*
"""
    
    return summary


def gather_all_data() -> Dict:
    """Gather all data from database."""
    return {
        'documents': get_all_documents(),
        'medicines': get_all_medicines(),
        'lab_values': get_all_lab_values(),
        'insurance_risks': get_all_insurance_risks(),
        'bill_risks': get_all_bill_risks(),
        'statistics': get_statistics()
    }


def format_data_for_prompt(data: Dict) -> str:
    """Format gathered data for LLM prompt."""
    text = ""
    
    if data['documents']:
        text += f"Documents: {len(data['documents'])} uploaded\n"
        for doc in data['documents'][:5]:
            text += f"- {doc.get('filename', '')} ({doc.get('document_type', '')})\n"
    
    if data['medicines']:
        text += f"\nMedicines ({len(data['medicines'])}):\n"
        for med in data['medicines'][:10]:
            text += f"- {med.get('name', '')} {med.get('dose', '')} {med.get('frequency', '')}\n"
    
    if data['lab_values']:
        text += f"\nLab Values ({len(data['lab_values'])}):\n"
        for lab in data['lab_values'][:10]:
            text += f"- {lab.get('test_name', '')}: {lab.get('value', '')} {lab.get('unit', '')} ({lab.get('status', 'unknown')})\n"
    
    if data['insurance_risks']:
        text += f"\nInsurance Findings ({len(data['insurance_risks'])}):\n"
        for risk in data['insurance_risks'][:5]:
            text += f"- {risk.get('clause_type', '')}: {risk.get('simple_meaning', '')}\n"
    
    if data['bill_risks']:
        text += f"\nBilling Concerns ({len(data['bill_risks'])}):\n"
        for risk in data['bill_risks'][:5]:
            text += f"- {risk.get('item_name', '')}: {risk.get('reason', '')}\n"
    
    return text


def generate_simple_summary(data: Dict) -> str:
    """Generate simple summary without LLM."""
    summary = "# Your Health Summary\n\n"
    
    summary += f"## Documents Analyzed: {len(data['documents'])}\n\n"
    
    if data['medicines']:
        summary += "## Your Medicines\n"
        for med in data['medicines'][:10]:
            summary += f"- {med.get('name', 'Unknown')} {med.get('dose', '')}\n"
        summary += "\n"
    
    if data['lab_values']:
        summary += "## Your Lab Results\n"
        for lab in data['lab_values'][:10]:
            summary += f"- {lab.get('test_name', 'Unknown')}: {lab.get('value', '')} ({lab.get('status', 'unknown')})\n"
        summary += "\n"
    
    summary += SAFETY_FOOTER
    
    return summary


def generate_professional_summary(data: Dict) -> str:
    """Generate professional summary without LLM."""
    return f"""
PATIENT HEALTH SUMMARY
Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}

DOCUMENTS REVIEWED: {len(data['documents'])}
MEDICATIONS: {len(data['medicines'])}
LAB VALUES: {len(data['lab_values'])}
INSURANCE CLAUSES: {len(data['insurance_risks'])}
BILLING ITEMS: {len(data['bill_risks'])}

---
This summary is for informational purposes only.
Please verify all information with appropriate healthcare providers.
"""
