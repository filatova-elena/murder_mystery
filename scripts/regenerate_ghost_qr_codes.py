#!/usr/bin/env python3
"""
Regenerate QR codes for ghost characters with correct GitHub URLs
"""

import qrcode
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Base URL for the hosted game
BASE_URL = "https://filatova-elena.github.io/murder_mystery"

# Ghost characters QR codes
GHOST_QR_CODES = {
    'ghost_alice': f'{BASE_URL}/character/ghost_alice.html',
    'ghost_cordelia': f'{BASE_URL}/character/ghost_cordelia.html',
    'ghost_sebastian': f'{BASE_URL}/character/ghost_sebastian.html',
}

def create_qr_code(url, filename, output_dir="qr_codes"):
    """
    Create a QR code for a given URL and save it as an image file.
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
    output_path = Path(output_dir) / f"{filename}.png"
    img.save(output_path)
    print(f"✓ Generated: {filename}.png -> {url}")
    return output_path

def main():
    """Generate ghost QR codes"""
    
    print("="*70)
    print("🎭 Ghost Character QR Code Generator")
    print("="*70 + "\n")
    
    successful = 0
    for character_key, url in GHOST_QR_CODES.items():
        qr_filename = f'character_{character_key}'
        if create_qr_code(url, qr_filename):
            successful += 1
    
    print("\n" + "="*70)
    print(f"✅ Generated {successful}/{len(GHOST_QR_CODES)} ghost QR codes")
    print(f"📍 Base URL: {BASE_URL}")
    print("="*70)

if __name__ == "__main__":
    main()
