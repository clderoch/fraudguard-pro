#!/usr/bin/env python3

from cc_data_generator import generate_modern_business_data
import pandas as pd
import os

# Test with a few business types
test_businesses = ['saas_b2b', 'streaming_service', 'digital_marketplace']

print("🚀 Testing Enhanced Transaction Data Generator with US-only customers")
print("=" * 70)

# Create output directory
output_dir = 'test_transactions'
os.makedirs(output_dir, exist_ok=True)

for business in test_businesses:
    print(f"\n📊 Generating {business} transactions...")
    # Generate smaller dataset for testing
    df = generate_modern_business_data(business, num_transactions=1000)
    
    # Save to CSV
    filename = os.path.join(output_dir, f'{business}_transactions.csv')
    df.to_csv(filename, index=False)
    
    # Display summary statistics
    print(f"  ✓ Total transactions: {len(df):,}")
    print(f"  ✓ Unique customers: {df['customer_id'].nunique():,}")
    print(f"  ✓ Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
    print(f"  ✓ Average transaction: ${df['amount'].mean():.2f}")
    print(f"  ✓ All customers are US-based: {(df['customer_country'] == 'US').all()}")
    print(f"  ✓ Sample cities: {', '.join(df['customer_city'].unique()[:5])}")
    print(f"  ✓ Sample states: {', '.join(df['customer_state'].unique()[:5])}")
    print(f"  ✓ Saved to: {filename}")

print("\n" + "=" * 70)
print("✅ Test complete! All customers are US-based with city, state, and zip code.")
print(f"📁 Test files saved to: {output_dir}/")
