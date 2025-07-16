#!/usr/bin/env python3
"""
Server runner for FraudGuard Pro
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Import the main application
    from main import app
    print("✅ Successfully imported FastAPI app")
    
    # Start the server
    import uvicorn
    print("🚀 Starting FraudGuard Pro server...")
    print("📍 Server will be available at: http://localhost:8080")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8080,  # Use different port to avoid conflicts
        reload=False,  # Disable reload for stability
        log_level="info"
    )
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all dependencies are installed:")
    print("  pip install fastapi uvicorn python-multipart pandas numpy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Server error: {e}")
    sys.exit(1)
