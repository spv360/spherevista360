# Favicon Setup Guide for SphereVista360

## Files Needed:
- `favicon.ico` (16x16, 32x32, 48x48 pixels)
- `apple-touch-icon.png` (180x180 pixels)

## How to Create These Files:

### Option 1: Use Online Tools
1. Go to https://favicon.io/favicon-generator/
2. Upload your logo or create a simple icon
3. Download the generated favicon.ico and apple-touch-icon.png

### Option 2: Use Image Editor
1. Create a square logo/icon (at least 512x512 pixels)
2. Use tools like:
   - GIMP (free)
   - Photoshop
   - Online favicon generators

### Option 3: Convert Existing Logo
If you have a logo file, convert it using:
- https://favicon.io/favicon-converter/
- https://www.favicon-generator.org/

## File Specifications:
- favicon.ico: Multi-size ICO file (16x16, 32x32, 48x48)
- apple-touch-icon.png: 180x180 PNG with transparency

## WordPress Integration:
Add this code to your theme's header.php or use a plugin:

```html
<!-- Favicon -->
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="shortcut icon" href="/favicon.ico">

<!-- Apple Touch Icon -->
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
```

## Placement:
Place both files in your WordPress root directory:
/home/kddevops/projects/spherevista360/