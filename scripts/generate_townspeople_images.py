#!/usr/bin/env python3
"""
Generate images for townspeople characters: Detective and Journalist
Both in Mansion of Madness aesthetic
"""

import os
import json
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

def generate_townspeople_images():
    """Generate images for Detective and Journalist townspeople"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
        return False
    
    genai.configure(api_key=api_key)
    
    characters = [
        {
            'id': 'townperson_detective',
            'name': 'Townperson Detective',
            'filename': 'townperson_detective.png',
            'prompt': """Create a portrait of a sharp, observant detective in 1920s detective noir style.
            
The character should have:
- Dark, serious expression with keen, analytical eyes
- Well-dressed in a sleek dark suit and fedora hat (tilted slightly)
- Slight stubble, suggesting years of investigating
- One hand near the lapel, other holding a cigarette or notebook
- Standing in shadows and dim lighting, very film noir
- Background suggesting an interrogation room or office
- Overall aesthetic: Mansion of Madness game style - dark, mysterious, noir detective from 1920s
- The character should radiate intelligence and determination
- Professional photographer quality, realistic details"""
        },
        {
            'id': 'townperson_journalist',
            'name': 'Townperson Journalist',
            'filename': 'townperson_journalist.png',
            'prompt': """Create a portrait of a sharp, curious journalist in 1920s style.
            
The character should have:
- Alert, intelligent expression with piercing eyes
- Well-dressed in fashionable 1920s attire: vest, dress shirt, and jacket
- Holding a notepad and pen, ready to take notes
- Sleek, styled hair (1920s fashion)
- Standing in an office or newspaper room setting
- Professional but slightly worn appearance suggesting years of chasing stories
- Overall aesthetic: Mansion of Madness game style - period detective/mystery game vibes
- The character should radiate ambition and sharp intellect
- Professional photographer quality, realistic period-accurate details"""
        }
    ]
    
    for char in characters:
        img_path = os.path.join(IMAGES_DIR, char['filename'])
        
        try:
            print(f"🎨 Generating image for {char['name']}...")
            model = genai.GenerativeModel('gemini-2.5-flash-image')
            response = model.generate_content([char['prompt']])
            
            if response and response.parts:
                for part in reversed(response.parts):
                    if hasattr(part, 'inline_data') and part.inline_data.data and len(part.inline_data.data) > 0:
                        image_data = part.inline_data.data
                        with open(img_path, 'wb') as f:
                            f.write(image_data)
                        print(f"✅ Image created: {img_path}")
                        break
            else:
                print(f"❌ No image data found for {char['name']}")
                
        except Exception as e:
            print(f"❌ Error generating image for {char['name']}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n✨ Image generation complete!")
    return True

if __name__ == '__main__':
    print("🔮 Generating Townspeople Characters...")
    print("=" * 60)
    generate_townspeople_images()


