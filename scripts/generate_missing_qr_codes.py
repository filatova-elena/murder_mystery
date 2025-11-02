#!/usr/bin/env python3
"""
Generate missing QR codes for ghost characters
"""

import qrcode
from pathlib import Path

# QR codes to generate for ghost characters
GHOST_QR_CODES = {
    'ghost_alice': 'character/ghost_alice.html',
    'ghost_cordelia': 'character/ghost_cordelia.html',
    'ghost_sebastian': 'character/ghost_sebastian.html',
}

def generate_qr_code(filename: str, url: str):
    """Generate a QR code and save it"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        output_path = Path('qr_codes') / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        img.save(output_path)
        print(f"✅ Generated: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error generating {filename}: {e}")
        return False

def main():
    """Generate missing ghost QR codes"""
    
    print("="*70)
    print("🎯 QR Code Generator - Missing Ghost Characters")
    print("="*70 + "\n")
    
    successful = 0
    for qr_name, url in GHOST_QR_CODES.items():
        qr_filename = f'character_{qr_name}.png'
        if generate_qr_code(qr_filename, url):
            successful += 1
    
    print("\n" + "="*70)
    print(f"✅ Generated {successful}/{len(GHOST_QR_CODES)} QR codes")
    print("="*70)

if __name__ == "__main__":
    main()
