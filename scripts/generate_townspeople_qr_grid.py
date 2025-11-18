#!/usr/bin/env python3
"""
Generate a 2x2 QR code grid for townspeople characters
Detective, Journalist, Animal Expert
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

# Townspeople characters
TOWNSPEOPLE = [
    {
        'id': 'townperson_detective',
        'name': 'Detective',
        'qr_file': 'townperson_detective.png'
    },
    {
        'id': 'townperson_journalist',
        'name': 'Journalist',
        'qr_file': 'townperson_journalist.png'
    },
    {
        'id': 'townperson_animalexpert',
        'name': 'Animal Expert',
        'qr_file': 'townperson_animalexpert.png'
    }
]

def create_qr_grid():
    """Create a 2x2 QR code grid PDF"""
    
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    QR_CODES_DIR = os.path.join(PROJECT_DIR, 'qr_codes')
    OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("🔲 Creating Townspeople QR Code Grid...")
    print("=" * 60)
    
    # Create page
    page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='#FFFAF0')
    draw = ImageDraw.Draw(page)
    
    # Draw border
    draw.rectangle([MARGIN_PX, MARGIN_PX, PAGE_W_PX - MARGIN_PX, PAGE_H_PX - MARGIN_PX],
                   outline='#8B7355', width=2)
    
    # Calculate grid positions (2x2 = 2 columns, up to 2 rows)
    usable_width = PAGE_W_PX - (MARGIN_PX * 2)
    usable_height = PAGE_H_PX - (MARGIN_PX * 2)
    
    # Space between codes
    spacing = int(0.5 * DPI)  # 0.5 inches
    
    # Calculate starting positions for 2-column layout
    col_width = (usable_width - spacing) / 2
    
    # Title at top
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 16)
    except:
        title_font = ImageFont.load_default()
    
    title_y = MARGIN_PX + 0.25 * DPI
    draw.text((PAGE_W_PX / 2, title_y), "Townspeople Characters", 
              fill='#8B7355', font=title_font, anchor="mm")
    
    # Grid starting position
    grid_start_y = title_y + 0.5 * DPI
    
    # Add QR codes in 2-column grid
    for idx, char in enumerate(TOWNSPEOPLE):
        row = idx // 2
        col = idx % 2
        
        qr_path = os.path.join(QR_CODES_DIR, char['qr_file'])
        
        # Calculate position
        x = MARGIN_PX + (col_width + spacing) * col + (col_width - QR_SIZE_PX) / 2
        y = grid_start_y + (QR_SIZE_PX + spacing) * row
        
        print(f"  {idx + 1}. {char['name']:<20}", end=" ")
        
        try:
            if Path(qr_path).exists():
                qr_img = Image.open(qr_path)
                qr_img.thumbnail((QR_SIZE_PX, QR_SIZE_PX), Image.Resampling.LANCZOS)
                
                # Paste QR code
                page.paste(qr_img, (int(x), int(y)))
                
                # Add label below QR code
                try:
                    label_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 11)
                except:
                    label_font = ImageFont.load_default()
                
                label_y = int(y + QR_SIZE_PX + 0.1 * DPI)
                label_x = int(x + QR_SIZE_PX / 2)
                draw.text((label_x, label_y), char['name'], 
                         fill='#8B7355', font=label_font, anchor="mm")
                
                print("✅")
            else:
                print(f"❌ (QR not found)")
        except Exception as e:
            print(f"❌ ({e})")
    
    # Save PDF
    pdf_path = os.path.join(OUTPUT_DIR, 'townspeople_qr_codes.pdf')
    page.save(pdf_path, 'PDF')
    
    print("\n" + "=" * 60)
    print(f"✅ PDF Created: {pdf_path}")
    print(f"   Layout: 2x2 QR Code Grid")
    print(f"   Size: 2.5 x 2.5 inches each")
    print(f"   Characters: {len(TOWNSPEOPLE)}")
    print("=" * 60)

if __name__ == '__main__':
    create_qr_grid()


