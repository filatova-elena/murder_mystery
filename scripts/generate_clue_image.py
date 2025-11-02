#!/usr/bin/env python3
"""
Generate images for clues using Gemini 2.5 Flash Image
Saves images to qr_codes/ directory with standardized naming
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

def generate_clue_image(clue_name: str, prompt: str, output_filename: str = None):
    """
    Generate an image for a clue
    
    Args:
        clue_name: Human-readable name for the clue
        prompt: Detailed prompt for image generation
        output_filename: Optional custom output filename (default: {clue_name}.png)
    
    Returns:
        Path to saved image or None if failed
    """
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: GEMINI_API_KEY not set in .env file")
        return None
    
    if output_filename is None:
        # Sanitize clue name for filename
        output_filename = clue_name.lower().replace(' ', '_') + '.png'
    
    output_path = Path('clue_images') / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"\n📸 Generating: {clue_name}")
        print(f"   Output: {output_path}")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        response = model.generate_content([prompt])
        
        # Extract image data
        image_count = 0
        if hasattr(response, 'parts'):
            for part in response.parts:
                if hasattr(part, 'inline_data'):
                    inline_data = part.inline_data
                    if inline_data and hasattr(inline_data, 'data'):
                        img_data = inline_data.data
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_data)
                        
                        image_count += 1
                        print(f"   ✅ Saved ({len(img_data)/(1024**2):.2f} MB)")
                        return output_path
        
        if image_count == 0:
            print(f"   ❌ No image in response")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    """Generate images for various clues"""
    
    print("="*60)
    print("🎨 Clue Image Generator")
    print("="*60)
    
    clues_to_generate = [
        {
            "name": "Romano Family Photograph",
            "prompt": """Create a vintage black and white photograph from the 1920s-1930s showing the Romano family. 
            The image should depict an Italian shipping family posed formally for a family portrait. 
            Include Frankie Romano (a distinguished man in his 30s-40s) with his family members around him in period clothing.
            Set it in an elegant studio or home setting with period furnishings from that era.
            Add subtle details that indicate wealth and involvement in shipping business (nautical elements, fine furniture).
            Use sepia and grayscale tones to make it look like an authentic historical photograph with film grain texture.
            The photo should have the formal, posed quality of 1920s-1930s family portraits."""
        }
    ]
    
    successful = 0
    for clue in clues_to_generate:
        result = generate_clue_image(clue["name"], clue["prompt"])
        if result:
            successful += 1
    
    print("\n" + "="*60)
    print(f"✅ Generated {successful}/{len(clues_to_generate)} images")
    print("="*60)
    
    return successful == len(clues_to_generate)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
