#!/usr/bin/env python3
"""
Test script to verify anomaly detection is working with generated test data
"""

import pandas as pd
import sys
import os

# Add the current directory to Python path to import the Streamlit app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import SimpleFraudDetectionModel

def test_anomaly_detection():
    """Test the anomaly detection with our generated test data"""
    
    print("🔍 Testing Anomaly Detection with Generated Data")
    print("=" * 60)
    
    # Initialize the fraud detection model
    model = SimpleFraudDetectionModel()
    
    # Test files - organized by category
    test_files = [
        # Original business data
        ('test_data_saas.csv', 'SaaS B2B'),
        ('test_data_gaming.csv', 'Gaming Platform'),
        ('test_data_food_delivery.csv', 'Food Delivery'),
        
        # Pure fraud pattern files
        ('high_fraud_patterns.csv', 'High Fraud Patterns'),
        ('ecommerce_fraud_patterns.csv', 'E-commerce Fraud'),
        ('financial_fraud_patterns.csv', 'Financial Fraud'),
        ('subscription_fraud_patterns.csv', 'Subscription Fraud'),
        ('mobile_app_fraud.csv', 'Mobile App Fraud'),
        ('travel_fraud.csv', 'Travel Fraud'),
        ('healthcare_fraud.csv', 'Healthcare Fraud'),
        ('charity_fraud.csv', 'Charity Fraud'),
        ('education_fraud.csv', 'Education Fraud'),
        
        # Mixed datasets (realistic scenarios)
        ('mixed_ecommerce_dataset.csv', 'Mixed E-commerce'),
        ('mixed_financial_dataset.csv', 'Mixed Financial'),
        ('mixed_subscription_dataset.csv', 'Mixed Subscription')
    ]
    
    results_summary = []
    
    for filename, business_type in test_files:
        if not os.path.exists(filename):
            print(f"❌ {filename} not found")
            continue
            
        print(f"\n📊 Testing {business_type} ({filename})")
        print("-" * 40)
        
        # Load data
        try:
            df = pd.read_csv(filename)
            print(f"✓ Loaded {len(df):,} transactions")
            
            # Run fraud detection
            results = model.detect_fraud(df)
            
            # Calculate metrics
            total_transactions = len(df)
            flagged_transactions = len(results[results['safety_level'] == 'Needs Your Attention'])
            flagged_percentage = flagged_transactions / total_transactions * 100
            
            # Check if we have known fraud indicators
            known_fraud = 0
            if 'is_fraudulent' in df.columns:
                known_fraud = len(df[df['is_fraudulent'] == True])
            
            # Look for specific anomaly transaction IDs
            anomaly_patterns = ['GEO_ANOM', 'VEL_ANOM', 'PAY_ANOM', 'BEH_ANOM', 'TEMP_ANOM', 'QUAL_ANOM',
                              'CARD_TEST', 'GEO_HOP', 'VEL_ATTACK', 'NIGHT_FRAUD', 'FAKE_DATA',
                              'TAKEOVER', 'RESHIP', 'STRUCT', 'PUMP', 'TRIAL_ABUSE', 'STACK',
                              'IAP_FRAUD', 'TRAVEL_FRAUD', 'FRAUD_MED', 'CHARITY_FRAUD', 'EDU_FRAUD']
            
            test_anomalies = df[df['transaction_id'].str.contains('|'.join(anomaly_patterns), na=False)]
            test_anomaly_count = len(test_anomalies)
            
            if test_anomaly_count > 0:
                test_results = results[results['transaction_id'].isin(test_anomalies['transaction_id'])]
                flagged_test_count = len(test_results[test_results['safety_level'] == 'Needs Your Attention'])
                test_detection_rate = flagged_test_count / test_anomaly_count * 100
                print(f"🎯 Test anomalies detected: {flagged_test_count}/{test_anomaly_count} ({test_detection_rate:.1f}%)")
            else:
                test_detection_rate = 0
                print(f"📝 No specific test anomalies found")
            
            print(f"🚨 Total flagged as fraud: {flagged_transactions:,} transactions ({flagged_percentage:.1f}%)")
            if known_fraud > 0:
                print(f"📋 Known fraudulent transactions: {known_fraud}")
            
            # Store results for summary
            results_summary.append({
                'dataset': business_type,
                'total': total_transactions,
                'flagged': flagged_transactions,
                'flagged_pct': flagged_percentage,
                'known_fraud': known_fraud,
                'test_anomalies': test_anomaly_count,
                'test_detection_rate': test_detection_rate
            })
            
            # Show some examples of flagged transactions
            flagged_sample = results[results['safety_level'] == 'Needs Your Attention'].head(3)
            if len(flagged_sample) > 0:
                print(f"\n🔍 Sample flagged transactions:")
                for _, row in flagged_sample.iterrows():
                    risk_score = row.get('risk_score', 0)
                    anomaly_flags = row.get('anomaly_flags', 'None')
                    print(f"  • {row['transaction_id']}: Risk Score {risk_score:.1f}")
                    if anomaly_flags and anomaly_flags != 'None detected':
                        print(f"    Anomalies: {anomaly_flags[:100]}...")
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")
            results_summary.append({
                'dataset': business_type,
                'total': 0,
                'flagged': 0,
                'flagged_pct': 0,
                'known_fraud': 0,
                'test_anomalies': 0,
                'test_detection_rate': 0
            })
    
    # Print summary
    print(f"\n" + "=" * 80)
    print("📊 COMPREHENSIVE ANOMALY DETECTION SUMMARY")
    print("=" * 80)
    
    total_files = len([r for r in results_summary if r['total'] > 0])
    total_transactions = sum([r['total'] for r in results_summary])
    total_flagged = sum([r['flagged'] for r in results_summary])
    total_known_fraud = sum([r['known_fraud'] for r in results_summary])
    
    print(f"📁 Files processed: {total_files}")
    print(f"💳 Total transactions: {total_transactions:,}")
    print(f"🚨 Total flagged: {total_flagged:,} ({total_flagged/total_transactions*100:.1f}%)")
    print(f"🎯 Known fraudulent: {total_known_fraud:,}")
    
    print(f"\n📋 Detection Performance by Dataset:")
    print(f"{'Dataset':<25} {'Total':<8} {'Flagged':<8} {'Rate':<8} {'Test Det.':<10}")
    print("-" * 70)
    
    for result in results_summary:
        if result['total'] > 0:
            print(f"{result['dataset']:<25} {result['total']:<8} {result['flagged']:<8} {result['flagged_pct']:<7.1f}% {result['test_detection_rate']:<9.1f}%")
    
    print(f"\n✅ Anomaly detection testing complete!")
    print(f"🎯 System successfully tested across {total_files} different fraud scenarios!")

if __name__ == "__main__":
    test_anomaly_detection()
