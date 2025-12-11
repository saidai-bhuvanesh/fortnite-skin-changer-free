"""
Backend Health Check Script
Tests if the backend server is running and responding correctly
"""

import requests
import sys
from colorama import init, Fore, Style

init(autoreset=True)

API_URL = "http://localhost:8000"

def print_status(message, success=True):
    """Print colored status message"""
    if success:
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def check_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print_status("Backend server is ONLINE", True)
            return True
        else:
            print_status(f"Backend returned status {response.status_code}", False)
            return False
    except requests.exceptions.ConnectionError:
        print_status("Backend server is OFFLINE - Cannot connect", False)
        print(f"{Fore.YELLOW}→ Make sure to run: python backend/main.py{Style.RESET_ALL}")
        return False
    except Exception as e:
        print_status(f"Error checking backend: {str(e)}", False)
        return False

def check_chat():
    """Test chat endpoint"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"query": "Hello", "mode": "chat"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print_status("Chat endpoint is WORKING", True)
            print(f"{Fore.CYAN}  Sample response: {data.get('answer', '')[:100]}...{Style.RESET_ALL}")
            return True
        else:
            print_status(f"Chat endpoint returned status {response.status_code}", False)
            return False
    except Exception as e:
        print_status(f"Chat endpoint error: {str(e)}", False)
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            print_status("Ollama is RUNNING", True)
            return True
        else:
            print_status("Ollama returned unexpected status", False)
            return False
    except requests.exceptions.ConnectionError:
        print_status("Ollama is NOT RUNNING", False)
        print(f"{Fore.YELLOW}→ Start Ollama to enable AI responses{Style.RESET_ALL}")
        return False
    except Exception as e:
        print_status(f"Ollama check error: {str(e)}", False)
        return False

def main():
    """Run all health checks"""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"  Bhuvi AI Assistant - Health Check")
    print(f"{'='*50}{Style.RESET_ALL}\n")
    
    # Check backend
    print(f"{Fore.YELLOW}[1/3] Checking Backend Server...{Style.RESET_ALL}")
    backend_ok = check_health()
    print()
    
    if not backend_ok:
        print(f"\n{Fore.RED}Backend is not running. Please start it first:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  python backend/main.py{Style.RESET_ALL}\n")
        sys.exit(1)
    
    # Check chat endpoint
    print(f"{Fore.YELLOW}[2/3] Testing Chat Endpoint...{Style.RESET_ALL}")
    chat_ok = check_chat()
    print()
    
    # Check Ollama
    print(f"{Fore.YELLOW}[3/3] Checking Ollama...{Style.RESET_ALL}")
    ollama_ok = check_ollama()
    print()
    
    # Summary
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    if backend_ok and chat_ok:
        print(f"{Fore.GREEN}✓ All systems operational!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}You can now open frontend/index.html in your browser{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}✗ Some systems are not working{Style.RESET_ALL}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
