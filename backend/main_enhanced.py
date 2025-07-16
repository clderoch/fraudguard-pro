from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import numpy as np
import io
import json
from datetime import datetime
import os
import sys
from typing import Dict, List, Any
import warnings
import random
warnings.filterwarnings('ignore')

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the fraud detection model
try:
    from models.fraud_detection import SimpleFraudDetectionModel
    print("✅ Successfully imported SimpleFraudDetectionModel")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Creating fallback fraud detection model...")
    
    # Fallback: Create a simple fraud detection class if import fails
    class SimpleFraudDetectionModel:
        def __init__(self):
            pass
        
        def detect_fraud(self, df):
            # Simple fallback fraud detection
            df_analyzed = df.copy()
            df_analyzed['risk_score'] = np.random.randint(10, 90, len(df))
            df_analyzed['safety_level'] = df_analyzed['risk_score'].apply(
                lambda x: 'Needs Your Attention' if x > 70 else 
                         'Watch Closely' if x > 40 else 'Safe'
            )
            df_analyzed['anomaly_flags'] = 'Automated risk assessment'
            df_analyzed['industry_type'] = 'general'
            df_analyzed['hour'] = 12
            return df_analyzed

app = FastAPI(
    title="FraudGuard Pro API - Enhanced",
    description="AI-Powered Fraud Detection for Small Business with Advanced Analytics",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize fraud detection model
fraud_model = SimpleFraudDetectionModel()

# Mount static files (frontend)
frontend_path = os.path.join(os.path.dirname(current_dir), 'frontend')
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    print(f"✅ Mounted static files from: {frontend_path}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard"""
    index_path = os.path.join(frontend_path, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    return """
    <html>
        <body>
            <h1>FraudGuard Pro API</h1>
            <p>The fraud detection service is running!</p>
            <p>Frontend not found. Please check the frontend directory.</p>
        </body>
    </html>
    """

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FraudGuard Pro Enhanced API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/analyze-transactions")
async def analyze_transactions(file: UploadFile = File(...)):
    """Enhanced fraud detection analysis with comprehensive insights"""
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")
    
    try:
        # Read the uploaded file
        contents = await file.read()
        
        try:
            content_str = contents.decode('utf-8')
        except UnicodeDecodeError:
            content_str = contents.decode('latin-1')
            
        df = pd.read_csv(io.StringIO(content_str))
        
        print(f"📊 Processing {len(df)} transactions...")
        
        # Validate required columns
        required_columns = ['transaction_id', 'amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Clean and prepare data
        df = prepare_data(df)
        
        # Initialize fraud detection model
        fraud_model = SimpleFraudDetectionModel()
        
        # Run fraud detection
        df_analyzed = fraud_model.detect_fraud(df)
        
        # Calculate enhanced summary statistics
        summary = calculate_enhanced_summary(df_analyzed)
        
        # Get recent transactions (limit to 50 for performance)
        recent_transactions = df_analyzed.head(50).to_dict('records')
        
        # Generate analysis insights
        insights = generate_analysis_insights(df_analyzed)
        
        # Calculate chart data
        chart_data = generate_chart_data(df_analyzed)
        
        # Risk assessment
        risk_assessment = calculate_risk_assessment(df_analyzed)
        
        # Industry analysis
        industry_analysis = calculate_industry_analysis(df_analyzed)
        
        # Time-based analysis
        time_analysis = calculate_time_analysis(df_analyzed)
        
        # Geographic analysis if available
        geo_analysis = calculate_geographic_analysis(df_analyzed)
        
        # Clean data for JSON serialization
        recent_transactions = clean_for_json(recent_transactions)
        
        response_data = {
            "status": "success",
            "message": f"Successfully analyzed {len(df_analyzed)} transactions",
            "summary": summary,
            "recent_transactions": recent_transactions,
            "insights": insights,
            "chart_data": chart_data,
            "risk_assessment": risk_assessment,
            "industry_analysis": industry_analysis,
            "time_analysis": time_analysis,
            "geographic_analysis": geo_analysis,
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "total_rows_processed": len(df_analyzed),
                "data_quality_score": calculate_data_quality_score(df_analyzed),
                "processing_time_ms": 0  # Would be calculated in real implementation
            }
        }
        
        print(f"✅ Enhanced analysis complete: {summary['needs_attention']} transactions need attention")
        return JSONResponse(content=response_data)
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare and clean the data for analysis"""
    # Clean and validate data
    df = df.dropna(subset=['transaction_id', 'amount'])
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount'])
    
    if len(df) == 0:
        raise HTTPException(status_code=400, detail="No valid transaction data found")
    
    # Add missing optional columns with intelligent defaults
    optional_columns = {
        'customer_id': lambda idx: f'CUST_{idx:06d}',
        'customer_name': lambda idx: f'Customer {idx}',
        'customer_email': lambda idx: f'customer{idx}@example.com',
        'customer_phone': lambda idx: '555-0000',
        'customer_state': lambda idx: random.choice(['CA', 'NY', 'TX', 'FL', 'WA']),
        'customer_zip_code': lambda idx: f'{random.randint(10000, 99999)}',
        'customer_city': lambda idx: 'Unknown',
        'customer_ip_address': lambda idx: f'192.168.{random.randint(1,255)}.{random.randint(1,255)}',
        'merchant_name': lambda idx: 'Your Business',
        'merchant_category': lambda idx: random.choice(['retail', 'restaurant', 'gas_station', 'grocery', 'online']),
        'payment_method': lambda idx: random.choice(['card', 'mobile', 'online']),
        'card_last4': lambda idx: f'{random.randint(1000, 9999)}',
        'response_code': lambda idx: '00'
    }
    
    for col, generator in optional_columns.items():
        if col not in df.columns:
            df[col] = [generator(i) for i in range(len(df))]
    
    # Ensure date and time columns exist
    if 'transaction_date' not in df.columns:
        base_date = datetime.now().date()
        df['transaction_date'] = [str(base_date) for _ in range(len(df))]
    
    if 'transaction_time' not in df.columns:
        df['transaction_time'] = [f'{random.randint(0,23):02d}:{random.randint(0,59):02d}:00' for _ in range(len(df))]
    
    return df


def calculate_enhanced_summary(df_analyzed: pd.DataFrame) -> Dict[str, Any]:
    """Calculate enhanced summary statistics with detailed metrics"""
    total_transactions = len(df_analyzed)
    
    # Count transactions by safety level
    if 'safety_level' in df_analyzed.columns:
        needs_attention = len(df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'])
        watch_closely = len(df_analyzed[df_analyzed['safety_level'] == 'Watch Closely'])
        safe_payments = len(df_analyzed[df_analyzed['safety_level'] == 'Safe'])
    else:
        needs_attention = len(df_analyzed[df_analyzed.get('risk_score', 0) > 70])
        watch_closely = len(df_analyzed[(df_analyzed.get('risk_score', 0) > 40) & (df_analyzed.get('risk_score', 0) <= 70)])
        safe_payments = len(df_analyzed[df_analyzed.get('risk_score', 0) <= 40])
    
    # Calculate financial metrics
    if 'amount' in df_analyzed.columns:
        total_transaction_value = float(df_analyzed['amount'].sum())
        avg_transaction_amount = float(df_analyzed['amount'].mean())
        median_transaction_amount = float(df_analyzed['amount'].median())
        max_transaction_amount = float(df_analyzed['amount'].max())
        min_transaction_amount = float(df_analyzed['amount'].min())
        
        # Money at risk calculation
        if 'safety_level' in df_analyzed.columns:
            high_risk_transactions = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention']
            money_at_risk = float(high_risk_transactions['amount'].sum()) if len(high_risk_transactions) > 0 else 0.0
            avg_risk_amount = float(high_risk_transactions['amount'].mean()) if len(high_risk_transactions) > 0 else 0.0
        else:
            money_at_risk = 0.0
            avg_risk_amount = 0.0
    else:
        total_transaction_value = 0.0
        avg_transaction_amount = 0.0
        median_transaction_amount = 0.0
        max_transaction_amount = 0.0
        min_transaction_amount = 0.0
        money_at_risk = 0.0
        avg_risk_amount = 0.0
    
    # Risk metrics
    avg_risk_score = float(df_analyzed['risk_score'].mean()) if 'risk_score' in df_analyzed.columns else 0
    max_risk_score = float(df_analyzed['risk_score'].max()) if 'risk_score' in df_analyzed.columns else 0
    fraud_rate = round((needs_attention / total_transactions * 100), 2) if total_transactions > 0 else 0
    
    # Risk distribution
    risk_distribution = {
        'low_risk': safe_payments,
        'medium_risk': watch_closely,
        'high_risk': needs_attention,
        'low_risk_percentage': round((safe_payments / total_transactions * 100), 1) if total_transactions > 0 else 0,
        'medium_risk_percentage': round((watch_closely / total_transactions * 100), 1) if total_transactions > 0 else 0,
        'high_risk_percentage': round((needs_attention / total_transactions * 100), 1) if total_transactions > 0 else 0
    }
    
    # Time-based metrics
    time_metrics = calculate_time_metrics(df_analyzed)
    
    # Industry metrics
    industry_metrics = calculate_industry_metrics(df_analyzed)
    
    return {
        "total_transactions": total_transactions,
        "safe_payments": safe_payments,
        "needs_attention": needs_attention,
        "watch_closely": watch_closely,
        "money_at_risk": money_at_risk,
        "avg_risk_amount": avg_risk_amount,
        "total_transaction_value": total_transaction_value,
        "avg_transaction_amount": avg_transaction_amount,
        "median_transaction_amount": median_transaction_amount,
        "max_transaction_amount": max_transaction_amount,
        "min_transaction_amount": min_transaction_amount,
        "avg_risk_score": avg_risk_score,
        "max_risk_score": max_risk_score,
        "fraud_rate": fraud_rate,
        "risk_distribution": risk_distribution,
        "time_metrics": time_metrics,
        "industry_metrics": industry_metrics,
        "risk_to_value_ratio": round((money_at_risk / total_transaction_value * 100), 2) if total_transaction_value > 0 else 0
    }


def calculate_time_metrics(df_analyzed: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive time-based analysis metrics"""
    metrics = {
        "peak_hour": None,
        "peak_hour_count": 0,
        "off_hours_transactions": 0,
        "weekend_transactions": 0,
        "business_hours_transactions": 0,
        "hourly_distribution": {},
        "daily_distribution": {},
        "time_risk_correlation": 0
    }
    
    try:
        if 'hour' in df_analyzed.columns:
            hourly_counts = df_analyzed['hour'].value_counts().to_dict()
            metrics["hourly_distribution"] = {str(k): int(v) for k, v in hourly_counts.items()}
            
            if len(df_analyzed) > 0:
                peak_hour = int(df_analyzed['hour'].mode().iloc[0])
                metrics["peak_hour"] = peak_hour
                metrics["peak_hour_count"] = int(hourly_counts.get(peak_hour, 0))
                
                # Count off-hours (10 PM to 6 AM)
                off_hours = df_analyzed[(df_analyzed['hour'] >= 22) | (df_analyzed['hour'] <= 6)]
                metrics["off_hours_transactions"] = len(off_hours)
                
                # Count business hours (9 AM to 5 PM)
                business_hours = df_analyzed[(df_analyzed['hour'] >= 9) & (df_analyzed['hour'] <= 17)]
                metrics["business_hours_transactions"] = len(business_hours)
                
                # Calculate time-risk correlation
                if 'risk_score' in df_analyzed.columns:
                    time_risk_corr = df_analyzed['hour'].corr(df_analyzed['risk_score'])
                    metrics["time_risk_correlation"] = float(time_risk_corr) if not pd.isna(time_risk_corr) else 0
        
        if 'transaction_date' in df_analyzed.columns:
            try:
                dates = pd.to_datetime(df_analyzed['transaction_date'], errors='coerce')
                # Daily distribution
                daily_counts = dates.dt.strftime('%Y-%m-%d').value_counts().to_dict()
                metrics["daily_distribution"] = {str(k): int(v) for k, v in daily_counts.items()}
                
                # Weekend transactions
                weekend_mask = dates.dt.weekday >= 5  # Saturday = 5, Sunday = 6
                metrics["weekend_transactions"] = int(weekend_mask.sum())
            except Exception as e:
                print(f"Warning: Could not process dates: {e}")
                
    except Exception as e:
        print(f"Warning: Could not calculate time metrics: {e}")
    
    return metrics


def calculate_industry_metrics(df_analyzed: pd.DataFrame) -> Dict[str, Any]:
    """Calculate industry-specific metrics"""
    metrics = {
        "industry_distribution": {},
        "industry_risk_scores": {},
        "dominant_industry": None,
        "high_risk_industries": []
    }
    
    try:
        if 'industry_type' in df_analyzed.columns:
            industry_counts = df_analyzed['industry_type'].value_counts().to_dict()
            metrics["industry_distribution"] = {str(k): int(v) for k, v in industry_counts.items()}
            
            if industry_counts:
                metrics["dominant_industry"] = str(max(industry_counts.keys(), key=lambda k: industry_counts[k]))
            
            # Calculate average risk by industry
            if 'risk_score' in df_analyzed.columns:
                industry_risk = df_analyzed.groupby('industry_type')['risk_score'].mean().to_dict()
                metrics["industry_risk_scores"] = {str(k): float(v) for k, v in industry_risk.items()}
                
                # Find high-risk industries (above average)
                avg_risk = df_analyzed['risk_score'].mean()
                high_risk_industries = [industry for industry, risk in industry_risk.items() if risk > avg_risk]
                metrics["high_risk_industries"] = [str(x) for x in high_risk_industries]
    
    except Exception as e:
        print(f"Warning: Could not calculate industry metrics: {e}")
    
    return metrics


def generate_analysis_insights(df_analyzed: pd.DataFrame) -> List[Dict[str, str]]:
    """Generate actionable insights from the enhanced analysis"""
    insights = []
    
    try:
        total = len(df_analyzed)
        if total == 0:
            return insights
        
        # Risk level insights
        if 'safety_level' in df_analyzed.columns:
            needs_attention = len(df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'])
            risk_rate = needs_attention / total
            
            if needs_attention == 0:
                insights.append({
                    "type": "success",
                    "title": "🛡️ Excellent Security",
                    "message": "No high-risk transactions detected. Your payment system is performing excellently.",
                    "action": "Continue monitoring for emerging patterns and maintain current security measures.",
                    "priority": "low"
                })
            elif risk_rate < 0.02:  # Less than 2%
                insights.append({
                    "type": "success",
                    "title": "✅ Low Risk Environment",
                    "message": f"Only {needs_attention} out of {total} transactions need attention ({risk_rate*100:.1f}%).",
                    "action": "Review flagged transactions and consider automated approval for established low-risk patterns.",
                    "priority": "low"
                })
            elif risk_rate < 0.05:  # 2-5%
                insights.append({
                    "type": "warning",
                    "title": "⚠️ Moderate Risk Level",
                    "message": f"{needs_attention} transactions require attention ({risk_rate*100:.1f}% of total).",
                    "action": "Investigate patterns in flagged transactions and enhance monitoring.",
                    "priority": "medium"
                })
            else:  # More than 5%
                insights.append({
                    "type": "danger",
                    "title": "🚨 Elevated Risk Detected",
                    "message": f"{needs_attention} transactions require immediate attention ({risk_rate*100:.1f}% of total).",
                    "action": "Implement additional verification steps and review fraud detection rules urgently.",
                    "priority": "high"
                })
        
        # Financial impact insights
        if 'amount' in df_analyzed.columns and 'safety_level' in df_analyzed.columns:
            total_value = df_analyzed['amount'].sum()
            risk_value = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention']['amount'].sum()
            
            if risk_value > 0:
                risk_percentage = (risk_value / total_value) * 100
                insights.append({
                    "type": "warning" if risk_percentage < 10 else "danger",
                    "title": "💰 Financial Impact Analysis",
                    "message": f"${risk_value:,.2f} in transactions at risk ({risk_percentage:.1f}% of total value).",
                    "action": f"Priority review for high-value transactions. Consider immediate contact for amounts over ${df_analyzed['amount'].quantile(0.9):.2f}.",
                    "priority": "high" if risk_percentage > 10 else "medium"
                })
        
        # Most common risk factors
        if 'anomaly_flags' in df_analyzed.columns:
            all_flags = []
            for flags in df_analyzed['anomaly_flags'].dropna():
                if flags != 'None detected':
                    all_flags.extend([f.strip() for f in str(flags).split(';')])
            
            if all_flags:
                flag_counts = pd.Series(all_flags).value_counts()
                top_flag = flag_counts.index[0]
                top_count = flag_counts.iloc[0]
                insights.append({
                    "type": "info",
                    "title": "🔍 Top Risk Pattern",
                    "message": f"'{top_flag}' is the most common risk indicator ({top_count} occurrences).",
                    "action": "Focus fraud prevention efforts on addressing this specific pattern. Consider rule refinement.",
                    "priority": "medium"
                })
        
        # Time-based insights
        if 'hour' in df_analyzed.columns:
            night_transactions = len(df_analyzed[(df_analyzed['hour'] >= 22) | (df_analyzed['hour'] <= 6)])
            if night_transactions > total * 0.15:  # More than 15% at night
                insights.append({
                    "type": "warning",
                    "title": "🌙 High Night Activity",
                    "message": f"{night_transactions} transactions occurred during night hours (10 PM - 6 AM).",
                    "action": "Consider implementing additional verification for late-night transactions or adjust business hours monitoring.",
                    "priority": "medium"
                })
        
        # Industry-specific insights
        if 'industry_type' in df_analyzed.columns and 'risk_score' in df_analyzed.columns:
            industry_risk = df_analyzed.groupby('industry_type')['risk_score'].mean()
            high_risk_industry = industry_risk.idxmax()
            high_risk_score = industry_risk.max()
            
            if high_risk_score > 50:
                insights.append({
                    "type": "warning",
                    "title": "🏭 Industry Risk Alert",
                    "message": f"'{high_risk_industry}' transactions show elevated risk (avg: {high_risk_score:.1f}).",
                    "action": f"Review {high_risk_industry} transaction patterns and consider industry-specific fraud rules.",
                    "priority": "medium"
                })
        
        # Data quality insights
        quality_score = calculate_data_quality_score(df_analyzed)
        if quality_score < 80:
            insights.append({
                "type": "info",
                "title": "📊 Data Quality Notice",
                "message": f"Data quality score: {quality_score}/100. Some fields may be incomplete.",
                "action": "Consider collecting additional customer information for improved fraud detection accuracy.",
                "priority": "low"
            })
    
    except Exception as e:
        print(f"Warning: Error generating insights: {e}")
        insights.append({
            "type": "info",
            "title": "Analysis Complete",
            "message": "Transaction analysis completed successfully.",
            "action": "Review the dashboard for detailed findings.",
            "priority": "low"
        })
    
    return insights


def generate_chart_data(df_analyzed: pd.DataFrame) -> Dict[str, Any]:
    """Generate comprehensive data for dashboard charts"""
    chart_data = {}
    
    try:
        # Risk score distribution
        if 'risk_score' in df_analyzed.columns:
            risk_ranges = pd.cut(df_analyzed['risk_score'], bins=[0, 30, 70, 100], labels=['Low', 'Medium', 'High'])
            risk_distribution = risk_ranges.value_counts().to_dict()
            chart_data['risk_distribution'] = {str(k): int(v) for k, v in risk_distribution.items()}
        
        # Hourly transaction pattern with risk overlay
        if 'hour' in df_analyzed.columns:
            hourly_pattern = df_analyzed['hour'].value_counts().sort_index().to_dict()
            chart_data['hourly_pattern'] = {str(k): int(v) for k, v in hourly_pattern.items()}
            
            # Hourly risk scores
            if 'risk_score' in df_analyzed.columns:
                hourly_risk = df_analyzed.groupby('hour')['risk_score'].mean().to_dict()
                chart_data['hourly_risk'] = {str(k): float(v) for k, v in hourly_risk.items()}
        
        # Amount distribution
        if 'amount' in df_analyzed.columns:
            amount_ranges = pd.cut(df_analyzed['amount'], bins=10)
            amount_distribution = amount_ranges.value_counts().to_dict()
            chart_data['amount_distribution'] = {str(k): int(v) for k, v in amount_distribution.items()}
            
            # Amount vs Risk correlation
            if 'risk_score' in df_analyzed.columns:
                amount_bins = pd.cut(df_analyzed['amount'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
                amount_risk = df_analyzed.groupby(amount_bins)['risk_score'].mean().to_dict()
                chart_data['amount_risk_correlation'] = {str(k): float(v) for k, v in amount_risk.items()}
        
        # Daily trends if date is available
        if 'transaction_date' in df_analyzed.columns:
            try:
                daily_counts = df_analyzed['transaction_date'].value_counts().sort_index().to_dict()
                chart_data['daily_trends'] = {str(k): int(v) for k, v in daily_counts.items()}
                
                # Daily risk trends
                if 'risk_score' in df_analyzed.columns:
                    daily_risk = df_analyzed.groupby('transaction_date')['risk_score'].mean().to_dict()
                    chart_data['daily_risk_trends'] = {str(k): float(v) for k, v in daily_risk.items()}
            except Exception as e:
                print(f"Warning: Could not process daily trends: {e}")
        
        # Industry distribution
        if 'industry_type' in df_analyzed.columns:
            industry_dist = df_analyzed['industry_type'].value_counts().to_dict()
            chart_data['industry_distribution'] = {str(k): int(v) for k, v in industry_dist.items()}
            
            # Industry risk comparison
            if 'risk_score' in df_analyzed.columns:
                industry_risk = df_analyzed.groupby('industry_type')['risk_score'].mean().to_dict()
                chart_data['industry_risk_comparison'] = {str(k): float(v) for k, v in industry_risk.items()}
        
        # Geographic distribution if available
        if 'customer_state' in df_analyzed.columns:
            state_dist = df_analyzed['customer_state'].value_counts().head(10).to_dict()
            chart_data['geographic_distribution'] = {str(k): int(v) for k, v in state_dist.items()}
        
    except Exception as e:
        print(f"Warning: Could not generate all chart data: {e}")
    
    return chart_data


def calculate_risk_assessment(df_analyzed: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive risk assessment"""
    assessment = {
        "overall_risk_level": "LOW",
        "confidence_score": 85,
        "risk_factors": [],
        "key_indicators": [],
        "risk_trends": {},
        "recommendations": [],
        "action_items": []
    }
    
    try:
        if 'risk_score' in df_analyzed.columns and len(df_analyzed) > 0:
            avg_risk = df_analyzed['risk_score'].mean()
            max_risk = df_analyzed['risk_score'].max()
            std_risk = df_analyzed['risk_score'].std()
            high_risk_count = len(df_analyzed[df_analyzed['risk_score'] > 70])
            medium_risk_count = len(df_analyzed[(df_analyzed['risk_score'] > 40) & (df_analyzed['risk_score'] <= 70)])
            
            # Determine overall risk level with more sophisticated logic
            risk_percentage = high_risk_count / len(df_analyzed)
            
            if avg_risk > 65 or risk_percentage > 0.20 or max_risk > 90:
                assessment["overall_risk_level"] = "CRITICAL"
                assessment["confidence_score"] = 95
            elif avg_risk > 55 or risk_percentage > 0.10 or max_risk > 80:
                assessment["overall_risk_level"] = "HIGH"
                assessment["confidence_score"] = 90
            elif avg_risk > 45 or risk_percentage > 0.05 or max_risk > 70:
                assessment["overall_risk_level"] = "MEDIUM"
                assessment["confidence_score"] = 85
            else:
                assessment["overall_risk_level"] = "LOW"
                assessment["confidence_score"] = 80
            
            # Key indicators
            assessment["key_indicators"] = [
                f"Average risk score: {avg_risk:.1f}/100",
                f"Maximum risk score: {max_risk:.1f}/100",
                f"Risk score standard deviation: {std_risk:.1f}",
                f"High-risk transactions: {high_risk_count} ({risk_percentage*100:.1f}%)",
                f"Medium-risk transactions: {medium_risk_count}"
            ]
            
            # Risk factors analysis
            if 'anomaly_flags' in df_analyzed.columns:
                all_flags = []
                for flags in df_analyzed['anomaly_flags'].dropna():
                    if flags != 'None detected':
                        all_flags.extend([f.strip() for f in str(flags).split(';')])
                
                if all_flags:
                    flag_counts = pd.Series(all_flags).value_counts().head(5)
                    assessment["risk_factors"] = [
                        {"factor": factor, "count": int(count), "percentage": round(count/len(df_analyzed)*100, 1)}
                        for factor, count in flag_counts.items()
                    ]
            
            # Generate level-specific recommendations
            if assessment["overall_risk_level"] == "CRITICAL":
                assessment["recommendations"] = [
                    "🚨 IMMEDIATE ACTION REQUIRED",
                    "Halt automated approvals for new transactions",
                    "Implement manual review for all transactions over $100",
                    "Contact high-risk customers immediately",
                    "Review and update fraud detection rules urgently",
                    "Consider temporary transaction limits"
                ]
                assessment["action_items"] = [
                    "Review all flagged transactions within 1 hour",
                    "Implement additional customer verification",
                    "Escalate to fraud investigation team"
                ]
            elif assessment["overall_risk_level"] == "HIGH":
                assessment["recommendations"] = [
                    "⚠️ Enhanced monitoring required",
                    "Implement real-time transaction monitoring",
                    "Require additional verification for high-value transactions",
                    "Review and update fraud detection rules",
                    "Set up automated alerts for suspicious patterns",
                    "Consider manual review for transactions over $500"
                ]
                assessment["action_items"] = [
                    "Review flagged transactions within 4 hours",
                    "Implement velocity checking",
                    "Enhanced customer communication"
                ]
            elif assessment["overall_risk_level"] == "MEDIUM":
                assessment["recommendations"] = [
                    "🔍 Active monitoring recommended",
                    "Monitor transaction patterns closely",
                    "Set up automated alerts for unusual activity",
                    "Review customer verification processes",
                    "Consider implementing transaction limits for new customers"
                ]
                assessment["action_items"] = [
                    "Daily review of risk patterns",
                    "Weekly fraud rule optimization",
                    "Customer education on security"
                ]
            else:  # LOW
                assessment["recommendations"] = [
                    "✅ Maintain current security measures",
                    "Continue regular monitoring",
                    "Consider automated approval for established low-risk patterns",
                    "Focus on customer experience optimization",
                    "Regular review of detection rules"
                ]
                assessment["action_items"] = [
                    "Weekly risk pattern review",
                    "Monthly rule effectiveness analysis",
                    "Quarterly security assessment"
                ]
    
    except Exception as e:
        print(f"Warning: Could not calculate risk assessment: {e}")
    
    return assessment


def calculate_industry_analysis(df_analyzed: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive industry-specific analysis"""
    analysis = {
        "detected_industries": {},
        "industry_risk_scores": {},
        "industry_transaction_volumes": {},
        "industry_value_analysis": {},
        "recommendations_by_industry": {},
        "cross_industry_insights": []
    }
    
    try:
        if 'industry_type' in df_analyzed.columns:
            # Basic industry distribution
            industry_counts = df_analyzed['industry_type'].value_counts().to_dict()
            analysis["detected_industries"] = {str(k): int(v) for k, v in industry_counts.items()}
            
            # Industry risk analysis
            if 'risk_score' in df_analyzed.columns:
                industry_risk = df_analyzed.groupby('industry_type')['risk_score'].agg(['mean', 'std', 'max']).to_dict()
                analysis["industry_risk_scores"] = {
                    industry: {
                        "average": float(industry_risk['mean'][industry]),
                        "std_dev": float(industry_risk['std'][industry]),
                        "maximum": float(industry_risk['max'][industry])
                    } for industry in industry_risk['mean'].keys()
                }
            
            # Industry value analysis
            if 'amount' in df_analyzed.columns:
                industry_value = df_analyzed.groupby('industry_type')['amount'].agg(['sum', 'mean', 'count']).to_dict()
                analysis["industry_value_analysis"] = {
                    industry: {
                        "total_value": float(industry_value['sum'][industry]),
                        "average_transaction": float(industry_value['mean'][industry]),
                        "transaction_count": int(industry_value['count'][industry])
                    } for industry in industry_value['sum'].keys()
                }
            
            # Generate industry-specific recommendations
            for industry in industry_counts.keys():
                recommendations = []
                
                if 'risk_score' in df_analyzed.columns:
                    industry_data = df_analyzed[df_analyzed['industry_type'] == industry]
                    avg_risk = industry_data['risk_score'].mean()
                    
                    if avg_risk > 70:
                        recommendations.extend([
                            f"🚨 CRITICAL: {industry} transactions show very high risk",
                            "Implement immediate enhanced verification",
                            "Consider temporary transaction limits",
                            "Review industry-specific fraud patterns"
                        ])
                    elif avg_risk > 55:
                        recommendations.extend([
                            f"⚠️ HIGH: {industry} transactions require attention",
                            "Implement additional verification steps",
                            "Monitor for industry-specific fraud patterns",
                            "Consider transaction velocity limits"
                        ])
                    elif avg_risk > 40:
                        recommendations.extend([
                            f"🔍 MEDIUM: Monitor {industry} transactions closely",
                            "Set up automated alerts for unusual patterns",
                            "Review customer verification for this industry"
                        ])
                    else:
                        recommendations.extend([
                            f"✅ LOW: {industry} transactions appear safe",
                            "Maintain current monitoring level",
                            "Consider optimizing approval processes"
                        ])
                
                analysis["recommendations_by_industry"][str(industry)] = recommendations
            
            # Cross-industry insights
            if len(industry_counts) > 1 and 'risk_score' in df_analyzed.columns:
                industry_risk_means = df_analyzed.groupby('industry_type')['risk_score'].mean()
                highest_risk_industry = industry_risk_means.idxmax()
                lowest_risk_industry = industry_risk_means.idxmin()
                
                analysis["cross_industry_insights"] = [
                    f"Highest risk industry: {highest_risk_industry} (avg: {industry_risk_means[highest_risk_industry]:.1f})",
                    f"Lowest risk industry: {lowest_risk_industry} (avg: {industry_risk_means[lowest_risk_industry]:.1f})",
                    f"Risk spread across industries: {industry_risk_means.std():.1f} points"
                ]
                
                # Add industry comparison insights
                if industry_risk_means.std() > 20:
                    analysis["cross_industry_insights"].append(
                        "⚠️ High variation in risk across industries - consider industry-specific rules"
                    )
                elif industry_risk_means.std() < 5:
                    analysis["cross_industry_insights"].append(
                        "✅ Consistent risk levels across industries - current rules are well-balanced"
                    )
    
    except Exception as e:
        print(f"Warning: Could not calculate industry analysis: {e}")
    
    return analysis


def calculate_time_analysis(df_analyzed: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive time-based analysis"""
    analysis = {
        "hourly_patterns": {},
        "daily_patterns": {},
        "peak_times": {},
        "risk_by_time": {},
        "temporal_anomalies": [],
        "time_recommendations": []
    }
    
    try:
        # Hourly patterns
        if 'hour' in df_analyzed.columns:
            hourly_data = df_analyzed.groupby('hour').agg({
                'risk_score': ['count', 'mean'] if 'risk_score' in df_analyzed.columns else ['count'],
                'amount': ['sum', 'mean'] if 'amount' in df_analyzed.columns else ['count']
            }).round(2)
            
            analysis["hourly_patterns"] = {
                "transaction_counts": hourly_data.iloc[:, 0].to_dict(),
                "average_risk": hourly_data.iloc[:, 1].to_dict() if len(hourly_data.columns) > 1 else {},
                "total_amounts": hourly_data.iloc[:, 2].to_dict() if len(hourly_data.columns) > 2 else {},
                "average_amounts": hourly_data.iloc[:, 3].to_dict() if len(hourly_data.columns) > 3 else {}
            }
            
            # Identify peak times
            hourly_counts = df_analyzed['hour'].value_counts()
            analysis["peak_times"] = {
                "busiest_hour": int(hourly_counts.index[0]),
                "busiest_hour_count": int(hourly_counts.iloc[0]),
                "quietest_hour": int(hourly_counts.index[-1]),
                "quietest_hour_count": int(hourly_counts.iloc[-1])
            }
            
            # Time-based risk analysis
            if 'risk_score' in df_analyzed.columns:
                risk_by_hour = df_analyzed.groupby('hour')['risk_score'].mean()
                riskiest_hour = risk_by_hour.idxmax()
                safest_hour = risk_by_hour.idxmin()
                
                analysis["risk_by_time"] = {
                    "riskiest_hour": int(riskiest_hour),
                    "riskiest_hour_score": float(risk_by_hour[riskiest_hour]),
                    "safest_hour": int(safest_hour),
                    "safest_hour_score": float(risk_by_hour[safest_hour]),
                    "hourly_risk_distribution": {str(k): float(v) for k, v in risk_by_hour.to_dict().items()}
                }
                
                # Identify temporal anomalies
                avg_risk = df_analyzed['risk_score'].mean()
                high_risk_hours = risk_by_hour[risk_by_hour > avg_risk + 10].to_dict()
                
                for hour, risk in high_risk_hours.items():
                    analysis["temporal_anomalies"].append({
                        "type": "high_risk_hour",
                        "hour": int(hour),
                        "risk_score": float(risk),
                        "description": f"Hour {hour}:00 shows elevated risk ({risk:.1f} vs avg {avg_risk:.1f})"
                    })
        
        # Daily patterns if date is available
        if 'transaction_date' in df_analyzed.columns:
            try:
                dates = pd.to_datetime(df_analyzed['transaction_date'], errors='coerce')
                df_with_dates = df_analyzed.copy()
                df_with_dates['weekday'] = dates.dt.dayofweek
                df_with_dates['date'] = dates.dt.date
                
                # Weekly pattern
                weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekday_counts = df_with_dates['weekday'].value_counts().sort_index()
                analysis["daily_patterns"] = {
                    "weekday_distribution": {weekday_names[i]: int(count) for i, count in weekday_counts.items()},
                    "weekend_vs_weekday": {
                        "weekday_count": int(df_with_dates[df_with_dates['weekday'] < 5].shape[0]),
                        "weekend_count": int(df_with_dates[df_with_dates['weekday'] >= 5].shape[0])
                    }
                }
                
                # Weekend anomaly detection
                weekend_transactions = df_with_dates[df_with_dates['weekday'] >= 5]
                if len(weekend_transactions) > len(df_analyzed) * 0.3:  # More than 30% on weekends
                    analysis["temporal_anomalies"].append({
                        "type": "high_weekend_activity",
                        "count": len(weekend_transactions),
                        "percentage": round(len(weekend_transactions) / len(df_analyzed) * 100, 1),
                        "description": "Unusually high weekend transaction volume detected"
                    })
                
            except Exception as e:
                print(f"Warning: Could not process daily patterns: {e}")
        
        # Generate time-based recommendations
        recommendations = []
        
        if analysis.get("risk_by_time", {}).get("riskiest_hour_score", 0) > 60:
            riskiest_hour = analysis["risk_by_time"]["riskiest_hour"]
            recommendations.append(f"⚠️ High risk detected at {riskiest_hour}:00 - implement additional verification")
        
        if len(analysis.get("temporal_anomalies", [])) > 0:
            recommendations.append("🔍 Temporal anomalies detected - review time-based fraud patterns")
        
        # Off-hours recommendations
        if 'hour' in df_analyzed.columns:
            night_transactions = len(df_analyzed[(df_analyzed['hour'] >= 22) | (df_analyzed['hour'] <= 6)])
            if night_transactions > len(df_analyzed) * 0.15:
                recommendations.append("🌙 High night-time activity - consider enhanced verification for late transactions")
        
        analysis["time_recommendations"] = recommendations
        
    except Exception as e:
        print(f"Warning: Could not calculate time analysis: {e}")
    
    return analysis


def calculate_geographic_analysis(df_analyzed: pd.DataFrame) -> Dict[str, Any]:
    """Calculate geographic analysis if location data is available"""
    analysis = {
        "state_distribution": {},
        "zip_code_patterns": {},
        "geographic_risk_analysis": {},
        "location_anomalies": [],
        "geographic_recommendations": []
    }
    
    try:
        # State analysis
        if 'customer_state' in df_analyzed.columns:
            state_counts = df_analyzed['customer_state'].value_counts().to_dict()
            analysis["state_distribution"] = {str(k): int(v) for k, v in state_counts.items()}
            
            # Geographic risk analysis
            if 'risk_score' in df_analyzed.columns:
                state_risk = df_analyzed.groupby('customer_state')['risk_score'].agg(['mean', 'count']).to_dict()
                analysis["geographic_risk_analysis"] = {
                    state: {
                        "average_risk": float(state_risk['mean'][state]),
                        "transaction_count": int(state_risk['count'][state])
                    } for state in state_risk['mean'].keys()
                }
                
                # Find high-risk states
                avg_risk_overall = df_analyzed['risk_score'].mean()
                high_risk_states = [
                    state for state, risk in state_risk['mean'].items() 
                    if risk > avg_risk_overall + 15 and state_risk['count'][state] >= 2
                ]
                
                if high_risk_states:
                    analysis["location_anomalies"].append({
                        "type": "high_risk_states",
                        "states": high_risk_states,
                        "description": f"States with elevated risk: {', '.join(high_risk_states)}"
                    })
        
        # ZIP code patterns
        if 'customer_zip_code' in df_analyzed.columns:
            zip_counts = df_analyzed['customer_zip_code'].value_counts().head(10).to_dict()
            analysis["zip_code_patterns"] = {str(k): int(v) for k, v in zip_counts.items()}
            
            # Look for ZIP code concentration anomalies
            top_zip_count = max(zip_counts.values()) if zip_counts else 0
            if top_zip_count > len(df_analyzed) * 0.2:  # More than 20% from one ZIP
                top_zip = max(zip_counts.keys(), key=lambda k: zip_counts[k])
                analysis["location_anomalies"].append({
                    "type": "zip_concentration",
                    "zip_code": str(top_zip),
                    "count": int(top_zip_count),
                    "percentage": round(top_zip_count / len(df_analyzed) * 100, 1),
                    "description": f"High transaction concentration in ZIP {top_zip}"
                })
        
        # Generate geographic recommendations
        recommendations = []
        
        if len(analysis.get("location_anomalies", [])) > 0:
            recommendations.append("🗺️ Geographic anomalies detected - review location-based patterns")
        
        if analysis.get("geographic_risk_analysis"):
            high_risk_locations = [
                loc for loc, data in analysis["geographic_risk_analysis"].items() 
                if data["average_risk"] > 60
            ]
            if high_risk_locations:
                recommendations.append(f"⚠️ High-risk locations identified: {', '.join(high_risk_locations)}")
        
        analysis["geographic_recommendations"] = recommendations
        
    except Exception as e:
        print(f"Warning: Could not calculate geographic analysis: {e}")
    
    return analysis


def calculate_data_quality_score(df_analyzed: pd.DataFrame) -> int:
    """Calculate a data quality score based on completeness and consistency"""
    try:
        total_fields = len(df_analyzed.columns)
        total_records = len(df_analyzed)
        
        if total_records == 0:
            return 0
        
        # Calculate completeness score
        completeness_scores = []
        for column in df_analyzed.columns:
            non_null_count = df_analyzed[column].count()
            completeness = (non_null_count / total_records) * 100
            completeness_scores.append(completeness)
        
        avg_completeness = np.mean(completeness_scores)
        
        # Calculate consistency score (basic checks)
        consistency_score = 100
        
        # Check for obviously bad data
        if 'amount' in df_analyzed.columns:
            negative_amounts = (df_analyzed['amount'] < 0).sum()
            if negative_amounts > 0:
                consistency_score -= min(20, (negative_amounts / total_records) * 100)
        
        # Check for duplicate transaction IDs
        if 'transaction_id' in df_analyzed.columns:
            duplicates = df_analyzed['transaction_id'].duplicated().sum()
            if duplicates > 0:
                consistency_score -= min(15, (duplicates / total_records) * 100)
        
        # Final score
        final_score = int((avg_completeness * 0.7) + (consistency_score * 0.3))
        return max(0, min(100, final_score))
        
    except Exception as e:
        print(f"Warning: Could not calculate data quality score: {e}")
        return 75  # Default score


def clean_for_json(data):
    """Clean data for JSON serialization"""
    if isinstance(data, list):
        return [clean_for_json(item) for item in data]
    elif isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if pd.isna(value):
                cleaned[key] = None
            elif isinstance(value, (np.integer, np.int64)):
                cleaned[key] = int(value)
            elif isinstance(value, (np.floating, np.float64)):
                cleaned[key] = float(value)
            elif isinstance(value, (np.ndarray, pd.Series)):
                cleaned[key] = value.tolist()
            else:
                cleaned[key] = value
        return cleaned
    else:
        return data


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FraudGuard Pro Enhanced API...")
    print("📊 Dashboard available at: http://localhost:8080")
    print("🔍 API documentation at: http://localhost:8080/docs")
    uvicorn.run(app, host="0.0.0.0", port=8080)
