import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="FraudGuard Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 2px dashed #dee2e6;
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .risk-high { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); }
    .risk-medium { background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); }
    .risk-low { background: linear-gradient(135deg, #48cab2 0%, #4ecdc4 100%); }
</style>
""", unsafe_allow_html=True)

def create_risk_score(row):
    """Create a risk score based on transaction characteristics"""
    risk_score = 0
    
    # Amount-based risk
    if row['amount'] > 1000:
        risk_score += 30
    elif row['amount'] > 500:
        risk_score += 15
    elif row['amount'] < 5:
        risk_score += 25
    
    # Time-based risk (if transaction is between 11 PM and 6 AM)
    hour = pd.to_datetime(row['transaction_time'], format='%H:%M:%S').hour
    if hour >= 23 or hour <= 6:
        risk_score += 20
    
    # Category-based risk
    high_risk_categories = ['ATM', 'Online Retail', 'Electronics']
    if row['merchant_category'] in high_risk_categories:
        risk_score += 15
    
    # Response code risk
    if row['response_code'] != '00':
        risk_score += 35
    
    # Known fraud flag
    if row['is_fraud'] == 1:
        risk_score = 95  # High risk for known fraud
    
    return min(risk_score, 100)  # Cap at 100

def analyze_data(df):
    """Analyze the uploaded data and return key metrics"""
    
    # Create risk scores
    df['risk_score'] = df.apply(create_risk_score, axis=1)
    
    # Define risk categories
    df['risk_category'] = pd.cut(df['risk_score'], 
                                bins=[0, 30, 70, 100], 
                                labels=['Low', 'Medium', 'High'])
    
    # Calculate metrics
    total_transactions = len(df)
    high_risk_count = len(df[df['risk_category'] == 'High'])
    high_risk_percentage = (high_risk_count / total_transactions) * 100
    
    # Transaction volume trends
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    daily_volume = df.groupby('transaction_date').size().reset_index(name='count')
    
    # Risk score distribution
    risk_distribution = df['risk_category'].value_counts()
    
    return {
        'total_transactions': total_transactions,
        'high_risk_count': high_risk_count,
        'high_risk_percentage': high_risk_percentage,
        'daily_volume': daily_volume,
        'risk_distribution': risk_distribution,
        'df_with_risk': df
    }

def create_volume_trend_chart(daily_volume):
    """Create transaction volume trend chart"""
    fig = px.line(daily_volume, 
                  x='transaction_date', 
                  y='count',
                  title='Transaction Volume Trends',
                  color_discrete_sequence=['#2a5298'])
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_size=20,
        title_font_color='#2a5298',
        xaxis_title="Date",
        yaxis_title="Number of Transactions"
    )
    
    return fig

def create_risk_distribution_chart(risk_distribution):
    """Create risk score distribution chart"""
    colors = ['#48cab2', '#feca57', '#ff6b6b']
    
    fig = px.pie(values=risk_distribution.values,
                 names=risk_distribution.index,
                 title='Risk Score Distribution',
                 color_discrete_sequence=colors)
    
    fig.update_layout(
        title_font_size=20,
        title_font_color='#2a5298',
        paper_bgcolor='white'
    )
    
    return fig

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ FraudGuard Pro</h1>
        <p>Advanced Credit Card Fraud Detection & Analysis Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown("""
    <div class="upload-section">
        <h3>📁 Upload Transaction Data</h3>
        <p>Upload your CSV file containing credit card transaction data for analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file with transaction data including columns: transaction_id, amount, merchant_category, transaction_date, transaction_time, response_code, is_fraud"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_columns = ['transaction_id', 'amount', 'merchant_category', 
                              'transaction_date', 'transaction_time', 'response_code', 'is_fraud']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
                st.info("Please ensure your CSV file contains all required columns.")
                return
            
            # Analyze data
            analysis_results = analyze_data(df)
            
            st.success(f"✅ Successfully loaded {len(df)} transactions!")
            
            # Display key metrics
            st.markdown("## 📊 Key Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{analysis_results['total_transactions']:,}</p>
                    <p class="metric-label">Total Transactions</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card risk-high">
                    <p class="metric-value">{analysis_results['high_risk_count']:,}</p>
                    <p class="metric-label">High Risk Flagged</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card risk-medium">
                    <p class="metric-value">{analysis_results['high_risk_percentage']:.1f}%</p>
                    <p class="metric-label">High Risk Rate</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                avg_amount = df['amount'].mean()
                st.markdown(f"""
                <div class="metric-card risk-low">
                    <p class="metric-value">${avg_amount:,.2f}</p>
                    <p class="metric-label">Average Transaction</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Charts section
            st.markdown("## 📈 Analytics Dashboard")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Transaction volume trends
                volume_chart = create_volume_trend_chart(analysis_results['daily_volume'])
                st.plotly_chart(volume_chart, use_container_width=True)
            
            with col2:
                # Risk distribution
                risk_chart = create_risk_distribution_chart(analysis_results['risk_distribution'])
                st.plotly_chart(risk_chart, use_container_width=True)
            
            # Additional insights
            st.markdown("## 🔍 Additional Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top risk merchants
                st.markdown("### 🏪 High-Risk Merchant Categories")
                risk_by_category = df.groupby('merchant_category')['risk_score'].mean().sort_values(ascending=False)
                top_risk_categories = risk_by_category.head(5)
                
                for category, score in top_risk_categories.items():
                    st.write(f"**{category}**: {score:.1f} avg risk score")
            
            with col2:
                # Risk summary
                st.markdown("### ⚠️ Risk Summary")
                risk_counts = analysis_results['risk_distribution']
                st.write(f"🟢 **Low Risk**: {risk_counts.get('Low', 0):,} transactions")
                st.write(f"🟡 **Medium Risk**: {risk_counts.get('Medium', 0):,} transactions")
                st.write(f"🔴 **High Risk**: {risk_counts.get('High', 0):,} transactions")
            
            # Show sample high-risk transactions
            st.markdown("## 🚨 Sample High-Risk Transactions")
            high_risk_sample = analysis_results['df_with_risk'][
                analysis_results['df_with_risk']['risk_category'] == 'High'
            ].head(10)
            
            if not high_risk_sample.empty:
                display_columns = ['transaction_id', 'amount', 'merchant_category', 
                                 'transaction_date', 'risk_score', 'is_fraud']
                st.dataframe(high_risk_sample[display_columns], use_container_width=True)
            else:
                st.info("No high-risk transactions found in the current dataset.")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please check your file format and ensure it contains the required columns.")
    
    else:
        # Show sample data format
        st.markdown("## 📋 Sample Data Format")
        st.info("Upload a CSV file with the following structure:")
        
        sample_data = {
            'transaction_id': ['TXN_00000001', 'TXN_00000002', 'TXN_00000003'],
            'amount': [45.67, 1250.00, 2.50],
            'merchant_category': ['Grocery', 'Electronics', 'ATM'],
            'transaction_date': ['2024-01-15', '2024-01-15', '2024-01-16'],
            'transaction_time': ['14:30:00', '23:45:00', '02:15:00'],
            'response_code': ['00', '00', '05'],
            'is_fraud': [0, 1, 0]
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)

if __name__ == "__main__":
    main()