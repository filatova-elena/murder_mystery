#!/usr/bin/env python3
"""
QR Code PDF Generator for Murder Mystery Game
Creates a printable PDF with QR codes in a grid layout
Uses PIL/Pillow to create the PDF
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import argparse
import math

def create_qr_code_pdf(qr_dir="qr_codes", output_file="qr_codes_grid.pdf"):
    """
    Create a PDF with QR codes arranged in a grid.
    
    Layout:
    - Page size: 8.5" x 11" (letter)
    - Margins: 0.5" on all sides
    - QR code size: 2.5" x 2.5"
    - Grid: 3 columns x 4 rows = 12 QR codes per page
    - DPI: 150 (standard screen viewing)
    """
    
    # Page settings (in inches)
    page_width = 8.5
    page_height = 11.0
    margin = 0.5
    qr_size = 2.5
    title_height = 0.5
    dpi = 150
    
    # Convert to pixels
    page_width_px = int(page_width * dpi)
    page_height_px = int(page_height * dpi)
    margin_px = int(margin * dpi)
    qr_size_px = int(qr_size * dpi)
    title_height_px = int(title_height * dpi)
    
    # Calculate grid
    usable_width_px = page_width_px - (2 * margin_px)
    usable_height_px = page_height_px - (2 * margin_px) - title_height_px
    
    cols_per_page = int(usable_width_px / qr_size_px)  # 3 columns
    rows_per_page = int(usable_height_px / qr_size_px)  # 4 rows
    qr_codes_per_page = cols_per_page * rows_per_page
    
    print(f"\n{'='*60}")
    print(f"QR Code PDF Generator for Murder Mystery")
    print(f"{'='*60}")
    print(f"Page size: {page_width}\" x {page_height}\"")
    print(f"Margins: {margin}\" on all sides")
    print(f"QR code size: {qr_size}\" x {qr_size}\"")
    print(f"DPI: {dpi}")
    print(f"Grid layout: {cols_per_page} columns × {rows_per_page} rows")
    print(f"QR codes per page: {qr_codes_per_page}")
    print(f"{'='*60}\n")
    
    # Get all QR code files
    qr_path = Path(qr_dir)
    qr_files = sorted([f for f in qr_path.glob("*.png") if f.is_file()])
    
    if not qr_files:
        print(f"❌ Error: No QR codes found in {qr_dir}")
        return False
    
    print(f"📊 Found {len(qr_files)} QR code files")
    print(f"📄 Generating PDF...\n")
    
    # Calculate number of pages
    num_pages = math.ceil(len(qr_files) / qr_codes_per_page)
    
    # Create pages
    pages = []
    qr_index = 0
    
    for page_num in range(1, num_pages + 1):
        # Create new page image
        page_img = Image.new('RGB', (page_width_px, page_height_px), color='white')
        draw = ImageDraw.Draw(page_img)
        
        # Add page title
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
            title_font = font
        
        title = f"Murder Mystery QR Codes - Page {page_num}"
        draw.text((margin_px, margin_px // 2), title, fill='black', font=title_font)
        
        # Draw grid of QR codes
        for row in range(rows_per_page):
            if qr_index >= len(qr_files):
                break
                
            for col in range(cols_per_page):
                if qr_index >= len(qr_files):
                    break
                
                # Calculate position
                x = margin_px + (col * qr_size_px)
                y = margin_px + title_height_px + (row * qr_size_px)
                
                # Get QR code file
                qr_file = qr_files[qr_index]
                
                try:
                    # Load and resize QR code
                    qr_img = Image.open(qr_file).convert('RGB')
                    qr_img = qr_img.resize((qr_size_px - 10, qr_size_px - 30), Image.Resampling.LANCZOS)
                    
                    # Paste QR code onto page
                    page_img.paste(qr_img, (x + 5, y + 5))
                    
                    # Draw border
                    draw.rectangle([x, y, x + qr_size_px, y + qr_size_px], outline='black', width=1)
                    
                    # Add filename
                    filename = qr_file.stem
                    if len(filename) > 28:
                        filename = filename[:25] + "..."
                    draw.text((x + 5, y + qr_size_px - 20), filename, fill='black', font=font)
                    
                    qr_index += 1
                    
                except Exception as e:
                    print(f"⚠️  Warning: Could not process {qr_file.name}: {e}")
                    qr_index += 1
        
        pages.append(page_img)
    
    # Save as PDF
    if pages:
        pages[0].save(output_file, save_all=True, append_images=pages[1:])
        
        print(f"{'='*60}")
        print(f"✅ PDF successfully created!")
        print(f"{'='*60}")
        print(f"📄 Filename: {output_file}")
        print(f"📊 Total pages: {len(pages)}")
        print(f"📦 Total QR codes: {len(qr_files)}")
        print(f"{'='*60}\n")
        
        return True
    else:
        print(f"❌ Error: No pages created")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate PDF with QR codes in grid layout"
    )
    parser.add_argument(
        "--qr-dir",
        default="qr_codes",
        help="Directory containing QR code PNG files (default: qr_codes)"
    )
    parser.add_argument(
        "--output",
        default="qr_codes_grid.pdf",
        help="Output PDF filename (default: qr_codes_grid.pdf)"
    )
    
    args = parser.parse_args()
    
    success = create_qr_code_pdf(args.qr_dir, args.output)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
