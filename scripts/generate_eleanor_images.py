#!/usr/bin/env python3
"""
Generate photographs of Eleanor Sullivan at different ages
Based on artifact clue descriptions
"""

import os
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai

# Eleanor photos prompts based on artifact descriptions
ELEANOR_PROMPTS = {
    'photograph_eleanor_baby': """Create a vintage black and white studio photograph from the 1920s of a baby Eleanor Sullivan in formal christening wear.
        The infant is in an expensive white christening gown with delicate lace details.
        Professional studio lighting, formal pose on elegant background.
        High-quality portrait photography of an infant from a wealthy family.
        Soft focus, vintage film stock appearance. Black and white.
        The photograph should look professionally commissioned and formal.""",
    
    'photograph_eleanor_child': """Create a vintage black and white photograph from the late 1920s/early 1930s of young Eleanor Sullivan as a small child playing in a garden.
        She wears a simple white dress with a bow.
        Garden setting visible in background - 1920s Long Beach residential property.
        Natural outdoor lighting, candid but posed moment.
        Shows a young girl with innocent, happy expression.
        Vintage film quality, black and white portrait photograph.""",
    
    'photograph_eleanor_adolescent': """Create a vintage black and white photograph from the mid-1930s of Eleanor Sullivan at age 10 standing in front of a house.
        She wears period-appropriate clothing for a young girl in the 1930s.
        Standing pose in front of a 1920s-1930s Long Beach residential house.
        More mature expression than childhood photos, beginning to show awareness.
        Formal portrait style but softer than infant christening photo.
        Black and white, vintage film quality.""",
}

def generate_eleanor_image(photo_id: str, description: str, prompt: str, output_filename: str = None):
    """
    Generate an Eleanor photograph image
    
    Args:
        photo_id: ID of the photograph
        description: Human-readable description
        prompt: Detailed prompt for image generation
        output_filename: Optional custom output filename
    
    Returns:
        Path to saved image or None if failed
    """
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: GEMINI_API_KEY not set in .env file")
        return None
    
    if output_filename is None:
        output_filename = f'{photo_id}.png'
    
    output_path = Path('clue_images') / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"📸 {description:<50}", end=" ")
        sys.stdout.flush()
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        response = model.generate_content([prompt])
        
        # Extract image data
        if hasattr(response, 'parts'):
            for part in response.parts:
                if hasattr(part, 'inline_data'):
                    inline_data = part.inline_data
                    if inline_data and hasattr(inline_data, 'data'):
                        img_data = inline_data.data
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_data)
                        
                        print(f"✅ ({len(img_data)/(1024**2):.1f}MB)")
                        return output_path
        
        print("❌ No image in response")
        return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Generate Eleanor Sullivan photographs"""
    
    print("="*70)
    print("📷 Eleanor Sullivan Photograph Generator")
    print("   Vintage portraits from artifact clues")
    print("="*70)
    
    photos = [
        ('photograph_eleanor_baby', 'Baby Eleanor in Christening Gown (1925)', ELEANOR_PROMPTS['photograph_eleanor_baby']),
        ('photograph_eleanor_child', 'Young Eleanor in Garden (1928-1930)', ELEANOR_PROMPTS['photograph_eleanor_child']),
        ('photograph_eleanor_adolescent', 'Eleanor at Age 10 (1935)', ELEANOR_PROMPTS['photograph_eleanor_adolescent']),
    ]
    
    print(f"\nGenerating {len(photos)} Eleanor Sullivan photographs...\n")
    
    successful = 0
    failed = 0
    
    for i, (photo_id, description, prompt) in enumerate(photos, 1):
        result = generate_eleanor_image(photo_id, description, prompt)
        if result:
            successful += 1
        else:
            failed += 1
        
        # Rate limiting: wait between requests
        if i < len(photos):
            time.sleep(2)  # 2 second delay between requests
    
    print("\n" + "="*70)
    print(f"✅ Complete! Generated {successful}/{len(photos)} Eleanor photographs")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    print(f"📁 Location: clue_images/")
    print("="*70)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
