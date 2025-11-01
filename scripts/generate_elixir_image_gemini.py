#!/usr/bin/env python3
"""
Generate an alchemical-styled image of Sebastian's Elixir formula using Gemini API
Then create QR code and PDF with both
"""

import os
import json
import qrcode
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
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images/clue_images_documents')
QR_CODES_DIR = os.path.join(PROJECT_DIR, 'qr_codes')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(QR_CODES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_elixir_image_with_gemini():
    """Generate an alchemical-styled elixir formula image using Gemini"""
    img_path = os.path.join(IMAGES_DIR, 'sebastian_elixir_formula_alchemical.png')
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
        return None
    
    genai.configure(api_key=api_key)
    
    # Detailed prompt for the alchemical elixir image
    prompt = """Create a detailed alchemical illustration of Sebastian Crane's "Elixir of Eternal Love" formula from 1920s.

The image should show:
- An ornate, aged parchment background in cream and gold tones
- Sacred geometry and alchemical symbols (circled cross, heart symbol, Venus symbol, constellations)
- An elegant glass bottle at the center containing a luminous, mystical liquid in emerald green
- Around the bottle, arranged in circular orbits like planetary systems:
  * Botanical ingredients (damiana leaves, valerian root, rose otto droplet, ginseng root with forked shape)
  * Pharmaceutical elements (crystal formations for potassium bromide, calcium lactate, iron citrate)
  * Base and flavoring elements (honey droplets, cherry red, vanilla swirls)
- Decorative borders with Art Deco and alchemical designs
- Handwritten-style labels for each ingredient with their quantities (3 parts, 2 parts, 1 drop, 10 grains, etc.)
- At the top: "ELIXIR OF ETERNAL LOVE" in ornate script
- Celestial elements: Jupiter and Venus symbols, constellation imagery
- At the bottom: "Prepared for Jupiter-Venus Conjunction | September 4, 1925, 6:14 AM"
- Overall aesthetic: 1920s occult, romantic alchemy, scientific mysticism, like something from a master alchemist's private journal
- Color palette: Cream, gold, deep greens, burgundy, with mystical glowing effects
- High detail, hand-drawn quality, mysterious and beautiful"""

    try:
        print("🎨 Generating alchemical elixir image with Gemini...")
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        response = model.generate_content([prompt])
        
        # The image is usually in the last part with actual data
        if response and response.parts:
            for part in reversed(response.parts):
                if hasattr(part, 'inline_data') and part.inline_data.data and len(part.inline_data.data) > 0:
                    image_data = part.inline_data.data
                    # Save the image
                    with open(img_path, 'wb') as f:
                        f.write(image_data)
                    print(f"✅ Image created: {img_path}")
                    return img_path
        
        print("❌ No image data found in Gemini response")
        return None
            
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_qr_code():
    """Generate QR code for the elixir formula document"""
    qr_path = os.path.join(QR_CODES_DIR, 'sebastian_elixir_formula.png')
    
    # URL to the document
    url = "https://filatova-elena.github.io/murder_mystery/clue/documents/sebastian_elixir_formula.html"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(qr_path)
    print(f"✅ QR code created: {qr_path}")
    return qr_path

def create_pdf(elixir_img_path, qr_code_path):
    """Create PDF with elixir image and QR code in bottom right"""
    pdf_path = os.path.join(OUTPUT_DIR, 'sebastian_elixir_formula.pdf')
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 0.5 * inch
    
    # Add the elixir formula image
    img_display_width = 6 * inch
    img_display_height = 7.5 * inch
    x = (width - img_display_width) / 2
    y = height - 1 * inch - img_display_height
    
    if os.path.exists(elixir_img_path):
        c.drawImage(elixir_img_path, x, y, width=img_display_width, height=img_display_height)
        print(f"✅ Image added to PDF")
    
    # Add QR code in bottom right (2x2 inches)
    qr_size = 2 * inch
    qr_x = width - qr_size - margin
    qr_y = margin
    
    if os.path.exists(qr_code_path):
        c.drawImage(qr_code_path, qr_x, qr_y, width=qr_size, height=qr_size)
        print(f"✅ QR code added to PDF")
    
    # Add footer text
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor('#666666'))
    c.drawCentredString(width/2, 0.25*inch, "Scan to view full formula document")
    
    c.save()
    print(f"✅ PDF created: {pdf_path}")

# Main execution
if __name__ == '__main__':
    print("🔬 Generating Sebastian's Alchemical Elixir Formula...")
    print("=" * 60)
    
    # Create the alchemical elixir image using Gemini
    elixir_img = generate_elixir_image_with_gemini()
    
    if elixir_img:
        # Create QR code
        qr_code = create_qr_code()
        
        # Create PDF with both
        create_pdf(elixir_img, qr_code)
        
        print("=" * 60)
        print("✨ All files created successfully!")
    else:
        print("❌ Failed to generate image. Please check your Gemini API key.")
