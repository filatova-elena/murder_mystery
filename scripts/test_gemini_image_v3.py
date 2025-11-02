#!/usr/bin/env python3
"""
Test Gemini 2.5 Flash Image generation - Extract and save images
"""

import os
import sys
from pathlib import Path
import base64

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai

def generate_test_image():
    """Generate a test image using Gemini 2.5 Flash Image"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: Please set GEMINI_API_KEY in .env file")
        return False
    
    print("🎨 Testing Gemini 2.5 Flash Image Generation")
    print("="*60)
    print(f"API Key loaded: {api_key[:10]}...{api_key[-10:]}")
    print("Model: gemini-2.5-flash-image")
    print("="*60 + "\n")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        # Test with image generation prompt
        print("🖼️  Generating: Vintage 1920s harbor photograph")
        print("-" * 60)
        prompt = """Create a vintage black and white photograph from the 1920s showing a bustling harbor scene. 
        Include period-appropriate boats, wooden docks, and harbor workers in 1920s attire.
        Make it look like an authentic historical photograph with sepia tones and film grain."""
        
        print(f"Prompt: {prompt[:80]}...\n")
        
        response = model.generate_content([prompt])
        
        print(f"✅ Response received from Gemini 2.5 Flash Image!")
        
        # Check for images in the response
        print(f"\nExtracting image data...")
        image_count = 0
        
        if hasattr(response, 'parts'):
            for i, part in enumerate(response.parts):
                # Check if this part has inline image data
                if hasattr(part, 'inline_data'):
                    inline_data = part.inline_data
                    if inline_data and hasattr(inline_data, 'data'):
                        image_count += 1
                        img_data = inline_data.data
                        
                        # Determine file extension from mime type
                        mime_type = inline_data.mime_type if hasattr(inline_data, 'mime_type') else 'image/png'
                        ext = mime_type.split('/')[-1]
                        
                        output_path = Path(f'test_generated_image.{ext}')
                        
                        # Write binary data
                        with open(output_path, 'wb') as f:
                            f.write(img_data)
                        
                        print(f"Part {i}: ✅ Image saved!")
                        print(f"  MIME type: {mime_type}")
                        print(f"  File: {output_path}")
                        print(f"  Size: {len(img_data)} bytes ({len(img_data)/(1024**2):.2f} MB)")
        
        print("\n" + "="*60)
        if image_count > 0:
            print(f"✅ SUCCESS! Generated and saved {image_count} image(s)!")
            print(f"  Image file: test_generated_image.png")
            print(f"\n🎉 Gemini 2.5 Flash Image is working perfectly!")
        else:
            print("❌ No images extracted from response")
        print("="*60)
        
        return image_count > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_test_image()
    sys.exit(0 if success else 1)
