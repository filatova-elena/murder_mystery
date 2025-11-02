#!/usr/bin/env python3
"""
Crop document images to remove dark backgrounds and save ink
Automatically detects and crops dark margins
"""

from PIL import Image
from pathlib import Path

def crop_dark_background(img_path, output_path):
    """
    Crop image to remove dark backgrounds
    Finds the bounding box of non-dark content
    """
    img = Image.open(img_path)
    img_rgb = img.convert('RGB')
    
    width, height = img_rgb.size
    
    # Define dark threshold (RGB values)
    dark_threshold = 80
    
    # Find content bounds by scanning from edges
    left = 0
    right = width
    top = 0
    bottom = height
    
    # Scan from left
    for x in range(width):
        col = img_rgb.crop((x, 0, x+1, height))
        pixels = list(col.getdata())
        avg_brightness = sum(sum(p) for p in pixels) / (len(pixels) * 3)
        if avg_brightness > dark_threshold:
            left = x
            break
    
    # Scan from right
    for x in range(width-1, -1, -1):
        col = img_rgb.crop((x, 0, x+1, height))
        pixels = list(col.getdata())
        avg_brightness = sum(sum(p) for p in pixels) / (len(pixels) * 3)
        if avg_brightness > dark_threshold:
            right = x + 1
            break
    
    # Scan from top
    for y in range(height):
        row = img_rgb.crop((0, y, width, y+1))
        pixels = list(row.getdata())
        avg_brightness = sum(sum(p) for p in pixels) / (len(pixels) * 3)
        if avg_brightness > dark_threshold:
            top = y
            break
    
    # Scan from bottom
    for y in range(height-1, -1, -1):
        row = img_rgb.crop((0, y, width, y+1))
        pixels = list(row.getdata())
        avg_brightness = sum(sum(p) for p in pixels) / (len(pixels) * 3)
        if avg_brightness > dark_threshold:
            bottom = y + 1
            break
    
    # Add small margin
    margin = 10
    left = max(0, left - margin)
    right = min(width, right + margin)
    top = max(0, top - margin)
    bottom = min(height, bottom + margin)
    
    # Crop
    cropped = img_rgb.crop((left, top, right, bottom))
    cropped.save(output_path)
    
    return cropped.size, (width, height)

def main():
    """Crop all document images with dark backgrounds"""
    
    print("="*70)
    print("✂️ Document Image Cropper")
    print("   Removing dark backgrounds to save ink")
    print("="*70 + "\n")
    
    doc_folder = Path('assets/clue_images_documents')
    
    # Documents to crop (manually identified or based on user feedback)
    documents_to_check = list(doc_folder.glob('*.png'))
    
    cropped_count = 0
    skipped_count = 0
    
    for img_path in sorted(documents_to_check):
        try:
            original_size, new_size = crop_dark_background(img_path, img_path)
            
            if original_size != new_size:
                percentage = ((new_size[0] * new_size[1]) / (original_size[0] * original_size[1])) * 100
                print(f"✂️ {img_path.name:<40} ({percentage:.0f}% of original size)")
                cropped_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"❌ {img_path.name:<40} Error: {e}")
    
    print("\n" + "="*70)
    print(f"✅ Complete!")
    print(f"   Cropped: {cropped_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"   Ink savings: Significant reduction in dark background printing")
    print("="*70)

if __name__ == "__main__":
    main()
