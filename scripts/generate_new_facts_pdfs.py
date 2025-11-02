#!/usr/bin/env python3
import json
import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import textwrap

# Paths
FACTS_FILE = '../data/facts.json'
OUTPUT_DIR = '../to_print'
IMAGES_DIR = '../images/clue_images_facts'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Load facts
with open(FACTS_FILE, 'r') as f:
    data = json.load(f)

facts = data['facts']

# Get the two new facts
heiress_fact = next((f for f in facts if f['id'] == 'heiress_fact_5'), None)
fiduciary_fact = next((f for f in facts if f['id'] == 'fiduciary_fact_5'), None)

def create_fact_card_pdf():
    """Create PDF with the two new facts"""
    pdf_path = os.path.join(OUTPUT_DIR, 'new_facts.pdf')
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 0.5 * inch
    
    # Title
    c.setFont("Garamond", 28, leading=32)
    c.drawCentredString(width/2, height - 0.75*inch, "SECRETS REVEALED")
    
    # Draw line
    c.setStrokeColor(HexColor('#DAA520'))
    c.setLineWidth(2)
    c.line(margin, height - 1*inch, width - margin, height - 1*inch)
    
    # Fact 1 - Heiress
    y_pos = height - 1.5*inch
    c.setFont("Garamond", 16, leading=20)
    c.setFillColor(HexColor('#2C1810'))
    
    c.drawString(margin, y_pos, "The Heiress Knows:")
    y_pos -= 0.3*inch
    
    c.setFont("Garamond", 12, leading=18)
    wrapped_text = textwrap.wrap(heiress_fact['text'], width=80)
    for line in wrapped_text[:10]:  # Limit to prevent overflow
        c.drawString(margin + 0.2*inch, y_pos, line)
        y_pos -= 0.2*inch
    
    y_pos -= 0.3*inch
    c.setLineWidth(1)
    c.line(margin, y_pos, width - margin, y_pos)
    
    # Fact 2 - Fiduciary
    y_pos -= 0.3*inch
    c.setFont("Garamond", 16, leading=20)
    c.drawString(margin, y_pos, "The Fiduciary's Secret:")
    y_pos -= 0.3*inch
    
    c.setFont("Garamond", 12, leading=18)
    wrapped_text = textwrap.wrap(fiduciary_fact['text'], width=80)
    for line in wrapped_text[:10]:
        c.drawString(margin + 0.2*inch, y_pos, line)
        y_pos -= 0.2*inch
    
    c.save()
    print(f"Created: {pdf_path}")

def create_rose_bread_recipe_image():
    """Generate an image of a handwritten rose bread recipe"""
    img_path = os.path.join(IMAGES_DIR, 'rose_bread_recipe_handwritten.png')
    
    # Create image
    img_width, img_height = 800, 1000
    img = Image.new('RGB', (img_width, img_height), color=(245, 240, 230))  # Cream background
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        signature_font = ImageFont.truetype("/System/Library/Fonts/Brush Script MT.ttf", 40)
    except:
        title_font = text_font = signature_font = ImageFont.load_default()
    
    # Draw decorative border
    border_color = (139, 69, 19)  # Saddle brown
    draw.rectangle([30, 30, img_width-30, img_height-30], outline=border_color, width=3)
    draw.rectangle([40, 40, img_width-40, img_height-40], outline=border_color, width=1)
    
    # Title
    title = "Rose Bread Recipe"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((img_width - title_width) // 2, 80), title, fill=border_color, font=title_font)
    
    # Draw decorative line
    draw.line([100, 150, img_width-100, 150], fill=border_color, width=2)
    
    # Recipe text (handwritten style)
    y_position = 200
    line_height = 45
    
    recipe_lines = [
        "Ingredients:",
        "• 2 cups flour",
        "• 1 cup sugar",
        "• 6 rose petals, fresh",
        "• 1/2 cup butter, melted",
        "• 2 eggs",
        "• 1 tsp vanilla extract",
        "• 1/2 tsp salt",
        "",
        "Instructions:",
        "1. Crush rose petals gently",
        "2. Mix flour, sugar, and salt",
        "3. Combine butter and eggs",
        "4. Fold in rose petals",
        "5. Bake at 350°F for 45 min",
        "",
        "For eternal love & memory",
        "- Cordelia"
    ]
    
    for line in recipe_lines:
        if line.startswith("- Cordelia"):
            # Use signature font for the signature
            draw.text((600, y_position), line, fill=border_color, font=signature_font)
        elif line:
            draw.text((80, y_position), line, fill=border_color, font=text_font)
        y_position += line_height
    
    # Save image
    img.save(img_path)
    print(f"Created image: {img_path}")
    return img_path

def create_rose_bread_pdf(recipe_img_path):
    """Create PDF with the rose bread recipe image"""
    pdf_path = os.path.join(OUTPUT_DIR, 'rose_bread_recipe.pdf')
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 0.5 * inch
    
    # Title
    c.setFont("Garamond", 24, leading=28)
    c.setFillColor(HexColor('#2C1810'))
    c.drawCentredString(width/2, height - 0.75*inch, "Eleanor's Rose Bread Recipe")
    
    # Decorative line
    c.setStrokeColor(HexColor('#DAA520'))
    c.setLineWidth(2)
    c.line(margin, height - 1*inch, width - margin, height - 1*inch)
    
    # Add the recipe image
    if os.path.exists(recipe_img_path):
        # Draw image centered, sized to fit on page
        img_display_width = 5 * inch
        img_display_height = 6 * inch
        x = (width - img_display_width) / 2
        y = height - 1.5*inch - img_display_height
        
        c.drawImage(recipe_img_path, x, y, width=img_display_width, height=img_display_height)
        
        # Add footer text
        c.setFont("Garamond", 10)
        c.setFillColor(HexColor('#666666'))
        c.drawCentredString(width/2, 0.75*inch, "A cherished family recipe passed through generations")
    
    c.save()
    print(f"Created: {pdf_path}")

# Main execution
if __name__ == '__main__':
    print("Generating new fact PDFs and recipe image...")
    
    # Create the rose bread recipe image
    recipe_img = create_rose_bread_recipe_image()
    
    # Create fact card PDF
    create_fact_card_pdf()
    
    # Create rose bread recipe PDF
    create_rose_bread_pdf(recipe_img)
    
    print("All PDFs created successfully!")
