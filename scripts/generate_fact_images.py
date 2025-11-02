#!/usr/bin/env python3
"""
Generate images for facts/rumors using Gemini 2.5 Flash Image
Creates evocative 1920s-themed visuals for each fact
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
    """Load facts from rumors.json"""
    with open('data/rumors.json', 'r') as f:
        data = json.load(f)
    return data.get('rumors', [])

def create_image_prompt(fact_text: str, fact_id: int) -> str:
    """Create a detailed image prompt based on fact text"""
    
    prompts = {
        1: """Create a moody 1920s harbor scene showing mysterious alchemical operations. 
            Show warehouses at the docks with subtle signs of secret activities, barrels, crates, and shadowy figures.
            Include period-accurate ships and harbor workers. Use dim lighting, sepia and grayscale tones.
            Add mystical elements like hanging bottles, glass vials, and chemical apparatus visible through warehouse windows.
            Make it look like a vintage photograph with film grain from the 1920s era.""",
        
        2: """Create a dramatic 1920s scene showing an elegant woman (Cordelia) in a beautiful period dress, 
            appearing troubled or contemplative. Set in an opulent mansion interior with art deco details.
            Show her gazing out a window or in a dimly lit room suggesting secrecy and mystery.
            Use soft lighting, sepia tones, and the quality of a vintage portrait photograph.
            The atmosphere should convey mystery and hidden circumstances.""",
        
        3: """Create a dramatic 1920s photograph of a bakery fire. Show the Sullivan Bakery storefront engulfed in flames,
            with smoke billowing into the night sky. Include period-accurate fire trucks and firefighters battling the blaze.
            Show concerned onlookers and the chaos of an urban fire. Use orange and red flames contrasting with dark sepia tones.
            The composition should suggest deliberate arson, not an accident.""",
        
        4: """Create a mystical 1920s portrait of Alice Whitmore, a young woman with an ethereal, otherworldly quality.
            Show her with a distant, knowing gaze, perhaps surrounded by candlelight or mystical symbols.
            Her appearance should suggest supernatural abilities - perhaps see visions, crystals, tarot cards nearby.
            Use sepia tones with mysterious lighting, shadows, and a dreamy atmosphere.
            Make it look like a vintage spiritualist photograph.""",
        
        5: """Create an imposing 1920s photograph of a shipping magnate's office overlooking the harbor.
            Show Frankie Romano (distinguished man) at a grand mahogany desk surrounded by shipping maps, manifests, and ledgers.
            Large windows behind showing the bustling port and multiple ships. Include period furnishings showing wealth and power.
            Use sepia tones and formal studio lighting. The composition should convey absolute control and authority.""",
        
        6: """Create a poignant 1920s photograph showing a young woman and child together, suggesting hidden family bonds.
            Set in an elegant but somewhat hidden location - perhaps a mansion's private room or garden.
            The composition should evoke secrecy, concealment, and family scandal. Use soft lighting and sepia tones.
            Include period-accurate clothing and furnishings that suggest Montrose family wealth.
            The emotional tone should suggest a hidden tragedy.""",
        
        7: """Create a romantic but melancholic 1920s scene showing a young tailor (Elias Monroe) 
            working on an elaborate wedding dress. Show him with a distant, longing expression.
            The dress is exquisite and clearly meant for his lost love (Cordelia).
            Set in an upscale tailor shop with fabrics, patterns, and sewing materials.
            Use sepia tones and poignant lighting. The atmosphere should convey heartbreak and unrequited love.""",
    }
    
    if fact_id in prompts:
        return prompts[fact_id]
    
    # Default prompt for unknown facts
    return f"""Create a moody 1920s-style photograph illustrating this mystery: "{fact_text[:60]}..."
    Use sepia and grayscale tones, vintage film grain, and atmospheric lighting.
    Include period-appropriate elements and settings from the 1920s era.
    The composition should be evocative and mysterious."""

def generate_fact_image(fact_id: int, fact_text: str, output_filename: str = None):
    """
    Generate an image for a fact
    
    Args:
        fact_id: ID of the fact
        fact_text: The fact text
        output_filename: Optional custom output filename
    
    Returns:
        Path to saved image or None if failed
    """
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: GEMINI_API_KEY not set in .env file")
        return None
    
    if output_filename is None:
        output_filename = f'fact_{fact_id:02d}.png'
    
    output_path = Path('fact_images') / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"📸 Fact #{fact_id}: {fact_text[:50]}...", end=" ")
        sys.stdout.flush()
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        prompt = create_image_prompt(fact_text, fact_id)
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
    print("🎨 Fact Image Generator - Murder Mystery")
    print("="*70)
    
    facts = load_facts()
    print(f"\nFound {len(facts)} facts to generate images for")
    print("(Generating images with detailed 1920s themes)\n")
    
    successful = 0
    failed = 0
    
    for i, fact in enumerate(facts, 1):
        result = generate_fact_image(fact['id'], fact['text'])
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
    print(f"📁 Location: fact_images/")
    print("="*70)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
