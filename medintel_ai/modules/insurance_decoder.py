"""
MedIntel AI - Insurance Policy Decoder
"""
from typing import Dict, List, Optional
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modules.llm_client import call_llm, call_llm_json, check_llm_available
from modules.structured_extractor import extract_insurance_clauses
from modules.database import get_all_insurance_risks
from utils.config import INSURANCE_CLAUSE_TYPES


def decode_insurance_policy(text: str) -> Dict:
    """
    Decode and analyze an insurance policy document.
    
    Args:
        text: Policy document text
        
    Returns:
        Decoded policy information
    """
    result = {
        'clauses': [],
        'policy_summary': {},
        'risk_score': 0,
        'high_risk_clauses': [],
        'medium_risk_clauses': [],
        'low_risk_clauses': [],
        'questions_for_insurer': [],
        'overall_assessment': ''
    }
    
    # Extract clauses using LLM
    extraction = extract_insurance_clauses(text)
    
    if extraction:
        result['clauses'] = extraction.get('clauses', [])
        result['policy_summary'] = extraction.get('policy_summary', {})
    
    # Categorize by risk
    for clause in result['clauses']:
        severity = clause.get('severity', 'Medium')
        if severity == 'High':
            result['high_risk_clauses'].append(clause)
            result['risk_score'] += 3
        elif severity == 'Medium':
            result['medium_risk_clauses'].append(clause)
            result['risk_score'] += 2
        else:
            result['low_risk_clauses'].append(clause)
            result['risk_score'] += 1
        
        # Collect questions
        if clause.get('question_to_ask'):
            result['questions_for_insurer'].append(clause['question_to_ask'])
    
    # Generate overall assessment
    result['overall_assessment'] = generate_policy_assessment(result)
    
    return result


def detect_waiting_period(text: str) -> List[Dict]:
    """
    Detect waiting period clauses.
    
    Args:
        text: Policy text
        
    Returns:
        List of waiting period clauses
    """
    waiting_periods = []
    
    # Common patterns
    patterns = [
        r'waiting\s+period[:\s]+(\d+)\s*(days?|months?|years?)',
        r'(\d+)\s*(days?|months?|years?)\s+waiting\s+period',
        r'initial\s+waiting\s+period[:\s]+(\d+)',
        r'pre-existing\s+disease\s+waiting[:\s]+(\d+)',
    ]
    
    text_lower = text.lower()
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            period = match[0] if isinstance(match, tuple) else match
            unit = match[1] if isinstance(match, tuple) and len(match) > 1 else 'days'
            
            waiting_periods.append({
                'type': 'waiting_period',
                'duration': period,
                'unit': unit,
                'severity': 'High' if int(period) > 30 else 'Medium'
            })
    
    return waiting_periods


def detect_room_rent_cap(text: str) -> List[Dict]:
    """
    Detect room rent cap clauses.
    
    Args:
        text: Policy text
        
    Returns:
        List of room rent cap clauses
    """
    caps = []
    
    patterns = [
        r'room\s+rent[:\s]+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*)',
        r'room\s+rent\s+(?:cap|limit)[:\s]+(\d+)%',
        r'(\d+)%\s+of\s+sum\s+insured\s+(?:for\s+)?room',
    ]
    
    text_lower = text.lower()
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            caps.append({
                'type': 'room_rent_cap',
                'value': match,
                'severity': 'High',
                'explanation': 'Room rent cap may reduce your claim if you choose a higher category room.'
            })
    
    return caps


def detect_copay(text: str) -> List[Dict]:
    """
    Detect co-payment clauses.
    
    Args:
        text: Policy text
        
    Returns:
        List of copay clauses
    """
    copays = []
    
    patterns = [
        r'co-?pay(?:ment)?[:\s]+(\d+)%',
        r'(\d+)%\s+co-?pay',
        r'patient\s+(?:pays?|share)[:\s]+(\d+)%',
    ]
    
    text_lower = text.lower()
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            percentage = int(match)
            copays.append({
                'type': 'copay',
                'percentage': percentage,
                'severity': 'High' if percentage > 15 else 'Medium',
                'explanation': f'You need to pay {percentage}% of eligible claim amount from your pocket.'
            })
    
    return copays


def detect_exclusions(text: str) -> List[Dict]:
    """
    Detect policy exclusions.
    
    Args:
        text: Policy text
        
    Returns:
        List of exclusions
    """
    common_exclusions = [
        'cosmetic', 'dental', 'vision', 'maternity', 'infertility',
        'pre-existing', 'congenital', 'obesity', 'aids', 'hiv',
        'alcohol', 'drug abuse', 'self-inflicted', 'adventure sports',
        'war', 'nuclear', 'terrorism'
    ]
    
    exclusions = []
    text_lower = text.lower()
    
    # Look for exclusion section
    exclusion_section = re.search(r'exclusion[s]?[:\s]+([\s\S]{100,1000}?)(?:(?:terms|conditions|general|coverage)|\Z)', 
                                  text_lower)
    
    search_text = exclusion_section.group(1) if exclusion_section else text_lower
    
    for exc in common_exclusions:
        if exc in search_text:
            exclusions.append({
                'type': 'exclusion',
                'condition': exc,
                'severity': 'High' if exc in ['pre-existing', 'maternity'] else 'Medium',
                'explanation': f'{exc.title()} related conditions/treatments may not be covered.'
            })
    
    return exclusions


def explain_clause(clause: Dict) -> str:
    """
    Get detailed explanation of a clause using LLM.
    
    Args:
        clause: Clause dictionary
        
    Returns:
        Detailed explanation
    """
    if not check_llm_available():
        return clause.get('simple_meaning', 'Explanation not available.')
    
    prompt = f"""Explain this insurance clause in simple language for a patient:

Clause Type: {clause.get('clause_type', 'Unknown')}
Clause Text: {clause.get('clause_text', 'Not provided')}

Provide:
1. What this means in plain language
2. How it could affect the patient financially
3. Example scenario
4. One key question to ask the insurance company

Keep it simple and patient-friendly."""
    
    return call_llm(prompt)


def generate_policy_assessment(decoded: Dict) -> str:
    """
    Generate overall policy assessment.
    
    Args:
        decoded: Decoded policy dictionary
        
    Returns:
        Assessment text
    """
    high_count = len(decoded.get('high_risk_clauses', []))
    medium_count = len(decoded.get('medium_risk_clauses', []))
    total = len(decoded.get('clauses', []))
    
    if total == 0:
        return "No specific clauses were extracted. Please ensure the uploaded document is a clear insurance policy."
    
    if high_count == 0:
        assessment = "✅ **Good News:** No high-risk clauses were identified in your policy."
    elif high_count <= 2:
        assessment = "⚠️ **Attention Needed:** A few high-risk clauses were found that you should understand clearly."
    else:
        assessment = "🚨 **Review Carefully:** Multiple high-risk clauses were found. Understand these before making claims."
    
    assessment += f"\n\nFound {total} clauses: {high_count} high-risk, {medium_count} medium-risk."
    
    if decoded.get('questions_for_insurer'):
        assessment += f"\n\n📋 We've identified {len(decoded['questions_for_insurer'])} questions you should ask your insurer."
    
    return assessment


def generate_claim_risk_report(policy_data: Dict, treatment_type: str = None) -> Dict:
    """
    Generate a risk report for a potential claim.
    
    Args:
        policy_data: Decoded policy data
        treatment_type: Type of treatment being claimed
        
    Returns:
        Risk report
    """
    report = {
        'can_claim': True,
        'potential_risks': [],
        'estimated_coverage': 'Unknown',
        'deductions': [],
        'recommendations': []
    }
    
    # Check exclusions
    for clause in policy_data.get('clauses', []):
        if clause.get('clause_type') == 'exclusion':
            report['potential_risks'].append({
                'type': 'Exclusion',
                'description': clause.get('simple_meaning', ''),
                'impact': 'May not be covered'
            })
    
    # Check waiting period
    for clause in policy_data.get('clauses', []):
        if clause.get('clause_type') == 'waiting_period':
            report['potential_risks'].append({
                'type': 'Waiting Period',
                'description': clause.get('simple_meaning', ''),
                'impact': 'Check if waiting period has passed'
            })
    
    # Check copay
    for clause in policy_data.get('clauses', []):
        if clause.get('clause_type') == 'copay':
            report['deductions'].append({
                'type': 'Co-payment',
                'description': clause.get('simple_meaning', '')
            })
    
    # Check room rent
    for clause in policy_data.get('clauses', []):
        if clause.get('clause_type') == 'room_rent_cap':
            report['deductions'].append({
                'type': 'Room Rent Cap',
                'description': clause.get('simple_meaning', '')
            })
    
    # Generate recommendations
    if report['potential_risks']:
        report['recommendations'].append('Verify with your insurer before treatment if possible.')
    if report['deductions']:
        report['recommendations'].append('Factor in out-of-pocket costs due to copay or caps.')
    report['recommendations'].append('Keep all original bills and documents for claim submission.')
    
    return report


def get_insurance_summary() -> Dict:
    """
    Get summary of all insurance-related findings.
    
    Returns:
        Summary dictionary
    """
    all_risks = get_all_insurance_risks()
    
    summary = {
        'total_clauses': len(all_risks),
        'high_risk_count': sum(1 for r in all_risks if r.get('severity') == 'High'),
        'by_type': {},
        'key_concerns': [],
        'questions': []
    }
    
    for risk in all_risks:
        clause_type = risk.get('clause_type', 'other')
        if clause_type not in summary['by_type']:
            summary['by_type'][clause_type] = 0
        summary['by_type'][clause_type] += 1
        
        if risk.get('severity') == 'High':
            summary['key_concerns'].append({
                'type': clause_type,
                'text': risk.get('simple_meaning', '')
            })
        
        if risk.get('question_to_ask'):
            summary['questions'].append(risk['question_to_ask'])
    
    # Deduplicate questions
    summary['questions'] = list(set(summary['questions']))[:10]
    summary['key_concerns'] = summary['key_concerns'][:5]
    
    return summary
