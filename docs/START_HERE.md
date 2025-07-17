# 🚀 FraudGuard Pro - How to Start the Application

## **Quick Start (Choose One Method)**

### **Method 1: Full Setup & Start (Recommended for first time)**
```bash
cd c:\Users\craig\fraudguard-pro
python run.py
```
- ✅ Checks system requirements
- ✅ Installs dependencies automatically  
- ✅ Creates necessary directories
- ✅ Starts server on port 8080
- ✅ Opens browser automatically

### **Method 2: Direct Server Start (Fastest)**
```bash
cd c:\Users\craig\fraudguard-pro\backend
python run_server.py
```
- ✅ Direct server startup
- ✅ Runs on port 8080
- ✅ No dependency checks (assumes already installed)
- ✅ Most reliable for development

## **Access Your Dashboard**
Once started, open your browser to:
- **http://localhost:8080**

## **Current Status**
- ✅ Server is currently running on port 8080
- ✅ Upload functionality is working
- ✅ All tests passed

## **Troubleshooting**

### If Method 1 doesn't work:
```bash
cd c:\Users\craig\fraudguard-pro\backend
python run_server.py
```

### If port 8080 is busy:
```bash
cd c:\Users\craig\fraudguard-pro\backend
# Edit run_server.py and change port to 8090
python run_server.py
```

### To stop the server:
- Press `Ctrl+C` in the terminal

## **File Upload Testing**
1. Go to http://localhost:8080
2. Upload `sample_transactions.csv` (in main directory)
3. View fraud analysis results

## **What Each File Does**
- **`run.py`** (main directory) - Full setup and startup script
- **`run_server.py`** (backend) - Direct server runner
- **`main.py`** (backend) - FastAPI application code
- **`test_upload_api.py`** (backend) - Upload functionality tests

## **Recommended Workflow**
1. **First time**: Use `python run.py` from main directory
2. **Development**: Use `python run_server.py` from backend directory
3. **Testing**: Use the test scripts in backend directory
