#!/usr/bin/env python3
"""
Generate images of all documents from the game
Based on document descriptions
"""

import os
import sys
import json
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai

def load_documents():
    """Load documents from documents.json"""
    with open('data/documents.json', 'r') as f:
        data = json.load(f)
    return data.get('documents', [])

def create_document_prompt(doc_id: str, title: str, doc_type: str, details: str) -> str:
    """Create a detailed image prompt based on document details"""
    
    prompts = {
        'death_cert_alice': """Create a vintage death certificate document from 1925. 
            Official government document style with typed text and official stamps.
            For Alice Whitmore, dated October 7, 1925.
            Signed by Dr. Thaddeus Crane.
            Black and white, aged paper appearance.
            Shows "Cause of Death" section with formal medical language.
            Includes official seals and signatures.
            Vintage form layout typical of 1920s documents.""",
        
        'death_cert_sebastian': """Create a vintage death certificate document from 1925.
            Official Long Beach government document.
            For Sebastian Crane, dated October 12-13, 1925.
            Signed by Dr. Thaddeus Crane.
            Shows suspicion of poisoning with vague official cause.
            Black and white, aged parchment paper.
            Official stamps, signature lines, typed information.
            Typical 1920s death certificate format.""",
        
        'death_cert_cordelia': """Create a vintage death certificate document from 1925.
            Official government death certificate form.
            For Cordelia Montrose, dated October 18, 1925.
            Signed by Dr. Thaddeus Crane.
            Medical examination section shows cumulative toxin damage.
            Black and white, aged document appearance.
            Official seals and stamps visible.
            1920s government form style.""",
        
        'autopsy_alice': """Create a vintage autopsy report document from 1925.
            Medical examination record on official form.
            Prepared by Silas Blackwell, Mortician, October 8, 1925.
            Shows physical examination findings.
            References to blunt force trauma and skull examination.
            Black and white, medical document format.
            Handwritten notes and typed sections.
            Signs of correction or redaction visible.
            Vintage mortuary report style.""",
        
        'autopsy_sebastian': """Create a vintage autopsy report document from 1925.
            Medical/mortuary examination record.
            By Silas Blackwell, dated October 14, 1925.
            Shows body examination findings.
            References to poisoning and organ tissue analysis.
            Evidence of handwritten corrections or strikes through text.
            Black and white aged parchment.
            Medical terminology and measurements.
            Cover-up evident in revisions.""",
        
        'autopsy_cordelia': """Create a vintage autopsy report document from 1925.
            Medical examination form, October 19, 1925.
            Silas Blackwell mortician examination.
            Shows examination of female body.
            References to cumulative toxin effects.
            Black and white, medical document format.
            Handwritten notes visible.
            Evidence of redaction or censoring.
            Vintage 1920s mortuary report.""",
        
        'prenup_agreement': """Create a vintage legal document from 1925 - a pre-nuptial agreement.
            Formal legal contract on parchment paper.
            Multiple pages with legal language and paragraphs.
            Dates and signatures at bottom.
            Property and inheritance clause visible.
            Legal terminology from 1920s era.
            Black and white, official legal document style.
            Shows wealthy family legal protection.""",
        
        'payment_records': """Create a vintage accounting document from 1925.
            Payment ledger or financial record sheet.
            Shows rows of handwritten or typed transactions.
            Amounts in columns, dates visible.
            Could show payments to mortician or other services.
            Black and white, aged paper.
            Accounting notation and figures.
            Official financial records format.""",
        
        'romano_shipping': """Create a vintage shipping company document from the 1920s.
            Harbor Import & Trading Co. business record.
            Shows shipping information and cargo details.
            Manifest-style layout with typed information.
            Dates and quantities listed.
            Business letterhead visible.
            Black and white, commercial document format.
            Evidence of legitimate shipping business.""",
        
        'trust_records': """Create a vintage trust/estate document from early 20th century.
            Legal financial document on parchment.
            Shows trust establishment and inheritance details.
            Montrose family trust documentation.
            Legal language and beneficiary information.
            Signatures and official notary marks.
            Black and white, formal legal document.
            Shows wealth management.""",
        
        'name_change_docs': """Create a vintage legal name change document from 1960s.
            Official government form for surname change.
            Crane family name change to Sinclair.
            Court-issued documentation.
            States official reason for change.
            Black and white, legal court document format.
            Signatures and court seals visible.
            Shows formal legal process.""",
        
        'shipping_manifests_romano': """Create a vintage shipping manifest document from 1920s.
            Detailed cargo manifest from Harbor Import & Trading Co.
            Lists items being shipped with notations.
            Shows quantities and destinations.
            Some items have coded or hidden notations.
            Black and white, commercial shipping document.
            Typed form with handwritten additions.
            Evidence of organized smuggling operation.""",
        
        'marriage_certificate_dimarco': """Create a vintage marriage certificate from early 20th century.
            Legal marriage document, formal style.
            Shows marriage between two parties.
            Official government document with seals.
            Bride and groom information listed.
            Date and location of marriage.
            Black and white, aged parchment.
            Official signatures and stamps visible.""",
        
        'bank_statement_fragments': """Create a vintage bank statement document from post-1960s.
            Bank of America or similar institution statement.
            Shows fragmented or torn pages.
            Account information partially visible.
            Transaction details and amounts.
            Shows financial activity over time.
            Black and white aged paper.
            Some sections appear intentionally obscured.""",
        
        'boat_registration_marina': """Create a vintage marine registry document from early 20th century.
            Official boat/vessel registration form.
            For ship named 'La Stella Nuova'.
            Shows vessel specifications and ownership.
            Registry numbers and classification.
            Black and white, maritime official document.
            Shows connection to Harbor Import & Trading Co.""",
        
        'treasure_map_hand_drawn': """Create a vintage hand-drawn map document from 1925.
            Faded aged parchment with hand-drawn markings.
            Shows estate grounds layout with measurements.
            Rose garden location specifically marked.
            Contains handwritten notes and distance notations.
            Appears to show burial or hidden location.
            Black and white, aged paper with ink markings.
            Military-style surveying measurements visible.""",
    }
    
    if doc_id in prompts:
        return prompts[doc_id]
    
    # Default prompt for unknown documents
    return f"""Create a vintage document image from the 1920s-1960s era for: {title}
    Style: {doc_type}
    Make it look like an authentic historical document.
    Black and white, aged paper appearance.
    Include appropriate text, signatures, and official markings.
    Vintage document format appropriate to its type."""

def generate_document_image(doc_id: str, title: str, output_filename: str = None):
    """
    Generate a document image
    
    Args:
        doc_id: ID of the document
        title: Title of the document
        output_filename: Optional custom output filename
    
    Returns:
        Path to saved image or None if failed
    """
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: GEMINI_API_KEY not set in .env file")
        return None
    
    if output_filename is None:
        output_filename = f'{doc_id}.png'
    
    output_path = Path('assets/clue_images_documents') / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"📄 {title:<50}", end=" ")
        sys.stdout.flush()
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        prompt = create_document_prompt(doc_id, title, "", "")
        response = model.generate_content([prompt])
        
        # Extract image data
        if hasattr(response, 'parts'):
            for part in response.parts:
                if hasattr(part, 'inline_data'):
                    inline_data = part.inline_data
                    if inline_data and hasattr(inline_data, 'data'):
                        img_data = inline_data.data
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_data)
                        
                        print(f"✅ ({len(img_data)/(1024**2):.1f}MB)")
                        return output_path
        
        print("❌ No image in response")
        return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Generate all document images"""
    
    print("="*70)
    print("📄 Document Image Generator")
    print("   Creating vintage document visuals")
    print("="*70)
    
    documents = load_documents()
    print(f"\nGenerating {len(documents)} document images...\n")
    
    successful = 0
    failed = 0
    
    for i, doc in enumerate(documents, 1):
        result = generate_document_image(doc['id'], doc['title'])
        if result:
            successful += 1
        else:
            failed += 1
        
        # Rate limiting: wait between requests
        if i < len(documents):
            time.sleep(2)  # 2 second delay between requests
    
    print("\n" + "="*70)
    print(f"✅ Complete! Generated {successful}/{len(documents)} document images")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    print(f"📁 Location: assets/clue_images_documents/")
    print("="*70)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
