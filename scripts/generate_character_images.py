#!/usr/bin/env python3
"""
Generate character portrait images using Gemini 2.5 Flash Image
Creates Mansion of Madness style character portraits with specific genders
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

# Character portrait prompts - Mansion of Madness style with specific genders and descriptions
CHARACTER_PROMPTS = {
    'heiress': """Create a Mansion of Madness style portrait of an elegant upper-class woman (the Heiress).
        She is dripping in fine jewelry - diamonds, pearls, emeralds - and wearing luxurious clothing.
        Confident, aristocratic bearing with a hint of mystery. 
        Dark, atmospheric setting with hints of wealth and secrets.
        Moody lighting with shadows, slightly unsettling elegant atmosphere.
        Oil painting style with dark sepia and jewel tones. Vintage luxury aesthetic.""",
    
    'doctor': """Create a Mansion of Madness style portrait of a sophisticated female physician/doctor.
        Professional, intelligent woman with piercing eyes and knowing expression.
        Contemporary but vintage-looking attire, perhaps medical coat or professional dress.
        Dark atmospheric setting, perhaps with medical or scientific elements in background.
        Moody, mysterious lighting. Oil painting style.
        Dark academia aesthetic - intellectual but haunting.""",
    
    'baker': """Create a Mansion of Madness style portrait of a mature male baker (Baker/Eleanor's counterpart).
        Strong, capable man with flour dust on his hands or apron.
        Contemporary but vintage-looking attire, working class dignity.
        Dark, atmospheric bakery or kitchen setting with ovens in shadows.
        Moody lighting that emphasizes character and determination.
        Oil painting style with warm dark tones. Working class mystery.""",
    
    'explorer': """Create a Mansion of Madness style portrait of a rugged male explorer (Indiana Jones style).
        Adventurous man in explorer's gear - leather jacket, wide-brimmed hat, weathered face.
        Scarred, experienced, dangerous but charismatic.
        Dark atmospheric setting with hints of ancient artifacts and adventure.
        Dramatic moody lighting with shadows emphasizing adventure and danger.
        Oil painting style. Swashbuckling but dark and mysterious.""",
    
    'psychic': """Create a Mansion of Madness style portrait of a mysterious female psychic/medium.
        Woman with piercing, knowing gaze, perhaps with third eye symbolism subtle in background.
        Contemporary but vintage-looking flowing attire, perhaps with mystical shawl.
        Dark spiritualist setting with candles, shadows, mystical symbols.
        Eerie, atmospheric lighting. Oil painting style.
        Occult mysticism - beautiful but deeply unsettling.""",
    
    'mortician': """Create a Mansion of Madness style portrait of a severe, elegant female mortician.
        Professional woman in dark contemporary attire, composed and mysterious.
        Intelligent, capable expression with hint of darkness.
        Dark funeral parlor setting with elegant drapes and shadows.
        Moody professional lighting. Oil painting style.
        Death profession aesthetic - dignified but ominous.""",
    
    'professor': """Create a Mansion of Madness style portrait of a scholarly male professor/academic.
        Intelligent man in contemporary but vintage-looking academic attire - vest, glasses perhaps.
        Deep, thoughtful expression with hint of dangerous knowledge.
        Dark university study or library setting with ancient tomes and curiosities.
        Moody academic lighting with shadows. Oil painting style.
        Dark academia - intellectual mystery and hidden knowledge.""",
    
    'influencer': """Create a Mansion of Madness style portrait of a charismatic male influencer/social figure.
        Well-dressed contemporary man with magnetic but slightly unsettling charm.
        Beautiful but with hint of danger in his expression.
        Dark social venue or office setting with subtle signs of influence and power.
        Moody dramatic lighting. Oil painting style.
        Contemporary style - charming but mysterious.""",
    
    'fiduciary': """Create a Mansion of Madness style portrait of a shrewd female fiduciary/estate manager.
        Professional woman in contemporary but vintage-looking business attire.
        Sharp, calculating eyes, intelligent and formidable presence.
        Dark office or study with ledgers, safes, documents in shadows.
        Moody professional lighting. Oil painting style.
        Financial power - elegant but ruthless.""",
    
    'dressmaker': """Create a Mansion of Madness style portrait of a refined female dressmaker/tailor.
        Artistic woman in contemporary but vintage-looking attire, sensitive but mysterious.
        Beautiful with hint of hidden sorrow or secrets.
        Dark tailoring shop with elegant fabrics, dress forms in shadows.
        Moody creative lighting. Oil painting style.
        Artistic mystery - beautiful but troubled.""",
    
    'artcollector': """Create a Mansion of Madness style portrait of a sophisticated male art collector.
        Distinguished man in contemporary but vintage-looking refined attire.
        Cultured, discerning expression with hint of obsession.
        Dark gallery or study with valuable paintings and sculptures in shadows.
        Moody gallery-quality lighting. Oil painting style.
        Refined aesthetic - collector of dark mysteries.""",
    
    'clockmaker': """Create a Mansion of Madness style portrait of a precise male clockmaker.
        Meticulous man in contemporary but vintage-looking craftsman attire.
        Focused, methodical expression with obsessive intensity.
        Dark workshop with intricate timepieces, gears, and mechanisms in shadows.
        Moody workshop lighting. Oil painting style.
        Precision craft - obsessive and mysterious.""",
    
    'ghost_alice': """Create a mystical 1920s portrait of Alice Whitmore's ethereal spirit/ghost.
        Young woman with otherworldly, haunting beauty and mystical presence.
        Ethereal, semi-transparent appearance with supernatural glow.
        Supernatural 1920s spiritualist setting with candlelight and mystical elements.
        Ghostly ethereal lighting with pale luminescence. Oil painting style.
        Tragic supernatural beauty - peaceful but haunting.""",
    
    'ghost_cordelia': """Create a tragic 1920s portrait of Cordelia Montrose's haunting spirit/ghost.
        Beautiful young woman in 1920s wedding dress, ethereal and melancholic.
        Ethereal, semi-transparent with supernatural glow around her.
        Supernatural 1920s setting with hints of her wedding and fate.
        Haunting ethereal lighting with pale luminescence. Oil painting style.
        Tragic beauty - forever young, forever sad.""",
    
    'ghost_sebastian': """Create a mysterious 1920s portrait of Sebastian Crane's spirit/ghost.
        Man in 1920s alchemist attire, ethereal but intense presence.
        Ghostly, semi-transparent with supernatural glow.
        Supernatural 1920s setting with alchemical symbols, books, mysterious elements.
        Eerie ethereal lighting with pale mystical glow. Oil painting style.
        Mysterious alchemist spirit - knowledge beyond death.""",
}

def generate_character_image(character_name: str, prompt: str, output_filename: str = None):
    """
    Generate a character portrait image
    
    Args:
        character_name: Name of the character
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
        output_filename = f'{character_name}.png'
    
    output_path = Path('assets/characters') / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"🎭 {character_name:<20}", end=" ")
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
    """Generate character portrait images"""
    
    print("="*70)
    print("🎭 Character Portrait Image Generator")
    print("   Style: Mansion of Madness")
    print("="*70)
    
    characters = sorted(CHARACTER_PROMPTS.keys())
    print(f"\nRegenerating {len(characters)} character portraits...\n")
    
    successful = 0
    failed = 0
    
    for i, character in enumerate(characters, 1):
        prompt = CHARACTER_PROMPTS[character]
        result = generate_character_image(character, prompt)
        if result:
            successful += 1
        else:
            failed += 1
        
        # Rate limiting: wait between requests
        if i < len(characters):
            time.sleep(2)  # 2 second delay between requests
    
    print("\n" + "="*70)
    print(f"✅ Complete! Generated {successful}/{len(characters)} character images")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    print(f"📁 Location: assets/characters/")
    print("="*70)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
