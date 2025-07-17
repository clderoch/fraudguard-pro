#!/usr/bin/env python3
"""
Generate Realistic Credit Card Transaction Data for Small Merchants
Creates proper merchant data with NO fraud indicators in raw data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate_clean_merchant_data import generate_clean_merchant_transactions, generate_mixed_transactions_with_fraud_simulation
import pandas as pd

def generate_sample_datasets(num_transactions=1000, merchant_type='Local Retail Store', fraud_rate=0.15):
    """Generate sample datasets - clean merchant data and fraud detection results"""
    
    print("🚀 Generating Realistic Credit Card Transaction Datasets")
    print("=" * 60)
    
    # Create transaction_files directory if it doesn't exist
    output_dir = 'transaction_files'
    os.makedirs(output_dir, exist_ok=True)
    
    # Dataset 1: Clean transactions (what merchants actually have)
    print("\n📊 Generating clean_credit_card_transactions...")
    print("   📝 Description: Raw merchant data with NO fraud indicators")
    print("   🏪 Merchant Type: Local Retail Store")
    print("   📈 Size: 1000 transactions")
    print("   🚫 Fraud indicators: NONE (merchant raw data)")
    
    clean_df = generate_clean_merchant_transactions(num_transactions, merchant_type)
    # Add upload compatibility columns
    if 'date' in clean_df.columns:
        clean_df['transaction_date'] = clean_df['date']
    if 'time' in clean_df.columns:
        clean_df['transaction_time'] = clean_df['time']
    # Validate required columns
    required_cols = ['transaction_date', 'transaction_time']
    missing = [col for col in required_cols if col not in clean_df.columns]
    if missing:
        print(f"⚠️ Warning: Missing columns in clean data: {missing}")
    clean_filename = os.path.join(output_dir, "clean_credit_card_transactions_new.csv")
    clean_df.to_csv(clean_filename, index=False)
    print(f"   ✅ Generated {len(clean_df)} transactions")
    print(f"   👥 Unique customers: {clean_df['customer_id'].nunique()}")
    print(f"   💳 Card transactions: {(clean_df['payment_method'].isin(['credit_card', 'debit_card'])).sum()}")
    print(f"   💰 Average amount: ${clean_df['amount'].mean():.2f}")
    print(f"   ✅ Clean dataset: 0 fraud columns (as expected)")
    print(f"   💾 Saved: {clean_filename}")
    print(f"   📋 Columns: {list(clean_df.columns)}")
    print(f"   📦 File size: {os.path.getsize(clean_filename)//1024} KB")
    
    # Dataset 2: Mixed transactions with fraud detection results
    print("\n📊 Generating mixed_credit_card_transactions...")
    print("   📝 Description: Results AFTER FraudGuard Pro processes the data")
    print("   🏪 Merchant Type: Local Retail Store")
    print("   📈 Size: 1000 transactions")
    print("   ⚠️ Fraud Rate: 15.0%")
    
    mixed_df = generate_mixed_transactions_with_fraud_simulation(num_transactions, fraud_rate)
    # Add upload compatibility columns
    if 'date' in mixed_df.columns:
        mixed_df['transaction_date'] = mixed_df['date']
    if 'time' in mixed_df.columns:
        mixed_df['transaction_time'] = mixed_df['time']
    # Validate required columns
    missing = [col for col in required_cols if col not in mixed_df.columns]
    if missing:
        print(f"⚠️ Warning: Missing columns in mixed data: {missing}")
    mixed_filename = os.path.join(output_dir, "mixed_credit_card_transactions_new.csv")
    mixed_df.to_csv(mixed_filename, index=False)
    fraud_count = mixed_df['is_fraud'].sum()
    print(f"   ✅ Generated {len(mixed_df)} transactions")
    print(f"   👥 Unique customers: {mixed_df['customer_id'].nunique()}")
    print(f"   💳 Card transactions: {(mixed_df['payment_method'].isin(['credit_card', 'debit_card'])).sum()}")
    print(f"   💰 Average amount: ${mixed_df['amount'].mean():.2f}")
    print(f"   🚨 Fraudulent transactions: {fraud_count} ({fraud_count/len(mixed_df):.1%})")
    print(f"   💾 Saved: {mixed_filename}")
    print(f"   📋 Columns: {list(mixed_df.columns)}")
    print(f"   📦 File size: {os.path.getsize(mixed_filename)//1024} KB")
    
    print(f"\n🎉 Sample datasets generated successfully!")
    print(f"📁 All files saved to: {output_dir}/")
    print(f"")
    print(f"💡 Files:")
    print(f"   • clean_credit_card_transactions_new.csv - Upload to test fraud detection")
    print(f"   • mixed_credit_card_transactions_new.csv - View fraud detection results")
    print(f"")
    print(f"🔍 Key Points:")
    print(f"   • Clean file has NO fraud indicators (realistic merchant data)")
    print(f"   • Mixed file shows what dashboard displays AFTER processing")
    print(f"   • Merchants only get fraud detection through FraudGuard Pro")
    
    return [
        {"name": "clean_credit_card_transactions", "type": "merchant_raw_data", "file": clean_filename},
        {"name": "mixed_credit_card_transactions", "type": "fraud_detection_results", "file": mixed_filename}
    ]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate realistic credit card transaction datasets for small merchants.")
    parser.add_argument('--num', type=int, default=1000, help='Number of transactions per dataset (default: 1000)')
    parser.add_argument('--merchant', type=str, default='Local Retail Store', help='Merchant type/name (default: Local Retail Store)')
    parser.add_argument('--fraud_rate', type=float, default=0.15, help='Fraud rate for mixed dataset (default: 0.15)')
    args = parser.parse_args()
    generate_sample_datasets(num_transactions=args.num, merchant_type=args.merchant, fraud_rate=args.fraud_rate)
