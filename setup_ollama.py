"""
Ollama Setup Script
Downloads and tests Ollama model for unlimited AI fallback
"""

import subprocess
import sys

def run_command(cmd):
    """Run a command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🤖 Ollama Setup for Unlimited AI")
    print("=" * 50)
    
    # Check if Ollama is installed
    print("\n1️⃣ Checking Ollama installation...")
    success, stdout, stderr = run_command("ollama --version")
    
    if not success:
        print("❌ Ollama not found in PATH")
        print("\n📥 Please follow these steps:")
        print("   1. Restart your terminal/PowerShell")
        print("   2. Or run: $env:Path += ';C:\\Users\\$env:USERNAME\\AppData\\Local\\Programs\\Ollama'")
        print("   3. Then run this script again")
        return
    
    print(f"✅ Ollama installed: {stdout.strip()}")
    
    # Download Llama 3.1 model
    print("\n2️⃣ Downloading Llama 3.1 model (this may take a few minutes)...")
    print("   Model size: ~4.7GB")
    
    success, stdout, stderr = run_command("ollama pull llama3.1")
    
    if success:
        print("✅ Llama 3.1 downloaded successfully!")
    else:
        print(f"❌ Failed to download model: {stderr}")
        return
    
    # Test the model
    print("\n3️⃣ Testing Ollama...")
    success, stdout, stderr = run_command('ollama run llama3.1 "Say hello in one sentence"')
    
    if success:
        print(f"✅ Ollama is working!")
        print(f"   Response: {stdout.strip()}")
    else:
        print(f"❌ Test failed: {stderr}")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Ollama setup complete!")
    print("\n📝 Next steps:")
    print("   1. Your backend is already configured for Ollama fallback")
    print("   2. Restart your backend server")
    print("   3. When Gemini quota is exhausted, Ollama will automatically take over")
    print("\n💡 Tip: Ollama runs locally, so it's 100% free and unlimited!")

if __name__ == "__main__":
    main()
