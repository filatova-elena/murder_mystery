# QR Code Generator for Murder Mystery

This script generates QR codes that link to different clues and investigation materials in the Murder Mystery game.

## Installation

1. Install the required dependencies:
```bash
pip install -r qr_requirements.txt
```

## Usage

### Generate All QR Codes
```bash
python generate_qr_codes.py
```
This generates QR codes for all botanicals, documents, and characters.

### Generate Specific Types

**Botanical Clues:**
```bash
python generate_qr_codes.py --type botanicals
```

**Document Clues:**
```bash
python generate_qr_codes.py --type documents
```

**Character Pages:**
```bash
python generate_qr_codes.py --type characters
```

### Generate Custom QR Code
```bash
python generate_qr_codes.py --type custom --url "https://example.com" --name "my_custom_qr"
```

### Specify Output Directory
```bash
python generate_qr_codes.py --output /path/to/output
```

### Use Custom Base URL
```bash
python generate_qr_codes.py --base-url "https://yourdomain.com/murder-mystery"
```

## Output

All QR codes are saved as PNG images in the `qr_codes/` directory (or your specified output directory).

File naming convention:
- `botanical_{name}.png` - Links to botanical clue pages
- `document_{name}.png` - Links to document pages
- `character_{name}.png` - Links to character pages

## Using the QR Codes

You can:
1. **Print them** for a physical murder mystery game
2. **Display them** on screens during gameplay
3. **Share them** digitally with players
4. **Embed them** in clue cards or puzzles

When scanned, they'll link directly to the investigation materials on your hosted GitHub Pages site.

## Example Workflow

```bash
# Install dependencies
pip install -r qr_requirements.txt

# Generate all QR codes in organized folders
mkdir -p qr_codes/{botanicals,documents,characters}
python generate_qr_codes.py --type botanicals --output qr_codes/botanicals
python generate_qr_codes.py --type documents --output qr_codes/documents
python generate_qr_codes.py --type characters --output qr_codes/characters

# Now print or use the QR codes!
```

## Troubleshooting

**ImportError: No module named 'qrcode'**
- Run: `pip install -r qr_requirements.txt`

**Permission denied when saving**
- Ensure the output directory exists and you have write permissions
- Or specify a different output directory with `--output`

**QR Code won't scan**
- Make sure the base URL is correct
- Check that the linked pages exist and are accessible
- Try scanning with different QR code readers
