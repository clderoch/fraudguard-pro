#!/usr/bin/env python3
"""
Demo script for Universal Transaction Generator
Demonstrates how to generate realistic transaction data for any industry
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_transaction_generator import generate_business_data, UniversalTransactionGenerator
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def demo_single_business_type():
    """Demo: Generate data for a single business type"""
    print("🔬 Demo 1: Single Business Type Generation")
    print("-" * 50)
    
    # Generate SaaS B2B data
    print("Generating SaaS B2B transaction data...")
    df = generate_business_data('saas_b2b', num_transactions=1000, region='US')
    
    print(f"✅ Generated {len(df)} transactions")
    print(f"📊 Sample data preview:")
    print(df[['transaction_id', 'customer_name', 'amount', 'subscription_tier', 
              'payment_status', 'risk_score']].head())
    
    # Save sample
    df.to_csv('demo_saas_transactions.csv', index=False)
    print(f"💾 Saved to: demo_saas_transactions.csv")
    
    return df

def demo_multiple_industries():
    """Demo: Generate data for multiple industries"""
    print("\n🏭 Demo 2: Multiple Industry Generation")
    print("-" * 50)
    
    # Select diverse business types
    business_types = [
        'saas_b2b',           # Technology
        'fashion_ecommerce',   # Retail
        'telehealth_platform', # Healthcare
        'fintech_payment_app', # Finance
        'food_delivery',       # Food Service
        'travel_booking'       # Travel
    ]
    
    all_data = []
    
    for business_type in business_types:
        print(f"Generating {business_type} data...")
        df = generate_business_data(business_type, num_transactions=500, region='US')
        df['business_type'] = business_type
        all_data.append(df)
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print(f"✅ Generated {len(combined_df)} total transactions across {len(business_types)} industries")
    
    # Industry comparison
    industry_summary = combined_df.groupby('business_type').agg({
        'amount': ['mean', 'sum', 'count'],
        'is_fraudulent': 'mean',
        'customer_id': 'nunique'
    }).round(2)
    
    print(f"📈 Industry Comparison:")
    print(industry_summary)
    
    # Save combined data
    combined_df.to_csv('demo_multi_industry_transactions.csv', index=False)
    print(f"💾 Saved to: demo_multi_industry_transactions.csv")
    
    return combined_df

def demo_fraud_analysis():
    """Demo: Fraud pattern analysis"""
    print("\n🚨 Demo 3: Fraud Pattern Analysis")
    print("-" * 50)
    
    # Generate data with focus on fraud detection
    df = generate_business_data('crypto_exchange', num_transactions=2000, region='US')
    
    # Fraud analysis
    fraud_rate = df['is_fraudulent'].mean() * 100
    print(f"Overall fraud rate: {fraud_rate:.2f}%")
    
    # Risk score distribution
    risk_by_fraud = df.groupby('is_fraudulent')['risk_score'].describe()
    print(f"\nRisk score by fraud status:")
    print(risk_by_fraud)
    
    # Common fraud indicators
    fraud_transactions = df[df['is_fraudulent'] == True]
    if len(fraud_transactions) > 0:
        print(f"\nCommon fraud indicators:")
        all_indicators = []
        for indicators in fraud_transactions['fraud_indicators'].dropna():
            if indicators:
                all_indicators.extend(indicators.split(','))
        
        from collections import Counter
        indicator_counts = Counter(all_indicators)
        for indicator, count in indicator_counts.most_common(5):
            print(f"  - {indicator}: {count} occurrences")
    
    return df

def demo_international_data():
    """Demo: International/multi-region data"""
    print("\n🌍 Demo 4: International Data Generation")
    print("-" * 50)
    
    regions = ['US', 'CA', 'GB', 'DE', 'JP']
    international_data = []
    
    for region in regions:
        print(f"Generating data for {region}...")
        df = generate_business_data('streaming_service', num_transactions=300, region=region)
        df['region'] = region
        international_data.append(df)
    
    # Combine international data
    international_df = pd.concat(international_data, ignore_index=True)
    
    print(f"✅ Generated {len(international_df)} international transactions")
    
    # Regional analysis
    regional_summary = international_df.groupby('region').agg({
        'amount': 'mean',
        'customer_id': 'nunique',
        'language': lambda x: x.mode().iloc[0] if not x.empty else 'unknown'
    }).round(2)
    
    print(f"🌎 Regional Summary:")
    print(regional_summary)
    
    # Save international data
    international_df.to_csv('demo_international_transactions.csv', index=False)
    print(f"💾 Saved to: demo_international_transactions.csv")
    
    return international_df

def demo_custom_business_type():
    """Demo: Custom business type with dynamic pattern generation"""
    print("\n🎨 Demo 5: Custom Business Type")
    print("-" * 50)
    
    # The generator can handle unknown business types by creating dynamic patterns
    custom_business_types = [
        'ai_chatbot_service',
        'drone_delivery_startup', 
        'virtual_reality_arcade',
        'sustainable_fashion_brand'
    ]
    
    for business_type in custom_business_types:
        print(f"Generating data for custom business: {business_type}")
        df = generate_business_data(business_type, num_transactions=200, region='US')
        
        print(f"  ✅ Generated {len(df)} transactions")
        print(f"  💰 Avg transaction: ${df['amount'].mean():.2f}")
        print(f"  👥 Unique customers: {df['customer_id'].nunique()}")
        
        # Save each custom type
        filename = f"demo_{business_type}_transactions.csv"
        df.to_csv(filename, index=False)
        print(f"  💾 Saved to: {filename}")

def main():
    """Run all demonstrations"""
    print("🚀 Universal Transaction Generator - Comprehensive Demo")
    print("=" * 70)
    print("This demo shows how to generate realistic transaction data")
    print("for any business type across all major industries.")
    print("=" * 70)
    
    try:
        # Run all demos
        demo_single_business_type()
        demo_multiple_industries() 
        demo_fraud_analysis()
        demo_international_data()
        demo_custom_business_type()
        
        print("\n" + "=" * 70)
        print("🎉 All demos completed successfully!")
        print("📁 Check the generated CSV files for transaction data")
        print("💡 Use this data to test your fraud detection dashboard")
        print("=" * 70)
        
        # Show available business types
        generator = UniversalTransactionGenerator()
        patterns = generator.get_comprehensive_business_patterns()
        
        print(f"\n📋 Available Business Types ({len(patterns)} total):")
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
        
        print(f"\n💻 Usage Examples:")
        print(f"   from universal_transaction_generator import generate_business_data")
        print(f"   df = generate_business_data('your_business_type', 5000, 'US')")
        print(f"   df.to_csv('your_data.csv', index=False)")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
