"""
MedIntel AI - Lab Report Analyzer
"""
from typing import Dict, List, Optional, Tuple
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import LAB_REFERENCE_RANGES
from utils.helpers import normalize_lab_name, parse_date
from modules.llm_client import call_llm, check_llm_available
from modules.structured_extractor import extract_lab_values
from modules.database import get_all_lab_values, get_lab_values_by_test

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


def analyze_lab_value(test_name: str, value: float, unit: str = None) -> Dict:
    """
    Analyze a single lab value against reference ranges.
    
    Args:
        test_name: Name of the test
        value: Test value
        unit: Unit of measurement
        
    Returns:
        Analysis dictionary
    """
    normalized_name = normalize_lab_name(test_name)
    
    result = {
        'test_name': test_name,
        'normalized_name': normalized_name,
        'value': value,
        'unit': unit or '',
        'status': 'unknown',
        'reference_range': '',
        'explanation': '',
        'severity': 'unknown',
        'discussion_point': ''
    }
    
    # Check if we have reference range
    if normalized_name in LAB_REFERENCE_RANGES:
        ref = LAB_REFERENCE_RANGES[normalized_name]
        result['unit'] = unit or ref.get('unit', '')
        result['reference_range'] = f"{ref['min']} - {ref['max']} {ref.get('unit', '')}"
        
        # Determine status
        if value < ref['min']:
            result['status'] = 'low'
            deviation = ((ref['min'] - value) / ref['min']) * 100
            result['severity'] = 'critical' if deviation > 30 else 'moderate' if deviation > 15 else 'mild'
        elif value > ref['max']:
            result['status'] = 'high'
            deviation = ((value - ref['max']) / ref['max']) * 100
            result['severity'] = 'critical' if deviation > 30 else 'moderate' if deviation > 15 else 'mild'
        else:
            result['status'] = 'normal'
            result['severity'] = 'normal'
        
        # Generate explanation
        result['explanation'] = get_lab_explanation(normalized_name, result['status'], value)
        result['discussion_point'] = get_discussion_point(normalized_name, result['status'])
    
    return result


def get_lab_explanation(test_name: str, status: str, value: float) -> str:
    """Get simple explanation for a lab result."""
    explanations = {
        'hemoglobin': {
            'low': 'Your hemoglobin is below normal, which may indicate anemia. This can cause fatigue and weakness.',
            'high': 'Your hemoglobin is above normal. This could be due to dehydration or other conditions.',
            'normal': 'Your hemoglobin is within the normal range, indicating healthy red blood cell levels.'
        },
        'hba1c': {
            'low': 'Your HbA1c is low, suggesting good blood sugar control.',
            'high': 'Your HbA1c is elevated, indicating higher average blood sugar levels over the past 2-3 months.',
            'normal': 'Your HbA1c is in the normal range, suggesting good blood sugar control.'
        },
        'fasting_glucose': {
            'low': 'Your fasting glucose is low, which could indicate hypoglycemia.',
            'high': 'Your fasting glucose is elevated, which may indicate prediabetes or diabetes.',
            'normal': 'Your fasting glucose is normal, indicating healthy blood sugar regulation.'
        },
        'total_cholesterol': {
            'low': 'Your cholesterol is within healthy limits.',
            'high': 'Your total cholesterol is elevated, which may increase heart disease risk.',
            'normal': 'Your cholesterol is in the healthy range.'
        },
        'ldl': {
            'low': 'Your LDL (bad cholesterol) is at a healthy level.',
            'high': 'Your LDL cholesterol is elevated. LDL is often called "bad" cholesterol.',
            'normal': 'Your LDL cholesterol is in the optimal range.'
        },
        'hdl': {
            'low': 'Your HDL (good cholesterol) is below optimal. Higher HDL is generally better.',
            'high': 'Your HDL (good cholesterol) is high, which is typically beneficial.',
            'normal': 'Your HDL cholesterol is in a healthy range.'
        },
        'creatinine': {
            'low': 'Your creatinine is low, which is usually not concerning.',
            'high': 'Your creatinine is elevated, which may indicate kidney function issues.',
            'normal': 'Your creatinine is normal, suggesting healthy kidney function.'
        },
        'tsh': {
            'low': 'Your TSH is low, which may indicate an overactive thyroid.',
            'high': 'Your TSH is elevated, which may indicate an underactive thyroid.',
            'normal': 'Your TSH is normal, suggesting healthy thyroid function.'
        }
    }
    
    if test_name in explanations:
        return explanations[test_name].get(status, f'Your {test_name} value is {status}.')
    
    return f'Your {test_name} result is {status} compared to reference ranges.'


def get_discussion_point(test_name: str, status: str) -> str:
    """Get discussion point for doctor consultation."""
    if status == 'normal':
        return ''
    
    points = {
        'hemoglobin': 'Ask your doctor about possible causes of abnormal hemoglobin and if any dietary changes or supplements are needed.',
        'hba1c': 'Discuss your blood sugar management plan and if medication or lifestyle changes are needed.',
        'fasting_glucose': 'Ask about diabetes screening and lifestyle modifications for blood sugar control.',
        'total_cholesterol': 'Discuss heart health, diet modifications, and whether cholesterol medication is needed.',
        'ldl': 'Ask about strategies to lower LDL including diet, exercise, and possible medication.',
        'creatinine': 'Discuss kidney function and if any follow-up tests or lifestyle changes are needed.',
        'tsh': 'Ask about thyroid function and if thyroid medication adjustment is needed.'
    }
    
    return points.get(test_name, f'Discuss your {test_name} results and what they mean for your health.')


def analyze_lab_report(text: str) -> Dict:
    """
    Analyze a complete lab report.
    
    Args:
        text: Lab report text
        
    Returns:
        Complete analysis
    """
    # Extract lab values
    lab_values = extract_lab_values(text)
    
    analysis = {
        'total_tests': len(lab_values),
        'normal_count': 0,
        'abnormal_count': 0,
        'values': [],
        'abnormal_values': [],
        'summary': '',
        'discussion_points': []
    }
    
    for lab in lab_values:
        try:
            value = float(str(lab.get('value', 0)).replace(',', ''))
            result = analyze_lab_value(
                lab.get('test_name', ''),
                value,
                lab.get('unit', '')
            )
            result['date'] = lab.get('date', '')
            result['source_snippet'] = lab.get('source_snippet', '')
            
            analysis['values'].append(result)
            
            if result['status'] == 'normal':
                analysis['normal_count'] += 1
            elif result['status'] in ['high', 'low']:
                analysis['abnormal_count'] += 1
                analysis['abnormal_values'].append(result)
                if result['discussion_point']:
                    analysis['discussion_points'].append(result['discussion_point'])
        except:
            pass
    
    # Generate summary
    if analysis['abnormal_count'] > 0:
        analysis['summary'] = f"Found {analysis['abnormal_count']} value(s) outside normal range that may need attention."
    else:
        analysis['summary'] = "All extracted values appear to be within normal ranges."
    
    return analysis


def detect_lab_trends(test_name: str) -> Dict:
    """
    Detect trends in lab values over time.
    
    Args:
        test_name: Normalized test name
        
    Returns:
        Trend analysis
    """
    values = get_lab_values_by_test(test_name)
    
    trend = {
        'test_name': test_name,
        'data_points': len(values),
        'trend_direction': 'insufficient_data',
        'trend_explanation': '',
        'values': values,
        'chart': None
    }
    
    if len(values) < 2:
        trend['trend_explanation'] = 'Not enough data points to determine trend. Upload more reports with this test.'
        return trend
    
    if PANDAS_AVAILABLE:
        # Sort by date
        sorted_values = sorted(values, key=lambda x: x.get('report_date', ''))
        
        numeric_values = [v['value'] for v in sorted_values if v.get('value')]
        
        if len(numeric_values) >= 2:
            # Simple trend detection
            first_half = sum(numeric_values[:len(numeric_values)//2]) / (len(numeric_values)//2)
            second_half = sum(numeric_values[len(numeric_values)//2:]) / (len(numeric_values) - len(numeric_values)//2)
            
            if second_half > first_half * 1.1:
                trend['trend_direction'] = 'increasing'
                trend['trend_explanation'] = f'Your {test_name} values appear to be increasing over time.'
            elif second_half < first_half * 0.9:
                trend['trend_direction'] = 'decreasing'
                trend['trend_explanation'] = f'Your {test_name} values appear to be decreasing over time.'
            else:
                trend['trend_direction'] = 'stable'
                trend['trend_explanation'] = f'Your {test_name} values appear to be relatively stable.'
    
    return trend


def create_lab_trend_chart(test_name: str) -> Optional[object]:
    """
    Create a Plotly chart for lab value trends.
    
    Args:
        test_name: Test name to chart
        
    Returns:
        Plotly figure or None
    """
    if not PLOTLY_AVAILABLE or not PANDAS_AVAILABLE:
        return None
    
    values = get_lab_values_by_test(test_name)
    
    if len(values) < 2:
        return None
    
    # Prepare data
    dates = []
    test_values = []
    
    for v in values:
        if v.get('report_date') and v.get('value'):
            dates.append(v['report_date'])
            test_values.append(v['value'])
    
    if len(dates) < 2:
        return None
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=test_values,
        mode='lines+markers',
        name=test_name,
        line=dict(color='#0066CC', width=2),
        marker=dict(size=8)
    ))
    
    # Add reference range if available
    normalized = normalize_lab_name(test_name)
    if normalized in LAB_REFERENCE_RANGES:
        ref = LAB_REFERENCE_RANGES[normalized]
        fig.add_hline(y=ref['min'], line_dash="dash", line_color="orange", 
                     annotation_text="Low limit")
        fig.add_hline(y=ref['max'], line_dash="dash", line_color="red",
                     annotation_text="High limit")
    
    fig.update_layout(
        title=f'{test_name.title()} Trend Over Time',
        xaxis_title='Date',
        yaxis_title='Value',
        template='plotly_white',
        height=400
    )
    
    return fig


def generate_lab_insights(analysis: Dict) -> str:
    """
    Generate AI insights for lab analysis.
    
    Args:
        analysis: Lab analysis dictionary
        
    Returns:
        AI-generated insights
    """
    if not check_llm_available():
        return "AI insights not available. Please configure LLM API key."
    
    if not analysis.get('values'):
        return "No lab values to analyze."
    
    # Prepare prompt
    values_text = "\n".join([
        f"- {v['test_name']}: {v['value']} {v.get('unit', '')} (Status: {v['status']})"
        for v in analysis['values']
    ])
    
    prompt = f"""Analyze these lab results and provide patient-friendly insights:

Lab Values:
{values_text}

Provide:
1. Overall assessment (1-2 sentences)
2. Key findings that need attention
3. Positive findings
4. Suggested lifestyle considerations (if applicable)
5. Questions to discuss with doctor

Keep explanations simple and avoid medical jargon. Include a safety note that these are observations, not diagnoses."""
    
    return call_llm(prompt)


def get_comprehensive_lab_summary() -> Dict:
    """
    Get comprehensive summary of all lab values in the system.
    
    Returns:
        Summary dictionary
    """
    all_values = get_all_lab_values()
    
    summary = {
        'total_tests': len(all_values),
        'unique_tests': len(set(v['normalized_name'] for v in all_values if v.get('normalized_name'))),
        'abnormal_count': 0,
        'tests_by_category': {},
        'recent_abnormal': [],
        'tests_with_trends': []
    }
    
    # Group by test
    test_groups = {}
    for v in all_values:
        name = v.get('normalized_name', v.get('test_name', 'unknown'))
        if name not in test_groups:
            test_groups[name] = []
        test_groups[name].append(v)
    
    # Analyze each test
    for test_name, values in test_groups.items():
        if len(values) >= 2:
            summary['tests_with_trends'].append(test_name)
        
        for v in values:
            if v.get('status') in ['high', 'low']:
                summary['abnormal_count'] += 1
                summary['recent_abnormal'].append({
                    'test': test_name,
                    'value': v.get('value'),
                    'status': v.get('status'),
                    'date': v.get('report_date')
                })
    
    # Limit recent abnormal to last 10
    summary['recent_abnormal'] = summary['recent_abnormal'][:10]
    
    return summary
