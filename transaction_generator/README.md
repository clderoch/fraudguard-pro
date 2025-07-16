# Universal Transaction Data Generator

A comprehensive Python script that generates realistic transaction data for **any business type** across **all major industry verticals**. Designed specifically for testing fraud detection systems with real-world transaction patterns.

## 🎯 Key Features

### ✅ **100+ Business Types Supported**
- **Technology & Software**: SaaS, Cybersecurity, Cloud Services
- **E-commerce & Retail**: Fashion, Electronics, Home Goods
- **Healthcare & Medical**: Telehealth, Pharmacy, Medical Devices
- **Financial Services**: Fintech, Crypto, Investment Platforms
- **Education & Learning**: Online Courses, Tutoring, Certification
- **Entertainment & Media**: Streaming, Gaming, Music
- **Travel & Hospitality**: Booking Platforms, Hotels, Airlines
- **Food & Restaurant**: Delivery, POS Systems, Meal Kits
- **Professional Services**: Legal, Accounting, Consulting
- **Automotive & Transportation**: Ride Sharing, Auto Parts
- **Non-Profit & Social Impact**: Donations, Crowdfunding

### ✅ **Realistic Data Generation**
- **Customer Profiles**: Behavioral segmentation, CLV, acquisition channels
- **Transaction Patterns**: Business hours, seasonality, peak times
- **Payment Processing**: Multiple payment methods, success/failure rates
- **Geographic Diversity**: Global support with regional preferences
- **Device Intelligence**: Mobile, desktop, tablet usage patterns
- **Fraud Indicators**: Sophisticated anomaly generation for testing

### ✅ **Industry-Specific Patterns**
- **Subscription Models**: Tiered pricing, billing cycles, churn
- **E-commerce**: Cart abandonment, returns, seasonal sales
- **Financial**: Trading fees, regulatory compliance, KYC
- **Healthcare**: Insurance coverage, appointment types, prescriptions
- **B2B Services**: Enterprise contracts, professional billing

## 🚀 Quick Start

### Basic Usage

```python
from universal_transaction_generator import generate_business_data

# Generate 5000 transactions for a SaaS business
df = generate_business_data('saas_b2b', num_transactions=5000, region='US')

# Save to CSV
df.to_csv('saas_transactions.csv', index=False)

# View summary
print(f"Generated {len(df)} transactions")
print(f"Fraud rate: {df['is_fraudulent'].mean()*100:.2f}%")
print(f"Average transaction: ${df['amount'].mean():.2f}")
```

### Generate Multiple Industries

```python
# Generate data for different industries
business_types = [
    'saas_b2b',           # Technology
    'fashion_ecommerce',   # Retail  
    'telehealth_platform', # Healthcare
    'crypto_exchange',     # Finance
    'food_delivery',       # Food Service
    'travel_booking'       # Travel
]

for business_type in business_types:
    df = generate_business_data(business_type, 3000, 'US')
    df.to_csv(f'{business_type}_transactions.csv', index=False)
```

### International Data

```python
# Generate data for different regions
regions = ['US', 'CA', 'GB', 'DE', 'JP', 'AU']

for region in regions:
    df = generate_business_data('streaming_service', 2000, region)
    df.to_csv(f'streaming_{region}_transactions.csv', index=False)
```

## 📊 Generated Data Schema

### Core Transaction Fields
| Field | Description | Example |
|-------|-------------|---------|
| `transaction_id` | Unique transaction identifier | `TXN_20250716_00001234` |
| `customer_id` | Unique customer identifier | `CUST_87654321` |
| `transaction_datetime` | ISO timestamp | `2025-01-15 14:30:45` |
| `amount` | Transaction amount | `149.99` |
| `payment_status` | Success/failure status | `completed` |
| `merchant_name` | Business name | `CloudSync Enterprise` |
| `merchant_category` | Business category | `B2B SaaS Platform` |

### Customer Information
| Field | Description | Example |
|-------|-------------|---------|
| `customer_name` | Customer full name | `John Smith` |
| `customer_email` | Email address | `john.smith@example.com` |
| `customer_segment` | Customer type | `enterprise` |
| `customer_lifetime_value` | CLV prediction | `25000.00` |
| `customer_acquisition_channel` | Marketing channel | `paid_search` |

### Fraud Detection Fields
| Field | Description | Example |
|-------|-------------|---------|
| `is_fraudulent` | Fraud flag (boolean) | `false` |
| `risk_score` | Risk score (0-100) | `23.5` |
| `fraud_indicators` | Comma-separated flags | `geo_mismatch,round_amount` |
| `fraud_type` | Type of fraud if detected | `card_testing` |

### Business Intelligence
| Field | Description | Example |
|-------|-------------|---------|
| `device_type` | Customer device | `mobile_ios` |
| `is_mobile` | Mobile transaction flag | `true` |
| `timezone` | Customer timezone | `EST` |
| `language` | Customer language | `en` |
| `quarter` | Business quarter | `Q1` |
| `is_weekend` | Weekend transaction | `false` |

## 🏭 Supported Business Types

### Technology & Software
```python
business_types = [
    'saas_b2b',
    'saas_b2c', 
    'cybersecurity_platform',
    'cloud_hosting',
    'ai_platform',
    'api_service'
]
```

### E-commerce & Retail
```python
business_types = [
    'fashion_ecommerce',
    'electronics_store',
    'home_goods',
    'beauty_cosmetics',
    'sporting_goods',
    'jewelry_store'
]
```

### Healthcare & Medical
```python
business_types = [
    'telehealth_platform',
    'pharmacy_online',
    'medical_devices',
    'mental_health',
    'dental_practice',
    'veterinary_services'
]
```

### Financial Services
```python
business_types = [
    'fintech_payment_app',
    'crypto_exchange',
    'investment_platform',
    'insurance_online',
    'mortgage_broker',
    'tax_preparation'
]
```

## 🎨 Customization Options

### Custom Business Pattern
```python
from universal_transaction_generator import UniversalTransactionGenerator

generator = UniversalTransactionGenerator()

# The generator automatically creates patterns for unknown business types
df = generator.generate_transaction_data(
    num_transactions=1000,
    business_type='your_custom_business',
    region='US'
)
```

### Advanced Configuration
```python
# Configure specific parameters
generator = UniversalTransactionGenerator()

# Modify currency rates
generator.currency_rates['EUR'] = 0.88

# Add custom marketing channels
generator.marketing_channels['podcast_ads'] = {
    'weight': 0.03, 
    'cost_per_acquisition': (15, 35)
}

# Generate with custom settings
df = generator.generate_transaction_data(5000, 'saas_b2b')
```

## 🧪 Testing & Validation

### Run Demo Script
```bash
python demo_generator.py
```

This generates sample data for multiple industries and shows:
- Single business type generation
- Multi-industry comparison
- Fraud pattern analysis
- International data generation
- Custom business type handling

### Fraud Detection Testing
```python
# Generate data with higher fraud rates for testing
df = generate_business_data('crypto_exchange', 3000, 'US')

# Analyze fraud patterns
fraud_df = df[df['is_fraudulent'] == True]
print(f"Fraud rate: {len(fraud_df)/len(df)*100:.2f}%")

# Common fraud indicators
fraud_indicators = df[df['is_fraudulent']]['fraud_indicators'].value_counts()
print("Top fraud indicators:")
print(fraud_indicators.head())
```

## 📈 Use Cases

### 1. Fraud Detection Dashboard Testing
```python
# Generate comprehensive test data
industries = ['saas_b2b', 'ecommerce', 'fintech', 'healthcare']
test_data = []

for industry in industries:
    df = generate_business_data(industry, 2000, 'US')
    test_data.append(df)

combined_df = pd.concat(test_data, ignore_index=True)
combined_df.to_csv('fraud_detection_test_data.csv', index=False)
```

### 2. Performance Testing
```python
# Generate large datasets for performance testing
large_df = generate_business_data('payment_processor', 50000, 'US')
large_df.to_csv('performance_test_data.csv', index=False)
```

### 3. Machine Learning Training
```python
# Generate balanced dataset for ML training
df = generate_business_data('crypto_exchange', 10000, 'US')

# Split features and labels
features = df.drop(['is_fraudulent', 'fraud_type'], axis=1)
labels = df['is_fraudulent']

# Use for training fraud detection models
```

## 🔧 Requirements

```python
# Core dependencies
pandas>=1.3.0
numpy>=1.20.0

# Optional for demo visualizations
matplotlib>=3.3.0
seaborn>=0.11.0
```

## 📝 Output Files

The generator creates CSV files with the following naming convention:
- `{business_type}_transactions.csv` - Main transaction data
- `demo_*.csv` - Demo script outputs
- `{region}_{business_type}_transactions.csv` - Regional data

## 🌟 Key Improvements Over Original

1. **Universal Coverage**: Supports 100+ business types vs. limited set
2. **Industry Expertise**: Deep patterns for each vertical vs. generic
3. **Global Support**: Multi-region, multi-currency, multi-language
4. **Enhanced Fraud**: Sophisticated anomaly patterns for testing
5. **Better Realism**: Industry-specific customer behavior and transactions
6. **Comprehensive Schema**: 40+ fields vs. basic set
7. **Easy Integration**: Simple API for any business type
8. **Production Ready**: Error handling, validation, performance optimized

## 🤝 Contributing

To add new business types:

1. Add pattern to `get_comprehensive_business_patterns()`
2. Implement specific generation logic if needed
3. Test with demo script
4. Update documentation

## 📄 License

MIT License - Feel free to use for commercial fraud detection systems.

---

**Perfect for:** Fraud detection dashboards, ML model training, performance testing, business intelligence, compliance testing, and any application requiring realistic transaction data across multiple industries.
