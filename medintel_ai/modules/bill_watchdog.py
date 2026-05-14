"""
MedIntel AI - Hospital Bill Watchdog
"""
from typing import Dict, List, Optional, Tuple
from collections import Counter
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import BILL_BENCHMARKS
from utils.helpers import normalize_bill_item, extract_amount
from modules.llm_client import call_llm, check_llm_available
from modules.structured_extractor import extract_bill_items
from modules.database import get_all_bill_risks, get_all_bill_items
from utils.prompts import BILL_RISK_EXPLANATION_PROMPT

try:
    from sklearn.ensemble import IsolationForest
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def analyze_hospital_bill(text: str) -> Dict:
    """
    Comprehensive hospital bill analysis.
    
    Args:
        text: Bill document text
        
    Returns:
        Complete analysis with risk flags
    """
    result = {
        'bill_items': [],
        'bill_summary': {},
        'risk_flags': [],
        'risk_score': 0,
        'total_amount': 0,
        'category_totals': {},
        'duplicate_items': [],
        'high_cost_items': [],
        'unusual_items': [],
        'questions_for_billing': [],
        'overall_assessment': '',
        'ai_explanation': ''
    }
    
    # Extract bill items using LLM
    extraction = extract_bill_items(text)
    
    if extraction:
        result['bill_items'] = extraction.get('bill_items', [])
        result['bill_summary'] = extraction.get('bill_summary', {})
    
    # If no items extracted, return early
    if not result['bill_items']:
        result['overall_assessment'] = "Could not extract bill items. Please ensure the document is a clear hospital bill."
        return result
    
    # Calculate totals
    for item in result['bill_items']:
        try:
            amount = float(str(item.get('total_amount', 0)).replace(',', ''))
            item['total_amount'] = amount
            result['total_amount'] += amount
            
            category = item.get('category', 'other')
            if category not in result['category_totals']:
                result['category_totals'][category] = 0
            result['category_totals'][category] += amount
        except:
            pass
    
    # Run all detection algorithms
    result['duplicate_items'] = detect_duplicate_items(result['bill_items'])
    result['high_cost_items'] = detect_high_cost_items(result['bill_items'])
    result['unusual_items'] = detect_unusual_charges(result['bill_items'])
    
    # Compile all risk flags
    for dup in result['duplicate_items']:
        result['risk_flags'].append({
            'type': 'Possible Duplicate',
            'item': dup['item_name'],
            'severity': 'Medium',
            'reason': f"Item '{dup['item_name']}' appears {dup['count']} times",
            'amount': dup.get('total_amount', 0)
        })
        result['risk_score'] += 2
    
    for high in result['high_cost_items']:
        result['risk_flags'].append({
            'type': 'Higher Than Benchmark',
            'item': high['item_name'],
            'severity': 'Medium',
            'reason': high['reason'],
            'amount': high.get('amount', 0)
        })
        result['risk_score'] += 2
    
    for unusual in result['unusual_items']:
        result['risk_flags'].append({
            'type': 'Unusual Charge',
            'item': unusual['item_name'],
            'severity': unusual.get('severity', 'Low'),
            'reason': unusual['reason'],
            'amount': unusual.get('amount', 0)
        })
        result['risk_score'] += 1
    
    # Check estimate vs final
    if result['bill_summary'].get('estimated_amount') and result['bill_summary'].get('final_amount'):
        estimate_check = compare_estimate_vs_final(
            result['bill_summary']['estimated_amount'],
            result['bill_summary']['final_amount']
        )
        if estimate_check:
            result['risk_flags'].append(estimate_check)
            result['risk_score'] += 3
    
    # Optional: ML-based anomaly detection
    if SKLEARN_AVAILABLE and len(result['bill_items']) >= 5:
        ml_anomalies = detect_anomalies_ml(result['bill_items'])
        for anomaly in ml_anomalies:
            result['risk_flags'].append(anomaly)
            result['risk_score'] += 1
    
    # Generate questions
    result['questions_for_billing'] = generate_billing_questions(result['risk_flags'])
    
    # Generate assessment
    result['overall_assessment'] = generate_bill_assessment(result)
    
    # Get AI explanation
    if result['risk_flags'] and check_llm_available():
        result['ai_explanation'] = explain_bill_risks(result['risk_flags'], result['bill_summary'])
    
    return result


def detect_duplicate_items(items: List[Dict]) -> List[Dict]:
    """
    Detect potentially duplicate bill items.
    
    Args:
        items: List of bill items
        
    Returns:
        List of potential duplicates
    """
    duplicates = []
    
    # Group by item name (normalized)
    item_counts = Counter()
    item_totals = {}
    
    for item in items:
        name = normalize_bill_item(item.get('item_name', ''))
        amount = item.get('total_amount', 0)
        date = item.get('date', '')
        
        key = f"{name}_{date}" if date else name
        item_counts[key] += 1
        
        if key not in item_totals:
            item_totals[key] = {'count': 0, 'total': 0, 'name': item.get('item_name', '')}
        item_totals[key]['count'] += 1
        item_totals[key]['total'] += amount
    
    # Flag items appearing multiple times
    for key, data in item_totals.items():
        if data['count'] > 1:
            # Some items are legitimately repeated (daily charges, medicines)
            if not any(x in key.lower() for x in ['room', 'nursing', 'bed', 'diet']):
                duplicates.append({
                    'item_name': data['name'],
                    'count': data['count'],
                    'total_amount': data['total']
                })
    
    return duplicates


def detect_high_cost_items(items: List[Dict]) -> List[Dict]:
    """
    Detect items priced higher than benchmarks.
    
    Args:
        items: List of bill items
        
    Returns:
        List of high-cost items
    """
    high_cost = []
    
    for item in items:
        name = normalize_bill_item(item.get('item_name', ''))
        amount = item.get('total_amount', 0)
        
        if name in BILL_BENCHMARKS:
            benchmark = BILL_BENCHMARKS[name]
            if amount > benchmark['max']:
                high_cost.append({
                    'item_name': item.get('item_name', ''),
                    'amount': amount,
                    'benchmark_max': benchmark['max'],
                    'reason': f"Charged ₹{amount:,.0f} vs typical max ₹{benchmark['max']:,.0f}"
                })
    
    return high_cost


def detect_unusual_charges(items: List[Dict]) -> List[Dict]:
    """
    Detect unusual or suspicious charges.
    
    Args:
        items: List of bill items
        
    Returns:
        List of unusual items
    """
    unusual = []
    
    # Check for excessive consumables
    consumable_total = sum(
        item.get('total_amount', 0) 
        for item in items 
        if item.get('category') == 'consumable'
    )
    
    total = sum(item.get('total_amount', 0) for item in items)
    
    if total > 0 and consumable_total / total > 0.2:
        unusual.append({
            'item_name': 'Consumables Total',
            'amount': consumable_total,
            'reason': f'Consumables are {consumable_total/total*100:.1f}% of total bill, which is higher than typical',
            'severity': 'Medium'
        })
    
    # Check for round numbers (potential padding)
    for item in items:
        amount = item.get('total_amount', 0)
        if amount >= 1000 and amount % 1000 == 0:
            # Could be legitimate, just flag for review
            pass
    
    # Check for very small repeated charges
    small_charges = [i for i in items if 0 < i.get('total_amount', 0) < 100]
    if len(small_charges) > 10:
        total_small = sum(i.get('total_amount', 0) for i in small_charges)
        unusual.append({
            'item_name': 'Multiple Small Charges',
            'amount': total_small,
            'reason': f'{len(small_charges)} items under ₹100 totaling ₹{total_small:.0f}',
            'severity': 'Low'
        })
    
    return unusual


def compare_estimate_vs_final(estimate: float, final: float) -> Optional[Dict]:
    """
    Compare initial estimate with final bill.
    
    Args:
        estimate: Estimated amount
        final: Final bill amount
        
    Returns:
        Risk flag if significant difference
    """
    try:
        estimate = float(str(estimate).replace(',', ''))
        final = float(str(final).replace(',', ''))
        
        if estimate <= 0:
            return None
        
        difference = final - estimate
        percentage = (difference / estimate) * 100
        
        if percentage > 20:
            return {
                'type': 'Estimate Mismatch',
                'item': 'Total Bill',
                'severity': 'High' if percentage > 50 else 'Medium',
                'reason': f'Final bill (₹{final:,.0f}) is {percentage:.1f}% higher than estimate (₹{estimate:,.0f})',
                'amount': difference
            }
    except:
        pass
    
    return None


def detect_anomalies_ml(items: List[Dict]) -> List[Dict]:
    """
    Use ML (Isolation Forest) to detect anomalous charges.
    
    Args:
        items: List of bill items
        
    Returns:
        List of anomalous items
    """
    if not SKLEARN_AVAILABLE or len(items) < 5:
        return []
    
    anomalies = []
    
    try:
        # Prepare features
        amounts = np.array([item.get('total_amount', 0) for item in items]).reshape(-1, 1)
        
        # Fit Isolation Forest
        clf = IsolationForest(contamination=0.1, random_state=42)
        predictions = clf.fit_predict(amounts)
        
        # Get anomalies
        for i, pred in enumerate(predictions):
            if pred == -1:  # Anomaly
                anomalies.append({
                    'type': 'Statistical Anomaly',
                    'item': items[i].get('item_name', 'Unknown'),
                    'severity': 'Low',
                    'reason': f"Amount (₹{items[i].get('total_amount', 0):,.0f}) is statistically unusual compared to other items",
                    'amount': items[i].get('total_amount', 0)
                })
    except:
        pass
    
    return anomalies[:3]  # Limit to top 3


def generate_billing_questions(risk_flags: List[Dict]) -> List[str]:
    """
    Generate questions to ask the billing department.
    
    Args:
        risk_flags: List of risk flags
        
    Returns:
        List of questions
    """
    questions = []
    
    for flag in risk_flags:
        flag_type = flag.get('type', '')
        item = flag.get('item', '')
        
        if 'Duplicate' in flag_type:
            questions.append(f"Can you explain why '{item}' appears multiple times on the bill?")
        elif 'Benchmark' in flag_type or 'Higher' in flag_type:
            questions.append(f"Can you provide a breakdown of the charges for '{item}'?")
        elif 'Estimate' in flag_type:
            questions.append("Can you explain why the final bill is significantly higher than the initial estimate?")
        elif 'Consumable' in flag_type:
            questions.append("Can I see a detailed list of all consumables charged?")
        elif 'Anomaly' in flag_type:
            questions.append(f"Can you verify the charge for '{item}'?")
    
    # Add general questions
    if questions:
        questions.append("Can I have an itemized bill with all charges explained?")
    
    return list(set(questions))[:8]


def generate_bill_assessment(analysis: Dict) -> str:
    """
    Generate overall bill assessment.
    
    Args:
        analysis: Bill analysis dictionary
        
    Returns:
        Assessment text
    """
    risk_score = analysis.get('risk_score', 0)
    flag_count = len(analysis.get('risk_flags', []))
    total = analysis.get('total_amount', 0)
    
    if flag_count == 0:
        assessment = "✅ **Good News:** No concerning patterns were detected in your bill."
    elif risk_score < 5:
        assessment = "ℹ️ **Minor Observations:** A few items may be worth verifying with the billing desk."
    elif risk_score < 10:
        assessment = "⚠️ **Review Recommended:** Some charges need clarification before payment."
    else:
        assessment = "🔍 **Detailed Review Needed:** Multiple items require verification with the hospital."
    
    assessment += f"\n\n**Total Bill:** ₹{total:,.2f}"
    assessment += f"\n**Items Flagged:** {flag_count}"
    
    if analysis.get('category_totals'):
        assessment += "\n\n**Breakdown by Category:**"
        for cat, amount in sorted(analysis['category_totals'].items(), key=lambda x: x[1], reverse=True):
            if amount > 0:
                assessment += f"\n- {cat.title()}: ₹{amount:,.2f}"
    
    return assessment


def explain_bill_risks(flags: List[Dict], summary: Dict) -> str:
    """
    Get AI explanation of bill risks.
    
    Args:
        flags: Risk flags
        summary: Bill summary
        
    Returns:
        AI explanation
    """
    if not check_llm_available():
        return "AI explanation not available. Please configure LLM API key."
    
    flags_text = "\n".join([
        f"- {f['type']}: {f.get('item', 'N/A')} - {f.get('reason', '')}"
        for f in flags
    ])
    
    summary_text = f"""
Hospital: {summary.get('hospital_name', 'Unknown')}
Patient: {summary.get('patient_name', 'Unknown')}
Admission: {summary.get('admission_date', 'Unknown')}
Discharge: {summary.get('discharge_date', 'Unknown')}
Total: {summary.get('final_amount', 'Unknown')}
"""
    
    prompt = BILL_RISK_EXPLANATION_PROMPT.format(
        flags=flags_text,
        bill_summary=summary_text
    )
    
    return call_llm(prompt)


def get_bill_summary() -> Dict:
    """
    Get summary of all bill-related findings.
    
    Returns:
        Summary dictionary
    """
    all_risks = get_all_bill_risks()
    all_items = get_all_bill_items()
    
    summary = {
        'total_items': len(all_items),
        'total_risks': len(all_risks),
        'total_amount': sum(item.get('total_amount', 0) for item in all_items),
        'high_risk_count': sum(1 for r in all_risks if r.get('severity') == 'High'),
        'risk_types': {},
        'top_risks': []
    }
    
    for risk in all_risks:
        risk_type = risk.get('risk_type', 'other')
        if risk_type not in summary['risk_types']:
            summary['risk_types'][risk_type] = 0
        summary['risk_types'][risk_type] += 1
    
    # Get top risks
    summary['top_risks'] = sorted(
        all_risks, 
        key=lambda x: {'High': 3, 'Medium': 2, 'Low': 1}.get(x.get('severity', 'Low'), 0),
        reverse=True
    )[:5]
    
    return summary
