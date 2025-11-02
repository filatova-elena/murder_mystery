#!/usr/bin/env python3
"""
Generate PDF with new secret facts - styled like other fact cards with images
"""

import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_new_secrets_pdf():
    """Create PDF with the two new secret facts"""
    pdf_path = os.path.join(OUTPUT_DIR, 'new_secret_facts.pdf')
    
    # Two facts to add
    facts = [
        {
            "id": "heiress_fact_5",
            "character": "heiress",
            "title": "FACT",
            "text": "I heard Cordelia kept a diary. It should be in her room. Her room must have blue wall colors—she really liked the color blue.",
            "image": os.path.join(IMAGES_DIR, 'clue_images/photograph_eleanor_adolescent.png'),  # Blue-themed
        },
        {
            "id": "fiduciary_fact_5",
            "character": "fiduciary",
            "title": "FACT",
            "text": "There must be a record of who is the true heir of Montrose estate. There's that ornate desk at the fiduciary office—maybe one of the drawers contains a secret.",
            "image": os.path.join(IMAGES_DIR, 'clue_images_documents/trust_records.png'),  # Document-related
        }
    ]
    
    # Settings
    page_width = 8.5 * inch
    page_height = 11 * inch
    margin = 0.5 * inch
    card_width = 2.5 * inch
    card_height = 3.5 * inch
    
    c = canvas.Canvas(pdf_path, pagesize=(page_width, page_height))
    
    # Draw cards
    x_pos = margin
    y_pos = page_height - margin - card_height
    
    for i, fact in enumerate(facts):
        # Card background with border
        c.setLineWidth(2)
        c.setStrokeColor(HexColor('#DAA520'))  # Gold border
        c.rect(x_pos, y_pos, card_width, card_height, stroke=1, fill=0)
        
        # Title "FACT"
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(HexColor('#DAA520'))
        title_y = y_pos + card_height - 0.25*inch
        c.drawCentredString(x_pos + card_width/2, title_y, fact["title"])
        
        # Divider line under title
        c.setLineWidth(1)
        c.line(x_pos + 0.15*inch, title_y - 0.1*inch, x_pos + card_width - 0.15*inch, title_y - 0.1*inch)
        
        # Image
        img_y_start = title_y - 0.3*inch
        img_height = card_height * 0.5
        img_path = fact["image"]
        
        if os.path.exists(img_path):
            # Load and draw image
            try:
                img = Image.open(img_path)
                img_aspect = img.width / img.height
                img_width = img_height * img_aspect
                if img_width > card_width - 0.3*inch:
                    img_width = card_width - 0.3*inch
                    img_height = img_width / img_aspect
                
                img_x = x_pos + (card_width - img_width) / 2
                img_y = img_y_start - img_height
                c.drawImage(img_path, img_x, img_y, width=img_width, height=img_height)
            except:
                pass
        
        # Text
        text_y = img_y_start - img_height - 0.2*inch
        text_height = y_pos + 0.4*inch - text_y
        
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor('#2C1810'))
        
        # Wrap and draw text
        lines = []
        words = fact["text"].split()
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) > 30:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        
        text_start_y = text_y + text_height - 12
        for j, line in enumerate(lines[:4]):  # Max 4 lines
            line_y = text_start_y - (j * 10)
            if line_y > y_pos + 5:
                c.drawString(x_pos + 0.15*inch, line_y, line)
        
        # Character name at bottom
        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(HexColor('#666666'))
        c.drawRightString(x_pos + card_width - 0.1*inch, y_pos + 0.05*inch, fact["character"].upper())
        
        # Move to next card position
        x_pos += card_width + margin * 0.5
        if (i + 1) % 2 == 0:  # 2 cards per row
            x_pos = margin
            y_pos -= card_height + margin * 0.5
    
    c.save()
    print(f"✅ PDF created: {pdf_path}")

# Main execution
if __name__ == '__main__':
    print("📄 Generating new secret facts PDF...")
    create_new_secrets_pdf()
    print("✨ Done!")
