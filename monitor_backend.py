#!/usr/bin/env python3
"""
Backend Health Monitor - PERMANENT FIX
Ensures the backend stays running, handles crashes, and cleans up zombie processes.
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
CHECK_INTERVAL = 10  # Check every 10 seconds
MAX_RETRIES = 999999 # Effectively infinite

def kill_existing_backend():
    """Force kill any existing uvicorn processes to free the port"""
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/IM", "uvicorn.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/FI", "WINDOWTITLE eq *uvicorn*"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("🧹 Cleaned up existing backend processes.")
    except Exception as e:
        pass

def is_backend_running():
    """Check if backend is responding"""
    try:
        response = requests.get(BACKEND_URL, timeout=3)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend server"""
    backend_dir = Path(__file__).parent / "backend"
    
    # Ensure backend directory exists
    if not backend_dir.exists():
        print(f"❌ Error: Backend directory not found at {backend_dir}")
        return None

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"
    ]
    
    print(f"🚀 Starting backend server...")
    try:
        process = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    except Exception as e:
        print(f"❌ Failed to launch backend: {e}")
        return None

def monitor_backend():
    """Monitor backend and restart if needed"""
    print("🛡️  Starting PERMANENT Backend Monitor")
    print("    This script will keep the backend alive no matter what.")
    print("    Press Ctrl+C to stop.\n")
    
    # Initial cleanup
    kill_existing_backend()
    
    backend_process = None
    
    # First start
    backend_process = start_backend()
    time.sleep(5) # Warmup
    
    while True:
        try:
            if not is_backend_running():
                print(f"⚠️  Backend seems DOWN. Restarting in 2s...")
                
                # Cleanup old process
                if backend_process:
                    try:
                        backend_process.terminate()
                        backend_process.wait(timeout=3)
                    except:
                        try:
                            backend_process.kill()
                        except:
                            pass
                
                kill_existing_backend()
                time.sleep(2)
                
                # Restart
                backend_process = start_backend()
                
                # Wait a bit longer for startup
                time.sleep(8)
                
                if is_backend_running():
                    print("✅ Backend recovered and is ONLINE!")
                else:
                    print("⚠️  Backend taking time to respond... will check again.")
            
            # Sleep before next check
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped by user.")
            if backend_process:
                backend_process.terminate()
            sys.exit(0)
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_backend()
