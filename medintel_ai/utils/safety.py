"""
MedIntel AI - Safety Rules and Disclaimers
"""

# Emergency keywords to detect
EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "stroke", "unconscious", "not breathing",
    "severe bleeding", "seizure", "choking", "suicide", "overdose",
    "difficulty breathing", "shortness of breath", "paralysis",
    "severe allergic reaction", "anaphylaxis", "severe burn",
    "head injury", "loss of consciousness", "coughing blood",
    "severe abdominal pain", "high fever with confusion"
]

# Emergency Response
EMERGENCY_MESSAGE = """
⚠️ **EMERGENCY ALERT** ⚠️

If you or someone is experiencing:
- Severe chest pain or pressure
- Difficulty breathing or shortness of breath
- Signs of stroke (face drooping, arm weakness, speech difficulty)
- Loss of consciousness
- Severe bleeding that won't stop
- Severe allergic reaction
- Seizures
- Any life-threatening symptom

**PLEASE SEEK IMMEDIATE MEDICAL CARE**

📞 Call Emergency Services: **112** (India) or your local emergency number
🏥 Go to the nearest emergency room immediately

**This AI system is NOT a replacement for emergency medical services.**
"""

# Standard Medical Disclaimer
MEDICAL_DISCLAIMER = """
⚕️ **Medical Disclaimer**

MedIntel AI is an information assistance tool, NOT a medical device or service.

- This system does NOT diagnose diseases
- This system does NOT prescribe or recommend medications
- This system does NOT replace professional medical advice
- All medical decisions should be made with qualified healthcare providers

The information provided is based on your uploaded documents and AI interpretation. 
Always verify important medical information with your doctor.
"""

# Billing Disclaimer
BILLING_DISCLAIMER = """
💰 **Billing Analysis Disclaimer**

This analysis is automated and indicative only.

- Flagged items are suggestions for review, not accusations
- Actual billing verification should be done with the hospital
- Pricing comparisons are approximate benchmarks
- Medical necessity of services should be confirmed with your doctor

Please approach the hospital billing desk politely with any questions.
"""

# Insurance Disclaimer
INSURANCE_DISCLAIMER = """
📋 **Insurance Analysis Disclaimer**

This is a simplified interpretation of policy terms.

- Final claim decisions are made by the insurance company
- Policy terms may have specific definitions not captured here
- Always read your policy document carefully
- Contact your insurer for official clarifications
- Claim eligibility depends on many factors

For accurate information, contact your insurance provider directly.
"""

# Data Privacy Notice
PRIVACY_NOTICE = """
🔒 **Privacy Notice**

Your documents are processed locally and are not shared externally.

- Uploaded files are stored temporarily on this server
- AI processing uses secure API connections
- We recommend not uploading documents with unnecessary personal information
- You can delete your uploaded documents at any time

For sensitive medical information, review our privacy practices.
"""

# Safety Footer
SAFETY_FOOTER = """
---
*MedIntel AI is designed to help you understand your healthcare documents. 
It is not a substitute for professional medical advice, diagnosis, or treatment. 
Always consult with qualified healthcare providers for medical decisions.*
"""

def check_for_emergency(text: str) -> bool:
    """Check if text contains emergency keywords."""
    text_lower = text.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

def get_emergency_response() -> str:
    """Get emergency response message."""
    return EMERGENCY_MESSAGE

def get_medical_disclaimer() -> str:
    """Get standard medical disclaimer."""
    return MEDICAL_DISCLAIMER

def get_billing_disclaimer() -> str:
    """Get billing analysis disclaimer."""
    return BILLING_DISCLAIMER

def get_insurance_disclaimer() -> str:
    """Get insurance analysis disclaimer."""
    return INSURANCE_DISCLAIMER

def get_privacy_notice() -> str:
    """Get privacy notice."""
    return PRIVACY_NOTICE

def get_safety_footer() -> str:
    """Get safety footer."""
    return SAFETY_FOOTER

def add_safety_note(response: str, category: str = "medical") -> str:
    """Add appropriate safety note to a response."""
    disclaimers = {
        "medical": "\n\n---\n*⚕️ Medical information should be verified with your healthcare provider.*",
        "billing": "\n\n---\n*💰 Billing analysis is indicative. Please verify with the hospital.*",
        "insurance": "\n\n---\n*📋 Insurance interpretation is simplified. Contact your insurer for official terms.*",
        "general": "\n\n---\n*ℹ️ This information is based on your uploaded documents.*"
    }
    return response + disclaimers.get(category, disclaimers["general"])

def get_confidence_badge(confidence: str) -> str:
    """Get HTML badge for confidence level."""
    badges = {
        "high": '<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">✓ High Confidence</span>',
        "medium": '<span style="background-color: #ffc107; color: black; padding: 2px 8px; border-radius: 4px; font-size: 12px;">◐ Medium Confidence</span>',
        "low": '<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">◯ Low Confidence</span>'
    }
    return badges.get(confidence.lower(), badges["medium"])

def get_severity_badge(severity: str) -> str:
    """Get HTML badge for severity level."""
    badges = {
        "high": '<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">⚠️ High Risk</span>',
        "medium": '<span style="background-color: #ffc107; color: black; padding: 2px 8px; border-radius: 4px; font-size: 12px;">⚡ Medium Risk</span>',
        "low": '<span style="background-color: #17a2b8; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">ℹ️ Low Risk</span>'
    }
    return badges.get(severity.lower(), badges["medium"])

def get_status_badge(status: str) -> str:
    """Get HTML badge for lab value status."""
    badges = {
        "normal": '<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">✓ Normal</span>',
        "high": '<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">↑ High</span>',
        "low": '<span style="background-color: #ffc107; color: black; padding: 2px 8px; border-radius: 4px; font-size: 12px;">↓ Low</span>',
        "critical": '<span style="background-color: #721c24; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">⚠️ Critical</span>'
    }
    return badges.get(status.lower(), badges["normal"])
