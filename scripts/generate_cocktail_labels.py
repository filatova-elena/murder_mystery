#!/usr/bin/env python3
"""
Generate cocktail labels for Eternal Love Elixir (alcoholic and non-alcoholic)
in Sebastian's alchemical elixir style
"""

import os
from pathlib import Path
from PIL import Image

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images/cocktail_labels')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_cocktail_labels():
    """Generate two cocktail label images using Gemini"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
        return None, None
    
    genai.configure(api_key=api_key)
    
    labels = [
        {
            'id': 'eternal_love_elixir_alcoholic',
            'filename': 'eternal_love_elixir_alcoholic.png',
            'prompt': """Create an ornate vintage cocktail bottle label for "Eternal Love Elixir" (contains alcohol).

The label should have:
- Ornate parchment background in cream, gold, and deep burgundy tones
- Elegant script font at the top: "ETERNAL LOVE ELIXIR"
- Alchemical symbols and romantic motifs (hearts, Venus symbols, roses, celestial elements)
- A subtitle: "An Exquisite Blend of Botanical Essences & Spirits"
- Description: "Blended with passion for lovers seeking timeless connection"
- Vintage 1920s apothecary/alchemical aesthetic
- Sacred geometry and decorative borders with Art Deco elements
- A small illustration of an elegant glass bottle or hearts
- Ornate corner designs with flourishes
- Aged, mystical appearance with gold accents
- Include text: "Distilled with Intent | For Eternal Love"
- Professional vintage label design, high detail"""
        },
        {
            'id': 'eternal_love_elixir_nonalcoholic',
            'filename': 'eternal_love_elixir_nonalcoholic.png',
            'prompt': """Create an ornate vintage cocktail bottle label for "Eternal Love Elixir" (non-alcoholic).

The label should have:
- Ornate parchment background in soft rose, cream, and gold tones
- Elegant script font at the top: "ETERNAL LOVE ELIXIR"
- Subtitle: "BOTANICAL BLEND" (non-alcoholic version)
- Alchemical symbols and romantic motifs (hearts, Venus symbols, roses, celestial elements)
- Description: "A Sophisticated Non-Alcoholic Blend of Premium Botanicals"
- Vintage 1920s apothecary aesthetic with lighter, more elegant color palette
- Sacred geometry and decorative borders with Art Deco elements
- A small illustration of an elegant glass bottle or hearts
- Ornate corner designs with flourishes
- Mystical, romantic appearance with rose gold accents
- Include text: "Crafted with Care | For All Who Seek Love"
- Professional vintage label design, high detail"""
        }
    ]
    
    generated_paths = []
    
    for label in labels:
        img_path = os.path.join(IMAGES_DIR, label['filename'])
        
        try:
            print(f"🎨 Generating {label['id']}...")
            model = genai.GenerativeModel('gemini-2.5-flash-image')
            response = model.generate_content([label['prompt']])
            
            if response and response.parts:
                for part in reversed(response.parts):
                    if hasattr(part, 'inline_data') and part.inline_data.data and len(part.inline_data.data) > 0:
                        image_data = part.inline_data.data
                        with open(img_path, 'wb') as f:
                            f.write(image_data)
                        print(f"✅ Label created: {img_path}")
                        generated_paths.append(img_path)
                        break
            else:
                print(f"❌ No image data found for {label['id']}")
                
        except Exception as e:
            print(f"❌ Error generating {label['id']}: {e}")
            import traceback
            traceback.print_exc()
    
    return generated_paths

def create_labels_pdf(label_paths):
    """Create PDF with both cocktail labels"""
    
    if not label_paths or len(label_paths) == 0:
        print("❌ No label images to process")
        return False
    
    pdf_path = os.path.join(OUTPUT_DIR, 'eternal_love_elixir_labels.pdf')
    
    try:
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        margin = 0.5 * inch
        
        # Position labels on the page
        label_width = 3.5 * inch
        label_height = 5 * inch
        
        # Calculate centered positions
        x_center = (width - label_width) / 2
        
        # First label at top
        y1 = height - margin - label_height
        
        # Second label below
        y2 = y1 - label_height - 0.5 * inch
        
        # Add labels to PDF
        for idx, label_path in enumerate(label_paths[:2]):
            try:
                if Path(label_path).exists():
                    # Open and check image dimensions
                    img = Image.open(label_path)
                    
                    # Calculate position
                    if idx == 0:
                        y_pos = y1
                        label_name = "Alcoholic"
                    else:
                        y_pos = y2
                        label_name = "Non-Alcoholic"
                    
                    # Draw the label image
                    c.drawImage(label_path, x_center, y_pos, width=label_width, height=label_height)
                    
                    # Add label text below image
                    c.setFont("Helvetica", 10)
                    c.setFillColor(HexColor('#8B7355'))
                    text_y = y_pos - 0.3 * inch
                    c.drawCentredString(width/2, text_y, f"Eternal Love Elixir - {label_name}")
                    
                    print(f"✅ Label {idx + 1} added to PDF")
            except Exception as e:
                print(f"⚠️ Could not add label {idx + 1}: {e}")
        
        c.save()
        print(f"✅ PDF created: {pdf_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🍸 Generating Eternal Love Elixir Cocktail Labels...")
    print("=" * 60)
    
    # Generate label images
    label_paths = generate_cocktail_labels()
    
    if label_paths and len(label_paths) > 0:
        print("\n" + "=" * 60)
        print("📄 Creating PDF document...")
        create_labels_pdf(label_paths)
        
        print("\n" + "=" * 60)
        print("✨ Complete!")
        print(f"   Labels created: {len(label_paths)}")
        print(f"   PDF: to_print/eternal_love_elixir_labels.pdf")
        print("=" * 60)
    else:
        print("❌ Failed to generate labels")



