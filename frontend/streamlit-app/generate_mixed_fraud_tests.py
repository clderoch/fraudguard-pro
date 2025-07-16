#!/usr/bin/env python3
"""
Generate mixed datasets with both legitimate and fraudulent transactions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from faker import Faker

fake = Faker('en_US')

def generate_mixed_ecommerce_dataset():
    """Generate mixed e-commerce dataset with 80% legitimate, 20% fraudulent"""
    transactions = []
    base_time = datetime.now() - timedelta(days=7)
    
    # Generate legitimate customers
    legitimate_customers = []
    for i in range(15):
        legitimate_customers.append({
            'customer_id': f'LEGIT_ECOM_{i:03d}',
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': random.choice(['regular', 'vip', 'new']),
            'customer_country': 'US'
        })
    
    # Generate 40 legitimate transactions
    for i in range(40):
        customer = random.choice(legitimate_customers)
        amount = round(random.uniform(25, 500), 2)
        trans_time = base_time + timedelta(hours=random.randint(0, 168))  # Random within week
        
        transactions.append({
            'transaction_id': f'LEGIT_ECOM_{i:04d}',
            'customer_id': customer['customer_id'],
            'customer_name': customer['customer_name'],
            'customer_email': customer['customer_email'],
            'customer_phone': customer['customer_phone'],
            'customer_address': customer['customer_address'],
            'customer_city': customer['customer_city'],
            'customer_state': customer['customer_state'],
            'customer_zip_code': customer['customer_zip_code'],
            'customer_ip_address': customer['customer_ip_address'],
            'customer_segment': customer['customer_segment'],
            'customer_country': customer['customer_country'],
            'transaction_datetime': trans_time,
            'transaction_date': trans_time.strftime('%Y-%m-%d'),
            'transaction_time': trans_time.strftime('%H:%M:%S'),
            'merchant_name': 'Online Fashion Store',
            'merchant_category': 'Retail',
            'amount': amount,
            'payment_method': random.choice(['visa', 'mastercard', 'amex']),
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': fake.random_number(digits=4, fix_len=True),
            'transaction_type': 'purchase',
            'is_fraudulent': False,
            'fraud_indicators': '',
            'risk_score': random.uniform(10, 40),
            'fraud_type': ''
        })
    
    # Generate 10 fraudulent transactions
    fraud_patterns = [
        # Card testing
        {'amount': 1.00, 'pattern': 'card_testing'},
        {'amount': 0.50, 'pattern': 'card_testing'},
        {'amount': 2.00, 'pattern': 'card_testing'},
        # Velocity attack
        {'amount': 799.99, 'pattern': 'velocity'},
        {'amount': 899.99, 'pattern': 'velocity'},
        {'amount': 999.99, 'pattern': 'velocity'},
        # Geographic anomaly
        {'amount': 1299.99, 'pattern': 'geographic'},
        {'amount': 649.99, 'pattern': 'geographic'},
        # High value suspicious
        {'amount': 2499.99, 'pattern': 'high_value'},
        {'amount': 1899.99, 'pattern': 'high_value'}
    ]
    
    for i, fraud_pattern in enumerate(fraud_patterns):
        # Create suspicious customer data
        if fraud_pattern['pattern'] == 'geographic':
            # ZIP/state mismatch
            city, state, zip_code = 'Los Angeles', 'CA', '10001'  # NY ZIP in CA
        else:
            city, state, zip_code = fake.city(), fake.state(), fake.zipcode()
        
        customer_name = 'TEST USER' if fraud_pattern['pattern'] == 'card_testing' else fake.name()
        email = 'temp@10minutemail.com' if fraud_pattern['pattern'] == 'card_testing' else fake.email()
        
        trans_time = base_time + timedelta(hours=random.randint(0, 168))
        if fraud_pattern['pattern'] == 'velocity':
            # Make velocity transactions close together
            trans_time = base_time + timedelta(minutes=i*2)
        
        transactions.append({
            'transaction_id': f'FRAUD_ECOM_{i:04d}',
            'customer_id': f'FRAUD_ECOM_{i:03d}',
            'customer_name': customer_name,
            'customer_email': email,
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': city,
            'customer_state': state,
            'customer_zip_code': zip_code,
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'suspicious',
            'customer_country': 'US',
            'transaction_datetime': trans_time,
            'transaction_date': trans_time.strftime('%Y-%m-%d'),
            'transaction_time': trans_time.strftime('%H:%M:%S'),
            'merchant_name': 'Online Fashion Store',
            'merchant_category': 'Retail',
            'amount': fraud_pattern['amount'],
            'payment_method': random.choice(['visa', 'mastercard']),
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': f"{1111 + i}" if fraud_pattern['pattern'] == 'card_testing' else fake.random_number(digits=4, fix_len=True),
            'transaction_type': 'purchase',
            'is_fraudulent': True,
            'fraud_indicators': fraud_pattern['pattern'],
            'risk_score': random.uniform(70, 95),
            'fraud_type': fraud_pattern['pattern']
        })
    
    return pd.DataFrame(transactions)

def generate_mixed_financial_dataset():
    """Generate mixed financial dataset"""
    transactions = []
    base_time = datetime.now() - timedelta(days=5)
    
    # Legitimate financial transactions
    legit_customers = [
        {
            'customer_id': 'BANK_CUSTOMER_001',
            'customer_name': 'Alice Williams',
            'customer_email': 'alice.williams@email.com',
            'customer_phone': '555-1234',
            'customer_segment': 'premium'
        },
        {
            'customer_id': 'BANK_CUSTOMER_002', 
            'customer_name': 'Bob Anderson',
            'customer_email': 'bob.anderson@email.com',
            'customer_phone': '555-5678',
            'customer_segment': 'standard'
        }
    ]
    
    # Generate 30 legitimate transactions
    for i in range(30):
        customer = random.choice(legit_customers)
        amount = round(random.uniform(50, 2000), 2)
        trans_time = base_time + timedelta(hours=random.randint(9, 17), minutes=random.randint(0, 59))  # Business hours
        
        transactions.append({
            'transaction_id': f'LEGIT_FIN_{i:04d}',
            'customer_id': customer['customer_id'],
            'customer_name': customer['customer_name'],
            'customer_email': customer['customer_email'],
            'customer_phone': customer['customer_phone'],
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': customer['customer_segment'],
            'customer_country': 'US',
            'transaction_datetime': trans_time,
            'transaction_date': trans_time.strftime('%Y-%m-%d'),
            'transaction_time': trans_time.strftime('%H:%M:%S'),
            'merchant_name': 'SecureBank Online',
            'merchant_category': 'Financial Services',
            'amount': amount,
            'payment_method': 'bank_transfer',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '',
            'transaction_type': random.choice(['transfer', 'payment', 'deposit']),
            'is_fraudulent': False,
            'fraud_indicators': '',
            'risk_score': random.uniform(5, 30),
            'fraud_type': ''
        })
    
    # Generate 10 suspicious transactions (structuring)
    structuring_amounts = [9999.99, 9800.00, 9750.50, 9900.00, 9850.25, 9999.00, 9700.00, 9950.00, 9825.00, 9875.00]
    for i, amount in enumerate(structuring_amounts):
        trans_time = base_time + timedelta(days=i//2, hours=random.randint(14, 16))
        
        transactions.append({
            'transaction_id': f'STRUCT_FIN_{i:04d}',
            'customer_id': f'STRUCT_CUSTOMER_{i:03d}',
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'business',
            'customer_country': 'US',
            'transaction_datetime': trans_time,
            'transaction_date': trans_time.strftime('%Y-%m-%d'),
            'transaction_time': trans_time.strftime('%H:%M:%S'),
            'merchant_name': 'SecureBank Online',
            'merchant_category': 'Financial Services',
            'amount': amount,
            'payment_method': 'bank_transfer',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '',
            'transaction_type': 'transfer',
            'is_fraudulent': True,
            'fraud_indicators': 'structuring',
            'risk_score': random.uniform(80, 95),
            'fraud_type': 'money_laundering'
        })
    
    return pd.DataFrame(transactions)

def generate_mixed_subscription_dataset():
    """Generate mixed subscription dataset"""
    transactions = []
    base_time = datetime.now() - timedelta(days=30)
    
    # Legitimate subscribers
    legit_subs = []
    for i in range(20):
        legit_subs.append({
            'customer_id': f'SUB_CUSTOMER_{i:03d}',
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': random.choice(['individual', 'family', 'premium']),
            'customer_country': 'US'
        })
    
    # Generate 60 legitimate subscription transactions
    for i in range(60):
        customer = random.choice(legit_subs)
        trans_time = base_time + timedelta(days=random.randint(0, 30))
        amount = random.choice([9.99, 14.99, 19.99, 29.99])  # Standard subscription tiers
        
        transactions.append({
            'transaction_id': f'LEGIT_SUB_{i:04d}',
            'customer_id': customer['customer_id'],
            'customer_name': customer['customer_name'],
            'customer_email': customer['customer_email'],
            'customer_phone': customer['customer_phone'],
            'customer_address': customer['customer_address'],
            'customer_city': customer['customer_city'],
            'customer_state': customer['customer_state'],
            'customer_zip_code': customer['customer_zip_code'],
            'customer_ip_address': customer['customer_ip_address'],
            'customer_segment': customer['customer_segment'],
            'customer_country': customer['customer_country'],
            'transaction_datetime': trans_time,
            'transaction_date': trans_time.strftime('%Y-%m-%d'),
            'transaction_time': trans_time.strftime('%H:%M:%S'),
            'merchant_name': 'StreamMax Pro',
            'merchant_category': 'Streaming Service',
            'amount': amount,
            'payment_method': random.choice(['visa', 'mastercard', 'paypal']),
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': fake.random_number(digits=4, fix_len=True),
            'transaction_type': 'subscription',
            'is_fraudulent': False,
            'fraud_indicators': '',
            'risk_score': random.uniform(5, 25),
            'fraud_type': ''
        })
    
    # Generate 15 fraudulent trial abuse transactions
    temp_domains = ['10minutemail.com', 'guerrillamail.com', 'tempmail.org']
    for i in range(15):
        trans_time = base_time + timedelta(hours=i*2)
        
        transactions.append({
            'transaction_id': f'TRIAL_ABUSE_{i:04d}',
            'customer_id': f'TRIAL_ABUSER_{i:03d}',
            'customer_name': f'Trial User{i}',
            'customer_email': f'trial{i}@{random.choice(temp_domains)}',
            'customer_phone': f'555-{random.randint(1000, 9999)}',
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': f'192.168.1.{100+i}',  # Similar IP range
            'customer_segment': 'trial',
            'customer_country': 'US',
            'transaction_datetime': trans_time,
            'transaction_date': trans_time.strftime('%Y-%m-%d'),
            'transaction_time': trans_time.strftime('%H:%M:%S'),
            'merchant_name': 'StreamMax Pro',
            'merchant_category': 'Streaming Service',
            'amount': 0.00,  # Free trial
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': f'{1000 + i}',  # Sequential pattern
            'transaction_type': 'free_trial',
            'is_fraudulent': True,
            'fraud_indicators': 'trial_abuse,temp_email,sequential_cards',
            'risk_score': random.uniform(75, 90),
            'fraud_type': 'trial_abuse'
        })
    
    return pd.DataFrame(transactions)

def add_required_columns(df):
    """Add required columns for fraud detection"""
    df['customer_lifetime_value'] = np.where(df['is_fraudulent'], 
                                            np.random.uniform(50, 500, len(df)),
                                            np.random.uniform(500, 5000, len(df)))
    df['customer_acquisition_channel'] = np.random.choice(['organic_search', 'paid_search', 'social_media', 'direct'], len(df))
    df['days_since_acquisition'] = np.where(df['is_fraudulent'],
                                           np.random.randint(1, 30, len(df)),
                                           np.random.randint(30, 365, len(df)))
    df['transaction_count'] = np.where(df['is_fraudulent'],
                                      np.random.randint(1, 3, len(df)),
                                      np.random.randint(3, 20, len(df)))
    df['device_type'] = np.random.choice(['Windows PC', 'iPhone/iOS', 'Android Mobile', 'Mac OS'], len(df))
    df['is_mobile'] = df['device_type'].str.contains('iPhone|Android')
    df['session_duration_seconds'] = np.where(df['is_fraudulent'],
                                             np.random.randint(30, 300, len(df)),
                                             np.random.randint(300, 1800, len(df)))
    df['pages_viewed'] = np.where(df['is_fraudulent'],
                                 np.random.randint(1, 5, len(df)),
                                 np.random.randint(5, 20, len(df)))
    df['processing_time_ms'] = np.random.randint(100, 2000, len(df))
    
    return df

def main():
    """Generate mixed datasets with legitimate and fraudulent transactions"""
    print("🔍 Generating Mixed Fraud Detection Test Files")
    print("=" * 60)
    
    datasets = [
        ("mixed_ecommerce_dataset.csv", generate_mixed_ecommerce_dataset, "80% legitimate, 20% fraudulent e-commerce"),
        ("mixed_financial_dataset.csv", generate_mixed_financial_dataset, "75% legitimate, 25% structuring fraud"),
        ("mixed_subscription_dataset.csv", generate_mixed_subscription_dataset, "80% legitimate, 20% trial abuse")
    ]
    
    for filename, generator_func, description in datasets:
        print(f"\n📊 Generating {filename}...")
        print(f"    {description}")
        
        df = generator_func()
        df = add_required_columns(df)
        
        # Save the dataset
        df.to_csv(filename, index=False)
        
        fraud_count = len(df[df['is_fraudulent'] == True])
        legit_count = len(df[df['is_fraudulent'] == False])
        
        print(f"  ✓ Created {len(df)} total transactions")
        print(f"  ✓ Legitimate: {legit_count} ({legit_count/len(df)*100:.1f}%)")
        print(f"  ✓ Fraudulent: {fraud_count} ({fraud_count/len(df)*100:.1f}%)")
        print(f"  ✓ Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
        print(f"  ✓ Total value: ${df['amount'].sum():,.2f}")
        print(f"  ✓ Saved to: {filename}")
    
    print(f"\n" + "=" * 60)
    print("✅ Mixed fraud detection test files generated!")
    print("\n🎯 Mixed Test Files Created:")
    print("  11. mixed_ecommerce_dataset.csv - Realistic e-commerce with hidden fraud")
    print("  12. mixed_financial_dataset.csv - Banking transactions with structuring")
    print("  13. mixed_subscription_dataset.csv - Subscription service with trial abuse")
    print("\n💡 These files are perfect for testing detection accuracy!")

if __name__ == "__main__":
    main()
