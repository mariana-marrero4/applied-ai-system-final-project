#!/usr/bin/env python3
"""Quick test script to verify Google Gemini API key configuration"""

import os
import sys
from pathlib import Path

# Find project root by looking for .env file
def find_project_root():
    """Search up the directory tree for .env file"""
    current = Path(__file__).parent
    for _ in range(5):  # Search up to 5 levels
        if (current / ".env").exists():
            return current
        current = current.parent
    # Fallback to parent of tests/ directory
    return Path(__file__).parent.parent

project_root = find_project_root()
env_path = project_root / ".env"

print("=" * 60)
print("🔍 API Key Configuration Test")
print("=" * 60)

# Check if .env file exists
print(f"\n✓ .env file path: {env_path}")
print(f"  Exists: {env_path.exists()}")

if not env_path.exists():
    print(f"  ❌ ERROR: Could not find .env file!")
    print(f"  Project root detected as: {project_root}")
    sys.exit(1)

# Load .env
from dotenv import load_dotenv
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key is loaded
print(f"\n✓ GOOGLE_API_KEY loaded: {'✅ YES' if api_key else '❌ NO'}")
if api_key:
    print(f"  Key (first 30 chars): {api_key[:30]}...")
    print(f"  Key length: {len(api_key)} characters")
else:
    print("  ⚠️ API key is None or empty!")

# Try to import and test Gemini
try:
    import google.generativeai as genai
    print(f"\n✓ google-generativeai library: ✅ Installed")
    
    if api_key:
        genai.configure(api_key=api_key)
        print("  ✅ API configured successfully")
        
        # Try to generate a simple response
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("\n  Testing model with simple prompt...")
        response = model.generate_content("Responde solamente con 'OK'")
        print(f"  Response: {response.text}")
        print("\n✅ API CONNECTION TEST PASSED!")
    else:
        print("  ❌ Cannot test: API key not loaded")
        
except ImportError as e:
    print(f"\n✓ google-generativeai library: ❌ Not installed")
    print(f"  Error: {e}")
except Exception as e:
    print(f"\n❌ Error during API test: {e}")

print("\n" + "=" * 60)
