#!/usr/bin/env python3

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path to import from app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the fraud detection model
try:
    from app import SimpleFraudDetectionModel
    print("✅ Successfully imported SimpleFraudDetectionModel")
except ImportError as e:
    print(f"❌ Error importing: {e}")
    exit(1)

# Create test data with geographical anomalies
test_data = {
    'transaction_id': ['TEST_001', 'TEST_002', 'TEST_003', 'TEST_004', 'TEST_005'],
    'amount': [45.67, 1250.00, 23.50, 89.99, 3.99],
    'merchant_category': ['Restaurant', 'Electronics', 'Coffee Shop', 'Gas Station', 'Online'],
    'transaction_date': ['2024-01-15', '2024-01-15', '2024-01-16', '2024-01-16', '2024-01-17'],
    'transaction_time': ['14:30:00', '23:45:00', '08:15:00', '12:00:00', '02:30:00'],
    'customer_id': ['CUST_001', 'CUST_002', 'CUST_003', 'CUST_004', 'CUST_005'],
    'customer_state': ['CA', 'NY', 'TX', 'FL', 'CA'],
    'customer_zip_code': ['10001', '90210', '77001', '33101', '90210'],  # Mismatched ZIP/state
    'customer_ip_address': ['8.8.8.8', '192.168.1.1', '1.1.1.1', '45.123.45.67', '103.45.67.89'],
    'customer_city': ['Los Angeles', 'New York', 'Houston', 'Miami', 'San Francisco']
}

print("\n🔍 Testing Geographical Anomaly Detection")
print("=" * 50)

# Create DataFrame
df = pd.DataFrame(test_data)
print(f"📊 Created test data with {len(df)} transactions")

# Initialize fraud detection model
model = SimpleFraudDetectionModel()
print("🤖 Initialized fraud detection model")

# Run fraud detection
print("\n🔍 Running fraud detection...")
result_df = model.detect_fraud(df)

# Display results
print("\n📋 Fraud Detection Results:")
print("-" * 50)

for idx, row in result_df.iterrows():
    print(f"\nTransaction {idx + 1}:")
    print(f"  Amount: ${row['amount']:,.2f}")
    print(f"  Customer: {row['customer_id']}")
    print(f"  Location: {row['customer_city']}, {row['customer_state']} {row['customer_zip_code']}")
    print(f"  IP Address: {row['customer_ip_address']}")
    print(f"  Risk Score: {row['risk_score']}")
    print(f"  Safety Level: {row['safety_level']}")
    print(f"  Anomalies: {row['anomaly_flags']}")

# Summary
print("\n📊 Summary:")
print("-" * 20)
safety_counts = result_df['safety_level'].value_counts()
print(f"Safe: {safety_counts.get('Safe', 0)}")
print(f"Watch Closely: {safety_counts.get('Watch Closely', 0)}")
print(f"Needs Attention: {safety_counts.get('Needs Your Attention', 0)}")

print("\n✅ Test completed successfully!")
