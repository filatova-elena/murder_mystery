#!/usr/bin/env python3
"""
List available Gemini models
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai

api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

print("🔍 Available Gemini Models:")
print("="*60)

for model in genai.list_models():
    print(f"\nModel: {model.name}")
    print(f"  Display: {model.display_name}")
    print(f"  Description: {model.description[:100]}...")
    if hasattr(model, 'supported_generation_methods'):
        print(f"  Methods: {model.supported_generation_methods}")
