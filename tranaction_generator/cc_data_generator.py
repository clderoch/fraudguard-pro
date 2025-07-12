import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_credit_card_data(num_transactions=1000, fraud_rate=0.05):
    """
    Generate synthetic credit card transaction data with fraudulent transactions
    
    Parameters:
    - num_transactions: Total number of transactions to generate
    - fraud_rate: Percentage of transactions that should be fraudulent (0.05 = 5%)
    """
    
    # Generate basic transaction data
    transactions = []
    
    # Define merchant categories and their typical transaction ranges
    merchant_categories = {
        'Grocery': (10, 150),
        'Gas Station': (20, 80),
        'Restaurant': (15, 120),
        'Online Retail': (25, 300),
        'Department Store': (30, 250),
        'Pharmacy': (5, 60),
        'ATM': (20, 500),
        'Hotel': (80, 400),
        'Entertainment': (10, 100),
        'Electronics': (50, 1200)
    }
    
    # Common merchant names for each category
    merchants = {
        'Grocery': ['Walmart', 'Target', 'Kroger', 'Safeway', 'Whole Foods'],
        'Gas Station': ['Shell', 'BP', 'Exxon', 'Chevron', 'Mobil'],
        'Restaurant': ['McDonald\'s', 'Starbucks', 'Subway', 'Pizza Hut', 'Olive Garden'],
        'Online Retail': ['Amazon', 'eBay', 'Best Buy Online', 'Walmart.com', 'Target.com'],
        'Department Store': ['Macy\'s', 'JCPenney', 'Nordstrom', 'Kohl\'s', 'Sears'],
        'Pharmacy': ['CVS', 'Walgreens', 'Rite Aid', 'Pharmacy Plus', 'Health Mart'],
        'ATM': ['Bank ATM', 'Credit Union ATM', 'Convenience Store ATM', 'Mall ATM', 'Gas Station ATM'],
        'Hotel': ['Marriott', 'Hilton', 'Holiday Inn', 'Best Western', 'Hyatt'],
        'Entertainment': ['Movie Theater', 'Concert Hall', 'Sports Arena', 'Theme Park', 'Bowling Alley'],
        'Electronics': ['Best Buy', 'Circuit City', 'Fry\'s Electronics', 'Micro Center', 'RadioShack']
    }
    
    # Generate customer IDs
    customer_ids = [f"CUST_{i:06d}" for i in range(1, 501)]  # 500 unique customers
    
    # Generate card numbers (fake, for demo purposes)
    card_prefixes = ['4532', '5555', '4716', '4024', '4485']  # Common card prefixes
    
    # Start date for transactions (last 6 months)
    start_date = datetime.now() - timedelta(days=180)
    
    num_fraudulent = int(num_transactions * fraud_rate)
    
    for i in range(num_transactions):
        # Determine if this transaction is fraudulent
        is_fraud = i < num_fraudulent
        
        # Generate transaction timestamp
        days_offset = random.randint(0, 180)
        hours_offset = random.randint(0, 23)
        minutes_offset = random.randint(0, 59)
        transaction_time = start_date + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)
        
        # Select customer
        customer_id = random.choice(customer_ids)
        
        # Generate card number
        card_prefix = random.choice(card_prefixes)
        card_number = card_prefix + ''.join([str(random.randint(0, 9)) for _ in range(12)])
        
        # Select merchant category and merchant
        category = random.choice(list(merchant_categories.keys()))
        merchant = random.choice(merchants[category])
        
        # Generate transaction amount based on fraud status
        if is_fraud:
            # Fraudulent transactions tend to be either very small (testing) or very large (maximize theft)
            if random.random() < 0.3:  # 30% chance of small fraud (card testing)
                amount = round(random.uniform(1, 10), 2)
            else:  # 70% chance of large fraud
                amount = round(random.uniform(500, 2000), 2)
        else:
            # Normal transactions within typical ranges for category
            min_amount, max_amount = merchant_categories[category]
            amount = round(random.uniform(min_amount, max_amount), 2)
        
        # Generate location data
        states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
        cities = {
            'CA': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento'],
            'NY': ['New York', 'Buffalo', 'Rochester', 'Syracuse'],
            'TX': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
            'FL': ['Miami', 'Tampa', 'Orlando', 'Jacksonville'],
            'IL': ['Chicago', 'Springfield', 'Peoria', 'Rockford'],
            'PA': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Erie'],
            'OH': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo'],
            'GA': ['Atlanta', 'Savannah', 'Augusta', 'Columbus'],
            'NC': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham'],
            'MI': ['Detroit', 'Grand Rapids', 'Warren', 'Sterling Heights']
        }
        
        state = random.choice(states)
        city = random.choice(cities[state])
        
        # For fraudulent transactions, sometimes use unusual locations
        if is_fraud and random.random() < 0.4:  # 40% of fraud from unusual locations
            unusual_states = ['AK', 'HI', 'MT', 'WY', 'VT']
            state = random.choice(unusual_states)
            city = f"Remote_{state}"
        
        # Generate additional fraud indicators
        if is_fraud:
            # Fraudulent transactions more likely to be declined initially
            response_code = random.choice(['00', '05', '14', '51', '61'])  # Mix of approved and declined
            # Unusual times (late night/early morning more common for fraud)
            if random.random() < 0.6:
                transaction_time = transaction_time.replace(hour=random.randint(0, 5))
        else:
            response_code = '00'  # Approved
        
        # Create transaction record
        transaction = {
            'transaction_id': f"TXN_{i+1:08d}",
            'customer_id': customer_id,
            'card_number': card_number[-4:],  # Only last 4 digits for privacy
            'transaction_date': transaction_time.strftime('%Y-%m-%d'),
            'transaction_time': transaction_time.strftime('%H:%M:%S'),
            'amount': amount,
            'merchant_name': merchant,
            'merchant_category': category,
            'city': city,
            'state': state,
            'response_code': response_code,
            'is_fraud': 1 if is_fraud else 0
        }
        
        transactions.append(transaction)
    
    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    
    # Sort by transaction date and time
    df['datetime'] = pd.to_datetime(df['transaction_date'] + ' ' + df['transaction_time'])
    df = df.sort_values('datetime').drop('datetime', axis=1)
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

# Generate the sample data
print("Generating credit card transaction data...")
df = generate_credit_card_data(num_transactions=1000, fraud_rate=0.05)

# Display summary statistics
print(f"\nDataset Summary:")
print(f"Total transactions: {len(df)}")
print(f"Fraudulent transactions: {df['is_fraud'].sum()}")
print(f"Fraud rate: {df['is_fraud'].mean():.2%}")
print(f"Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")

# Display first few rows
print(f"\nFirst 5 rows:")
print(df.head())

# Display fraud distribution by category
print(f"\nFraud distribution by merchant category:")
fraud_by_category = df.groupby('merchant_category')['is_fraud'].agg(['count', 'sum', 'mean'])
fraud_by_category.columns = ['total_transactions', 'fraud_count', 'fraud_rate']
fraud_by_category['fraud_rate'] = fraud_by_category['fraud_rate'].apply(lambda x: f"{x:.2%}")
print(fraud_by_category.sort_values('fraud_count', ascending=False))

# Create transaction_files directory if it doesn't exist
output_dir = 'transaction_files'
os.makedirs(output_dir, exist_ok=True)

# Save to CSV in the transaction_files folder
output_filename = os.path.join(output_dir, 'credit_card_transactions.csv')
df.to_csv(output_filename, index=False)
print(f"\nData saved to {output_filename}")

# Display sample of fraudulent transactions
print(f"\nSample fraudulent transactions:")
fraud_sample = df[df['is_fraud'] == 1].head(3)
print(fraud_sample[['transaction_id', 'amount', 'merchant_name', 'merchant_category', 'city', 'state']])

# Display data types and basic info
print(f"\nData types:")
print(df.dtypes)