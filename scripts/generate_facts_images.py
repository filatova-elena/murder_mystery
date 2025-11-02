#!/usr/bin/env python3
"""
Generate images for facts using Gemini 2.5 Flash Image
Creates images based on fact content and themes
"""

import os
import sys
import json
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai

def load_facts():
    """Load facts from facts.json"""
    with open('data/facts.json', 'r') as f:
        data = json.load(f)
    return data.get('facts', [])

def create_image_prompt(fact_text: str, character: str) -> str:
    """Create a detailed image prompt based on fact text and character"""
    
    # Character-specific prompts to create thematic images
    character_themes = {
        'heiress': 'Create a 1920s photograph of high society. Include elegant furnishings, fine art, ornate decorations, and hints of wealth and status. Use sepia and grayscale tones with soft lighting.',
        'doctor': 'Create a 1920s medical office or study. Include period medical instruments, leather furniture, bookshelves with medical texts, and an atmosphere of professional expertise. Use sepia tones.',
        'baker': 'Create a 1920s bakery interior. Show ovens, bread displays, flour-dusted surfaces, and the warm, inviting atmosphere of a working bakery. Use warm sepia and golden tones.',
        'explorer': 'Create a 1920s shipping office or harbor warehouse. Include shipping maps, maritime instruments, crates, and evidence of global trade. Use sepia tones.',
        'psychic medium': 'Create a mystical 1920s spiritualist parlor. Include candlelight, crystals, tarot cards, mysterious symbols, and an otherworldly atmosphere. Use dim sepia and purple tones.',
        'mortician': 'Create a 1920s funeral parlor. Include period furnishings, funeral arrangements, and the solemn atmosphere of a mortuary. Use formal grayscale and muted tones.',
        'professor': 'Create a 1920s university study or laboratory. Include books, specimens, scientific instruments, and an academic atmosphere. Use sepia tones with focused lighting.',
        'influencer': 'Create a 1920s social scene or newspaper office. Include crowds, party atmosphere, or printing equipment. Use vibrant sepia and grayscale tones.',
        'fiduciary': 'Create a 1920s law office or bank. Include mahogany desks, safes, legal documents, and an atmosphere of trust and authority. Use formal grayscale tones.',
        'dressmaker': 'Create a 1920s tailoring shop. Include dress forms, fine fabrics, sewing materials, and elegant clothing. Use warm sepia tones.',
        'art collector': 'Create a 1920s gallery or private collection room. Include valuable paintings, sculptures, and fine art. Use gallery lighting and rich sepia tones.',
        'clockmaker': 'Create a 1920s clockmaker shop. Include intricate timepieces, gears, precision instruments, and watches. Use warm sepia tones.',
    }
    
    # Get theme for character, default to generic 1920s
    theme = character_themes.get(character.lower(), 'Create an evocative 1920s photograph. Use sepia and grayscale tones with period-appropriate details.')
    
    return f"""Create a vintage 1920s photograph related to: "{fact_text[:80]}..."
    
    {theme}
    
    The photograph should look authentic with film grain, natural lighting appropriate to the setting, and historically accurate details. Make it suitable for a period mystery game."""

def generate_fact_image(fact_id: str, fact_text: str, character: str, output_filename: str = None):
    """
    Generate an image for a fact
    
    Args:
        fact_id: ID of the fact
        fact_text: The fact text
        character: Character who knows this fact
        output_filename: Optional custom output filename
    
    Returns:
        Path to saved image or None if failed
    """
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: GEMINI_API_KEY not set in .env file")
        return None
    
    if output_filename is None:
        # Use fact_id as filename
        output_filename = f'{fact_id}.png'
    
    output_path = Path('fact_images_character') / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"📸 {fact_id}: {fact_text[:50]:<50}", end=" ")
        sys.stdout.flush()
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        prompt = create_image_prompt(fact_text, character)
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
    """Generate images for all facts"""
    
    print("="*70)
    print("🎨 Facts Image Generator - Murder Mystery")
    print("="*70)
    
    facts = load_facts()
    print(f"\nFound {len(facts)} facts to generate images for")
    print("(Generating character-specific 1920s themed images)\n")
    
    successful = 0
    failed = 0
    
    for i, fact in enumerate(facts, 1):
        result = generate_fact_image(fact['id'], fact['text'], fact['character'])
        if result:
            successful += 1
        else:
            failed += 1
        
        # Rate limiting: wait between requests
        if i < len(facts):
            time.sleep(2)  # 2 second delay between requests
    
    print("\n" + "="*70)
    print(f"✅ Complete! Generated {successful}/{len(facts)} images")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    print(f"📁 Location: fact_images_character/")
    print("="*70)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
