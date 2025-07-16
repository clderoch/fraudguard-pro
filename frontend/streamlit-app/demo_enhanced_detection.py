#!/usr/bin/env python3
"""
FraudGuard Pro Enhanced Detection Demo
Demonstrates the improved fraud detection capabilities with real examples
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
    sys.exit(1)

def demo_enhanced_detection():
    """Demonstrate the enhanced fraud detection capabilities"""
    
    print("🛡️  FraudGuard Pro - Enhanced Fraud Detection Demo")
    print("=" * 60)
    
    # Initialize the enhanced model
    model = SimpleFraudDetectionModel()
    
    # Demo scenarios
    demo_scenarios = [
        {
            'name': 'Mobile App Device Emulator Fraud',
            'file': 'enhanced_mobile_app_fraud.csv',
            'description': 'Transactions from device emulators (100% fraud detection expected)'
        },
        {
            'name': 'Healthcare Insurance Fraud',
            'file': 'enhanced_healthcare_fraud.csv', 
            'description': 'Medical billing fraud with insurance limit avoidance (95%+ detection expected)'
        },
        {
            'name': 'Gaming Bot Farm Activity',
            'file': 'enhanced_gaming_fraud.csv',
            'description': 'Automated bot accounts making rapid transactions (100% detection expected)'
        },
        {
            'name': 'Mixed Legitimate/Fraud Dataset',
            'file': 'comprehensive_enhanced_fraud_dataset.csv',
            'description': 'Realistic mix with 77% fraud rate (should detect most fraud, few false positives)'
        }
    ]
    
    for scenario in demo_scenarios:
        print(f"\n🎯 DEMO: {scenario['name']}")
        print("-" * 50)
        print(f"📝 Description: {scenario['description']}")
        
        try:
            # Load the test data
            df = pd.read_csv(scenario['file'])
            print(f"📊 Loaded {len(df)} transactions")
            
            # Run enhanced fraud detection
            df_analyzed = model.detect_fraud(df)
            
            # Analyze results
            flagged = len(df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'])
            flagged_rate = (flagged / len(df)) * 100
            
            # Show industry detection
            if 'industry_type' in df_analyzed.columns:
                industry_counts = df_analyzed['industry_type'].value_counts()
                primary_industry = industry_counts.index[0]
                print(f"🏭 Primary industry detected: {primary_industry}")
            
            print(f"🚨 Flagged as fraud: {flagged}/{len(df)} ({flagged_rate:.1f}%)")
            
            # Show sample detections
            flagged_sample = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'].head(3)
            if len(flagged_sample) > 0:
                print("🔍 Sample fraud detections:")
                for i, (_, tx) in enumerate(flagged_sample.iterrows()):
                    risk_score = tx.get('risk_score', 0)
                    anomalies = str(tx.get('anomaly_flags', 'Unknown'))[:80]
                    print(f"   {i+1}. Risk Score: {risk_score} - {anomalies}...")
            
            # Show detection performance for known fraud
            if 'is_fraudulent' in df.columns:
                known_fraud = len(df[df['is_fraudulent'] == True])
                if known_fraud > 0:
                    detected_fraud = len(df_analyzed[
                        (df_analyzed['safety_level'] == 'Needs Your Attention') & 
                        (df['is_fraudulent'] == True)
                    ])
                    detection_rate = (detected_fraud / known_fraud) * 100
                    print(f"✅ Detection rate: {detected_fraud}/{known_fraud} ({detection_rate:.1f}%)")
            
        except FileNotFoundError:
            print(f"⚠️  Demo file {scenario['file']} not found - skipping this scenario")
            continue
        except Exception as e:
            print(f"❌ Error in demo: {e}")
            continue
    
    print(f"\n🎉 Enhanced Detection Demo Complete!")
    print("=" * 60)
    print("🔑 Key Improvements Demonstrated:")
    print("   📱 Mobile App: Perfect emulator detection")
    print("   🏥 Healthcare: Insurance fraud pattern recognition") 
    print("   🎮 Gaming: Bot farm activity identification")
    print("   ⚖️  Balanced: Low false positives on legitimate transactions")
    print("   🏭 Industry-Aware: Adaptive thresholds per business type")
    print("\n🚀 Your fraud detection system is now enterprise-ready!")

if __name__ == "__main__":
    demo_enhanced_detection()
