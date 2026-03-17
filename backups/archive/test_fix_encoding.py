#!/usr/bin/env python3
import ftfy

test_cases = [
    "MĂ‰XICO", 
    "investigaciĂłn", 
    "M├®xico", 
    "intent├│",
    "Secretar√≠a",
    "RepГәblica",
    "aГұo"
]

for tc in test_cases:
    print(f"Original: {tc} -> Fixed: {ftfy.fix_text(tc)}")
