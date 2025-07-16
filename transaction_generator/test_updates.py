#!/usr/bin/env python3

from cc_data_generator import generate_modern_business_data
import pandas as pd

print("Testing updated cc_data_generator with US-only customers...")

# Generate a small sample
df = generate_modern_business_data('saas_b2b', 100)

print(f"✓ Total transactions: {len(df)}")
print(f"✓ Unique customers: {df['customer_id'].nunique()}")

# Check new fields exist
required_fields = ['customer_city', 'customer_state', 'customer_zip_code', 'customer_country']
for field in required_fields:
    if field in df.columns:
        print(f"✓ Field '{field}' exists")
    else:
        print(f"✗ Field '{field}' missing")

print("\nSample customer data:")
print(df[['customer_name', 'customer_city', 'customer_state', 'customer_zip_code', 'customer_country']].head())

print("\nCountries in data:", df['customer_country'].unique())

print("\nTest complete!")
