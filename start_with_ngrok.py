"""
Start EduBot with Ngrok - Public Internet Access
Run this to get a worldwide URL for your chatbot
"""
from pyngrok import ngrok
import os
import sys
import subprocess
import time

# Configuration
NGROK_AUTH_TOKEN = "35YcshiRPCEINX3ghfX6Fs6BMux_5fnrMy7UFwq2LHDB2S2QC"  # Your ngrok auth token
FLASK_PORT = 5000

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Ngrok is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("[WARNING] Ngrok not found in PATH")
    print("\nPlease install ngrok:")
    print("1. Download from: https://ngrok.com/download")
    print("2. Extract ngrok.exe to C:\\ngrok\\")
    print("3. Add C:\\ngrok\\ to your PATH")
    print("\nOr run: choco install ngrok")
    return False

def setup_ngrok():
    """Set up ngrok tunnel"""
    try:
        # Set auth token if provided
        if NGROK_AUTH_TOKEN != "YOUR_AUTH_TOKEN_HERE":
            ngrok.set_auth_token(NGROK_AUTH_TOKEN)
            print("[OK] Ngrok authenticated")
        else:
            print("[WARNING] Using ngrok without auth token")
            print("Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken")
            print("Then edit this file and replace YOUR_AUTH_TOKEN_HERE")
            print("\nContinuing anyway (limited to 40 connections/min)...\n")
            time.sleep(2)
        
        # Start tunnel
        print(f"[OK] Starting ngrok tunnel on port {FLASK_PORT}...")
        public_url = ngrok.connect(FLASK_PORT)
        
        # Display success message
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                🎉 EDUBOT IS NOW PUBLIC! 🎉                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🌍 PUBLIC URL (Share this worldwide):                       ║
║  {str(public_url):^60} ║
║                                                               ║
║  📱 Local URL (Your computer only):                          ║
║  http://localhost:{FLASK_PORT}                                       ║
║                                                               ║
║  🎛️  Ngrok Dashboard (Monitor traffic):                      ║
║  http://127.0.0.1:4040                                       ║
║                                                               ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ Share the PUBLIC URL with ANYONE worldwide!              ║
║  ✅ Valid for 2 hours (restart to get new session)           ║
║  ✅ Press CTRL+C to stop both Flask and Ngrok                ║
║                                                               ║
║  📊 Monitor live traffic at: http://127.0.0.1:4040           ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        return public_url
        
    except Exception as e:
        print(f"[ERROR] Failed to start ngrok: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have internet connection")
        print("2. Get auth token from: https://dashboard.ngrok.com")
        print("3. Set NGROK_AUTH_TOKEN in this file")
        print("4. Install pyngrok: pip install pyngrok")
        sys.exit(1)

def start_flask():
    """Start Flask application"""
    print("\n[OK] Starting Flask server...")
    print("=" * 60)
    
    try:
        # Import and run Flask app
        from app import app
        app.run(
            host='0.0.0.0',
            port=FLASK_PORT,
            debug=False  # Disable debug in public mode for security
        )
    except KeyboardInterrupt:
        print("\n[OK] Shutting down Flask and Ngrok...")
        ngrok.kill()
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Flask failed to start: {e}")
        ngrok.kill()
        sys.exit(1)

def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║             EduBot - Public Deployment with Ngrok             ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check dependencies
    try:
        import pyngrok
        print("[OK] pyngrok module found")
    except ImportError:
        print("[ERROR] pyngrok not installed")
        print("\nInstall it with:")
        print("  pip install pyngrok")
        sys.exit(1)
    
    # Setup ngrok tunnel
    public_url = setup_ngrok()
    
    # Start Flask
    start_flask()

if __name__ == '__main__':
    main()
