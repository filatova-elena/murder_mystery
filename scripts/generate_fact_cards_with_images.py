#!/usr/bin/env python3
"""
Generate fact cards PDF with AI-generated images, ornate 1920s styling
Creates fact_cards3.pdf with images from fact_images/
Adjusts image size if text doesn't fit, adds 10px padding
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

def load_facts():
    """Load facts from rumors.json"""
    with open('data/rumors.json', 'r') as f:
        data = json.load(f)
    return data.get('rumors', [])

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

def measure_text_height(lines, font, line_spacing=12):
    """Calculate height needed for text lines"""
    return len(lines) * line_spacing

def create_fact_card(fact_id, fact_text, image_path):
    """
    Create a single fact card image
    Dynamically adjusts image size if text doesn't fit
    
    Returns:
        PIL Image object for the card
    """
    # Create card with background
    card = Image.new('RGB', (CARD_W_PX, CARD_H_PX), color='#F5E6D3')
    draw = ImageDraw.Draw(card)
    
    # Draw ornate border
    draw_ornate_border(draw, 5, 5, CARD_W_PX - 10, CARD_H_PX - 10, color='#8B7355')
    
    try:
        # Try to load fonts - fallback to default if not available
        title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 24)
        text_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 10)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Draw "FACT" title
    fact_text_bbox = draw.textbbox((0, 0), "FACT", font=title_font)
    fact_text_width = fact_text_bbox[2] - fact_text_bbox[0]
    fact_x = (CARD_W_PX - fact_text_width) // 2
    draw.text((fact_x, 12), "FACT", fill='#8B7355', font=title_font)
    
    title_end = 12 + (fact_text_bbox[3] - fact_text_bbox[1]) + 8  # 8px gap after title
    
    # Prepare text with padding
    text_content_width = CARD_W_PX - (TEXT_PADDING * 2)
    max_chars = int((text_content_width / (CARD_W_PX)) * 35)  # Approximate chars per line
    
    # Wrap text
    wrapped = textwrap.fill(fact_text, width=max_chars)
    lines = wrapped.split('\n')
    line_height = 12
    
    # Start with 55% image height and reduce if needed
    image_height_percent = 0.55
    
    # Try to load and resize image
    image_loaded = False
    img = None
    img_height = 0
    content_start = title_end
    
    try:
        if Path(image_path).exists():
            img = Image.open(image_path)
            
            # Calculate available space for text
            available_for_text = CARD_H_PX - title_end - TEXT_PADDING - TEXT_PADDING
            
            # Adjust image height based on text length
            # Start with 55% and reduce if text is too long
            for percent in [0.55, 0.45, 0.35, 0.25, 0.15]:
                potential_img_height = int(CARD_H_PX * percent)
                text_space = CARD_H_PX - title_end - potential_img_height - (TEXT_PADDING * 3)
                max_lines = max(1, int(text_space / line_height))
                
                if len(lines) <= max_lines:
                    image_height_percent = percent
                    break
            
            img_height = int(CARD_H_PX * image_height_percent)
            img.thumbnail((CARD_W_PX - 20, img_height), Image.Resampling.LANCZOS)
            
            # Center image horizontally
            img_x = (CARD_W_PX - img.width) // 2
            img_y = title_end
            
            # Paste image onto card
            card.paste(img, (img_x, img_y))
            
            content_start = img_y + img.height + TEXT_PADDING
            image_loaded = True
    except Exception as e:
        print(f"  ⚠️ Could not load image: {e}")
        image_loaded = False
    
    # Calculate final text space
    text_area_height = CARD_H_PX - content_start - TEXT_PADDING
    max_lines_available = max(1, int(text_area_height / line_height))
    
    # Truncate lines if necessary
    if len(lines) > max_lines_available:
        lines = lines[:max_lines_available]
        if lines:
            # Remove last word and add ellipsis if we truncated
            lines[-1] = (lines[-1][:max_chars - 5]).rstrip() + '...'
    
    # Draw wrapped text with padding
    line_y = content_start + TEXT_PADDING
    for line in lines:
        if line_y + line_height < CARD_H_PX - TEXT_PADDING:
            draw.text((TEXT_PADDING, line_y), line, fill='#2C2C2C', font=text_font)
            line_y += line_height
    
    return card

def main():
    """Generate fact cards PDF"""
    
    print("="*70)
    print("📋 Fact Cards PDF Generator (with AI images)")
    print("="*70)
    
    facts = load_facts()
    print(f"\nLoading {len(facts)} facts...")
    
    # Create list to hold page images
    pages = []
    current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='#FFFAF0')
    current_card_index = 0
    
    print(f"Grid: {COLS} columns × {ROWS} rows = {CARDS_PER_PAGE} cards per page")
    print(f"Text padding: {TEXT_PADDING}px")
    print(f"Creating cards...\n")
    
    for fact_idx, fact in enumerate(facts, 1):
        fact_id = fact['id']
        fact_text = fact['text']
        image_path = f"fact_images/fact_{fact_id:02d}.png"
        
        print(f"Card {fact_idx:2d}: {fact_text[:50]:<50}", end=" ")
        
        try:
            # Create card
            card = create_fact_card(fact_id, fact_text, image_path)
            
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
            'fact_cards3.pdf',
            'PDF',
            save_all=True,
            append_images=pages[1:] if len(pages) > 1 else []
        )
        print(f"✅ Saved: fact_cards3.pdf")
    
    print("\n" + "="*70)
    print(f"✅ Complete!")
    print(f"   Total cards: {len(facts)}")
    print(f"   Total pages: {len(pages)}")
    print(f"   File: fact_cards3.pdf")
    print(f"   Card dims: {CARD_WIDTH}\" × {CARD_HEIGHT}\"")
    print(f"   Text padding: {TEXT_PADDING}px")
    print(f"   Dynamic image sizing: Enabled (adjusts for text fit)")
    print("="*70)

if __name__ == "__main__":
    main()
