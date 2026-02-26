#!/usr/bin/env python3

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))

# Update CSS references in site HTML files
for i in range(1, 10):
    site_file = SITES_DIR / f"site{i}.html"
    
    if site_file.exists():
        with open(site_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the CSS reference to be relative to the site's directory
        # Change from "../templates/css/templateX.css" to "./templates/css/templateX.css" 
        # or just "templates/css/templateX.css"
        updated_content = re.sub(
            r'href="\.\./templates/css/template\d+\.css"',
            f'href="templates/css/template{i}.css"',
            content
        )
        
        # Write the updated content back
        with open(site_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated {site_file} to use templates/css/template{i}.css")

print("All site HTML files have been updated with correct CSS references.")
