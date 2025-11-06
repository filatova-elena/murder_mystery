#!/usr/bin/env python3
"""
Generate PDF with QR codes for ghost characters
The Lonely Ghost (Alice), The Heartbroken Ghost (Cordelia), The Ghost of the Alchemist (Sebastian)
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Page dimensions
PAGE_WIDTH = 8.5
PAGE_HEIGHT = 11
MARGIN = 0.5

# Convert inches to pixels (72 DPI)
DPI = 72
PAGE_W_PX = int(PAGE_WIDTH * DPI)
PAGE_H_PX = int(PAGE_HEIGHT * DPI)
MARGIN_PX = int(MARGIN * DPI)

# QR code size: 2.5 x 2.5 inches
QR_SIZE_INCH = 2.5
QR_SIZE_PX = int(QR_SIZE_INCH * DPI)

# Ghost characters
GHOSTS = [
    {
        'id': 'ghost_alice',
        'name': 'The Lonely Ghost',
        'qr_file': 'ghost_alice.png'
    },
    {
        'id': 'ghost_cordelia',
        'name': 'The Heartbroken Ghost',
        'qr_file': 'ghost_cordelia.png'
    },
    {
        'id': 'ghost_sebastian',
        'name': 'The Ghost of the Alchemist',
        'qr_file': 'ghost_sebastian.png'
    }
]

def create_ghost_qr_pdf():
    """Create a PDF with ghost character QR codes"""
    
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    QR_CODES_DIR = os.path.join(PROJECT_DIR, 'qr_codes')
    OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("👻 Creating Ghost Character QR Code PDF...")
    print("=" * 60)
    
    # Create page
    page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='#FFFAF0')
    draw = ImageDraw.Draw(page)
    
    # Draw border
    draw.rectangle([MARGIN_PX, MARGIN_PX, PAGE_W_PX - MARGIN_PX, PAGE_H_PX - MARGIN_PX],
                   outline='#8B7355', width=2)
    
    # Title at top
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 16)
    except:
        title_font = ImageFont.load_default()
    
    title_y = MARGIN_PX + 0.25 * DPI
    draw.text((PAGE_W_PX / 2, title_y), "Ghost Characters", 
              fill='#8B7355', font=title_font, anchor="mm")
    
    # Calculate grid positions (vertical layout, centered)
    spacing = int(0.4 * DPI)  # 0.4 inches between codes
    total_height = (QR_SIZE_PX * len(GHOSTS)) + (spacing * (len(GHOSTS) - 1))
    grid_start_y = title_y + 0.6 * DPI
    
    # Center the QR codes horizontally
    x_center = (PAGE_W_PX - QR_SIZE_PX) / 2
    
    # Add QR codes vertically
    for idx, ghost in enumerate(GHOSTS):
        qr_path = os.path.join(QR_CODES_DIR, ghost['qr_file'])
        
        # Calculate position
        y = grid_start_y + (QR_SIZE_PX + spacing) * idx
        
        print(f"  {idx + 1}. {ghost['name']:<35}", end=" ")
        
        try:
            if Path(qr_path).exists():
                qr_img = Image.open(qr_path)
                qr_img.thumbnail((QR_SIZE_PX, QR_SIZE_PX), Image.Resampling.LANCZOS)
                
                # Paste QR code
                page.paste(qr_img, (int(x_center), int(y)))
                
                # Add label below QR code
                try:
                    label_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 11)
                except:
                    label_font = ImageFont.load_default()
                
                label_y = int(y + QR_SIZE_PX + 0.15 * DPI)
                label_x = int(PAGE_W_PX / 2)
                draw.text((label_x, label_y), ghost['name'], 
                         fill='#8B7355', font=label_font, anchor="mm")
                
                print("✅")
            else:
                print(f"❌ (QR not found)")
        except Exception as e:
            print(f"❌ ({e})")
    
    # Save PDF
    pdf_path = os.path.join(OUTPUT_DIR, 'ghost_qr_codes.pdf')
    page.save(pdf_path, 'PDF')
    
    print("\n" + "=" * 60)
    print(f"✅ PDF Created: {pdf_path}")
    print(f"   Layout: Vertical Grid")
    print(f"   Size: 2.5 x 2.5 inches each")
    print(f"   Characters: {len(GHOSTS)}")
    print("=" * 60)

if __name__ == '__main__':
    create_ghost_qr_pdf()

