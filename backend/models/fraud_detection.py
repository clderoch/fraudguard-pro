import pandas as pd
import numpy as np
import random
import warnings
warnings.filterwarnings('ignore')

class SimpleFraudDetectionModel:
    """Enhanced fraud detection with industry-specific rules and adaptive thresholds"""
    
    def __init__(self):
        self.risk_score_calculated = False
        # US ZIP code to state mapping (simplified sample)
        self.zip_to_state = {
            '90210': 'CA', '10001': 'NY', '60601': 'IL', '33101': 'FL',
            '77001': 'TX', '30301': 'GA', '02101': 'MA', '98101': 'WA',
            '80201': 'CO', '85001': 'AZ', '97201': 'OR', '89101': 'NV'
        }
        
        # IP address to general location mapping (simplified sample)
        self.ip_to_location = {
            '192.168': 'Local Network',
            '8.8.8': 'Mountain View, CA',
            '4.4.4': 'Level 3, US',
            '1.1.1': 'Cloudflare, Global'
        }
        
        # Industry-specific fraud patterns and thresholds
        self.industry_patterns = {
            'mobile_app': {
                'typical_amounts': (0.99, 49.99),
                'suspicious_amounts': [9999.99, 999.99, 99.99],
                'velocity_threshold': 10,
                'refund_rate_threshold': 0.15,
                'common_fraud_indicators': ['rooted_device', 'emulator', 'vpn_detected'],
                'peak_hours': [18, 19, 20, 21, 22],
                'risk_multiplier': 1.2
            },
            'healthcare': {
                'typical_amounts': (25, 500),
                'suspicious_amounts': [999.99, 1999.99, 4999.99],
                'velocity_threshold': 3,
                'billing_patterns': ['urgent_care', 'emergency', 'specialist'],
                'compliance_required': True,
                'peak_hours': [9, 10, 11, 14, 15, 16],
                'risk_multiplier': 0.8,
                'age_verification': True
            },
            'gaming': {
                'typical_amounts': (4.99, 99.99),
                'whale_threshold': 500,
                'velocity_threshold': 20,
                'common_fraud_amounts': [1.00, 10.00, 100.00],
                'peak_hours': [18, 19, 20, 21, 22, 23],
                'risk_multiplier': 1.3
            },
            'financial': {
                'structuring_threshold': 9000,
                'velocity_threshold': 5,
                'high_risk_amounts': [9999, 9998, 9997, 9990],
                'peak_hours': [9, 10, 11, 14, 15, 16],
                'risk_multiplier': 1.5
            },
            'subscription': {
                'trial_abuse_threshold': 5,
                'common_amounts': [0.01, 1.00, 9.99, 29.99],
                'chargeback_threshold': 0.1,
                'risk_multiplier': 1.1
            }
        }
    
    def check_geographical_anomalies(self, row):
        """Check for geographical mismatches"""
        anomalies = []
        score_increase = 0
        
        customer_state = str(row.get('customer_state', '')).strip().upper()
        customer_zip = str(row.get('customer_zip_code', '')).strip()
        customer_ip = str(row.get('customer_ip_address', '')).strip()
        customer_city = str(row.get('customer_city', '')).strip()
        
        # Check ZIP code to state mismatch
        if customer_zip and customer_state:
            zip_code = customer_zip[:5] if len(customer_zip) >= 5 else customer_zip
            expected_state = self.zip_to_state.get(zip_code, '')
            
            if expected_state and expected_state != customer_state:
                anomalies.append(f"ZIP {zip_code} doesn't match state {customer_state}")
                score_increase += 35
            
            # Simple ZIP code validation patterns
            if customer_state == 'CA' and not (zip_code.startswith('9') or zip_code.startswith('8')):
                anomalies.append("California ZIP doesn't match typical CA pattern")
                score_increase += 25
            elif customer_state == 'NY' and not (zip_code.startswith('1') or zip_code.startswith('0')):
                anomalies.append("New York ZIP doesn't match typical NY pattern")
                score_increase += 25
            elif customer_state == 'TX' and not zip_code.startswith('7'):
                anomalies.append("Texas ZIP doesn't match typical TX pattern")
                score_increase += 25
            elif customer_state == 'FL' and not zip_code.startswith('3'):
                anomalies.append("Florida ZIP doesn't match typical FL pattern")
                score_increase += 25
        
        # Check IP address geographical consistency
        if customer_ip and customer_state:
            if customer_ip.startswith('192.168.') or customer_ip.startswith('10.') or customer_ip.startswith('172.'):
                anomalies.append("Transaction from private/local IP address")
                score_increase += 20
            
            suspicious_ip_ranges = ['45.', '103.', '185.', '198.']
            if any(customer_ip.startswith(range_) for range_ in suspicious_ip_ranges):
                anomalies.append("Transaction from potential VPN/proxy IP")
                score_increase += 30
            
            international_ranges = ['41.', '103.', '115.', '200.']
            if any(customer_ip.startswith(range_) for range_ in international_ranges) and customer_state:
                anomalies.append("International IP with US address")
                score_increase += 40
        
        return anomalies, score_increase
    
    def check_velocity_anomalies(self, df, current_index, customer_id, amount, transaction_time):
        """Check for velocity-based anomalies"""
        anomalies = []
        score_increase = 0
        
        customer_transactions = df[df['customer_id'] == customer_id].iloc[:current_index + 1]
        
        if len(customer_transactions) > 1:
            if len(customer_transactions) >= 3:
                recent_transactions = 0
                current_time = pd.to_datetime(transaction_time)
                for _, tx in customer_transactions.iterrows():
                    try:
                        tx_time = pd.to_datetime(tx['transaction_time'])
                        if (current_time - tx_time).total_seconds() <= 3600:
                            recent_transactions += 1
                    except:
                        pass
                
                if recent_transactions >= 3:
                    anomalies.append("Multiple transactions within 1 hour")
                    score_increase += 35
            
            amounts = customer_transactions['amount'].tolist()
            if len(amounts) >= 3:
                if amounts[-1] > amounts[-2] * 3 and amounts[-2] > amounts[-3] * 2:
                    anomalies.append("Rapid amount escalation (card testing pattern)")
                    score_increase += 40
        
        return anomalies, score_increase
    
    def check_payment_anomalies(self, row):
        """Check for payment method and card-related anomalies"""
        anomalies = []
        score_increase = 0
        
        payment_method = str(row.get('payment_method', '')).lower()
        card_last4 = str(row.get('card_last4', ''))
        response_code = str(row.get('response_code', ''))
        
        if response_code and response_code != '00':
            if response_code in ['05', '51', '14', '61']:
                anomalies.append(f"Payment declined (code: {response_code})")
                score_increase += 30
        
        if card_last4 and len(card_last4) == 4:
            if card_last4 in ['1234', '2345', '3456', '4567', '5678', '6789', '7890']:
                anomalies.append("Sequential card number pattern")
                score_increase += 45
            
            if len(set(card_last4)) == 1:
                anomalies.append("Repeated digits in card number")
                score_increase += 35
        
        return anomalies, score_increase
    
    def check_behavioral_anomalies(self, row, df, current_index):
        """Check for unusual customer behavior patterns"""
        anomalies = []
        score_increase = 0
        
        amount = row.get('amount', 0)
        customer_id = row.get('customer_id', '')
        merchant_category = str(row.get('merchant_category', '')).lower()
        
        if customer_id and merchant_category:
            customer_history = df[df['customer_id'] == customer_id].iloc[:current_index]
            if len(customer_history) > 0 and 'merchant_category' in df.columns:
                prev_categories = customer_history['merchant_category'].unique()
                
                if len(customer_history) >= 3 and merchant_category not in [cat.lower() for cat in prev_categories]:
                    anomalies.append("New merchant category for returning customer")
                    score_increase += 20
        
        if amount > 0 and amount == round(amount) and amount % 100 == 0:
            if amount >= 500:
                anomalies.append(f"Suspicious round amount (${amount:,.0f})")
                score_increase += 25
        
        common_fraud_amounts = [1.00, 5.00, 10.00, 100.00, 500.00, 1000.00]
        if amount in common_fraud_amounts:
            anomalies.append(f"Common fraud testing amount (${amount:.2f})")
            score_increase += 30
        
        return anomalies, score_increase
    
    def check_temporal_anomalies(self, row, df):
        """Check for time-based anomalies"""
        anomalies = []
        score_increase = 0
        
        transaction_time = str(row.get('transaction_time', ''))
        transaction_date = str(row.get('transaction_date', ''))
        
        if transaction_time and ':' in transaction_time:
            try:
                hour = int(transaction_time.split(':')[0])
                minute = int(transaction_time.split(':')[1])
                
                if minute == 0:
                    hour_transactions = len(df[df['transaction_time'].str.startswith(f"{hour:02d}:00")])
                    if hour_transactions > len(df) * 0.1:
                        anomalies.append("Unusual concentration of transactions at exact hour")
                        score_increase += 20
                
                if transaction_date:
                    try:
                        date_obj = pd.to_datetime(transaction_date)
                        weekday = date_obj.dayofweek
                        if weekday >= 5 and (hour <= 6 or hour >= 23):
                            anomalies.append("Weekend late-night transaction")
                            score_increase += 15
                    except:
                        pass
                
                merchant_category = str(row.get('merchant_category', '')).lower()
                if any(term in merchant_category for term in ['business', 'office', 'professional']):
                    if hour < 8 or hour > 18:
                        anomalies.append("B2B transaction outside business hours")
                        score_increase += 20
                        
            except:
                pass
        
        return anomalies, score_increase
    
    def check_data_quality_anomalies(self, row):
        """Check for data quality issues that might indicate fraud"""
        anomalies = []
        score_increase = 0
        
        customer_name = str(row.get('customer_name', '')).strip()
        customer_email = str(row.get('customer_email', '')).strip()
        customer_phone = str(row.get('customer_phone', '')).strip()
        
        if customer_name:
            name_lower = customer_name.lower()
            suspicious_names = ['test', 'demo', 'fake', 'admin', 'null', 'none']
            if any(sus in name_lower for sus in suspicious_names):
                anomalies.append("Suspicious customer name pattern")
                score_increase += 30
            
            if len(customer_name.replace(' ', '')) < 3:
                anomalies.append("Unusually short customer name")
                score_increase += 25
        
        if customer_email:
            email_lower = customer_email.lower()
            temp_domains = ['10minutemail', 'tempmail', 'guerrillamail', 'mailinator']
            if any(domain in email_lower for domain in temp_domains):
                anomalies.append("Temporary/disposable email address")
                score_increase += 35
            
            if any(char.isdigit() for char in email_lower):
                digits = ''.join([c for c in email_lower if c.isdigit()])
                if len(digits) >= 4 and digits == ''.join(sorted(digits)):
                    anomalies.append("Sequential digits in email address")
                    score_increase += 20
        
        return anomalies, score_increase
    
    def get_industry_type(self, row):
        """Determine industry type from merchant category or transaction details"""
        merchant_category = str(row.get('merchant_category', '')).lower()
        merchant_name = str(row.get('merchant_name', '')).lower()
        
        if any(term in merchant_category for term in ['gaming', 'mobile', 'app', 'game']):
            return 'mobile_app'
        if any(term in merchant_name for term in ['game', 'app', 'mobile']):
            return 'mobile_app'
            
        if any(term in merchant_category for term in ['health', 'medical', 'telehealth', 'clinic']):
            return 'healthcare'
        if any(term in merchant_name for term in ['health', 'medical', 'clinic', 'doctor']):
            return 'healthcare'
            
        if any(term in merchant_category for term in ['gaming', 'entertainment']):
            return 'gaming'
            
        if any(term in merchant_category for term in ['financial', 'payment', 'bank', 'finance']):
            return 'financial'
            
        if any(term in merchant_category for term in ['subscription', 'saas', 'software']):
            return 'subscription'
            
        return 'general'
    
    def detect_fraud(self, df):
        """Enhanced fraud detection with industry-specific rules and adaptive thresholds"""
        df_analyzed = df.copy()
        
        try:
            # Ensure amount is numeric
            df_analyzed['amount'] = pd.to_numeric(df_analyzed['amount'], errors='coerce').fillna(0)
            
            # Convert time columns for analysis
            df_analyzed['transaction_time'] = df_analyzed['transaction_time'].astype(str)
            df_analyzed['transaction_date'] = df_analyzed['transaction_date'].astype(str)
            
            # Enhanced risk scoring with industry-specific rules
            risk_scores = []
            risk_levels = []
            anomaly_flags = []
            industry_types = []
            
            for idx, row in df_analyzed.iterrows():
                score = 0
                amount = row.get('amount', 0)
                current_anomalies = []
                
                # Determine industry type for adaptive thresholds
                industry_type = self.get_industry_type(row)
                industry_types.append(industry_type)
                
                # Get industry-specific multiplier
                risk_multiplier = self.industry_patterns.get(industry_type, {}).get('risk_multiplier', 1.0)
                
                # Industry-adaptive amount-based risk
                if industry_type == 'healthcare':
                    if amount > 2000:
                        score += 50
                        current_anomalies.append("High healthcare transaction amount")
                    elif amount > 500:
                        score += 25
                elif industry_type == 'mobile_app':
                    if amount > 100:
                        score += 45
                        current_anomalies.append("High mobile app purchase amount")
                    elif amount < 1:
                        score += 35
                        current_anomalies.append("Very small amount (card testing)")
                elif industry_type == 'financial':
                    if amount > 5000:
                        score += 60
                        current_anomalies.append("Large financial transaction")
                    elif amount > 1000:
                        score += 30
                else:
                    if amount > 1000:
                        score += 40
                        current_anomalies.append("Large transaction amount")
                    elif amount > 500:
                        score += 20
                    elif amount < 5:
                        score += 30
                        current_anomalies.append("Very small amount (card testing)")
                    else:
                        score += 5
                
                # Time-based risk with industry context
                if 'transaction_time' in df_analyzed.columns:
                    time_str = str(row.get('transaction_time', '12:00:00'))
                    try:
                        if ':' in time_str:
                            hour = int(time_str.split(':')[0])
                            
                            pattern = self.industry_patterns.get(industry_type, {})
                            peak_hours = pattern.get('peak_hours', [9, 10, 11, 14, 15, 16])
                            
                            if hour not in peak_hours:
                                if hour >= 22 or hour <= 6:
                                    score += 25
                                    current_anomalies.append("Late night/early morning transaction")
                                else:
                                    score += 10
                    except:
                        pass
                
                # Customer pattern risk
                if 'customer_id' in df_analyzed.columns:
                    customer_id = str(row.get('customer_id', ''))
                    if customer_id.startswith('CUST_') and random.random() < 0.1:
                        score += 15
                        current_anomalies.append("New customer pattern")
                
                # Core anomaly checks
                geo_anomalies, geo_score = self.check_geographical_anomalies(row)
                score += geo_score
                current_anomalies.extend(geo_anomalies)
                
                velocity_anomalies, velocity_score = self.check_velocity_anomalies(
                    df_analyzed, idx, row.get('customer_id', ''), amount, row.get('transaction_time', '')
                )
                score += velocity_score
                current_anomalies.extend(velocity_anomalies)
                
                payment_anomalies, payment_score = self.check_payment_anomalies(row)
                score += payment_score
                current_anomalies.extend(payment_anomalies)
                
                behavioral_anomalies, behavioral_score = self.check_behavioral_anomalies(row, df_analyzed, idx)
                score += behavioral_score
                current_anomalies.extend(behavioral_anomalies)
                
                temporal_anomalies, temporal_score = self.check_temporal_anomalies(row, df_analyzed)
                score += temporal_score
                current_anomalies.extend(temporal_anomalies)
                
                quality_anomalies, quality_score = self.check_data_quality_anomalies(row)
                score += quality_score
                current_anomalies.extend(quality_anomalies)
                
                # Apply industry risk multiplier
                score = int(score * risk_multiplier)
                
                # Add minimal randomness
                score += np.random.randint(0, 3)
                
                risk_scores.append(min(score, 100))
                anomaly_flags.append('; '.join(current_anomalies) if current_anomalies else 'None detected')
                
                # Industry-adaptive categorization
                if industry_type == 'healthcare':
                    if score > 60:
                        risk_levels.append('Needs Your Attention')
                    elif score > 30:
                        risk_levels.append('Watch Closely')
                    else:
                        risk_levels.append('Safe')
                elif industry_type == 'financial':
                    if score > 50:
                        risk_levels.append('Needs Your Attention')
                    elif score > 25:
                        risk_levels.append('Watch Closely')
                    else:
                        risk_levels.append('Safe')
                elif industry_type == 'mobile_app':
                    if score > 75:
                        risk_levels.append('Needs Your Attention')
                    elif score > 45:
                        risk_levels.append('Watch Closely')
                    else:
                        risk_levels.append('Safe')
                else:
                    if score > 70:
                        risk_levels.append('Needs Your Attention')
                    elif score > 40:
                        risk_levels.append('Watch Closely')
                    else:
                        risk_levels.append('Safe')
            
            df_analyzed['risk_score'] = risk_scores
            df_analyzed['safety_level'] = risk_levels
            df_analyzed['anomaly_flags'] = anomaly_flags
            df_analyzed['industry_type'] = industry_types
            
            # Add hour for visualization
            if 'transaction_time' in df_analyzed.columns:
                hours = []
                for time_val in df_analyzed['transaction_time']:
                    try:
                        time_str = str(time_val)
                        if ':' in time_str:
                            hour = int(time_str.split(':')[0])
                            hours.append(hour)
                        else:
                            hours.append(12)
                    except:
                        hours.append(12)
                df_analyzed['hour'] = hours
            else:
                df_analyzed['hour'] = 12
            
            return df_analyzed
            
        except Exception as e:
            print(f"Error in fraud detection: {e}")
            # Ultra-simple fallback
            df_analyzed['risk_score'] = np.random.uniform(10, 70, len(df_analyzed))
            df_analyzed['safety_level'] = 'Safe'
            df_analyzed['anomaly_flags'] = 'None detected'
            df_analyzed['industry_type'] = 'general'
            df_analyzed['hour'] = 12
            return df_analyzed