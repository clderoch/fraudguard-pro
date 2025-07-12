import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import joblib

class FraudDetector:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'amount', 'hour', 'day_of_week', 'merchant_category',
            'payment_method', 'device_score', 'location_risk'
        ]
    
    def preprocess_data(self, df):
        """Preprocess transaction data for model input"""
        # Feature engineering
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Risk scoring features
        df['amount_zscore'] = np.abs((df['amount'] - df['amount'].mean()) / df['amount'].std())
        df['velocity_risk'] = self._calculate_velocity_risk(df)
        
        return df[self.feature_columns]
    
    def train(self, training_data):
        """Train the fraud detection model"""
        X = self.preprocess_data(training_data)
        y = training_data['is_fraud']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train ensemble model
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        print(f"Model AUC Score: {auc_score:.4f}")
        
        return self.model
    
    def predict_risk_score(self, transaction_data):
        """Predict risk score for a single transaction"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X = self.preprocess_data(transaction_data)
        X_scaled = self.scaler.transform(X)
        
        # Get probability of fraud (0-1) and convert to risk score (0-100)
        fraud_probability = self.model.predict_proba(X_scaled)[:, 1]
        risk_score = (fraud_probability * 100).astype(int)
        
        return risk_score[0] if len(risk_score) == 1 else risk_score
    
    def analyze_batch(self, df):
        """Analyze a batch of transactions"""
        risk_scores = self.predict_risk_score(df)
        
        df['risk_score'] = risk_scores
        df['risk_category'] = pd.cut(
            risk_scores, 
            bins=[0, 30, 70, 100], 
            labels=['Low', 'Medium', 'High']
        )
        
        return df
    
    def save_model(self, filepath):
        """Save trained model and scaler"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }, filepath)
    
    def load_model(self, filepath):
        """Load trained model and scaler"""
        saved_objects = joblib.load(filepath)
        self.model = saved_objects['model']
        self.scaler = saved_objects['scaler']
        self.feature_columns = saved_objects['feature_columns']
    
    def _calculate_velocity_risk(self, df):
        """Calculate velocity-based risk score"""
        # Simplified velocity calculation
        return np.random.rand(len(df)) * 0.3  # Placeholder