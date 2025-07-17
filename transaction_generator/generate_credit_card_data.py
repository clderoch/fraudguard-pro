#!/usr/bin/env python3
"""
Generate Realistic Credit Card Transaction Data for Small Merchants
Optimized for fraud detection systems with real-world patterns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_transaction_generator import generate_business_data
import pandas as pd

def generate_sample_datasets():
    """Generate sample datasets for testing"""
    
    datasets = [
        {
            'name': 'credit_card_transactions',
            'merchant_type': 'local_retail',
            'size': 1000,
            'description': 'Local retail store credit card transactions'
        },
        {
            'name': 'restaurant_transactions', 
            'merchant_type': 'local_restaurant',
            'size': 800,
            'description': 'Restaurant credit card transactions with tips'
        },
        {
            'name': 'service_transactions',
            'merchant_type': 'service_business', 
            'size': 600,
            'description': 'Service business credit card transactions'
        }
    ]
    
    print("🚀 Generating Realistic Credit Card Transaction Datasets")
    print("=" * 60)
    
    for dataset in datasets:
        print(f"\n📊 Generating {dataset['name']}...")
        print(f"   📝 Description: {dataset['description']}")
        print(f"   🏪 Merchant Type: {dataset['merchant_type']}")
        print(f"   📈 Size: {dataset['size']} transactions")
        
        # Generate data
        df = generate_business_data(
            business_type='local_business',
            num_transactions=dataset['size'],
            region='US',
            merchant_type=dataset['merchant_type']
        )
        
        # Save to current directory
        filename = f"{dataset['name']}.csv"
        df.to_csv(filename, index=False)
        
        # Display statistics
        print(f"   ✅ Generated {len(df)} transactions")
        print(f"   👥 Unique customers: {df['customer_id'].nunique()}")
        print(f"   💳 Card transactions: {(df['payment_method'] == 'card').sum()}")
        print(f"   💰 Average amount: ${df['amount'].mean():.2f}")
        print(f"   🚨 Fraud rate: {df['is_fraud'].mean() * 100:.2f}%")
        print(f"   📁 Saved: {filename}")
    
    print(f"\n🎉 Sample datasets generated successfully!")
    print(f"💡 Use these datasets to test your fraud detection system")
    
    return datasets

if __name__ == "__main__":
    generate_sample_datasets()
