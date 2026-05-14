"""
MedIntel AI - Reusable UI Components
"""
import streamlit as st
from typing import Dict, List, Optional, Any

def inject_custom_css():
    """Inject custom CSS for premium UI."""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #0066CC;
        --secondary-color: #00A8A8;
        --success-color: #28A745;
        --warning-color: #FFC107;
        --danger-color: #DC3545;
        --info-color: #17A2B8;
        --light-bg: #F8F9FA;
        --dark-text: #343A40;
        --gradient-start: #667eea;
        --gradient-end: #764ba2;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .custom-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border: 1px solid #E9ECEF;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    .card-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--dark-text);
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-content {
        color: #6C757D;
        line-height: 1.6;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.25rem;
        color: white;
        text-align: center;
    }
    
    .metric-card.blue {
        background: linear-gradient(135deg, #0066CC 0%, #0099FF 100%);
    }
    
    .metric-card.green {
        background: linear-gradient(135deg, #28A745 0%, #34D058 100%);
    }
    
    .metric-card.orange {
        background: linear-gradient(135deg, #FD7E14 0%, #FFC107 100%);
    }
    
    .metric-card.red {
        background: linear-gradient(135deg, #DC3545 0%, #FF6B6B 100%);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    
    .metric-label {
        font-size: 0.875rem;
        opacity: 0.9;
        margin-top: 0.25rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #E9ECEF;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: var(--primary-color);
        box-shadow: 0 10px 30px rgba(0, 102, 204, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--dark-text);
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #6C757D;
        line-height: 1.5;
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-success {
        background: #D4EDDA;
        color: #155724;
    }
    
    .badge-warning {
        background: #FFF3CD;
        color: #856404;
    }
    
    .badge-danger {
        background: #F8D7DA;
        color: #721C24;
    }
    
    .badge-info {
        background: #D1ECF1;
        color: #0C5460;
    }
    
    .badge-primary {
        background: #CCE5FF;
        color: #004085;
    }
    
    /* Risk meter */
    .risk-meter {
        width: 100%;
        height: 8px;
        background: #E9ECEF;
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .risk-meter-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .risk-low { background: linear-gradient(90deg, #28A745, #34D058); }
    .risk-medium { background: linear-gradient(90deg, #FFC107, #FFDA6A); }
    .risk-high { background: linear-gradient(90deg, #DC3545, #FF6B6B); }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed #CED4DA;
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        background: #FAFBFC;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: var(--primary-color);
        background: #F0F7FF;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .chat-message.user {
        background: #E3F2FD;
        margin-left: 2rem;
    }
    
    .chat-message.assistant {
        background: #F5F5F5;
        margin-right: 2rem;
    }
    
    /* Source citation */
    .source-citation {
        background: #FFF8E1;
        border-left: 4px solid #FFC107;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    /* Timeline */
    .timeline-item {
        position: relative;
        padding-left: 2rem;
        padding-bottom: 1.5rem;
        border-left: 2px solid #E9ECEF;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: var(--primary-color);
        border: 2px solid white;
    }
    
    /* Tabs enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    /* Sidebar enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #F8F9FA 0%, #FFFFFF 100%);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    }
    
    /* Expander enhancement */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--dark-text);
    }
    
    /* Info boxes */
    .info-box {
        background: #E7F3FF;
        border: 1px solid #B8DAFF;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #FFF8E1;
        border: 1px solid #FFE082;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .danger-box {
        background: #FFEBEE;
        border: 1px solid #FFCDD2;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #E8F5E9;
        border: 1px solid #C8E6C9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Disclaimer styling */
    .disclaimer {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.85rem;
        color: #6C757D;
        border: 1px solid #DEE2E6;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F1F1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #C1C1C1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #A1A1A1;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = ""):
    """Render main header with gradient."""
    st.markdown(f"""
    <div class="main-header animate-fade-in">
        <h1>🏥 {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(value: str, label: str, color: str = "blue"):
    """Render a metric card."""
    st.markdown(f"""
    <div class="metric-card {color}">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_feature_card(icon: str, title: str, description: str):
    """Render a feature card."""
    st.markdown(f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def render_info_card(title: str, content: str, icon: str = "📋"):
    """Render an info card."""
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-header">{icon} {title}</div>
        <div class="card-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_badge(text: str, badge_type: str = "info"):
    """Render a status badge."""
    return f'<span class="badge badge-{badge_type}">{text}</span>'


def render_risk_meter(score: float, max_score: float = 100):
    """Render a risk meter."""
    percentage = min(100, (score / max_score) * 100)
    risk_class = "risk-low" if percentage < 33 else "risk-medium" if percentage < 66 else "risk-high"
    st.markdown(f"""
    <div class="risk-meter">
        <div class="risk-meter-fill {risk_class}" style="width: {percentage}%"></div>
    </div>
    """, unsafe_allow_html=True)


def render_source_citation(source: str, snippet: str):
    """Render a source citation."""
    st.markdown(f"""
    <div class="source-citation">
        <strong>📄 Source:</strong> {source}<br>
        <em>"{snippet[:200]}..."</em>
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(message: str, is_user: bool = False):
    """Render a chat message."""
    msg_class = "user" if is_user else "assistant"
    icon = "👤" if is_user else "🤖"
    st.markdown(f"""
    <div class="chat-message {msg_class}">
        <strong>{icon}</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def render_timeline_item(title: str, content: str, date: str = ""):
    """Render a timeline item."""
    st.markdown(f"""
    <div class="timeline-item">
        <strong>{title}</strong>
        {f'<span style="color: #6C757D; font-size: 0.85rem;"> • {date}</span>' if date else ''}
        <p style="margin: 0.5rem 0 0; color: #6C757D;">{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_disclaimer(text: str):
    """Render a disclaimer box."""
    st.markdown(f"""
    <div class="disclaimer">
        ⚠️ {text}
    </div>
    """, unsafe_allow_html=True)


def render_info_box(text: str, box_type: str = "info"):
    """Render an info/warning/danger box."""
    icons = {"info": "ℹ️", "warning": "⚠️", "danger": "🚨", "success": "✅"}
    icon = icons.get(box_type, "ℹ️")
    st.markdown(f"""
    <div class="{box_type}-box">
        {icon} {text}
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = ""):
    """Render a section header."""
    st.markdown(f"""
    <h3 style="color: #343A40; margin: 2rem 0 1rem; display: flex; align-items: center; gap: 0.5rem;">
        {icon} {title}
    </h3>
    """, unsafe_allow_html=True)
