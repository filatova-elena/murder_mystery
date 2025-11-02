#!/usr/bin/env python3
"""
Generate a PDF document with all game documents
QR codes overlaid in the center to cover incorrect AI-generated text
Layout: Full page or half page depending on document size
Uses real artifact image for treasure map instead of AI-generated
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw
import math

# Page dimensions (in inches, 72 DPI)
PAGE_WIDTH = 8.5
PAGE_HEIGHT = 11
DPI = 72
PAGE_W_PX = int(PAGE_WIDTH * DPI)
PAGE_H_PX = int(PAGE_HEIGHT * DPI)

def load_documents():
    """Load documents from documents.json"""
    with open('data/documents.json', 'r') as f:
        data = json.load(f)
    return data.get('documents', [])

def load_document_image(doc_id: str):
    """Load document image from assets/clue_images_documents/"""
    # Special case: use real treasure map artifact instead of AI-generated
    if doc_id == 'treasure_map_hand_drawn':
        image_path = Path('assets/treasure_map.jpg')
        if image_path.exists():
            return Image.open(image_path)
    
    image_path = Path(f'assets/clue_images_documents/{doc_id}.png')
    if image_path.exists():
        return Image.open(image_path)
    return None

def load_qr_code(doc_id: str):
    """Load QR code from qr_codes/"""
    qr_path = Path(f'qr_codes/document_{doc_id}.png')
    if qr_path.exists():
        return Image.open(qr_path)
    return None

def create_document_with_qr(doc_image, qr_code, doc_id: str):
    """
    Create a document image with QR code overlay in the center
    QR code covers at least 1/3 of the document
    """
    if doc_image is None:
        return None
    
    # Work with a copy
    doc_img = doc_image.copy()
    
    # Convert to RGB if necessary (for JPG files)
    if doc_img.mode != 'RGB':
        doc_img = doc_img.convert('RGB')
    
    # Calculate QR code size (should cover 1/3 of document)
    doc_width = doc_img.width
    doc_height = doc_img.height
    
    # QR code should be ~1/3 of the smaller dimension
    qr_size = int(min(doc_width, doc_height) / 2.5)
    
    if qr_code is not None:
        # Resize QR code
        qr = qr_code.copy()
        qr.thumbnail((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        # Center QR code on document
        qr_x = (doc_width - qr.width) // 2
        qr_y = (doc_height - qr.height) // 2
        
        # Paste QR code
        doc_img.paste(qr, (qr_x, qr_y))
    
    return doc_img

def determine_layout(doc_image):
    """
    Determine if document should be full page or half page
    Return: ('full', height) or ('half', height)
    """
    if doc_image is None:
        return ('full', PAGE_H_PX)
    
    # Calculate aspect ratio
    width = doc_image.width
    height = doc_image.height
    aspect_ratio = width / height if height > 0 else 1
    
    # If it's roughly letter-sized (8.5x11 aspect), use full page
    letter_ratio = PAGE_WIDTH / PAGE_HEIGHT  # ~0.77
    
    if abs(aspect_ratio - letter_ratio) < 0.15:  # Within 15% of letter ratio
        return ('full', PAGE_H_PX)
    else:
        return ('half', PAGE_H_PX // 2)

def main():
    """Generate documents PDF"""
    
    print("="*70)
    print("📄 Game Documents PDF Generator")
    print("   With QR Code Overlays")
    print("   Using Real Artifact for Treasure Map")
    print("="*70)
    
    documents = load_documents()
    print(f"\nProcessing {len(documents)} documents...\n")
    
    # Create list to hold page images
    pages = []
    current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='white')
    current_y = 0
    
    for i, doc in enumerate(documents, 1):
        doc_id = doc['id']
        title = doc['title']
        
        print(f"Doc {i:2d}: {title:<50}", end=" ")
        
        try:
            # Load document image
            doc_img = load_document_image(doc_id)
            if doc_img is None:
                print("❌ Image not found")
                continue
            
            # Load QR code
            qr_code = load_qr_code(doc_id)
            
            # Create document with QR overlay
            doc_with_qr = create_document_with_qr(doc_img, qr_code, doc_id)
            if doc_with_qr is None:
                print("❌ Failed to create document")
                continue
            
            # Determine layout
            layout, layout_height = determine_layout(doc_with_qr)
            
            # Resize document to fit page
            if layout == 'full':
                # Full page
                max_width = PAGE_W_PX - 40  # 20px margin on each side
                max_height = PAGE_H_PX - 40
            else:
                # Half page
                max_width = PAGE_W_PX - 40
                max_height = (PAGE_H_PX // 2) - 30
            
            # Resize maintaining aspect ratio
            doc_with_qr.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Check if document fits on current page
            if layout == 'full':
                # Full page document
                if current_y > 0:
                    # Start new page
                    pages.append(current_page)
                    current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='white')
                    current_y = 0
                
                # Center document on page
                doc_x = (PAGE_W_PX - doc_with_qr.width) // 2
                doc_y = (PAGE_H_PX - doc_with_qr.height) // 2
                current_page.paste(doc_with_qr, (doc_x, doc_y))
                
                # Add page and start new one
                pages.append(current_page)
                current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='white')
                current_y = 0
                
                is_real = " (Real Artifact)" if doc_id == 'treasure_map_hand_drawn' else ""
                print(f"✅ (Full page){is_real}")
            else:
                # Half page document
                if current_y + doc_with_qr.height + 30 > PAGE_H_PX:
                    # Start new page
                    pages.append(current_page)
                    current_page = Image.new('RGB', (PAGE_W_PX, PAGE_H_PX), color='white')
                    current_y = 0
                
                # Center horizontally, position vertically
                doc_x = (PAGE_W_PX - doc_with_qr.width) // 2
                doc_y = current_y + 15
                current_page.paste(doc_with_qr, (doc_x, doc_y))
                current_y = doc_y + doc_with_qr.height + 15
                
                is_real = " (Real Artifact)" if doc_id == 'treasure_map_hand_drawn' else ""
                print(f"✅ (Half page){is_real}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Add final page if it has content
    if current_y > 0:
        pages.append(current_page)
    
    # Save as PDF
    print(f"\n📄 Saving PDF with {len(pages)} pages...")
    if pages:
        pages[0].save(
            'documents_visual.pdf',
            'PDF',
            save_all=True,
            append_images=pages[1:] if len(pages) > 1 else []
        )
        print(f"✅ Saved: documents_visual.pdf")
    
    print("\n" + "="*70)
    print(f"✅ Complete!")
    print(f"   Total documents: {len(documents)}")
    print(f"   Total pages: {len(pages)}")
    print(f"   File: documents_visual.pdf")
    print(f"   Features:")
    print(f"   - Document images with QR code overlays")
    print(f"   - QR codes cover incorrect AI text")
    print(f"   - Treasure Map uses real artifact image")
    print(f"   - Scan QR to see correct information")
    print(f"   - Full/half page layouts")
    print("="*70)

if __name__ == "__main__":
    main()
