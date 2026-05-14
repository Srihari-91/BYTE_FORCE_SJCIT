"""
MedIntel AI - Premium Healthcare Intelligence Platform
Enhanced UI/UX - Dark Theme Healthcare SaaS Dashboard
Version 2.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="MedIntel AI - Healthcare Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PREMIUM DARK THEME CSS
# ============================================================
def inject_premium_css():
    st.markdown("""
    <style>
    /* ===== CSS VARIABLES ===== */
    :root {
        /* Background Colors */
        --bg-primary: #070B14;
        --bg-secondary: #0D1324;
        --bg-elevated: #111827;
        --bg-card: rgba(255, 255, 255, 0.03);
        --bg-card-hover: rgba(255, 255, 255, 0.06);
        --bg-glass: rgba(255, 255, 255, 0.05);
        
        /* Primary Colors */
        --primary-blue: #2563EB;
        --primary-cyan: #06B6D4;
        --primary-teal: #14B8A6;
        --primary-violet: #8B5CF6;
        
        /* Gradients */
        --gradient-primary: linear-gradient(135deg, #2563EB 0%, #06B6D4 50%, #8B5CF6 100%);
        --gradient-hero: linear-gradient(135deg, #0B5FFF 0%, #06B6D4 50%, #4F46E5 100%);
        --gradient-card: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        --gradient-success: linear-gradient(135deg, #059669 0%, #10B981 100%);
        --gradient-warning: linear-gradient(135deg, #D97706 0%, #F59E0B 100%);
        --gradient-danger: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
        
        /* Text Colors */
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;
        --text-dark: #0F172A;
        
        /* Border Colors */
        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-medium: rgba(255, 255, 255, 0.12);
        --border-strong: rgba(255, 255, 255, 0.2);
        
        /* Status Colors */
        --success: #22C55E;
        --warning: #F59E0B;
        --danger: #EF4444;
        --info: #3B82F6;
        
        /* Shadows */
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 20px 50px rgba(0, 0, 0, 0.5);
        --shadow-glow: 0 0 40px rgba(37, 99, 235, 0.3);
        --shadow-glow-cyan: 0 0 40px rgba(6, 182, 212, 0.25);
        
        /* Spacing */
        --section-gap: 48px;
        --card-padding: 28px;
        --border-radius: 20px;
        --border-radius-sm: 12px;
        --border-radius-lg: 28px;
        
        /* Max Width */
        --max-width: 1200px;
    }
    
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* ===== STREAMLIT OVERRIDES ===== */
    .stApp {
        background: var(--bg-primary);
    }
    
    #MainMenu, footer, header[data-testid="stHeader"] {
        visibility: hidden;
        display: none;
    }
    
    .main .block-container {
        padding: 1rem 2rem 3rem;
        max-width: var(--max-width);
        margin: 0 auto;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0F1A 0%, #0D1324 100%);
        border-right: 1px solid var(--border-subtle);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 0;
    }
    
    /* ===== SIDEBAR STYLES ===== */
    .sidebar-container {
        padding: 0;
    }
    
    .sidebar-logo {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
        border-bottom: 1px solid var(--border-subtle);
        padding: 24px 20px;
        margin: 0 -1rem;
        text-align: center;
    }
    
    .sidebar-logo-icon {
        font-size: 36px;
        margin-bottom: 8px;
    }
    
    .sidebar-logo h1 {
        font-size: 22px;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .sidebar-logo p {
        font-size: 11px;
        color: var(--text-muted);
        margin: 4px 0 0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }
    
    .sidebar-status {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 10px;
        padding: 10px 14px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .sidebar-status-dot {
        width: 8px;
        height: 8px;
        background: var(--success);
        border-radius: 50%;
        animation: pulse-dot 2s infinite;
    }
    
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    .sidebar-status span {
        font-size: 12px;
        color: var(--success);
        font-weight: 600;
    }
    
    .sidebar-nav {
        padding: 8px 0;
    }
    
    .sidebar-nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        margin: 4px 0;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 500;
        color: var(--text-secondary);
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    
    .sidebar-nav-item:hover {
        background: var(--bg-glass);
        color: var(--text-primary);
        border-color: var(--border-subtle);
    }
    
    .sidebar-nav-item.active {
        background: var(--gradient-primary);
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
    }
    
    .sidebar-nav-icon {
        font-size: 18px;
        width: 24px;
        text-align: center;
    }
    
    .sidebar-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 16px;
        background: linear-gradient(0deg, var(--bg-secondary) 0%, transparent 100%);
    }
    
    .sidebar-safety-badge {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 10px;
        padding: 12px;
        font-size: 11px;
        color: var(--text-muted);
        line-height: 1.5;
    }
    
    .sidebar-safety-badge strong {
        color: var(--warning);
        display: block;
        margin-bottom: 4px;
    }
    
    /* ===== HERO SECTION ===== */
    .hero-section {
        background: var(--gradient-hero);
        border-radius: var(--border-radius-lg);
        padding: 48px;
        margin-bottom: var(--section-gap);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 30px 80px rgba(37, 99, 235, 0.25);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 80%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(6, 182, 212, 0.2) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 50%;
        height: 100%;
        background: radial-gradient(ellipse, rgba(139, 92, 246, 0.15) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .hero-grid {
        display: grid;
        grid-template-columns: 1.1fr 0.9fr;
        gap: 48px;
        align-items: center;
        position: relative;
        z-index: 1;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        padding: 8px 16px;
        font-size: 12px;
        font-weight: 600;
        color: white;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .hero-badge-dot {
        width: 6px;
        height: 6px;
        background: var(--success);
        border-radius: 50%;
    }
    
    .hero-title {
        font-size: 56px;
        font-weight: 900;
        color: white;
        line-height: 1.1;
        letter-spacing: -2px;
        margin: 0 0 12px;
    }
    
    .hero-subtitle {
        font-size: 22px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        margin: 0 0 20px;
        line-height: 1.4;
    }
    
    .hero-description {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.7;
        margin-bottom: 28px;
        max-width: 520px;
    }
    
    .hero-buttons {
        display: flex;
        gap: 14px;
        margin-bottom: 28px;
        flex-wrap: wrap;
    }
    
    .hero-btn {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 14px 28px;
        border-radius: 14px;
        font-size: 15px;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
    }
    
    .hero-btn-primary {
        background: white;
        color: var(--primary-blue);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    
    .hero-btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
    }
    
    .hero-btn-secondary {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .hero-btn-secondary:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-3px);
    }
    
    .hero-trust-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .trust-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Hero Product Card */
    .hero-product-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }
    
    .hero-product-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-product-title {
        font-size: 14px;
        font-weight: 700;
        color: white;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .hero-product-live {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        color: var(--success);
        font-weight: 600;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: var(--success);
        border-radius: 50%;
        animation: pulse-dot 1.5s infinite;
    }
    
    .hero-product-metrics {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .hero-metric-item {
        text-align: center;
        padding: 14px 10px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .hero-metric-value {
        font-size: 26px;
        font-weight: 800;
        color: white;
        line-height: 1;
    }
    
    .hero-metric-value.danger { color: var(--danger); }
    .hero-metric-value.warning { color: var(--warning); }
    .hero-metric-value.success { color: var(--success); }
    
    .hero-metric-label {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 6px;
        font-weight: 500;
    }
    
    .hero-product-progress {
        margin-bottom: 20px;
    }
    
    .progress-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    
    .progress-label {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
    }
    
    .progress-value {
        font-size: 12px;
        color: var(--danger);
        font-weight: 700;
    }
    
    .progress-bar-bg {
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--warning), var(--danger));
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .hero-product-checklist {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .checklist-item {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
        color: rgba(255, 255, 255, 0.85);
    }
    
    .checklist-icon {
        width: 20px;
        height: 20px;
        background: rgba(34, 197, 94, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        color: var(--success);
    }
    
    /* ===== SECTION STYLES ===== */
    .section {
        margin-bottom: var(--section-gap);
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 36px;
    }
    
    .section-label {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--gradient-card);
        border: 1px solid var(--border-subtle);
        border-radius: 50px;
        padding: 8px 18px;
        font-size: 12px;
        font-weight: 600;
        color: var(--primary-cyan);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
    }
    
    .section-title {
        font-size: 40px;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.2;
        letter-spacing: -1px;
        margin: 0 0 12px;
    }
    
    .section-subtitle {
        font-size: 17px;
        color: var(--text-muted);
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* ===== PROBLEM CARDS ===== */
    .problem-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 24px;
    }
    
    .problem-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: var(--border-radius);
        padding: 28px;
        transition: all 0.3s ease;
    }
    
    .problem-card:hover {
        border-color: var(--border-medium);
        background: var(--bg-card-hover);
        transform: translateY(-4px);
    }
    
    .problem-icon {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 18px;
    }
    
    .problem-icon.red { background: rgba(239, 68, 68, 0.15); }
    .problem-icon.orange { background: rgba(245, 158, 11, 0.15); }
    .problem-icon.yellow { background: rgba(234, 179, 8, 0.15); }
    
    .problem-title {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 10px;
    }
    
    .problem-text {
        font-size: 14px;
        color: var(--text-muted);
        line-height: 1.6;
        margin: 0;
    }
    
    .solution-strip {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 1px solid rgba(37, 99, 235, 0.2);
        border-radius: 16px;
        padding: 20px 28px;
        text-align: center;
    }
    
    .solution-strip p {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .solution-strip span {
        color: var(--primary-cyan);
    }
    
    /* ===== METRIC CARDS ===== */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin-bottom: 20px;
    }
    
    .metric-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: var(--border-radius);
        padding: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    
    .metric-card.blue::before { background: var(--gradient-primary); }
    .metric-card.green::before { background: var(--gradient-success); }
    .metric-card.orange::before { background: var(--gradient-warning); }
    .metric-card.red::before { background: var(--gradient-danger); }
    .metric-card.purple::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
    
    .metric-card:hover {
        border-color: var(--border-medium);
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
    }
    
    .metric-icon-box {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        margin-bottom: 16px;
    }
    
    .metric-icon-box.blue { background: rgba(37, 99, 235, 0.15); }
    .metric-icon-box.green { background: rgba(34, 197, 94, 0.15); }
    .metric-icon-box.orange { background: rgba(245, 158, 11, 0.15); }
    .metric-icon-box.red { background: rgba(239, 68, 68, 0.15); }
    .metric-icon-box.purple { background: rgba(139, 92, 246, 0.15); }
    
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 6px;
    }
    
    .metric-label {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 4px;
    }
    
    .metric-subtext {
        font-size: 12px;
        color: var(--text-muted);
    }
    
    /* Claim Risk Score Card - Special */
    .claim-risk-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: var(--border-radius);
        padding: 28px;
        grid-column: span 2;
        display: flex;
        align-items: center;
        gap: 28px;
        position: relative;
        overflow: hidden;
    }
    
    .claim-risk-card::before {
        content: '⚡';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 120px;
        opacity: 0.05;
    }
    
    .claim-risk-score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(var(--danger) 0% 78%, rgba(255,255,255,0.1) 78% 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        flex-shrink: 0;
    }
    
    .claim-risk-score-inner {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: var(--bg-primary);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .claim-risk-score-value {
        font-size: 32px;
        font-weight: 800;
        color: var(--danger);
        line-height: 1;
    }
    
    .claim-risk-score-label {
        font-size: 11px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }
    
    .claim-risk-info h3 {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 8px;
    }
    
    .claim-risk-info p {
        font-size: 14px;
        color: var(--text-muted);
        margin: 0 0 16px;
        line-height: 1.5;
    }
    
    .claim-risk-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 8px 14px;
        font-size: 13px;
        font-weight: 700;
        color: var(--danger);
    }
    
    /* ===== FEATURE CARDS ===== */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
    }
    
    .feature-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: var(--border-radius);
        padding: 26px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .feature-card:hover {
        border-color: var(--primary-cyan);
        background: var(--bg-card-hover);
        transform: translateY(-4px);
        box-shadow: var(--shadow-glow-cyan);
    }
    
    .feature-card.signature {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%);
        border-color: rgba(139, 92, 246, 0.3);
    }
    
    .feature-card.signature:hover {
        border-color: var(--primary-violet);
        box-shadow: 0 0 40px rgba(139, 92, 246, 0.3);
    }
    
    .feature-badge {
        position: absolute;
        top: 14px;
        right: 14px;
        background: var(--gradient-primary);
        color: white;
        font-size: 9px;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .feature-icon-box {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 18px;
    }
    
    .feature-icon-box.blue { background: linear-gradient(135deg, rgba(37, 99, 235, 0.2), rgba(37, 99, 235, 0.1)); }
    .feature-icon-box.cyan { background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(6, 182, 212, 0.1)); }
    .feature-icon-box.green { background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1)); }
    .feature-icon-box.orange { background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1)); }
    .feature-icon-box.red { background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1)); }
    .feature-icon-box.purple { background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.1)); }
    .feature-icon-box.teal { background: linear-gradient(135deg, rgba(20, 184, 166, 0.2), rgba(20, 184, 166, 0.1)); }
    .feature-icon-box.pink { background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(236, 72, 153, 0.1)); }
    
    .feature-title {
        font-size: 17px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 10px;
    }
    
    .feature-description {
        font-size: 13px;
        color: var(--text-muted);
        line-height: 1.6;
        margin: 0;
    }
    
    /* ===== PIPELINE SECTION ===== */
    .pipeline-container {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: var(--border-radius-lg);
        padding: 36px;
    }
    
    .pipeline-grid {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        position: relative;
    }
    
    .pipeline-grid::before {
        content: '';
        position: absolute;
        top: 35px;
        left: 60px;
        right: 60px;
        height: 2px;
        background: linear-gradient(90deg, var(--primary-blue), var(--primary-cyan), var(--primary-violet));
        opacity: 0.3;
    }
    
    .pipeline-step {
        flex: 1;
        text-align: center;
        position: relative;
        z-index: 1;
    }
    
    .pipeline-number {
        width: 70px;
        height: 70px;
        margin: 0 auto 16px;
        border-radius: 50%;
        background: var(--gradient-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: white;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
        position: relative;
    }
    
    .pipeline-step-title {
        font-size: 14px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 6px;
    }
    
    .pipeline-step-desc {
        font-size: 12px;
        color: var(--text-muted);
        margin: 0;
        max-width: 120px;
        margin: 0 auto;
    }
    
    .pipeline-note {
        text-align: center;
        margin-top: 28px;
        padding-top: 20px;
        border-top: 1px solid var(--border-subtle);
    }
    
    .pipeline-note p {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.2);
        border-radius: 10px;
        padding: 10px 18px;
        font-size: 13px;
        color: var(--success);
        font-weight: 500;
        margin: 0;
    }
    
    /* ===== COMPARISON SECTION ===== */
    .comparison-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
    }
    
    .comparison-card {
        border-radius: var(--border-radius);
        padding: 32px;
        position: relative;
    }
    
    .comparison-card.negative {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.03) 100%);
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    .comparison-card.positive {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 2px solid rgba(37, 99, 235, 0.4);
        box-shadow: var(--shadow-glow);
    }
    
    .comparison-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }
    
    .comparison-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
    
    .comparison-card.negative .comparison-icon {
        background: rgba(239, 68, 68, 0.15);
    }
    
    .comparison-card.positive .comparison-icon {
        background: rgba(37, 99, 235, 0.15);
    }
    
    .comparison-title {
        font-size: 20px;
        font-weight: 700;
        margin: 0;
    }
    
    .comparison-card.negative .comparison-title { color: #FCA5A5; }
    .comparison-card.positive .comparison-title { color: var(--text-primary); }
    
    .comparison-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .comparison-list li {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 0;
        font-size: 14px;
        line-height: 1.5;
        border-bottom: 1px solid var(--border-subtle);
    }
    
    .comparison-list li:last-child {
        border-bottom: none;
    }
    
    .comparison-card.negative .comparison-list li {
        color: var(--text-muted);
    }
    
    .comparison-card.positive .comparison-list li {
        color: var(--text-secondary);
    }
    
    .comparison-list-icon {
        flex-shrink: 0;
        margin-top: 2px;
    }
    
    .comparison-card.negative .comparison-list-icon { color: #F87171; }
    .comparison-card.positive .comparison-list-icon { color: var(--success); }
    
    .comparison-footer {
        text-align: center;
        margin-top: 32px;
        padding: 24px;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
    }
    
    .comparison-footer p {
        font-size: 17px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .comparison-footer span {
        color: var(--primary-cyan);
    }
    
    /* ===== SIGNATURE FEATURE SECTION ===== */
    .signature-section {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(37, 99, 235, 0.08) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: var(--border-radius-lg);
        padding: 40px;
        position: relative;
        overflow: hidden;
    }
    
    .signature-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -25%;
        width: 50%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(139, 92, 246, 0.1) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .signature-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--primary-violet);
        color: white;
        font-size: 11px;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 50px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }
    
    .signature-content {
        display: grid;
        grid-template-columns: 1fr 1.2fr;
        gap: 40px;
        align-items: center;
    }
    
    .signature-info h2 {
        font-size: 32px;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 0 14px;
        line-height: 1.2;
    }
    
    .signature-info p {
        font-size: 16px;
        color: var(--text-muted);
        line-height: 1.6;
        margin: 0 0 24px;
    }
    
    .signature-cta {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: var(--gradient-primary);
        color: white;
        font-size: 15px;
        font-weight: 700;
        padding: 14px 28px;
        border-radius: 12px;
        text-decoration: none;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
    }
    
    .signature-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(37, 99, 235, 0.4);
    }
    
    .signature-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-medium);
        border-radius: var(--border-radius);
        padding: 28px;
    }
    
    .signature-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--border-subtle);
    }
    
    .signature-score {
        display: flex;
        align-items: baseline;
        gap: 8px;
    }
    
    .signature-score-value {
        font-size: 42px;
        font-weight: 800;
        color: var(--danger);
    }
    
    .signature-score-max {
        font-size: 18px;
        color: var(--text-muted);
    }
    
    .signature-score-badge {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 700;
        color: var(--danger);
    }
    
    .signature-risks {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .signature-risk-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 14px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    
    .signature-risk-item:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: var(--border-medium);
    }
    
    .risk-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
    }
    
    .risk-icon.high { background: rgba(239, 68, 68, 0.15); color: var(--danger); }
    .risk-icon.medium { background: rgba(245, 158, 11, 0.15); color: var(--warning); }
    .risk-icon.low { background: rgba(34, 197, 94, 0.15); color: var(--success); }
    
    .signature-risk-text {
        font-size: 13px;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    /* ===== SAFETY SECTION ===== */
    .safety-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-bottom: 28px;
    }
    
    .safety-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: var(--border-radius);
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .safety-card:hover {
        border-color: var(--border-medium);
        transform: translateY(-4px);
    }
    
    .safety-icon {
        width: 56px;
        height: 56px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        margin: 0 auto 16px;
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.05));
    }
    
    .safety-title {
        font-size: 15px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 8px;
    }
    
    .safety-text {
        font-size: 13px;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }
    
    .safety-disclaimer {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(245, 158, 11, 0.03) 100%);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    
    .safety-disclaimer p {
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.7;
        margin: 0;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .safety-disclaimer strong {
        color: var(--warning);
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 1024px) {
        .hero-grid {
            grid-template-columns: 1fr;
            gap: 36px;
        }
        
        .hero-title { font-size: 44px; }
        
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .claim-risk-card {
            grid-column: span 2;
        }
        
        .features-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .problem-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .problem-grid > div:last-child {
            grid-column: span 2;
        }
        
        .signature-content {
            grid-template-columns: 1fr;
        }
        
        .comparison-grid {
            grid-template-columns: 1fr;
        }
        
        .pipeline-grid::before {
            display: none;
        }
        
        .pipeline-grid {
            flex-wrap: wrap;
            gap: 24px;
        }
        
        .pipeline-step {
            flex: 0 0 calc(33.333% - 16px);
        }
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 1rem 2rem;
        }
        
        .hero-section {
            padding: 32px 24px;
        }
        
        .hero-title { font-size: 36px; }
        .hero-subtitle { font-size: 18px; }
        .section-title { font-size: 28px; }
        
        .metrics-grid,
        .features-grid,
        .problem-grid,
        .safety-grid {
            grid-template-columns: 1fr;
        }
        
        .claim-risk-card {
            grid-column: span 1;
            flex-direction: column;
            text-align: center;
        }
        
        .problem-grid > div:last-child {
            grid-column: span 1;
        }
        
        .pipeline-step {
            flex: 0 0 100%;
        }
    }
    
    /* ===== STREAMLIT COMPONENT OVERRIDES ===== */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4);
    }
    
    div[data-testid="stExpander"] {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
    }
    
    .stRadio > div {
        background: transparent;
    }
    
    .stRadio > div > label {
        color: var(--text-secondary) !important;
    }
    
    hr {
        border: none;
        height: 1px;
        background: var(--border-subtle);
        margin: 32px 0;
    }
    
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.metrics = {
            "documents": 4,
            "facts": 47,
            "insurance_risks": 5,
            "bill_risks": 3,
            "claim_risk_score": 78
        }

# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-container">
            <div class="sidebar-logo">
                <div class="sidebar-logo-icon">🧠</div>
                <h1>MedIntel AI</h1>
                <p>Healthcare Intelligence</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-status">
            <div class="sidebar-status-dot"></div>
            <span>AI Engine Ready</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            [
                "🏠 Home Dashboard",
                "📤 Upload Documents",
                "🧠 Medical Memory",
                "📈 Health Trends",
                "🛡️ Insurance Decoder",
                "🧾 Bill Watchdog",
                "⚡ Claim Risk Engine",
                "📄 Summary Reports",
                "🔒 Safety & About"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Docs", st.session_state.metrics["documents"])
        with col2:
            st.metric("Risks", st.session_state.metrics["insurance_risks"] + st.session_state.metrics["bill_risks"])
        
        st.markdown("""
        <div class="sidebar-safety-badge">
            <strong>⚠️ Important Notice</strong>
            Decision support only. Not medical diagnosis. Doctor-in-the-loop design.
        </div>
        """, unsafe_allow_html=True)
        
        return page

# ============================================================
# HOME DASHBOARD
# ============================================================
def render_home():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-grid">
            <div class="hero-content">
                <div class="hero-badge">
                    <div class="hero-badge-dot"></div>
                    AI Healthcare Intelligence Platform
                </div>
                <h1 class="hero-title">MedIntel AI</h1>
                <p class="hero-subtitle">Personal Medical Memory, Insurance Decoder & Hospital Bill Watchdog</p>
                <p class="hero-description">
                    Turn scattered medical records, insurance policies, and hospital bills into 
                    source-backed health insights and financial protection. Every answer grounded in your own documents.
                </p>
                <div class="hero-buttons">
                    <span class="hero-btn hero-btn-primary">📤 Upload Documents</span>
                    <span class="hero-btn hero-btn-secondary">▶️ View Demo Flow</span>
                </div>
                <div class="hero-trust-chips">
                    <span class="trust-chip">✓ Source-backed AI</span>
                    <span class="trust-chip">✓ RAG-powered</span>
                    <span class="trust-chip">✓ Doctor-in-the-loop</span>
                    <span class="trust-chip">✓ No diagnosis</span>
                </div>
            </div>
            <div class="hero-product">
                <div class="hero-product-card">
                    <div class="hero-product-header">
                        <span class="hero-product-title">Live Patient Intelligence</span>
                        <span class="hero-product-live">
                            <div class="live-dot"></div>
                            Active
                        </span>
                    </div>
                    <div class="hero-product-metrics">
                        <div class="hero-metric-item">
                            <div class="hero-metric-value">4</div>
                            <div class="hero-metric-label">Documents</div>
                        </div>
                        <div class="hero-metric-item">
                            <div class="hero-metric-value warning">8</div>
                            <div class="hero-metric-label">Risks Found</div>
                        </div>
                        <div class="hero-metric-item">
                            <div class="hero-metric-value danger">High</div>
                            <div class="hero-metric-label">Claim Risk</div>
                        </div>
                    </div>
                    <div class="hero-product-progress">
                        <div class="progress-header">
                            <span class="progress-label">Claim Risk Score</span>
                            <span class="progress-value">78/100</span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: 78%;"></div>
                        </div>
                    </div>
                    <div class="hero-product-checklist">
                        <div class="checklist-item">
                            <span class="checklist-icon">✓</span>
                            <span>OCR extraction completed</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">✓</span>
                            <span>RAG memory indexed</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">✓</span>
                            <span>3 bill risks detected</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">✓</span>
                            <span>5 policy clauses decoded</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Problem Section
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-label">🎯 The Real Problem</div>
            <h2 class="section-title">Why Patients Struggle</h2>
            <p class="section-subtitle">Healthcare challenges go beyond medical care — they include information chaos and financial opacity</p>
        </div>
        
        <div class="problem-grid">
            <div class="problem-card">
                <div class="problem-icon red">📂</div>
                <h3 class="problem-title">Fragmented Medical Records</h3>
                <p class="problem-text">Prescriptions, lab reports, and discharge summaries scattered across paper files, WhatsApp, emails, and hospital portals.</p>
            </div>
            <div class="problem-card">
                <div class="problem-icon orange">📋</div>
                <h3 class="problem-title">Confusing Insurance Clauses</h3>
                <p class="problem-text">Room rent caps, exclusions, waiting periods, co-pay, and sublimits are impossible to understand before hospitalization.</p>
            </div>
            <div class="problem-card">
                <div class="problem-icon yellow">🧾</div>
                <h3 class="problem-title">Opaque Hospital Billing</h3>
                <p class="problem-text">Patients struggle to verify duplicate charges, inflated diagnostics, repeated consumables, and claim deduction risks.</p>
            </div>
        </div>
        
        <div class="solution-strip">
            <p>💡 <span>MedIntel AI</span> connects medical records + insurance policy + hospital bill into one patient-side intelligence layer.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics Section
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-label">📊 Dashboard</div>
            <h2 class="section-title">Your Health Intelligence</h2>
            <p class="section-subtitle">Real-time insights extracted from your uploaded documents</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card blue">
                <div class="metric-icon-box blue">📄</div>
                <div class="metric-value">4</div>
                <div class="metric-label">Documents Processed</div>
                <div class="metric-subtext">Uploaded and indexed</div>
            </div>
            <div class="metric-card green">
                <div class="metric-icon-box green">🔍</div>
                <div class="metric-value">47</div>
                <div class="metric-label">Medical Facts Extracted</div>
                <div class="metric-subtext">Medicines, tests, diagnoses</div>
            </div>
            <div class="metric-card orange">
                <div class="metric-icon-box orange">🛡️</div>
                <div class="metric-value">5</div>
                <div class="metric-label">Insurance Risks Found</div>
                <div class="metric-subtext">Clauses needing attention</div>
            </div>
            <div class="metric-card red">
                <div class="metric-icon-box red">🧾</div>
                <div class="metric-value">3</div>
                <div class="metric-label">Bill Risks Flagged</div>
                <div class="metric-subtext">Charges worth verifying</div>
            </div>
        </div>
        
        <div class="claim-risk-card">
            <div class="claim-risk-score-circle">
                <div class="claim-risk-score-inner">
                    <div class="claim-risk-score-value">78</div>
                    <div class="claim-risk-score-label">Risk Score</div>
                </div>
            </div>
            <div class="claim-risk-info">
                <h3>⚡ Claim Risk Intelligence</h3>
                <p>Your insurance policy and hospital bill have been analyzed. Multiple risk factors detected that may affect claim payout.</p>
                <span class="claim-risk-badge">🔴 High Risk — Review Recommended</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-label">✨ Features</div>
            <h2 class="section-title">AI-Powered Healthcare Intelligence</h2>
            <p class="section-subtitle">Comprehensive document understanding and risk analysis</p>
        </div>
        
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon-box blue">🧠</div>
                <h3 class="feature-title">Medical Memory</h3>
                <p class="feature-description">Ask questions from your uploaded prescriptions, reports, and discharge summaries.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon-box cyan">💬</div>
                <h3 class="feature-title">Source-backed RAG Chat</h3>
                <p class="feature-description">Every answer includes citations and evidence from your actual documents.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon-box green">📈</div>
                <h3 class="feature-title">Health Trend Intelligence</h3>
                <p class="feature-description">Track lab values across reports and detect changes over time.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon-box orange">🛡️</div>
                <h3 class="feature-title">Insurance Decoder</h3>
                <p class="feature-description">Understand room rent caps, waiting periods, exclusions, and co-pay clauses.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon-box red">🧾</div>
                <h3 class="feature-title">Hospital Bill Watchdog</h3>
                <p class="feature-description">Flag possible duplicate charges, unusual costs, and repeated consumables.</p>
            </div>
            <div class="feature-card signature">
                <span class="feature-badge">⭐ Signature</span>
                <div class="feature-icon-box purple">⚡</div>
                <h3 class="feature-title">Claim Risk Engine</h3>
                <p class="feature-description">Connect insurance clauses with bill items to estimate claim risks.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon-box teal">📄</div>
                <h3 class="feature-title">Doctor-Ready Summary</h3>
                <p class="feature-description">Generate concise summaries for doctors and insurers with evidence.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon-box pink">🌐</div>
                <h3 class="feature-title">Multilingual Support</h3>
                <p class="feature-description">Explain complex medical and insurance terms in simple language.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pipeline Section
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-label">🔄 How It Works</div>
            <h2 class="section-title">Real-Time AI Pipeline</h2>
            <p class="section-subtitle">From document upload to actionable insights in seconds</p>
        </div>
        
        <div class="pipeline-container">
            <div class="pipeline-grid">
                <div class="pipeline-step">
                    <div class="pipeline-number">📤</div>
                    <h4 class="pipeline-step-title">Upload</h4>
                    <p class="pipeline-step-desc">PDF, images, scanned documents</p>
                </div>
                <div class="pipeline-step">
                    <div class="pipeline-number">👁️</div>
                    <h4 class="pipeline-step-title">OCR Extract</h4>
                    <p class="pipeline-step-desc">Text extraction from any format</p>
                </div>
                <div class="pipeline-step">
                    <div class="pipeline-number">🤖</div>
                    <h4 class="pipeline-step-title">AI Parse</h4>
                    <p class="pipeline-step-desc">Structured entity extraction</p>
                </div>
                <div class="pipeline-step">
                    <div class="pipeline-number">🧠</div>
                    <h4 class="pipeline-step-title">Vector Memory</h4>
                    <p class="pipeline-step-desc">Embeddings for RAG search</p>
                </div>
                <div class="pipeline-step">
                    <div class="pipeline-number">💬</div>
                    <h4 class="pipeline-step-title">RAG Answer</h4>
                    <p class="pipeline-step-desc">Source-backed responses</p>
                </div>
                <div class="pipeline-step">
                    <div class="pipeline-number">⚡</div>
                    <h4 class="pipeline-step-title">Risk Intel</h4>
                    <p class="pipeline-step-desc">Insurance + bill analysis</p>
                </div>
                <div class="pipeline-step">
                    <div class="pipeline-number">📄</div>
                    <h4 class="pipeline-step-title">Summary</h4>
                    <p class="pipeline-step-desc">Doctor-ready reports</p>
                </div>
            </div>
            <div class="pipeline-note">
                <p>✨ Dynamic workflow — works on newly uploaded documents, not fixed datasets</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Signature Feature Section
    st.markdown("""
    <div class="section">
        <div class="signature-section">
            <span class="signature-badge">⭐ Signature Differentiator</span>
            <div class="signature-content">
                <div class="signature-info">
                    <h2>Claim Risk Intelligence Engine</h2>
                    <p>Most tools explain insurance and bills separately. MedIntel AI connects both to estimate real claim risk BEFORE you file — helping you take corrective action and ask the right questions.</p>
                    <button class="signature-cta">⚡ Open Claim Risk Engine →</button>
                </div>
                <div class="signature-card">
                    <div class="signature-card-header">
                        <div class="signature-score">
                            <span class="signature-score-value">78</span>
                            <span class="signature-score-max">/100</span>
                        </div>
                        <span class="signature-score-badge">🔴 HIGH RISK</span>
                    </div>
                    <div class="signature-risks">
                        <div class="signature-risk-item">
                            <div class="risk-icon high">!</div>
                            <span class="signature-risk-text">Room rent cap conflict — ₹8,000/day vs ₹5,000 limit</span>
                        </div>
                        <div class="signature-risk-item">
                            <div class="risk-icon high">!</div>
                            <span class="signature-risk-text">Consumables may not be fully covered</span>
                        </div>
                        <div class="signature-risk-item">
                            <div class="risk-icon medium">⚠</div>
                            <span class="signature-risk-text">20% co-payment will apply to total claim</span>
                        </div>
                        <div class="signature-risk-item">
                            <div class="risk-icon medium">⚠</div>
                            <span class="signature-risk-text">MRI charge ₹12,500 above benchmark</span>
                        </div>
                        <div class="signature-risk-item">
                            <div class="risk-icon low">?</div>
                            <span class="signature-risk-text">Possible duplicate CBC charge worth verifying</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Comparison Section
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-label">🏆 Why Different</div>
            <h2 class="section-title">Not Just Another Healthcare Chatbot</h2>
            <p class="section-subtitle">MedIntel AI is a document-grounded intelligence system</p>
        </div>
        
        <div class="comparison-grid">
            <div class="comparison-card negative">
                <div class="comparison-header">
                    <div class="comparison-icon">❌</div>
                    <h3 class="comparison-title">Generic Healthcare Chatbot</h3>
                </div>
                <ul class="comparison-list">
                    <li><span class="comparison-list-icon">✗</span> Generic web-sourced answers</li>
                    <li><span class="comparison-list-icon">✗</span> No patient-specific memory</li>
                    <li><span class="comparison-list-icon">✗</span> No document evidence or citations</li>
                    <li><span class="comparison-list-icon">✗</span> No insurance-bill connection</li>
                    <li><span class="comparison-list-icon">✗</span> No claim risk intelligence</li>
                    <li><span class="comparison-list-icon">✗</span> High hallucination risk</li>
                </ul>
            </div>
            <div class="comparison-card positive">
                <div class="comparison-header">
                    <div class="comparison-icon">🧠</div>
                    <h3 class="comparison-title">MedIntel AI</h3>
                </div>
                <ul class="comparison-list">
                    <li><span class="comparison-list-icon">✓</span> Uses YOUR uploaded documents</li>
                    <li><span class="comparison-list-icon">✓</span> Source-backed answers with confidence</li>
                    <li><span class="comparison-list-icon">✓</span> OCR + RAG + Vector memory</li>
                    <li><span class="comparison-list-icon">✓</span> Insurance policy decoding</li>
                    <li><span class="comparison-list-icon">✓</span> Hospital bill risk detection</li>
                    <li><span class="comparison-list-icon">✓</span> Claim Risk Intelligence Engine</li>
                </ul>
            </div>
        </div>
        
        <div class="comparison-footer">
            <p>💡 The differentiator is not chat. The differentiator is <span>patient-side medical and financial intelligence</span>.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Safety Section
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-label">🔒 Safety First</div>
            <h2 class="section-title">Built for Safe, Doctor-in-the-loop Assistance</h2>
            <p class="section-subtitle">Responsible AI design for healthcare</p>
        </div>
        
        <div class="safety-grid">
            <div class="safety-card">
                <div class="safety-icon">🚫</div>
                <h4 class="safety-title">Not a Diagnosis</h4>
                <p class="safety-text">MedIntel AI never diagnoses conditions or diseases</p>
            </div>
            <div class="safety-card">
                <div class="safety-icon">💊</div>
                <h4 class="safety-title">No Prescription Changes</h4>
                <p class="safety-text">Never recommends stopping or changing medications</p>
            </div>
            <div class="safety-card">
                <div class="safety-icon">📄</div>
                <h4 class="safety-title">Source-backed Answers</h4>
                <p class="safety-text">Every response cites the exact document and snippet</p>
            </div>
            <div class="safety-card">
                <div class="safety-icon">🚨</div>
                <h4 class="safety-title">Emergency Escalation</h4>
                <p class="safety-text">Detects emergency symptoms and urges immediate care</p>
            </div>
            <div class="safety-card">
                <div class="safety-icon">🗣️</div>
                <h4 class="safety-title">Careful Billing Language</h4>
                <p class="safety-text">Uses "possible" and "verify" — never accuses fraud</p>
            </div>
            <div class="safety-card">
                <div class="safety-icon">📊</div>
                <h4 class="safety-title">Confidence Scoring</h4>
                <p class="safety-text">Shows confidence levels for all AI outputs</p>
            </div>
        </div>
        
        <div class="safety-disclaimer">
            <p><strong>⚠️ Important Disclaimer:</strong> MedIntel AI provides AI-assisted document understanding and decision support. 
            It does not diagnose, prescribe, replace qualified medical professionals, guarantee claim approval, or accuse hospitals of fraud. 
            Always consult your doctor for medical decisions and your insurer for claim queries.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PLACEHOLDER PAGES
# ============================================================
def render_upload():
    st.markdown("""
    <div class="section-header" style="text-align: left;">
        <div class="section-label">📤 Upload</div>
        <h2 class="section-title">Upload Healthcare Documents</h2>
        <p class="section-subtitle">Upload prescriptions, lab reports, discharge summaries, insurance policies, or hospital bills</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Drop files here or click to browse",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
        # Backend hook: process_documents(uploaded_files)

def render_chat():
    st.markdown("""
    <div class="section-header" style="text-align: left;">
        <div class="section-label">🧠 Medical Memory</div>
        <h2 class="section-title">Ask Your Health Records</h2>
        <p class="section-subtitle">Every answer is source-backed from your uploaded documents</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_input = st.chat_input("Ask about your medical records...")
    if user_input:
        st.info(f"🔍 Searching documents for: {user_input}")
        # Backend hook: rag_answer = generate_answer(user_input)

def render_trends():
    st.markdown("""
    <div class="section-header" style="text-align: left;">
        <div class="section-label">📈 Trends</div>
        <h2 class="section-title">Health Trend Intelligence</h2>
        <p class="section-subtitle">Track your lab values over time</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample chart
    dates = pd.date_range(start='2024-01-01', periods=6, freq='M')
    values = [7.2, 7.0, 6.9, 6.8, 6.8, 6.5]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', 
                             line=dict(color='#06B6D4', width=3),
                             marker=dict(size=10)))
    fig.add_hline(y=5.7, line_dash="dash", line_color="#22C55E")
    fig.add_hline(y=6.5, line_dash="dash", line_color="#EF4444")
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        title="HbA1c Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

def render_insurance():
    st.markdown("""
    <div class="section-header" style="text-align: left;">
        <div class="section-label">🛡️ Insurance</div>
        <h2 class="section-title">Insurance Policy Decoder</h2>
        <p class="section-subtitle">Understand hidden clauses that may affect your claim</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📋 Upload an insurance policy document to decode clauses")

def render_bill():
    st.markdown("""
    <div class="section-header" style="text-align: left;">
        <div class="section-label">🧾 Bill Watchdog</div>
        <h2 class="section-title">Hospital Bill Analysis</h2>
        <p class="section-subtitle">Identify unusual charges and verify billing accuracy</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🧾 Upload a hospital bill to analyze for potential issues")

def render_claim_risk():
    st.markdown("""
    <div class="section-header" style="text-align: left;">
        <div class="section-label">⚡ Claim Risk Engine</div>
        <h2 class="section-title">Claim Risk Intelligence</h2>
        <p class="section-subtitle">Connect insurance policy + hospital bill to estimate claim risks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("⚠️ Upload both insurance policy and hospital bill to run claim risk analysis")

def render_summary():
    st.markdown("""
    <div class="section-header" style="text-align: left;">
        <div class="section-label">📄 Summary</div>
        <h2 class="section-title">Doctor & Insurer Summary</h2>
        <p class="section-subtitle">Generate comprehensive reports for consultations</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("📋 Generate Doctor Summary", use_container_width=True)
    with col2:
        st.button("🏢 Generate Insurer Summary", use_container_width=True)

def render_safety():
    st.markdown("""
    <div class="section-header" style="text-align: left;">
        <div class="section-label">🔒 Safety</div>
        <h2 class="section-title">About & Safety Information</h2>
        <p class="section-subtitle">Understanding MedIntel AI's capabilities and limitations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### What MedIntel AI Does
    - Reads and extracts text from healthcare documents
    - Builds searchable medical memory from records
    - Explains medical terms in simple language
    - Decodes insurance policy clauses
    - Flags unusual hospital bill charges
    - Generates doctor-ready summaries
    
    ### What MedIntel AI Does NOT Do
    - Does NOT diagnose diseases
    - Does NOT prescribe medications
    - Does NOT replace doctors
    - Does NOT guarantee claims
    - Does NOT accuse hospitals
    """)

# ============================================================
# MAIN
# ============================================================
def main():
    inject_premium_css()
    init_session_state()
    
    page = render_sidebar()
    
    if page == "🏠 Home Dashboard":
        render_home()
    elif page == "📤 Upload Documents":
        render_upload()
    elif page == "🧠 Medical Memory":
        render_chat()
    elif page == "📈 Health Trends":
        render_trends()
    elif page == "🛡️ Insurance Decoder":
        render_insurance()
    elif page == "🧾 Bill Watchdog":
        render_bill()
    elif page == "⚡ Claim Risk Engine":
        render_claim_risk()
    elif page == "📄 Summary Reports":
        render_summary()
    elif page == "🔒 Safety & About":
        render_safety()

if __name__ == "__main__":
    main()
