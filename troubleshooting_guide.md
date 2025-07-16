# 🔧 FraudGuard Pro - Upload Troubleshooting Guide

## Quick Fix Checklist

### ✅ **Step 1: Check Server Status**
```bash
# Run this to test your setup
python test_upload.py
```

### ✅ **Step 2: Verify File Structure**
Make sure your project looks like this:
```
fraudguard-pro/
├── backend/
│   ├── main.py                 ← Fixed version
│   ├── models/
│   │   └── fraud_detection.py
│   ├── requirements.txt
│   └── uploads/               ← Auto-created
├── frontend/
│   └── index.html
├── run.py
├── test_upload.py             ← New test script
└── sample_transactions.csv    ← Test file
```

### ✅ **Step 3: Test with Sample Data**
1. Use the sample CSV I provided above
2. Save it as `sample_transactions.csv`
3. Test upload with this file first

## Common Issues & Solutions

### 🚨 **Issue 1: "Server is not running"**

**Solution:**
```bash
cd backend
python main.py
# OR
python run.py
```

**Check if running:**
- Open http://localhost:8000/api/health
- Should show: `{"status":"healthy"}`

---

### 🚨 **Issue 2: "Missing required columns"**

**Error:** `Missing required columns: ['transaction_id', 'amount']`

**Solution:** Your CSV must have these exact column names:
- `transaction_id` (required)
- `amount` (required) 
- `transaction_date` (required)
- `transaction_time` (required)

**Example header row:**
```csv
transaction_id,amount,transaction_date,transaction_time
TXN_001,45.67,2024-01-15,14:30:00
```

---

### 🚨 **Issue 3: "File must be a CSV"**

**Solution:**
- Save your file with `.csv` extension
- Make sure it's comma-separated values
- Don't use Excel (.xlsx) files

---

### 🚨 **Issue 4: "Import error: No module named 'models.fraud_detection'"**

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Check if file exists
ls models/fraud_detection.py

# If missing, create the file from the artifact above
```

---

### 🚨 **Issue 5: Upload button doesn't work**

**Possible causes:**
1. **JavaScript errors** - Check browser console (F12)
2. **CORS issues** - Server should show CORS enabled
3. **File not selected** - Make sure file is selected first

**Solution:**
1. Open browser developer tools (F12)
2. Check Console tab for errors
3. Try the basic dashboard at http://localhost:8000

---

### 🚨 **Issue 6: "Analysis failed: [error]"**

**Common errors:**

**"Error reading CSV"**
- Check file encoding (should be UTF-8)
- Remove special characters from file
- Try saving as "CSV UTF-8" in Excel

**"No valid transaction data found"** 
- Check amount column has numbers
- Remove empty rows
- Make sure transaction_id is not empty

---

### 🚨 **Issue 7: Frontend shows "Backend is running" but upload fails**

**This means:**
- ✅ Server is working
- ❌ Frontend HTML is missing or broken

**Solution:**
1. Check that `frontend/index.html` exists
2. Copy the complete HTML from the artifact above
3. Restart the server

---

## Testing Your Setup

### **Quick Test:**
```bash
# Run this to test everything
python test_upload.py
```

### **Manual Test:**
1. **Check server:** http://localhost:8000/api/health
2. **Check dashboard:** http://localhost:8000
3. **Test upload:** Use sample_transactions.csv

### **Create Test CSV:**
```csv
transaction_id,amount,transaction_date,transaction_time
TEST_001,100.00,2024-01-01,12:00:00
TEST_002,50.00,2024-01-01,13:00:00
```

## Debug Information

### **Server Logs:**
When you start the server, you should see:
```
✅ Successfully imported SimpleFraudDetectionModel
📁 Frontend directory: /path/to/frontend
📁 Upload directory: /path/to/uploads
✅ Static files mounted successfully
✅ Fraud detection model initialized
```

### **Upload Process:**
When uploading, server should show:
```
📁 Processing file: your_file.csv
📊 Loaded 10 rows from CSV
✅ All required columns found
✅ Cleaned data: 10 valid transactions
✅ Added default values for missing columns
🔍 Running fraud detection...
✅ Fraud detection completed
✅ Analysis complete: 10 transactions processed
```

### **Browser Console:**
Open F12 and check for JavaScript errors. Should see:
- No red error messages
- Upload progress updates
- Success notifications

## Advanced Debugging

### **Check Python Environment:**
```bash
python --version  # Should be 3.8+
pip list | grep fastapi  # Should show fastapi installed
```

### **Test API Directly:**
```bash
# Test with curl
curl -X POST -F "file=@sample_transactions.csv" http://localhost:8000/api/analyze-transactions
```

### **Check File Permissions:**
```bash
# Make sure you can read/write files
ls -la backend/
ls -la frontend/
```

## Still Having Issues?

### **Try This Minimal Test:**

1. **Create simple CSV:**
```csv
transaction_id,amount,transaction_date,transaction_time
T1,10.00,2024-01-01,12:00:00
```

2. **Save as `test.csv`**

3. **Test upload:**
```bash
python test_upload.py test.csv
```

### **Reset Everything:**
```bash
# Stop server (Ctrl+C)
# Delete uploads folder
rm -rf backend/uploads

# Restart
python run.py
```

### **Check Dependencies:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

---

## Success Indicators

### ✅ **Working Upload Should Show:**
1. File selected in upload area
2. Progress bar appears
3. "Analysis completed successfully!" message
4. Results showing transaction counts
5. Charts update with your data

### ✅ **API Response Should Include:**
```json
{
  "status": "success",
  "summary": {
    "total_transactions": 10,
    "safe_payments": 7,
    "needs_attention": 3,
    "money_at_risk": 1250.00
  }
}
```

If you're still having issues after trying these solutions, the problem might be:
1. **Port conflict** - Try using port 8001 instead
2. **Firewall blocking** - Check firewall settings
3. **Python environment** - Try creating a virtual environment
4. **File corruption** - Re-download the code files

Remember: The test script (`python test_upload.py`) will help identify exactly what's not working! 🔍