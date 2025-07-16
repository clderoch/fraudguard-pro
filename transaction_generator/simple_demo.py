#!/usr/bin/env python3
"""
Simple demo for Universal Transaction Generator
Demonstrates core functionality with working business types
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_transaction_generator import generate_business_data, UniversalTransactionGenerator
import pandas as pd

def simple_demo():
    """Simple demonstration of the transaction generator"""
    print("🚀 Universal Transaction Generator - Simple Demo")
    print("=" * 60)
    
    # Test working business types
    business_types = [
        'saas_b2b',
        'fashion_ecommerce', 
        'telehealth_platform',
        'crypto_exchange',
        'streaming_service'
    ]
    
    for business_type in business_types:
        print(f"\n📊 Generating {business_type} data...")
        
        try:
            # Generate smaller dataset for demo
            df = generate_business_data(business_type, num_transactions=1000, region='US')
            
            print(f"  ✅ Success! Generated {len(df)} transactions")
            print(f"  💰 Average amount: ${df['amount'].mean():.2f}")
            print(f"  🚨 Fraud rate: {df['is_fraudulent'].mean()*100:.1f}%")
            print(f"  👥 Unique customers: {df['customer_id'].nunique()}")
            
            # Save to CSV
            filename = f"simple_demo_{business_type}.csv"
            df.to_csv(filename, index=False)
            print(f"  💾 Saved: {filename}")
            
            # Show sample data
            print(f"  📋 Sample transactions:")
            sample_cols = ['transaction_id', 'customer_name', 'amount', 'payment_status', 'risk_score']
            print(df[sample_cols].head(3).to_string(index=False))
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            continue
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"📁 Check generated CSV files for transaction data")

def show_business_types():
    """Show all available business types"""
    print(f"\n📋 Available Business Types:")
    generator = UniversalTransactionGenerator()
    patterns = generator.get_comprehensive_business_patterns()
    
    industries = {}
    for business_type, pattern in patterns.items():
        industry = pattern.get('industry', 'Other')
        if industry not in industries:
            industries[industry] = []
        industries[industry].append(business_type)
    
    for industry, types in industries.items():
        print(f"\n🏢 {industry}:")
        for business_type in sorted(types):
            print(f"   • {business_type}")

def fraud_analysis_demo():
    """Demonstrate fraud detection capabilities"""
    print(f"\n🚨 Fraud Analysis Demo:")
    print("-" * 40)
    
    # Generate crypto exchange data (higher fraud rates)
    df = generate_business_data('crypto_exchange', num_transactions=2000, region='US')
    
    # Fraud statistics
    total_transactions = len(df)
    fraud_transactions = len(df[df['is_fraudulent'] == True])
    fraud_rate = (fraud_transactions / total_transactions) * 100
    
    print(f"Total transactions: {total_transactions}")
    print(f"Fraudulent transactions: {fraud_transactions}")
    print(f"Fraud rate: {fraud_rate:.2f}%")
    
    # Risk score analysis
    print(f"\nRisk Score Analysis:")
    print(f"Average risk score (all): {df['risk_score'].mean():.1f}")
    print(f"Average risk score (fraud): {df[df['is_fraudulent']]['risk_score'].mean():.1f}")
    print(f"Average risk score (legitimate): {df[~df['is_fraudulent']]['risk_score'].mean():.1f}")
    
    # Save fraud analysis
    df.to_csv('fraud_analysis_demo.csv', index=False)
    print(f"💾 Saved fraud analysis data: fraud_analysis_demo.csv")

def main():
    """Run the simple demo"""
    try:
        simple_demo()
        show_business_types()
        fraud_analysis_demo()
        
        print(f"\n" + "=" * 60)
        print(f"✨ Universal Transaction Generator Demo Complete!")
        print(f"💡 Usage: from universal_transaction_generator import generate_business_data")
        print(f"💡 Example: df = generate_business_data('saas_b2b', 5000, 'US')")
        print(f"=" * 60)
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
