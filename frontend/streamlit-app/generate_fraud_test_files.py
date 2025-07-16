#!/usr/bin/env python3
"""
Generate specialized test files for comprehensive anomaly detection testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from faker import Faker

# Initialize Faker
fake = Faker('en_US')

def generate_high_fraud_dataset():
    """Generate a dataset with high concentration of fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(days=7)
    
    # Create customers for fraud testing
    customers = []
    for i in range(20):
        customers.append({
            'customer_id': f"FRAUD_TEST_{i:03d}",
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'high_risk',
            'customer_country': 'US'
        })
    
    # 1. Card Testing Patterns (small amounts, rapid fire)
    customer = customers[0]
    test_amounts = [1.00, 0.50, 0.01, 2.00, 5.00, 10.00]
    for i, amount in enumerate(test_amounts):
        transactions.append({
            'transaction_id': f"CARD_TEST_{i:03d}",
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
            'transaction_datetime': base_time + timedelta(seconds=i*30),
            'transaction_date': (base_time + timedelta(seconds=i*30)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(seconds=i*30)).strftime('%H:%M:%S'),
            'merchant_name': 'Test Merchant',
            'merchant_category': 'Online Retail',
            'amount': amount,
            'payment_method': 'visa',
            'payment_status': 'completed' if i < 4 else 'failed',
            'response_code': '00' if i < 4 else '51',
            'response_text': 'Approved' if i < 4 else 'Insufficient funds',
            'card_last4': f"{1111 + i}",
            'transaction_type': 'purchase'
        })
    
    # 2. Geographic Anomalies (location hopping)
    customer = customers[1]
    locations = [
        ('New York', 'NY', '10001', '74.125.224.72'),  # NY
        ('Los Angeles', 'CA', '90210', '173.252.66.7'),  # CA
        ('Miami', 'FL', '33101', '8.8.8.8'),  # FL
        ('Seattle', 'WA', '98101', '157.240.2.1'),  # WA
    ]
    
    for i, (city, state, zip_code, ip) in enumerate(locations):
        transactions.append({
            'transaction_id': f"GEO_HOP_{i:03d}",
            'customer_id': customer['customer_id'],
            'customer_name': customer['customer_name'],
            'customer_email': customer['customer_email'],
            'customer_phone': customer['customer_phone'],
            'customer_address': customer['customer_address'],
            'customer_city': city,
            'customer_state': state,
            'customer_zip_code': zip_code,
            'customer_ip_address': ip,
            'customer_segment': customer['customer_segment'],
            'customer_country': customer['customer_country'],
            'transaction_datetime': base_time + timedelta(hours=i*2),
            'transaction_date': (base_time + timedelta(hours=i*2)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=i*2)).strftime('%H:%M:%S'),
            'merchant_name': 'Travel Store',
            'merchant_category': 'Travel',
            'amount': round(random.uniform(200, 800), 2),
            'payment_method': 'mastercard',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '4567',
            'transaction_type': 'purchase'
        })
    
    # 3. Velocity Attacks (same customer, rapid high-value transactions)
    customer = customers[2]
    for i in range(8):  # 8 transactions in 10 minutes
        transactions.append({
            'transaction_id': f"VEL_ATTACK_{i:03d}",
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
            'transaction_datetime': base_time + timedelta(minutes=i*1.25),
            'transaction_date': (base_time + timedelta(minutes=i*1.25)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(minutes=i*1.25)).strftime('%H:%M:%S'),
            'merchant_name': 'Electronics Store',
            'merchant_category': 'Electronics',
            'amount': round(500 + (i * 100), 2),  # Escalating amounts
            'payment_method': 'amex',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '9876',
            'transaction_type': 'purchase'
        })
    
    # 4. Off-Hours Suspicious Activity
    customer = customers[3]
    suspicious_hours = [2, 3, 4, 23, 1]  # Late night/early morning
    for i, hour in enumerate(suspicious_hours):
        night_time = base_time.replace(hour=hour, minute=random.randint(0, 59))
        # Make it weekend
        days_to_saturday = (5 - night_time.weekday()) % 7
        night_time = night_time + timedelta(days=days_to_saturday)
        
        transactions.append({
            'transaction_id': f"NIGHT_FRAUD_{i:03d}",
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
            'transaction_datetime': night_time,
            'transaction_date': night_time.strftime('%Y-%m-%d'),
            'transaction_time': night_time.strftime('%H:%M:%S'),
            'merchant_name': 'Late Night Store',
            'merchant_category': 'Convenience Store',
            'amount': round(random.uniform(150, 500), 2),
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '1357',
            'transaction_type': 'purchase'
        })
    
    # 5. Data Quality Issues
    fake_customers = [
        {
            'customer_id': 'FAKE_001',
            'customer_name': 'TEST USER',
            'customer_email': 'test@10minutemail.com',
            'customer_phone': '555-0123',
            'card_last4': '1234'
        },
        {
            'customer_id': 'FAKE_002',
            'customer_name': 'JOHN DOE',
            'customer_email': 'fake@guerrillamail.com',
            'customer_phone': '555-1234',
            'card_last4': '2345'
        },
        {
            'customer_id': 'FAKE_003',
            'customer_name': 'FRAUD TEST',
            'customer_email': 'temp@tempmail.org',
            'customer_phone': '555-2345',
            'card_last4': '3456'
        }
    ]
    
    for i, fake_cust in enumerate(fake_customers):
        transactions.append({
            'transaction_id': f"FAKE_DATA_{i:03d}",
            'customer_id': fake_cust['customer_id'],
            'customer_name': fake_cust['customer_name'],
            'customer_email': fake_cust['customer_email'],
            'customer_phone': fake_cust['customer_phone'],
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'suspicious',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(hours=i+10),
            'transaction_date': (base_time + timedelta(hours=i+10)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=i+10)).strftime('%H:%M:%S'),
            'merchant_name': 'Suspicious Store',
            'merchant_category': 'Online Retail',
            'amount': round(random.uniform(50, 200), 2),
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': fake_cust['card_last4'],
            'transaction_type': 'purchase'
        })
    
    return pd.DataFrame(transactions)

def generate_ecommerce_fraud_dataset():
    """Generate e-commerce specific fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(days=14)
    
    # 1. Account Takeover Pattern
    legitimate_customer = {
        'customer_id': 'LEGIT_001',
        'customer_name': 'Sarah Johnson',
        'customer_email': 'sarah.johnson@gmail.com',
        'customer_phone': '555-0987',
        'customer_address': '123 Main St, Apt 4B',
        'customer_city': 'Denver',
        'customer_state': 'CO',
        'customer_zip_code': '80202',
        'customer_ip_address': '192.168.1.100',
        'customer_segment': 'regular',
        'customer_country': 'US'
    }
    
    # Normal transaction first
    transactions.append({
        'transaction_id': 'NORMAL_001',
        'customer_id': legitimate_customer['customer_id'],
        'customer_name': legitimate_customer['customer_name'],
        'customer_email': legitimate_customer['customer_email'],
        'customer_phone': legitimate_customer['customer_phone'],
        'customer_address': legitimate_customer['customer_address'],
        'customer_city': legitimate_customer['customer_city'],
        'customer_state': legitimate_customer['customer_state'],
        'customer_zip_code': legitimate_customer['customer_zip_code'],
        'customer_ip_address': legitimate_customer['customer_ip_address'],
        'customer_segment': legitimate_customer['customer_segment'],
        'customer_country': legitimate_customer['customer_country'],
        'transaction_datetime': base_time,
        'transaction_date': base_time.strftime('%Y-%m-%d'),
        'transaction_time': base_time.strftime('%H:%M:%S'),
        'merchant_name': 'Fashion Boutique',
        'merchant_category': 'Clothing',
        'amount': 89.99,
        'payment_method': 'visa',
        'payment_status': 'completed',
        'response_code': '00',
        'response_text': 'Approved',
        'card_last4': '4567',
        'transaction_type': 'purchase'
    })
    
    # Account takeover - same customer, different IP, different shipping
    transactions.append({
        'transaction_id': 'TAKEOVER_001',
        'customer_id': legitimate_customer['customer_id'],
        'customer_name': legitimate_customer['customer_name'],
        'customer_email': legitimate_customer['customer_email'],
        'customer_phone': legitimate_customer['customer_phone'],
        'customer_address': '999 Suspicious Lane',  # Different address
        'customer_city': 'Miami',  # Different city
        'customer_state': 'FL',  # Different state
        'customer_zip_code': '33101',  # Different ZIP
        'customer_ip_address': '203.0.113.5',  # Different IP
        'customer_segment': legitimate_customer['customer_segment'],
        'customer_country': legitimate_customer['customer_country'],
        'transaction_datetime': base_time + timedelta(hours=2),
        'transaction_date': (base_time + timedelta(hours=2)).strftime('%Y-%m-%d'),
        'transaction_time': (base_time + timedelta(hours=2)).strftime('%H:%M:%S'),
        'merchant_name': 'Electronics World',
        'merchant_category': 'Electronics',
        'amount': 1299.99,  # Much higher amount
        'payment_method': 'visa',
        'payment_status': 'completed',
        'response_code': '00',
        'response_text': 'Approved',
        'card_last4': '4567',  # Same card
        'transaction_type': 'purchase'
    })
    
    # 2. Reshipping Fraud Pattern
    for i in range(5):
        transactions.append({
            'transaction_id': f'RESHIP_{i:03d}',
            'customer_id': f'RESHIP_CUST_{i}',
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': f'{random.randint(100, 999)} Warehouse Blvd',
            'customer_city': 'Various',
            'customer_state': random.choice(['FL', 'NY', 'CA']),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'new',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(hours=i*3),
            'transaction_date': (base_time + timedelta(hours=i*3)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=i*3)).strftime('%H:%M:%S'),
            'merchant_name': 'Tech Store',
            'merchant_category': 'Electronics',
            'amount': round(random.uniform(800, 2000), 2),
            'payment_method': random.choice(['visa', 'mastercard']),
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': fake.random_number(digits=4, fix_len=True),
            'transaction_type': 'purchase'
        })
    
    return pd.DataFrame(transactions)

def generate_financial_fraud_dataset():
    """Generate financial services fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(days=5)
    
    # 1. Money Laundering Pattern (structured transactions)
    customer = {
        'customer_id': 'LAUNDER_001',
        'customer_name': 'Michael Chen',
        'customer_email': 'mchen@example.com',
        'customer_phone': '555-7890',
        'customer_address': '456 Business Ave',
        'customer_city': 'Las Vegas',
        'customer_state': 'NV',
        'customer_zip_code': '89101',
        'customer_ip_address': '198.51.100.1',
        'customer_segment': 'business',
        'customer_country': 'US'
    }
    
    # Multiple transactions just under reporting threshold
    structured_amounts = [9999.99, 9800.00, 9750.50, 9900.00, 9850.25]
    for i, amount in enumerate(structured_amounts):
        transactions.append({
            'transaction_id': f'STRUCT_{i:03d}',
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
            'transaction_datetime': base_time + timedelta(days=i),
            'transaction_date': (base_time + timedelta(days=i)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(days=i)).strftime('%H:%M:%S'),
            'merchant_name': 'Crypto Exchange Pro',
            'merchant_category': 'Financial Services',
            'amount': amount,
            'payment_method': 'bank_transfer',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '',
            'transaction_type': 'deposit'
        })
    
    # 2. Pump and Dump Pattern (rapid crypto trades)
    for i in range(10):
        transactions.append({
            'transaction_id': f'PUMP_{i:03d}',
            'customer_id': f'TRADER_{i:02d}',
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'trader',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(minutes=i*15),
            'transaction_date': (base_time + timedelta(minutes=i*15)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(minutes=i*15)).strftime('%H:%M:%S'),
            'merchant_name': 'Crypto Exchange Pro',
            'merchant_category': 'Cryptocurrency',
            'amount': round(random.uniform(5000, 50000), 2),
            'payment_method': 'crypto',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '',
            'transaction_type': 'buy' if i < 5 else 'sell'
        })
    
    return pd.DataFrame(transactions)

def generate_subscription_fraud_dataset():
    """Generate subscription service fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(days=30)
    
    # 1. Free Trial Abuse
    for i in range(15):
        fake_email_domains = ['10minutemail.com', 'guerrillamail.com', 'tempmail.org', 'mailinator.com']
        transactions.append({
            'transaction_id': f'TRIAL_ABUSE_{i:03d}',
            'customer_id': f'TRIAL_USER_{i:03d}',
            'customer_name': f'Trial User{i}',
            'customer_email': f'user{i}@{random.choice(fake_email_domains)}',
            'customer_phone': f'555-{random.randint(1000, 9999)}',
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': f'192.168.1.{100+i}',  # Similar IP range
            'customer_segment': 'trial',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(hours=i*2),
            'transaction_date': (base_time + timedelta(hours=i*2)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=i*2)).strftime('%H:%M:%S'),
            'merchant_name': 'StreamFlix Plus',
            'merchant_category': 'Streaming Service',
            'amount': 0.00,  # Free trial
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': f'{1111 + i}',  # Sequential cards
            'transaction_type': 'free_trial'
        })
    
    # 2. Subscription Stacking (same user, multiple accounts)
    base_customer = {
        'customer_name': 'Robert Smith',
        'customer_phone': '555-9876',
        'customer_address': '789 Oak Street',
        'customer_city': 'Portland',
        'customer_state': 'OR',
        'customer_zip_code': '97201',
        'customer_ip_address': '203.0.113.10'
    }
    
    variations = [
        'Robert Smith', 'Bob Smith', 'R Smith', 'Robert S', 'Rob Smith'
    ]
    
    for i, name_variation in enumerate(variations):
        transactions.append({
            'transaction_id': f'STACK_{i:03d}',
            'customer_id': f'STACK_USER_{i:03d}',
            'customer_name': name_variation,
            'customer_email': f'{name_variation.lower().replace(" ", ".")}@gmail.com',
            'customer_phone': base_customer['customer_phone'],
            'customer_address': base_customer['customer_address'],
            'customer_city': base_customer['customer_city'],
            'customer_state': base_customer['customer_state'],
            'customer_zip_code': base_customer['customer_zip_code'],
            'customer_ip_address': base_customer['customer_ip_address'],
            'customer_segment': 'subscriber',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(days=i*2),
            'transaction_date': (base_time + timedelta(days=i*2)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(days=i*2)).strftime('%H:%M:%S'),
            'merchant_name': 'Premium Music Service',
            'merchant_category': 'Music Streaming',
            'amount': 9.99,
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '7890',  # Same card
            'transaction_type': 'subscription'
        })
    
    return pd.DataFrame(transactions)

def main():
    """Generate all specialized fraud test datasets"""
    print("🔍 Generating Specialized Fraud Detection Test Files")
    print("=" * 60)
    
    test_datasets = [
        ("high_fraud_patterns.csv", generate_high_fraud_dataset),
        ("ecommerce_fraud_patterns.csv", generate_ecommerce_fraud_dataset),
        ("financial_fraud_patterns.csv", generate_financial_fraud_dataset),
        ("subscription_fraud_patterns.csv", generate_subscription_fraud_dataset)
    ]
    
    for filename, generator_func in test_datasets:
        print(f"\n📊 Generating {filename}...")
        df = generator_func()
        
        # Add missing columns that fraud detection expects
        df['customer_lifetime_value'] = 1000.0
        df['customer_acquisition_channel'] = 'direct'
        df['days_since_acquisition'] = 30
        df['transaction_count'] = 1
        df['device_type'] = 'Windows PC'
        df['is_mobile'] = False
        df['session_duration_seconds'] = 300
        df['pages_viewed'] = 5
        df['is_fraudulent'] = True  # Mark as fraudulent for testing
        df['fraud_indicators'] = 'test_pattern'
        df['risk_score'] = 85
        df['fraud_type'] = 'test'
        df['processing_time_ms'] = 500
        
        # Save the dataset
        df.to_csv(filename, index=False)
        
        print(f"  ✓ Created {len(df)} transactions")
        print(f"  ✓ Unique customers: {df['customer_id'].nunique()}")
        print(f"  ✓ Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
        print(f"  ✓ Total value: ${df['amount'].sum():,.2f}")
        print(f"  ✓ Saved to: {filename}")
    
    print(f"\n" + "=" * 60)
    print("✅ Specialized fraud test files generated!")
    print("\n🎯 Test Files Created:")
    print("  1. high_fraud_patterns.csv - Card testing, velocity attacks, geo anomalies")
    print("  2. ecommerce_fraud_patterns.csv - Account takeover, reshipping fraud")
    print("  3. financial_fraud_patterns.csv - Money laundering, crypto manipulation")
    print("  4. subscription_fraud_patterns.csv - Trial abuse, account stacking")

if __name__ == "__main__":
    main()
