# Universal Transaction Generator - Enhanced for Small Merchants

## 🎯 Major Improvements Made

Your `universal_transaction_generator.py` has been significantly enhanced with a focus on **realistic credit card transaction data for small merchants**. Here are the key improvements:

### 1. **Realistic Credit Card Data Generation**
- **Valid Credit Card Numbers**: Implemented Luhn algorithm validation
- **Card Type Distribution**: Realistic distribution (Visa 60%, Mastercard 28%, Amex 8%, Discover 4%)
- **Card Prefixes**: Real card prefixes matching actual card networks

### 2. **Enhanced Payment Processing Realism**
- **Real Decline Codes**: Actual payment processor response codes with realistic frequencies
  - `00`: Approved
  - `05`: Do not honor (25% of declines)
  - `51`: Insufficient funds (20% of declines)
  - `14`: Invalid card (15% of declines)
  - `54`: Expired card (12% of declines)
  - And more...

- **Processing Times**: Realistic processing times for small merchants (800-3500ms)
- **Success Rates**: Dynamic success rates based on amount, risk, and time

### 3. **Small Merchant Focus**
- **Merchant Types**: 5 specialized small merchant categories:
  - Local Restaurant
  - Local Retail Store
  - Service Business
  - Professional Services
  - Healthcare Practice

- **Merchant-Specific Patterns**:
  - Realistic transaction amounts per business type
  - Peak hours and seasonal variations
  - Card present/not present ratios
  - Tip handling for restaurants
  - Tax calculations

### 4. **Realistic Fraud Patterns**
- **Small Merchant Fraud Types**:
  - Card Testing (40%): Small amounts like $1.00, $2.00, $9.99
  - Stolen Card (35%): Larger amounts, different locations
  - Friendly Fraud (20%): Legitimate customers disputing charges
  - Account Takeover (5%): Compromised customer accounts

- **Lower Fraud Rates**: Realistic 0.1-0.5% fraud rates for small merchants
- **Contextual Indicators**: Fraud indicators specific to each fraud type

### 5. **Enhanced Customer Behavior**
- **Repeat Customers**: 30% regular customers with realistic visit patterns
- **Customer Loyalty**: Repeat visit frequencies and spending patterns
- **Preferred Payment Methods**: Customer payment preferences
- **Geographic Consistency**: Consistent customer locations

### 6. **Transaction Entry Methods**
- **Card Present Transactions**: Chip (70%), Swipe (25%), Tap (5%)
- **Card Not Present**: Keyed transactions with higher decline rates
- **Entry Method Impact**: Different processing patterns based on entry method

## 📊 New Data Fields Added

### Credit Card Specific:
- `card_number`: Valid credit card numbers
- `card_type`: visa, mastercard, amex, discover
- `card_present`: True/False for transaction type
- `entry_method`: chip, swipe, tap, keyed
- `response_code`: Real payment processor codes
- `response_text`: Human-readable response messages
- `processing_time_ms`: Realistic processing times

### Merchant Specific:
- `tip_amount`: Tips for restaurant transactions
- `tax_amount`: Calculated tax amounts
- `terminal_id`: Merchant terminal identifier
- `batch_number`: Transaction batch processing
- `merchant_type`: Small merchant category

### Fraud Detection:
- `fraud_type`: Specific fraud pattern type
- `fraud_indicators`: Comma-separated fraud indicators
- `is_fraud`: 0/1 fraud indicator
- `fraud_score`: Risk score (0-100)

## 🔧 Usage Examples

### Basic Usage:
```python
from universal_transaction_generator import generate_business_data

# Generate restaurant transactions
df = generate_business_data(
    business_type='local_business',
    num_transactions=1000,
    region='US',
    merchant_type='local_restaurant'
)

# Save to CSV
df.to_csv('restaurant_transactions.csv', index=False)
```

### Quick Sample Generation:
```python
# Run the simple generator
python generate_credit_card_data.py
```

### Full Dataset Generation:
```python
# Run the main generator
python universal_transaction_generator.py
```

## 📋 Recommended Kaggle Datasets for Reference

Based on research, these datasets can complement your generated data:

1. **Credit Card Fraud Detection** (MLG-ULB)
   - 284,807 transactions from European cardholders
   - Real fraud patterns but anonymized features
   - Good for benchmarking fraud detection models

2. **IEEE-CIS Fraud Detection**
   - Real-world fraud detection competition data
   - Complex feature engineering examples
   - Industry-standard fraud detection patterns

3. **Fraud Detection Handbook Simulator**
   - Academic simulator with realistic patterns
   - Customer/terminal geographic modeling
   - Time-based fraud scenarios

## 🚀 Next Steps

1. **Test Your Generated Data**: Use the sample datasets to test your fraud detection system
2. **Compare with Real Data**: Validate patterns against any real transaction data you have
3. **Iterate and Improve**: Add more merchant-specific patterns as needed
4. **Benchmark**: Compare fraud detection performance across different merchant types

## 💡 Key Advantages

- **Realistic**: Based on actual payment processing patterns
- **Scalable**: Generate any size dataset
- **Flexible**: Multiple merchant types and business scenarios
- **Fraud-Focused**: Designed specifically for fraud detection systems
- **Compliant**: No real customer data, fully synthetic
- **Immediate**: Ready to use for testing and training

Your enhanced transaction generator now produces much more realistic credit card transaction data that closely mirrors what small merchants actually process, making it ideal for training and testing fraud detection systems.
