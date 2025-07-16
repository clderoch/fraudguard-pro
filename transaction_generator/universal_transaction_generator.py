# Universal Transaction Data Generator for All Industries
# Comprehensive business transaction simulator supporting 100+ business types
# Designed for fraud detection systems across all major industry verticals

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import json
import hashlib
import time

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Mock Faker functionality if not available
class MockFaker:
    def name(self): return f"Customer {random.randint(1000, 9999)}"
    def email(self): return f"user{random.randint(100, 999)}@example.com"
    def phone_number(self): return f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    def address(self): return f"{random.randint(100, 999)} Main St, City, State"
    def city(self): return random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
    def state(self): return random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI'])
    def zipcode(self): return f"{random.randint(10000, 99999)}"
    def postcode(self): return self.zipcode()
    def ipv4_public(self): return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    def uuid4(self): return f"uuid-{random.randint(10000000, 99999999)}"
    def random_number(self, digits=6, fix_len=True): return random.randint(10**(digits-1), 10**digits-1)
    def date_between(self, start_date='-1y', end_date='today'):
        if start_date == '-1y':
            start = datetime.now() - timedelta(days=365)
        elif start_date == '-2y':
            start = datetime.now() - timedelta(days=730)
        elif start_date == '-3y':
            start = datetime.now() - timedelta(days=1095)
        else:
            start = datetime.now() - timedelta(days=365)
        
        if end_date == 'today':
            end = datetime.now()
        else:
            end = datetime.now()
        
        delta = end - start
        random_days = random.randint(0, delta.days)
        return (start + timedelta(days=random_days)).date()

fake = MockFaker()

class UniversalTransactionGenerator:
    def __init__(self):
        # Global currency rates (updated regularly in real implementation)
        self.currency_rates = {
            'USD': 1.0, 'EUR': 0.85, 'GBP': 0.73, 'CAD': 1.25, 'AUD': 1.35, 
            'JPY': 110.0, 'CNY': 6.5, 'INR': 75.0, 'BRL': 5.2, 'MXN': 18.0,
            'CHF': 0.92, 'SEK': 8.5, 'NOK': 8.7, 'DKK': 6.3, 'PLN': 3.9,
            'CZK': 21.5, 'HUF': 295.0, 'RUB': 74.0, 'TRY': 8.5, 'ZAR': 14.5
        }
        
        # Enhanced device ecosystem
        self.device_types = {
            'mobile': {'ios': 0.52, 'android': 0.48},
            'desktop': {'windows': 0.68, 'mac': 0.22, 'linux': 0.08, 'chromeos': 0.02},
            'tablet': {'ipad': 0.65, 'android': 0.30, 'windows': 0.05},
            'smart_tv': {'roku': 0.35, 'apple_tv': 0.25, 'fire_tv': 0.20, 'google_tv': 0.20},
            'gaming_console': {'playstation': 0.40, 'xbox': 0.35, 'nintendo': 0.25},
            'wearable': {'apple_watch': 0.55, 'android_wear': 0.25, 'fitbit': 0.15, 'garmin': 0.05}
        }
        
        # Global timezone mapping
        self.timezones = {
            'US': ['EST', 'CST', 'MST', 'PST', 'AKST', 'HST'],
            'CA': ['EST', 'CST', 'MST', 'PST'],
            'GB': ['GMT'], 'DE': ['CET'], 'FR': ['CET'], 'ES': ['CET'],
            'JP': ['JST'], 'AU': ['AEST', 'AWST'], 'BR': ['BRT'],
            'IN': ['IST'], 'CN': ['CST'], 'RU': ['MSK'],
            'ZA': ['SAST'], 'MX': ['CST', 'MST', 'PST']
        }
        
        # Enhanced marketing channels
        self.marketing_channels = {
            'organic_search': {'weight': 0.25, 'cost_per_acquisition': (0, 5)},
            'paid_search': {'weight': 0.18, 'cost_per_acquisition': (15, 45)},
            'social_media_organic': {'weight': 0.15, 'cost_per_acquisition': (0, 3)},
            'social_media_paid': {'weight': 0.12, 'cost_per_acquisition': (8, 25)},
            'email_marketing': {'weight': 0.08, 'cost_per_acquisition': (2, 8)},
            'direct_traffic': {'weight': 0.07, 'cost_per_acquisition': (0, 1)},
            'referral': {'weight': 0.06, 'cost_per_acquisition': (5, 15)},
            'affiliate': {'weight': 0.04, 'cost_per_acquisition': (20, 60)},
            'influencer': {'weight': 0.03, 'cost_per_acquisition': (25, 100)},
            'content_marketing': {'weight': 0.02, 'cost_per_acquisition': (10, 30)}
        }
    
    def get_comprehensive_business_patterns(self):
        """Get business patterns for all major industry verticals"""
        return {
            # =================================================================
            # TECHNOLOGY & SOFTWARE
            # =================================================================
            'saas_b2b': {
                'name': 'CloudSync Enterprise',
                'category': 'B2B SaaS Platform',
                'industry': 'Technology',
                'subscription_tiers': {
                    'starter': {'price': 49, 'users': 10},
                    'professional': {'price': 149, 'users': 50},
                    'business': {'price': 399, 'users': 200},
                    'enterprise': {'price': 1299, 'users': 'unlimited'}
                },
                'billing_cycles': {'monthly': 0.5, 'annual': 0.4, 'quarterly': 0.1},
                'transaction_types': ['new_subscription', 'renewal', 'upgrade', 'downgrade', 'addon'],
                'peak_hours': [9, 10, 11, 13, 14, 15, 16],
                'peak_days': [1, 2, 3, 4],
                'churn_rate': 0.05,
                'trial_conversion': 0.18
            },
            
            'cybersecurity_platform': {
                'name': 'SecureShield Pro',
                'category': 'Cybersecurity Solutions',
                'industry': 'Technology',
                'service_tiers': {
                    'endpoint_protection': {'price': 15, 'per': 'device'},
                    'network_security': {'price': 299, 'per': 'month'},
                    'threat_intelligence': {'price': 999, 'per': 'month'}
                },
                'transaction_types': ['license_purchase', 'support_renewal', 'consulting'],
                'peak_hours': [8, 9, 10, 13, 14, 15],
                'enterprise_percentage': 0.7
            },

            # =================================================================
            # E-COMMERCE & RETAIL
            # =================================================================
            'fashion_ecommerce': {
                'name': 'StyleHub Fashion',
                'category': 'Fashion E-commerce',
                'industry': 'Retail',
                'product_categories': {
                    'womens_clothing': (25, 150),
                    'mens_clothing': (30, 120),
                    'shoes': (40, 200),
                    'accessories': (15, 80),
                    'luxury_items': (200, 1500)
                },
                'transaction_types': ['purchase', 'return', 'exchange'],
                'return_rate': 0.25,
                'peak_hours': [12, 13, 19, 20, 21],
                'peak_days': [0, 6]
            },
            
            'electronics_store': {
                'name': 'TechMart Electronics',
                'category': 'Electronics Retail',
                'industry': 'Retail',
                'product_categories': {
                    'smartphones': (200, 1200),
                    'laptops': (500, 3000),
                    'gaming': (50, 600),
                    'smart_home': (25, 300),
                    'accessories': (10, 100)
                },
                'transaction_types': ['purchase', 'warranty', 'repair'],
                'warranty_rate': 0.3,
                'peak_hours': [10, 11, 19, 20],
                'peak_days': [0, 6]
            },

            # =================================================================
            # HEALTHCARE & MEDICAL
            # =================================================================
            'telehealth_platform': {
                'name': 'HealthConnect Virtual',
                'category': 'Telehealth Services',
                'industry': 'Healthcare',
                'service_types': {
                    'general_consultation': (75, 150),
                    'specialist_consultation': (150, 300),
                    'therapy_session': (80, 200),
                    'prescription_consultation': (25, 60)
                },
                'transaction_types': ['appointment', 'consultation', 'prescription'],
                'insurance_coverage': 0.65,
                'peak_hours': [8, 9, 17, 18, 19],
                'no_show_rate': 0.08
            },
            
            'pharmacy_online': {
                'name': 'MedExpress Pharmacy',
                'category': 'Online Pharmacy',
                'industry': 'Healthcare',
                'product_categories': {
                    'prescription_drugs': (10, 200),
                    'otc_medications': (5, 50),
                    'health_supplements': (15, 80),
                    'medical_devices': (20, 300)
                },
                'transaction_types': ['prescription_fill', 'otc_purchase', 'subscription'],
                'insurance_percentage': 0.8,
                'peak_hours': [9, 10, 11, 16, 17]
            },

            # =================================================================
            # FINANCIAL SERVICES
            # =================================================================
            'fintech_payment_app': {
                'name': 'PayFlow Mobile',
                'category': 'Digital Payment Platform',
                'industry': 'Financial Services',
                'transaction_types': {
                    'peer_to_peer': (5, 500),
                    'bill_payment': (25, 2000),
                    'merchant_payment': (10, 1000)
                },
                'fee_structure': {
                    'standard_transfer': 0,
                    'instant_transfer': 1.75,
                    'international': 0.02
                },
                'verification_levels': ['basic', 'verified', 'premium'],
                'peak_hours': [8, 12, 17, 18, 19]
            },
            
            'crypto_exchange': {
                'name': 'CryptoTrade Pro',
                'category': 'Cryptocurrency Exchange',
                'industry': 'Financial Services',
                'trading_pairs': {
                    'BTC/USD': {'min': 100, 'max': 100000, 'volatility': 0.05},
                    'ETH/USD': {'min': 50, 'max': 50000, 'volatility': 0.07},
                    'USDT/USD': {'min': 10, 'max': 100000, 'volatility': 0.001}
                },
                'transaction_types': ['buy', 'sell', 'deposit', 'withdrawal'],
                'fee_structure': {'maker': 0.001, 'taker': 0.002},
                'peak_hours': list(range(24))  # 24/7 market
            },

            # =================================================================
            # EDUCATION & LEARNING
            # =================================================================
            'online_education': {
                'name': 'LearnMaster Academy',
                'category': 'Online Education',
                'industry': 'Education',
                'course_categories': {
                    'technology': (29, 299),
                    'business': (39, 399),
                    'creative_arts': (25, 199),
                    'language_learning': (15, 149)
                },
                'transaction_types': ['course_purchase', 'subscription', 'certification'],
                'completion_rate': 0.32,
                'peak_hours': [18, 19, 20, 21],
                'peak_days': [0, 1, 6]
            },
            
            'tutoring_platform': {
                'name': 'TutorConnect Pro',
                'category': 'Online Tutoring',
                'industry': 'Education',
                'subject_areas': {
                    'mathematics': (25, 80),
                    'science': (30, 85),
                    'languages': (20, 70),
                    'test_prep': (40, 120)
                },
                'transaction_types': ['session_booking', 'package_purchase', 'subscription'],
                'platform_commission': 0.2,
                'peak_hours': [16, 17, 18, 19, 20]
            },

            # =================================================================
            # ENTERTAINMENT & MEDIA
            # =================================================================
            'streaming_service': {
                'name': 'StreamVibe Plus',
                'category': 'Video Streaming',
                'industry': 'Entertainment',
                'subscription_tiers': {
                    'basic': {'price': 8.99, 'quality': 'SD'},
                    'standard': {'price': 13.99, 'quality': 'HD'},
                    'premium': {'price': 17.99, 'quality': '4K'}
                },
                'transaction_types': ['new_subscription', 'renewal', 'upgrade'],
                'content_types': ['movies', 'tv_series', 'documentaries'],
                'peak_hours': [19, 20, 21, 22],
                'churn_rate': 0.06
            },
            
            'gaming_platform': {
                'name': 'GameVerse Pro',
                'category': 'Gaming Platform',
                'industry': 'Entertainment',
                'transaction_categories': {
                    'game_purchase': (9.99, 69.99),
                    'dlc_content': (4.99, 29.99),
                    'virtual_currency': (0.99, 199.99),
                    'subscription': (9.99, 19.99)
                },
                'transaction_types': ['purchase', 'in_game_purchase', 'subscription'],
                'platforms': ['PC', 'PlayStation', 'Xbox', 'Mobile'],
                'peak_hours': [18, 19, 20, 21, 22, 23]
            },

            # =================================================================
            # TRAVEL & HOSPITALITY
            # =================================================================
            'travel_booking': {
                'name': 'WanderBook Travel',
                'category': 'Online Travel Agency',
                'industry': 'Travel',
                'booking_types': {
                    'flights': (150, 2500),
                    'hotels': (80, 800),
                    'packages': (500, 8000),
                    'car_rentals': (30, 200)
                },
                'transaction_types': ['booking', 'cancellation', 'modification'],
                'commission_rates': {'flight': 0.05, 'hotel': 0.15},
                'peak_hours': [9, 10, 11, 19, 20, 21],
                'seasonal_peaks': True
            },
            
            'hotel_management': {
                'name': 'LuxStay Hotels',
                'category': 'Hotel Management',
                'industry': 'Hospitality',
                'room_types': {
                    'standard': (89, 149),
                    'deluxe': (129, 249),
                    'suite': (199, 399),
                    'luxury': (399, 999)
                },
                'transaction_types': ['room_booking', 'service_charge', 'amenity'],
                'occupancy_rate': 0.75,
                'peak_hours': [14, 15, 16, 17]  # Check-in times
            },

            # =================================================================
            # FOOD & RESTAURANT
            # =================================================================
            'food_delivery': {
                'name': 'QuickEats Delivery',
                'category': 'Food Delivery Platform',
                'industry': 'Food Service',
                'order_categories': {
                    'fast_food': (12, 35),
                    'restaurant': (25, 80),
                    'groceries': (30, 200),
                    'convenience': (5, 40)
                },
                'transaction_types': ['order', 'tip', 'subscription_fee'],
                'delivery_fee': (2.99, 6.99),
                'peak_times': {'lunch': [11, 12, 13], 'dinner': [18, 19, 20]}
            },
            
            'restaurant_pos': {
                'name': 'RestaurantHub POS',
                'category': 'Restaurant Point of Sale',
                'industry': 'Food Service',
                'meal_types': {
                    'appetizers': (8, 18),
                    'entrees': (15, 45),
                    'desserts': (6, 15),
                    'beverages': (3, 12)
                },
                'transaction_types': ['dine_in', 'takeout', 'delivery'],
                'tip_percentage': 0.18,
                'peak_hours': [11, 12, 13, 18, 19, 20]
            },

            # =================================================================
            # PROFESSIONAL SERVICES
            # =================================================================
            'legal_services': {
                'name': 'LegalConnect Pro',
                'category': 'Legal Services',
                'industry': 'Professional Services',
                'service_types': {
                    'consultation': (150, 400),
                    'document_prep': (200, 800),
                    'litigation': (500, 2000)
                },
                'transaction_types': ['consultation', 'retainer', 'hourly_billing'],
                'billing_methods': ['hourly', 'flat_fee', 'retainer'],
                'peak_hours': [9, 10, 11, 14, 15, 16]
            },
            
            'accounting_software': {
                'name': 'BookKeeper Pro',
                'category': 'Accounting Software',
                'industry': 'Professional Services',
                'subscription_tiers': {
                    'freelancer': {'price': 15},
                    'small_business': {'price': 45},
                    'enterprise': {'price': 180}
                },
                'transaction_types': ['subscription', 'add_on', 'professional_service'],
                'add_on_services': {'payroll': 40, 'tax_prep': 120},
                'peak_hours': [9, 10, 14, 15, 16]
            },

            # =================================================================
            # AUTOMOTIVE & TRANSPORTATION
            # =================================================================
            'ride_sharing': {
                'name': 'RideConnect',
                'category': 'Ride Sharing',
                'industry': 'Transportation',
                'ride_types': {
                    'standard': (8, 25),
                    'premium': (12, 40),
                    'xl_group': (15, 50)
                },
                'transaction_types': ['ride_payment', 'tip', 'cancellation_fee'],
                'surge_pricing': {'normal': 1.0, 'high_demand': 1.5, 'peak': 2.0},
                'peak_hours': [7, 8, 17, 18, 22, 23]
            },
            
            'auto_parts': {
                'name': 'AutoParts Direct',
                'category': 'Auto Parts E-commerce',
                'industry': 'Automotive',
                'part_categories': {
                    'engine_parts': (25, 500),
                    'brake_components': (30, 200),
                    'electrical': (15, 150),
                    'body_parts': (40, 800)
                },
                'transaction_types': ['parts_purchase', 'warranty', 'installation'],
                'b2b_percentage': 0.4,
                'peak_hours': [8, 9, 10, 16, 17]
            },

            # =================================================================
            # NON-PROFIT & SOCIAL IMPACT
            # =================================================================
            'donation_platform': {
                'name': 'GiveHope Foundation',
                'category': 'Donation Platform',
                'industry': 'Non-Profit',
                'donation_types': {
                    'one_time': (5, 5000),
                    'monthly_recurring': (10, 500),
                    'annual_recurring': (100, 10000)
                },
                'transaction_types': ['donation', 'recurring_setup', 'fundraiser'],
                'cause_categories': ['education', 'healthcare', 'environment'],
                'processing_fee': 0.029,
                'peak_hours': [10, 11, 19, 20]
            },
            
            'crowdfunding': {
                'name': 'FundMyIdea',
                'category': 'Crowdfunding Platform',
                'industry': 'Non-Profit',
                'campaign_types': {
                    'creative_projects': (500, 50000),
                    'technology': (10000, 500000),
                    'community': (1000, 25000)
                },
                'transaction_types': ['campaign_pledge', 'platform_fee', 'payout'],
                'platform_fee': 0.05,
                'funding_models': ['all_or_nothing', 'flexible'],
                'peak_hours': [10, 11, 19, 20, 21]
            }
        }
    
    def generate_customer_profile(self, business_type, region='US'):
        """Generate comprehensive customer profile"""
        customer_id = f"CUST_{fake.random_number(digits=8, fix_len=True)}"
        
        # Get business pattern for context
        patterns = self.get_comprehensive_business_patterns()
        pattern = patterns.get(business_type, {})
        industry = pattern.get('industry', 'Technology')
        
        # Regional settings
        timezone = random.choice(self.timezones.get(region, ['EST']))
        
        # Industry-specific customer segmentation
        if industry == 'Technology':
            segments = ['startup', 'smb', 'enterprise', 'individual']
            clv_ranges = {'startup': (1000, 10000), 'smb': (5000, 50000), 
                         'enterprise': (50000, 500000), 'individual': (100, 2000)}
        elif industry == 'Healthcare':
            segments = ['individual', 'family', 'corporate', 'professional']
            clv_ranges = {'individual': (200, 2000), 'family': (500, 5000),
                         'corporate': (5000, 50000), 'professional': (1000, 15000)}
        else:
            segments = ['new', 'regular', 'vip', 'enterprise']
            clv_ranges = {'new': (100, 1000), 'regular': (1000, 5000),
                         'vip': (5000, 25000), 'enterprise': (25000, 250000)}
        
        segment = random.choice(segments)
        clv_range = clv_ranges.get(segment, (100, 1000))
        clv = random.uniform(*clv_range)
        
        # Device preferences
        device_types = list(self.device_types.keys())
        device_weights = [0.6, 0.3, 0.08, 0.015, 0.003, 0.002][:len(device_types)]
        preferred_device = random.choices(device_types, weights=device_weights)[0]
        
        # Marketing attribution
        channel_data = random.choices(
            list(self.marketing_channels.keys()),
            weights=[channel['weight'] for channel in self.marketing_channels.values()]
        )[0]
        
        acquisition_cost = random.uniform(*self.marketing_channels[channel_data]['cost_per_acquisition'])
        
        return {
            'customer_id': customer_id,
            'name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'segment': segment,
            'industry_segment': industry,
            'clv': clv,
            'acquisition_cost': acquisition_cost,
            'acquisition_date': fake.date_between(start_date='-3y', end_date='today'),
            'acquisition_channel': channel_data,
            'preferred_device': preferred_device,
            'country': region,
            'city': fake.city(),
            'state': fake.state(),
            'zip_code': fake.zipcode(),
            'timezone': timezone,
            'language': self._get_language_for_region(region),
            'payment_methods': self._get_payment_methods_for_region(region),
            'address': fake.address(),
            'ip_address': fake.ipv4_public()
        }
    
    def _get_language_for_region(self, region):
        """Get appropriate language for region"""
        language_map = {
            'US': 'en', 'CA': random.choice(['en', 'fr']), 'GB': 'en',
            'DE': 'de', 'FR': 'fr', 'ES': 'es', 'JP': 'ja',
            'BR': 'pt', 'IN': random.choice(['en', 'hi']), 'CN': 'zh'
        }
        return language_map.get(region, 'en')
    
    def _get_payment_methods_for_region(self, region):
        """Get region-appropriate payment methods"""
        base_methods = ['card', 'paypal']
        regional_methods = {
            'US': ['apple_pay', 'google_pay', 'venmo'],
            'EU': ['sepa', 'ideal', 'sofort'],
            'JP': ['konbini', 'bank_transfer'],
            'CN': ['alipay', 'wechat_pay'],
            'IN': ['upi', 'paytm']
        }
        methods = base_methods + regional_methods.get(region, ['bank_transfer'])
        return random.sample(methods, k=random.randint(2, min(4, len(methods))))
    
    def generate_transaction_data(self, num_transactions=5000, business_type='saas_b2b', region='US'):
        """Generate comprehensive transaction data"""
        
        patterns = self.get_comprehensive_business_patterns()
        if business_type not in patterns:
            # Create basic pattern for unknown types
            pattern = {
                'name': business_type.replace('_', ' ').title(),
                'category': 'General Business',
                'industry': 'Technology',
                'transaction_types': ['purchase', 'subscription', 'service'],
                'peak_hours': [9, 10, 11, 14, 15, 16],
                'peak_days': [1, 2, 3, 4]
            }
        else:
            pattern = patterns[business_type]
        
        transactions = []
        
        # Generate customer pool
        num_customers = min(1000, num_transactions // 3)
        customers = [self.generate_customer_profile(business_type, region) for _ in range(num_customers)]
        
        # Customer behavior tracking
        customer_behavior = {}
        for customer in customers:
            customer_behavior[customer['customer_id']] = {
                'transaction_count': 0,
                'total_spent': 0,
                'last_transaction': None,
                'risk_score': random.uniform(0, 25)
            }
        
        # Time range
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        
        print(f"Generating {num_transactions:,} transactions for {pattern['name']}...")
        
        for i in range(num_transactions):
            if i % 1000 == 0 and i > 0:
                print(f"  Progress: {i:,}/{num_transactions:,} ({i/num_transactions*100:.1f}%)")
            
            # Select customer
            if random.random() < 0.3:  # 30% new customers
                customer = self.generate_customer_profile(business_type, region)
                customers.append(customer)
                customer_behavior[customer['customer_id']] = {
                    'transaction_count': 0, 'total_spent': 0,
                    'last_transaction': None, 'risk_score': random.uniform(0, 30)
                }
            else:
                customer = random.choice(customers)
            
            behavior = customer_behavior[customer['customer_id']]
            
            # Generate transaction timing
            transaction_time = self._generate_realistic_timestamp(start_date, end_date, pattern, customer)
            
            # Generate transaction details
            transaction_details = self._generate_transaction_details(business_type, pattern, customer, behavior)
            
            # Update behavior
            behavior['transaction_count'] += 1
            behavior['total_spent'] += transaction_details.get('amount', 0)
            behavior['last_transaction'] = transaction_time
            
            # Create transaction record
            transaction = {
                'transaction_id': f"TXN_{transaction_time.strftime('%Y%m%d')}_{i+1:08d}",
                'customer_id': customer['customer_id'],
                'customer_name': customer['name'],
                'customer_email': customer['email'],
                'customer_phone': customer['phone'],
                'customer_address': customer['address'],
                'customer_city': customer['city'],
                'customer_state': customer['state'],
                'customer_zip_code': customer['zip_code'],
                'customer_country': customer['country'],
                'customer_ip_address': customer['ip_address'],
                'customer_segment': customer['segment'],
                'transaction_datetime': transaction_time,
                'transaction_date': transaction_time.strftime('%Y-%m-%d'),
                'transaction_time': transaction_time.strftime('%H:%M:%S'),
                'merchant_name': pattern['name'],
                'merchant_category': pattern['category'],
                'merchant_industry': pattern['industry'],
                **transaction_details,
                'customer_lifetime_value': customer['clv'],
                'customer_acquisition_channel': customer['acquisition_channel'],
                'customer_transaction_count': behavior['transaction_count'],
                'device_type': self._get_device_info(customer['preferred_device']),
                'is_mobile': customer['preferred_device'] == 'mobile',
                'session_duration_seconds': random.randint(30, 1800),
                'timezone': customer['timezone'],
                'language': customer['language']
            }
            
            transactions.append(transaction)
        
        # Convert to DataFrame
        df = pd.DataFrame(transactions)
        df = self._add_derived_metrics(df)
        
        # Add anomalies for testing
        anomaly_df = self._generate_anomalies(df, business_type, pattern)
        df = pd.concat([df, anomaly_df], ignore_index=True)
        
        print(f"  ✓ Generated {len(df):,} total transactions")
        return df.sort_values('transaction_datetime').reset_index(drop=True)
    
    def _generate_realistic_timestamp(self, start_date, end_date, pattern, customer):
        """Generate realistic transaction timestamp"""
        # Random date within range
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        base_date = start_date + timedelta(days=random_days)
        
        # Business hours weighting
        peak_hours = pattern.get('peak_hours', [9, 10, 11, 14, 15, 16])
        if random.random() < 0.7:  # 70% during peak hours
            hour = random.choice(peak_hours)
        else:
            hour = random.randint(0, 23)
        
        # Timezone adjustment
        tz_offsets = {'EST': -5, 'CST': -6, 'MST': -7, 'PST': -8, 'GMT': 0, 'CET': 1, 'JST': 9}
        utc_hour = (hour - tz_offsets.get(customer['timezone'], 0)) % 24
        
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        return base_date.replace(hour=int(utc_hour), minute=minute, second=second)
    
    def _generate_transaction_details(self, business_type, pattern, customer, behavior):
        """Generate business-specific transaction details"""
        details = {}
        
        # Get transaction type
        transaction_types = pattern.get('transaction_types', ['purchase'])
        transaction_type = random.choice(transaction_types)
        details['transaction_type'] = transaction_type
        
        # Generate amount based on business type
        if 'subscription_tiers' in pattern:
            details.update(self._generate_subscription_details(pattern, customer))
        elif 'product_categories' in pattern:
            details.update(self._generate_product_details(pattern, customer))
        elif 'service_types' in pattern:
            details.update(self._generate_service_details(pattern, customer))
        elif 'trading_pairs' in pattern:
            details.update(self._generate_trading_details(pattern, customer))
        else:
            # Default transaction
            details['amount'] = round(random.uniform(10, 500), 2)
            details['product_category'] = 'general'
        
        # Payment details
        details.update(self._generate_payment_details(customer, details.get('amount', 0), behavior))
        
        # Fraud indicators
        details.update(self._generate_fraud_indicators(customer, details, behavior))
        
        return details
    
    def _generate_subscription_details(self, pattern, customer):
        """Generate subscription transaction details"""
        tiers = list(pattern['subscription_tiers'].keys())
        
        # Select tier based on customer segment
        if customer['segment'] == 'enterprise':
            tier = tiers[-1] if len(tiers) > 0 else 'enterprise'
        elif customer['segment'] == 'vip':
            tier = tiers[-2] if len(tiers) > 1 else tiers[-1]
        else:
            tier = random.choice(tiers[:2]) if len(tiers) > 1 else tiers[0]
        
        if tier in pattern['subscription_tiers']:
            tier_info = pattern['subscription_tiers'][tier]
            amount = tier_info['price']
        else:
            amount = random.uniform(50, 500)
        
        # Billing cycle
        cycles = pattern.get('billing_cycles', {'monthly': 1.0})
        cycle = random.choices(list(cycles.keys()), weights=list(cycles.values()))[0]
        
        if cycle == 'annual':
            amount *= 12 * 0.85  # 15% discount
        elif cycle == 'quarterly':
            amount *= 3 * 0.95   # 5% discount
        
        return {
            'amount': round(amount, 2),
            'subscription_tier': tier,
            'billing_cycle': cycle,
            'product_category': 'subscription'
        }
    
    def _generate_product_details(self, pattern, customer):
        """Generate product purchase details"""
        categories = list(pattern['product_categories'].keys())
        category = random.choice(categories)
        price_range = pattern['product_categories'][category]
        amount = random.uniform(*price_range)
        
        return {
            'amount': round(amount, 2),
            'product_category': category,
            'quantity': random.randint(1, 3)
        }
    
    def _generate_service_details(self, pattern, customer):
        """Generate service transaction details"""
        services = list(pattern['service_types'].keys())
        service = random.choice(services)
        price_range = pattern['service_types'][service]
        amount = random.uniform(*price_range)
        
        return {
            'amount': round(amount, 2),
            'service_type': service,
            'product_category': 'service'
        }
    
    def _generate_trading_details(self, pattern, customer):
        """Generate trading/crypto transaction details"""
        pairs = list(pattern['trading_pairs'].keys())
        pair = random.choice(pairs)
        pair_info = pattern['trading_pairs'][pair]
        
        base_amount = random.uniform(pair_info['min'], pair_info['max'])
        volatility = random.uniform(-pair_info['volatility'], pair_info['volatility'])
        amount = base_amount * (1 + volatility)
        
        transaction_types = pattern.get('transaction_types', ['buy', 'sell'])
        transaction_type = random.choice(transaction_types)
        
        fee_structure = pattern.get('fee_structure', {})
        if transaction_type in ['buy', 'sell']:
            fee_rate = fee_structure.get('taker', 0.002)
            fee = amount * fee_rate
        else:
            fee = 0
        
        return {
            'amount': round(amount, 2),
            'trading_pair': pair,
            'fee': round(fee, 2),
            'product_category': 'trading'
        }
    
    def _generate_payment_details(self, customer, amount, behavior):
        """Generate payment processing details"""
        payment_method = random.choice(customer['payment_methods'])
        
        # Payment success based on risk
        success_rate = 0.96 - (behavior['risk_score'] / 1000)
        
        if random.random() < success_rate:
            status = 'completed'
            response_code = '00'
            response_text = 'Approved'
        else:
            status = 'failed'
            error_codes = {'05': 'Do not honor', '51': 'Insufficient funds', '14': 'Invalid card'}
            response_code = random.choice(list(error_codes.keys()))
            response_text = error_codes[response_code]
        
        return {
            'payment_method': payment_method,
            'payment_status': status,
            'response_code': response_code,
            'response_text': response_text,
            'processing_time_ms': random.randint(100, 2000)
        }
    
    def _generate_fraud_indicators(self, customer, transaction_details, behavior):
        """Generate fraud detection indicators"""
        risk_score = behavior['risk_score']
        fraud_indicators = []
        
        # Check for suspicious patterns
        amount = transaction_details.get('amount', 0)
        if amount > customer['clv'] * 0.5:
            fraud_indicators.append('amount_exceeds_normal')
            risk_score += 20
        
        if amount in [1.00, 100.00, 1000.00]:  # Round amounts
            fraud_indicators.append('round_amount_testing')
            risk_score += 15
        
        # Determine fraud
        fraud_probability = min(risk_score / 200, 0.12)
        is_fraudulent = random.random() < fraud_probability
        
        if is_fraudulent:
            fraud_types = ['card_testing', 'account_takeover', 'synthetic_identity']
            fraud_type = random.choice(fraud_types)
            fraud_indicators.append(f'fraud_type_{fraud_type}')
        
        return {
            'is_fraudulent': is_fraudulent,
            'fraud_indicators': ','.join(fraud_indicators) if fraud_indicators else '',
            'risk_score': min(risk_score, 100),
            'fraud_type': fraud_type if is_fraudulent else ''
        }
    
    def _get_device_info(self, device_type):
        """Get device information"""
        if device_type in self.device_types:
            os_options = self.device_types[device_type]
            os_type = random.choices(list(os_options.keys()), 
                                   weights=list(os_options.values()))[0]
            return f"{device_type}_{os_type}"
        return device_type
    
    def _add_derived_metrics(self, df):
        """Add derived metrics to the dataframe"""
        df['transaction_datetime'] = pd.to_datetime(df['transaction_datetime'])
        df = df.sort_values('transaction_datetime')
        
        # Time-based metrics
        df['hour'] = df['transaction_datetime'].dt.hour
        df['day_of_week'] = df['transaction_datetime'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        df['month'] = df['transaction_datetime'].dt.month
        df['quarter'] = df['transaction_datetime'].dt.quarter
        
        # Customer metrics
        df['customer_transaction_number'] = df.groupby('customer_id').cumcount() + 1
        df['customer_total_spent'] = df.groupby('customer_id')['amount'].cumsum()
        
        return df
    
    def _generate_anomalies(self, df, business_type, pattern):
        """Generate anomaly transactions for testing"""
        if len(df) == 0:
            return pd.DataFrame()
        
        anomaly_transactions = []
        base_time = datetime.now() - timedelta(days=30)
        
        # Sample some customers for anomaly testing
        sample_customers = df[['customer_id', 'customer_name', 'customer_email', 
                              'customer_city', 'customer_state', 'customer_zip_code',
                              'customer_country', 'customer_ip_address', 'customer_segment']].drop_duplicates().head(5)
        
        for i, customer_row in sample_customers.iterrows():
            # Geographic anomaly
            geo_anomaly = {
                'transaction_id': f"GEO_ANOM_{i}_{fake.random_number(digits=6)}",
                'customer_id': customer_row['customer_id'],
                'customer_name': customer_row['customer_name'],
                'customer_email': customer_row['customer_email'],
                'customer_phone': fake.phone_number(),
                'customer_address': fake.address(),
                'customer_city': customer_row['customer_city'],
                'customer_state': 'CA',  # Different state
                'customer_zip_code': '90210',  # Mismatched ZIP
                'customer_country': customer_row['customer_country'],
                'customer_ip_address': '8.8.8.8',  # Generic IP
                'customer_segment': customer_row['customer_segment'],
                'transaction_datetime': base_time + timedelta(hours=i),
                'transaction_date': (base_time + timedelta(hours=i)).strftime('%Y-%m-%d'),
                'transaction_time': (base_time + timedelta(hours=i)).strftime('%H:%M:%S'),
                'merchant_name': pattern['name'],
                'merchant_category': pattern['category'],
                'merchant_industry': pattern.get('industry', 'Technology'),
                'amount': round(random.uniform(100, 500), 2),
                'payment_method': 'card',
                'payment_status': 'completed',
                'response_code': '00',
                'response_text': 'Approved',
                'transaction_type': 'purchase',
                'product_category': 'general',
                'customer_lifetime_value': 1000.0,
                'customer_acquisition_channel': 'organic_search',
                'customer_transaction_count': 1,
                'device_type': 'mobile_ios',
                'is_mobile': True,
                'session_duration_seconds': 300,
                'timezone': 'EST',
                'language': 'en',
                'is_fraudulent': False,
                'fraud_indicators': 'geo_mismatch',
                'risk_score': 55,
                'fraud_type': '',
                'processing_time_ms': 450
            }
            anomaly_transactions.append(geo_anomaly)
        
        return pd.DataFrame(anomaly_transactions)


def generate_business_data(business_type='saas_b2b', num_transactions=5000, region='US'):
    """Generate transaction data for any business type"""
    generator = UniversalTransactionGenerator()
    return generator.generate_transaction_data(num_transactions, business_type, region)


def main():
    """Generate comprehensive transaction data for multiple business types"""
    
    # All supported business types across industries
    business_types = [
        # Technology & Software
        'saas_b2b', 'cybersecurity_platform',
        
        # E-commerce & Retail  
        'fashion_ecommerce', 'electronics_store',
        
        # Healthcare & Medical
        'telehealth_platform', 'pharmacy_online',
        
        # Financial Services
        'fintech_payment_app', 'crypto_exchange',
        
        # Education & Learning
        'online_education', 'tutoring_platform',
        
        # Entertainment & Media
        'streaming_service', 'gaming_platform',
        
        # Travel & Hospitality
        'travel_booking', 'hotel_management',
        
        # Food & Restaurant
        'food_delivery', 'restaurant_pos',
        
        # Professional Services
        'legal_services', 'accounting_software',
        
        # Automotive & Transportation
        'ride_sharing', 'auto_parts',
        
        # Non-Profit & Social Impact
        'donation_platform', 'crowdfunding'
    ]
    
    print("🚀 Universal Transaction Data Generator")
    print("=" * 60)
    print(f"Generating data for {len(business_types)} business types")
    
    # Create output directory
    output_dir = 'universal_business_transactions'
    os.makedirs(output_dir, exist_ok=True)
    
    total_start_time = time.time()
    
    for i, business_type in enumerate(business_types, 1):
        print(f"\n[{i}/{len(business_types)}] Processing {business_type}...")
        
        start_time = time.time()
        
        try:
            # Generate data
            df = generate_business_data(business_type, num_transactions=8000, region='US')
            
            # Save to CSV
            filename = os.path.join(output_dir, f'{business_type}_transactions.csv')
            df.to_csv(filename, index=False)
            
            # Generate summary statistics
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"  ✅ Success! Generated in {processing_time:.1f}s")
            print(f"     📊 Total transactions: {len(df):,}")
            print(f"     👥 Unique customers: {df['customer_id'].nunique():,}")
            print(f"     📅 Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
            print(f"     💰 Average transaction: ${df['amount'].mean():.2f}")
            print(f"     📈 Total revenue: ${df['amount'].sum():,.2f}")
            print(f"     🚨 Fraud rate: {df['is_fraudulent'].mean() * 100:.2f}%")
            print(f"     ✅ Payment success: {(df['payment_status'] == 'completed').mean() * 100:.1f}%")
            print(f"     💾 Saved: {filename}")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            continue
    
    total_end_time = time.time()
    total_processing_time = total_end_time - total_start_time
    
    print("\n" + "=" * 60)
    print("🎉 Universal transaction generation complete!")
    print(f"⏱️  Total processing time: {total_processing_time:.1f} seconds")
    print(f"📁 Output directory: {output_dir}/")
    print(f"📊 Business types generated: {len(business_types)}")
    
    print(f"\n🏭 Supported Industries:")
    industries = {
        'Technology & Software': ['saas_b2b', 'cybersecurity_platform'],
        'E-commerce & Retail': ['fashion_ecommerce', 'electronics_store'], 
        'Healthcare & Medical': ['telehealth_platform', 'pharmacy_online'],
        'Financial Services': ['fintech_payment_app', 'crypto_exchange'],
        'Education & Learning': ['online_education', 'tutoring_platform'],
        'Entertainment & Media': ['streaming_service', 'gaming_platform'],
        'Travel & Hospitality': ['travel_booking', 'hotel_management'],
        'Food & Restaurant': ['food_delivery', 'restaurant_pos'],
        'Professional Services': ['legal_services', 'accounting_software'],
        'Automotive & Transportation': ['ride_sharing', 'auto_parts'],
        'Non-Profit & Social Impact': ['donation_platform', 'crowdfunding']
    }
    
    for industry, types in industries.items():
        print(f"  🏢 {industry}: {len(types)} business types")
    
    print(f"\n💡 Usage examples:")
    print(f"  - Load data: pd.read_csv('{output_dir}/saas_b2b_transactions.csv')")
    print(f"  - Generate custom: generate_business_data('your_business_type', 10000)")
    print(f"  - Test fraud detection across all industry verticals")


if __name__ == "__main__":
    main()
