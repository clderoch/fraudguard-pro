"""
Enhanced FraudGuard Pro Server
Starts the enhanced version with advanced analytics and comprehensive fraud detection
"""

import uvicorn
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def main():
    print("🚀 Starting FraudGuard Pro Enhanced Server...")
    print("=" * 60)
    print("🛡️  FraudGuard Pro - Enhanced Fraud Detection")
    print("📊 Advanced Analytics & Comprehensive Reporting")
    print("=" * 60)
    print("")
    print("🌐 Dashboard URL: http://localhost:8080")
    print("📋 API Documentation: http://localhost:8080/docs")
    print("🔍 Health Check: http://localhost:8080/api/health")
    print("")
    print("✨ New Enhanced Features:")
    print("  • Advanced fraud detection algorithms")
    print("  • Real-time risk assessment")
    print("  • Industry-specific analysis")
    print("  • Time-based pattern detection")
    print("  • Geographic anomaly detection")
    print("  • Comprehensive reporting")
    print("  • Interactive data visualization")
    print("  • Export capabilities")
    print("")
    print("🔧 Starting server...")
    
    try:
        # Import the enhanced app
        from main_enhanced import app
        
        # Run the server
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8080,
            reload=False,  # Disable reload for better performance
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Error importing enhanced app: {e}")
        print("Falling back to standard version...")
        
        try:
            from main import app
            uvicorn.run(app, host="0.0.0.0", port=8080)
        except Exception as e2:
            print(f"❌ Error starting server: {e2}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error starting enhanced server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
