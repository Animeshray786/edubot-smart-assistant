"""
Start EduBot with LocalTunnel - FREE, NO SIGNUP REQUIRED!
Instant public URL with zero configuration
"""
import subprocess
import sys
import time
import threading

def check_localtunnel():
    """Check if localtunnel is installed"""
    try:
        result = subprocess.run(['lt', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] LocalTunnel is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("[INFO] LocalTunnel not found, installing...")
    print("Running: npm install -g localtunnel")
    
    try:
        subprocess.run(['npm', 'install', '-g', 'localtunnel'], check=True)
        print("[OK] LocalTunnel installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install LocalTunnel")
        print("Please run manually: npm install -g localtunnel")
        return False

def start_flask_in_background():
    """Start Flask server in background"""
    print("[OK] Starting Flask server on port 5000...")
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_localtunnel():
    """Start LocalTunnel"""
    print("[OK] Starting LocalTunnel...")
    print("[INFO] This may take 10-15 seconds...\n")
    
    # Start localtunnel
    process = subprocess.Popen(
        ['lt', '--port', '5000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Read output
    public_url = None
    for line in process.stdout:
        print(line.strip())
        if 'your url is:' in line.lower():
            public_url = line.split('is:')[-1].strip()
            break
    
    if public_url:
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║              🎉 EDUBOT IS NOW PUBLIC! 🎉                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🌍 PUBLIC URL (Share this worldwide):                       ║
║  {public_url:^60} ║
║                                                               ║
║  📱 Local URL (Your computer only):                          ║
║  http://localhost:5000                                       ║
║                                                               ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ NO SIGNUP REQUIRED!                                      ║
║  ✅ Share the PUBLIC URL with ANYONE worldwide!              ║
║  ✅ Press CTRL+C to stop both Flask and LocalTunnel          ║
║                                                               ║
║  ⚠️  First-time visitors may see a warning page             ║
║      (just click "Continue" - it's safe!)                    ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    return process

def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║          EduBot - Public Deployment with LocalTunnel          ║
║                  FREE - NO SIGNUP REQUIRED!                   ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check/Install LocalTunnel
    if not check_localtunnel():
        sys.exit(1)
    
    print("\n" + "="*60)
    
    # Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask_in_background, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    print("[INFO] Waiting for Flask to start...")
    time.sleep(3)
    
    print("[OK] Flask is running!")
    print("="*60 + "\n")
    
    # Start LocalTunnel
    lt_process = start_localtunnel()
    
    try:
        # Keep running
        lt_process.wait()
    except KeyboardInterrupt:
        print("\n[OK] Shutting down...")
        lt_process.terminate()
        sys.exit(0)

if __name__ == '__main__':
    main()
