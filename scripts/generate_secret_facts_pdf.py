#!/usr/bin/env python3
"""
Secret Facts PDF Generator - Matches existing fact card style
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
import math
import textwrap
import os

def get_text_width(draw, text, font):
    """Get the width of text for centering"""
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]
    except:
        return len(text) * 6

def create_secret_facts_pdf(output_file="to_print/new_secret_facts.pdf"):
    """
    Create a PDF with secret facts using the same style as fact_cards.pdf
    """
    
    # Define the two secret facts
    facts = [
        {
            "id": "heiress_secret",
            "text": "I heard Cordelia kept a diary. It should be in her room. Her room must have blue wall colors—she really liked the color blue.",
            "possession": "heiress"
        },
        {
            "id": "fiduciary_secret",
            "text": "There must be a record of who is the true heir of Montrose estate. There's that ornate desk at the fiduciary office—maybe one of the drawers contains a secret.",
            "possession": "fiduciary"
        }
    ]
    
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
    print(f"Secret Facts PDF Generator - 1920s Mystery Style")
    print(f"{'='*60}")
    print(f"Page size: {page_width}\" x {page_height}\"")
    print(f"Card size: {card_width}\" x {card_height}\"")
    print(f"Grid layout: {cols_per_page} columns × {rows_per_page} rows")
    print(f"{'='*60}\n")
    
    print(f"📊 Found {len(facts)} secret facts")
    print(f"📄 Generating PDF...\n")
    
    # Calculate number of pages
    num_pages = math.ceil(len(facts) / cards_per_page)
    
    # Create pages
    pages = []
    card_index = 0
    
    for page_num in range(1, num_pages + 1):
        # Create new page image
        page_img = Image.new('RGB', (page_width_px, page_height_px), color='white')
        draw = ImageDraw.Draw(page_img)
        
        # Try to load fonts
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 32)
            text_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 14)
            owner_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 10)
        except:
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
                text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
                owner_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 10)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                owner_font = ImageFont.load_default()
        
        # Draw grid of cards
        for row in range(rows_per_page):
            if card_index >= len(facts):
                break
                
            for col in range(cols_per_page):
                if card_index >= len(facts):
                    break
                
                # Calculate position
                x = margin_px + (col * card_width_px)
                y = margin_px + (row * card_height_px)
                card_center_x = x + (card_width_px // 2)
                
                # Get fact
                fact = facts[card_index]
                
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
                    # Top-left corner
                    draw.line([(x + 8, y + 6), (x + 12, y + 6)], fill='#1a1a1a', width=1)
                    draw.line([(x + 6, y + 8), (x + 6, y + 12)], fill='#1a1a1a', width=1)
                    # Top-right corner
                    draw.line([(x + card_width_px - 12, y + 6), (x + card_width_px - 8, y + 6)], fill='#1a1a1a', width=1)
                    draw.line([(x + card_width_px - 6, y + 8), (x + card_width_px - 6, y + 12)], fill='#1a1a1a', width=1)
                    
                    # Add title "FACT" centered
                    title_text = "FACT"
                    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
                    title_width = title_bbox[2] - title_bbox[0]
                    title_x = card_center_x - (title_width // 2)
                    draw.text(
                        (title_x, y + 10),
                        title_text,
                        fill='#1a1a1a',
                        font=title_font
                    )
                    
                    # Decorative line under title
                    draw.line(
                        [(x + 12, y + 50), (x + card_width_px - 12, y + 50)],
                        fill='#2a2a2a',
                        width=2
                    )
                    
                    # Add decorative dots
                    dot_y = y + 50
                    draw.ellipse([(x + 16, dot_y - 2), (x + 20, dot_y + 2)], fill='#2a2a2a')
                    draw.ellipse([(x + card_width_px - 20, dot_y - 2), (x + card_width_px - 16, dot_y + 2)], fill='#2a2a2a')
                    
                    # Add fact text with word wrapping, centered
                    text = fact.get('text', 'No text')
                    
                    # Wrap text at 13 characters per line
                    lines = textwrap.wrap(text, width=13)
                    
                    # Ensure we don't exceed card height
                    available_height = card_height_px - 120
                    line_spacing = 16
                    max_lines = available_height // line_spacing
                    
                    # Trim to fit
                    if len(lines) > max_lines:
                        lines = lines[:max_lines-1]
                        if lines:
                            lines[-1] = lines[-1].rstrip() + "..."
                    
                    # Calculate starting Y to center text vertically in available space
                    total_text_height = len(lines) * line_spacing
                    text_start_y = y + 60 + ((available_height - total_text_height) // 2)
                    
                    for i, line in enumerate(lines):
                        line_bbox = draw.textbbox((0, 0), line, font=text_font)
                        line_width = line_bbox[2] - line_bbox[0]
                        line_x = card_center_x - (line_width // 2)
                        draw.text(
                            (line_x, text_start_y + (i * line_spacing)),
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
                    
                    # Add possession at the bottom, centered
                    possession = fact.get('possession', 'UNKNOWN').lower()
                    owner_text = f"— {possession.upper()} —"
                    owner_bbox = draw.textbbox((0, 0), owner_text, font=owner_font)
                    owner_width = owner_bbox[2] - owner_bbox[0]
                    owner_x = card_center_x - (owner_width // 2)
                    draw.text(
                        (owner_x, y + card_height_px - 24),
                        owner_text,
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
        print(f"📦 Total fact cards: {len(facts)}")
        print(f"✨ Style: 1920s Mystery - Centered, Full Text")
        print(f"{'='*60}\n")
        
        return True
    else:
        print(f"❌ Error: No pages created")
        return False

# Main execution
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output = os.path.join(project_dir, 'to_print', 'new_secret_facts.pdf')
    
    print("📄 Generating new secret facts PDF...")
    success = create_secret_facts_pdf(output)
    exit(0 if success else 1)
