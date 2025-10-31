#!/usr/bin/env python3
"""
Fact Cards PDF Generator for Murder Mystery Game
Creates a printable PDF with fact cards in a 1920s mystery style
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
import argparse
import math
import textwrap

def create_fact_cards_pdf(data_file="data/rumors.json", output_file="fact_cards.pdf"):
    """
    Create a PDF with fact cards arranged in a grid (1920s style).
    
    Layout:
    - Page size: 8.5" x 11" (letter)
    - Margins: 0.5" on all sides
    - Card size: 2.5" wide x 3.5" high
    - Grid: 3 columns x 2 rows = 6 cards per page
    - DPI: 150 (standard screen viewing)
    - Style: 1920s mystery with elegant typography
    """
    
    # Page settings (in inches)
    page_width = 8.5
    page_height = 11.0
    margin = 0.5
    card_width = 2.5
    card_height = 3.5
    dpi = 150
    
    # Convert to pixels
    page_width_px = int(page_width * dpi)
    page_height_px = int(page_height * dpi)
    margin_px = int(margin * dpi)
    card_width_px = int(card_width * dpi)
    card_height_px = int(card_height * dpi)
    
    # Calculate grid
    usable_width_px = page_width_px - (2 * margin_px)
    usable_height_px = page_height_px - (2 * margin_px)
    
    cols_per_page = int(usable_width_px / card_width_px)  # 3 columns
    rows_per_page = int(usable_height_px / card_height_px)  # 2 rows
    cards_per_page = cols_per_page * rows_per_page
    
    print(f"\n{'='*60}")
    print(f"Fact Cards PDF Generator - 1920s Mystery Style")
    print(f"{'='*60}")
    print(f"Page size: {page_width}\" x {page_height}\"")
    print(f"Margins: {margin}\" on all sides")
    print(f"Card size: {card_width}\" x {card_height}\"")
    print(f"DPI: {dpi}")
    print(f"Grid layout: {cols_per_page} columns × {rows_per_page} rows")
    print(f"Cards per page: {cards_per_page}")
    print(f"{'='*60}\n")
    
    # Load rumors from JSON
    data_path = Path(data_file)
    if not data_path.exists():
        print(f"❌ Error: {data_file} not found")
        return False
    
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
        rumors = data.get('rumors', [])
    except Exception as e:
        print(f"❌ Error reading {data_file}: {e}")
        return False
    
    if not rumors:
        print(f"❌ Error: No rumors found in {data_file}")
        return False
    
    print(f"📊 Found {len(rumors)} fact cards")
    print(f"📄 Generating PDF...\n")
    
    # Calculate number of pages
    num_pages = math.ceil(len(rumors) / cards_per_page)
    
    # Create pages
    pages = []
    card_index = 0
    
    for page_num in range(1, num_pages + 1):
        # Create new page image
        page_img = Image.new('RGB', (page_width_px, page_height_px), color='white')
        draw = ImageDraw.Draw(page_img)
        
        # Try to load fonts (using system fonts for 1920s feel)
        try:
            # Use serif fonts for elegant, vintage feel
            title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 16)
            text_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 11)
            owner_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 9)
        except:
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
                text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11)
                owner_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 9)
            except:
                # Fallback to default font
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                owner_font = ImageFont.load_default()
        
        # Draw grid of cards
        for row in range(rows_per_page):
            if card_index >= len(rumors):
                break
                
            for col in range(cols_per_page):
                if card_index >= len(rumors):
                    break
                
                # Calculate position
                x = margin_px + (col * card_width_px)
                y = margin_px + (row * card_height_px)
                
                # Get rumor/fact
                rumor = rumors[card_index]
                
                try:
                    # Draw ornate card border (1920s style)
                    # Outer border
                    draw.rectangle(
                        [x, y, x + card_width_px, y + card_height_px],
                        outline='#1a1a1a',
                        width=3
                    )
                    # Inner decorative border
                    draw.rectangle(
                        [x + 4, y + 4, x + card_width_px - 4, y + card_height_px - 4],
                        outline='#4a4a4a',
                        width=1
                    )
                    
                    # Add decorative corner elements
                    corner_size = 8
                    # Top-left corner
                    draw.line([(x + 8, y + 6), (x + 12, y + 6)], fill='#1a1a1a', width=1)
                    draw.line([(x + 6, y + 8), (x + 6, y + 12)], fill='#1a1a1a', width=1)
                    # Top-right corner
                    draw.line([(x + card_width_px - 12, y + 6), (x + card_width_px - 8, y + 6)], fill='#1a1a1a', width=1)
                    draw.line([(x + card_width_px - 6, y + 8), (x + card_width_px - 6, y + 12)], fill='#1a1a1a', width=1)
                    
                    # Add title "FACT" with ornamental separator
                    draw.text(
                        (x + card_width_px // 2 - 12, y + 12),
                        "FACT",
                        fill='#1a1a1a',
                        font=title_font
                    )
                    
                    # Decorative line under title
                    draw.line(
                        [(x + 12, y + 40), (x + card_width_px - 12, y + 40)],
                        fill='#2a2a2a',
                        width=2
                    )
                    
                    # Add decorative dots
                    dot_y = y + 40
                    draw.ellipse([(x + 16, dot_y - 2), (x + 20, dot_y + 2)], fill='#2a2a2a')
                    draw.ellipse([(x + card_width_px - 20, dot_y - 2), (x + card_width_px - 16, dot_y + 2)], fill='#2a2a2a')
                    
                    # Add fact text with word wrapping
                    text = rumor.get('text', 'No text')
                    lines = textwrap.wrap(text, width=22)
                    
                    text_y = y + 50
                    line_spacing = 17
                    for i, line in enumerate(lines[:4]):  # Max 4 lines
                        draw.text(
                            (x + 12, text_y + (i * line_spacing)),
                            line,
                            fill='#1a1a1a',
                            font=text_font
                        )
                    
                    # Decorative line before attribution
                    draw.line(
                        [(x + 12, y + card_height_px - 32), (x + card_width_px - 12, y + card_height_px - 32)],
                        fill='#2a2a2a',
                        width=1
                    )
                    
                    # Add who starts with this card at the bottom
                    possession = rumor.get('possession', 'UNKNOWN').lower()
                    draw.text(
                        (x + 12, y + card_height_px - 24),
                        f"— {possession.upper()} —",
                        fill='#1a1a1a',
                        font=owner_font
                    )
                    
                    card_index += 1
                    
                except Exception as e:
                    print(f"⚠️  Warning: Could not process fact {card_index}: {e}")
                    card_index += 1
        
        pages.append(page_img)
    
    # Save as PDF
    if pages:
        pages[0].save(output_file, save_all=True, append_images=pages[1:])
        
        print(f"{'='*60}")
        print(f"✅ PDF successfully created!")
        print(f"{'='*60}")
        print(f"📄 Filename: {output_file}")
        print(f"📊 Total pages: {len(pages)}")
        print(f"📦 Total fact cards: {len(rumors)}")
        print(f"✨ Style: 1920s Mystery with elegant typography")
        print(f"{'='*60}\n")
        
        return True
    else:
        print(f"❌ Error: No pages created")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate PDF with 1920s-styled fact cards"
    )
    parser.add_argument(
        "--data",
        default="data/rumors.json",
        help="JSON file containing rumors/facts (default: data/rumors.json)"
    )
    parser.add_argument(
        "--output",
        default="fact_cards.pdf",
        help="Output PDF filename (default: fact_cards.pdf)"
    )
    
    args = parser.parse_args()
    
    success = create_fact_cards_pdf(args.data, args.output)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
