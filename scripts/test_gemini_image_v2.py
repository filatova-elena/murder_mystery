#!/usr/bin/env python3
"""
Test Gemini 2.5 Pro image generation - Extract images from response
"""

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai

def generate_test_image():
    """Generate a test image using Gemini 2.5 Pro"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: Please set GEMINI_API_KEY in .env file")
        return False
    
    print("🎨 Testing Gemini 2.5 Pro - Examining Response Structure")
    print("="*60)
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        prompt = """Create a vintage black and white photograph from the 1920s showing a harbor scene."""
        
        print("📤 Sending request...")
        response = model.generate_content([prompt])
        
        print(f"\n✅ Response received!")
        print(f"Response type: {type(response)}")
        
        # Check all attributes
        print(f"\nResponse attributes:")
        for attr in dir(response):
            if not attr.startswith('_'):
                try:
                    value = getattr(response, attr)
                    if not callable(value):
                        print(f"  {attr}: {type(value).__name__}")
                except:
                    pass
        
        # Detailed part analysis
        print(f"\n\nDetailed Parts Analysis:")
        print(f"Number of parts: {len(response.parts)}")
        
        for i, part in enumerate(response.parts):
            print(f"\n--- Part {i} ---")
            print(f"Type: {type(part).__name__}")
            
            # List all attributes of this part
            for attr in dir(part):
                if not attr.startswith('_'):
                    try:
                        value = getattr(part, attr)
                        if not callable(value):
                            if isinstance(value, bytes):
                                print(f"  {attr}: <bytes: {len(value)} bytes>")
                            else:
                                val_str = str(value)
                                if len(val_str) > 100:
                                    print(f"  {attr}: {val_str[:100]}...")
                                else:
                                    print(f"  {attr}: {val_str}")
                    except:
                        pass
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_test_image()
    sys.exit(0 if success else 1)
