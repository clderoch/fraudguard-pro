import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import random
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FraudGuard Pro - Small Business Protection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# MODERN CSS - Updated with Modernize-inspired design
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Modern CSS Variables */
    :root {
        --primary-color: #5d87ff;
        --secondary-color: #49beff;
        --success-color: #13deb9;
        --danger-color: #fa896b;
        --warning-color: #ffae1f;
        --info-color: #539bff;
        --light-color: #f5f5f9;
        --dark-color: #2a3547;
        --border-color: #e5eaef;
        --text-muted: #5a6a85;
        --white: #ffffff;
        --gray-50: #f8fafc;
        --gray-100: #f1f5f9;
        --gray-200: #e2e8f0;
        --gray-300: #cbd5e1;
        --gray-400: #94a3b8;
        --gray-500: #64748b;
        --gray-600: #475569;
        --gray-700: #334155;
        --gray-800: #1e293b;
        --gray-900: #0f172a;
        --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        --radius-sm: 0.25rem;
        --radius-md: 0.375rem;
        --radius-lg: 0.5rem;
        --radius-xl: 0.75rem;
        --radius-2xl: 1rem;
        --radius-3xl: 1.5rem;
    }
    
    /* Reset and Base Styles */
    .stApp {
        background-color: var(--light-color);
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit branding */
    .css-1d391kg, [data-testid="stHeader"] {padding: 1rem 2rem 2rem;}
    [data-testid="stToolbar"] {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Modern Header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 3rem 2rem;
        border-radius: var(--radius-2xl);
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        letter-spacing: -0.025em;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.125rem;
        font-weight: 400;
        opacity: 0.95;
        margin: 0;
    }
    
    /* Modern Cards */
    .modern-card {
        background: var(--white);
        border-radius: var(--radius-xl);
        padding: 2rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }
    
    /* Status Cards */
    .status-card {
        background: var(--white);
        border-radius: var(--radius-2xl);
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .status-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .status-card.success {
        border-left: 4px solid var(--success-color);
        background: linear-gradient(135deg, rgba(19, 222, 185, 0.05) 0%, var(--white) 100%);
    }
    
    .status-card.warning {
        border-left: 4px solid var(--warning-color);
        background: linear-gradient(135deg, rgba(255, 174, 31, 0.05) 0%, var(--white) 100%);
    }
    
    .status-card.danger {
        border-left: 4px solid var(--danger-color);
        background: linear-gradient(135deg, rgba(250, 137, 107, 0.05) 0%, var(--white) 100%);
    }
    
    .status-card.info {
        border-left: 4px solid var(--info-color);
        background: linear-gradient(135deg, rgba(83, 155, 255, 0.05) 0%, var(--white) 100%);
    }
    
    .status-number {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: var(--dark-color);
        font-feature-settings: 'tnum', 'lnum';
    }
    
    .status-card.success .status-number {
        color: var(--success-color);
    }
    
    .status-card.warning .status-number {
        color: var(--warning-color);
    }
    
    .status-card.danger .status-number {
        color: var(--danger-color);
    }
    
    .status-card.info .status-number {
        color: var(--info-color);
    }
    
    .status-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-badge {
        padding: 0.375rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
        box-shadow: var(--shadow-sm);
    }
    
    .status-badge.success {
        background: var(--success-color);
    }
    
    .status-badge.warning {
        background: var(--warning-color);
    }
    
    .status-badge.danger {
        background: var(--danger-color);
    }
    
    /* Modern File Upload */
    .stFileUploader {
        border: 2px dashed var(--border-color);
        border-radius: var(--radius-xl);
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        background: var(--white);
    }
    
    .stFileUploader:hover {
        border-color: var(--primary-color);
        background: rgba(93, 135, 255, 0.05);
    }
    
    /* Modern Metrics */
    .stMetric {
        background: var(--white);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    .stMetric [data-testid="metric-container"] {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    .stMetric [data-testid="metric-container"] > div {
        color: var(--dark-color);
        font-weight: 600;
    }
    
    .stMetric [data-testid="metric-container"] > div:first-child {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-color);
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: var(--radius-lg);
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        text-transform: none;
        letter-spacing: 0.025em;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Modern Expander */
    .stExpander {
        background: var(--white);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    .stExpander > div:first-child {
        background: linear-gradient(135deg, var(--gray-50) 0%, var(--white) 100%);
        border-bottom: 1px solid var(--border-color);
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: var(--dark-color);
    }
    
    .stExpander > div:first-child:hover {
        background: linear-gradient(135deg, var(--gray-100) 0%, var(--gray-50) 100%);
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--white);
        border-radius: var(--radius-lg);
        padding: 0.25rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: var(--radius-md);
        color: var(--text-muted);
        font-weight: 500;
        margin: 0.25rem;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(93, 135, 255, 0.1);
        color: var(--primary-color);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--primary-color);
        color: white;
        font-weight: 600;
    }
    
    /* Modern Dataframe */
    .stDataFrame {
        background: var(--white);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        overflow: hidden;
    }
    
    .stDataFrame [data-testid="stDataFrame"] {
        background: var(--white);
    }
    
    .stDataFrame [data-testid="stDataFrame"] thead th {
        background: var(--gray-50);
        color: var(--dark-color);
        font-weight: 600;
        padding: 1rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    .stDataFrame [data-testid="stDataFrame"] tbody td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* Modern Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-color) 0%, rgba(19, 222, 185, 0.8) 100%);
        color: white;
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        border: none;
        box-shadow: var(--shadow-md);
        font-weight: 500;
    }
    
    .stError {
        background: linear-gradient(135deg, var(--danger-color) 0%, rgba(250, 137, 107, 0.8) 100%);
        color: white;
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        border: none;
        box-shadow: var(--shadow-md);
        font-weight: 500;
    }
    
    .stWarning {
        background: linear-gradient(135deg, var(--warning-color) 0%, rgba(255, 174, 31, 0.8) 100%);
        color: white;
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        border: none;
        box-shadow: var(--shadow-md);
        font-weight: 500;
    }
    
    .stInfo {
        background: linear-gradient(135deg, var(--info-color) 0%, rgba(83, 155, 255, 0.8) 100%);
        color: white;
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        border: none;
        box-shadow: var(--shadow-md);
        font-weight: 500;
    }
    
    /* Modern Sidebar */
    .stSidebar {
        background: var(--white);
        border-right: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
    }
    
    .stSidebar .stSelectbox {
        background: var(--white);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-xs);
    }
    
    /* Modern Plotly Charts */
    .stPlotlyChart {
        background: var(--white);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Custom Alert Styles */
    .modern-alert {
        background: var(--white);
        border-radius: var(--radius-xl);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .modern-alert::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--primary-color);
    }
    
    .modern-alert.success::before {
        background: var(--success-color);
    }
    
    .modern-alert.warning::before {
        background: var(--warning-color);
    }
    
    .modern-alert.danger::before {
        background: var(--danger-color);
    }
    
    .modern-alert:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    .alert-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--dark-color);
        margin-bottom: 0.5rem;
    }
    
    .alert-content {
        color: var(--text-muted);
        line-height: 1.6;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .modern-card {
            padding: 1.5rem;
        }
        
        .status-card {
            padding: 1.5rem;
        }
        
        .status-number {
            font-size: 2rem;
        }
    }
    
    /* Loading States */
    .loading-shimmer {
        background: linear-gradient(90deg, var(--gray-200) 25%, var(--gray-100) 50%, var(--gray-200) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: var(--radius-md);
        height: 1rem;
        margin: 0.5rem 0;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* Modern Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--dark-color);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
        position: relative;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: var(--primary-color);
    }
</style>
""", unsafe_allow_html=True)

# Keep all your existing SimpleFraudDetectionModel class here
class SimpleFraudDetectionModel:
    # [Keep your existing fraud detection code exactly as it is]
    def __init__(self):
        self.risk_score_calculated = False
        # ... [rest of your existing code]
        
    # [Include all your existing methods]
    def detect_fraud(self, df):
        # ... [keep your existing implementation]
        pass

# Updated helper functions with modern styling
def create_modern_status_display(df_analyzed):
    """Display modern status cards"""
    total_transactions = len(df_analyzed)
    
    if 'safety_level' in df_analyzed.columns:
        needs_attention = len(df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'])
        watch_closely = len(df_analyzed[df_analyzed['safety_level'] == 'Watch Closely'])
        safe_payments = len(df_analyzed[df_analyzed['safety_level'] == 'Safe'])
    else:
        needs_attention = len(df_analyzed[df_analyzed.get('risk_score', 0) > 70])
        watch_closely = len(df_analyzed[(df_analyzed.get('risk_score', 0) > 40) & (df_analyzed.get('risk_score', 0) <= 70)])
        safe_payments = len(df_analyzed[df_analyzed.get('risk_score', 0) <= 40])
    
    # Calculate money at risk
    if 'amount' in df_analyzed.columns and 'safety_level' in df_analyzed.columns:
        money_at_risk = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention']['amount'].sum()
    else:
        money_at_risk = 0
    
    # Overall status
    if needs_attention == 0:
        overall_status = "🛡️ Excellent - All payments look safe!"
        status_class = "success"
    elif needs_attention <= total_transactions * 0.05:
        overall_status = f"✅ Good - Only {needs_attention} payments need attention"
        status_class = "success"
    elif needs_attention <= total_transactions * 0.15:
        overall_status = f"⚠️ Watch - {needs_attention} payments need review"
        status_class = "warning"
    else:
        overall_status = f"🚨 Action Needed - {needs_attention} suspicious payments!"
        status_class = "danger"
    
    # Display overall status
    st.markdown(f"""
    <div class="modern-alert {status_class}">
        <div class="alert-title">Security Status</div>
        <div class="alert-content">{overall_status}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display metrics in modern cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="status-card success">
            <div class="status-number">{safe_payments:,}</div>
            <div class="status-label">Safe Payments</div>
            <div class="status-badge success">✓ Good</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        card_class = "warning" if watch_closely > 0 else "success"
        st.markdown(f"""
        <div class="status-card {card_class}">
            <div class="status-number">{watch_closely:,}</div>
            <div class="status-label">Watch Closely</div>
            <div class="status-badge {card_class}">{'⚠ Review' if watch_closely > 0 else '✓ None'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        card_class = "danger" if needs_attention > 0 else "success"
        st.markdown(f"""
        <div class="status-card {card_class}">
            <div class="status-number">{needs_attention:,}</div>
            <div class="status-label">Need Attention</div>
            <div class="status-badge {card_class}">{'🚨 Urgent' if needs_attention > 0 else '✓ None'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        money_class = "danger" if money_at_risk > 0 else "success"
        st.markdown(f"""
        <div class="status-card {money_class}">
            <div class="status-number">${money_at_risk:,.0f}</div>
            <div class="status-label">Money at Risk</div>
            <div class="status-badge {money_class}">{'💰 Review' if money_at_risk > 0 else '✓ Safe'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    return needs_attention, safe_payments, money_at_risk

def create_modern_charts(df_analyzed):
    """Create modern charts with better styling"""
    
    # Daily transactions chart
    if 'transaction_date' in df_analyzed.columns:
        daily_counts = df_analyzed.groupby('transaction_date').size().reset_index(name='transactions')
        
        fig_daily = px.bar(
            daily_counts,
            x='transaction_date',
            y='transactions',
            title='📊 Daily Payment Activity',
            color_discrete_sequence=['#5d87ff']
        )
        
        fig_daily.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=20,
            title_font_color='#2a3547',
            title_font_family='Plus Jakarta Sans',
            font_family='Plus Jakarta Sans',
            font_size=12,
            height=400,
            showlegend=False,
            xaxis_title="Date",
            yaxis_title="Number of Payments",
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        fig_daily.update_traces(
            marker_line_color='#0284c7',
            marker_line_width=1,
            hovertemplate='<b>%{x}</b><br>Payments: %{y}<extra></extra>'
        )
        
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_daily, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Safety overview chart
    if 'safety_level' in df_analyzed.columns:
        safety_counts = df_analyzed['safety_level'].value_counts()
        
        fig_safety = px.pie(
            values=safety_counts.values,
            names=safety_counts.index,
            title='🛡️ Payment Safety Overview',
            color_discrete_map={
                'Safe': '#13deb9',
                'Watch Closely': '#ffae1f',
                'Needs Your Attention': '#fa896b'
            }
        )
        
        fig_safety.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=20,
            title_font_color='#2a3547',
            title_font_family='Plus Jakarta Sans',
            font_family='Plus Jakarta Sans',
            font_size=12,
            height=400,
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        fig_safety.update_traces(
            textinfo='label+percent',
            textfont_size=12,
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_safety, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def display_modern_risky_transactions(df_analyzed, needs_attention):
    """Display risky transactions with modern styling"""
    
    if needs_attention > 0:
        st.markdown('<div class="section-header">🔍 Transactions That Need Your Attention</div>', unsafe_allow_html=True)
        
        # Get risky transactions
        if 'safety_level' in df_analyzed.columns:
            risky_transactions = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention']
        else:
            risky_transactions = df_analyzed[df_analyzed['risk_score'] > 70]
        
        # Display in modern tabs
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Details", "📈 Analysis"])
        
        with tab1:
            # Quick overview
            total_risk_amount = risky_transactions['amount'].sum()
            avg_risk_score = risky_transactions['risk_score'].mean()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("💰 Total at Risk", f"${total_risk_amount:,.2f}")
            with col2:
                st.metric("📊 Avg Risk Score", f"{avg_risk_score:.1f}/100")
            with col3:
                st.metric("🚨 Transactions", f"{len(risky_transactions)}")
        
        with tab2:
            # Detailed view with modern styling
            for idx, (_, row) in enumerate(risky_transactions.iterrows()):
                amount = row.get('amount', 0)
                customer_name = row.get('customer_name', 'Unknown')
                risk_score = row.get('risk_score', 0)
                anomalies = row.get('anomaly_flags', 'No details available')
                
                with st.expander(f"💰 ${amount:,.2f} - {customer_name} (Risk: {risk_score}/100)"):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.markdown("**Transaction Details:**")
                        st.write(f"• **Date:** {row.get('transaction_date', 'N/A')}")
                        st.write(f"• **Time:** {row.get('transaction_time', 'N/A')}")
                        st.write(f"• **Customer:** {customer_name}")
                        st.write(f"• **Amount:** ${amount:,.2f}")
                    
                    with col_b:
                        st.markdown("**Risk Factors:**")
                        if anomalies and anomalies != 'None detected':
                            factors = anomalies.split(';')
                            for factor in factors[:3]:  # Show top 3
                                st.write(f"⚠️ {factor.strip()}")
                        else:
                            st.write("⚠️ General risk pattern detected")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✅ Mark Safe", key=f"safe_{idx}"):
                            st.success("Marked as safe")
                    with col2:
                        if st.button("📞 Contact", key=f"contact_{idx}"):
                            st.info("Customer contacted")
                    with col3:
                        if st.button("🚫 Block", key=f"block_{idx}"):
                            st.error("Transaction blocked")
        
        with tab3:
            # Risk analysis
            st.markdown("**Risk Level Distribution**")
            
            high_risk = len(risky_transactions[risky_transactions['risk_score'] >= 80])
            medium_risk = len(risky_transactions[risky_transactions['risk_score'] < 80])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🔴 Very High Risk", f"{high_risk} transactions")
            with col2:
                st.metric("🟡 High Risk", f"{medium_risk} transactions")

# Main app with modern styling
def main():
    # Modern Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ FraudGuard Pro</h1>
        <p>AI-Powered Fraud Detection for Small Business</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern file upload
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Upload Your Transaction Data")
    st.markdown("Upload your CSV file to analyze payments for potential fraud")
    
    uploaded_file = st.file_uploader(
        "Choose your transaction file",
        type="csv",
        help="Upload a CSV file with your payment transaction data"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Load and process data
            with st.spinner("🔍 Analyzing your transactions..."):
                df = pd.read_csv(uploaded_file)
                
                # Add validation and processing here
                # [Include your existing data validation logic]
                
                # Run fraud detection
                fraud_model = SimpleFraudDetectionModel()
                df_analyzed = fraud_model.detect_fraud(df)
            
            st.success(f"✅ Analyzed {len(df):,} transactions successfully!")
            
            # Display modern status
            needs_attention, safe_payments, money_at_risk = create_modern_status_display(df_analyzed)
            
            # Create modern charts
            create_modern_charts(df_analyzed)
            
            # Display risky transactions
            display_modern_risky_transactions(df_analyzed, needs_attention)
            
            # Download button
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            if st.button("📥 Download Detailed Report"):
                csv = df_analyzed.to_csv(index=False)
                st.download_button(
                    label="Download Full Analysis",
                    data=csv,
                    file_name=f"fraud_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("💡 Please ensure your CSV file has the required columns")
    
    else:
        # Show requirements with modern styling
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 📋 What You Need")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Required Columns:**
            - `transaction_id` - Unique identifier
            - `amount` - Payment amount
            - `transaction_date` - Date of transaction
            - `transaction_time` - Time of transaction
            """)
        
        with col2:
            st.markdown("""
            **Optional (for better detection):**
            - `customer_state` - Customer's state
            - `customer_zip_code` - ZIP code
            - `customer_ip_address` - IP address
            - `merchant_category` - Business type
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample data
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Sample Data Format")
        
        sample_data = {
            'transaction_id': ['TXN_001', 'TXN_002', 'TXN_003'],
            'amount': [45.67, 1250.00, 23.50],
            'transaction_date': ['2024-01-15', '2024-01-15', '2024-01-16'],
            'transaction_time': ['14:30:00', '23:45:00', '08:15:00'],
            'customer_state': ['CA', 'NY', 'TX'],
            'customer_zip_code': ['90210', '10001', '77001']
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()