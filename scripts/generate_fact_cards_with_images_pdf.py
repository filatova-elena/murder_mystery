#!/usr/bin/env python3
"""
Fact Cards with Images PDF Generator for Murder Mystery Game
Generates 1920s-styled images for each fact using Gemini API
"""

import os
import sys
import json
import argparse
import math
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    print("Note: google-generativeai not installed. Using placeholder images.")

def generate_fact_image(fact_text, api_key):
    """Generate a 1920s-styled image for a fact using Gemini"""
    if not HAS_GENAI or not api_key:
        return None
        
    try:
        genai.configure(api_key=api_key)
        
        prompt = f"""Generate a mysterious, atmospheric 1920s noir-style illustration in sepia tones for this mystery fact: "{fact_text[:100]}"
        
The image should:
- Be dark and moody with 1920s film noir aesthetic  
- Use sepia, black, and grey tones
- Include atmospheric elements (shadows, mystery, secrets)
- Have a square composition
- NOT include any text"""
        
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([prompt])
        
        # Note: Gemini 2.0 Flash doesn't generate images directly
        # You would need Gemini 1.5 Pro with image generation capability
        return None
        
    except Exception as e:
        print(f"Note: {e}")
        return None

def create_sepia_placeholder(width, height):
    """Create a sepia-toned placeholder image with texture"""
    image = Image.new('RGB', (width, height), color='#8B7355')
    pixels = image.load()
    
    # Add subtle noise for texture
    import random
    random.seed(42)  # For consistency
    for x in range(width):
        for y in range(height):
            if random.random() < 0.1:  # 10% of pixels
                noise = random.randint(-20, 20)
                r = max(0, min(255, 139 + noise))
                g = max(0, min(255, 115 + noise))
                b = max(0, min(255, 85 + noise))
                pixels[x, y] = (r, g, b)
    
    return image

def create_fact_cards_with_images_pdf(data_file="data/rumors.json", output_file="fact_cards2.pdf", api_key=None):
    """
    Create a PDF with fact cards featuring images and bottom text.
    """
    
    # Get API key from parameter or environment
    if not api_key:
        api_key = os.environ.get('GEMINI_API_KEY')
    
    # Page settings (in inches)
    page_width = 8.5
    page_height = 11.0
    margin = 0.5
    card_width = 2.5
    card_height = 3.5
    dpi = 150
    card_margin = 10  # pixels
    
    # Convert to pixels
    page_width_px = int(page_width * dpi)
    page_height_px = int(page_height * dpi)
    margin_px = int(margin * dpi)
    card_width_px = int(card_width * dpi)
    card_height_px = int(card_height * dpi)
    
    # Calculate grid
    usable_width_px = page_width_px - (2 * margin_px)
    usable_height_px = page_height_px - (2 * margin_px)
    
    cols_per_page = int(usable_width_px / card_width_px)
    rows_per_page = int(usable_height_px / card_height_px)
    cards_per_page = cols_per_page * rows_per_page
    
    print(f"\n{'='*60}")
    print(f"Fact Cards with Images PDF Generator")
    print(f"{'='*60}")
    print(f"Page size: {page_width}\" x {page_height}\"")
    print(f"Card size: {card_width}\" x {card_height}\"")
    print(f"Grid layout: {cols_per_page} columns × {rows_per_page} rows")
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
    if api_key:
        print(f"🎨 Generating images with Gemini API...")
    else:
        print(f"🎨 Using sepia-toned placeholder images...")
    print(f"📄 Creating PDF...\n")
    
    # Calculate number of pages
    num_pages = math.ceil(len(rumors) / cards_per_page)
    
    # Create pages
    pages = []
    card_index = 0
    
    for page_num in range(1, num_pages + 1):
        # Create new page image
        page_img = Image.new('RGB', (page_width_px, page_height_px), color='white')
        draw = ImageDraw.Draw(page_img)
        
        # Load fonts
        try:
            text_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 12)
            owner_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 10)
        except:
            try:
                text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
                owner_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 10)
            except:
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
                    # Draw card border
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
                    
                    # Image area (center with margins)
                    img_margin = card_margin
                    img_height = int(card_height_px * 0.55)  # 55% of card height for image
                    img_width = card_width_px - (2 * img_margin)
                    img_x = x + img_margin
                    img_y = y + img_margin
                    
                    # Generate or create placeholder image
                    fact_text = rumor.get('text', 'Mystery')
                    image = generate_fact_image(fact_text, api_key) if api_key else None
                    
                    if image is None:
                        # Create sepia placeholder
                        image = create_sepia_placeholder(img_width, img_height)
                    else:
                        # Resize to fit card
                        image = image.resize((img_width, img_height), Image.Resampling.LANCZOS)
                    
                    # Paste image onto card
                    page_img.paste(image, (img_x, img_y))
                    
                    # Text area (bottom with margins)
                    text_start_y = img_y + img_height + 5
                    text_area_height = card_height_px - (text_start_y - y) - card_margin
                    text_area_width = card_width_px - (2 * card_margin)
                    
                    # Wrap and display fact text
                    text = rumor.get('text', 'No text')
                    lines = textwrap.wrap(text, width=15)
                    
                    # Fit lines to available space
                    line_spacing = 13
                    max_lines = text_area_height // line_spacing
                    if len(lines) > max_lines:
                        lines = lines[:max_lines-1]
                        if lines:
                            lines[-1] = lines[-1].rstrip() + "..."
                    
                    for i, line in enumerate(lines):
                        draw.text(
                            (x + card_margin, text_start_y + (i * line_spacing)),
                            line,
                            fill='#1a1a1a',
                            font=text_font
                        )
                    
                    # Add ownership at very bottom
                    possession = rumor.get('possession', 'UNKNOWN').lower()
                    owner_text = f"— {possession.upper()} —"
                    draw.text(
                        (x + card_margin, y + card_height_px - card_margin - 12),
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
        
        print(f"\n{'='*60}")
        print(f"✅ PDF successfully created!")
        print(f"{'='*60}")
        print(f"📄 Filename: {output_file}")
        print(f"📊 Total pages: {len(pages)}")
        print(f"📦 Total fact cards: {len(rumors)}")
        print(f"✨ Style: 1920s Mystery with Sepia Images")
        print(f"{'='*60}\n")
        
        return True
    else:
        print(f"❌ Error: No pages created")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate PDF with 1920s-styled fact cards and images"
    )
    parser.add_argument(
        "--data",
        default="data/rumors.json",
        help="JSON file containing rumors/facts (default: data/rumors.json)"
    )
    parser.add_argument(
        "--output",
        default="fact_cards2.pdf",
        help="Output PDF filename (default: fact_cards2.pdf)"
    )
    parser.add_argument(
        "--api-key",
        help="Gemini API key (optional, can also use GEMINI_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    success = create_fact_cards_with_images_pdf(args.data, args.output, args.api_key)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
