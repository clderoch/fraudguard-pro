import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import io

# Page configuration
st.set_page_config(
    page_title="FraudGuard Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .risk-high { 
        background-color: #fee; 
        color: #c53030; 
        padding: 0.25rem 0.5rem; 
        border-radius: 0.25rem; 
        font-weight: bold;
    }
    .risk-medium { 
        background-color: #fef5e7; 
        color: #dd6b20; 
        padding: 0.25rem 0.5rem; 
        border-radius: 0.25rem; 
        font-weight: bold;
    }
    .risk-low { 
        background-color: #f0fff4; 
        color: #38a169; 
        padding: 0.25rem 0.5rem; 
        border-radius: 0.25rem; 
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame({
        'transaction_id': ['TXN-2024-001', 'TXN-2024-002', 'TXN-2024-003', 'TXN-2024-004', 'TXN-2024-005'],
        'amount': [2850.00, 1200.00, 450.00, 890.00, 3200.00],
        'merchant': ['Electronics Store', 'Online Retailer', 'Restaurant', 'Gas Station', 'Luxury Goods'],
        'date': ['2024-07-10', '2024-07-10', '2024-07-09', '2024-07-09', '2024-07-08'],
        'risk_score': [87, 65, 25, 45, 92],
        'status': ['Under Review', 'Monitoring', 'Approved', 'Approved', 'Blocked'],
        'card_type': ['Visa', 'Mastercard', 'American Express', 'Visa', 'Mastercard'],
        'location': ['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Miami, FL'],
        'ip_address': ['192.168.1.100', '192.168.1.200', '192.168.1.300', '192.168.1.400', '192.168.1.500'],
        'device_id': ['DEV-12345', 'DEV-67890', 'DEV-11111', 'DEV-22222', 'DEV-33333']
    })

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant", 
            "content": "👋 Hi! I'm your FraudGuard Assistant. I can help you analyze transactions, understand risk scores, and provide insights about your fraud prevention. How can I assist you today?"
        }
    ]

if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        'total_transactions': 1247,
        'high_risk_count': 23,
        'chargebacks_prevented': 15,
        'savings_amount': 3750,
        'false_positive_rate': 8.2,
        'accuracy_rate': 94.7
    }

# Helper functions
def get_risk_category(score):
    if score >= 70:
        return "🔴 High Risk", "risk-high"
    elif score >= 40:
        return "🟡 Medium Risk", "risk-medium"
    else:
        return "🟢 Low Risk", "risk-low"

def format_currency(amount):
    return f"${amount:,.2f}"

def get_risk_factors_explanation(risk_score):
    if risk_score >= 85:
        return """• **Very High Amount:** Transaction significantly above customer's typical spending pattern
• **New Device:** First transaction from this device fingerprint
• **Suspicious Location:** Transaction from high-risk geographic region
• **Velocity Alert:** Multiple transactions in short time period
• **IP Risk:** Transaction from known proxy/VPN service"""
    elif risk_score >= 70:
        return """• **High Amount:** Transaction above average for this merchant category
• **Geographic Anomaly:** Transaction from unusual location for this customer
• **Time Pattern:** Transaction outside normal business hours
• **Device Risk:** Inconsistent device characteristics"""
    elif risk_score >= 40:
        return """• **Moderate Amount:** Slightly elevated transaction amount
• **New Location:** Transaction from new but not high-risk location
• **Velocity Check:** Moderate transaction frequency"""
    else:
        return """• **Normal Pattern:** Transaction consistent with customer history
• **Known Device:** Transaction from recognized device
• **Standard Location:** Transaction from customer's typical geographic area
• **Appropriate Amount:** Transaction amount within normal range"""

def get_action_recommendations(risk_score):
    if risk_score >= 85:
        return """• **IMMEDIATE ACTION REQUIRED:** Contact customer within 1 hour
• **Verify Identity:** Request additional authentication
• **Consider Blocking:** If unable to verify quickly
• **Monitor Closely:** Watch for additional suspicious activity"""
    elif risk_score >= 70:
        return """• **Review Within 24 Hours:** Analyze transaction details
• **Customer Contact:** Consider calling customer for verification
• **Enhanced Monitoring:** Flag account for additional scrutiny
• **Documentation:** Record findings for future reference"""
    elif risk_score >= 40:
        return """• **Monitor Transaction:** Keep under standard surveillance
• **Automated Checks:** Let system continue monitoring
• **No Immediate Action:** But review if pattern emerges"""
    else:
        return """• **Approve Transaction:** Low risk, normal processing
• **Standard Monitoring:** Continue routine surveillance
• **Positive Signal:** Use to improve customer profile"""

def generate_ai_response(user_message):
    message = user_message.lower()
    
    if 'risk' in message or 'score' in message:
        return """🎯 **Risk Analysis Insights:**

Based on your current data, you have 23 high-risk transactions (score 70+) that need immediate review. Here's what I'm seeing:

**Top Risk Factors:**
• High transaction amounts (>$2,000) - 45% of flagged transactions
• New device fingerprints - 32% of flagged transactions  
• Unusual geographic patterns - 28% of flagged transactions
• Velocity anomalies - 23% of flagged transactions

**Recommendations:**
• Review transactions with scores above 85 within 2 hours
• Set up automated blocking for scores above 95
• Consider additional verification for amounts over $2,500

Would you like me to analyze a specific transaction or show detailed risk factor breakdown?"""
    
    elif 'chargeback' in message or 'dispute' in message:
        return """💳 **Chargeback Prevention Summary:**

Excellent news! Your fraud prevention is performing exceptionally well:

**This Month's Performance:**
• **15 chargebacks prevented** - saving you $3,750 in fees
• **94.7% accuracy rate** in fraud detection
• **8.2% false positive rate** - industry leading
• **Average response time:** 2.3 minutes for high-risk alerts

**Financial Impact:**
• Direct savings: $3,750 (chargeback fees avoided)
• Indirect savings: ~$11,250 (lost merchandise + processing costs)
• **Total monthly impact: $15,000 saved**

I recommend reviewing transactions with scores above 75 within 24 hours for optimal prevention rates."""
    
    elif 'trend' in message or 'pattern' in message:
        return """📊 **Fraud Pattern Analysis:**

I've identified several important trends in your recent transaction data:

**Emerging Patterns:**
• **45% increase** in card-not-present fraud attempts (last 30 days)
• **Peak risk hours:** 2-4 AM and 11 PM-1 AM EST
• **Geographic hotspots:** 3 new high-risk IP ranges detected
• **Device patterns:** 67% of fraud attempts from mobile devices

**Positive Indicators:**
• Overall fraud rate decreased 12% this month
• Customer education reducing false disputes
• Faster merchant response times improving outcomes"""
    
    elif 'save' in message or 'money' in message or 'roi' in message:
        return """💰 **ROI & Cost Savings Analysis:**

Your FraudGuard Pro investment is delivering exceptional returns:

**Monthly Financial Impact:**
• **Monthly subscription:** $299 (Professional Plan)
• **Chargeback fees saved:** $3,750
• **Lost merchandise prevented:** $8,200
• **Processing cost savings:** $1,150
• **Net monthly savings:** $12,801

**Annual Projections:**
• **Projected annual savings:** $153,612
• **ROI:** 4,184% return on investment
• **Payback period:** 5.6 days"""
    
    else:
        return f"""🤖 I understand you're asking about "{user_message}". 

Based on your current fraud detection data, I can provide insights about:
• Risk scores and transaction analysis
• Chargeback prevention strategies  
• Fraud pattern identification
• ROI and savings calculations

What specific aspect would you like to explore?"""

# Header
st.markdown("""
<div class="main-header">
    <h1>🛡️ FraudGuard Pro</h1>
    <p>AI-powered fraud detection for small and medium businesses</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🧭 Navigation")
    page = st.selectbox(
        "Choose a page", 
        ["📊 Dashboard", "📤 Upload Transactions", "🔍 Transaction Analysis", "🤖 AI Assistant", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.subheader("📈 Quick Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Transactions", "1,247", "+12.3%")
        st.metric("Monthly Savings", "$3,750", "+32.1%")
    with col2:
        st.metric("High Risk Flagged", "23", "-8.1%")
        st.metric("Accuracy Rate", "94.7%", "+2.1%")
    
    st.markdown("---")
    st.subheader("🟢 System Status")
    st.success("All systems operational")
    st.info("Last updated: " + datetime.now().strftime("%H:%M:%S"))

# Main content based on page selection
if page == "📊 Dashboard":
    st.title("📊 Dashboard Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💳 Total Transactions",
            value=f"{st.session_state.metrics['total_transactions']:,}",
            delta="12.3%"
        )
    
    with col2:
        st.metric(
            label="⚠️ High Risk Flagged",
            value=str(st.session_state.metrics['high_risk_count']),
            delta="-8.1%"
        )
    
    with col3:
        st.metric(
            label="🛡️ Chargebacks Prevented",
            value=str(st.session_state.metrics['chargebacks_prevented']),
            delta="45.2%"
        )
    
    with col4:
        st.metric(
            label="💰 Monthly Savings",
            value=format_currency(st.session_state.metrics['savings_amount']),
            delta="32.1%"
        )
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Risk Score Distribution")
        risk_data = pd.DataFrame({
            'Risk Level': ['Low Risk (0-30)', 'Medium Risk (31-70)', 'High Risk (71-100)'],
            'Count': [820, 204, 23]
        })
        
        fig = px.pie(
            risk_data, 
            values='Count', 
            names='Risk Level',
            color_discrete_sequence=['#48bb78', '#ed8936', '#f56565'],
            title="Distribution of Transaction Risk Levels"
        )
        fig.update_layout(showlegend=True, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Transaction Volume Trends")
        trend_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            'Total Transactions': [850, 920, 1100, 1050, 1200, 1180, 1247],
            'High Risk Flagged': [45, 38, 52, 41, 35, 28, 23]
        })
        
        fig = px.line(
            trend_data, 
            x='Month', 
            y=['Total Transactions', 'High Risk Flagged'],
            title="7-Month Transaction Trends",
            color_discrete_sequence=['#667eea', '#f56565']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent transactions table
    st.markdown("---")
    st.subheader("🚨 Recent High-Risk Transactions")
    
    high_risk_transactions = st.session_state.transactions[
        st.session_state.transactions['risk_score'] >= 60
    ].copy()
    
    high_risk_transactions['risk_level'] = high_risk_transactions['risk_score'].apply(
        lambda x: get_risk_category(x)[0]
    )
    
    high_risk_transactions['formatted_amount'] = high_risk_transactions['amount'].apply(format_currency)
    
    st.dataframe(
        high_risk_transactions[['transaction_id', 'formatted_amount', 'merchant', 'date', 'risk_score', 'risk_level', 'status']].rename(columns={
            'transaction_id': 'Transaction ID',
            'formatted_amount': 'Amount',
            'merchant': 'Merchant',
            'date': 'Date',
            'risk_score': 'Risk Score',
            'risk_level': 'Risk Level',
            'status': 'Status'
        }),
        use_container_width=True,
        height=300
    )

elif page == "📤 Upload Transactions":
    st.title("📤 Upload Transaction Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📁 File Upload")
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your transaction data for fraud analysis"
        )
        
        if uploaded_file is not None:
            st.success("✅ File uploaded successfully!")
            
            with st.spinner('🔄 Processing transactions...'):
                time.sleep(2)
                
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.success(f"✅ Successfully loaded {len(df):,} transactions")
                    
                    st.subheader("👀 Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    if st.button("🔍 Run Fraud Analysis", type="primary"):
                        with st.spinner('🧠 Analyzing for fraud patterns...'):
                            time.sleep(3)
                            
                            df['risk_score'] = np.random.randint(0, 100, len(df))
                            df['risk_level'] = df['risk_score'].apply(lambda x: get_risk_category(x)[0])
                            
                            high_risk_count = len(df[df['risk_score'] >= 70])
                            
                            st.success("🎯 Analysis complete!")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("📊 Total Analyzed", len(df))
                            with col2:
                                st.metric("🔴 High Risk Found", high_risk_count)
                            with col3:
                                st.metric("💰 Estimated Savings", f"${high_risk_count * 250:,}")
                
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
    
    with col2:
        st.subheader("📋 Upload Guidelines")
        st.info("""
        **Required Columns:**
        - amount: Transaction amount
        - merchant: Merchant name  
        - date: Transaction date
        """)

elif page == "🔍 Transaction Analysis":
    st.title("🔍 Detailed Transaction Analysis")
    
    selected_transaction_id = st.selectbox(
        "🔍 Select a transaction to analyze:",
        options=st.session_state.transactions['transaction_id'].tolist()
    )
    
    if selected_transaction_id:
        transaction = st.session_state.transactions[
            st.session_state.transactions['transaction_id'] == selected_transaction_id
        ].iloc[0]
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Transaction Details")
            st.info(f"""
            **Transaction ID:** {transaction['transaction_id']}  
            **Amount:** {format_currency(transaction['amount'])}  
            **Merchant:** {transaction['merchant']}  
            **Date:** {transaction['date']}  
            **Status:** {transaction['status']}  
            **Card Type:** {transaction['card_type']}  
            **Location:** {transaction['location']}
            """)
        
        with col2:
            st.subheader("🎯 Risk Assessment")
            
            risk_score = transaction['risk_score']
            risk_level, risk_class = get_risk_category(risk_score)
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ]
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"**Risk Level:** {risk_level}")
        
        st.markdown("---")
        st.subheader("⚠️ Risk Factors Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Identified Risk Factors:**")
            st.markdown(get_risk_factors_explanation(risk_score))
        
        with col2:
            st.markdown("**Recommended Actions:**")
            st.markdown(get_action_recommendations(risk_score))
        
        st.markdown("---")
        st.subheader("🎬 Take Action")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ Approve", type="primary"):
                st.success("✅ Transaction approved!")
        
        with col2:
            if st.button("⚠️ Flag for Review"):
                st.warning("⚠️ Transaction flagged!")
        
        with col3:
            if st.button("🚫 Block"):
                st.error("🚫 Transaction blocked!")
        
        with col4:
            if st.button("📞 Contact Customer"):
                st.info("📞 Customer contact initiated!")

elif page == "🤖 AI Assistant":
    st.title("🤖 AI Fraud Detection Assistant")
    
    st.subheader("💬 Chat with your Fraud Detection Assistant")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about fraud patterns, risk scores, or analytics..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                time.sleep(1)
                response = generate_ai_response(prompt)
                st.markdown(response)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Quick action buttons
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Show Risk Analysis", use_container_width=True):
            analysis_prompt = "Show me risk analysis and patterns"
            st.session_state.chat_history.append({"role": "user", "content": analysis_prompt})
            response = generate_ai_response(analysis_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("💰 Calculate ROI", use_container_width=True):
            roi_prompt = "What's my ROI and cost savings?"
            st.session_state.chat_history.append({"role": "user", "content": roi_prompt})
            response = generate_ai_response(roi_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("📈 Fraud Trends", use_container_width=True):
            trends_prompt = "Show me fraud trends and patterns"
            st.session_state.chat_history.append({"role": "user", "content": trends_prompt})
            response = generate_ai_response(trends_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

elif page == "⚙️ Settings":
    st.title("⚙️ System Settings & Configuration")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Risk Thresholds", "🔔 Notifications", "📊 Reporting"])
    
    with tab1:
        st.subheader("🎯 Risk Score Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            high_risk_threshold = st.slider("High Risk Threshold", 60, 90, 70)
            medium_risk_threshold = st.slider("Medium Risk Threshold", 30, 60, 40)
            auto_block_threshold = st.selectbox(
                "Auto-block transactions above:",
                ["Disabled", "Score 90+", "Score 95+"],
                index=1
            )
        
        with col2:
            current_high = len(st.session_state.transactions[st.session_state.transactions['risk_score'] >= high_risk_threshold])
            st.metric("High Risk Transactions", current_high)
            
            if high_risk_threshold < 70:
                st.warning("⚠️ Lower threshold will increase alerts")
            else:
                st.success("✅ Balanced threshold setting")
    
    with tab2:
        st.subheader("🔔 Notification Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_alerts = st.checkbox("📧 Email Alerts", value=True)
            if email_alerts:
                email_address = st.text_input("Email Address", value="admin@company.com")
            
            sms_alerts = st.checkbox("📱 SMS Alerts", value=True)
            if sms_alerts:
                phone_number = st.text_input("Phone Number", value="+1-555-0123")
        
        with col2:
            real_time_alerts = st.checkbox("⚡ Real-time Alerts", value=True)
            daily_summary = st.checkbox("📅 Daily Summary Report", value=True)
            business_hours_only = st.checkbox("🕒 Business Hours Only", value=False)
    
    with tab3:
        st.subheader("📊 Reporting Configuration")
        
        auto_reports = st.checkbox("📅 Automatic Report Generation", value=True)
        
        if auto_reports:
            report_frequency = st.selectbox("Report Frequency:", ["Daily", "Weekly", "Monthly"], index=1)
            include_charts = st.checkbox("📈 Include Charts in Reports", value=True)
    
    st.markdown("---")
    if st.button("💾 Save All Settings", type="primary"):
        st.success("✅ Settings saved successfully!")
        st.balloons()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🛡️ FraudGuard Pro v1.0.0")

with col2:
    st.caption(f"🕒 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col3:
    st.caption("📊 System Status: ✅ Operational")