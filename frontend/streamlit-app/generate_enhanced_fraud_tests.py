#!/usr/bin/env python3
"""
Enhanced Fraud Test Data Generator
Generates comprehensive test data for mobile app and healthcare fraud scenarios
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker
import numpy as np

fake = Faker('en_US')

def generate_mobile_app_fraud_tests():
    """Generate comprehensive mobile app fraud test cases"""
    transactions = []
    base_time = datetime.now() - timedelta(days=15)
    
    # Test Case 1: Device Emulator Fraud
    for i in range(8):
        transaction = {
            'transaction_id': f"MOBILE_EMULATOR_{i:03d}",
            'customer_id': f"MOBILE_FRAUD_USER_{i}",
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",  # Local IP
            'customer_segment': 'new',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(minutes=i*2),
            'transaction_date': (base_time + timedelta(minutes=i*2)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(minutes=i*2)).strftime('%H:%M:%S'),
            'merchant_name': 'GameVerse Online',
            'merchant_category': 'Gaming Platform',
            'amount': random.choice([9999.99, 999.99, 99.99]),  # Suspicious amounts
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': f"{random.randint(1000, 9999)}",
            'transaction_type': 'in_game_purchase',
            'device_type': 'Android Emulator',  # Key fraud indicator
            'is_mobile': True,
            'customer_lifetime_value': 0,  # New accounts
            'customer_acquisition_channel': 'unknown',
            'days_since_acquisition': 0,
            'transaction_count': i + 1,
            'session_duration_seconds': random.randint(30, 120),
            'pages_viewed': 1,
            'is_fraudulent': True,  # Known fraud
            'fraud_indicators': 'emulator_detected,suspicious_amount,new_account',
            'risk_score': 85,
            'fraud_type': 'device_emulator',
            'processing_time_ms': random.randint(200, 800)
        }
        transactions.append(transaction)
    
    # Test Case 2: Micro-transaction Abuse
    customer_id = "MICRO_ABUSE_001"
    for i in range(12):
        transaction = {
            'transaction_id': f"MICRO_ABUSE_{i:03d}",
            'customer_id': customer_id,
            'customer_name': 'John Microtester',
            'customer_email': 'test@tempmail.com',
            'customer_phone': '+1-555-0123',
            'customer_address': '123 Test Street',
            'customer_city': 'San Francisco',
            'customer_state': 'CA',
            'customer_zip_code': '94102',
            'customer_ip_address': f"8.8.8.{random.randint(1,255)}",
            'customer_segment': 'regular',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(minutes=i*5),
            'transaction_date': (base_time + timedelta(minutes=i*5)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(minutes=i*5)).strftime('%H:%M:%S'),
            'merchant_name': 'MobileGaming Pro',
            'merchant_category': 'Mobile Gaming',
            'amount': random.choice([0.99, 1.99, 2.99, 4.99]),  # Micro-transactions
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '1234',  # Sequential pattern
            'transaction_type': 'virtual_currency',
            'device_type': 'iPhone/iOS',
            'is_mobile': True,
            'customer_lifetime_value': 50,
            'customer_acquisition_channel': 'app_store',
            'days_since_acquisition': 1,
            'transaction_count': i + 1,
            'session_duration_seconds': random.randint(300, 600),
            'pages_viewed': 3,
            'is_fraudulent': True,
            'fraud_indicators': 'rapid_micro_transactions,sequential_card,disposable_email',
            'risk_score': 75,
            'fraud_type': 'micro_transaction_abuse',
            'processing_time_ms': random.randint(150, 400)
        }
        transactions.append(transaction)
    
    # Test Case 3: Account Takeover in Gaming
    for i in range(6):
        transaction = {
            'transaction_id': f"GAME_TAKEOVER_{i:03d}",
            'customer_id': 'LEGIT_GAMER_001',  # Existing account
            'customer_name': 'Sarah GamePlayer',
            'customer_email': 'sarah.gamer@email.com',
            'customer_phone': '+1-555-0789',
            'customer_address': '456 Gaming Ave',
            'customer_city': 'Austin',
            'customer_state': 'TX',
            'customer_zip_code': '73301',  # Wrong ZIP for TX
            'customer_ip_address': f"45.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",  # VPN range
            'customer_segment': 'vip',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(hours=12, minutes=i*10),
            'transaction_date': (base_time + timedelta(hours=12, minutes=i*10)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=12, minutes=i*10)).strftime('%H:%M:%S'),
            'merchant_name': 'Epic Gaming Store',
            'merchant_category': 'Gaming Platform',
            'amount': 599.99 if i == 0 else random.choice([49.99, 99.99, 199.99]),  # Sudden large purchase
            'payment_method': 'mastercard',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '9876',
            'transaction_type': 'game_purchase',
            'device_type': 'Windows PC',
            'is_mobile': False,
            'customer_lifetime_value': 2500,
            'customer_acquisition_channel': 'organic_search',
            'days_since_acquisition': 365,
            'transaction_count': 50 + i,  # Established account
            'session_duration_seconds': random.randint(1800, 3600),
            'pages_viewed': random.randint(5, 15),
            'is_fraudulent': True,
            'fraud_indicators': 'account_takeover,spending_spike,geo_mismatch,vpn_detected',
            'risk_score': 90,
            'fraud_type': 'account_takeover',
            'processing_time_ms': random.randint(300, 1000)
        }
        transactions.append(transaction)
    
    # Test Case 4: Virtual Currency Laundering
    for i in range(5):
        transaction = {
            'transaction_id': f"CURRENCY_LAUNDER_{i:03d}",
            'customer_id': f"CURRENCY_USER_{i}",
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': f"103.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'customer_segment': 'new',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(hours=24, minutes=i*30),
            'transaction_date': (base_time + timedelta(hours=24, minutes=i*30)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=24, minutes=i*30)).strftime('%H:%M:%S'),
            'merchant_name': 'CryptoGaming Exchange',
            'merchant_category': 'Gaming Platform',
            'amount': random.choice([9999.99, 9998.99, 9997.99]),  # Just under limits
            'payment_method': 'cryptocurrency',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '',
            'transaction_type': 'virtual_currency_large',
            'device_type': 'Linux Desktop',
            'is_mobile': False,
            'customer_lifetime_value': 0,
            'customer_acquisition_channel': 'unknown',
            'days_since_acquisition': 0,
            'transaction_count': 1,
            'session_duration_seconds': random.randint(60, 180),
            'pages_viewed': 2,
            'is_fraudulent': True,
            'fraud_indicators': 'money_laundering,high_value_new_account,crypto_payment,international_ip',
            'risk_score': 95,
            'fraud_type': 'money_laundering',
            'processing_time_ms': random.randint(500, 2000)
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def generate_healthcare_fraud_tests():
    """Generate comprehensive healthcare fraud test cases"""
    transactions = []
    base_time = datetime.now() - timedelta(days=10)
    
    # Test Case 1: Insurance Billing Fraud
    customer_id = "INSURANCE_FRAUD_001"
    for i in range(8):
        transaction = {
            'transaction_id': f"INSURANCE_FRAUD_{i:03d}",
            'customer_id': customer_id,
            'customer_name': 'Robert FakeBilling',
            'customer_email': 'rbilling@healthfraud.com',
            'customer_phone': '+1-555-0456',
            'customer_address': '789 Medical Plaza',
            'customer_city': 'Chicago',
            'customer_state': 'IL',
            'customer_zip_code': '60601',
            'customer_ip_address': f"198.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'customer_segment': 'regular',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(hours=i*3),
            'transaction_date': (base_time + timedelta(hours=i*3)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(hours=i*3)).strftime('%H:%M:%S'),
            'merchant_name': 'QuickCare Medical',
            'merchant_category': 'Healthcare Services',
            'amount': random.choice([999.99, 1999.99, 4999.99]),  # Just under insurance limits
            'payment_method': 'insurance_claim',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '',
            'transaction_type': 'medical_procedure',
            'device_type': 'Windows PC',
            'is_mobile': False,
            'customer_lifetime_value': 5000,
            'customer_acquisition_channel': 'insurance_network',
            'days_since_acquisition': 30,
            'transaction_count': i + 1,
            'session_duration_seconds': random.randint(600, 1800),
            'pages_viewed': random.randint(8, 20),
            'is_fraudulent': True,
            'fraud_indicators': 'insurance_limit_avoidance,rapid_billing,multiple_procedures_same_day',
            'risk_score': 85,
            'fraud_type': 'insurance_billing_fraud',
            'processing_time_ms': random.randint(1000, 3000)
        }
        transactions.append(transaction)
    
    # Test Case 2: After-hours Medical Billing (Suspicious)
    for i in range(6):
        transaction = {
            'transaction_id': f"AFTERHOURS_MEDICAL_{i:03d}",
            'customer_id': f"NIGHT_PATIENT_{i}",
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'new',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(days=2, hours=2, minutes=i*15),  # 2 AM
            'transaction_date': (base_time + timedelta(days=2, hours=2, minutes=i*15)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(days=2, hours=2, minutes=i*15)).strftime('%H:%M:%S'),
            'merchant_name': 'MidnightMed Services',
            'merchant_category': 'Telehealth Platform',
            'amount': random.choice([2500, 3500, 4500]),
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': f"{random.randint(1000, 9999)}",
            'transaction_type': 'emergency_consultation',
            'device_type': 'iPhone/iOS',
            'is_mobile': True,
            'customer_lifetime_value': 500,
            'customer_acquisition_channel': 'emergency_referral',
            'days_since_acquisition': 0,
            'transaction_count': 1,
            'session_duration_seconds': random.randint(180, 600),
            'pages_viewed': random.randint(3, 8),
            'is_fraudulent': True,
            'fraud_indicators': 'after_hours_billing,high_value_emergency,new_patient',
            'risk_score': 75,
            'fraud_type': 'suspicious_billing_time',
            'processing_time_ms': random.randint(500, 1500)
        }
        transactions.append(transaction)
    
    # Test Case 3: Youth Account High-Value Medical
    for i in range(4):
        transaction = {
            'transaction_id': f"YOUTH_HIGH_VALUE_{i:03d}",
            'customer_id': f"YOUTH_ACCOUNT_{i}",
            'customer_name': f"Teen User {i+1}",
            'customer_email': f"teen{i+1}@youth-email.com",
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': 'new',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(days=3, hours=i*4),
            'transaction_date': (base_time + timedelta(days=3, hours=i*4)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(days=3, hours=i*4)).strftime('%H:%M:%S'),
            'merchant_name': 'YouthHealth Direct',
            'merchant_category': 'Healthcare Services',
            'amount': random.choice([3500, 4500, 5500]),  # High value for youth
            'payment_method': 'amex',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': f"{random.randint(1000, 9999)}",
            'transaction_type': 'specialist_consultation',
            'device_type': 'iPad',
            'is_mobile': True,
            'customer_lifetime_value': 200,
            'customer_acquisition_channel': 'social_media',
            'days_since_acquisition': 1,
            'transaction_count': 1,
            'session_duration_seconds': random.randint(300, 900),
            'pages_viewed': random.randint(5, 12),
            'is_fraudulent': True,
            'fraud_indicators': 'youth_high_value,specialist_without_referral,new_account',
            'risk_score': 70,
            'fraud_type': 'age_verification_fraud',
            'processing_time_ms': random.randint(400, 1200)
        }
        transactions.append(transaction)
    
    # Test Case 4: Medical Identity Theft
    for i in range(5):
        transaction = {
            'transaction_id': f"MEDICAL_IDENTITY_{i:03d}",
            'customer_id': 'STOLEN_MEDICAL_ID',
            'customer_name': 'Jane PatientVictim',
            'customer_email': 'j.victim@email.com',
            'customer_phone': '+1-555-0999',
            'customer_address': '321 Victim Street',
            'customer_city': 'Phoenix',
            'customer_state': 'AZ',
            'customer_zip_code': '10001',  # NY ZIP with AZ state - mismatch
            'customer_ip_address': f"41.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",  # International IP
            'customer_segment': 'vip',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(days=5, hours=i*2),
            'transaction_date': (base_time + timedelta(days=5, hours=i*2)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(days=5, hours=i*2)).strftime('%H:%M:%S'),
            'merchant_name': 'GlobalHealth Services',
            'merchant_category': 'Healthcare Services',
            'amount': random.choice([1500, 2500, 3500]),
            'payment_method': 'discover',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': '5555',  # Repeated digits
            'transaction_type': 'prescription_order',
            'device_type': 'Android Mobile',
            'is_mobile': True,
            'customer_lifetime_value': 8000,
            'customer_acquisition_channel': 'insurance_network',
            'days_since_acquisition': 1095,  # 3 years
            'transaction_count': 50 + i,
            'session_duration_seconds': random.randint(120, 300),
            'pages_viewed': random.randint(2, 5),
            'is_fraudulent': True,
            'fraud_indicators': 'geo_mismatch,international_ip,repeated_card_digits,identity_theft',
            'risk_score': 95,
            'fraud_type': 'medical_identity_theft',
            'processing_time_ms': random.randint(800, 2500)
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def generate_enhanced_gaming_tests():
    """Generate additional gaming fraud scenarios"""
    transactions = []
    base_time = datetime.now() - timedelta(days=7)
    
    # Test Case 1: Bot Farm Activity
    for i in range(15):
        transaction = {
            'transaction_id': f"BOT_FARM_{i:03d}",
            'customer_id': f"BOT_ACCOUNT_{i:03d}",
            'customer_name': f"Bot User {i:03d}",
            'customer_email': f"bot{i:03d}@tempmail.org",
            'customer_phone': f"+1-555-{i:04d}",
            'customer_address': f"{i+1} Bot Street",
            'customer_city': 'San Jose',
            'customer_state': 'CA',
            'customer_zip_code': '95101',
            'customer_ip_address': f"192.168.1.{i+100}",  # Sequential local IPs
            'customer_segment': 'new',
            'customer_country': 'US',
            'transaction_datetime': base_time + timedelta(minutes=i*2),  # Rapid succession
            'transaction_date': (base_time + timedelta(minutes=i*2)).strftime('%Y-%m-%d'),
            'transaction_time': (base_time + timedelta(minutes=i*2)).strftime('%H:%M:%S'),
            'merchant_name': 'MMO Gold Exchange',
            'merchant_category': 'Gaming Platform',
            'amount': 10.00,  # Consistent small amounts
            'payment_method': 'visa',
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': f"{1000 + i}",  # Sequential card numbers
            'transaction_type': 'virtual_currency',
            'device_type': 'Linux Server',
            'is_mobile': False,
            'customer_lifetime_value': 10,
            'customer_acquisition_channel': 'automated',
            'days_since_acquisition': 0,
            'transaction_count': 1,
            'session_duration_seconds': 60,  # Very short sessions
            'pages_viewed': 1,
            'is_fraudulent': True,
            'fraud_indicators': 'bot_farm,sequential_accounts,rapid_succession,automated_behavior',
            'risk_score': 90,
            'fraud_type': 'bot_farm_activity',
            'processing_time_ms': 150
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def main():
    """Generate all enhanced fraud test data"""
    print("🔧 Generating Enhanced Fraud Test Data...")
    
    # Generate mobile app fraud tests
    print("📱 Generating mobile app fraud scenarios...")
    mobile_df = generate_mobile_app_fraud_tests()
    mobile_df.to_csv('enhanced_mobile_app_fraud.csv', index=False)
    print(f"✅ Created enhanced_mobile_app_fraud.csv with {len(mobile_df)} transactions")
    
    # Generate healthcare fraud tests
    print("🏥 Generating healthcare fraud scenarios...")
    healthcare_df = generate_healthcare_fraud_tests()
    healthcare_df.to_csv('enhanced_healthcare_fraud.csv', index=False)
    print(f"✅ Created enhanced_healthcare_fraud.csv with {len(healthcare_df)} transactions")
    
    # Generate additional gaming tests
    print("🎮 Generating enhanced gaming fraud scenarios...")
    gaming_df = generate_enhanced_gaming_tests()
    gaming_df.to_csv('enhanced_gaming_fraud.csv', index=False)
    print(f"✅ Created enhanced_gaming_fraud.csv with {len(gaming_df)} transactions")
    
    # Generate comprehensive mixed dataset
    print("📊 Creating comprehensive mixed fraud dataset...")
    all_fraud_df = pd.concat([mobile_df, healthcare_df, gaming_df], ignore_index=True)
    
    # Add some legitimate transactions for testing false positive rates
    legitimate_transactions = []
    for i in range(20):
        transaction = {
            'transaction_id': f"LEGIT_ENHANCED_{i:03d}",
            'customer_id': f"LEGIT_USER_{i}",
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_phone': fake.phone_number(),
            'customer_address': fake.address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_ip_address': fake.ipv4_public(),
            'customer_segment': random.choice(['regular', 'vip']),
            'customer_country': 'US',
            'transaction_datetime': datetime.now() - timedelta(hours=random.randint(1, 48)),
            'transaction_date': (datetime.now() - timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%d'),
            'transaction_time': (datetime.now() - timedelta(hours=random.randint(1, 48))).strftime('%H:%M:%S'),
            'merchant_name': random.choice(['LegitApp Store', 'TrustedHealth Clinic', 'ReliableGaming']),
            'merchant_category': random.choice(['Mobile Gaming', 'Healthcare Services', 'Gaming Platform']),
            'amount': round(random.uniform(15, 150), 2),
            'payment_method': random.choice(['visa', 'mastercard', 'amex']),
            'payment_status': 'completed',
            'response_code': '00',
            'response_text': 'Approved',
            'card_last4': f"{random.randint(1000, 9999)}",
            'transaction_type': 'purchase',
            'device_type': random.choice(['iPhone/iOS', 'Android Mobile', 'Windows PC']),
            'is_mobile': random.choice([True, False]),
            'customer_lifetime_value': random.randint(500, 5000),
            'customer_acquisition_channel': random.choice(['organic_search', 'app_store', 'referral']),
            'days_since_acquisition': random.randint(30, 1000),
            'transaction_count': random.randint(5, 50),
            'session_duration_seconds': random.randint(300, 1800),
            'pages_viewed': random.randint(3, 15),
            'is_fraudulent': False,
            'fraud_indicators': 'none_detected',
            'risk_score': random.randint(5, 35),
            'fraud_type': '',
            'processing_time_ms': random.randint(200, 800)
        }
        legitimate_transactions.append(transaction)
    
    legit_df = pd.DataFrame(legitimate_transactions)
    comprehensive_df = pd.concat([all_fraud_df, legit_df], ignore_index=True)
    
    # Shuffle the dataset
    comprehensive_df = comprehensive_df.sample(frac=1).reset_index(drop=True)
    comprehensive_df.to_csv('comprehensive_enhanced_fraud_dataset.csv', index=False)
    
    print(f"✅ Created comprehensive_enhanced_fraud_dataset.csv with {len(comprehensive_df)} transactions")
    print(f"   - {len(all_fraud_df)} fraudulent transactions")
    print(f"   - {len(legit_df)} legitimate transactions")
    print(f"   - Fraud rate: {len(all_fraud_df)/len(comprehensive_df)*100:.1f}%")
    
    print("\n🎯 Enhanced fraud test data generation complete!")
    print("📁 Files created:")
    print("   - enhanced_mobile_app_fraud.csv")
    print("   - enhanced_healthcare_fraud.csv") 
    print("   - enhanced_gaming_fraud.csv")
    print("   - comprehensive_enhanced_fraud_dataset.csv")

if __name__ == "__main__":
    main()
