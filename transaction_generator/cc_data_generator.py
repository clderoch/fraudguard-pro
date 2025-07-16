# Enhanced SMB Transaction Data Generator with Modern Online Business Types
# Save as: enhanced_smb_transaction_generator.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import json
from faker import Faker
from faker.providers import credit_card, person, company, address
import hashlib

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Initialize Faker with multiple locales for international transactions
fake = Faker('en_US')
fake.add_provider(credit_card)
fake.add_provider(person)
fake.add_provider(company)
fake.add_provider(address)

class EnhancedTransactionGenerator:
    def __init__(self):
        self.currency_rates = {
            'USD': 1.0, 'EUR': 0.85, 'GBP': 0.73, 'CAD': 1.25, 
            'AUD': 1.35, 'JPY': 110.0, 'CNY': 6.5, 'INR': 75.0
        }
        
        self.device_types = {
            'mobile': {'ios': 0.55, 'android': 0.45},
            'desktop': {'windows': 0.7, 'mac': 0.25, 'linux': 0.05},
            'tablet': {'ipad': 0.65, 'android': 0.35}
        }
        
        self.marketing_channels = [
            'organic_search', 'paid_search', 'social_media', 'email', 
            'affiliate', 'direct', 'referral', 'display_ads', 'influencer'
        ]

    def generate_customer_profile(self, business_type):
        """Generate enhanced customer profile with behavioral attributes"""
        customer_id = f"CUST_{fake.random_number(digits=8, fix_len=True)}"
        
        # Customer segments based on business type
        if 'subscription' in business_type or 'saas' in business_type:
            segments = ['individual', 'small_team', 'enterprise', 'startup']
            segment = random.choice(segments)
        elif 'marketplace' in business_type:
            segments = ['buyer', 'seller', 'both']
            segment = random.choice(segments)
        else:
            segments = ['new', 'regular', 'vip', 'dormant']
            segment = random.choice(segments)
        
        # Generate customer lifetime value based on segment
        clv_ranges = {
            'new': (50, 500), 'regular': (500, 2000), 'vip': (2000, 10000),
            'dormant': (100, 800), 'individual': (100, 1000),
            'small_team': (1000, 5000), 'enterprise': (5000, 50000),
            'startup': (500, 3000), 'buyer': (100, 2000), 
            'seller': (1000, 20000), 'both': (2000, 30000)
        }
        
        clv_range = clv_ranges.get(segment, (100, 1000))
        clv = random.uniform(*clv_range)
        
        # Device preferences
        device_prefs = random.choices(['mobile', 'desktop', 'tablet'], 
                                     weights=[0.6, 0.3, 0.1])[0]
        
        # Generate US location with timezone
        country = 'US'  # Only US customers
        timezone = random.choice(['EST', 'CST', 'MST', 'PST'])
        
        # Generate US address components
        fake_us = Faker('en_US')
        city = fake_us.city()
        state = fake_us.state()
        zip_code = fake_us.zipcode()
        
        return {
            'customer_id': customer_id,
            'name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'segment': segment,
            'clv': clv,
            'acquisition_date': fake.date_between(start_date='-2y', end_date='today'),
            'acquisition_channel': random.choice(self.marketing_channels),
            'preferred_device': device_prefs,
            'country': country,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'timezone': timezone,
            'language': random.choice(['en', 'es', 'fr', 'de', 'ja']),
            'payment_methods': random.sample(['card', 'paypal', 'apple_pay', 'google_pay', 
                                            'crypto', 'bank_transfer'], k=random.randint(1, 3)),
            'address': fake.address(),  # Add customer address
            'ip_address': fake.ipv4_public()  # Add customer IP address
        }

    def generate_enhanced_transaction_data(self, num_transactions=2000, business_type='saas_b2b'):
        """Generate realistic transaction data for modern online businesses"""
        
        # Enhanced business patterns for modern online businesses
        business_patterns = {
            # SUBSCRIPTION BUSINESSES
            'saas_b2b': {
                'name': 'CloudSync Pro',
                'category': 'SaaS - B2B',
                'subscription_tiers': {
                    'starter': {'price': 29, 'users': 5, 'features': 'basic'},
                    'professional': {'price': 99, 'users': 20, 'features': 'advanced'},
                    'business': {'price': 299, 'users': 100, 'features': 'premium'},
                    'enterprise': {'price': 999, 'users': 'unlimited', 'features': 'custom'}
                },
                'billing_cycles': {'monthly': 0.6, 'annual': 0.4},
                'transaction_types': ['new_subscription', 'renewal', 'upgrade', 'downgrade', 
                                    'addon', 'overage', 'refund'],
                'peak_hours': [9, 10, 11, 14, 15, 16],
                'peak_days': [1, 2, 3, 4],
                'churn_rate': 0.05,
                'trial_conversion': 0.15
            },
            
            'streaming_service': {
                'name': 'StreamFlix Plus',
                'category': 'Digital Entertainment',
                'subscription_tiers': {
                    'basic': {'price': 8.99, 'quality': 'SD', 'screens': 1},
                    'standard': {'price': 13.99, 'quality': 'HD', 'screens': 2},
                    'premium': {'price': 17.99, 'quality': '4K', 'screens': 4},
                    'family': {'price': 22.99, 'quality': '4K', 'screens': 6}
                },
                'billing_cycles': {'monthly': 0.85, 'annual': 0.15},
                'transaction_types': ['new_subscription', 'renewal', 'upgrade', 'gift_subscription'],
                'peak_hours': [19, 20, 21, 22],
                'peak_days': [4, 5, 6],
                'churn_rate': 0.08,
                'seasonal_shows_impact': True
            },
            
            'online_education': {
                'name': 'SkillMaster Academy',
                'category': 'E-Learning Platform',
                'course_categories': {
                    'programming': (49, 299),
                    'design': (39, 199),
                    'business': (59, 399),
                    'language': (29, 149),
                    'certification': (199, 999),
                    'bootcamp': (2999, 9999)
                },
                'subscription_options': {
                    'monthly_unlimited': 39.99,
                    'annual_unlimited': 299.99
                },
                'transaction_types': ['course_purchase', 'subscription', 'certification_fee', 
                                    'bootcamp_enrollment', 'bundle_purchase'],
                'peak_hours': [18, 19, 20, 21],
                'peak_days': [0, 1, 6],
                'completion_rate': 0.3,
                'seasonal_pattern': 'new_year_september'
            },
            
            # MARKETPLACE BUSINESSES
            'digital_marketplace': {
                'name': 'CreativeMarket Pro',
                'category': 'Digital Assets Marketplace',
                'product_categories': {
                    'templates': (5, 150),
                    'graphics': (2, 80),
                    'fonts': (10, 200),
                    'photos': (1, 50),
                    'videos': (20, 500),
                    'audio': (5, 100),
                    '3d_models': (15, 300)
                },
                'commission_rate': 0.3,
                'seller_payout_schedule': 'weekly',
                'transaction_types': ['purchase', 'bundle_purchase', 'subscription_download', 
                                    'seller_payout', 'refund'],
                'peak_hours': [9, 10, 11, 14, 15],
                'peak_days': [1, 2, 3, 4],
                'international_sales': 0.4
            },
            
            'freelance_platform': {
                'name': 'TalentHub Global',
                'category': 'Freelance Services Platform',
                'service_categories': {
                    'writing': (20, 500),
                    'design': (50, 2000),
                    'development': (100, 5000),
                    'marketing': (75, 1500),
                    'video': (100, 3000),
                    'consulting': (150, 5000)
                },
                'platform_fee': 0.2,
                'escrow_period': 7,
                'transaction_types': ['project_payment', 'milestone_payment', 'tip', 
                                    'platform_fee', 'withdrawal', 'dispute_resolution'],
                'peak_hours': [10, 11, 14, 15, 16],
                'peak_days': [1, 2, 3, 4],
                'international_transactions': 0.6
            },
            
            # GAMING & VIRTUAL GOODS
            'gaming_platform': {
                'name': 'GameVerse Online',
                'category': 'Gaming Platform',
                'transaction_categories': {
                    'game_purchase': (9.99, 69.99),
                    'dlc': (4.99, 29.99),
                    'season_pass': (19.99, 49.99),
                    'virtual_currency_small': (4.99, 9.99),
                    'virtual_currency_medium': (19.99, 49.99),
                    'virtual_currency_large': (99.99, 199.99),
                    'subscription': (9.99, 14.99)
                },
                'payment_methods': ['card', 'paypal', 'crypto', 'gift_card', 'mobile_billing'],
                'transaction_types': ['purchase', 'in_game_purchase', 'subscription', 'gift'],
                'peak_hours': [18, 19, 20, 21, 22, 23],
                'peak_days': [4, 5, 6],
                'whale_percentage': 0.02  # 2% of users are high spenders
            },
            
            # FINTECH & FINANCIAL SERVICES
            'payment_processor': {
                'name': 'PayFlow Solutions',
                'category': 'Payment Processing',
                'merchant_types': {
                    'small_business': {'volume': (1000, 50000), 'fee': 0.029},
                    'medium_business': {'volume': (50000, 500000), 'fee': 0.025},
                    'enterprise': {'volume': (500000, 10000000), 'fee': 0.019}
                },
                'transaction_types': ['payment', 'refund', 'chargeback', 'payout', 
                                    'fee_collection', 'currency_conversion'],
                'currencies': ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY'],
                'peak_hours': [10, 11, 14, 15, 16],
                'peak_days': [1, 2, 3, 4],
                'fraud_rate': 0.001
            },
            
            'crypto_exchange': {
                'name': 'CryptoTrade Pro',
                'category': 'Cryptocurrency Exchange',
                'trading_pairs': {
                    'BTC/USD': {'min': 100, 'max': 100000, 'volatility': 0.05},
                    'ETH/USD': {'min': 50, 'max': 50000, 'volatility': 0.07},
                    'USDT/USD': {'min': 10, 'max': 100000, 'volatility': 0.001},
                    'other_alts': {'min': 10, 'max': 10000, 'volatility': 0.15}
                },
                'fee_structure': {
                    'maker': 0.001,
                    'taker': 0.002,
                    'withdrawal': {'fixed': 25, 'percentage': 0.0005}
                },
                'transaction_types': ['buy', 'sell', 'deposit', 'withdrawal', 'staking_reward'],
                'peak_hours': list(range(24)),  # 24/7 market
                'peak_days': list(range(7)),    # All days
                'institutional_percentage': 0.3
            },
            
            # MODERN E-COMMERCE
            'dropshipping_store': {
                'name': 'TrendyFinds Direct',
                'category': 'Dropshipping E-commerce',
                'product_categories': {
                    'electronics': (15, 150),
                    'fashion': (10, 80),
                    'home_gadgets': (20, 100),
                    'fitness': (15, 120),
                    'beauty': (8, 60)
                },
                'supplier_locations': ['CN', 'VN', 'TH', 'US'],
                'shipping_times': {
                    'economy': (15, 30),
                    'standard': (7, 15),
                    'express': (3, 7)
                },
                'transaction_types': ['purchase', 'upsell', 'abandoned_cart_recovery'],
                'peak_hours': [12, 13, 19, 20, 21],
                'peak_days': [0, 6],
                'return_rate': 0.15
            },
            
            'subscription_box': {
                'name': 'CuratedBox Monthly',
                'category': 'Subscription Box Service',
                'box_types': {
                    'beauty_box': {'price': 25, 'frequency': 'monthly'},
                    'snack_box': {'price': 35, 'frequency': 'monthly'},
                    'book_box': {'price': 40, 'frequency': 'monthly'},
                    'wine_box': {'price': 89, 'frequency': 'monthly'},
                    'craft_box': {'price': 45, 'frequency': 'quarterly'}
                },
                'addons': {
                    'extra_item': (5, 20),
                    'premium_upgrade': (10, 30),
                    'gift_wrapping': (5, 10)
                },
                'transaction_types': ['new_subscription', 'renewal', 'addon', 'gift', 'pause'],
                'peak_hours': [10, 11, 19, 20],
                'peak_days': [0, 6],
                'churn_rate': 0.1
            },
            
            # TRAVEL & BOOKING
            'travel_booking': {
                'name': 'WanderBook Travel',
                'category': 'Online Travel Agency',
                'booking_types': {
                    'flight': (150, 2500),
                    'hotel': (80, 500),
                    'vacation_package': (500, 5000),
                    'car_rental': (30, 150),
                    'activity': (25, 300),
                    'travel_insurance': (50, 300)
                },
                'booking_window': {  # Days before travel
                    'last_minute': (1, 7),
                    'standard': (8, 60),
                    'advance': (61, 365)
                },
                'commission_rates': {
                    'flight': 0.05,
                    'hotel': 0.15,
                    'package': 0.12,
                    'car': 0.10,
                    'activity': 0.20
                },
                'transaction_types': ['booking', 'cancellation', 'modification', 'insurance'],
                'peak_hours': [9, 10, 11, 19, 20, 21],
                'peak_days': [0, 1, 6],
                'seasonal_peaks': ['summer', 'holidays']
            },
            
            # FOOD DELIVERY & MEAL SERVICES
            'food_delivery_platform': {
                'name': 'QuickEats Delivery',
                'category': 'Food Delivery Platform',
                'order_categories': {
                    'fast_food': (15, 40),
                    'restaurant': (25, 80),
                    'groceries': (30, 150),
                    'alcohol': (20, 100),
                    'convenience': (10, 50)
                },
                'fees': {
                    'delivery': (2.99, 6.99),
                    'service': 0.15,  # 15% of order
                    'small_order': 2.00
                },
                'peak_times': {
                    'lunch': [11, 12, 13],
                    'dinner': [18, 19, 20],
                    'late_night': [22, 23, 0]
                },
                'transaction_types': ['order', 'tip', 'subscription_fee', 'refund', 'credit'],
                'driver_payout_percentage': 0.8,
                'order_frequency': 'multiple_per_week'
            },
            
            # DIGITAL HEALTH
            'telehealth_platform': {
                'name': 'HealthConnect Virtual',
                'category': 'Telehealth Services',
                'service_types': {
                    'consultation': (75, 200),
                    'therapy_session': (100, 250),
                    'prescription': (10, 50),
                    'lab_order': (50, 300),
                    'specialist': (150, 500),
                    'subscription_plan': (29.99, 99.99)
                },
                'insurance_coverage': 0.6,  # 60% use insurance
                'appointment_types': ['immediate', 'scheduled', 'follow_up'],
                'transaction_types': ['appointment', 'copay', 'subscription', 'prescription'],
                'peak_hours': [9, 10, 11, 14, 15, 16],
                'peak_days': [1, 2, 3, 4],
                'no_show_rate': 0.05
            }
        }
        
        if business_type not in business_patterns:
            # Fallback generic pattern for undefined business types
            pattern = {
                'name': business_type.replace('_', ' ').title(),
                'category': 'Generic Online Business',
                'product_categories': {
                    'general': (20, 200),
                    'premium': (100, 500)
                },
                'transaction_types': ['purchase', 'refund', 'subscription'],
                'peak_hours': [10, 11, 19, 20],
                'peak_days': [0, 6],
            }
        else:
            pattern = business_patterns[business_type]
        transactions = []
        
        # Generate enhanced customer pool
        num_customers = min(300, num_transactions // 3)
        customers = [self.generate_customer_profile(business_type) for _ in range(num_customers)]
        
        # Track customer behavior
        customer_behavior = {}
        for customer in customers:
            customer_behavior[customer['customer_id']] = {
                'last_transaction': None,
                'transaction_count': 0,
                'total_spent': 0,
                'products_purchased': [],
                'subscription_status': None,
                'risk_score': random.uniform(0, 20)
            }
        
        # Generate time series
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        
        # Generate transactions with realistic patterns
        for i in range(num_transactions):
            # Select customer with realistic behavior
            if random.random() < 0.3:  # 30% new customers
                customer = self.generate_customer_profile(business_type)
                customers.append(customer)
                customer_behavior[customer['customer_id']] = {
                    'last_transaction': None,
                    'transaction_count': 0,
                    'total_spent': 0,
                    'products_purchased': [],
                    'subscription_status': None,
                    'risk_score': random.uniform(0, 30)
                }
            else:
                # Weighted selection based on customer value
                weights = [c['clv'] for c in customers]
                customer = random.choices(customers, weights=weights)[0]
            
            behavior = customer_behavior[customer['customer_id']]
            
            # Generate transaction timing with timezone consideration
            transaction_time = self._generate_realistic_timestamp(
                start_date, end_date, pattern, customer['timezone'], behavior
            )
            
            # Generate transaction details based on business type
            transaction_details = self._generate_transaction_details(
                business_type, pattern, customer, behavior, transaction_time
            )
            
            # Update customer behavior
            behavior['last_transaction'] = transaction_time
            behavior['transaction_count'] += 1
            behavior['total_spent'] += transaction_details['amount']
            
            # Create transaction record
            transaction = {
                'transaction_id': f"TXN_{datetime.now().strftime('%Y%m%d')}_{i+1:08d}",
                'customer_id': customer['customer_id'],
                'customer_name': customer['name'],
                'customer_email': customer['email'],
                'customer_phone': customer['phone'],
                'customer_address': customer['address'],
                'customer_city': customer['city'],
                'customer_state': customer['state'],
                'customer_zip_code': customer['zip_code'],
                'customer_ip_address': customer['ip_address'],
                'customer_segment': customer['segment'],
                'customer_country': customer['country'],
                'transaction_datetime': transaction_time,
                'transaction_date': transaction_time.strftime('%Y-%m-%d'),
                'transaction_time': transaction_time.strftime('%H:%M:%S'),
                **transaction_details,
                'customer_lifetime_value': customer['clv'],
                'customer_acquisition_channel': customer['acquisition_channel'],
                'days_since_acquisition': (transaction_time.date() - customer['acquisition_date']).days,
                'transaction_count': behavior['transaction_count'],
                'device_type': self._get_device_info(customer['preferred_device']),
                'is_mobile': customer['preferred_device'] == 'mobile',
                'session_duration_seconds': random.randint(30, 1800),
                'pages_viewed': random.randint(1, 20)
            }
            
            transactions.append(transaction)
        
        # Convert to DataFrame and add derived metrics
        df = pd.DataFrame(transactions)
        df = self._add_derived_metrics(df, business_type)
        
        # Generate anomaly test transactions
        anomaly_df = self._generate_anomaly_test_transactions(df, business_type, pattern)
        df = pd.concat([df, anomaly_df], ignore_index=True)
        
        return df
    
    def _generate_realistic_timestamp(self, start_date, end_date, pattern, timezone, behavior):
        """Generate realistic timestamp considering timezone and customer behavior"""
        # If customer has recent transaction, consider purchase frequency
        if behavior['last_transaction']:
            days_since_last = (datetime.now() - behavior['last_transaction']).days
            if days_since_last < 7:
                # Recent customer, higher chance of near-term transaction
                days_offset = random.randint(0, min(30, days_since_last + 7))
            else:
                days_offset = random.randint(0, 180)
        else:
            days_offset = random.randint(0, 365)
        
        base_date = end_date - timedelta(days=days_offset)
        
        # Adjust for timezone
        timezone_offsets = {
            'PST': -8, 'MST': -7, 'CST': -6, 'EST': -5,
            'GMT': 0, 'CET': 1, 'JST': 9, 'AEST': 10,
            'AWST': 8, 'BRT': -3, 'IST': 5.5
        }
        
        # Select hour based on business pattern and timezone
        if 'peak_hours' in pattern:
            local_peak_hours = pattern['peak_hours']
        elif 'peak_times' in pattern:
            # Flatten peak_times structure for food delivery
            local_peak_hours = []
            for time_period, hours in pattern['peak_times'].items():
                local_peak_hours.extend(hours)
        else:
            # Default peak hours if not specified
            local_peak_hours = [9, 10, 11, 14, 15, 16, 19, 20]
            
        if random.random() < 0.7:  # 70% during peak hours
            hour = random.choice(local_peak_hours)
        else:
            hour = random.randint(0, 23)
        
        # Adjust for timezone
        utc_hour = (hour - timezone_offsets.get(timezone, 0)) % 24
        
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        return base_date.replace(hour=int(utc_hour), minute=minute, second=second)
    
    def _generate_transaction_details(self, business_type, pattern, customer, behavior, transaction_time):
        """Generate detailed transaction information based on business type"""
        details = {}
        
        # Common fields
        details['merchant_name'] = pattern['name']
        details['merchant_category'] = pattern['category']
        
        # Business-specific transaction generation
        if 'subscription_tiers' in pattern and (business_type in ['saas_b2b', 'streaming_service'] or 'subscription' in business_type):
            details.update(self._generate_subscription_transaction(pattern, customer, behavior))
        elif 'marketplace' in business_type or business_type in ['digital_marketplace', 'freelance_platform']:
            details.update(self._generate_marketplace_transaction(pattern, customer))
        elif business_type == 'gaming_platform':
            details.update(self._generate_gaming_transaction(pattern, customer, behavior))
        elif business_type == 'crypto_exchange':
            details.update(self._generate_crypto_transaction(pattern, customer))
        elif business_type == 'travel_booking':
            details.update(self._generate_booking_transaction(pattern, customer, transaction_time))
        elif business_type == 'food_delivery_platform':
            details.update(self._generate_food_delivery_transaction(pattern, customer))
        else:
            details.update(self._generate_ecommerce_transaction(pattern, customer))
        
        # Add payment processing details
        details.update(self._generate_payment_details(customer, details['amount'], behavior))
        
        # Add fraud detection
        details.update(self._generate_fraud_indicators(customer, details, behavior, transaction_time))
        
        return details
    
    def _generate_subscription_transaction(self, pattern, customer, behavior):
        """Generate subscription-specific transaction details"""
        details = {}
        
        # Determine transaction type
        valid_tiers = list(pattern['subscription_tiers'].keys())
        if behavior['subscription_status'] is None:
            transaction_type = 'new_subscription'
            # Select tier based on customer segment
            if customer['segment'] == 'enterprise':
                tier = 'enterprise'
            elif customer['segment'] == 'vip':
                tier = 'business'
            else:
                tier = 'starter'
            if tier not in valid_tiers:
                tier = valid_tiers[0]
            behavior['subscription_status'] = {
                'tier': tier,
                'billing_cycle': random.choices(['monthly', 'annual'], weights=[0.6, 0.4])[0],
                'start_date': datetime.now()
            }
        else:
            # Existing subscriber
            transaction_types = ['renewal', 'upgrade', 'addon']
            if behavior['subscription_status']['tier'] != 'enterprise':
                transaction_types.append('upgrade')
            if behavior['subscription_status']['tier'] != 'starter':
                transaction_types.append('downgrade')
            transaction_type = random.choice(transaction_types)
        # Ensure tier is valid before accessing
        tier = behavior['subscription_status']['tier']
        if tier not in valid_tiers:
            tier = valid_tiers[0]
            behavior['subscription_status']['tier'] = tier
        details['transaction_type'] = transaction_type
        details['subscription_tier'] = tier
        details['billing_cycle'] = behavior['subscription_status']['billing_cycle']
        # Calculate amount
        tier_info = pattern['subscription_tiers'][tier]
        base_amount = tier_info['price']
        if behavior['subscription_status']['billing_cycle'] == 'annual':
            base_amount *= 12 * 0.85  # 15% discount for annual
        if transaction_type == 'addon':
            base_amount *= random.uniform(0.1, 0.3)
        details['amount'] = round(base_amount, 2)
        details['mrr_impact'] = base_amount if behavior['subscription_status']['billing_cycle'] == 'monthly' else base_amount / 12
        return details
    
    def _generate_marketplace_transaction(self, pattern, customer):
        """Generate marketplace transaction details"""
        details = {}
        
        # Select product category
        categories = list(pattern.get('product_categories', pattern.get('service_categories', {})).keys())
        category = random.choice(categories)
        
        # Get price range
        price_range = pattern.get('product_categories', pattern.get('service_categories', {}))[category]
        amount = random.uniform(*price_range)
        
        # Apply marketplace fees
        if 'commission_rate' in pattern:
            marketplace_fee = amount * pattern['commission_rate']
            seller_payout = amount - marketplace_fee
        else:
            marketplace_fee = amount * pattern.get('platform_fee', 0.2)
            seller_payout = amount - marketplace_fee
        
        details['transaction_type'] = random.choice(pattern['transaction_types'])
        details['product_category'] = category
        details['amount'] = round(amount, 2)
        details['marketplace_fee'] = round(marketplace_fee, 2)
        details['seller_payout'] = round(seller_payout, 2)
        details['seller_id'] = f"SELL_{fake.random_number(digits=6, fix_len=True)}"
        
        # International transaction
        if random.random() < pattern.get('international_sales', pattern.get('international_transactions', 0.3)):
            details['is_international'] = True
            details['currency'] = random.choice(['EUR', 'GBP', 'CAD', 'AUD'])
            details['exchange_rate'] = self.currency_rates[details['currency']]
            details['amount_usd'] = details['amount']
            details['amount_local'] = round(details['amount'] * details['exchange_rate'], 2)
        else:
            details['is_international'] = False
            details['currency'] = 'USD'
        
        return details
    
    def _generate_gaming_transaction(self, pattern, customer, behavior):
        """Generate gaming platform transaction details"""
        details = {}
        
        # Determine if whale (high spender)
        is_whale = random.random() < pattern['whale_percentage']
        
        # Select transaction category
        if is_whale:
            # Whales prefer virtual currency
            categories = ['virtual_currency_medium', 'virtual_currency_large', 'season_pass']
        else:
            categories = list(pattern['transaction_categories'].keys())
        
        category = random.choice(categories)
        price_range = pattern['transaction_categories'][category]
        
        details['transaction_type'] = category
        details['amount'] = round(random.uniform(*price_range), 2)
        details['is_whale'] = is_whale
        
        # Game-specific details
        details['game_id'] = f"GAME_{random.randint(1000, 9999)}"
        details['platform'] = random.choice(['PC', 'PlayStation', 'Xbox', 'Mobile', 'Switch'])
        details['session_id'] = fake.uuid4()
        
        # In-game metrics
        if 'virtual_currency' in category:
            details['virtual_currency_amount'] = int(details['amount'] * random.uniform(100, 150))
        
        return details
    
    def _generate_crypto_transaction(self, pattern, customer):
        """Generate cryptocurrency exchange transaction details"""
        details = {}
        
        # Select trading pair
        pairs = list(pattern['trading_pairs'].keys())
        pair = random.choice(pairs)
        pair_info = pattern['trading_pairs'][pair]
        
        # Generate trade amount with volatility
        base_amount = random.uniform(pair_info['min'], pair_info['max'])
        volatility = random.uniform(-pair_info['volatility'], pair_info['volatility'])
        amount = base_amount * (1 + volatility)
        
        # Transaction type
        transaction_type = random.choice(pattern['transaction_types'])
        
        if transaction_type in ['buy', 'sell']:
            # Trading fees
            is_maker = random.random() < 0.4
            fee_rate = pattern['fee_structure']['maker'] if is_maker else pattern['fee_structure']['taker']
            fee = amount * fee_rate
        elif transaction_type == 'withdrawal':
            fee = pattern['fee_structure']['withdrawal']['fixed'] + (amount * pattern['fee_structure']['withdrawal']['percentage'])
        else:
            fee = 0
        
        details['transaction_type'] = transaction_type
        details['trading_pair'] = pair
        details['amount'] = round(amount, 2)
        details['fee'] = round(fee, 2)
        details['is_institutional'] = random.random() < pattern['institutional_percentage']
        
        # Add market data
        details['price_usd'] = round(random.uniform(30000, 60000), 2) if 'BTC' in pair else round(random.uniform(2000, 4000), 2)
        details['volume_24h'] = round(random.uniform(1000000, 100000000), 2)
        
        return details
    
    def _generate_booking_transaction(self, pattern, customer, transaction_time):
        """Generate booking platform transaction details"""
        details = {}
        
        # Select booking type
        booking_type = random.choice(list(pattern['booking_types'].keys()))
        price_range = pattern['booking_types'][booking_type]
        
        # Booking window
        window_type = random.choice(list(pattern['booking_window'].keys()))
        days_ahead = random.randint(*pattern['booking_window'][window_type])
        booking_date = transaction_time + timedelta(days=days_ahead)
        
        # Calculate amount with seasonal adjustments
        base_amount = random.uniform(*price_range)
        if booking_date.month in [6, 7, 8, 12]:  # Summer and December
            base_amount *= 1.3
        
        details['transaction_type'] = 'booking'
        details['booking_type'] = booking_type
        details['amount'] = round(base_amount, 2)
        details['booking_date'] = booking_date.strftime('%Y-%m-%d')
        details['days_until_travel'] = days_ahead
        details['booking_window'] = window_type
        
        # Commission for OTA
        if 'commission_rates' in pattern:
            # Map booking type to commission rate key
            commission_key_map = {
                'vacation_package': 'package',
                'car_rental': 'car',
                'travel_insurance': 'activity'  # fallback
            }
            commission_key = commission_key_map.get(booking_type, booking_type)
            
            if commission_key in pattern['commission_rates']:
                commission = base_amount * pattern['commission_rates'][commission_key]
                details['commission'] = round(commission, 2)
                details['net_revenue'] = round(base_amount - commission, 2)
            else:
                # Default commission rate if not found
                commission = base_amount * 0.1
                details['commission'] = round(commission, 2)
                details['net_revenue'] = round(base_amount - commission, 2)
        
        return details
    
    def _generate_food_delivery_transaction(self, pattern, customer):
        """Generate food delivery platform transaction details"""
        details = {}
        
        # Select order category
        categories = list(pattern['order_categories'].keys())
        category = random.choice(categories)
        
        # Get price range for the category
        price_range = pattern['order_categories'][category]
        base_amount = random.uniform(*price_range)
        
        # Add delivery fee
        delivery_fee = random.uniform(*pattern['fees']['delivery'])
        
        # Add service fee (percentage of order)
        service_fee = base_amount * pattern['fees']['service']
        
        # Small order fee if applicable
        small_order_fee = 0
        if base_amount < 20:  # Small order threshold
            small_order_fee = pattern['fees']['small_order']
        
        total_amount = base_amount + delivery_fee + service_fee + small_order_fee
        
        details['transaction_type'] = random.choice(pattern['transaction_types'])
        details['order_category'] = category
        details['subtotal'] = round(base_amount, 2)
        details['delivery_fee'] = round(delivery_fee, 2)
        details['service_fee'] = round(service_fee, 2)
        details['small_order_fee'] = round(small_order_fee, 2)
        details['amount'] = round(total_amount, 2)
        
        # Driver details
        details['driver_id'] = f"DRV_{fake.random_number(digits=6, fix_len=True)}"
        details['driver_payout'] = round(total_amount * pattern['driver_payout_percentage'], 2)
        details['estimated_delivery_time'] = random.randint(15, 60)  # minutes
        
        # Order specifics
        details['items_count'] = random.randint(1, 8)
        details['restaurant_id'] = f"REST_{fake.random_number(digits=5, fix_len=True)}"
        
        return details

    def _generate_ecommerce_transaction(self, pattern, customer):
        """Generate standard e-commerce transaction details"""
        details = {}
        
        # Select product category
        categories = list(pattern.get('product_categories', {}).keys())
        category = random.choice(categories) if categories else 'general'
        
        if 'product_categories' in pattern:
            price_range = pattern['product_categories'][category]
            amount = random.uniform(*price_range)
        else:
            amount = random.uniform(20, 200)
        
        details['transaction_type'] = 'purchase'
        details['product_category'] = category
        details['amount'] = round(amount, 2)
        
        # Cart details
        details['items_in_cart'] = random.randint(1, 5)
        details['cart_total'] = round(amount * random.uniform(1.0, 1.3), 2)
        
        # Shipping for physical products
        if pattern.get('shipping_times'):
            shipping_method = random.choice(list(pattern['shipping_times'].keys()))
            shipping_days = random.randint(*pattern['shipping_times'][shipping_method])
            details['shipping_method'] = shipping_method
            details['estimated_delivery_days'] = shipping_days
            details['shipping_cost'] = round(random.uniform(5, 25), 2)
        
        return details
    
    def _generate_payment_details(self, customer, amount, behavior):
        """Generate payment method and processing details"""
        details = {}
        
        # Select payment method
        payment_method = random.choice(customer['payment_methods'])
        
        if payment_method == 'card':
            card_types = ['visa', 'mastercard', 'amex', 'discover']
            card_type = random.choice(card_types)
            details['payment_method'] = card_type
            details['card_last4'] = fake.random_number(digits=4, fix_len=True)
            details['card_bin'] = fake.random_number(digits=6, fix_len=True)
            details['issuing_bank'] = random.choice(['Chase', 'Bank of America', 'Wells Fargo', 'Citi'])
        elif payment_method == 'crypto':
            details['payment_method'] = 'cryptocurrency'
            details['crypto_currency'] = random.choice(['BTC', 'ETH', 'USDT', 'USDC'])
            details['wallet_address'] = hashlib.sha256(fake.uuid4().encode()).hexdigest()[:42]
        else:
            details['payment_method'] = payment_method
        
        # Payment processor response
        success_rate = 0.95 - (behavior['risk_score'] / 1000)  # Higher risk = lower success
        
        if random.random() < success_rate:
            details['payment_status'] = 'completed'
            details['response_code'] = '00'
            details['response_text'] = 'Approved'
        else:
            details['payment_status'] = 'failed'
            error_codes = {
                '05': 'Do not honor',
                '51': 'Insufficient funds',
                '14': 'Invalid card number',
                '61': 'Exceeds limit'
            }
            details['response_code'] = random.choice(list(error_codes.keys()))
            details['response_text'] = error_codes[details['response_code']]
        
        # Processing time
        details['processing_time_ms'] = random.randint(100, 2000)
        
        return details
    
    def _generate_fraud_indicators(self, customer, transaction_details, behavior, transaction_time):
        """Generate sophisticated fraud detection indicators"""
        fraud_indicators = []
        risk_score = behavior['risk_score']
        
        # Check for suspicious patterns
        if transaction_details['amount'] > customer['clv'] * 0.5:
            fraud_indicators.append('amount_exceeds_normal')
            risk_score += 20
        
        if transaction_time.hour >= 2 and transaction_time.hour <= 5:
            fraud_indicators.append('unusual_hour')
            risk_score += 15
        
        if behavior['transaction_count'] == 1 and transaction_details['amount'] > 500:
            fraud_indicators.append('high_first_transaction')
            risk_score += 25
        
        if 'is_international' in transaction_details and transaction_details['is_international']:
            fraud_indicators.append('international_transaction')
            risk_score += 10
        
        # Velocity checks
        if behavior['last_transaction']:
            hours_since_last = (transaction_time - behavior['last_transaction']).total_seconds() / 3600
            if hours_since_last < 1:
                fraud_indicators.append('rapid_transactions')
                risk_score += 30
        
        # Determine if fraudulent
        fraud_probability = min(risk_score / 200, 0.15)  # Max 15% fraud rate
        is_fraudulent = random.random() < fraud_probability
        
        if is_fraudulent:
            fraud_types = ['card_testing', 'account_takeover', 'synthetic_identity', 'friendly_fraud']
            fraud_type = random.choice(fraud_types)
            fraud_indicators.append(f'fraud_type_{fraud_type}')
        
        return {
            'is_fraudulent': is_fraudulent,
            'fraud_indicators': ','.join(fraud_indicators) if fraud_indicators else '',
            'risk_score': min(risk_score, 100),
            'fraud_type': fraud_type if is_fraudulent else ''
        }
    
    def _get_device_info(self, device_type):
        """Get detailed device information"""
        os_options = self.device_types[device_type]
        os_type = random.choices(list(os_options.keys()), 
                                weights=list(os_options.values()))[0]
        
        device_info = {
            'mobile': {
                'ios': 'iPhone/iOS',
                'android': 'Android Mobile'
            },
            'desktop': {
                'windows': 'Windows PC',
                'mac': 'Mac OS',
                'linux': 'Linux'
            },
            'tablet': {
                'ipad': 'iPad',
                'android': 'Android Tablet'
            }
        }
        
        return device_info[device_type][os_type]
    
    def _add_derived_metrics(self, df, business_type):
        """Add derived metrics and calculations"""
        # Sort by datetime
        df['transaction_datetime'] = pd.to_datetime(df['transaction_datetime'])
        df = df.sort_values('transaction_datetime')
        
        # Customer metrics
        df['customer_transaction_number'] = df.groupby('customer_id').cumcount() + 1
        df['customer_total_spent'] = df.groupby('customer_id')['amount'].cumsum()
        
        # Time-based metrics
        df['hour'] = df['transaction_datetime'].dt.hour
        df['day_of_week'] = df['transaction_datetime'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        df['month'] = df['transaction_datetime'].dt.month
        df['quarter'] = df['transaction_datetime'].dt.quarter
        
        # Business-specific metrics
        if 'subscription' in business_type:
            df['is_renewal'] = df['transaction_type'] == 'renewal'
            df['is_upgrade'] = df['transaction_type'] == 'upgrade'
            
        if 'marketplace' in business_type:
            df['net_revenue'] = df['amount'] - df.get('marketplace_fee', 0)
        
        return df

    def _generate_anomaly_test_transactions(self, df, business_type, pattern):
        """Generate additional transactions specifically designed to trigger anomaly detection"""
        anomaly_transactions = []
        
        # Get some existing customers for anomaly testing
        if len(df) > 0:
            existing_customers = df[['customer_id', 'customer_name', 'customer_email', 'customer_phone', 
                                   'customer_address', 'customer_city', 'customer_state', 
                                   'customer_zip_code', 'customer_ip_address', 'customer_segment', 
                                   'customer_country']].drop_duplicates().head(10)
        else:
            # Create test customers if no existing data
            existing_customers = pd.DataFrame([{
                'customer_id': f"TEST_CUST_{i}",
                'customer_name': fake.name(),
                'customer_email': fake.email(),
                'customer_phone': fake.phone_number(),
                'customer_address': fake.address(),
                'customer_city': fake.city(),
                'customer_state': fake.state(),
                'customer_zip_code': fake.zipcode(),
                'customer_ip_address': fake.ipv4_public(),
                'customer_segment': 'regular',
                'customer_country': 'US'
            } for i in range(10)])
        
        base_time = datetime.now() - timedelta(days=30)
        
        # 1. GEOGRAPHICAL ANOMALIES
        for i in range(3):
            customer = existing_customers.iloc[i % len(existing_customers)]
            
            # ZIP/State mismatch
            geo_anomaly = {
                'transaction_id': f"GEO_ANOM_{i}_{fake.random_number(digits=6)}",
                'customer_id': customer['customer_id'],
                'customer_name': customer['customer_name'],
                'customer_email': customer['customer_email'],
                'customer_phone': customer['customer_phone'],
                'customer_address': customer['customer_address'],
                'customer_city': customer['customer_city'],
                'customer_state': 'CA',  # Wrong state for ZIP
                'customer_zip_code': '10001',  # NY ZIP with CA state
                'customer_ip_address': '8.8.8.8',  # Generic IP that doesn't match location
                'customer_segment': customer['customer_segment'],
                'customer_country': customer['customer_country'],
                'transaction_datetime': base_time + timedelta(hours=i),
                'transaction_date': (base_time + timedelta(hours=i)).strftime('%Y-%m-%d'),
                'transaction_time': (base_time + timedelta(hours=i)).strftime('%H:%M:%S'),
                'merchant_name': pattern['name'],
                'merchant_category': pattern['category'],
                'amount': round(random.uniform(50, 200), 2),
                'payment_method': 'visa',
                'payment_status': 'completed',
                'response_code': '00',
                'response_text': 'Approved',
                'card_last4': '1234',
                'transaction_type': 'purchase',
                'customer_lifetime_value': 1000.0,
                'customer_acquisition_channel': 'organic_search',
                'days_since_acquisition': 30,
                'transaction_count': 1,
                'device_type': 'iPhone/iOS',
                'is_mobile': True,
                'session_duration_seconds': 300,
                'pages_viewed': 5,
                'is_fraudulent': False,
                'fraud_indicators': 'geo_mismatch',
                'risk_score': 45,
                'fraud_type': '',
                'processing_time_ms': 450
            }
            anomaly_transactions.append(geo_anomaly)
        
        # 2. VELOCITY ANOMALIES
        customer = existing_customers.iloc[0]
        for i in range(4):  # 4 transactions within 5 minutes
            velocity_anomaly = {
                'transaction_id': f"VEL_ANOM_{i}_{fake.random_number(digits=6)}",
                'customer_id': customer['customer_id'],
                'customer_name': customer['customer_name'],
                'customer_email': customer['customer_email'],
                'customer_phone': customer['customer_phone'],
                'customer_address': customer['customer_address'],
                'customer_city': customer['customer_city'],
                'customer_state': customer['customer_state'],
                'customer_zip_code': customer['customer_zip_code'],
                'customer_ip_address': customer['customer_ip_address'],
                'customer_segment': customer['customer_segment'],
                'customer_country': customer['customer_country'],
                'transaction_datetime': base_time + timedelta(minutes=i),  # Rapid transactions
                'transaction_date': (base_time + timedelta(minutes=i)).strftime('%Y-%m-%d'),
                'transaction_time': (base_time + timedelta(minutes=i)).strftime('%H:%M:%S'),
                'merchant_name': pattern['name'],
                'merchant_category': pattern['category'],
                'amount': round(50 * (i + 1), 2),  # Escalating amounts
                'payment_method': 'mastercard',
                'payment_status': 'completed',
                'response_code': '00',
                'response_text': 'Approved',
                'card_last4': '5678',
                'transaction_type': 'purchase',
                'customer_lifetime_value': 2000.0,
                'customer_acquisition_channel': 'paid_search',
                'days_since_acquisition': 45,
                'transaction_count': i + 1,
                'device_type': 'Android Mobile',
                'is_mobile': True,
                'session_duration_seconds': 120,
                'pages_viewed': 3,
                'is_fraudulent': False,
                'fraud_indicators': 'rapid_transactions,amount_escalation',
                'risk_score': 65,
                'fraud_type': '',
                'processing_time_ms': 200
            }
            anomaly_transactions.append(velocity_anomaly)
        
        # 3. PAYMENT ANOMALIES
        customer = existing_customers.iloc[1]
        # Failed payment pattern
        for i in range(3):
            payment_anomaly = {
                'transaction_id': f"PAY_ANOM_{i}_{fake.random_number(digits=6)}",
                'customer_id': customer['customer_id'],
                'customer_name': customer['customer_name'],
                'customer_email': customer['customer_email'],
                'customer_phone': customer['customer_phone'],
                'customer_address': customer['customer_address'],
                'customer_city': customer['customer_city'],
                'customer_state': customer['customer_state'],
                'customer_zip_code': customer['customer_zip_code'],
                'customer_ip_address': customer['customer_ip_address'],
                'customer_segment': customer['customer_segment'],
                'customer_country': customer['customer_country'],
                'transaction_datetime': base_time + timedelta(hours=i + 1),
                'transaction_date': (base_time + timedelta(hours=i + 1)).strftime('%Y-%m-%d'),
                'transaction_time': (base_time + timedelta(hours=i + 1)).strftime('%H:%M:%S'),
                'merchant_name': pattern['name'],
                'merchant_category': pattern['category'],
                'amount': round(random.uniform(100, 300), 2),
                'payment_method': 'visa',
                'payment_status': 'failed',
                'response_code': '51',  # Insufficient funds
                'response_text': 'Insufficient funds',
                'card_last4': '1111',  # Sequential pattern
                'transaction_type': 'purchase',
                'customer_lifetime_value': 500.0,
                'customer_acquisition_channel': 'social_media',
                'days_since_acquisition': 10,
                'transaction_count': i + 1,
                'device_type': 'Windows PC',
                'is_mobile': False,
                'session_duration_seconds': 600,
                'pages_viewed': 8,
                'is_fraudulent': False,
                'fraud_indicators': 'failed_payments,sequential_card',
                'risk_score': 70,
                'fraud_type': '',
                'processing_time_ms': 1500
            }
            anomaly_transactions.append(payment_anomaly)
        
        # 4. BEHAVIORAL ANOMALIES
        customer = existing_customers.iloc[2]
        behavioral_anomalies = [
            # Round amount testing
            {
                'amount': 100.00,  # Exact round amount
                'merchant_category': 'Electronics'
            },
            {
                'amount': 1.00,  # Fraud testing amount
                'merchant_category': 'Groceries'  # Different category
            },
            {
                'amount': 0.01,  # Another fraud testing amount
                'merchant_category': 'Gas Stations'  # Another different category
            }
        ]
        
        for i, behavioral in enumerate(behavioral_anomalies):
            behavioral_anomaly = {
                'transaction_id': f"BEH_ANOM_{i}_{fake.random_number(digits=6)}",
                'customer_id': customer['customer_id'],
                'customer_name': customer['customer_name'],
                'customer_email': customer['customer_email'],
                'customer_phone': customer['customer_phone'],
                'customer_address': customer['customer_address'],
                'customer_city': customer['customer_city'],
                'customer_state': customer['customer_state'],
                'customer_zip_code': customer['customer_zip_code'],
                'customer_ip_address': customer['customer_ip_address'],
                'customer_segment': customer['customer_segment'],
                'customer_country': customer['customer_country'],
                'transaction_datetime': base_time + timedelta(hours=i + 5),
                'transaction_date': (base_time + timedelta(hours=i + 5)).strftime('%Y-%m-%d'),
                'transaction_time': (base_time + timedelta(hours=i + 5)).strftime('%H:%M:%S'),
                'merchant_name': pattern['name'],
                'merchant_category': behavioral['merchant_category'],
                'amount': behavioral['amount'],
                'payment_method': 'amex',
                'payment_status': 'completed',
                'response_code': '00',
                'response_text': 'Approved',
                'card_last4': '9999',
                'transaction_type': 'purchase',
                'customer_lifetime_value': 1500.0,
                'customer_acquisition_channel': 'email',
                'days_since_acquisition': 60,
                'transaction_count': i + 1,
                'device_type': 'iPad',
                'is_mobile': False,
                'session_duration_seconds': 240,
                'pages_viewed': 2,
                'is_fraudulent': False,
                'fraud_indicators': 'round_amount,category_hopping,fraud_testing',
                'risk_score': 55,
                'fraud_type': '',
                'processing_time_ms': 350
            }
            anomaly_transactions.append(behavioral_anomaly)
        
        # 5. TEMPORAL ANOMALIES
        customer = existing_customers.iloc[3]
        temporal_times = [
            (3, 0, 0),   # 3:00 AM - Weekend night
            (2, 30, 0),  # 2:30 AM - Weekend night
            (23, 0, 0),  # 11:00 PM - Exact hour
            (1, 0, 0),   # 1:00 AM - Exact hour
        ]
        
        for i, (hour, minute, second) in enumerate(temporal_times):
            # Make it a weekend (Saturday)
            weekend_time = base_time.replace(hour=hour, minute=minute, second=second)
            days_ahead = (5 - weekend_time.weekday()) % 7  # Get to Saturday
            weekend_time = weekend_time + timedelta(days=days_ahead)
            
            temporal_anomaly = {
                'transaction_id': f"TEMP_ANOM_{i}_{fake.random_number(digits=6)}",
                'customer_id': customer['customer_id'],
                'customer_name': customer['customer_name'],
                'customer_email': customer['customer_email'],
                'customer_phone': customer['customer_phone'],
                'customer_address': customer['customer_address'],
                'customer_city': customer['customer_city'],
                'customer_state': customer['customer_state'],
                'customer_zip_code': customer['customer_zip_code'],
                'customer_ip_address': customer['customer_ip_address'],
                'customer_segment': customer['customer_segment'],
                'customer_country': customer['customer_country'],
                'transaction_datetime': weekend_time,
                'transaction_date': weekend_time.strftime('%Y-%m-%d'),
                'transaction_time': weekend_time.strftime('%H:%M:%S'),
                'merchant_name': pattern['name'],
                'merchant_category': pattern['category'],
                'amount': round(random.uniform(75, 250), 2),
                'payment_method': 'discover',
                'payment_status': 'completed',
                'response_code': '00',
                'response_text': 'Approved',
                'card_last4': '4444',
                'transaction_type': 'purchase',
                'customer_lifetime_value': 800.0,
                'customer_acquisition_channel': 'referral',
                'days_since_acquisition': 90,
                'transaction_count': i + 1,
                'device_type': 'Mac OS',
                'is_mobile': False,
                'session_duration_seconds': 180,
                'pages_viewed': 4,
                'is_fraudulent': False,
                'fraud_indicators': 'weekend_night,exact_hour,off_hours',
                'risk_score': 50,
                'fraud_type': '',
                'processing_time_ms': 600
            }
            anomaly_transactions.append(temporal_anomaly)
        
        # 6. DATA QUALITY ANOMALIES
        data_quality_anomalies = [
            {
                'customer_name': 'TEST USER',  # Suspicious name
                'customer_email': 'test@10minutemail.com',  # Temporary email
                'card_last4': '1234'  # Sequential
            },
            {
                'customer_name': 'John123',  # Name with numbers
                'customer_email': 'fake@guerrillamail.com',  # Temporary email
                'card_last4': '2345'  # Sequential
            },
            {
                'customer_name': 'FRAUD TEST',  # All caps suspicious
                'customer_email': 'temp@tempmail.org',  # Temporary email
                'card_last4': '3456'  # Sequential
            }
        ]
        
        for i, quality_data in enumerate(data_quality_anomalies):
            quality_anomaly = {
                'transaction_id': f"QUAL_ANOM_{i}_{fake.random_number(digits=6)}",
                'customer_id': f"QUAL_CUST_{i}",
                'customer_name': quality_data['customer_name'],
                'customer_email': quality_data['customer_email'],
                'customer_phone': fake.phone_number(),
                'customer_address': fake.address(),
                'customer_city': fake.city(),
                'customer_state': fake.state(),
                'customer_zip_code': fake.zipcode(),
                'customer_ip_address': fake.ipv4_public(),
                'customer_segment': 'new',
                'customer_country': 'US',
                'transaction_datetime': base_time + timedelta(hours=i + 10),
                'transaction_date': (base_time + timedelta(hours=i + 10)).strftime('%Y-%m-%d'),
                'transaction_time': (base_time + timedelta(hours=i + 10)).strftime('%H:%M:%S'),
                'merchant_name': pattern['name'],
                'merchant_category': pattern['category'],
                'amount': round(random.uniform(30, 150), 2),
                'payment_method': 'visa',
                'payment_status': 'completed',
                'response_code': '00',
                'response_text': 'Approved',
                'card_last4': quality_data['card_last4'],
                'transaction_type': 'purchase',
                'customer_lifetime_value': 200.0,
                'customer_acquisition_channel': 'direct',
                'days_since_acquisition': 1,
                'transaction_count': 1,
                'device_type': 'Windows PC',
                'is_mobile': False,
                'session_duration_seconds': 90,
                'pages_viewed': 1,
                'is_fraudulent': False,
                'fraud_indicators': 'suspicious_name,temp_email,sequential_data',
                'risk_score': 75,
                'fraud_type': '',
                'processing_time_ms': 800
            }
            anomaly_transactions.append(quality_anomaly)
        
        return pd.DataFrame(anomaly_transactions)

# Example usage function
def generate_modern_business_data(business_type='saas_b2b', num_transactions=1000):
    """Generate transaction data for a specific modern business type"""
    generator = EnhancedTransactionGenerator()
    return generator.generate_enhanced_transaction_data(num_transactions, business_type)

# Main execution
if __name__ == "__main__":
    # List of modern business types to generate
    modern_businesses = [
        'saas_b2b', 'streaming_service', 'online_education',
        'digital_marketplace', 'freelance_platform', 'gaming_platform',
        'payment_processor', 'crypto_exchange', 'dropshipping_store',
        'subscription_box', 'travel_booking', 'food_delivery_platform',
        'telehealth_platform',
        'mobile_app_store', 'influencer_platform', 'online_fitness',
        'digital_publishing', 'virtual_events', 'online_consulting',
        'crowdfunding_platform', 'remote_work_tool', 'online_tutoring',
        'digital_art_marketplace', 'podcast_platform', 'online_music_store',
        'virtual_reality_platform', 'online_pet_services', 'e-learning_kids',
        'online_grocery', 'subscription_meal_kit', 'online_therapy',
        'digital_ticketing', 'online_auction', 'virtual_conference',
        'online_language_learning', 'digital_gift_cards', 'online_home_services'
    ]
    
    print("🚀 Generating Enhanced Modern Business Transaction Data")
    print("=" * 70)
    
    # Create output directory
    output_dir = 'modern_business_transactions'
    os.makedirs(output_dir, exist_ok=True)
    
    for business in modern_businesses:
        print(f"\n📊 Generating {business} transactions...")
        # Increase transaction count for more robust testing
        df = generate_modern_business_data(business, num_transactions=10000)
        # Save to CSV
        filename = os.path.join(output_dir, f'{business}_transactions.csv')
        df.to_csv(filename, index=False)
        # Display summary statistics
        print(f"  ✓ Total transactions: {len(df):,}")
        print(f"  ✓ Unique customers: {df['customer_id'].nunique():,}")
        print(f"  ✓ Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
        print(f"  ✓ Average transaction: ${df['amount'].mean():.2f}")
        print(f"  ✓ Total revenue: ${df['amount'].sum():,.2f}")
        print(f"  ✓ Fraud rate: {df['is_fraudulent'].mean() * 100:.2f}%")
        print(f"  ✓ Payment success rate: {(df['payment_status'] == 'completed').mean() * 100:.1f}%")
        print(f"  ✓ Saved to: {filename}")
    
    print("\n" + "=" * 70)
    print("✅ Enhanced transaction generation complete!")
    print(f"📁 Files saved to: {output_dir}/")
    print("\n🎯 Available modern business types:")
    for i, business in enumerate(modern_businesses, 1):
        print(f"  {i}. {business}")

