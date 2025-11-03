#!/usr/bin/env python3
"""
Upload Loan EMI Calculator files to web server
This script helps upload the calculator files to the web server
"""

import os
import sys
import shutil
from pathlib import Path


def create_upload_package():
    """Create a zip package of the calculator files for upload"""

    calculator_dir = Path("tools/calculators/loan_emi_calculator")
    if not calculator_dir.exists():
        print("❌ Calculator directory not found")
        return False

    # Create upload directory
    upload_dir = Path("upload_package")
    upload_dir.mkdir(exist_ok=True)

    # Files to upload (only the essential ones)
    essential_files = [
        "loan_emi_calculator.html",  # Main calculator interface
        "loan_emi_calculator.py",    # Backend logic (for API if needed)
        "README.md"                  # Documentation
    ]

    print("📦 Creating upload package...")

    for file in essential_files:
        src = calculator_dir / file
        if src.exists():
            shutil.copy2(src, upload_dir / file)
            print(f"✅ Copied {file}")
        else:
            print(f"⚠️  {file} not found")

    # Create a simple .htaccess if needed
    htaccess_content = """# Allow access to calculator files
<Files "*.html">
    Allow from all
</Files>

# Prevent access to Python files
<Files "*.py">
    Order deny,allow
    Deny from all
</Files>
"""

    with open(upload_dir / ".htaccess", "w") as f:
        f.write(htaccess_content)

    print("✅ Created .htaccess file")

    # Create upload instructions
    instructions = f"""
# Upload Instructions for Loan EMI Calculator

## Files to Upload:
Upload the following files to: /public_html/tools/calculators/loan_emi_calculator/

{chr(10).join(f"- {file}" for file in essential_files + ['.htaccess'])}

## Directory Structure:
```
/public_html/
├── tools/
│   └── calculators/
│       └── loan_emi_calculator/
│           ├── loan_emi_calculator.html  ← Main calculator interface
│           ├── loan_emi_calculator.py    ← Backend logic
│           ├── README.md                 ← Documentation
│           └── .htaccess                 ← Security settings
```

## Verification:
After upload, test these URLs:
- https://spherevista360.com/tools/calculators/loan_emi_calculator/loan_emi_calculator.html
- https://spherevista360.com/loan-emi-calculator/

## FTP Upload:
Use your hosting control panel or FTP client to upload these files.
"""

    with open(upload_dir / "UPLOAD_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)

    print("✅ Created upload instructions")

    # Create zip archive
    zip_name = "loan_emi_calculator_upload.zip"
    shutil.make_archive("loan_emi_calculator_upload", 'zip', upload_dir)

    print(f"✅ Created {zip_name}")

    print(f"\n📁 Upload package created in: {upload_dir.absolute()}")
    print(f"📦 Zip archive: {zip_name}")

    return True


def main():
    """Main function"""
    print("📤 Loan EMI Calculator Upload Package Creator")
    print("=" * 50)

    if create_upload_package():
        print("\n✅ Upload package created successfully!")
        print("\n📋 Next steps:")
        print("1. Upload the files from 'upload_package/' directory to your web server")
        print("2. Place them in: /public_html/tools/calculators/loan_emi_calculator/")
        print("3. Test the calculator at: https://spherevista360.com/loan-emi-calculator/")
        print("\n📦 Or use the zip file 'loan_emi_calculator_upload.zip' for easy upload")
    else:
        print("❌ Failed to create upload package")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())