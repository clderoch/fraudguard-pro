#!/usr/bin/env python3
"""
FraudGuard Pro - Easy Startup Script
This script helps you get FraudGuard Pro running quickly
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import time

def print_banner():
    """Print the FraudGuard Pro banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🛡️  FraudGuard Pro - AI-Powered Fraud Detection for Small Business       ║
║                                                                              ║
║   Starting your modern fraud detection dashboard...                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def setup_directories():
    """Create necessary directories"""
    directories = [
        "backend",
        "backend/models",
        "backend/uploads",
        "frontend"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    requirements_path = Path("backend/requirements.txt")
    
    if not requirements_path.exists():
        print("❌ Error: requirements.txt not found in backend folder")
        print("   Please make sure you have the requirements.txt file in backend/")
        sys.exit(1)
    
    try:
        # Install dependencies
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
        ], check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("   Please install dependencies manually with:")
        print(f"   pip install -r {requirements_path}")
        sys.exit(1)

def check_files():
    """Check if all necessary files exist"""
    required_files = [
        "backend/main.py",
        "backend/models/fraud_detection.py",
        "backend/requirements.txt",
        "frontend/index.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Error: Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n   Please make sure all files are in the correct locations")
        sys.exit(1)
    
    print("✅ All required files found")

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting FraudGuard Pro server...")
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        sys.exit(1)
    
    # Use the reliable server runner
    try:
        print("   Using backend/run_server.py for reliable startup")
        print("   Server will be available at http://localhost:8080")
        print("   Press Ctrl+C to stop the server")
        print("\n" + "="*80)
        
        # Wait a moment then open browser
        import threading
        def open_browser():
            time.sleep(3)
            webbrowser.open("http://localhost:8080")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the server using our reliable runner
        subprocess.run([
            sys.executable, "run_server.py"
        ], cwd=backend_dir)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("💡 Try running: cd backend && python run_server.py")
        sys.exit(1)

def main():
    """Main function to run the startup process"""
    print_banner()
    
    print("🔍 Checking system requirements...")
    check_python_version()
    
    print("\n📁 Setting up directories...")
    setup_directories()
    
    print("\n📋 Checking required files...")
    check_files()
    
    print("\n📦 Installing dependencies...")
    install_dependencies()
    
    print("\n✅ Setup complete! Starting server...")
    time.sleep(2)
    
    start_server()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)