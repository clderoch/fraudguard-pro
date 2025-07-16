#!/usr/bin/env python3
"""
Enhanced Anomaly Detection Performance Test
Tests the improved fraud detection system across all datasets including new enhanced tests
"""

import pandas as pd
import sys
import os
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import SimpleFraudDetectionModel
except ImportError:
    print("Error: Could not import SimpleFraudDetectionModel from app.py")
    print("Make sure you're running this script from the correct directory.")
    sys.exit(1)

def test_enhanced_fraud_detection():
    """Test the enhanced fraud detection system"""
    print("🔍 Testing Enhanced Anomaly Detection System")
    print("=" * 80)
    
    # Initialize the enhanced fraud detection model
    model = SimpleFraudDetectionModel()
    
    # List of all test files including new enhanced ones
    test_files = [
        # Original test files
        ('SaaS B2B', 'test_data_saas.csv'),
        ('Gaming Platform', 'test_data_gaming.csv'),
        ('Food Delivery', 'test_data_food_delivery.csv'),
        ('High Fraud Patterns', 'high_fraud_patterns.csv'),
        ('E-commerce Fraud', 'ecommerce_fraud_patterns.csv'),
        ('Financial Fraud', 'financial_fraud_patterns.csv'),
        ('Subscription Fraud', 'subscription_fraud_patterns.csv'),
        ('Mobile App Fraud', 'mobile_app_fraud.csv'),
        ('Travel Fraud', 'travel_fraud.csv'),
        ('Healthcare Fraud', 'healthcare_fraud.csv'),
        ('Charity Fraud', 'charity_fraud.csv'),
        ('Education Fraud', 'education_fraud.csv'),
        ('Mixed E-commerce', 'mixed_ecommerce_dataset.csv'),
        ('Mixed Financial', 'mixed_financial_dataset.csv'),
        ('Mixed Subscription', 'mixed_subscription_dataset.csv'),
        
        # New enhanced test files
        ('Enhanced Mobile App', 'enhanced_mobile_app_fraud.csv'),
        ('Enhanced Healthcare', 'enhanced_healthcare_fraud.csv'),
        ('Enhanced Gaming', 'enhanced_gaming_fraud.csv'),
        ('Comprehensive Enhanced', 'comprehensive_enhanced_fraud_dataset.csv')
    ]
    
    results = []
    total_transactions = 0
    total_flagged = 0
    total_known_fraud = 0
    total_detected = 0
    
    for dataset_name, filename in test_files:
        try:
            print(f"📊 Testing {dataset_name} ({filename})")
            print("-" * 60)
            
            # Load the dataset
            df = pd.read_csv(filename)
            
            if len(df) == 0:
                print(f"⚠️  Warning: {filename} is empty")
                continue
            
            print(f"✓ Loaded {len(df)} transactions")
            
            # Run fraud detection
            df_analyzed = model.detect_fraud(df)
            
            # Count flagged transactions
            flagged_transactions = len(df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'])
            flagged_rate = (flagged_transactions / len(df)) * 100
            
            # Count known fraudulent transactions
            if 'is_fraudulent' in df.columns:
                known_fraudulent = len(df[df['is_fraudulent'] == True])
                
                # Calculate detection rate for known fraud
                if known_fraudulent > 0:
                    fraud_detected = len(df_analyzed[
                        (df_analyzed['safety_level'] == 'Needs Your Attention') & 
                        (df['is_fraudulent'] == True)
                    ])
                    detection_rate = (fraud_detected / known_fraudulent) * 100
                else:
                    fraud_detected = 0
                    detection_rate = 0
            else:
                # For datasets without fraud labels, look for specific test anomaly patterns
                test_anomaly_patterns = [
                    'GEO_ANOM', 'VEL_ANOM', 'PAY_ANOM', 'BEH_ANOM', 'TEMPORAL_ANOM',
                    'CARD_TEST', 'STRUCT', 'TRIAL_ABUSE', 'TRAVEL_FRAUD', 
                    'CHARITY_FRAUD', 'EDU_FRAUD', 'MOBILE_EMULATOR', 'INSURANCE_FRAUD'
                ]
                
                known_fraudulent = 0
                fraud_detected = 0
                
                for pattern in test_anomaly_patterns:
                    pattern_transactions = df[df['transaction_id'].str.contains(pattern, na=False)]
                    known_fraudulent += len(pattern_transactions)
                    
                    # Check how many of these were flagged
                    pattern_flagged = len(df_analyzed[
                        (df_analyzed['transaction_id'].str.contains(pattern, na=False)) &
                        (df_analyzed['safety_level'] == 'Needs Your Attention')
                    ])
                    fraud_detected += pattern_flagged
                
                detection_rate = (fraud_detected / known_fraudulent * 100) if known_fraudulent > 0 else 0
            
            # Industry type analysis
            if 'industry_type' in df_analyzed.columns:
                industry_breakdown = df_analyzed['industry_type'].value_counts()
                primary_industry = industry_breakdown.index[0] if len(industry_breakdown) > 0 else 'general'
            else:
                primary_industry = 'general'
            
            print(f"🎯 Test anomalies detected: {fraud_detected}/{known_fraudulent} ({detection_rate:.1f}%)")
            print(f"🚨 Total flagged as fraud: {flagged_transactions} transactions ({flagged_rate:.1f}%)")
            print(f"📋 Known fraudulent transactions: {known_fraudulent}")
            print(f"🏭 Primary industry type: {primary_industry}")
            
            # Show sample flagged transactions
            flagged_sample = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'].head(3)
            if len(flagged_sample) > 0:
                print("🔍 Sample flagged transactions:")
                for _, tx in flagged_sample.iterrows():
                    anomalies = str(tx.get('anomaly_flags', 'Unknown'))[:100]
                    print(f"  • {tx.get('transaction_id', 'Unknown')}: Risk Score {tx.get('risk_score', 0)}")
                    print(f"    Anomalies: {anomalies}...")
            
            # Store results
            results.append({
                'Dataset': dataset_name,
                'Total': len(df),
                'Flagged': flagged_transactions,
                'Rate': flagged_rate,
                'Known Fraud': known_fraudulent,
                'Detected': fraud_detected,
                'Detection Rate': detection_rate,
                'Primary Industry': primary_industry
            })
            
            # Update totals
            total_transactions += len(df)
            total_flagged += flagged_transactions
            total_known_fraud += known_fraudulent
            total_detected += fraud_detected
            
        except FileNotFoundError:
            print(f"⚠️  Warning: {filename} not found, skipping...")
            continue
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            continue
        
        print()
    
    # Print comprehensive summary
    print("=" * 100)
    print("📊 ENHANCED ANOMALY DETECTION PERFORMANCE SUMMARY")
    print("=" * 100)
    
    print(f"📁 Files processed: {len(results)}")
    print(f"💳 Total transactions: {total_transactions:,}")
    print(f"🚨 Total flagged: {total_flagged:,} ({total_flagged/total_transactions*100:.1f}%)")
    print(f"🎯 Known fraudulent: {total_known_fraud:,}")
    print(f"✅ Successfully detected: {total_detected:,}")
    
    overall_detection_rate = (total_detected / total_known_fraud * 100) if total_known_fraud > 0 else 0
    print(f"🏆 Overall detection rate: {overall_detection_rate:.1f}%")
    
    print(f"\n📋 Detection Performance by Dataset:")
    print("Dataset".ljust(25) + "Total".ljust(8) + "Flagged".ljust(9) + "Rate".ljust(8) + "Industry".ljust(15) + "Test Det.")
    print("-" * 85)
    
    for result in results:
        dataset_name = result['Dataset'][:24]
        total = str(result['Total'])
        flagged = str(result['Flagged'])
        rate = f"{result['Rate']:.1f}%"
        industry = result['Primary Industry'][:14]
        detection = f"{result['Detection Rate']:.1f}%"
        
        print(f"{dataset_name.ljust(25)}{total.ljust(8)}{flagged.ljust(9)}{rate.ljust(8)}{industry.ljust(15)}{detection}")
    
    # Performance improvements analysis
    print(f"\n🚀 PERFORMANCE IMPROVEMENTS:")
    
    # Find mobile app and healthcare results
    mobile_results = [r for r in results if 'mobile' in r['Dataset'].lower()]
    healthcare_results = [r for r in results if 'healthcare' in r['Dataset'].lower()]
    
    if mobile_results:
        enhanced_mobile = [r for r in mobile_results if 'enhanced' in r['Dataset'].lower()]
        original_mobile = [r for r in mobile_results if 'enhanced' not in r['Dataset'].lower()]
        
        if enhanced_mobile and original_mobile:
            enhanced_rate = enhanced_mobile[0]['Detection Rate']
            original_rate = original_mobile[0]['Detection Rate']
            improvement = enhanced_rate - original_rate
            print(f"📱 Mobile App Detection: {original_rate:.1f}% → {enhanced_rate:.1f}% (+{improvement:.1f}% improvement)")
    
    if healthcare_results:
        enhanced_health = [r for r in healthcare_results if 'enhanced' in r['Dataset'].lower()]
        original_health = [r for r in healthcare_results if 'enhanced' not in r['Dataset'].lower()]
        
        if enhanced_health and original_health:
            enhanced_rate = enhanced_health[0]['Detection Rate']
            original_rate = original_health[0]['Detection Rate']
            improvement = enhanced_rate - original_rate
            print(f"🏥 Healthcare Detection: {original_rate:.1f}% → {enhanced_rate:.1f}% (+{improvement:.1f}% improvement)")
    
    # Industry-specific insights
    print(f"\n🏭 INDUSTRY-SPECIFIC INSIGHTS:")
    industry_performance = {}
    for result in results:
        industry = result['Primary Industry']
        if industry not in industry_performance:
            industry_performance[industry] = {'datasets': 0, 'avg_detection': 0, 'total_detection': 0}
        industry_performance[industry]['datasets'] += 1
        industry_performance[industry]['total_detection'] += result['Detection Rate']
    
    for industry, stats in industry_performance.items():
        avg_detection = stats['total_detection'] / stats['datasets']
        print(f"   {industry.title()}: {avg_detection:.1f}% average detection rate ({stats['datasets']} datasets)")
    
    print(f"\n✅ Enhanced anomaly detection testing complete!")
    print(f"🎯 System successfully tested across {len(results)} different fraud scenarios!")
    
    return results

if __name__ == "__main__":
    test_enhanced_fraud_detection()
