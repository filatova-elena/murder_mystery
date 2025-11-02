#!/usr/bin/env python3
"""
Generate a PDF with all photographs from clue_images/
Layout: 2 photos per page in 4x6 inch frames
No QR codes
"""

from pathlib import Path
from PIL import Image

# Page dimensions (in inches, 72 DPI)
PAGE_WIDTH = 8.5
PAGE_HEIGHT = 11
DPI = 72
PAGE_W_PX = int(PAGE_WIDTH * DPI)
PAGE_H_PX = int(PAGE_HEIGHT * DPI)

# Photo frame dimensions (in inches, converted to pixels)
FRAME_WIDTH = 4  # inches
FRAME_HEIGHT = 6  # inches
FRAME_W_PX = int(FRAME_WIDTH * DPI)
FRAME_H_PX = int(FRAME_HEIGHT * DPI)

# Page margins
MARGIN_TOP = int(0.5 * DPI)
MARGIN_BOTTOM = int(0.5 * DPI)

# Photos per page
PHOTOS_PER_PAGE = 2

# Photo files
PHOTO_FILES = [
    'photograph_eleanor_baby.png',
    'photograph_eleanor_child.png',
    'photograph_eleanor_adolescent.png',
    'romano_family_photo_harbor.png',
    'romano_family_photograph2_at_home.png',
]

def load_photograph(photo_filename):
    """Load photograph from clue_images/"""
    photo_path = Path(f'assets/clue_images/{photo_filename}')
    if photo_path.exists():
        return Image.open(photo_path)
    return None

def create_photo_frame(photo):
    """
    Create a 4x6 photo frame with centered photo
    White background
    """
    # Create frame
    frame = Image.new('RGB', (FRAME_W_PX, FRAME_H_PX), color='white')
    
    if photo is not None:
        # Convert photo to RGB if needed
        photo_rgb = photo.copy()
        if photo_rgb.mode != 'RGB':
            photo_rgb = photo_rgb.convert('RGB')
        
        # Resize photo to fit in frame while maintaining aspect ratio
        photo_rgb.thumbnail((FRAME_W_PX - 20, FRAME_H_PX - 20), Image.Resampling.LANCZOS)
        
        # Center photo in frame
        photo_x = (FRAME_W_PX - photo_rgb.width) // 2
        photo_y = (FRAME_H_PX - photo_rgb.height) // 2
        
        # Paste photo
        frame.paste(photo_rgb, (photo_x, photo_y))
    
    return frame

def main():
    """Generate photographs PDF"""
    
    print("="*70)
    print("📷 Photographs PDF Generator (4x6 Layout)")
    print("   2 photos per page")
    print("="*70)
    
    print(f"\nProcessing {len(PHOTO_FILES)} photographs...\n")
    
    # Create list to hold page images
    pages = []
    current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='white')
    
    # Calculate positions for 2 frames per page (vertically stacked)
    frame_spacing = 20  # pixels between frames
    total_frames_height = (FRAME_H_PX * 2) + frame_spacing
    start_y = (PAGE_H_PX - total_frames_height) // 2
    frame_x = (PAGE_W_PX - FRAME_W_PX) // 2
    
    photo_positions = [
        (frame_x, start_y),                           # Top frame
        (frame_x, start_y + FRAME_H_PX + frame_spacing)  # Bottom frame
    ]
    
    frame_index = 0
    
    for filename in PHOTO_FILES:
        photo_name = filename.replace('.png', '')
        print(f"📷 {photo_name:<45}", end=" ")
        
        try:
            # Load photograph
            photo = load_photograph(filename)
            if photo is None:
                print("❌ Not found")
                continue
            
            # Create photo frame
            frame = create_photo_frame(photo)
            
            # Determine which position on page
            position_index = frame_index % PHOTOS_PER_PAGE
            
            if position_index == 0 and frame_index > 0:
                # Start new page
                pages.append(current_page)
                current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='white')
            
            # Paste frame on current page
            frame_x_pos, frame_y_pos = photo_positions[position_index]
            current_page.paste(frame, (frame_x_pos, frame_y_pos))
            
            frame_index += 1
            print("✅")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Add final page
    if frame_index > 0:
        pages.append(current_page)
    
    # Save as PDF
    print(f"\n📄 Saving PDF with {len(pages)} pages...")
    if pages:
        pages[0].save(
            'photographs.pdf',
            'PDF',
            save_all=True,
            append_images=pages[1:] if len(pages) > 1 else []
        )
        print(f"✅ Saved: photographs.pdf")
    
    print("\n" + "="*70)
    print(f"✅ Complete!")
    print(f"   Total photographs: {len(PHOTO_FILES)}")
    print(f"   Total pages: {len(pages)}")
    print(f"   File: photographs.pdf")
    print(f"   Features:")
    print(f"   - 4x6 inch photo frames")
    print(f"   - 2 photos per page")
    print(f"   - Centered photos")
    print(f"   - Clean layout (no QR codes)")
    print("="*70)

if __name__ == "__main__":
    main()
