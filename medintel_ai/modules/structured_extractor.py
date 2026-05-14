"""
MedIntel AI - LLM-based Structured Data Extraction
"""
import re
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modules.llm_client import call_llm_json, call_llm, check_llm_available
from utils.prompts import (
    MEDICINE_EXTRACTION_PROMPT,
    LAB_EXTRACTION_PROMPT,
    INSURANCE_EXTRACTION_PROMPT,
    BILL_EXTRACTION_PROMPT,
    DISCHARGE_EXTRACTION_PROMPT
)
from utils.helpers import safe_json_parse, normalize_lab_name


def extract_medicines(text: str) -> List[Dict]:
    """
    Extract medicines from prescription/discharge text using LLM.
    
    Args:
        text: Document text
        
    Returns:
        List of medicine dictionaries
    """
    if not check_llm_available():
        return fallback_extract_medicines(text)
    
    prompt = MEDICINE_EXTRACTION_PROMPT.format(text=text[:8000])
    result = call_llm_json(prompt)
    
    if result and 'medicines' in result:
        return result['medicines']
    
    # Fallback to regex extraction
    return fallback_extract_medicines(text)


def fallback_extract_medicines(text: str) -> List[Dict]:
    """
    Fallback regex-based medicine extraction.
    
    Args:
        text: Document text
        
    Returns:
        List of medicine dictionaries
    """
    medicines = []
    
    # Common medicine patterns
    patterns = [
        # Pattern: Medicine Name Dose Frequency
        r'(?:Tab|Cap|Syrup|Inj|Cream|Ointment)?\.?\s*([A-Za-z][A-Za-z0-9\-]+(?:\s+[A-Za-z]+)?)\s+(\d+(?:\.\d+)?\s*(?:mg|ml|g|mcg|iu)?)\s*[-–]?\s*(\d+[-–]\d+[-–]\d+|once|twice|thrice|daily|bd|tds|qid|od|hs|sos|prn)',
    ]
    
    text_lower = text.lower()
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) >= 2:
                medicines.append({
                    'name': match[0].strip(),
                    'dose': match[1].strip() if len(match) > 1 else '',
                    'frequency': match[2].strip() if len(match) > 2 else '',
                    'duration': '',
                    'instructions': '',
                    'source_snippet': ' '.join(match)
                })
    
    return medicines


def extract_lab_values(text: str) -> List[Dict]:
    """
    Extract lab test values from report text using LLM.
    
    Args:
        text: Document text
        
    Returns:
        List of lab value dictionaries
    """
    if not check_llm_available():
        return fallback_extract_lab_values(text)
    
    prompt = LAB_EXTRACTION_PROMPT.format(text=text[:8000])
    result = call_llm_json(prompt)
    
    if result and 'lab_values' in result:
        # Normalize test names
        for value in result['lab_values']:
            if 'test_name' in value:
                value['normalized_name'] = normalize_lab_name(value['test_name'])
        return result['lab_values']
    
    return fallback_extract_lab_values(text)


def fallback_extract_lab_values(text: str) -> List[Dict]:
    """
    Fallback regex-based lab value extraction.
    
    Args:
        text: Document text
        
    Returns:
        List of lab value dictionaries
    """
    lab_values = []
    
    # Common lab test patterns
    test_patterns = {
        'hemoglobin': r'(?:hemoglobin|hb|hgb)[:\s]+(\d+\.?\d*)\s*(g/dl|g%)?',
        'hba1c': r'(?:hba1c|glycated\s+hemo)[:\s]+(\d+\.?\d*)\s*(%)?',
        'glucose': r'(?:glucose|sugar|fbs|rbs)[:\s]+(\d+\.?\d*)\s*(mg/dl)?',
        'cholesterol': r'(?:total\s+cholesterol|tc)[:\s]+(\d+\.?\d*)\s*(mg/dl)?',
        'creatinine': r'(?:creatinine|creat)[:\s]+(\d+\.?\d*)\s*(mg/dl)?',
        'tsh': r'(?:tsh)[:\s]+(\d+\.?\d*)\s*(miu/l|uiu/ml)?',
    }
    
    text_lower = text.lower()
    
    for test_name, pattern in test_patterns.items():
        matches = re.findall(pattern, text_lower)
        for match in matches:
            lab_values.append({
                'test_name': test_name,
                'normalized_name': test_name,
                'value': match[0] if match else '',
                'unit': match[1] if len(match) > 1 else '',
                'reference_range': '',
                'status': '',
                'date': '',
                'source_snippet': match[0] if match else ''
            })
    
    return lab_values


def extract_insurance_clauses(text: str) -> Dict:
    """
    Extract insurance policy clauses using LLM.
    
    Args:
        text: Policy document text
        
    Returns:
        Dictionary with clauses and policy summary
    """
    if not check_llm_available():
        return {'clauses': [], 'policy_summary': {}}
    
    prompt = INSURANCE_EXTRACTION_PROMPT.format(text=text[:10000])
    result = call_llm_json(prompt)
    
    if result:
        return result
    
    return {'clauses': [], 'policy_summary': {}}


def extract_bill_items(text: str) -> Dict:
    """
    Extract hospital bill line items using LLM.
    
    Args:
        text: Bill document text
        
    Returns:
        Dictionary with bill_items and bill_summary
    """
    if not check_llm_available():
        return fallback_extract_bill_items(text)
    
    prompt = BILL_EXTRACTION_PROMPT.format(text=text[:10000])
    result = call_llm_json(prompt)
    
    if result:
        return result
    
    return fallback_extract_bill_items(text)


def fallback_extract_bill_items(text: str) -> Dict:
    """
    Fallback regex-based bill item extraction.
    
    Args:
        text: Bill text
        
    Returns:
        Dictionary with bill items
    """
    bill_items = []
    
    # Look for amount patterns
    amount_pattern = r'([A-Za-z][A-Za-z\s]+)[\s:]+(?:Rs\.?|₹)?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
    
    matches = re.findall(amount_pattern, text)
    for match in matches:
        item_name = match[0].strip()
        amount = match[1].replace(',', '')
        
        # Filter out obvious non-items
        if len(item_name) > 3 and len(item_name) < 50:
            try:
                bill_items.append({
                    'item_name': item_name,
                    'category': 'other',
                    'quantity': '1',
                    'unit_price': amount,
                    'total_amount': amount,
                    'date': '',
                    'source_snippet': f"{item_name}: {amount}"
                })
            except:
                pass
    
    # Try to find total
    total_pattern = r'(?:total|grand\s+total|net\s+amount)[:\s]+(?:Rs\.?|₹)?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
    total_match = re.search(total_pattern, text, re.IGNORECASE)
    
    bill_summary = {}
    if total_match:
        bill_summary['final_amount'] = total_match.group(1).replace(',', '')
    
    return {
        'bill_items': bill_items,
        'bill_summary': bill_summary
    }


def extract_discharge_summary(text: str) -> Dict:
    """
    Extract structured information from discharge summary.
    
    Args:
        text: Discharge summary text
        
    Returns:
        Structured discharge information
    """
    if not check_llm_available():
        return {}
    
    prompt = DISCHARGE_EXTRACTION_PROMPT.format(text=text[:10000])
    result = call_llm_json(prompt)
    
    return result if result else {}


def extract_all_entities(text: str, document_type: str) -> Dict:
    """
    Extract all relevant entities based on document type.
    
    Args:
        text: Document text
        document_type: Type of document
        
    Returns:
        Dictionary of all extracted entities
    """
    entities = {
        'document_type': document_type,
        'medicines': [],
        'lab_values': [],
        'diagnoses': [],
        'insurance_clauses': [],
        'bill_items': [],
        'bill_summary': {},
        'raw_extraction': {}
    }
    
    if document_type == 'Prescription':
        entities['medicines'] = extract_medicines(text)
    
    elif document_type == 'Lab Report':
        entities['lab_values'] = extract_lab_values(text)
    
    elif document_type == 'Discharge Summary':
        discharge_data = extract_discharge_summary(text)
        if discharge_data:
            entities['raw_extraction'] = discharge_data
            entities['medicines'] = discharge_data.get('medications_at_discharge', [])
            entities['diagnoses'] = discharge_data.get('diagnoses', [])
    
    elif document_type == 'Insurance Policy':
        insurance_data = extract_insurance_clauses(text)
        entities['insurance_clauses'] = insurance_data.get('clauses', [])
        entities['raw_extraction'] = insurance_data
    
    elif document_type == 'Hospital Bill':
        bill_data = extract_bill_items(text)
        entities['bill_items'] = bill_data.get('bill_items', [])
        entities['bill_summary'] = bill_data.get('bill_summary', {})
    
    else:
        # Try to extract common entities from any document
        entities['medicines'] = extract_medicines(text)
        entities['lab_values'] = extract_lab_values(text)
    
    return entities


def validate_extraction(entities: Dict) -> Dict:
    """
    Validate and clean extracted entities.
    
    Args:
        entities: Extracted entities dictionary
        
    Returns:
        Validated entities
    """
    # Validate medicines
    valid_medicines = []
    for med in entities.get('medicines', []):
        if med.get('name') and len(med['name']) > 2:
            valid_medicines.append(med)
    entities['medicines'] = valid_medicines
    
    # Validate lab values
    valid_labs = []
    for lab in entities.get('lab_values', []):
        if lab.get('test_name') and lab.get('value'):
            try:
                float(str(lab['value']).replace(',', ''))
                valid_labs.append(lab)
            except:
                pass
    entities['lab_values'] = valid_labs
    
    # Validate bill items
    valid_items = []
    for item in entities.get('bill_items', []):
        if item.get('item_name') and item.get('total_amount'):
            try:
                amount = float(str(item['total_amount']).replace(',', ''))
                if amount > 0:
                    item['total_amount'] = amount
                    valid_items.append(item)
            except:
                pass
    entities['bill_items'] = valid_items
    
    return entities
