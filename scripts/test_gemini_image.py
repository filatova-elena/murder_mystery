#!/usr/bin/env python3
"""
Test Gemini 2.5 Pro image generation
Uses .env file for API key configuration
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed, using environment variables directly")

import google.generativeai as genai

def generate_test_image():
    """Generate a test image using Gemini 2.5 Pro"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: Please set GEMINI_API_KEY in .env file")
        print("   Edit .env and replace 'your_gemini_api_key_here' with your actual key")
        return False
    
    print("🎨 Testing Gemini 2.5 Pro Image Generation")
    print("="*60)
    print(f"API Key loaded: {api_key[:10]}...{api_key[-10:]}")
    print("Model: gemini-2.5-pro")
    print("="*60 + "\n")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Test with image generation prompt
        print("Generating: Vintage 1920s photograph - Harbor scene")
        print("-" * 60)
        prompt = """Create a vintage black and white photograph from the 1920s showing a harbor scene. 
        The image should show period-appropriate boats, docks, and harbor workers in 1920s attire.
        Make it look like an authentic historical photograph from that era with sepia/grayscale tones and the quality of old film photography."""
        
        print(f"Prompt: {prompt[:80]}...\n")
        
        response = model.generate_content([prompt])
        
        print(f"✅ Response received from Gemini 2.5 Pro!")
        print(f"Response type: {type(response)}")
        
        if response.text:
            print(f"\nResponse text:\n{response.text[:500]}...\n")
        
        if hasattr(response, 'parts'):
            print(f"\nResponse parts: {len(response.parts)}")
            for i, part in enumerate(response.parts):
                print(f"  Part {i}: {type(part).__name__}")
                if hasattr(part, 'mime_type'):
                    print(f"    MIME type: {part.mime_type}")
                    if 'image' in part.mime_type:
                        print(f"    ✅ Image data found!")
                        # Save image
                        if hasattr(part, 'data'):
                            output_path = Path('test_generated_image.jpg')
                            with open(output_path, 'wb') as f:
                                f.write(part.data)
                            print(f"    Saved to: {output_path}")
        
        print("\n" + "="*60)
        print("✅ Gemini 2.5 Pro is working!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_test_image()
    sys.exit(0 if success else 1)
