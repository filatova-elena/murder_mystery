#!/usr/bin/env python3
import json
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DOCUMENT_FILE = os.path.join(PROJECT_DIR, 'data/documents/sebastian_elixir_formula.json')
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images/clue_images_documents')
QR_CODES_DIR = os.path.join(PROJECT_DIR, 'qr_codes')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(QR_CODES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the elixir formula document
with open(DOCUMENT_FILE, 'r') as f:
    data = json.load(f)

def create_elixir_image():
    """Generate an image of Sebastian's Elixir formula"""
    img_path = os.path.join(IMAGES_DIR, 'sebastian_elixir_formula.png')
    
    # Create image with elegant background
    img_width, img_height = 1000, 1200
    img = Image.new('RGB', (img_width, img_height), color=(30, 25, 20))  # Dark burgundy-brown
    draw = ImageDraw.Draw(img)
    
    # Try to use nice fonts
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        title_font = subtitle_font = text_font = small_font = ImageFont.load_default()
    
    # Draw decorative border
    border_color = (218, 165, 32)  # Gold
    draw.rectangle([40, 40, img_width-40, img_height-40], outline=border_color, width=4)
    draw.rectangle([50, 50, img_width-50, img_height-50], outline=border_color, width=1)
    
    # Title
    title = "ELIXIR OF ETERNAL LOVE"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((img_width - title_width) // 2, 100), title, fill=border_color, font=title_font)
    
    # Subtitle
    subtitle = "Sebastian Crane's Complete Formula"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((img_width - subtitle_width) // 2, 180), subtitle, fill=(245, 245, 220), font=subtitle_font)
    
    # Decorative line
    draw.line([100, 230, img_width-100, 230], fill=border_color, width=2)
    
    # Ingredients section
    y_pos = 280
    line_height = 35
    
    ingredients = [
        ("BOTANICAL INGREDIENTS", None),
        ("• Damiana - 3 parts", "Desire, heat, awakening"),
        ("• Valerian Root - 2 parts", "Calm, trust, grounding"),
        ("• Rose Otto - 1 drop", "Venus, transcendence"),
        ("• Ginseng Root - pinch", "Binding agent, eternity"),
        ("", ""),
        ("PHARMACEUTICAL INGREDIENTS", None),
        ("• Potassium Bromide - 10 grains", "Mild sedative"),
        ("• Calcium Lactate - 5 grains", "Strength, fortification"),
        ("• Iron Citrate - 3 grains", "Vitality, blood tonic"),
        ("", ""),
        ("BASE & FLAVORINGS", None),
        ("• Grain Alcohol - 8 oz", "Base and preservative"),
        ("• Vanilla, Cherry Syrup, Honey", "Flavor and sweetness"),
    ]
    
    for ingredient, purpose in ingredients:
        if ingredient == "":
            y_pos += 15
        elif purpose is None:
            # Section header
            draw.text((100, y_pos), ingredient, fill=border_color, font=subtitle_font)
        else:
            # Ingredient line
            draw.text((120, y_pos), ingredient, fill=(245, 245, 220), font=text_font)
            draw.text((550, y_pos), purpose, fill=(200, 200, 170), font=small_font)
        y_pos += line_height
    
    # Footer inscription
    y_pos += 40
    draw.line([100, y_pos, img_width-100, y_pos], fill=border_color, width=1)
    y_pos += 30
    
    footer = "\"A potion as delicate as the Elixir of Eternal Love\""
    footer_bbox = draw.textbbox((0, 0), footer, font=small_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((img_width - footer_width) // 2, y_pos), footer, fill=(200, 170, 120), font=small_font)
    
    y_pos += 40
    footer2 = "deserves a container worthy of it.  - Sebastian Crane"
    footer2_bbox = draw.textbbox((0, 0), footer2, font=small_font)
    footer2_width = footer2_bbox[2] - footer2_bbox[0]
    draw.text(((img_width - footer2_width) // 2, y_pos), footer2, fill=(200, 170, 120), font=small_font)
    
    # Save image
    img.save(img_path)
    print(f"Created image: {img_path}")
    return img_path

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
    print(f"Created QR code: {qr_path}")
    return qr_path

def create_pdf(elixir_img_path, qr_code_path):
    """Create PDF with elixir image and QR code in bottom right"""
    pdf_path = os.path.join(OUTPUT_DIR, 'sebastian_elixir_formula.pdf')
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 0.5 * inch
    
    # Add the elixir formula image
    # Image should fill most of the page, leaving space for QR code in bottom right
    img_display_width = 6 * inch
    img_display_height = 7.5 * inch
    x = (width - img_display_width) / 2
    y = height - 1 * inch - img_display_height
    
    if os.path.exists(elixir_img_path):
        c.drawImage(elixir_img_path, x, y, width=img_display_width, height=img_display_height)
    
    # Add QR code in bottom right (2x2 inches)
    qr_size = 2 * inch
    qr_x = width - qr_size - margin
    qr_y = margin
    
    if os.path.exists(qr_code_path):
        c.drawImage(qr_code_path, qr_x, qr_y, width=qr_size, height=qr_size)
    
    # Add footer text
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor('#666666'))
    c.drawCentredString(width/2, 0.25*inch, "Scan to view full formula document")
    
    c.save()
    print(f"Created PDF: {pdf_path}")

# Main execution
if __name__ == '__main__':
    print("Generating Sebastian's Elixir formula image, QR code, and PDF...")
    
    # Create the elixir formula image
    elixir_img = create_elixir_image()
    
    # Create QR code
    qr_code = create_qr_code()
    
    # Create PDF with both
    create_pdf(elixir_img, qr_code)
    
    print("All files created successfully!")
