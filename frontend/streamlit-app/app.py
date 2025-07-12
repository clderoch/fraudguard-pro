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
    .stSelectbox > div > div {
        background-color: #f8fafc;
    }
    .streamlit-expanderHeader {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        background: #f8fafc;
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

def generate_ai_response(user_message):
    """Generate AI assistant responses based on user input"""
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

**Best Practices Working:**
• Real-time transaction monitoring
• Machine learning pattern recognition
• Geographic and velocity checks

I recommend reviewing transactions with scores above 75 within 24 hours for optimal prevention rates."""
    
    elif 'trend' in message or 'pattern' in message or 'analysis' in message:
        return """📊 **Fraud Pattern Analysis:**

I've identified several important trends in your recent transaction data:

**Emerging Patterns:**
• **45% increase** in card-not-present fraud attempts (last 30 days)
• **Peak risk hours:** 2-4 AM and 11 PM-1 AM EST
• **Geographic hotspots:** 3 new high-risk IP ranges detected
• **Device patterns:** 67% of fraud attempts from mobile devices

**Seasonal Trends:**
• Higher risk transactions on weekends (+23%)
• Increased international transactions (+34% risk scores)
• Holiday shopping period showing elevated baseline risk

**Positive Indicators:**
• Overall fraud rate decreased 12% this month
• Customer education reducing false disputes
• Faster merchant response times improving outcomes

**Action Items:**
• Enhanced monitoring during peak risk hours
• Updated geographic risk scoring models
• Mobile device verification improvements"""
    
    elif 'help' in message or 'how' in message or 'what' in message:
        return """🔍 **FraudGuard Assistant Capabilities:**

I'm here to help you optimize your fraud prevention! Here's what I can assist with:

**Transaction Analysis:**
• Individual transaction risk assessment
• Bulk transaction pattern analysis
• Risk factor identification and explanation
• Chargeback probability scoring

**Performance Insights:**
• ROI calculations and savings reports
• Accuracy and false positive rate analysis
• Benchmark comparisons with industry standards
• Trend identification and forecasting

**Optimization Recommendations:**
• Risk threshold adjustments
• Alert configuration suggestions
• Workflow improvements
• Integration recommendations

**Reporting & Analytics:**
• Custom report generation
• Executive summary creation
• Compliance reporting assistance
• Performance dashboard insights

**Examples of questions I can answer:**
• "Why was transaction TXN-2024-001 flagged as high risk?"
• "What's my ROI from fraud prevention this quarter?"
• "Show me trends in international transactions"
• "How can I reduce false positives?"

Just ask me about any transaction, trend, or fraud prevention topic!"""
    
    elif 'save' in message or 'money' in message or 'roi' in message or 'cost' in message:
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
• **Annual subscription cost:** $3,588
• **Net annual benefit:** $150,024
• **ROI:** 4,184% return on investment

**Payback Analysis:**
• **Payback period:** 5.6 days
• **Break-even point:** Preventing just 2 chargebacks per month
• **Cost per prevented chargeback:** $19.93

**Industry Comparison:**
• Average chargeback cost: $150-500 per incident
• Your prevention rate: 92% (industry average: 67%)
• Cost savings vs. manual review: 89% reduction

**Key Value Drivers:**
• Automated 24/7 monitoring
• Real-time risk assessment
• Reduced manual review costs
• Improved customer experience"""
    
    elif 'alert' in message or 'notification' in message or 'setting' in message:
        return """🚨 **Alert & Notification Management:**

Your current alert configuration is optimized for maximum effectiveness:

**Current Alert Settings:**
• **High-risk threshold:** Score 70+ (triggering 23 alerts/month)
• **Critical threshold:** Score 85+ (auto-escalation)
• **Notification channels:** Email + SMS + Dashboard
• **Response time SLA:** 2 hours for high-risk

**Alert Performance:**
• **Average response time:** 47 minutes
• **False alert rate:** 8.2% (excellent)
• **Escalation rate:** 12% require manual review
• **Resolution rate:** 96.8% within SLA

**Optimization Recommendations:**
• Consider lowering threshold to 65 for even better protection
• Add Slack integration for team collaboration
• Set up weekend/holiday escalation procedures
• Implement automated actions for scores 95+

**Available Alert Types:**
• Real-time transaction alerts
• Daily/weekly summary reports  
• Pattern detection notifications
• Threshold breach warnings
• System health alerts

**Customization Options:**
• Risk score thresholds (adjustable 0-100)
• Time-based rules (business hours, weekends)
• Amount-based triggers ($500, $1000, $2500+)
• Geographic restrictions
• Velocity limits

Would you like me to help adjust any of these settings?"""
    
    elif 'transaction' in message and any(tid in message for tid in ['txn', 'TXN', '001', '002', '003']):
        # Extract transaction ID if mentioned
        transaction_id = None
        for tid in ['TXN-2024-001', 'TXN-2024-002', 'TXN-2024-003', 'TXN-2024-004', 'TXN-2024-005']:
            if tid.lower() in message.lower():
                transaction_id = tid
                break
        
        if transaction_id:
            transaction = st.session_state.transactions[
                st.session_state.transactions['transaction_id'] == transaction_id
            ]
            if not transaction.empty:
                tx = transaction.iloc[0]
                risk_level, _ = get_risk_category(tx['risk_score'])
                
                return f"""🔍 **Transaction Analysis: {transaction_id}**

**Basic Information:**
• **Amount:** {format_currency(tx['amount'])}
• **Merchant:** {tx['merchant']}
• **Date:** {tx['date']}
• **Card Type:** {tx['card_type']}
• **Location:** {tx['location']}

**Risk Assessment:**
• **Risk Score:** {tx['risk_score']}/100
• **Risk Level:** {risk_level}
• **Status:** {tx['status']}

**Technical Details:**
• **IP Address:** {tx['ip_address']}
• **Device ID:** {tx['device_id']}

**Risk Factors Identified:**
{get_risk_factors_explanation(tx['risk_score'])}

**Recommended Actions:**
{get_action_recommendations(tx['risk_score'])}

Would you like me to analyze any specific aspect of this transaction in more detail?"""
    
    # Default response for other queries
    return f"""🤖 **I understand you're asking about: "{user_message}"**

I'm here to help you with your fraud detection and prevention needs. Based on your current data, here's what I can help you explore:

**Current System Status:**
• 1,247 total transactions processed this month
• 23 high-risk transactions requiring attention
• 94.7% accuracy rate in fraud detection
• $15,000 in total savings this month

**What would you like to know more about?**
• Specific transaction analysis
• Risk pattern identification  
• Financial impact and ROI
• System optimization recommendations
• Alert and notification management

**Quick Actions I Can Help With:**
• "Analyze transaction TXN-2024-001"
• "Show me this month's fraud trends"
• "What's my ROI from fraud prevention?"
• "How can I reduce false positives?"

Please feel free to ask me anything specific about your fraud detection data or system!"""

def get_risk_factors_explanation(risk_score):
    """Generate risk factor explanations based on risk score"""
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
    """Generate action recommendations based on risk score"""
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
        ["📊 Dashboard", "📤 Upload Transactions", "🔍 Transaction Analysis", "🤖 AI Assistant", "⚙️ Settings"],
        format_func=lambda x: x
    )
    
    st.markdown("---")
    st.subheader("📈 Quick Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Transactions", "1,247", "+12.3%")
        st.metric("Monthly Savings", "$3,750", "+32.1%")
    with col2:
        if st.button("🔄 Refresh Analysis", type="secondary"):
            st.rerun()
    
    if selected_transaction_id:
        transaction = st.session_state.transactions[
            st.session_state.transactions['transaction_id'] == selected_transaction_id
        ].iloc[0]
        
        # Transaction overview
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Transaction Details")
            
            # Create a nice info box
            st.info(f"""
            **Transaction ID:** {transaction['transaction_id']}  
            **Amount:** {format_currency(transaction['amount'])}  
            **Merchant:** {transaction['merchant']}  
            **Date:** {transaction['date']}  
            **Status:** {transaction['status']}  
            **Card Type:** {transaction['card_type']}  
            **Location:** {transaction['location']}
            """)
            
            # Additional technical details
            with st.expander("🔧 Technical Details"):
                st.write(f"**IP Address:** {transaction['ip_address']}")
                st.write(f"**Device ID:** {transaction['device_id']}")
                st.write(f"**Processing Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        with col2:
            st.subheader("🎯 Risk Assessment")
            
            risk_score = transaction['risk_score']
            risk_level, risk_class = get_risk_category(risk_score)
            
            # Risk score gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Score"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk level display
            st.markdown(f"**Risk Level:** {risk_level}")
        
        # Risk factors analysis
        st.markdown("---")
        st.subheader("⚠️ Risk Factors Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Identified Risk Factors:**")
            risk_factors = get_risk_factors_explanation(risk_score)
            st.markdown(risk_factors)
        
        with col2:
            st.markdown("**Recommended Actions:**")
            recommendations = get_action_recommendations(risk_score)
            st.markdown(recommendations)
        
        # Action buttons
        st.markdown("---")
        st.subheader("🎬 Take Action")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ Approve Transaction", type="primary"):
                st.success("✅ Transaction approved!")
                st.balloons()
        
        with col2:
            if st.button("⚠️ Flag for Review", type="secondary"):
                st.warning("⚠️ Transaction flagged for manual review!")
        
        with col3:
            if st.button("🚫 Block Transaction", type="secondary"):
                st.error("🚫 Transaction blocked!")
        
        with col4:
            if st.button("📞 Contact Customer", type="secondary"):
                st.info("📞 Customer contact initiated!")
        
        # Historical analysis
        st.markdown("---")
        st.subheader("📊 Historical Context")
        
        # Simulate customer transaction history
        customer_history = pd.DataFrame({
            'date': pd.date_range(start='2024-06-01', end='2024-07-10', freq='3D'),
            'amount': np.random.uniform(50, 1000, 14),
            'risk_score': np.random.randint(10, 60, 14)
        })
        
        fig = px.line(
            customer_history, 
            x='date', 
            y='amount',
            title="Customer Transaction History (Last 30 Days)",
            markers=True
        )
        fig.add_hline(y=transaction['amount'], line_dash="dash", line_color="red", 
                     annotation_text="Current Transaction")
        st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 AI Assistant":
    st.title("🤖 AI Fraud Detection Assistant")
    
    # Chat interface
    st.subheader("💬 Chat with your Fraud Detection Assistant")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about fraud patterns, risk scores, analytics, or specific transactions..."):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        st.chat_message("user").write(prompt)
        
        # Generate and display AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                time.sleep(1)  # Simulate thinking time
                response = generate_ai_response(prompt)
                st.markdown(response)
        
        # Add AI response to history
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
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = [
            {
                "role": "assistant", 
                "content": "👋 Hi! I'm your FraudGuard Assistant. How can I help you today?"
            }
        ]
        st.rerun()

elif page == "⚙️ Settings":
    st.title("⚙️ System Settings & Configuration")
    
    # Create tabs for different settings categories
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Risk Thresholds", "🔔 Notifications", "🔐 Security", "📊 Reporting"])
    
    with tab1:
        st.subheader("🎯 Risk Score Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current Thresholds:**")
            
            high_risk_threshold = st.slider(
                "High Risk Threshold", 
                min_value=60, 
                max_value=90, 
                value=70,
                help="Transactions above this score are flagged as high risk"
            )
            
            medium_risk_threshold = st.slider(
                "Medium Risk Threshold", 
                min_value=30, 
                max_value=60, 
                value=40,
                help="Transactions above this score are flagged as medium risk"
            )
            
            auto_block_threshold = st.selectbox(
                "Auto-block transactions above:",
                options=["Disabled", "Score 90+", "Score 95+", "Score 98+"],
                index=1,
                help="Automatically block transactions above this threshold"
            )
        
        with col2:
            st.markdown("**Threshold Impact Analysis:**")
            
            # Simulate impact based on current data
            current_high = len(st.session_state.transactions[st.session_state.transactions['risk_score'] >= high_risk_threshold])
            current_medium = len(st.session_state.transactions[
                (st.session_state.transactions['risk_score'] >= medium_risk_threshold) & 
                (st.session_state.transactions['risk_score'] < high_risk_threshold)
            ])
            
            st.metric("High Risk Transactions", current_high)
            st.metric("Medium Risk Transactions", current_medium)
            
            if high_risk_threshold < 70:
                st.warning("⚠️ Lower threshold will increase alerts")
            elif high_risk_threshold > 80:
                st.info("ℹ️ Higher threshold may miss some fraud")
            else:
                st.success("✅ Balanced threshold setting")
    
    with tab2:
        st.subheader("🔔 Notification Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Alert Channels:**")
            
            email_alerts = st.checkbox("📧 Email Alerts", value=True)
            if email_alerts:
                email_address = st.text_input("Email Address", value="admin@company.com")
            
            sms_alerts = st.checkbox("📱 SMS Alerts", value=True)
            if sms_alerts:
                phone_number = st.text_input("Phone Number", value="+1-555-0123")
            
            slack_alerts = st.checkbox("💬 Slack Integration", value=False)
            if slack_alerts:
                slack_webhook = st.text_input("Slack Webhook URL", placeholder="https://hooks.slack.com/...")
            
            webhook_alerts = st.checkbox("🔗 Custom Webhook", value=False)
            if webhook_alerts:
                webhook_url = st.text_input("Webhook URL", placeholder="https://your-api.com/webhook")
        
        with col2:
            st.markdown("**Alert Timing:**")
            
            real_time_alerts = st.checkbox("⚡ Real-time Alerts", value=True)
            daily_summary = st.checkbox("📅 Daily Summary Report", value=True)
            weekly_report = st.checkbox("📊 Weekly Analytics Report", value=True)
            
            business_hours_only = st.checkbox("🕒 Business Hours Only", value=False)
            if business_hours_only:
                start_time = st.time_input("Start Time", value=datetime.strptime("09:00", "%H:%M").time())
                end_time = st.time_input("End Time", value=datetime.strptime("17:00", "%H:%M").time())
            
            weekend_alerts = st.checkbox("📅 Weekend Alerts", value=True)
    
    with tab3:
        st.subheader("🔐 Security & Access Control")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**API Security:**")
            
            api_key_visible = st.checkbox("👁️ Show API Key")
            if api_key_visible:
                st.code("sk-fraudguard-1234567890abcdef", language="text")
            else:
                st.code("sk-fraudguard-••••••••••••••••", language="text")
            
            if st.button("🔄 Regenerate API Key"):
                st.success("✅ New API key generated!")
            
            rate_limiting = st.selectbox(
                "API Rate Limiting:",
                ["100 requests/minute", "500 requests/minute", "1000 requests/minute", "Unlimited"],
                index=1
            )
            
            ip_whitelist = st.text_area(
                "IP Whitelist (one per line):",
                value="192.168.1.0/24\n10.0.0.0/8",
                help="Restrict API access to these IP addresses"
            )
        
        with col2:
            st.markdown("**Data Retention:**")
            
            transaction_retention = st.selectbox(
                "Transaction Data Retention:",
                ["30 days", "90 days", "1 year", "2 years", "Indefinite"],
                index=2
            )
            
            log_retention = st.selectbox(
                "Log Data Retention:",
                ["7 days", "30 days", "90 days", "1 year"],
                index=2
            )
            
            data_encryption = st.checkbox("🔒 Enhanced Data Encryption", value=True)
            audit_logging = st.checkbox("📋 Detailed Audit Logging", value=True)
            
            if st.button("🗑️ Purge Old Data"):
                st.info("ℹ️ Data purge scheduled for next maintenance window")
    
    with tab4:
        st.subheader("📊 Reporting Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Report Generation:**")
            
            auto_reports = st.checkbox("📅 Automatic Report Generation", value=True)
            
            if auto_reports:
                report_frequency = st.selectbox(
                    "Report Frequency:",
                    ["Daily", "Weekly", "Monthly", "Quarterly"],
                    index=1
                )
                
                report_recipients = st.text_area(
                    "Report Recipients (one email per line):",
                    value="ceo@company.com\ncfo@company.com\nrisk@company.com"
                )
            
            include_charts = st.checkbox("📈 Include Charts in Reports", value=True)
            include_raw_data = st.checkbox("📋 Include Raw Data Export", value=False)
            executive_summary = st.checkbox("📄 Executive Summary Only", value=False)
        
        with col2:
            st.markdown("**Custom Metrics:**")
            
            track_custom_metrics = st.checkbox("📊 Track Custom Metrics", value=False)
            
            if track_custom_metrics:
                custom_metric_1 = st.text_input("Custom Metric 1:", placeholder="e.g., High-value transaction rate")
                custom_metric_2 = st.text_input("Custom Metric 2:", placeholder="e.g., International transaction ratio")
                custom_metric_3 = st.text_input("Custom Metric 3:", placeholder="e.g., Weekend fraud rate")
            
            benchmark_comparison = st.checkbox("📊 Industry Benchmark Comparison", value=True)
            predictive_analytics = st.checkbox("🔮 Predictive Analytics", value=True)
    
    # Save settings button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 Save All Settings", type="primary", use_container_width=True):
            st.success("✅ Settings saved successfully!")
            st.balloons()
            time.sleep(2)
            st.rerun()

# Footer with system info
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🛡️ FraudGuard Pro v1.0.0")

with col2:
    st.caption(f"🕒 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col3:
    st.caption("📊 System Status: ✅ Operational")

# Auto-refresh for dashboard
if page == "📊 Dashboard":
    # Auto-refresh every 30 seconds for real-time feel
    time.sleep(0.1)
        st.metric("High Risk Flagged", "23", "-8.1%")
        st.metric("Accuracy Rate", "94.7%", "+2.1%")
    
    # Real-time status indicator
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
            delta="12.3%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="⚠️ High Risk Flagged",
            value=str(st.session_state.metrics['high_risk_count']),
            delta="-8.1%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="🛡️ Chargebacks Prevented",
            value=str(st.session_state.metrics['chargebacks_prevented']),
            delta="45.2%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="💰 Monthly Savings",
            value=format_currency(st.session_state.metrics['savings_amount']),
            delta="32.1%",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Risk Score Distribution")
        risk_data = pd.DataFrame({
            'Risk Level': ['Low Risk (0-30)', 'Medium Risk (31-70)', 'High Risk (71-100)'],
            'Count': [820, 204, 23],
            'Percentage': [78.3, 19.5, 2.2]
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
            'High Risk Flagged': [45, 38, 52, 41, 35, 28, 23],
            'Chargebacks Prevented': [8, 12, 18, 15, 20, 17, 15]
        })
        
        fig = px.line(
            trend_data, 
            x='Month', 
            y=['Total Transactions', 'High Risk Flagged', 'Chargebacks Prevented'],
            title="7-Month Transaction Trends",
            color_discrete_sequence=['#667eea', '#f56565', '#48bb78']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    st.markdown("---")
    st.subheader("🎯 Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🎯 Detection Accuracy",
            value=f"{st.session_state.metrics['accuracy_rate']}%",
            delta="2.1%"
        )
    
    with col2:
        st.metric(
            label="❌ False Positive Rate", 
            value=f"{st.session_state.metrics['false_positive_rate']}%",
            delta="-1.3%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="⚡ Avg Response Time",
            value="47 min",
            delta="-12 min",
            delta_color="inverse"
        )
    
    # Recent transactions table
    st.markdown("---")
    st.subheader("🚨 Recent High-Risk Transactions")
    
    # Filter for high-risk transactions
    high_risk_transactions = st.session_state.transactions[
        st.session_state.transactions['risk_score'] >= 60
    ].copy()
    
    # Add risk level column for display
    high_risk_transactions['risk_level'] = high_risk_transactions['risk_score'].apply(
        lambda x: get_risk_category(x)[0]
    )
    
    # Format amount for display
    high_risk_transactions['formatted_amount'] = high_risk_transactions['amount'].apply(format_currency)
    
    # Display table
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
            help="Upload your transaction data for fraud analysis. Supported formats: CSV, Excel (.xlsx, .xls)"
        )
        
        if uploaded_file is not None:
            # Show file details
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size:,} bytes",
                "File type": uploaded_file.type
            }
            
            st.success("✅ File uploaded successfully!")
            
            with st.expander("📋 File Details"):
                for key, value in file_details.items():
                    st.write(f"**{key}:** {value}")
            
            # Process file
            with st.spinner('🔄 Processing transactions...'):
                time.sleep(2)  # Simulate processing time
                
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.success(f"✅ Successfully loaded {len(df):,} transactions")
                    
                    # Show sample data
                    st.subheader("👀 Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Data validation
                    st.subheader("🔍 Data Validation")
                    required_columns = ['amount', 'merchant', 'date']
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    
                    if missing_columns:
                        st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                        st.info("💡 Please ensure your file contains: amount, merchant, date columns")
                    else:
                        st.success("✅ All required columns present")
                        
                        # Run fraud analysis
                        if st.button("🔍 Run Fraud Analysis", type="primary"):
                            with st.spinner('🧠 Analyzing for fraud patterns...'):
                                time.sleep(3)
                                
                                # Simulate fraud analysis
                                df['risk_score'] = np.random.randint(0, 100, len(df))
                                df['risk_level'] = df['risk_score'].apply(lambda x: get_risk_category(x)[0])
                                
                                high_risk_count = len(df[df['risk_score'] >= 70])
                                medium_risk_count = len(df[(df['risk_score'] >= 40) & (df['risk_score'] < 70)])
                                low_risk_count = len(df[df['risk_score'] < 40])
                                
                                st.success("🎯 Fraud analysis complete!")
                                
                                # Show results
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric("📊 Total Analyzed", len(df))
                                with col2:
                                    st.metric("🔴 High Risk", high_risk_count)
                                with col3:
                                    st.metric("🟡 Medium Risk", medium_risk_count)
                                with col4:
                                    st.metric("🟢 Low Risk", low_risk_count)
                                
                                # Update session state
                                new_transactions = df.head(10).copy()
                                if 'transaction_id' not in new_transactions.columns:
                                    new_transactions['transaction_id'] = [f'TXN-NEW-{i:03d}' for i in range(len(new_transactions))]
                                
                                st.session_state.transactions = pd.concat([
                                    st.session_state.transactions, 
                                    new_transactions[['transaction_id', 'amount', 'merchant', 'date', 'risk_score']].assign(
                                        status='Analyzed',
                                        card_type='Unknown',
                                        location='Unknown',
                                        ip_address='Unknown',
                                        device_id='Unknown'
                                    )
                                ], ignore_index=True)
                                
                                # Show high-risk transactions
                                if high_risk_count > 0:
                                    st.subheader("⚠️ High-Risk Transactions Detected")
                                    high_risk_df = df[df['risk_score'] >= 70]
                                    st.dataframe(
                                        high_risk_df[['amount', 'merchant', 'date', 'risk_score', 'risk_level']],
                                        use_container_width=True
                                    )
                                
                                # Estimated savings
                                estimated_savings = high_risk_count * 250  # $250 average chargeback cost
                                st.info(f"💰 Estimated potential savings: ${estimated_savings:,}")
                    
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
                    st.info("💡 Please check your file format and try again")
    
    with col2:
        st.subheader("📋 Upload Guidelines")
        
        st.info("""
        **Required Columns:**
        - `amount`: Transaction amount
        - `merchant`: Merchant name
        - `date`: Transaction date
        
        **Optional Columns:**
        - `card_type`: Visa, Mastercard, etc.
        - `location`: Transaction location
        - `customer_id`: Customer identifier
        """)
        
        st.warning("""
        **File Requirements:**
        - Maximum file size: 50MB
        - Supported formats: CSV, Excel
        - Date format: YYYY-MM-DD
        - Amount format: Numeric (no currency symbols)
        """)
        
        # Sample data download
        st.subheader("📥 Sample Data")
        sample_data = pd.DataFrame({
            'amount': [100.50, 250.00, 75.25],
            'merchant': ['Coffee Shop', 'Electronics Store', 'Gas Station'],
            'date': ['2024-07-10', '2024-07-10', '2024-07-09'],
            'card_type': ['Visa', 'Mastercard', 'Visa'],
            'location': ['New York, NY', 'Los Angeles, CA', 'Chicago, IL']
        })
        
        csv = sample_data.to_csv(index=False)
        st.download_button(
            label="📄 Download Sample CSV",
            data=csv,
            file_name='fraudguard_sample_data.csv',
            mime='text/csv'
        )

elif page == "🔍 Transaction Analysis":
    st.title("🔍 Detailed Transaction Analysis")
    
    # Transaction selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_transaction_id = st.selectbox(
            "🔍 Select a transaction to analyze:",
            options=st.session_state.transactions['transaction_id'].tolist(),
            help="Choose a transaction ID to view detailed analysis"
        )
    
    with col2: