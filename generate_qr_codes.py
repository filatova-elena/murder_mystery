#!/usr/bin/env python3
"""
QR Code Generator for Murder Mystery Game
Generates QR codes that link to different clues and investigation materials
"""

import os
import qrcode
from qrcode.image.pure import PyPNGImage
from PIL import Image, ImageDraw, ImageFont
import json
from pathlib import Path

# Base URL for the hosted game (change this to your GitHub Pages URL)
BASE_URL = "https://filatova-elena.github.io/murder_mystery"

def create_qr_code(url, filename, output_dir="qr_codes"):
    """
    Create a QR code for a given URL and save it as an image file.
    
    Args:
        url (str): The URL to encode in the QR code
        filename (str): Name of the output file (without extension)
        output_dir (str): Directory to save QR codes
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to RGB if necessary
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')
    
    # Add URL text on top of the QR code
    # Expand image to add space for text
    text_height = 40  # Space for text at the top
    new_width = qr_img.width
    new_height = qr_img.height + text_height
    
    # Create new image with expanded height
    img = Image.new('RGB', (new_width, new_height), color='white')
    
    # Paste QR code below the text area
    img.paste(qr_img, (0, text_height))
    
    # Add URL text
    try:
        draw = ImageDraw.Draw(img)
        # Try to use a default font with size
        font = ImageFont.load_default()
        
        # Use textbbox instead of textsize (textsize is deprecated)
        bbox = draw.textbbox((0, 0), url, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (new_width - text_width) // 2
        
        # Draw the text
        draw.text((text_x, 10), url, font=font, fill="black")
    except Exception as e:
        print(f"Warning: Could not add text to QR code: {e}")
    
    # Save the image
    output_path = os.path.join(output_dir, f"{filename}.png")
    img.save(output_path)
    print(f"✓ Generated: {output_path} -> {url}")
    return output_path

def generate_botanical_qr_codes(output_dir="qr_codes"):
    """Generate QR codes for all botanical clues"""
    print("\n📚 Generating Botanical Clue QR Codes...")
    
    botanicals = [
        "foxglove", "damiana", "valerian", "mandrake", "rose_otto",
        "potassium-bromide", "calcium-lactate", "iron-citrate",
        "vanilla-cherry-honey", "grain-alcohol", "plant-specimens",
        "herb-encyclopedia", "lavender", "rosemary", "thyme", "nettle",
        "chamomile", "ginger", "sage", "peppers"
    ]
    
    for botanical in botanicals:
        url = f"{BASE_URL}/clue/botanicals/{botanical}.html"
        create_qr_code(url, f"botanical_{botanical}", output_dir)

def generate_document_qr_codes(output_dir="qr_codes"):
    """Generate QR codes for all document clues"""
    print("\n📄 Generating Document QR Codes...")
    
    documents = [
        "engagement_card", "prenup_agreement", "death_cert_alice",
        "death_cert_sebastian", "death_cert_cordelia", "autopsy_alice",
        "autopsy_sebastian", "autopsy_cordelia", "payment_records",
        "trust_records", "name_change_docs", "romano_shipping",
        "shipping_manifests_romano", "marriage_certificate_dimarco",
        "bank_statement_fragments", "boat_registration_marina",
        "treasure_map_hand_drawn", "sebastian_pharmacy_orders"
    ]
    
    for document in documents:
        url = f"{BASE_URL}/clue/documents/{document}.html"
        create_qr_code(url, f"document_{document}", output_dir)

def generate_character_qr_codes(output_dir="qr_codes"):
    """Generate QR codes for all characters"""
    print("\n👥 Generating Character QR Codes...")
    
    characters = [
        "professor", "explorer", "baker", "heiress", "fiduciary",
        "doctor", "mortician", "clockmaker", "dressmaker", "artcollector",
        "influencer", "psychic"
    ]
    
    for character in characters:
        url = f"{BASE_URL}/character/{character}.html"
        create_qr_code(url, f"character_{character}", output_dir)

def generate_custom_qr_code(url, filename, output_dir="qr_codes"):
    """Generate a QR code for a custom URL"""
    print(f"\n🔗 Generating Custom QR Code...")
    create_qr_code(url, filename, output_dir)

def generate_all_qr_codes(output_dir="qr_codes"):
    """Generate all QR codes at once"""
    print(f"🎯 Generating all QR codes to: {output_dir}/")
    generate_botanical_qr_codes(output_dir)
    generate_document_qr_codes(output_dir)
    generate_character_qr_codes(output_dir)
    print(f"\n✅ All QR codes generated successfully!")
    print(f"📁 Find them in: {os.path.abspath(output_dir)}/")

def main():
    """Main entry point"""
    import argparse
    
    global BASE_URL
    
    parser = argparse.ArgumentParser(
        description="Generate QR codes for Murder Mystery game clues"
    )
    parser.add_argument(
        "--type",
        choices=["all", "botanicals", "documents", "characters", "custom"],
        default="all",
        help="Type of QR codes to generate (default: all)"
    )
    parser.add_argument(
        "--url",
        help="Custom URL for QR code (used with --type custom)"
    )
    parser.add_argument(
        "--name",
        help="Filename for custom QR code (used with --type custom)"
    )
    parser.add_argument(
        "--output",
        default="qr_codes",
        help="Output directory for QR codes (default: qr_codes)"
    )
    parser.add_argument(
        "--base-url",
        default=BASE_URL,
        help=f"Base URL for generated links (default: {BASE_URL})"
    )
    
    args = parser.parse_args()
    
    # Update global BASE_URL if provided
    BASE_URL = args.base_url
    
    if args.type == "all":
        generate_all_qr_codes(args.output)
    elif args.type == "botanicals":
        generate_botanical_qr_codes(args.output)
    elif args.type == "documents":
        generate_document_qr_codes(args.output)
    elif args.type == "characters":
        generate_character_qr_codes(args.output)
    elif args.type == "custom":
        if not args.url or not args.name:
            print("❌ Error: --url and --name are required for custom QR codes")
            return
        generate_custom_qr_code(args.url, args.name, args.output)

if __name__ == "__main__":
    main()
