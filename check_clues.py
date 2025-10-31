import os
import re
from pathlib import Path

# Get all HTML files in clue folder (excluding clues.html and template.html)
clue_dir = Path("clue")
all_html_files = set()

for root, dirs, files in os.walk(clue_dir):
    for file in files:
        if file.endswith('.html') and file not in ['clues.html', 'template.html']:
            # Get relative path
            rel_path = Path(root) / file
            rel_path = str(rel_path).replace('clue/', '')
            all_html_files.add(rel_path)

# Read clues.html and extract all href links
with open('clue/clues.html', 'r') as f:
    content = f.read()
    
# Find all href attributes
href_pattern = r'href="([^"]+)"'
linked_files = set()
for match in re.finditer(href_pattern, content):
    link = match.group(1)
    # Clean up the link (remove ../ and leading ./)
    link = link.replace('../', '').replace('./', '')
    linked_files.add(link)

# Find missing links
missing_links = all_html_files - linked_files
extra_links = linked_files - all_html_files

print("=" * 60)
print("CLUE LINKING ANALYSIS")
print("=" * 60)

if missing_links:
    print(f"\n❌ MISSING LINKS ({len(missing_links)} files):")
    print("These HTML files in clue/ are NOT linked in clues.html:\n")
    for file in sorted(missing_links):
        print(f"  - clue/{file}")
else:
    print("\n✅ All HTML files have links in clues.html!")

print(f"\nTotal files in clue folder (excluding clues.html & template.html): {len(all_html_files)}")
print(f"Total files linked in clues.html: {len(linked_files)}")

