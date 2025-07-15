# Complete SMB Transaction Data Generator with Fraud Detection
# Save as: smb_transaction_generator_complete.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from faker import Faker
from faker.providers import credit_card, person, company, address

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Initialize Faker
fake = Faker('en_US')
fake.add_provider(credit_card)
fake.add_provider(person)
fake.add_provider(company)
fake.add_provider(address)

def generate_smb_transaction_data(num_transactions=2000, business_type='restaurant'):
    """
    Generate realistic transaction data for small businesses with fraud patterns
    
    Parameters:
    - num_transactions: Total number of transactions to generate
    - business_type: Type of business (see business_patterns for available types)
    """
    
    # Define business-specific patterns
    business_patterns = {
        # PHYSICAL BUSINESSES
        'restaurant': {
            'name': 'Tony\'s Italian Bistro',
            'category': 'Restaurant',
            'amount_ranges': {
                'appetizer': (8, 18),
                'entree': (15, 35),
                'dessert': (6, 12),
                'beverage': (3, 8),
                'full_meal': (25, 85),
                'group_dining': (120, 350),
                'catering': (200, 800)
            },
            'peak_hours': [11, 12, 13, 17, 18, 19, 20],
            'peak_days': [4, 5, 6],
            'seasonal_multiplier': {'winter': 0.8, 'spring': 1.0, 'summer': 1.2, 'fall': 1.1},
            'payment_methods': ['Visa', 'Mastercard', 'American Express', 'Discover', 'Cash', 'Mobile Payment']
        },
        'retail': {
            'name': 'Sarah\'s Boutique',
            'category': 'Retail',
            'amount_ranges': {
                'accessory': (10, 45),
                'clothing': (35, 150),
                'shoes': (60, 200),
                'sale_item': (15, 80),
                'regular_purchase': (40, 120),
                'bulk_purchase': (150, 400),
                'gift_card': (25, 100)
            },
            'peak_hours': [11, 12, 13, 14, 15, 16, 18, 19],
            'peak_days': [5, 6],
            'seasonal_multiplier': {'winter': 1.3, 'spring': 1.0, 'summer': 0.9, 'fall': 1.2},
            'payment_methods': ['Visa', 'Mastercard', 'American Express', 'Discover', 'Mobile Payment']
        },
        'service': {
            'name': 'Mike\'s Auto Repair',
            'category': 'Automotive Service',
            'amount_ranges': {
                'oil_change': (35, 65),
                'tire_service': (80, 400),
                'brake_service': (150, 600),
                'major_repair': (300, 1500),
                'inspection': (25, 45),
                'diagnostic': (100, 200),
                'emergency_service': (200, 800)
            },
            'peak_hours': [8, 9, 10, 11, 14, 15, 16],
            'peak_days': [0, 1, 2, 3, 4],
            'seasonal_multiplier': {'winter': 1.2, 'spring': 1.1, 'summer': 1.0, 'fall': 1.1},
            'payment_methods': ['Visa', 'Mastercard', 'American Express', 'Cash', 'Check']
        },
        'healthcare': {
            'name': 'Downtown Dental Clinic',
            'category': 'Healthcare',
            'amount_ranges': {
                'cleaning': (80, 150),
                'filling': (120, 300),
                'crown': (800, 1500),
                'extraction': (150, 400),
                'consultation': (50, 120),
                'emergency': (200, 600),
                'cosmetic': (500, 2000)
            },
            'peak_hours': [9, 10, 11, 14, 15, 16],
            'peak_days': [0, 1, 2, 3, 4],
            'seasonal_multiplier': {'winter': 1.1, 'spring': 1.0, 'summer': 0.9, 'fall': 1.0},
            'payment_methods': ['Visa', 'Mastercard', 'American Express', 'Care Credit', 'Cash']
        },
        'coffee_shop': {
            'name': 'Bean There Coffee',
            'category': 'Coffee Shop',
            'amount_ranges': {
                'coffee': (3, 8),
                'pastry': (2, 6),
                'sandwich': (7, 12),
                'specialty_drink': (5, 10),
                'combo_meal': (8, 15),
                'group_order': (25, 60),
                'catering': (50, 200)
            },
            'peak_hours': [7, 8, 9, 12, 13, 15, 16],
            'peak_days': [0, 1, 2, 3, 4],
            'seasonal_multiplier': {'winter': 1.2, 'spring': 1.0, 'summer': 0.8, 'fall': 1.1},
            'payment_methods': ['Visa', 'Mastercard', 'Mobile Payment', 'Cash', 'Gift Card']
        },
        
        # E-COMMERCE BUSINESSES
        'handmade_crafts': {
            'name': 'Artisan Crafts Online',
            'category': 'E-commerce - Handmade',
            'amount_ranges': {
                'small_item': (15, 35),
                'jewelry': (25, 120),
                'home_decor': (40, 180),
                'custom_order': (60, 300),
                'gift_set': (80, 200),
                'seasonal_item': (30, 150),
                'workshop_kit': (45, 85)
            },
            'peak_hours': [10, 11, 14, 15, 19, 20, 21],
            'peak_days': [0, 1, 6],
            'seasonal_multiplier': {'winter': 1.4, 'spring': 1.1, 'summer': 0.9, 'fall': 1.3},
            'payment_methods': ['Visa', 'Mastercard', 'PayPal', 'Apple Pay', 'Google Pay', 'Shop Pay'],
            'shipping_methods': ['Standard', 'Expedited', 'Express', 'International'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'FR', 'IT', 'ES', 'NL', 'SE']
        },
        'fitness_supplements': {
            'name': 'Peak Performance Nutrition',
            'category': 'E-commerce - Health & Fitness',
            'amount_ranges': {
                'protein_powder': (25, 80),
                'vitamins': (15, 45),
                'pre_workout': (30, 60),
                'meal_replacement': (35, 70),
                'bulk_order': (100, 400),
                'subscription': (40, 120),
                'starter_kit': (80, 200)
            },
            'peak_hours': [6, 7, 8, 12, 13, 17, 18, 22],
            'peak_days': [0, 1, 6],
            'seasonal_multiplier': {'winter': 0.9, 'spring': 1.3, 'summer': 1.2, 'fall': 1.0},
            'payment_methods': ['Visa', 'Mastercard', 'American Express', 'PayPal', 'Apple Pay', 'Klarna'],
            'shipping_methods': ['Standard', 'Expedited', 'Express', 'Subscription'],
            'countries': ['US', 'CA', 'UK', 'AU', 'NZ']
        },
        'tech_accessories': {
            'name': 'TechGear Direct',
            'category': 'E-commerce - Electronics',
            'amount_ranges': {
                'phone_case': (12, 35),
                'charging_cable': (8, 25),
                'screen_protector': (10, 30),
                'wireless_charger': (25, 80),
                'phone_mount': (15, 45),
                'bundle_deal': (40, 120),
                'premium_accessory': (60, 200)
            },
            'peak_hours': [9, 10, 12, 13, 14, 19, 20, 21],
            'peak_days': [1, 2, 3, 4],
            'seasonal_multiplier': {'winter': 1.2, 'spring': 1.0, 'summer': 0.9, 'fall': 1.1},
            'payment_methods': ['Visa', 'Mastercard', 'American Express', 'PayPal', 'Apple Pay', 'Google Pay', 'Amazon Pay'],
            'shipping_methods': ['Standard', 'Expedited', 'Express', 'Same Day'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'FR', 'JP', 'KR']
        },
        'pet_supplies': {
            'name': 'Happy Paws Pet Store',
            'category': 'E-commerce - Pet Supplies',
            'amount_ranges': {
                'dog_toy': (8, 25),
                'cat_toy': (5, 20),
                'pet_food': (20, 80),
                'pet_treats': (10, 30),
                'grooming_supplies': (15, 60),
                'pet_bed': (30, 120),
                'bulk_food_order': (80, 300),
                'subscription_box': (25, 60)
            },
            'peak_hours': [8, 9, 12, 13, 18, 19, 20],
            'peak_days': [5, 6],
            'seasonal_multiplier': {'winter': 1.0, 'spring': 1.1, 'summer': 1.2, 'fall': 1.0},
            'payment_methods': ['Visa', 'Mastercard', 'Discover', 'PayPal', 'Apple Pay', 'Chewy Pay'],
            'shipping_methods': ['Standard', 'Expedited', 'Subscription', 'Auto-Ship'],
            'countries': ['US', 'CA', 'UK', 'AU']
        },
        'vintage_clothing': {
            'name': 'Retro Revival Vintage',
            'category': 'E-commerce - Vintage Fashion',
            'amount_ranges': {
                'vintage_tshirt': (20, 60),
                'vintage_dress': (45, 180),
                'vintage_jacket': (60, 250),
                'vintage_jeans': (35, 120),
                'accessories': (15, 80),
                'rare_item': (100, 500),
                'bundle_deal': (80, 300)
            },
            'peak_hours': [11, 12, 14, 15, 16, 19, 20, 21],
            'peak_days': [4, 5, 6],
            'seasonal_multiplier': {'winter': 1.1, 'spring': 1.3, 'summer': 0.8, 'fall': 1.2},
            'payment_methods': ['Visa', 'Mastercard', 'PayPal', 'Apple Pay', 'Klarna', 'Afterpay'],
            'shipping_methods': ['Standard', 'Expedited', 'Express', 'International'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'FR', 'IT', 'ES', 'JP']
        },
        
        # NEW E-COMMERCE BUSINESSES
        'beauty_cosmetics': {
            'name': 'Glow Beauty Co',
            'category': 'E-commerce - Beauty & Cosmetics',
            'amount_ranges': {
                'lipstick': (12, 35),
                'foundation': (25, 60),
                'skincare_item': (20, 80),
                'makeup_palette': (30, 100),
                'luxury_item': (80, 250),
                'beauty_set': (60, 200),
                'sample_kit': (15, 40),
                'subscription_box': (25, 50)
            },
            'peak_hours': [10, 11, 12, 15, 16, 19, 20, 21],
            'peak_days': [4, 5, 6],
            'seasonal_multiplier': {'winter': 1.2, 'spring': 1.3, 'summer': 1.1, 'fall': 1.0},
            'payment_methods': ['Visa', 'Mastercard', 'PayPal', 'Apple Pay', 'Klarna', 'Afterpay', 'Sezzle'],
            'shipping_methods': ['Standard', 'Expedited', 'Express', 'International', 'Subscription'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'FR', 'IT', 'ES', 'NL', 'SE', 'JP', 'KR']
        },
        'home_garden': {
            'name': 'Green Thumb Gardens',
            'category': 'E-commerce - Home & Garden',
            'amount_ranges': {
                'seeds': (5, 20),
                'small_plant': (15, 45),
                'garden_tool': (20, 80),
                'fertilizer': (12, 35),
                'large_plant': (40, 150),
                'garden_kit': (60, 200),
                'bulk_order': (100, 400),
                'seasonal_package': (80, 300)
            },
            'peak_hours': [9, 10, 11, 14, 15, 16, 19, 20],
            'peak_days': [5, 6],
            'seasonal_multiplier': {'winter': 0.6, 'spring': 1.8, 'summer': 1.4, 'fall': 1.0},
            'payment_methods': ['Visa', 'Mastercard', 'Discover', 'PayPal', 'Apple Pay', 'Google Pay'],
            'shipping_methods': ['Standard', 'Expedited', 'Express', 'Heavy Item', 'Local Delivery'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'NL']
        },
        'book_media': {
            'name': 'Digital Bookshelf',
            'category': 'E-commerce - Books & Media',
            'amount_ranges': {
                'ebook': (5, 25),
                'paperback': (8, 20),
                'hardcover': (15, 40),
                'audiobook': (10, 30),
                'book_bundle': (25, 80),
                'rare_book': (50, 300),
                'digital_course': (30, 150),
                'subscription': (15, 40)
            },
            'peak_hours': [12, 13, 17, 18, 19, 20, 21, 22],
            'peak_days': [0, 6],
            'seasonal_multiplier': {'winter': 1.3, 'spring': 1.0, 'summer': 0.8, 'fall': 1.2},
            'payment_methods': ['Visa', 'Mastercard', 'PayPal', 'Apple Pay', 'Google Pay', 'Amazon Pay'],
            'shipping_methods': ['Standard', 'Expedited', 'Digital Download', 'International'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'FR', 'IT', 'ES', 'NL', 'SE', 'JP', 'IN']
        },
        'art_supplies': {
            'name': 'Creative Canvas Studio',
            'category': 'E-commerce - Art Supplies',
            'amount_ranges': {
                'basic_supplies': (8, 30),
                'paint_set': (15, 60),
                'canvas': (10, 40),
                'brush_set': (20, 80),
                'professional_kit': (80, 250),
                'digital_tablet': (100, 600),
                'bulk_supplies': (60, 300),
                'custom_order': (50, 200)
            },
            'peak_hours': [10, 11, 14, 15, 16, 19, 20, 21],
            'peak_days': [5, 6],
            'seasonal_multiplier': {'winter': 1.1, 'spring': 1.2, 'summer': 1.0, 'fall': 1.3},
            'payment_methods': ['Visa', 'Mastercard', 'American Express', 'PayPal', 'Apple Pay', 'Klarna'],
            'shipping_methods': ['Standard', 'Expedited', 'Express', 'Heavy Item', 'International'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'FR', 'IT', 'ES', 'NL', 'JP']
        },
        'baby_kids': {
            'name': 'Little Angels Baby Store',
            'category': 'E-commerce - Baby & Kids',
            'amount_ranges': {
                'baby_clothes': (15, 50),
                'toy': (10, 40),
                'baby_food': (20, 60),
                'diaper_bundle': (30, 80),
                'stroller': (100, 500),
                'car_seat': (80, 400),
                'bulk_supplies': (60, 200),
                'subscription_box': (25, 60)
            },
            'peak_hours': [9, 10, 11, 13, 14, 19, 20, 21],
            'peak_days': [0, 6],
            'seasonal_multiplier': {'winter': 1.1, 'spring': 1.2, 'summer': 1.0, 'fall': 1.1},
            'payment_methods': ['Visa', 'Mastercard', 'Discover', 'PayPal', 'Apple Pay', 'Target RedCard'],
            'shipping_methods': ['Standard', 'Expedited', 'Express', 'Subscription', 'Heavy Item'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'FR']
        },
        'digital_downloads': {
            'name': 'PixelPerfect Digital',
            'category': 'E-commerce - Digital Products',
            'amount_ranges': {
                'stock_photo': (2, 15),
                'digital_template': (5, 25),
                'software_license': (20, 100),
                'online_course': (30, 200),
                'premium_bundle': (50, 300),
                'subscription_monthly': (15, 50),
                'enterprise_license': (100, 1000),
                'custom_design': (80, 500)
            },
            'peak_hours': [9, 10, 11, 13, 14, 15, 19, 20, 21],
            'peak_days': [1, 2, 3, 4],
            'seasonal_multiplier': {'winter': 1.0, 'spring': 1.1, 'summer': 0.9, 'fall': 1.2},
            'payment_methods': ['Visa', 'Mastercard', 'PayPal', 'Apple Pay', 'Google Pay', 'Stripe'],
            'shipping_methods': ['Digital Download', 'Email Delivery', 'Cloud Access'],
            'countries': ['US', 'CA', 'UK', 'AU', 'DE', 'FR', 'IT', 'ES', 'NL', 'SE', 'JP', 'KR', 'IN', 'BR']
        }
    }
    
    pattern = business_patterns[business_type]
    transactions = []
    
    # Generate customer pool
    regular_customers = []
    for _ in range(min(200, num_transactions // 5)):
        customer = {
            'customer_id': f"CUST_{fake.random_number(digits=6, fix_len=True)}",
            'name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'is_regular': True,
            'visit_frequency': random.choice(['weekly', 'bi-weekly', 'monthly']),
            'preferred_payment': random.choice(pattern['payment_methods']),
            'avg_spending': random.uniform(30, 200)
        }
        regular_customers.append(customer)
    
    # Time period for transactions
    start_date = datetime.now() - timedelta(days=180)
    end_date = datetime.now()
    
    # Generate transactions
    for i in range(num_transactions):
        # Select customer
        if regular_customers and random.random() < 0.6:
            customer = random.choice(regular_customers)
            is_new_customer = False
        else:
            customer = {
                'customer_id': f"CUST_{fake.random_number(digits=6, fix_len=True)}",
                'name': fake.name(),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'is_regular': False,
                'preferred_payment': random.choice(pattern['payment_methods']),
                'avg_spending': random.uniform(20, 150)
            }
            is_new_customer = True
        
        # Generate realistic transaction timing
        days_offset = random.randint(0, 180)
        base_date = start_date + timedelta(days=days_offset)
        
        # Apply day-of-week patterns
        day_of_week = base_date.weekday()
        if day_of_week in pattern['peak_days']:
            hour_weight = 1.5
        else:
            hour_weight = 0.8
        
        # Choose hour based on business peak hours
        if random.random() < 0.7 * hour_weight:
            hour = random.choice(pattern['peak_hours'])
        else:
            if business_type in ['restaurant', 'coffee_shop']:
                hour = random.choice(range(6, 23))
            else:
                hour = random.choice(range(8, 18))
        
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        transaction_time = base_date.replace(hour=hour, minute=minute, second=second)
        
        # Apply seasonal patterns
        month = transaction_time.month
        if month in [12, 1, 2]:
            season = 'winter'
        elif month in [3, 4, 5]:
            season = 'spring'
        elif month in [6, 7, 8]:
            season = 'summer'
        else:
            season = 'fall'
        
        seasonal_mult = pattern['seasonal_multiplier'][season]
        
        # Generate transaction amount
        transaction_types = list(pattern['amount_ranges'].keys())
        num_types = len(transaction_types)
        
        # Create weights based on business type and number of transaction types
        if business_type == 'restaurant' and num_types >= 7:
            type_weights = [0.15, 0.35, 0.10, 0.15, 0.20, 0.04, 0.01]
        elif business_type == 'retail' and num_types >= 7:
            type_weights = [0.25, 0.30, 0.15, 0.10, 0.15, 0.04, 0.01]
        elif business_type == 'service' and num_types >= 7:
            type_weights = [0.30, 0.15, 0.15, 0.20, 0.10, 0.08, 0.02]
        elif business_type == 'healthcare' and num_types >= 7:
            type_weights = [0.25, 0.20, 0.10, 0.15, 0.15, 0.10, 0.05]
        elif business_type == 'coffee_shop' and num_types >= 7:
            type_weights = [0.35, 0.20, 0.15, 0.15, 0.10, 0.04, 0.01]
        elif business_type == 'handmade_crafts' and num_types >= 7:
            type_weights = [0.20, 0.25, 0.20, 0.15, 0.10, 0.08, 0.02]
        elif business_type == 'fitness_supplements' and num_types >= 7:
            type_weights = [0.25, 0.20, 0.20, 0.15, 0.10, 0.08, 0.02]
        elif business_type == 'tech_accessories' and num_types >= 7:
            type_weights = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]
        elif business_type == 'pet_supplies' and num_types >= 8:
            type_weights = [0.15, 0.15, 0.25, 0.15, 0.10, 0.15, 0.05]
        elif business_type == 'vintage_clothing' and num_types >= 7:
            type_weights = [0.20, 0.25, 0.15, 0.15, 0.10, 0.10, 0.05]
        elif business_type == 'beauty_cosmetics' and num_types >= 8:
            type_weights = [0.15, 0.20, 0.25, 0.15, 0.10, 0.10, 0.03, 0.02]
        elif business_type == 'home_garden' and num_types >= 8:
            type_weights = [0.20, 0.25, 0.15, 0.15, 0.10, 0.08, 0.05, 0.02]
        elif business_type == 'book_media' and num_types >= 8:
            type_weights = [0.25, 0.20, 0.15, 0.15, 0.10, 0.05, 0.08, 0.02]
        elif business_type == 'art_supplies' and num_types >= 8:
            type_weights = [0.20, 0.20, 0.15, 0.15, 0.15, 0.05, 0.08, 0.02]
        elif business_type == 'baby_kids' and num_types >= 8:
            type_weights = [0.18, 0.20, 0.20, 0.15, 0.08, 0.10, 0.07, 0.02]
        elif business_type == 'digital_downloads' and num_types >= 8:
            type_weights = [0.15, 0.20, 0.20, 0.15, 0.10, 0.08, 0.05, 0.07]
        else:
            # Default equal weights for any business type or when counts don't match
            type_weights = [1.0 / num_types] * num_types
        
        # Ensure weights match the number of transaction types
        if len(type_weights) != num_types:
            # Adjust weights to match actual number of types
            if len(type_weights) > num_types:
                # Truncate weights and renormalize
                type_weights = type_weights[:num_types]
            else:
                # Extend weights with equal distribution for remaining types
                remaining = num_types - len(type_weights)
                remaining_weight = 0.1 / remaining if remaining > 0 else 0
                type_weights.extend([remaining_weight] * remaining)
            
            # Normalize weights to sum to 1
            total_weight = sum(type_weights)
            type_weights = [w / total_weight for w in type_weights]
        
        transaction_type = np.random.choice(transaction_types, p=type_weights)
        min_amount, max_amount = pattern['amount_ranges'][transaction_type]
        
        base_amount = random.uniform(min_amount, max_amount)
        amount = base_amount * seasonal_mult
        
        if customer['is_regular'] and random.random() < 0.3:
            amount *= 0.9
        
        amount = round(amount, 2)
        
        # Generate payment method
        if 'preferred_payment' in customer:
            if random.random() < 0.7:
                payment_method = customer['preferred_payment']
            else:
                payment_method = random.choice(pattern['payment_methods'])
        
        # Generate shipping and billing addresses for e-commerce
        is_ecommerce = business_type in [
            'handmade_crafts', 'fitness_supplements', 'tech_accessories', 
            'pet_supplies', 'vintage_clothing', 'beauty_cosmetics', 
            'home_garden', 'book_media', 'art_supplies', 'baby_kids', 
            'digital_downloads'
        ]
        
        if is_ecommerce:
            billing_address = {
                'billing_street': fake.street_address(),
                'billing_city': fake.city(),
                'billing_state': fake.state_abbr(),
                'billing_zip': fake.zipcode(),
                'billing_country': random.choice(pattern['countries'])
            }
            
            if random.random() < 0.9:
                shipping_address = {
                    'shipping_street': billing_address['billing_street'],
                    'shipping_city': billing_address['billing_city'],
                    'shipping_state': billing_address['billing_state'],
                    'shipping_zip': billing_address['billing_zip'],
                    'shipping_country': billing_address['billing_country']
                }
            else:
                shipping_address = {
                    'shipping_street': fake.street_address(),
                    'shipping_city': fake.city(),
                    'shipping_state': fake.state_abbr(),
                    'shipping_zip': fake.zipcode(),
                    'shipping_country': random.choice(pattern['countries'])
                }
            
            shipping_method = random.choice(pattern['shipping_methods'])
            shipping_costs = {
                'Standard': random.uniform(3.99, 8.99),
                'Expedited': random.uniform(8.99, 15.99),
                'Express': random.uniform(15.99, 25.99),
                'Same Day': random.uniform(25.99, 39.99),
                'International': random.uniform(15.99, 45.99),
                'Subscription': 0,
                'Auto-Ship': 0,
                'Digital Download': 0,
                'Email Delivery': 0,
                'Cloud Access': 0,
                'Heavy Item': random.uniform(15.99, 35.99),
                'Local Delivery': random.uniform(5.99, 12.99)
            }
            shipping_cost = round(shipping_costs.get(shipping_method, 5.99), 2)
            
            delivery_days = {
                'Standard': random.randint(5, 8),
                'Expedited': random.randint(2, 4),
                'Express': random.randint(1, 2),
                'Same Day': 0,
                'International': random.randint(7, 21),
                'Subscription': random.randint(3, 7),
                'Auto-Ship': random.randint(3, 7),
                'Digital Download': 0,
                'Email Delivery': 0,
                'Cloud Access': 0,
                'Heavy Item': random.randint(7, 14),
                'Local Delivery': random.randint(1, 3)
            }
            
            estimated_delivery = (transaction_time + timedelta(days=delivery_days.get(shipping_method, 5))).strftime('%Y-%m-%d')
            
            risk_factors = []
            high_risk_countries = ['NG', 'GH', 'ID', 'PK', 'BD']
            if shipping_address['shipping_country'] in high_risk_countries:
                risk_factors.append('international_high_risk')
            
            if billing_address['billing_country'] != shipping_address['shipping_country']:
                risk_factors.append('country_mismatch')
            
            if shipping_method in ['Express', 'Same Day'] and amount > 200:
                risk_factors.append('rush_expensive')
            
            if shipping_address['shipping_country'] != 'US' and amount > 300:
                risk_factors.append('high_value_international')
                
            tracking_number = f"{random.choice(['1Z', '9400', 'TBA'])}{fake.random_number(digits=12, fix_len=True)}"
            
        else:
            billing_address = {}
            shipping_address = {}
            shipping_method = 'N/A'
            shipping_cost = 0
            estimated_delivery = 'N/A'
            risk_factors = []
            tracking_number = 'N/A'
        
        # FRAUD INJECTION - Add realistic fraudulent transactions
        is_fraudulent = False
        fraud_type = None
        fraud_indicators = []
        
        # Determine if this should be a fraudulent transaction (3-8% fraud rate)
        base_fraud_rate = 0.05  # 5% base rate
        
        # Higher fraud rates for e-commerce and certain patterns
        if is_ecommerce:
            fraud_rate = base_fraud_rate * 1.5  # E-commerce has higher fraud
            
            # Increase fraud rate based on risk factors
            if len(risk_factors) > 0:
                fraud_rate *= 2  # Double rate for risky transactions
            
            # Night transactions more likely to be fraudulent
            if hour >= 23 or hour <= 5:
                fraud_rate *= 1.8
                
            # High-value transactions more targeted
            if amount > 500:
                fraud_rate *= 1.5
                
        else:
            fraud_rate = base_fraud_rate * 0.8  # Physical locations slightly lower
        
        # Cap fraud rate at reasonable level
        fraud_rate = min(fraud_rate, 0.12)  # Max 12% fraud rate
        
        if random.random() < fraud_rate:
            is_fraudulent = True
            
            # Define fraud types with realistic patterns
            fraud_types = {
                'stolen_card': {
                    'weight': 0.35,
                    'characteristics': {
                        'rush_shipping': 0.8,  # Fraudsters want items fast
                        'high_value': 0.6,     # Often go for expensive items
                        'multiple_attempts': 0.3,  # Sometimes multiple tries
                        'new_customer': 0.9,   # Usually new accounts
                        'different_address': 0.7,  # Ship to different address
                        'decline_rate': 0.25   # Higher chance of decline
                    }
                },
                'account_takeover': {
                    'weight': 0.20,
                    'characteristics': {
                        'existing_customer': 0.8,  # Use real customer accounts
                        'unusual_location': 0.6,   # Different location than usual
                        'large_orders': 0.7,       # Make large purchases
                        'address_change': 0.8,     # Change shipping address
                        'decline_rate': 0.15
                    }
                },
                'synthetic_identity': {
                    'weight': 0.15,
                    'characteristics': {
                        'new_customer': 0.95,      # Always new accounts
                        'gradual_buildup': 0.4,    # Start small, increase
                        'normal_behavior': 0.6,    # Try to appear normal
                        'decline_rate': 0.20
                    }
                },
                'friendly_fraud': {
                    'weight': 0.20,
                    'characteristics': {
                        'existing_customer': 0.9,  # Real customers
                        'normal_patterns': 0.8,    # Normal purchase behavior
                        'legitimate_card': 0.95,   # Real payment info
                        'decline_rate': 0.05       # Usually approves
                    }
                },
                'triangulation': {
                    'weight': 0.10,
                    'characteristics': {
                        'rapid_orders': 0.7,       # Multiple quick orders
                        'different_items': 0.8,    # Variety of products
                        'reshipping': 0.9,         # Ship to reshipping services
                        'decline_rate': 0.30
                    }
                }
            }
            
            # Select fraud type based on weights
            fraud_type_names = list(fraud_types.keys())
            fraud_weights = [fraud_types[ft]['weight'] for ft in fraud_type_names]
            fraud_type = np.random.choice(fraud_type_names, p=fraud_weights)
            
            fraud_char = fraud_types[fraud_type]['characteristics']
            
            # Apply fraud characteristics
            if fraud_type == 'stolen_card':
                fraud_indicators.append('stolen_card_pattern')
                
                # Rush shipping
                if random.random() < fraud_char['rush_shipping']:
                    if is_ecommerce and 'Express' in pattern['shipping_methods']:
                        shipping_method = 'Express'
                        fraud_indicators.append('rush_shipping')
                
                # High value preference
                if random.random() < fraud_char['high_value']:
                    # Increase amount for expensive items
                    amount *= random.uniform(2.0, 4.0)
                    amount = min(amount, max_amount * 3)  # Cap it
                    fraud_indicators.append('unusually_high_amount')
                
                # Different shipping address
                if random.random() < fraud_char['different_address'] and is_ecommerce:
                    # Change shipping to different country/far location
                    high_risk_countries = ['NG', 'GH', 'PK', 'ID', 'BD', 'RO', 'UA']
                    shipping_address['shipping_country'] = random.choice(high_risk_countries)
                    shipping_address['shipping_city'] = fake.city()
                    fraud_indicators.append('suspicious_shipping_location')
                
                # Force new customer
                if random.random() < fraud_char['new_customer']:
                    is_new_customer = True
                    customer['is_regular'] = False
                    fraud_indicators.append('new_account_high_value')
            
            elif fraud_type == 'account_takeover':
                fraud_indicators.append('account_takeover_pattern')
                
                # Use existing customer but change behavior
                if random.random() < fraud_char['existing_customer']:
                    is_new_customer = False
                    customer['is_regular'] = True
                
                # Unusual location (different IP geolocation)
                if random.random() < fraud_char['unusual_location'] and is_ecommerce:
                    fraud_indicators.append('unusual_location')
                
                # Large order
                if random.random() < fraud_char['large_orders']:
                    amount *= random.uniform(1.5, 3.0)
                    fraud_indicators.append('unusual_order_size')
                
                # Address change
                if random.random() < fraud_char['address_change'] and is_ecommerce:
                    # Ship to completely different location
                    shipping_address['shipping_street'] = fake.street_address()
                    shipping_address['shipping_city'] = fake.city()
                    shipping_address['shipping_state'] = fake.state_abbr()
                    fraud_indicators.append('address_change')
            
            elif fraud_type == 'synthetic_identity':
                fraud_indicators.append('synthetic_identity_pattern')
                
                # Always new customer
                is_new_customer = True
                customer['is_regular'] = False
                
                # Sometimes normal amounts to build trust
                if random.random() < fraud_char['normal_behavior']:
                    # Keep normal amount
                    pass
                else:
                    amount *= random.uniform(1.2, 2.0)
                    fraud_indicators.append('identity_testing')
            
            elif fraud_type == 'friendly_fraud':
                fraud_indicators.append('friendly_fraud_pattern')
                
                # Real customer
                is_new_customer = False
                customer['is_regular'] = True
                
                # Normal behavior - hardest to detect
                fraud_indicators.append('chargeback_risk')
            
            elif fraud_type == 'triangulation':
                fraud_indicators.append('triangulation_pattern')
                
                # Rapid/multiple orders pattern
                fraud_indicators.append('rapid_order_pattern')
                
                # Reshipping service address
                if is_ecommerce and random.random() < fraud_char['reshipping']:
                    reshipping_cities = ['Miami', 'Doral', 'Hialeah', 'New York', 'Los Angeles']
                    shipping_address['shipping_city'] = random.choice(reshipping_cities)
                    fraud_indicators.append('reshipping_service')
            
            # Adjust decline rate based on fraud type - this will be handled later
            # in the main response code logic section
            
            # Add common fraud indicators
            if amount > 1000:
                fraud_indicators.append('high_value_transaction')
            
            if is_ecommerce and shipping_address['shipping_country'] != billing_address['billing_country']:
                fraud_indicators.append('billing_shipping_mismatch')
            
            if hour >= 1 and hour <= 5:
                fraud_indicators.append('unusual_time')
        
        # Combine all risk factors
        all_risk_factors = risk_factors + fraud_indicators
        
        # Generate card details
        if payment_method in ['Visa', 'Mastercard', 'American Express', 'Discover']:
            if payment_method == 'Visa':
                card_number = fake.credit_card_number(card_type='visa')
            elif payment_method == 'Mastercard':
                card_number = fake.credit_card_number(card_type='mastercard')
            elif payment_method == 'American Express':
                card_number = fake.credit_card_number(card_type='amex')
            else:
                card_number = fake.credit_card_number(card_type='discover')
            
            card_last4 = card_number[-4:]
            exp_date = fake.credit_card_expire()
            
            if payment_method == 'American Express':
                cvv = fake.random_number(digits=4, fix_len=True)
            else:
                cvv = fake.random_number(digits=3, fix_len=True)
                
        else:
            card_number = None
            card_last4 = None
            exp_date = None
            cvv = None
        
        # Generate response codes with fraud consideration
        response_code = '00'  # Default to approved
        response_text = 'Approved'
        response_code_set = False  # Track if we've already set the response code
        
        if is_fraudulent:
            # For fraudulent transactions, check decline probability
            fraud_char = fraud_types[fraud_type]['characteristics']
            decline_probability = fraud_char['decline_rate']
            
            if random.random() < decline_probability:
                # Force a decline for this fraudulent transaction
                fraud_error_codes = {
                    '05': 'Do not honor',
                    '14': 'Invalid card number',
                    '51': 'Insufficient funds',
                    '57': 'Transaction not permitted',
                    '59': 'Suspected fraud',
                    '61': 'Exceeds withdrawal limit',
                    '62': 'Restricted card',
                    '65': 'Activity limit exceeded',
                    '78': 'Blocked - first use',
                    '96': 'System error'
                }
                response_code = random.choice(list(fraud_error_codes.keys()))
                response_text = fraud_error_codes[response_code]
                fraud_indicators.append('payment_declined')
                response_code_set = True
            # else: fraudulent transaction that gets approved (harder to detect)
        
        # For non-fraudulent transactions or fraudulent ones that weren't declined
        if not response_code_set:
            if is_ecommerce:
                if len(risk_factors) > 0:
                    success_rate = 0.85
                else:
                    success_rate = 0.94
            else:
                success_rate = 0.96
            
            if random.random() < success_rate:
                response_code = '00'
                response_text = 'Approved'
            else:
                if is_ecommerce:
                    ecommerce_errors = {
                        '05': 'Do not honor',
                        '14': 'Invalid card number',
                        '51': 'Insufficient funds', 
                        '57': 'Transaction not permitted',
                        '61': 'Exceeds withdrawal limit',
                        '62': 'Restricted card',
                        '65': 'Activity limit exceeded',
                        '78': 'Blocked - first use',
                        '96': 'System error'
                    }
                    error_codes = ecommerce_errors
                else:
                    error_codes = {
                        '05': 'Do not honor',
                        '14': 'Invalid card number',
                        '51': 'Insufficient funds',
                        '61': 'Exceeds withdrawal limit'
                    }
                
                response_code = random.choice(list(error_codes.keys()))
                response_text = error_codes[response_code]
        
        # Generate additional fields
        terminal_id = f"TRM_{random.randint(1000, 9999)}"
        batch_id = f"B{random.randint(100000, 999999)}"
        
        mcc_codes = {
            'Restaurant': '5812',
            'Retail': '5699',
            'Automotive Service': '7538',
            'Healthcare': '8021',
            'Coffee Shop': '5814',
            'E-commerce - Handmade': '5969',
            'E-commerce - Health & Fitness': '5499',
            'E-commerce - Electronics': '5732',
            'E-commerce - Pet Supplies': '5995',
            'E-commerce - Vintage Fashion': '5691',
            'E-commerce - Beauty & Cosmetics': '5977',
            'E-commerce - Home & Garden': '5261',
            'E-commerce - Books & Media': '5942',
            'E-commerce - Art Supplies': '5970',
            'E-commerce - Baby & Kids': '5641',
            'E-commerce - Digital Products': '5815'
        }
        
        if is_ecommerce:
            ip_address = fake.ipv4()
            user_agent = random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
                'Mozilla/5.0 (Android 11; Mobile; rv:94.0) Gecko/94.0'
            ])
            
            session_id = fake.uuid4()
            referrer = random.choice([
                'https://www.google.com',
                'https://www.facebook.com', 
                'https://www.instagram.com',
                'direct',
                'email_campaign',
                'paid_search'
            ])
        else:
            ip_address = 'N/A'
            user_agent = 'N/A'
            session_id = 'N/A'
            referrer = 'N/A'
        
        # Create transaction record with fraud data
        transaction = {
            'transaction_id': f"TXN_{i+1:08d}",
            'customer_id': customer['customer_id'],
            'customer_name': customer['name'],
            'customer_email': customer['email'] if random.random() < 0.8 else '',
            'customer_phone': customer['phone'] if random.random() < 0.6 else '',
            'transaction_date': transaction_time.strftime('%Y-%m-%d'),
            'transaction_time': transaction_time.strftime('%H:%M:%S'),
            'amount': round(amount, 2),
            'transaction_type': transaction_type,
            'payment_method': payment_method,
            'card_type': payment_method if payment_method in ['Visa', 'Mastercard', 'American Express', 'Discover'] else '',
            'card_last4': card_last4 if card_last4 else '',
            'card_exp_date': exp_date if exp_date else '',
            'merchant_name': pattern['name'],
            'merchant_category': pattern['category'],
            'merchant_category_code': mcc_codes[pattern['category']],
            'terminal_id': terminal_id,
            'batch_id': batch_id,
            'response_code': response_code,
            'response_text': response_text,
            'is_new_customer': is_new_customer,
            'is_regular_customer': customer['is_regular'],
            'tip_amount': round(amount * random.uniform(0.1, 0.2), 2) if business_type in ['restaurant', 'coffee_shop'] and random.random() < 0.7 else 0,
            'tax_amount': round(amount * 0.08875, 2),
            'employee_id': f"EMP_{random.randint(100, 999)}",
            'pos_system': random.choice(['Square', 'Clover', 'Toast', 'Shopify POS', 'Lightspeed', 'WooCommerce', 'Magento']),
            # FRAUD DETECTION FIELDS
            'is_fraudulent': is_fraudulent,
            'fraud_type': fraud_type if is_fraudulent else '',
            'fraud_indicators': ','.join(fraud_indicators) if fraud_indicators else '',
            'risk_score': calculate_risk_score(amount, hour, all_risk_factors, is_fraudulent, is_ecommerce),
            'all_risk_factors': ','.join(all_risk_factors) if all_risk_factors else ''
        }
        
        # Add e-commerce specific fields
        if is_ecommerce:
            ecommerce_fields = {
                'shipping_method': shipping_method,
                'shipping_cost': shipping_cost,
                'estimated_delivery': estimated_delivery,
                'tracking_number': tracking_number,
                'billing_street': billing_address['billing_street'],
                'billing_city': billing_address['billing_city'],
                'billing_state': billing_address['billing_state'],
                'billing_zip': billing_address['billing_zip'],
                'billing_country': billing_address['billing_country'],
                'shipping_street': shipping_address['shipping_street'],
                'shipping_city': shipping_address['shipping_city'],
                'shipping_state': shipping_address['shipping_state'],
                'shipping_zip': shipping_address['shipping_zip'],
                'shipping_country': shipping_address['shipping_country'],
                'ip_address': ip_address,
                'user_agent': user_agent,
                'session_id': session_id,
                'referrer_source': referrer,
                'risk_factors': ','.join(all_risk_factors) if all_risk_factors else '',
                'is_ecommerce': True
            }
            transaction.update(ecommerce_fields)
        else:
            ecommerce_fields = {
                'shipping_method': 'N/A',
                'shipping_cost': 0,
                'estimated_delivery': 'N/A',
                'tracking_number': 'N/A',
                'billing_street': 'N/A',
                'billing_city': 'N/A',
                'billing_state': 'N/A',
                'billing_zip': 'N/A',
                'billing_country': 'N/A',
                'shipping_street': 'N/A',
                'shipping_city': 'N/A',
                'shipping_state': 'N/A',
                'shipping_zip': 'N/A',
                'shipping_country': 'N/A',
                'ip_address': 'N/A',
                'user_agent': 'N/A',
                'session_id': 'N/A',
                'referrer_source': 'N/A',
                'risk_factors': ','.join(all_risk_factors) if all_risk_factors else '',
                'is_ecommerce': False
            }
            transaction.update(ecommerce_fields)
        
        transactions.append(transaction)
    
    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    
    # Sort by transaction date and time
    df['datetime'] = pd.to_datetime(df['transaction_date'] + ' ' + df['transaction_time'])
    df = df.sort_values('datetime').drop('datetime', axis=1)
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

def calculate_risk_score(amount, hour, risk_factors, is_fraudulent, is_ecommerce):
    """Calculate a risk score based on various factors"""
    score = 0
    
    # Base score from amount
    if amount > 1000:
        score += 30
    elif amount > 500:
        score += 20
    elif amount > 100:
        score += 10
    elif amount < 5:
        score += 25
    
    # Time-based risk
    if hour >= 23 or hour <= 5:
        score += 15
    elif hour >= 1 and hour <= 3:
        score += 25  # Very late night
    
    # Risk factors
    score += len(risk_factors) * 8
    
    # E-commerce penalty
    if is_ecommerce:
        score += 5
    
    # If actually fraudulent, ensure high score
    if is_fraudulent:
        score = max(score, 75)
        score += random.randint(0, 25)
    
    return min(score, 100)

# Global business scenarios definition
business_scenarios = {
    # PHYSICAL BUSINESSES
    'restaurant_transactions': {
        'business_type': 'restaurant',
        'transactions': 1500,
        'description': 'Italian restaurant with lunch and dinner service'
    },
    'retail_store_transactions': {
        'business_type': 'retail',
        'transactions': 1200,
        'description': 'Women\'s clothing boutique'
    },
    'auto_repair_transactions': {
        'business_type': 'service',
        'transactions': 800,
        'description': 'Local auto repair shop'
    },
    'dental_clinic_transactions': {
        'business_type': 'healthcare',
        'transactions': 600,
        'description': 'Family dental practice'
    },
    'coffee_shop_transactions': {
        'business_type': 'coffee_shop',
        'transactions': 2000,
        'description': 'Local coffee shop with breakfast and lunch'
    },
    
    # ORIGINAL E-COMMERCE BUSINESSES
    'handmade_crafts_ecommerce': {
        'business_type': 'handmade_crafts',
        'transactions': 1800,
        'description': 'Online artisan crafts store with international shipping'
    },
    'fitness_supplements_ecommerce': {
        'business_type': 'fitness_supplements',
        'transactions': 2200,
        'description': 'Online nutrition and supplement retailer'
    },
    'tech_accessories_ecommerce': {
        'business_type': 'tech_accessories',
        'transactions': 3000,
        'description': 'Online electronics accessories with fast shipping'
    },
    'pet_supplies_ecommerce': {
        'business_type': 'pet_supplies',
        'transactions': 1600,
        'description': 'Online pet store with subscription services'
    },
    'vintage_clothing_ecommerce': {
        'business_type': 'vintage_clothing',
        'transactions': 1200,
        'description': 'Online vintage fashion boutique with global reach'
    },
    
    # NEW E-COMMERCE BUSINESSES
    'beauty_cosmetics_ecommerce': {
        'business_type': 'beauty_cosmetics',
        'transactions': 2500,
        'description': 'Online beauty and cosmetics store with subscription boxes'
    },
    'home_garden_ecommerce': {
        'business_type': 'home_garden',
        'transactions': 1400,
        'description': 'Online gardening supplies with seasonal patterns'
    },
    'book_media_ecommerce': {
        'business_type': 'book_media',
        'transactions': 1800,
        'description': 'Digital bookstore with ebooks and physical books'
    },
    'art_supplies_ecommerce': {
        'business_type': 'art_supplies',
        'transactions': 1300,
        'description': 'Online art supplies store for professionals and hobbyists'
    },
    'baby_kids_ecommerce': {
        'business_type': 'baby_kids',
        'transactions': 2000,
        'description': 'Online baby and kids store with subscription services'
    },
    'digital_downloads_ecommerce': {
        'business_type': 'digital_downloads',
        'transactions': 2800,
        'description': 'Digital products marketplace with global reach'
    }
}

def generate_multiple_smb_datasets():
    """Generate multiple datasets for different SMB types"""
    
    # Create SMB_transaction_files directory if it doesn't exist
    output_dir = 'SMB_transaction_files'
    os.makedirs(output_dir, exist_ok=True)
    
    all_datasets_summary = []
    
    for dataset_name, config in business_scenarios.items():
        print(f"\nGenerating {dataset_name}...")
        print(f"Business: {config['description']}")
        
        df = generate_smb_transaction_data(
            num_transactions=config['transactions'],
            business_type=config['business_type']
        )
        
        # Save to CSV
        filename = os.path.join(output_dir, f'{dataset_name}.csv')
        df.to_csv(filename, index=False)
        
        # Calculate summary statistics
        summary = {
            'dataset': dataset_name,
            'business_type': config['business_type'],
            'total_transactions': len(df),
            'unique_customers': df['customer_id'].nunique(),
            'date_range': f"{df['transaction_date'].min()} to {df['transaction_date'].max()}",
            'avg_transaction': f"${df['amount'].mean():.2f}",
            'total_revenue': f"${df['amount'].sum():.2f}",
            'payment_methods': df['payment_method'].value_counts().to_dict(),
            'success_rate': f"{(df['response_code'] == '00').mean() * 100:.1f}%",
            'filename': filename
        }
        
        all_datasets_summary.append(summary)
        
        print(f"  Total transactions: {len(df):,}")
        print(f"  Unique customers: {df['customer_id'].nunique():,}")
        print(f"  Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
        print(f"  Average transaction: ${df['amount'].mean():.2f}")
        print(f"  Total revenue: ${df['amount'].sum():,.2f}")
        print(f"  Success rate: {(df['response_code'] == '00').mean() * 100:.1f}%")
        print(f"  Fraud rate: {df['is_fraudulent'].mean() * 100:.1f}%")
        print(f"  Fraudulent transactions: {df['is_fraudulent'].sum():,}")
        print(f"  Most common payment: {df['payment_method'].mode().iloc[0]}")
        print(f"  E-commerce: {'Yes' if df['is_ecommerce'].iloc[0] else 'No'}")
        print(f"  Saved to: {filename}")
    
    # Create a combined dataset summary
    summary_df = pd.DataFrame([{
        'Dataset': s['dataset'],
        'Business Type': s['business_type'].title(),
        'Transactions': s['total_transactions'],
        'Customers': s['unique_customers'],
        'Avg Amount': s['avg_transaction'],
        'Total Revenue': s['total_revenue'],
        'Success Rate': s['success_rate']
    } for s in all_datasets_summary])
    
    summary_filename = os.path.join(output_dir, 'datasets_summary.csv')
    summary_df.to_csv(summary_filename, index=False)
    
    return all_datasets_summary

# Generate the datasets
if __name__ == "__main__":
    print("🏪 Generating comprehensive SMB transaction datasets with fraud detection...")
    print("=" * 70)
    
    datasets_summary = generate_multiple_smb_datasets()
    
    print("\n" + "=" * 70)
    print("✅ SMB DATASET GENERATION COMPLETE WITH FRAUD DETECTION")
    print("=" * 70)
    
    # Show sample data structure
    print("\n📊 Sample e-commerce transaction structure:")
    sample_df = generate_smb_transaction_data(num_transactions=3, business_type='tech_accessories')
    
    # Display key columns including fraud data
    ecommerce_display_columns = [
        'transaction_id', 'customer_name', 'transaction_date', 'amount', 
        'transaction_type', 'payment_method', 'shipping_method', 'shipping_country',
        'is_fraudulent', 'fraud_type', 'risk_score', 'response_code'
    ]
    print(sample_df[ecommerce_display_columns].to_string(index=False))
    
    print(f"\n🚨 Fraud Summary Across All Datasets:")
    fraud_summary = []
    for dataset_name, config in list(business_scenarios.items())[:5]:  # Sample first 5
        temp_df = generate_smb_transaction_data(num_transactions=100, business_type=config['business_type'])
        fraud_count = temp_df['is_fraudulent'].sum()
        fraud_rate = (fraud_count / len(temp_df)) * 100
        fraud_summary.append(f"  • {dataset_name}: {fraud_rate:.1f}% fraud rate")
    
    for summary in fraud_summary:
        print(summary)
    print("  • ... (and more)")
    
    print("\n📋 Enhanced column descriptions (including fraud detection fields):")
    key_columns = {
        'transaction_id': 'Unique transaction identifier',
        'customer_name': 'Customer full name (Faker generated)',
        'amount': 'Transaction amount in USD',
        'payment_method': 'Payment method (cards, PayPal, Apple Pay, etc.)',
        'merchant_category': 'Business category (including e-commerce types)',
        'shipping_method': 'E-commerce shipping option',
        'shipping_country': 'Destination country for e-commerce',
        'response_code': 'Transaction response (00=approved, others=declined)',
        '--- FRAUD FIELDS ---': '--- FRAUD DETECTION CAPABILITIES ---',
        'is_fraudulent': 'Whether transaction is actually fraudulent (TRUE/FALSE)',
        'fraud_type': 'Type of fraud (stolen_card, account_takeover, etc.)',
        'fraud_indicators': 'Specific fraud pattern indicators',
        'risk_score': 'Calculated risk score (0-100)',
        'all_risk_factors': 'Combined list of all risk factors'
    }
    
    for column, description in key_columns.items():
        if column.startswith('---'):
            print(f"\n{description}")
        else:
            print(f"  • {column}: {description}")
    
    print(f"\n📁 All {len(business_scenarios)} datasets saved to: SMB_transaction_files/")
    print("\n🎯 Complete SMB Dataset Collection:")
    print("  • 5 Physical Business Types (restaurants, retail, services, etc.)")
    print("  • 11 E-commerce Business Types (handmade, tech, beauty, digital, etc.)")
    print("  • 🚨 Realistic Fraud Patterns (3-8% fraud rate)")
    print("  • 5 Fraud Types: stolen_card, account_takeover, synthetic_identity, friendly_fraud, triangulation")
    print("  • Complete risk scoring and fraud indicators")
    print("  • 27,000+ total transactions across all datasets")
    print("\n🚀 Perfect for testing FraudGuard Pro with comprehensive fraud scenarios!")
    print("\n💡 Installation: pip install faker pandas numpy")
    print("💡 Usage: python smb_transaction_generator_complete.py")