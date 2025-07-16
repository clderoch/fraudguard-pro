#!/usr/bin/env python3
"""
Generate additional industry-specific fraud test files
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from faker import Faker

fake = Faker('en_US')

def generate_mobile_app_fraud():
    """Generate mobile app specific fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(days=3)
    
    # 1. In-App Purchase Fraud (IAP)
    for i in range(12):
        transactions.append({
            'transaction_id': f'IAP_FRAUD_{i:03d}',
            'customer_id': f'MOBILE_USER_{i:03d}',
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'mobile_gamer',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(minutes=i*5),
            'transaction_date': (base_time + timedelta(minutes=i*5)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(minutes=i*5)).strftime('%H:%M:%S'),
            'merchant_name': 'Mobile Game Store',
            'merchant_category': 'Mobile Gaming',
            'amount': random.choice([0.99, 4.99, 9.99, 19.99, 49.99, 99.99]),
            'payment_method': random.choice(['apple_pay', 'google_pay', 'visa']),
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': fake.random_number(digits=4, fix_len=True),
            'transaction_type': 'in_app_purchase',
            'device_type': random.choice(['iPhone/iOS', 'Android Mobile']),
            'is_mobile': True
        })
    
    return pd.DataFrame(transactions)

def generate_travel_fraud():
    """Generate travel industry fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(days=2)
    
    # 1. Last-minute high-value bookings with mismatched data
    suspicious_bookings = [
        {
            'name': 'John Smith',
            'email': 'temp123@tempmail.org',
            'phone': '555-0000',
            'billing_state': 'CA',
            'billing_zip': '90210',
            'ip': '203.0.113.5',  # Different location IP
            'amount': 2499.99
        },
        {
            'name': 'Jane Doe',
            'email': 'fake@guerrillamail.com',
            'phone': '555-1111',
            'billing_state': 'NY',
            'billing_zip': '10001',
            'ip': '198.51.100.10',
            'amount': 3599.99
        }
    ]
    
    for i, booking in enumerate(suspicious_bookings):
        transactions.append({
            'transaction_id': f'TRAVEL_FRAUD_{i:03d}',
            'customer_id': f'TRAVELER_{i:03d}',
            'customer_name': booking['name'],
            'customer_email': booking['email'],
            'customer_phone': booking['phone'],
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': booking['billing_state'],
            'customer_zip_code': booking['billing_zip'],
            'customer_ip_address': booking['ip'],
            'customer_segment': 'new',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(hours=i*2),
            'transaction_date': (base_time + timedelta(hours=i*2)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=i*2)).strftime('%H:%M:%S'),
            'merchant_name': 'Global Travel Booking',
            'merchant_category': 'Travel Services',
            'amount': booking['amount'],
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': fake.random_number(digits=4, fix_len=True),
            'transaction_type': 'booking'
        })
    
    return pd.DataFrame(transactions)

def generate_healthcare_fraud():
    """Generate healthcare fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(days=1)
    
    # 1. Medical identity theft pattern
    victim_info = {
        'customer_id': 'MEDICAL_VICTIM_001',
        'customer_name': 'Mary Johnson',
        'customer_email': 'mary.johnson@email.com',
        'customer_phone': '555-9876',
        'customer_address': '123 Health St',
        'customer_city': 'Austin',
        'customer_state': 'TX',
        'customer_zip_code': '73301'
    }
    
    # Normal transaction
    transactions.append({
        'transaction_id': 'NORMAL_MED_001',
        'customer_id': victim_info['customer_id'],
        'customer_name': victim_info['customer_name'],
        'customer_email': victim_info['customer_email'],
        'customer_phone': victim_info['customer_phone'],
        'customer_address': victim_info['customer_address'],
        'customer_city': victim_info['customer_city'],
        'customer_state': victim_info['customer_state'],
        'customer_zip_code': victim_info['customer_zip_code'],
        'customer_ip_address': '192.168.1.50',
        'customer_segment': 'patient',
        'customer_country': 'US',
        'transaction_datetime': base_time,
        'transaction_date': base_time.strftime('%Y-%m-%d'),
        'transaction_time': base_time.strftime('%H:%M:%S'),
        'merchant_name': 'Austin Family Clinic',
        'merchant_category': 'Healthcare',
        'amount': 150.00,
        'payment_method': 'visa',
        'payment_status': 'completed',
        'response_code': '00',
        'response_text': 'Approved',
        'card_last4': '8901',
        'transaction_type': 'consultation'
    })
    
    # Fraudulent transaction - same patient, different location/IP
    transactions.append({
        'transaction_id': 'FRAUD_MED_001',
        'customer_id': victim_info['customer_id'],
        'customer_name': victim_info['customer_name'],
        'customer_email': victim_info['customer_email'],
        'customer_phone': victim_info['customer_phone'],
        'customer_address': '999 Fraud Avenue',  # Different address
        'customer_city': 'Miami',  # Different city
        'customer_state': 'FL',  # Different state
        'customer_zip_code': '33101',  # Different ZIP
        'customer_ip_address': '203.0.113.25',  # Different IP
        'customer_segment': 'patient',
        'customer_country': 'US',
        'transaction_datetime': base_time + timedelta(hours=3),
        'transaction_date': (base_time + timedelta(hours=3)).strftime('%Y-%m-%d'),
        'transaction_time': (base_time + timedelta(hours=3)).strftime('%H:%M:%S'),
        'merchant_name': 'Miami Specialty Center',
        'merchant_category': 'Healthcare',
        'amount': 750.00,  # Much higher amount
        'payment_method': 'visa',
        'payment_status': 'completed',
        'response_code': '00',
        'response_text': 'Approved',
        'card_last4': '8901',  # Same card
        'transaction_type': 'specialist_consultation'
    })
    
    return pd.DataFrame(transactions)

def generate_charity_fraud():
    """Generate charity/donation fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(hours=12)
    
    # 1. Disaster response fraud (fake emergency donations)
    for i in range(8):
        transactions.append({
            'transaction_id': f'CHARITY_FRAUD_{i:03d}',
            'customer_id': f'DONOR_{i:03d}',
            'customer_name': fake.name(),
            'customer_email': f'generous{i}@tempmail.org',
            'customer_phone': f'555-{random.randint(1000, 9999)}',
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': f'198.51.100.{20+i}',  # Similar IP range
            'customer_segment': 'donor',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(minutes=i*15),
            'transaction_date': (base_time + timedelta(minutes=i*15)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(minutes=i*15)).strftime('%H:%M:%S'),
            'merchant_name': 'Emergency Relief Fund',
            'merchant_category': 'Charity',
            'amount': round(random.uniform(25, 500), 2),
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': fake.random_number(digits=4, fix_len=True),
            'transaction_type': 'donation'
        })
    
    return pd.DataFrame(transactions)

def generate_education_fraud():
    """Generate education sector fraud patterns"""
    transactions = []
    base_time = datetime.now() - timedelta(hours=6)
    
    # 1. Student loan fraud / fake enrollment
    for i in range(6):
        transactions.append({
            'transaction_id': f'EDU_FRAUD_{i:03d}',
            'customer_id': f'STUDENT_{i:03d}',
            'customer_name': f'Student{i} Test',
            'customer_email': f'student{i}@fakeschool.edu',
            'customer_phone': f'555-{random.randint(2000, 2999)}',
            'customer_address': f'{random.randint(100, 999)} Campus Drive',
            'customer_city': 'Education City',
            'customer_state': random.choice(['CA', 'NY', 'TX']),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'student',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(hours=i),
            'transaction_date': (base_time + timedelta(hours=i)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=i)).strftime('%H:%M:%S'),
            'merchant_name': 'Online University Portal',
            'merchant_category': 'Education',
            'amount': round(random.uniform(2000, 8000), 2),  # High tuition amounts
            'payment_method': 'bank_transfer',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '',
            'transaction_type': 'tuition_payment'
        })
    
    return pd.DataFrame(transactions)

def add_standard_columns(df):
    """Add standard columns required by fraud detection"""
    df['customer_lifetime_value'] = np.random.uniform(500, 3000, len(df))
    df['customer_acquisition_channel'] = np.random.choice(['organic_search', 'paid_search', 'social_media', 'direct'], len(df))
    df['days_since_acquisition'] = np.random.randint(1, 365, len(df))
    df['transaction_count'] = np.random.randint(1, 10, len(df))
    df['device_type'] = df.get('device_type', 'Windows PC')
    df['is_mobile'] = df.get('is_mobile', False)
    df['session_duration_seconds'] = np.random.randint(60, 1800, len(df))
    df['pages_viewed'] = np.random.randint(1, 15, len(df))
    df['is_fraudulent'] = True  # These are all fraud test cases
    df['fraud_indicators'] = 'specialized_fraud_pattern'
    df['risk_score'] = np.random.uniform(70, 100, len(df))
    df['fraud_type'] = 'test_pattern'
    df['processing_time_ms'] = np.random.randint(200, 2000, len(df))
    return df

def main():
    """Generate additional specialized fraud test files"""
    print("🔍 Generating Additional Specialized Fraud Test Files")
    print("=" * 60)
    
    generators = [
        ("mobile_app_fraud.csv", generate_mobile_app_fraud),
        ("travel_fraud.csv", generate_travel_fraud),
        ("healthcare_fraud.csv", generate_healthcare_fraud),
        ("charity_fraud.csv", generate_charity_fraud),
        ("education_fraud.csv", generate_education_fraud)
    ]
    
    for filename, generator_func in generators:
        print(f"\n📊 Generating {filename}...")
        df = generator_func()
        df = add_standard_columns(df)
        
        # Save the dataset
        df.to_csv(filename, index=False)
        
        print(f"  ✓ Created {len(df)} transactions")
        print(f"  ✓ Unique customers: {df['customer_id'].nunique()}")
        print(f"  ✓ Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
        print(f"  ✓ Average amount: ${df['amount'].mean():.2f}")
        print(f"  ✓ Total value: ${df['amount'].sum():,.2f}")
        print(f"  ✓ Saved to: {filename}")
    
    print(f"\n" + "=" * 60)
    print("✅ Additional specialized fraud test files generated!")
    print("\n🎯 New Test Files Created:")
    print("  6. mobile_app_fraud.csv - In-app purchase fraud patterns")
    print("  7. travel_fraud.csv - Last-minute bookings with data mismatches")
    print("  8. healthcare_fraud.csv - Medical identity theft patterns")
    print("  9. charity_fraud.csv - Fake emergency donation campaigns")
    print("  10. education_fraud.csv - Student loan and enrollment fraud")

if __name__ == "__main__":
    main()
