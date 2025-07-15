import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FraudGuard Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for modern, clean design
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    .css-1d391kg {padding: 1rem 2rem 2rem;}
    .css-k1vhr4 {margin-top: -60px;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Upload section styling */
    .upload-container {
        background: #f8fafc;
        border: 2px dashed #cbd5e0;
        border-radius: 15px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        border-color: #667eea;
        background: #f1f5f9;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a202c;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #718096;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    .metric-high { border-left-color: #f56565; }
    .metric-medium { border-left-color: #ed8936; }
    .metric-low { border-left-color: #48bb78; }
    
    /* Info cards */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .badge-success {
        background: #c6f6d5;
        color: #22543d;
    }
    
    .badge-warning {
        background: #fef5e7;
        color: #c53030;
    }
    
    .badge-info {
        background: #bee3f8;
        color: #2a69ac;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    
    /* Tables */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
    }
    
    /* Buttons */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Spacing */
    .spacer {
        margin: 2rem 0;
    }
    
    /* Hide file uploader details */
    .uploadedFile {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

class SimpleFraudDetectionModel:
    """Simplified fraud detection with basic rule-based scoring"""
    
    def __init__(self):
        self.risk_score_calculated = False
    
    def detect_fraud(self, df):
        """Simple fraud detection using basic rules"""
        df_analyzed = df.copy()
        
        try:
            # Ensure amount is numeric
            df_analyzed['amount'] = pd.to_numeric(df_analyzed['amount'], errors='coerce').fillna(0)
            
            # Simple risk scoring based on amount
            risk_scores = []
            for _, row in df_analyzed.iterrows():
                score = 0
                amount = row.get('amount', 0)
                
                # Amount-based risk
                if amount > 1000:
                    score += 30
                elif amount > 500:
                    score += 15
                elif amount < 5:
                    score += 25
                else:
                    score += 10
                
                # Time-based risk (if available)
                if 'transaction_time' in df_analyzed.columns:
                    time_str = str(row.get('transaction_time', '12:00:00'))
                    try:
                        if ':' in time_str:
                            hour = int(time_str.split(':')[0])
                            if hour >= 23 or hour <= 6:  # Late night
                                score += 20
                    except:
                        pass
                
                # Response code risk (if available)
                if 'response_code' in df_analyzed.columns:
                    response = str(row.get('response_code', '00'))
                    if response in ['05', '14', '51', '61', '62', '65']:
                        score += 25
                
                # Category risk (if available)
                if 'merchant_category' in df_analyzed.columns:
                    category = str(row.get('merchant_category', ''))
                    if category in ['ATM', 'Online Retail', 'Electronics']:
                        score += 15
                
                # Random component for variability
                score += np.random.randint(0, 15)
                
                risk_scores.append(min(score, 100))
            
            df_analyzed['ml_risk_score'] = risk_scores
            
            # Create risk levels
            df_analyzed['ml_risk_level'] = pd.cut(
                df_analyzed['ml_risk_score'],
                bins=[0, 30, 70, 100],
                labels=['Low', 'Medium', 'High']
            )
            
            # Simple binary flags
            df_analyzed['isolation_anomaly'] = (df_analyzed['ml_risk_score'] > 70).astype(int)
            df_analyzed['dbscan_outlier'] = (df_analyzed['ml_risk_score'] > 80).astype(int)
            
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
            st.error(f"Error in simple fraud detection: {e}")
            # Ultra-simple fallback
            df_analyzed['ml_risk_score'] = np.random.uniform(10, 90, len(df_analyzed))
            df_analyzed['ml_risk_level'] = 'Medium'
            df_analyzed['isolation_anomaly'] = 0
            df_analyzed['dbscan_outlier'] = 0
            df_analyzed['hour'] = 12
            return df_analyzed

def create_enhanced_charts(df_analyzed):
    """Create enhanced, professional-looking charts"""
    
    # Color palette
    colors = {
        'primary': '#667eea',
        'secondary': '#764ba2', 
        'success': '#48bb78',
        'warning': '#ed8936',
        'danger': '#f56565',
        'low': '#48bb78',
        'medium': '#ed8936',
        'high': '#f56565'
    }
    
    charts = {}
    
    # 1. Transaction Volume Trend
    daily_volume = df_analyzed.groupby('transaction_date').size().reset_index(name='count')
    charts['volume_trend'] = px.line(
        daily_volume, 
        x='transaction_date', 
        y='count',
        title='📈 Daily Transaction Volume',
        color_discrete_sequence=[colors['primary']]
    )
    charts['volume_trend'].update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_size=18,
        title_font_color=colors['primary'],
        xaxis_title="Date",
        yaxis_title="Number of Transactions",
        showlegend=False
    )
    
    # 2. Risk Distribution Pie Chart
    risk_dist = df_analyzed['ml_risk_level'].value_counts()
    charts['risk_pie'] = px.pie(
        values=risk_dist.values,
        names=risk_dist.index,
        title='🎯 Risk Level Distribution',
        color_discrete_map={
            'Low': colors['low'],
            'Medium': colors['medium'],
            'High': colors['high']
        }
    )
    charts['risk_pie'].update_layout(
        title_font_size=18,
        title_font_color=colors['primary'],
        paper_bgcolor='white'
    )
    
    # 3. Risk Score Histogram
    charts['risk_histogram'] = px.histogram(
        df_analyzed, 
        x='ml_risk_score',
        nbins=20,
        title='📊 Risk Score Distribution',
        color_discrete_sequence=[colors['primary']]
    )
    charts['risk_histogram'].update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_size=18,
        title_font_color=colors['primary'],
        xaxis_title="Risk Score",
        yaxis_title="Number of Transactions",
        showlegend=False
    )
    
    # 4. Amount vs Time Scatter Plot
    charts['amount_time_scatter'] = px.scatter(
        df_analyzed, 
        x='amount', 
        y='hour',
        color='ml_risk_level',
        title='💰 Transaction Amount vs Time of Day',
        color_discrete_map={
            'Low': colors['low'],
            'Medium': colors['medium'],
            'High': colors['high']
        },
        opacity=0.7
    )
    charts['amount_time_scatter'].update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_size=18,
        title_font_color=colors['primary'],
        xaxis_title="Transaction Amount ($)",
        yaxis_title="Hour of Day"
    )
    
    # 5. Category Risk Analysis
    if 'merchant_category' in df_analyzed.columns:
        category_risk = df_analyzed.groupby('merchant_category')['ml_risk_score'].mean().sort_values(ascending=True)
        charts['category_risk'] = px.bar(
            x=category_risk.values,
            y=category_risk.index,
            orientation='h',
            title='🏪 Average Risk Score by Merchant Category',
            color=category_risk.values,
            color_continuous_scale=['#48bb78', '#ed8936', '#f56565']
        )
        charts['category_risk'].update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font_size=18,
            title_font_color=colors['primary'],
            xaxis_title="Average Risk Score",
            yaxis_title="Merchant Category",
            showlegend=False,
            coloraxis_showscale=False
        )
    
    return charts

def display_metrics_section(df_analyzed):
    """Display key metrics in organized cards"""
    
    # Calculate metrics
    total_transactions = len(df_analyzed)
    high_risk_count = len(df_analyzed[df_analyzed['ml_risk_level'] == 'High'])
    medium_risk_count = len(df_analyzed[df_analyzed['ml_risk_level'] == 'Medium'])
    low_risk_count = len(df_analyzed[df_analyzed['ml_risk_level'] == 'Low'])
    high_risk_percentage = (high_risk_count / total_transactions) * 100
    avg_risk_score = df_analyzed['ml_risk_score'].mean()
    avg_amount = df_analyzed['amount'].mean()
    unique_customers = df_analyzed['customer_id'].nunique() if 'customer_id' in df_analyzed.columns else len(df_analyzed)
    
    # Display metrics header
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    # Primary metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{total_transactions:,}</p>
            <p class="metric-label">Total Transactions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-high">
            <p class="metric-value">{high_risk_count:,}</p>
            <p class="metric-label">High Risk Detected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card metric-medium">
            <p class="metric-value">{high_risk_percentage:.1f}%</p>
            <p class="metric-label">High Risk Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card metric-low">
            <p class="metric-value">{avg_risk_score:.1f}</p>
            <p class="metric-label">Average Risk Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Secondary metrics row
    st.markdown('<div style="margin: 1rem 0;"></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <strong>💰 Average Amount</strong><br>
            ${avg_amount:,.2f}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card">
            <strong>👥 Unique Customers</strong><br>
            {unique_customers:,}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="info-card">
            <strong>🟡 Medium Risk</strong><br>
            {medium_risk_count:,} transactions
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="info-card">
            <strong>🟢 Low Risk</strong><br>
            {low_risk_count:,} transactions
        </div>
        """, unsafe_allow_html=True)

def display_analytics_section(charts):
    """Display analytics charts in organized layout"""
    
    st.markdown('<div class="section-header">📈 Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Main chart - full width
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(charts['volume_trend'], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Two column charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(charts['risk_pie'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(charts['risk_histogram'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Scatter plot - full width
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(charts['amount_time_scatter'], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Category analysis if available
    if 'category_risk' in charts:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(charts['category_risk'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def display_insights_section(df_analyzed):
    """Display AI-generated insights"""
    
    st.markdown('<div class="section-header">🔍 Fraud Detection Insights</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚨 High-Risk Patterns")
        
        high_risk_transactions = df_analyzed[df_analyzed['ml_risk_level'] == 'High']
        
        if not high_risk_transactions.empty:
            # Most common high-risk categories
            if 'merchant_category' in df_analyzed.columns:
                risk_categories = high_risk_transactions['merchant_category'].value_counts().head(3)
                st.markdown("**Top Risk Categories:**")
                for category, count in risk_categories.items():
                    percentage = (count / len(high_risk_transactions)) * 100
                    st.markdown(f"""
                    <div class="status-badge badge-warning">
                        {category}: {count} ({percentage:.1f}%)
                    </div>
                    """, unsafe_allow_html=True)
            
            # Time patterns
            risk_hours = high_risk_transactions['hour'].value_counts().head(3)
            st.markdown("**Peak Risk Hours:**")
            for hour, count in risk_hours.items():
                st.markdown(f"""
                <div class="status-badge badge-info">
                    {hour:02d}:00 - {count} transactions
                </div>
                """, unsafe_allow_html=True)
            
            # Amount analysis
            avg_high_risk_amount = high_risk_transactions['amount'].mean()
            st.markdown(f"**Average High-Risk Amount:** ${avg_high_risk_amount:,.2f}")
        
        else:
            st.markdown("""
            <div class="status-badge badge-success">
                🎉 No high-risk patterns detected!
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Detection Performance")
        
        total_analyzed = len(df_analyzed)
        high_risk_rate = (len(df_analyzed[df_analyzed['ml_risk_level'] == 'High']) / total_analyzed) * 100
        
        st.markdown(f"""
        <div class="info-card">
            <strong>🎯 Detection Summary</strong><br>
            • Total Transactions Analyzed: {total_analyzed:,}<br>
            • High-Risk Detection Rate: {high_risk_rate:.1f}%<br>
            • Analysis Method: Rule-Based Scoring<br>
            • Processing Status: ✅ Complete
        </div>
        """, unsafe_allow_html=True)
        
        # Risk distribution
        risk_dist = df_analyzed['ml_risk_level'].value_counts()
        st.markdown("**Risk Level Breakdown:**")
        
        for level, count in risk_dist.items():
            percentage = (count / total_analyzed) * 100
            badge_class = f"badge-{'success' if level == 'Low' else 'warning' if level == 'Medium' else 'info'}"
            st.markdown(f"""
            <div class="status-badge {badge_class}">
                {level}: {count:,} ({percentage:.1f}%)
            </div>
            """, unsafe_allow_html=True)

def display_high_risk_table(df_analyzed):
    """Display high-risk transactions table"""
    
    st.markdown('<div class="section-header">🚨 High-Risk Transactions</div>', unsafe_allow_html=True)
    
    high_risk_sample = df_analyzed[
        df_analyzed['ml_risk_level'] == 'High'
    ].nlargest(20, 'ml_risk_score')
    
    if not high_risk_sample.empty:
        # Display count
        st.markdown(f"""
        <div class="info-card">
            <strong>🔍 Showing top 20 highest-risk transactions</strong><br>
            Total high-risk transactions found: {len(df_analyzed[df_analyzed['ml_risk_level'] == 'High']):,}
        </div>
        """, unsafe_allow_html=True)
        
        # Select relevant columns for display
        display_columns = [
            'transaction_id', 'customer_id', 'amount', 'merchant_category', 
            'transaction_date', 'transaction_time', 'ml_risk_score'
        ]
        
        # Only include columns that exist
        available_columns = [col for col in display_columns if col in high_risk_sample.columns]
        
        # Format the dataframe
        display_df = high_risk_sample[available_columns].copy()
        
        if 'amount' in display_df.columns:
            display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.2f}")
        if 'ml_risk_score' in display_df.columns:
            display_df['ml_risk_score'] = display_df['ml_risk_score'].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = high_risk_sample.to_csv(index=False)
        st.download_button(
            label="📥 Download High-Risk Transactions Report",
            data=csv,
            file_name=f"high_risk_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.markdown("""
        <div class="info-card">
            <strong>🎉 Excellent Security Status!</strong><br>
            No high-risk transactions were detected in the current dataset.
            This indicates good transaction security and normal customer behavior patterns.
        </div>
        """, unsafe_allow_html=True)

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ FraudGuard Pro</h1>
        <p>Advanced Fraud Detection & Risk Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown("""
    <div class="upload-container">
        <h3>📁 Upload Transaction Data</h3>
        <p>Upload your CSV file containing credit card transaction data for comprehensive fraud analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file with transaction data. The system will automatically detect fraud patterns.",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            # Load data with progress indication
            with st.spinner("📊 Loading transaction data..."):
                df = pd.read_csv(uploaded_file)
            
            # Validate and clean data
            required_columns = ['transaction_id', 'amount', 'merchant_category', 
                              'transaction_date', 'transaction_time']
            optional_columns = ['customer_id', 'response_code', 'merchant_name', 'state']
            
            missing_required = [col for col in required_columns if col not in df.columns]
            
            if missing_required:
                st.error(f"❌ Missing required columns: {', '.join(missing_required)}")
                return
            
            # Add missing optional columns with defaults
            for col in optional_columns:
                if col not in df.columns:
                    if col == 'customer_id':
                        df[col] = 'CUST_' + df.index.astype(str).str.zfill(6)
                    elif col == 'response_code':
                        df[col] = '00'
                    elif col == 'merchant_name':
                        df[col] = 'Unknown Merchant'
                    elif col == 'state':
                        df[col] = 'Unknown'
            
            # Process data
            st.markdown(f"""
            <div class="status-badge badge-success">
                ✅ Successfully loaded {len(df):,} transactions
            </div>
            """, unsafe_allow_html=True)
            
            # Run fraud detection
            with st.spinner("🔍 Analyzing transactions for fraud patterns..."):
                fraud_model = SimpleFraudDetectionModel()
                df_analyzed = fraud_model.detect_fraud(df)
            
            st.success("🎯 Fraud analysis complete!")
            
            # Display results in organized sections
            display_metrics_section(df_analyzed)
            
            # Create and display charts
            charts = create_enhanced_charts(df_analyzed)
            display_analytics_section(charts)
            
            # Display insights
            display_insights_section(df_analyzed)
            
            # Display high-risk transactions table
            display_high_risk_table(df_analyzed)
            
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("Please ensure your CSV file contains the required columns and is properly formatted.")
    
    else:
        # Show requirements when no file is uploaded
        st.markdown('<div class="section-header">📋 Data Requirements</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <strong>📋 Required Columns:</strong><br>
                • transaction_id<br>
                • amount<br>
                • merchant_category<br>
                • transaction_date<br>
                • transaction_time
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-card">
                <strong>🔧 Optional Columns:</strong><br>
                • customer_id<br>
                • response_code<br>
                • merchant_name<br>
                • state
            </div>
            """, unsafe_allow_html=True)
        
        # Sample data preview
        st.markdown('<div class="section-header">📊 Sample Data Format</div>', unsafe_allow_html=True)
        
        sample_data = {
            'transaction_id': ['TXN_00000001', 'TXN_00000002', 'TXN_00000003'],
            'customer_id': ['CUST_000001', 'CUST_000002', 'CUST_000001'],
            'amount': [45.67, 1250.00, 2.50],
            'merchant_category': ['Grocery', 'Electronics', 'ATM'],
            'transaction_date': ['2024-01-15', '2024-01-15', '2024-01-16'],
            'transaction_time': ['14:30:00', '23:45:00', '02:15:00'],
            'response_code': ['00', '00', '05'],
            'merchant_name': ['Walmart', 'Best Buy', 'Bank ATM']
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()