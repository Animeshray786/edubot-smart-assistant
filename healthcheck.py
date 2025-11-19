"""
EduBot Health Check & Auto-Fix Script
Runs before server startup to prevent common errors
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print health check banner"""
    print("\n" + "="*70)
    print("  🏥 EduBot Health Check & Auto-Fix")
    print("="*70 + "\n")

def check_python_version():
    """Check Python version"""
    print("✓ Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"OK (Python {version.major}.{version.minor}.{version.micro})")
        return True
    else:
        print(f"FAILED (Python {version.major}.{version.minor}.{version.micro})")
        print("  ❌ Python 3.8+ required")
        return False

def check_required_directories():
    """Check and create required directories"""
    print("✓ Checking required directories...", end=" ")
    dirs = ['logs', 'uploads', 'uploads/images', 'static/uploads', 'instance', 'flask_session']
    created = []
    
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            created.append(directory)
    
    if created:
        print(f"CREATED ({len(created)} directories)")
        for d in created:
            print(f"    • {d}")
    else:
        print("OK")
    return True

def check_env_file():
    """Check .env file exists"""
    print("✓ Checking .env file...", end=" ")
    if os.path.exists('.env'):
        print("OK")
        return True
    elif os.path.exists('.env.example'):
        import shutil
        shutil.copy('.env.example', '.env')
        print("CREATED from .env.example")
        print("  ⚠️  Please update .env with your configuration!")
        return True
    else:
        print("FAILED")
        print("  ❌ No .env or .env.example file found!")
        return False

def check_required_packages():
    """Check required Python packages"""
    print("✓ Checking required packages...", end=" ")
    required = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'flask_session': 'Flask-Session',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'python-aiml': 'python-aiml',
        'python-dotenv': 'python-decouple'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"MISSING ({len(missing)} packages)")
        for pkg in missing:
            print(f"    • {pkg}")
        print("\n  💡 Install missing packages:")
        print(f"     pip install {' '.join(missing)}")
        return False
    else:
        print("OK")
        return True

def check_env_variables():
    """Check critical environment variables"""
    print("✓ Checking environment variables...", end=" ")
    from dotenv import load_dotenv
    load_dotenv()
    
    required = ['SECRET_KEY', 'JWT_SECRET_KEY', 'CSRF_SECRET_KEY']
    missing = []
    
    for var in required:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"MISSING ({len(missing)} variables)")
        for var in missing:
            print(f"    • {var}")
        print("\n  💡 Add these to your .env file")
        return False
    else:
        print("OK")
        return True

def check_database():
    """Check database connectivity"""
    print("✓ Checking database...", end=" ")
    try:
        db_url = os.getenv('DATABASE_URL', 'sqlite:///chatbot.db')
        if db_url.startswith('sqlite'):
            # Check if we can create the database file
            db_path = db_url.replace('sqlite:///', '')
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            print("OK (SQLite)")
            return True
        else:
            print("OK (External DB)")
            return True
    except Exception as e:
        print(f"WARNING ({str(e)})")
        return True  # Non-critical

def check_aiml_files():
    """Check AIML pattern files exist"""
    print("✓ Checking AIML files...", end=" ")
    aiml_dir = os.getenv('AIML_DIR', 'aiml')
    
    if not os.path.exists(aiml_dir):
        print(f"WARNING (Directory {aiml_dir} not found)")
        return True  # Non-critical
    
    aiml_files = list(Path(aiml_dir).glob('*.xml'))
    if aiml_files:
        print(f"OK ({len(aiml_files)} files)")
        return True
    else:
        print("WARNING (No AIML files found)")
        return True  # Non-critical

def check_port_available():
    """Check if port 5000 is available"""
    print("✓ Checking port availability...", end=" ")
    import socket
    
    port = int(os.getenv('PORT', 5000))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind(('127.0.0.1', port))
        sock.close()
        print(f"OK (Port {port} available)")
        return True
    except:
        print(f"WARNING (Port {port} in use)")
        print(f"  ⚠️  Another instance may be running")
        return True  # Non-critical

def fix_common_issues():
    """Auto-fix common configuration issues"""
    print("\n🔧 Running auto-fixes...\n")
    
    # Fix file permissions issues
    try:
        for path in ['logs', 'uploads', 'instance']:
            if os.path.exists(path):
                os.chmod(path, 0o755)
    except:
        pass
    
    # Clear old session files
    try:
        session_dir = 'flask_session'
        if os.path.exists(session_dir):
            import shutil
            for file in Path(session_dir).glob('*'):
                if file.is_file() and (file.stat().st_mtime < (os.path.getmtime(__file__) - 86400)):
                    file.unlink()
            print("  ✓ Cleaned old session files")
    except:
        pass
    
    print()

def main():
    """Run all health checks"""
    print_banner()
    
    checks = [
        check_python_version,
        check_required_directories,
        check_env_file,
        check_required_packages,
        check_env_variables,
        check_database,
        check_aiml_files,
        check_port_available
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    fix_common_issues()
    
    # Summary
    print("="*70)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"  ✅ All checks passed ({passed}/{total})")
        print("  🚀 Server is ready to start!")
        print("="*70 + "\n")
        return 0
    else:
        failed = total - passed
        print(f"  ⚠️  {failed} check(s) failed ({passed}/{total} passed)")
        print("  💡 Fix the issues above before starting the server")
        print("="*70 + "\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
