import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_robust_transaction_data(num_transactions=5000, num_customers=800):
    """
    Generate robust credit card transaction data without fraud labels
    
    Parameters:
    - num_transactions: Total number of transactions to generate
    - num_customers: Number of unique customers
    """
    
    transactions = []
    
    # Enhanced merchant categories with more detailed transaction patterns
    merchant_categories = {
        'Grocery': {
            'amount_range': (5, 180),
            'frequency_weight': 0.20,  # 20% of all transactions
            'peak_hours': [8, 12, 17, 19],  # Morning, lunch, evening
            'merchants': ['Walmart', 'Target', 'Kroger', 'Safeway', 'Whole Foods', 'Costco', 'Publix', 'Wegmans']
        },
        'Gas Station': {
            'amount_range': (15, 120),
            'frequency_weight': 0.15,
            'peak_hours': [7, 8, 17, 18],  # Commute times
            'merchants': ['Shell', 'BP', 'Exxon', 'Chevron', 'Mobil', 'Valero', 'Sunoco', 'Marathon']
        },
        'Restaurant': {
            'amount_range': (8, 150),
            'frequency_weight': 0.18,
            'peak_hours': [12, 13, 18, 19, 20],  # Meal times
            'merchants': ['McDonald\'s', 'Starbucks', 'Subway', 'Pizza Hut', 'Olive Garden', 'Chipotle', 'Panera', 'Domino\'s']
        },
        'Online Retail': {
            'amount_range': (10, 500),
            'frequency_weight': 0.12,
            'peak_hours': [14, 15, 16, 20, 21, 22],  # Afternoon and evening
            'merchants': ['Amazon', 'eBay', 'Best Buy Online', 'Walmart.com', 'Target.com', 'Etsy', 'Wayfair', 'Zappos']
        },
        'Department Store': {
            'amount_range': (25, 350),
            'frequency_weight': 0.08,
            'peak_hours': [11, 14, 15, 16],  # Shopping hours
            'merchants': ['Macy\'s', 'JCPenney', 'Nordstrom', 'Kohl\'s', 'Dillard\'s', 'Bloomingdale\'s', 'Saks']
        },
        'Pharmacy': {
            'amount_range': (3, 75),
            'frequency_weight': 0.06,
            'peak_hours': [9, 10, 11, 16, 17],  # Medical hours
            'merchants': ['CVS', 'Walgreens', 'Rite Aid', 'Pharmacy Plus', 'Health Mart', 'Duane Reade']
        },
        'ATM': {
            'amount_range': (20, 600),
            'frequency_weight': 0.05,
            'peak_hours': [12, 17, 18, 19],  # Lunch and after work
            'merchants': ['Bank ATM', 'Credit Union ATM', 'Convenience Store ATM', 'Mall ATM', 'Gas Station ATM']
        },
        'Entertainment': {
            'amount_range': (12, 120),
            'frequency_weight': 0.04,
            'peak_hours': [19, 20, 21, 22],  # Evening entertainment
            'merchants': ['Movie Theater', 'Concert Hall', 'Sports Arena', 'Theme Park', 'Bowling Alley', 'Casino']
        },
        'Electronics': {
            'amount_range': (50, 2000),
            'frequency_weight': 0.03,
            'peak_hours': [11, 14, 15, 16],  # Shopping hours
            'merchants': ['Best Buy', 'Apple Store', 'Micro Center', 'GameStop', 'Fry\'s Electronics', 'B&H Photo']
        },
        'Hotel': {
            'amount_range': (80, 600),
            'frequency_weight': 0.02,
            'peak_hours': [15, 16, 17],  # Check-in times
            'merchants': ['Marriott', 'Hilton', 'Holiday Inn', 'Best Western', 'Hyatt', 'Sheraton', 'Doubletree']
        },
        'Healthcare': {
            'amount_range': (50, 1500),
            'frequency_weight': 0.03,
            'peak_hours': [9, 10, 11, 14, 15],  # Medical appointment hours
            'merchants': ['Medical Center', 'Dental Office', 'Urgent Care', 'Specialist Clinic', 'Lab Services']
        },
        'Transportation': {
            'amount_range': (5, 200),
            'frequency_weight': 0.04,
            'peak_hours': [7, 8, 9, 17, 18, 19],  # Commute times
            'merchants': ['Uber', 'Lyft', 'Taxi', 'Public Transit', 'Parking Garage', 'Toll Road', 'Car Rental']
        }
    }
    
    # Generate realistic customer profiles
    customers = []
    for i in range(num_customers):
        customer_profile = {
            'customer_id': f"CUST_{i+1:06d}",
            'spending_pattern': random.choice(['conservative', 'moderate', 'high_spender']),
            'preferred_categories': random.sample(list(merchant_categories.keys()), k=random.randint(3, 6)),
            'home_state': random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI', 'WA', 'AZ', 'MA', 'VA', 'NJ']),
            'card_type': random.choice(['Visa', 'Mastercard', 'American Express', 'Discover'])
        }
        customers.append(customer_profile)
    
    # Enhanced location data
    locations = {
        'CA': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'Fresno', 'Long Beach', 'Oakland', 'Bakersfield'],
        'NY': ['New York', 'Buffalo', 'Rochester', 'Yonkers', 'Syracuse', 'Albany', 'New Rochelle', 'Cheektowaga'],
        'TX': ['Houston', 'San Antonio', 'Dallas', 'Austin', 'Fort Worth', 'El Paso', 'Arlington', 'Corpus Christi'],
        'FL': ['Jacksonville', 'Miami', 'Tampa', 'Orlando', 'St. Petersburg', 'Hialeah', 'Tallahassee', 'Fort Lauderdale'],
        'IL': ['Chicago', 'Aurora', 'Peoria', 'Rockford', 'Elgin', 'Naperville', 'Schaumburg', 'Evanston'],
        'PA': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Erie', 'Reading', 'Scranton', 'Bethlehem', 'Lancaster'],
        'OH': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo', 'Akron', 'Dayton', 'Parma', 'Canton'],
        'GA': ['Atlanta', 'Columbus', 'Augusta', 'Savannah', 'Athens', 'Sandy Springs', 'Roswell', 'Macon'],
        'NC': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham', 'Winston-Salem', 'Fayetteville', 'Cary', 'Wilmington'],
        'MI': ['Detroit', 'Grand Rapids', 'Warren', 'Sterling Heights', 'Lansing', 'Ann Arbor', 'Flint', 'Dearborn'],
        'WA': ['Seattle', 'Spokane', 'Tacoma', 'Vancouver', 'Bellevue', 'Everett', 'Kent', 'Renton'],
        'AZ': ['Phoenix', 'Tucson', 'Mesa', 'Chandler', 'Scottsdale', 'Glendale', 'Gilbert', 'Tempe'],
        'MA': ['Boston', 'Worcester', 'Springfield', 'Lowell', 'Cambridge', 'New Bedford', 'Brockton', 'Quincy'],
        'VA': ['Virginia Beach', 'Norfolk', 'Chesapeake', 'Richmond', 'Newport News', 'Alexandria', 'Hampton', 'Portsmouth'],
        'NJ': ['Newark', 'Jersey City', 'Paterson', 'Elizabeth', 'Edison', 'Woodbridge', 'Lakewood', 'Toms River']
    }
    
    # Generate card numbers with realistic prefixes
    card_prefixes = {
        'Visa': ['4532', '4556', '4716', '4024', '4485', '4539', '4556', '4929'],
        'Mastercard': ['5555', '5105', '5205', '5305', '5405', '5505', '5605', '2221'],
        'American Express': ['3714', '3787', '3759', '3741', '3782', '3793'],
        'Discover': ['6011', '6500', '6501', '6502', '6503', '6504', '6505']
    }
    
    # Time period for transactions (last 12 months)
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    
    # Generate transactions
    for i in range(num_transactions):
        # Select customer
        customer = random.choice(customers)
        
        # Weight category selection by frequency and customer preferences
        available_categories = list(merchant_categories.keys())
        category_weights = [merchant_categories[cat]['frequency_weight'] * 
                           (3 if cat in customer['preferred_categories'] else 1) 
                           for cat in available_categories]
        
        # Normalize weights
        total_weight = sum(category_weights)
        category_weights = [w/total_weight for w in category_weights]
        
        # Select category
        category = np.random.choice(available_categories, p=category_weights)
        category_info = merchant_categories[category]
        
        # Generate transaction timestamp with realistic patterns
        days_offset = random.randint(0, 365)
        base_date = start_date + timedelta(days=days_offset)
        
        # Choose hour based on category peak hours (weighted)
        if random.random() < 0.6:  # 60% chance of peak hour
            hour = random.choice(category_info['peak_hours'])
        else:
            hour = random.randint(0, 23)
        
        # Add some randomness to avoid perfect patterns
        hour = max(0, min(23, hour + random.randint(-1, 1)))
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        transaction_time = base_date.replace(hour=hour, minute=minute, second=second)
        
        # Generate amount based on customer spending pattern and category
        min_amount, max_amount = category_info['amount_range']
        
        # Adjust for customer spending pattern
        if customer['spending_pattern'] == 'conservative':
            max_amount *= 0.7
        elif customer['spending_pattern'] == 'high_spender':
            max_amount *= 1.8
        
        # Generate base amount
        amount = round(random.uniform(min_amount, max_amount), 2)
        
        # Add occasional unusual amounts (could be fraud indicators)
        if random.random() < 0.02:  # 2% chance of unusual amount
            if random.random() < 0.5:
                amount = round(random.uniform(1, 5), 2)  # Very small amount
            else:
                amount = round(random.uniform(max_amount * 2, max_amount * 5), 2)  # Very large amount
        
        # Select merchant
        merchant = random.choice(category_info['merchants'])
        
        # Generate location (mostly home state, sometimes travel)
        if random.random() < 0.85:  # 85% in home state
            state = customer['home_state']
        else:  # 15% travel
            state = random.choice(list(locations.keys()))
        
        city = random.choice(locations[state])
        
        # Generate card number
        card_type = customer['card_type']
        card_prefix = random.choice(card_prefixes[card_type])
        card_number = card_prefix + ''.join([str(random.randint(0, 9)) for _ in range(12)])
        
        # Generate response codes (mostly successful)
        response_codes = {
            '00': 0.92,  # Approved
            '05': 0.02,  # Do not honor
            '14': 0.02,  # Invalid card
            '51': 0.02,  # Insufficient funds
            '61': 0.01,  # Exceeds withdrawal limit
            '62': 0.005, # Restricted card
            '65': 0.005  # Activity limit exceeded
        }
        
        response_code = np.random.choice(list(response_codes.keys()), 
                                       p=list(response_codes.values()))
        
        # Generate additional realistic fields
        terminal_id = f"TRM_{random.randint(100000, 999999)}"
        
        # Generate MCC (Merchant Category Code) - 4 digit codes
        mcc_codes = {
            'Grocery': random.choice(['5411', '5499']),
            'Gas Station': random.choice(['5541', '5542']),
            'Restaurant': random.choice(['5812', '5814']),
            'Online Retail': random.choice(['5999', '5969']),
            'Department Store': random.choice(['5311', '5399']),
            'Pharmacy': random.choice(['5912', '5122']),
            'ATM': random.choice(['6011', '6012']),
            'Entertainment': random.choice(['7832', '7841']),
            'Electronics': random.choice(['5732', '5045']),
            'Hotel': random.choice(['7011', '3501']),
            'Healthcare': random.choice(['8011', '8021']),
            'Transportation': random.choice(['4111', '4121'])
        }
        
        mcc = mcc_codes[category]
        
        # Create transaction record
        transaction = {
            'transaction_id': f"TXN_{i+1:08d}",
            'customer_id': customer['customer_id'],
            'card_number_last4': card_number[-4:],
            'card_type': card_type,
            'transaction_date': transaction_time.strftime('%Y-%m-%d'),
            'transaction_time': transaction_time.strftime('%H:%M:%S'),
            'amount': amount,
            'merchant_name': merchant,
            'merchant_category': category,
            'merchant_category_code': mcc,
            'city': city,
            'state': state,
            'terminal_id': terminal_id,
            'response_code': response_code,
            'spending_pattern': customer['spending_pattern']
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

def generate_multiple_datasets():
    """Generate multiple datasets for different scenarios"""
    
    # Create transaction_files directory if it doesn't exist
    output_dir = 'transaction_files'
    os.makedirs(output_dir, exist_ok=True)
    
    datasets = {
        'small_dataset': {'transactions': 1000, 'customers': 200},
        'medium_dataset': {'transactions': 5000, 'customers': 800},
        'large_dataset': {'transactions': 10000, 'customers': 1500}
    }
    
    for dataset_name, params in datasets.items():
        print(f"\nGenerating {dataset_name}...")
        df = generate_robust_transaction_data(
            num_transactions=params['transactions'],
            num_customers=params['customers']
        )
        
        # Save to CSV
        filename = os.path.join(output_dir, f'{dataset_name}.csv')
        df.to_csv(filename, index=False)
        
        print(f"Dataset Summary for {dataset_name}:")
        print(f"  Total transactions: {len(df):,}")
        print(f"  Unique customers: {df['customer_id'].nunique():,}")
        print(f"  Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
        print(f"  Average transaction amount: ${df['amount'].mean():.2f}")
        print(f"  Merchant categories: {df['merchant_category'].nunique()}")
        print(f"  Response codes: {df['response_code'].value_counts().to_dict()}")
        print(f"  Saved to: {filename}")

# Generate the datasets
if __name__ == "__main__":
    print("Generating robust credit card transaction datasets...")
    generate_multiple_datasets()
    
    print("\n" + "="*50)
    print("DATASET GENERATION COMPLETE")
    print("="*50)
    
    # Show sample data structure
    print("\nSample data structure:")
    sample_df = generate_robust_transaction_data(num_transactions=5, num_customers=3)
    print(sample_df.to_string(index=False))
    
    print("\nColumn descriptions:")
    column_descriptions = {
        'transaction_id': 'Unique transaction identifier',
        'customer_id': 'Unique customer identifier',
        'card_number_last4': 'Last 4 digits of card number',
        'card_type': 'Type of credit card (Visa, Mastercard, etc.)',
        'transaction_date': 'Date of transaction (YYYY-MM-DD)',
        'transaction_time': 'Time of transaction (HH:MM:SS)',
        'amount': 'Transaction amount in USD',
        'merchant_name': 'Name of merchant',
        'merchant_category': 'Category of merchant',
        'merchant_category_code': 'MCC code for merchant category',
        'city': 'City where transaction occurred',
        'state': 'State where transaction occurred',
        'terminal_id': 'Terminal identifier',
        'response_code': 'Transaction response code',
        'spending_pattern': 'Customer spending pattern classification'
    }
    
    for column, description in column_descriptions.items():
        print(f"  {column}: {description}")