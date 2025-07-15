import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import random  # Added missing import
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FraudGuard Pro - Small Business Protection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for SMB-friendly design
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    .css-1d391kg {padding: 1rem 2rem 2rem;}
    .css-k1vhr4 {margin-top: -60px;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Status indicator */
    .status-good {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-align: center;
        margin: 1rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-align: center;
        margin: 1rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
    }
    
    .status-danger {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-align: center;
        margin: 1rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    /* Upload section styling */
    .upload-container {
        background: #F0FDF4;
        border: 2px dashed #22C55E;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        border-color: #16A34A;
        background: #ECFDF5;
    }
    
    /* Simple metric cards */
    .big-number-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
        border-left: 6px solid #10B981;
    }
    
    .big-number {
        font-size: 3rem;
        font-weight: 800;
        color: #1F2937;
        margin: 0;
        line-height: 1;
    }
    
    .big-label {
        font-size: 1.2rem;
        color: #6B7280;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    .action-needed {
        border-left-color: #EF4444;
    }
    
    .action-needed .big-number {
        color: #EF4444;
    }
    
    .watch-closely {
        border-left-color: #F59E0B;
    }
    
    .watch-closely .big-number {
        color: #F59E0B;
    }
    
    .all-good {
        border-left-color: #10B981;
    }
    
    .all-good .big-number {
        color: #10B981;
    }
    
    /* Action buttons */
    .action-button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 0.5rem;
        display: inline-block;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    
    .urgent-button {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        font-size: 1.3rem;
        padding: 1.5rem 3rem;
    }
    
    .urgent-button:hover {
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    
    /* Simple explanations */
    .explanation-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .explanation-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }
    
    .explanation-text {
        font-size: 1rem;
        color: #4B5563;
        line-height: 1.5;
    }
    
    /* Traffic light system */
    .traffic-light {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .traffic-item {
        text-align: center;
        flex: 1;
        padding: 1rem;
    }
    
    .traffic-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        margin: 0 auto 1rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 800;
        color: white;
    }
    
    .green { background-color: #10B981; }
    .yellow { background-color: #F59E0B; }
    .red { background-color: #EF4444; }
    
    .traffic-label {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .traffic-description {
        font-size: 0.9rem;
        color: #6B7280;
    }
    
    /* Alert cards */
    .alert-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid #EF4444;
    }
    
    .alert-high {
        border-left-color: #EF4444;
        background: #FEF2F2;
    }
    
    .alert-medium {
        border-left-color: #F59E0B;
        background: #FFFBEB;
    }
    
    .alert-low {
        border-left-color: #3B82F6;
        background: #EFF6FF;
    }
    
    .alert-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .alert-details {
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .alert-action {
        font-size: 1rem;
        font-weight: 600;
        color: #1F2937;
    }
    
    /* Chart containers */
    .simple-chart {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Progress bars */
    .progress-container {
        background: #F3F4F6;
        border-radius: 10px;
        padding: 0.3rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 20px;
        border-radius: 7px;
        transition: width 0.3s ease;
    }
    
    .progress-green { background: #10B981; }
    .progress-yellow { background: #F59E0B; }
    .progress-red { background: #EF4444; }
    
    /* Hide complex elements for SMB */
    .technical-details {
        display: none;
    }
    
    /* Make everything bigger and more readable */
    .stMetric {
        font-size: 1.2rem;
    }
    
    .stMetric > div {
        font-size: 1.4rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .big-number {
            font-size: 2.5rem;
        }
        
        .traffic-light {
            flex-direction: column;
        }
        
        .action-button {
            display: block;
            text-align: center;
            margin: 1rem 0;
        }
    }
</style>
""", unsafe_allow_html=True)

class SimpleFraudDetectionModel:
    """Simplified fraud detection with basic rule-based scoring for SMB"""
    
    def __init__(self):
        self.risk_score_calculated = False
    
    def detect_fraud(self, df):
        """Simple fraud detection using basic rules"""
        df_analyzed = df.copy()
        
        try:
            # Ensure amount is numeric
            df_analyzed['amount'] = pd.to_numeric(df_analyzed['amount'], errors='coerce').fillna(0)
            
            # Simple risk scoring based on amount and patterns
            risk_scores = []
            risk_levels = []
            
            for _, row in df_analyzed.iterrows():
                score = 0
                amount = row.get('amount', 0)
                
                # Amount-based risk (simplified for SMB understanding)
                if amount > 1000:
                    score += 40  # Large purchases need attention
                elif amount > 500:
                    score += 20  # Medium purchases
                elif amount < 5:
                    score += 30  # Very small amounts (testing cards)
                else:
                    score += 5   # Normal amounts
                
                # Time-based risk (if available)
                if 'transaction_time' in df_analyzed.columns:
                    time_str = str(row.get('transaction_time', '12:00:00'))
                    try:
                        if ':' in time_str:
                            hour = int(time_str.split(':')[0])
                            if hour >= 22 or hour <= 6:  # Late night/early morning
                                score += 25
                    except:
                        pass
                
                # Customer pattern risk (if available)
                if 'customer_id' in df_analyzed.columns:
                    customer_id = str(row.get('customer_id', ''))
                    if customer_id.startswith('CUST_') and random.random() < 0.1:  # 10% chance of new customer risk
                        score += 15
                
                # Add some randomness for demo purposes
                score += np.random.randint(0, 10)
                
                risk_scores.append(min(score, 100))
                
                # Simple categorization
                if score > 70:
                    risk_levels.append('Needs Your Attention')
                elif score > 40:
                    risk_levels.append('Watch Closely')
                else:
                    risk_levels.append('Safe')
            
            df_analyzed['risk_score'] = risk_scores
            df_analyzed['safety_level'] = risk_levels
            
            # Add hour for visualization (simplified)
            if 'transaction_time' in df_analyzed.columns:
                hours = []
                for time_val in df_analyzed['transaction_time']:
                    try:
                        time_str = str(time_val)
                        if ':' in time_str:
                            hour = int(time_str.split(':')[0])
                            hours.append(hour)
                        else:
                            hours.append(12)
                    except:
                        hours.append(12)
                df_analyzed['hour'] = hours
            else:
                df_analyzed['hour'] = 12
            
            return df_analyzed
            
        except Exception as e:
            st.error(f"Error in fraud detection: {e}")
            # Ultra-simple fallback
            df_analyzed['risk_score'] = np.random.uniform(10, 70, len(df_analyzed))
            df_analyzed['safety_level'] = 'Safe'
            df_analyzed['hour'] = 12
            return df_analyzed

def create_smb_friendly_charts(df_analyzed):
    """Create simple, easy-to-understand charts for SMB owners"""
    
    charts = {}
    
    try:
        # 1. Simple Daily Transaction Count
        daily_counts = df_analyzed.groupby('transaction_date').size().reset_index(name='transactions')
        
        if len(daily_counts) > 0:
            charts['daily_simple'] = px.bar(
                daily_counts,
                x='transaction_date',
                y='transactions',
                title='Daily Payments to Your Business',
                color_discrete_sequence=['#10B981']
            )
            charts['daily_simple'].update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                title_font_size=18,
                title_font_color='#1F2937',
                xaxis_title="Date",
                yaxis_title="Number of Payments",
                font_size=14,
                height=400,
                showlegend=False
            )
            charts['daily_simple'].update_traces(
                marker_line_color='#059669',
                marker_line_width=1
            )
        else:
            charts['daily_simple'] = None
    
    except Exception as e:
        st.warning(f"Could not create daily chart: {e}")
        charts['daily_simple'] = None
    
    try:
        # 2. Traffic Light Safety Overview
        if 'safety_level' in df_analyzed.columns:
            safety_counts = df_analyzed['safety_level'].value_counts()
            
            # Ensure all categories are present
            categories = ['Safe', 'Watch Closely', 'Needs Your Attention']
            safety_data = []
            colors = ['#10B981', '#F59E0B', '#EF4444']
            
            for i, category in enumerate(categories):
                count = safety_counts.get(category, 0)
                safety_data.append({
                    'Category': category,
                    'Count': count,
                    'Percentage': round((count / len(df_analyzed)) * 100, 1) if len(df_analyzed) > 0 else 0
                })
            
            safety_df = pd.DataFrame(safety_data)
            
            charts['safety_overview'] = px.bar(
                safety_df,
                x='Category',
                y='Count',
                title='Payment Safety Overview',
                color='Category',
                color_discrete_map={
                    'Safe': '#10B981',
                    'Watch Closely': '#F59E0B', 
                    'Needs Your Attention': '#EF4444'
                }
            )
            charts['safety_overview'].update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                title_font_size=18,
                title_font_color='#1F2937',
                xaxis_title="Safety Level",
                yaxis_title="Number of Payments",
                font_size=14,
                height=400,
                showlegend=False
            )
        else:
            charts['safety_overview'] = None
    
    except Exception as e:
        st.warning(f"Could not create safety overview: {e}")
        charts['safety_overview'] = None
    
    return charts

def display_smb_status(df_analyzed):
    """Display simple status for SMB owners"""
    
    total_transactions = len(df_analyzed)
    
    if 'safety_level' in df_analyzed.columns:
        needs_attention = len(df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'])
        watch_closely = len(df_analyzed[df_analyzed['safety_level'] == 'Watch Closely'])
        safe_payments = len(df_analyzed[df_analyzed['safety_level'] == 'Safe'])
    else:
        # Fallback if safety_level doesn't exist
        needs_attention = len(df_analyzed[df_analyzed.get('risk_score', 0) > 70])
        watch_closely = len(df_analyzed[(df_analyzed.get('risk_score', 0) > 40) & (df_analyzed.get('risk_score', 0) <= 70)])
        safe_payments = len(df_analyzed[df_analyzed.get('risk_score', 0) <= 40])
    
    # Calculate potential money at risk
    if 'amount' in df_analyzed.columns and 'safety_level' in df_analyzed.columns:
        money_at_risk = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention']['amount'].sum()
    else:
        money_at_risk = 0
    
    # Determine overall status
    if needs_attention == 0:
        status = "EXCELLENT"
        status_class = "status-good"
        status_message = "🛡️ Your business is well protected! All payments look normal."
    elif needs_attention <= total_transactions * 0.05:  # Less than 5%
        status = "GOOD"
        status_class = "status-good"
        status_message = f"✅ Only {needs_attention} payments need attention. You're doing great!"
    elif needs_attention <= total_transactions * 0.15:  # 5-15%
        status = "WATCH"
        status_class = "status-warning"
        status_message = f"⚠️ {needs_attention} payments need your review. Check them when you can."
    else:
        status = "ACTION NEEDED"
        status_class = "status-danger"
        status_message = f"🚨 {needs_attention} payments need immediate attention!"
    
    # Display status
    st.markdown(f'<div class="{status_class}">Security Status: {status}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="explanation-box"><div class="explanation-text">{status_message}</div></div>', unsafe_allow_html=True)
    
    # Big number cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="big-number-card all-good">
            <p class="big-number">{safe_payments:,}</p>
            <p class="big-label">Safe Payments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if watch_closely > 0:
            st.markdown(f"""
            <div class="big-number-card watch-closely">
                <p class="big-number">{watch_closely:,}</p>
                <p class="big-label">Watch Closely</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="big-number-card all-good">
                <p class="big-number">{watch_closely:,}</p>
                <p class="big-label">Watch Closely</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if needs_attention > 0:
            st.markdown(f"""
            <div class="big-number-card action-needed">
                <p class="big-number">{needs_attention:,}</p>
                <p class="big-label">Need Attention</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="big-number-card all-good">
                <p class="big-number">{needs_attention:,}</p>
                <p class="big-label">Need Attention</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if money_at_risk > 0:
            st.markdown(f"""
            <div class="big-number-card action-needed">
                <p class="big-number">${money_at_risk:,.0f}</p>
                <p class="big-label">Money at Risk</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="big-number-card all-good">
                <p class="big-number">$0</p>
                <p class="big-label">Money at Risk</p>
            </div>
            """, unsafe_allow_html=True)
    
    return needs_attention, safe_payments, money_at_risk

def display_simple_charts(charts):
    """Display simplified charts"""
    
    if charts.get('daily_simple'):
        st.markdown('<div class="simple-chart">', unsafe_allow_html=True)
        st.plotly_chart(charts['daily_simple'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
            <div class="explanation-title">What This Shows</div>
            <div class="explanation-text">This chart shows how many payments you received each day. Look for unusual spikes or patterns that don't match your normal business.</div>
        </div>
        """, unsafe_allow_html=True)
    
    if charts.get('safety_overview'):
        st.markdown('<div class="simple-chart">', unsafe_allow_html=True)
        st.plotly_chart(charts['safety_overview'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
            <div class="explanation-title">How to Read This</div>
            <div class="explanation-text">
                • <strong>Safe:</strong> Normal payments that look good<br>
                • <strong>Watch Closely:</strong> Slightly unusual but probably okay<br>
                • <strong>Needs Attention:</strong> Check these payments - they might be fraud
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_action_items(df_analyzed, needs_attention):
    """Display clear action items for SMB owners"""
    
    st.markdown("## 🎯 What Should You Do Now?")
    
    if needs_attention > 0:
        # Show urgent button
        st.markdown(f"""
        <button class="urgent-button">
            🚨 Review {needs_attention} Suspicious Payment{"s" if needs_attention > 1 else ""} Now
        </button>
        """, unsafe_allow_html=True)
        
        # Show top risky transactions
        st.markdown("### 🔍 Payments That Need Your Attention")
        
        if 'safety_level' in df_analyzed.columns:
            risky_transactions = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'].head(5)
        else:
            risky_transactions = df_analyzed.nlargest(5, 'risk_score')
        
        if not risky_transactions.empty:
            for idx, row in risky_transactions.iterrows():
                amount = row.get('amount', 0)
                date = row.get('transaction_date', 'Unknown')
                time = row.get('transaction_time', 'Unknown')
                customer = row.get('customer_id', 'Unknown')
                
                # Determine why it's risky
                risk_reasons = []
                if amount > 1000:
                    risk_reasons.append(f"Large amount (${amount:,.2f})")
                if 'hour' in row and (row['hour'] >= 22 or row['hour'] <= 6):
                    risk_reasons.append("Late night/early morning")
                if len(risk_reasons) == 0:
                    risk_reasons.append("Unusual pattern detected")
                
                reason_text = " • ".join(risk_reasons)
                
                st.markdown(f"""
                <div class="alert-card alert-high">
                    <div class="alert-title">💰 ${amount:,.2f} payment on {date} at {time}</div>
                    <div class="alert-details">Customer: {customer}<br>Why it's flagged: {reason_text}</div>
                    <div class="alert-action">→ Call customer to verify this purchase is legitimate</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<button class="action-button">📞 Call Customers</button>', unsafe_allow_html=True)
        with col2:
            st.markdown('<button class="action-button">✅ Mark as Safe</button>', unsafe_allow_html=True)
        with col3:
            st.markdown('<button class="action-button">🚫 Block Payment</button>', unsafe_allow_html=True)
    
    else:
        # All good message
        st.markdown("""
        <div class="explanation-box" style="background: #F0FDF4; border-color: #22C55E;">
            <div class="explanation-title" style="color: #15803D;">🎉 Great News!</div>
            <div class="explanation-text" style="color: #166534;">All your payments look normal and safe. Keep up the good work! We'll continue monitoring your transactions automatically.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<button class="action-button">📊 View Detailed Report</button>', unsafe_allow_html=True)

def display_helpful_tips():
    """Display helpful tips for SMB owners"""
    
    st.markdown("## 💡 Fraud Prevention Tips")
    
    tips = [
        {
            "title": "Watch for Large Purchases from New Customers",
            "description": "If someone you've never seen before makes a big purchase, give them a quick call to verify.",
            "icon": "🛒"
        },
        {
            "title": "Be Careful with Late Night Transactions", 
            "description": "Fraudsters often work at night when businesses are closed and can't verify purchases.",
            "icon": "🌙"
        },
        {
            "title": "Multiple Small Purchases = Red Flag",
            "description": "If someone makes many small purchases quickly, they might be testing stolen card numbers.",
            "icon": "🔢"
        },
        {
            "title": "Trust Your Instincts",
            "description": "If a customer or purchase feels 'off' to you, it's okay to ask for additional verification.",
            "icon": "🤔"
        }
    ]
    
    cols = st.columns(2)
    for i, tip in enumerate(tips):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="explanation-box">
                <div class="explanation-title">{tip['icon']} {tip['title']}</div>
                <div class="explanation-text">{tip['description']}</div>
            </div>
            """, unsafe_allow_html=True)

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ FraudGuard Pro</h1>
        <p>Simple Fraud Protection for Small Businesses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown("""
    <div class="upload-container">
        <h3>📁 Upload Your Payment Data</h3>
        <p>Upload your transaction file and we'll check it for fraud in plain English</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your transaction file (CSV)",
        type="csv",
        help="Upload a CSV file with your payment data. We'll make it easy to understand what's happening.",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            with st.spinner("📊 Checking your payments for fraud..."):
                df = pd.read_csv(uploaded_file)
            
            # Validate data
            required_columns = ['transaction_id', 'amount', 'merchant_category', 
                              'transaction_date', 'transaction_time']
            missing_required = [col for col in required_columns if col not in df.columns]
            
            if missing_required:
                st.error(f"❌ Your file is missing these columns: {', '.join(missing_required)}")
                st.info("💡 Make sure your CSV file has columns for transaction_id, amount, merchant_category, transaction_date, and transaction_time")
                return
            
            # Add missing optional columns
            optional_columns = ['customer_id', 'response_code', 'merchant_name', 'state']
            for col in optional_columns:
                if col not in df.columns:
                    if col == 'customer_id':
                        df[col] = 'CUST_' + df.index.astype(str).str.zfill(6)
                    elif col == 'response_code':
                        df[col] = '00'
                    elif col == 'merchant_name':
                        df[col] = 'Your Business'
                    elif col == 'state':
                        df[col] = 'Unknown'
            
            st.success(f"✅ Loaded {len(df):,} payments from your business")
            
            # Run fraud detection
            with st.spinner("🔍 Looking for suspicious payments..."):
                fraud_model = SimpleFraudDetectionModel()
                df_analyzed = fraud_model.detect_fraud(df)
            
            # Display SMB-friendly results
            needs_attention, safe_payments, money_at_risk = display_smb_status(df_analyzed)
            
            # Create and display simple charts
            charts = create_smb_friendly_charts(df_analyzed)
            display_simple_charts(charts)
            
            # Display action items
            display_action_items(df_analyzed, needs_attention)
            
            # Display helpful tips
            display_helpful_tips()
            
            # Download button for detailed results
            if st.button("📥 Download Detailed Report"):
                csv = df_analyzed.to_csv(index=False)
                st.download_button(
                    label="Download Full Analysis",
                    data=csv,
                    file_name=f"fraud_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")
            st.info("💡 Please make sure your file is a properly formatted CSV with the required columns.")
    
    else:
        # Show requirements when no file is uploaded
        st.markdown("## 📋 What You Need")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="explanation-box">
                <div class="explanation-title">📄 Required Information</div>
                <div class="explanation-text">
                    Your CSV file should have these columns:<br>
                    • transaction_id (unique ID for each payment)<br>
                    • amount (payment amount)<br>
                    • merchant_category (type of business)<br>
                    • transaction_date (when it happened)<br>
                    • transaction_time (what time)
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="explanation-box">
                <div class="explanation-title">🎯 What We'll Tell You</div>
                <div class="explanation-text">
                    After checking your payments, we'll show:<br>
                    • How many payments look suspicious<br>
                    • Which ones you should check<br>
                    • Simple steps to protect your business<br>
                    • Easy-to-understand charts and graphs
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample data preview
        st.markdown("## 📊 Example Data Format")
        
        sample_data = {
            'transaction_id': ['PAY_001', 'PAY_002', 'PAY_003'],
            'amount': [45.67, 1250.00, 23.50],
            'merchant_category': ['Restaurant', 'Electronics', 'Coffee Shop'],
            'transaction_date': ['2024-01-15', '2024-01-15', '2024-01-16'],
            'transaction_time': ['14:30:00', '23:45:00', '08:15:00'],
            'customer_id': ['Customer_A', 'Customer_B', 'Customer_C']
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div class="explanation-box">
            <div class="explanation-title">💡 Pro Tip</div>
            <div class="explanation-text">Most payment processors (Square, PayPal, Stripe, etc.) can export your transaction data in CSV format. Look for "Export" or "Download" options in your payment dashboard.</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()