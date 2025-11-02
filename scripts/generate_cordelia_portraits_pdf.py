#!/usr/bin/env python3
"""
Generate a PDF with 4x6 inch portrait cards of Cordelia
Two portraits per page, centered
"""

import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_cordelia_portraits_pdf():
    """Create PDF with two 4x6 Cordelia portrait cards"""
    pdf_path = os.path.join(OUTPUT_DIR, 'cordelia_portraits.pdf')
    
    # Two different Cordelia images for variety
    portraits = [
        os.path.join(IMAGES_DIR, 'rumor_images/cordelia_in_thought.png'),
        os.path.join(IMAGES_DIR, 'rumor_images/cordelia_socialite.png'),
    ]
    
    # Page settings
    page_width = 8.5 * inch
    page_height = 11 * inch
    portrait_width = 4 * inch
    portrait_height = 6 * inch
    
    c = canvas.Canvas(pdf_path, pagesize=(page_width, page_height))
    
    # Vertical positioning for two portraits
    top_y = page_height - 0.75 * inch - portrait_height
    bottom_y = 0.75 * inch
    x_center = (page_width - portrait_width) / 2
    
    for idx, portrait_path in enumerate(portraits):
        if not os.path.exists(portrait_path):
            print(f"⚠️  Portrait not found: {portrait_path}")
            continue
        
        # Determine Y position
        y_pos = top_y if idx == 0 else bottom_y
        
        # Draw portrait with border
        # Border
        c.setLineWidth(2)
        c.setStrokeColor(HexColor('#8B7355'))
        c.rect(x_center, y_pos, portrait_width, portrait_height, stroke=1, fill=0)
        
        # Draw image centered in the frame
        try:
            img = Image.open(portrait_path)
            
            # Calculate aspect ratio and fit to 4x6 frame
            img_aspect = img.width / img.height
            frame_aspect = 4 / 6  # 0.667 - portrait orientation
            
            if img_aspect > frame_aspect:
                # Image is wider - constrain by height
                display_height = portrait_height - 10
                display_width = display_height * img_aspect
            else:
                # Image is taller - constrain by width
                display_width = portrait_width - 10
                display_height = display_width / img_aspect
            
            # Center in frame
            img_x = x_center + (portrait_width - display_width) / 2
            img_y = y_pos + (portrait_height - display_height) / 2
            
            # Convert PIL Image to bytes for reportlab
            # Save image temporarily
            temp_path = '/tmp/temp_portrait.png'
            img.save(temp_path)
            c.drawImage(temp_path, img_x, img_y, width=display_width, height=display_height)
            
        except Exception as e:
            print(f"⚠️  Error loading portrait: {e}")
    
    c.save()
    print(f"✅ PDF created: {pdf_path}")
    print(f"   - Two 4x6 inch portrait frames")
    print(f"   - Cordelia images centered in frames")
    print(f"   - 0.75 inch margins top and bottom")

# Main execution
if __name__ == '__main__':
    print("📄 Generating Cordelia portraits PDF...")
    create_cordelia_portraits_pdf()
    print("✨ Done!")
