#!/usr/bin/env python3
"""
Generate image for Ace Ventura-style animal expert townperson
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

def generate_animalexpert_image():
    """Generate Ace Ventura-style animal expert image"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
        return False
    
    genai.configure(api_key=api_key)
    
    prompt = """Create a portrait of an eccentric, quirky animal expert/investigator in Ace Ventura style.

The character should have:
- Bright, expressive face with eccentric energy and wild confidence
- Flamboyant, colorful clothing (tropical shirt, bright colors, fun patterns)
- Casual, relaxed posture suggesting comfort and eccentricity
- Maybe holding or near an animal (bird, snake, or other creature would be perfect)
- Wild, tousled hair with personality
- Big expressive eyes suggesting deep connection to animals
- Background suggesting outdoor nature or animal sanctuary
- Overall aesthetic: Mansion of Madness game style but with Ace Ventura's zany, colorful 1920s interpretation
- The character should radiate eccentric genius and animal communion
- Should feel fun, quirky, and slightly unhinged in a charming way
- Professional photographer quality with vivid colors"""
    
    try:
        print("🎨 Generating Ace Ventura-style animal expert image...")
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        response = model.generate_content([prompt])
        
        if response and response.parts:
            for part in reversed(response.parts):
                if hasattr(part, 'inline_data') and part.inline_data.data and len(part.inline_data.data) > 0:
                    image_data = part.inline_data.data
                    img_path = os.path.join(IMAGES_DIR, 'townperson_animalexpert.png')
                    with open(img_path, 'wb') as f:
                        f.write(image_data)
                    print(f"✅ Image created: {img_path}")
                    return True
        
        print("❌ No image data found in Gemini response")
        return False
            
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🦜 Generating Animal Expert Townperson...")
    print("=" * 60)
    generate_animalexpert_image()



