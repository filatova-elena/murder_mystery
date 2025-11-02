#!/usr/bin/env python3
"""
Generate a PDF with 2 QR codes (2x2 inches each) for the portrait artifacts
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
QR_DIR = os.path.join(PROJECT_DIR, 'qr_codes')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_portrait_qr_pdf():
    pdf_path = os.path.join(OUTPUT_DIR, 'portrait_qr_codes.pdf')
    
    qr_codes = [
        {
            "name": "Portrait of Margaret Montrose",
            "path": os.path.join(QR_DIR, 'portrait_margaret_montrose.png'),
            "y": 8 * inch
        },
        {
            "name": "Portrait of Young Cordelia Montrose",
            "path": os.path.join(QR_DIR, 'portrait_young_cordelia.png'),
            "y": 4 * inch
        }
    ]
    
    page_width = 8.5 * inch
    page_height = 11 * inch
    qr_size = 2 * inch
    
    c = canvas.Canvas(pdf_path, pagesize=(page_width, page_height))
    
    for qr in qr_codes:
        if not os.path.exists(qr["path"]):
            print(f"⚠️  QR code not found: {qr['path']}")
            continue
        
        # Center QR code horizontally
        x = (page_width - qr_size) / 2
        y = qr["y"]
        
        # Draw label
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(HexColor('#2C1810'))
        label_y = y + qr_size + 0.2 * inch
        c.drawCentredString(page_width / 2, label_y, qr["name"])
        
        # Draw QR code
        c.drawImage(qr["path"], x, y, width=qr_size, height=qr_size)
    
    c.save()
    print(f"✅ PDF created: {pdf_path}")

if __name__ == '__main__':
    print("📄 Generating portrait QR codes PDF...")
    create_portrait_qr_pdf()
    print("✨ Done!")
