#!/usr/bin/env python3
import os
import qrcode
from pathlib import Path

BASE_URL = "https://filatova-elena.github.io/murder_mystery"

def create_qr_code(url, filename, output_dir="qr_codes"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')
    output_path = os.path.join(output_dir, f"{filename}.png")
    qr_img.save(output_path)
    print(f"✅ Generated: {output_path}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    qr_dir = os.path.join(project_dir, 'qr_codes')
    
    artifacts = [
        {"id": "portrait_margaret_montrose", "path": "clue/artifacts/portrait-margaret-montrose.html"},
        {"id": "portrait_young_cordelia", "path": "clue/artifacts/portrait-young-cordelia.html"}
    ]
    
    print("📱 Generating QR codes for portrait artifacts...")
    for artifact in artifacts:
        url = f"{BASE_URL}/{artifact['path']}"
        create_qr_code(url, artifact['id'], qr_dir)
    print("✨ Done!")
