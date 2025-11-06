#!/usr/bin/env python3
"""
Regenerate journalist image as a woman
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images/characters')
os.makedirs(IMAGES_DIR, exist_ok=True)

def regenerate_journalist_image():
    """Regenerate journalist image as a woman"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
        return False
    
    genai.configure(api_key=api_key)
    
    prompt = """Create a portrait of a sharp, intelligent female journalist in 1920s style.

The character should be:
- A woman with alert, intelligent expression and piercing eyes
- Well-dressed in fashionable 1920s attire: elegant vest, dress shirt, and blazer
- Holding a notepad and pen, ready to take notes
- Sleek, styled hair in 1920s fashion (bob cut or waves)
- Standing in a newspaper office or newsroom setting
- Professional but slightly worn appearance suggesting years of chasing stories
- Confident, ambitious, and sharp-minded
- Overall aesthetic: Mansion of Madness game style - period detective/mystery game vibes
- The character should radiate ambition and sharp intellect
- Professional photographer quality, realistic period-accurate details"""
    
    try:
        print("🎨 Regenerating journalist image as a woman...")
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        response = model.generate_content([prompt])
        
        if response and response.parts:
            for part in reversed(response.parts):
                if hasattr(part, 'inline_data') and part.inline_data.data and len(part.inline_data.data) > 0:
                    image_data = part.inline_data.data
                    img_path = os.path.join(IMAGES_DIR, 'townperson_journalist.png')
                    with open(img_path, 'wb') as f:
                        f.write(image_data)
                    print(f"✅ Image updated: {img_path}")
                    return True
        
        print("❌ No image data found in Gemini response")
        return False
            
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("📰 Regenerating Journalist as Female...")
    print("=" * 60)
    regenerate_journalist_image()

