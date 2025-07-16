#!/usr/bin/env python3
"""
FraudGuard Pro - Upload Test Script
This script tests the upload functionality and helps debug issues
"""

import requests
import json
import os
import sys
from pathlib import Path

def print_banner():
    print("🧪 FraudGuard Pro - Upload Test Script")
    print("=" * 50)

def test_server_health():
    """Test if the server is running"""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Server is running")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Fraud model loaded: {health_data.get('fraud_model_loaded')}")
            print(f"   Upload directory: {health_data.get('upload_directory')}")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        print("   Please start the server first with: python run.py")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

def create_sample_csv():
    """Create a sample CSV file for testing"""
    sample_csv_content = """transaction_id,amount,transaction_date,transaction_time,customer_id,customer_name,customer_email,customer_state,customer_zip_code,customer_ip_address,merchant_category
TXN_001,45.67,2024-01-15,14:30:00,CUST_001,John Smith,john.smith@email.com,CA,90210,192.168.1.1,general
TXN_002,1250.00,2024-01-15,23:45:00,CUST_002,Jane Doe,jane.doe@email.com,NY,10001,8.8.8.8,electronics
TXN_003,23.50,2024-01-16,08:15:00,CUST_003,Bob Johnson,bob.johnson@email.com,TX,77001,1.1.1.1,food
TXN_004,999.99,2024-01-16,02:30:00,CUST_004,Alice Brown,alice@tempmail.com,FL,33101,45.123.45.67,gaming
TXN_005,5000.00,2024-01-16,03:00:00,CUST_005,Test User,test@fake.com,CA,10001,103.45.67.89,financial"""
    
    csv_path = "sample_transactions.csv"
    
    with open(csv_path, "w") as f:
        f.write(sample_csv_content)
    
    print(f"📄 Created sample CSV file: {csv_path}")
    return csv_path

def test_file_upload(csv_path):
    """Test uploading a CSV file"""
    try:
        if not os.path.exists(csv_path):
            print(f"❌ File not found: {csv_path}")
            return False
        
        print(f"📤 Testing upload of: {csv_path}")
        
        with open(csv_path, "rb") as f:
            files = {"file": (csv_path, f, "text/csv")}
            
            response = requests.post(
                "http://localhost:8000/api/analyze-transactions",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Upload successful!")
            print(f"   Total transactions: {data['summary']['total_transactions']}")
            print(f"   Safe payments: {data['summary']['safe_payments']}")
            print(f"   Need attention: {data['summary']['needs_attention']}")
            print(f"   Money at risk: ${data['summary']['money_at_risk']:.2f}")
            return True
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Upload timed out (server may be processing)")
        return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def test_dashboard_access():
    """Test accessing the dashboard"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard accessible at http://localhost:8000")
            return True
        else:
            print(f"❌ Dashboard returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard access error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print_banner()
    
    # Test 1: Server Health
    print("\n1️⃣ Testing server health...")
    if not test_server_health():
        print("\n❌ Server tests failed. Please start the server and try again.")
        return False
    
    # Test 2: Dashboard Access
    print("\n2️⃣ Testing dashboard access...")
    test_dashboard_access()
    
    # Test 3: Sample File Creation
    print("\n3️⃣ Creating sample CSV file...")
    csv_path = create_sample_csv()
    
    # Test 4: File Upload
    print("\n4️⃣ Testing file upload...")
    upload_success = test_file_upload(csv_path)
    
    # Results
    print("\n" + "=" * 50)
    if upload_success:
        print("🎉 All tests passed! Upload functionality is working.")
        print("\n💡 Next steps:")
        print("   1. Open http://localhost:8000 in your browser")
        print("   2. Try uploading your own CSV file")
        print("   3. Use the sample file 'sample_transactions.csv' for testing")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Make sure the server is running with: python run.py")
        print("   2. Check that all files are in the correct locations")
        print("   3. Verify your CSV file has the required columns")
    
    return upload_success

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Test with user-provided file
        csv_path = sys.argv[1]
        print_banner()
        print(f"\n🧪 Testing with your file: {csv_path}")
        
        if test_server_health():
            test_file_upload(csv_path)
        
    else:
        # Run all tests
        run_all_tests()

if __name__ == "__main__":
    main()