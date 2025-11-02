#!/usr/bin/env python3
"""
Generate character cards PDF with character images and QR codes
Creates character_cards.pdf with character portraits and QR codes
Same style as RUMOR/FACT cards with ornate 1920s borders
Larger QR codes positioned to fit within borders
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Page and card dimensions (in inches)
PAGE_WIDTH = 8.5
PAGE_HEIGHT = 11
MARGIN = 0.5
CARD_WIDTH = 2.5
CARD_HEIGHT = 3.5

# Convert inches to pixels (72 DPI)
DPI = 72
PAGE_W_PX = int(PAGE_WIDTH * DPI)
PAGE_H_PX = int(PAGE_HEIGHT * DPI)
MARGIN_PX = int(MARGIN * DPI)
CARD_W_PX = int(CARD_WIDTH * DPI)
CARD_H_PX = int(CARD_HEIGHT * DPI)

# Padding in pixels
TEXT_PADDING = 10

# Calculate grid
USABLE_WIDTH = PAGE_W_PX - (MARGIN_PX * 2)
USABLE_HEIGHT = PAGE_H_PX - (MARGIN_PX * 2)
COLS = USABLE_WIDTH // CARD_W_PX  # 3 cards
ROWS = USABLE_HEIGHT // CARD_H_PX  # 2 cards
CARDS_PER_PAGE = COLS * ROWS

# Character names for display
CHARACTER_NAMES = {
    'artcollector': 'Art Collector',
    'baker': 'Baker',
    'clockmaker': 'Clockmaker',
    'doctor': 'Doctor',
    'dressmaker': 'Dressmaker',
    'explorer': 'Explorer',
    'fiduciary': 'Fiduciary',
    'ghost_alice': 'The Lonely Ghost',
    'ghost_cordelia': 'The Heartbroken Ghost',
    'ghost_sebastian': 'The Ghost of the Alchemist',
    'heiress': 'Heiress',
    'influencer': 'Influencer',
    'mortician': 'Mortician',
    'professor': 'Professor',
    'psychic': 'Psychic',
    'townperson': 'Townsperson',
}

def draw_ornate_border(draw, x, y, width, height, line_width=2, color='#8B7355'):
    """Draw ornate 1920s style border"""
    # Outer border
    draw.rectangle([x, y, x + width, y + height], outline=color, width=line_width)
    
    # Inner decorative border (slightly inside)
    inner_margin = line_width + 2
    draw.rectangle([x + inner_margin, y + inner_margin, 
                   x + width - inner_margin, y + height - inner_margin], 
                  outline=color, width=1)
    
    # Corner ornaments (small diamonds)
    corner_size = 4
    corners = [
        (x + 8, y + 8),  # top-left
        (x + width - 8, y + 8),  # top-right
        (x + 8, y + height - 8),  # bottom-left
        (x + width - 8, y + height - 8)  # bottom-right
    ]
    for cx, cy in corners:
        draw.ellipse([cx - corner_size, cy - corner_size, 
                     cx + corner_size, cy + corner_size], 
                    fill=color)

def create_character_card(character_key: str, character_name: str, image_path: str, qr_path: str):
    """
    Create a single character card image
    Layout: Character name at top, image in middle, QR code at bottom (larger, fitted within borders)
    
    Returns:
        PIL Image object for the card
    """
    # Create card with background
    card = Image.new('RGB', (CARD_W_PX, CARD_H_PX), color='#F5E6D3')
    draw = ImageDraw.Draw(card)
    
    # Draw ornate border
    draw_ornate_border(draw, 5, 5, CARD_W_PX - 10, CARD_H_PX - 10, color='#8B7355')
    
    try:
        # Load fonts
        name_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 12)
        small_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 8)
    except:
        name_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw character name at top (centered, smaller)
    name_bbox = draw.textbbox((0, 0), character_name, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (CARD_W_PX - name_width) // 2
    draw.text((name_x, 8), character_name, fill='#8B7355', font=name_font)
    
    name_end = 8 + (name_bbox[3] - name_bbox[1]) + 5  # 5px gap after name
    
    # QR code will be ~60px × 60px (fits well within border)
    qr_size = 60
    qr_bottom_padding = 12  # Padding from bottom edge to keep within border
    
    # Available height for character image
    available_height = CARD_H_PX - name_end - qr_size - qr_bottom_padding - 8
    
    # Load and resize character image
    image_loaded = False
    img_y_pos = name_end
    
    try:
        if Path(image_path).exists():
            img = Image.open(image_path)
            
            # Resize image to fit available space
            img_height = int(available_height * 0.95)  # Use most of available space
            img.thumbnail((CARD_W_PX - 20, img_height), Image.Resampling.LANCZOS)
            
            # Center image horizontally
            img_x = (CARD_W_PX - img.width) // 2
            img_y = img_y_pos
            
            # Paste image onto card
            card.paste(img, (img_x, img_y))
            
            img_y_pos = img_y + img.height + 3
            image_loaded = True
    except Exception as e:
        print(f"  ⚠️ Could not load image for {character_key}: {e}")
    
    # Load and paste QR code at bottom (fitted within borders)
    try:
        if Path(qr_path).exists():
            qr = Image.open(qr_path)
            
            # Resize QR code to fit
            qr.thumbnail((qr_size, qr_size), Image.Resampling.LANCZOS)
            
            # Center QR code horizontally and position near bottom with padding
            qr_x = (CARD_W_PX - qr.width) // 2
            qr_y = CARD_H_PX - qr.height - qr_bottom_padding  # Position with bottom padding
            
            # Paste QR code
            card.paste(qr, (qr_x, qr_y))
    except Exception as e:
        # QR code might not exist, that's okay
        pass
    
    return card

def main():
    """Generate character cards PDF"""
    
    print("="*70)
    print("🎭 Character Cards PDF Generator (Final)")
    print("="*70)
    
    characters = sorted(CHARACTER_NAMES.keys())
    print(f"\nLoading {len(characters)} characters...")
    
    # Create list to hold page images
    pages = []
    current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='#FFFAF0')
    current_card_index = 0
    
    print(f"Grid: {COLS} columns × {ROWS} rows = {CARDS_PER_PAGE} cards per page")
    print(f"QR codes: Correct GitHub URLs, fitted within borders\n")
    print(f"Creating cards...\n")
    
    for card_idx, character_key in enumerate(characters, 1):
        character_name = CHARACTER_NAMES[character_key]
        image_path = f"assets/characters/{character_key}.png"
        qr_path = f"qr_codes/character_{character_key}.png"
        
        print(f"Card {card_idx:2d}: {character_name:<30}", end=" ")
        
        try:
            # Create card
            card = create_character_card(character_key, character_name, image_path, qr_path)
            
            # Calculate position on page
            row = current_card_index // COLS
            col = current_card_index % COLS
            
            x = MARGIN_PX + (col * CARD_W_PX)
            y = MARGIN_PX + (row * CARD_H_PX)
            
            # Paste card onto current page
            current_page.paste(card, (x, y))
            current_card_index += 1
            
            print("✅")
            
            # Check if page is full
            if current_card_index >= CARDS_PER_PAGE:
                pages.append(current_page)
                current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='#FFFAF0')
                current_card_index = 0
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Add the last page if it has cards
    if current_card_index > 0:
        pages.append(current_page)
    
    # Save as PDF
    print(f"\n📄 Saving PDF with {len(pages)} pages...")
    if pages:
        pages[0].save(
            'character_cards.pdf',
            'PDF',
            save_all=True,
            append_images=pages[1:] if len(pages) > 1 else []
        )
        print(f"✅ Saved: character_cards.pdf")
    
    print("\n" + "="*70)
    print(f"✅ Complete!")
    print(f"   Total cards: {len(characters)}")
    print(f"   Total pages: {len(pages)}")
    print(f"   File: character_cards.pdf")
    print("="*70)

if __name__ == "__main__":
    main()
