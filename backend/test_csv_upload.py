#!/usr/bin/env python3
"""
Test CSV file upload directly with requests to debug the issue
"""

import requests
import os
from pathlib import Path

def test_csv_upload():
    """Test uploading the sample CSV file"""
    print("🔍 Testing CSV Upload Directly")
    print("=" * 40)
    
    # Find the sample CSV file
    sample_file = Path(__file__).parent.parent / "sample_transactions.csv"
    
    if not sample_file.exists():
        print(f"❌ Sample file not found: {sample_file}")
        return False
    
    print(f"📁 Found sample file: {sample_file}")
    print(f"📏 File size: {sample_file.stat().st_size} bytes")
    
    try:
        # Test the upload endpoint
        with open(sample_file, 'rb') as f:
            files = {
                'file': ('sample_transactions.csv', f, 'text/csv')
            }
            
            print("🔄 Uploading to http://localhost:8080/api/analyze-transactions")
            
            response = requests.post(
                'http://localhost:8080/api/analyze-transactions',
                files=files,
                timeout=30
            )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Upload successful!")
            print(f"   Total transactions: {data['summary']['total_transactions']}")
            print(f"   Safe payments: {data['summary']['safe_payments']}")
            print(f"   Need attention: {data['summary']['needs_attention']}")
            print(f"   Money at risk: ${data['summary']['money_at_risk']:.2f}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def check_file_details():
    """Check details about the sample CSV file"""
    sample_file = Path(__file__).parent.parent / "sample_transactions.csv"
    
    if sample_file.exists():
        print(f"\n📋 File Details:")
        print(f"   Path: {sample_file}")
        print(f"   Size: {sample_file.stat().st_size} bytes")
        print(f"   Extension: {sample_file.suffix}")
        
        # Read first few lines
        with open(sample_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:3]
            print(f"   First 3 lines:")
            for i, line in enumerate(lines, 1):
                print(f"     {i}: {line.strip()}")

if __name__ == "__main__":
    check_file_details()
    success = test_csv_upload()
    
    if success:
        print("\n✅ Backend API is working correctly")
        print("   The issue is likely in frontend file validation")
        print("   Try using the debug tool at: http://localhost:8080/static/debug_file_types.html")
    else:
        print("\n❌ Backend API has issues")
        print("   Check server logs for more details")
