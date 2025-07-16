#!/usr/bin/env python3
"""
Test the upload API endpoint to verify functionality
"""

import requests
import json
import os
from pathlib import Path

def test_upload_api():
    """Test the upload API endpoint"""
    print("🧪 Testing FraudGuard Pro Upload API")
    print("=" * 50)
    
    # Server URL
    base_url = "http://localhost:8080"
    
    # Test health endpoint first
    try:
        health_response = requests.get(f"{base_url}/api/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Server is running and healthy")
            health_data = health_response.json()
            print(f"   Status: {health_data.get('status')}")
            print(f"   Fraud model loaded: {health_data.get('fraud_model_loaded')}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the server is running on port 8080")
        return False
    
    # Test file upload
    sample_file = Path(__file__).parent.parent / "sample_transactions.csv"
    
    if not sample_file.exists():
        print(f"❌ Sample file not found: {sample_file}")
        return False
    
    print(f"📁 Using sample file: {sample_file}")
    
    try:
        with open(sample_file, 'rb') as f:
            files = {'file': ('sample_transactions.csv', f, 'text/csv')}
            
            print("🔄 Uploading file...")
            response = requests.post(
                f"{base_url}/api/analyze-transactions",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            print("✅ Upload successful!")
            
            data = response.json()
            print(f"\n📊 Analysis Results:")
            print(f"   Status: {data.get('status')}")
            
            summary = data.get('summary', {})
            print(f"   Total Transactions: {summary.get('total_transactions')}")
            print(f"   Safe Payments: {summary.get('safe_payments')}")
            print(f"   Need Attention: {summary.get('needs_attention')}")
            print(f"   Money at Risk: ${summary.get('money_at_risk', 0):.2f}")
            print(f"   Detection Accuracy: {summary.get('detection_accuracy')}%")
            
            # Show recent transactions
            recent = data.get('recent_transactions', [])
            if recent:
                print(f"\n📋 Recent Transactions ({len(recent)}):")
                for i, tx in enumerate(recent[:3]):  # Show first 3
                    print(f"   {i+1}. ID: {tx.get('transaction_id')} | Amount: ${tx.get('amount')} | Risk: {tx.get('risk_score')}")
            
            print("\n🎉 Upload functionality is working correctly!")
            return True
            
        else:
            print(f"❌ Upload failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_upload_api()
    if success:
        print("\n✅ All tests passed! Upload functionality is working.")
        print("\n📌 Next steps:")
        print("   1. Open browser: http://localhost:8080")
        print("   2. Use the upload form to test manually")
        print("   3. Upload sample_transactions.csv or any compatible CSV")
    else:
        print("\n❌ Tests failed. Check the server and try again.")
