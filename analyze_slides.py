"""
Analyze slide images to extract text and layout information
"""
from PIL import Image
import pytesseract
import os
from pathlib import Path
import json

# Set tesseract path (you may need to adjust this)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def analyze_slide(slide_path):
    """Analyze a single slide image"""
    img = Image.open(slide_path)
    
    # Get image properties
    width, height = img.size
    
    # Try to extract text using OCR
    try:
        text = pytesseract.image_to_string(img)
    except Exception as e:
        text = f"OCR Error: {str(e)}"
    
    # Basic analysis of image colors to determine background
    # Sample pixels from different regions
    pixels = img.load()
    sample_points = [
        (10, 10),  # top-left
        (width//2, height//2),  # center
        (width-10, 10),  # top-right
    ]
    
    brightness_values = []
    for x, y in sample_points:
        try:
            pixel = pixels[x, y]
            if isinstance(pixel, tuple) and len(pixel) >= 3:
                # Calculate brightness
                brightness = sum(pixel[:3]) / 3
                brightness_values.append(brightness)
        except:
            pass
    
    avg_brightness = sum(brightness_values) / len(brightness_values) if brightness_values else 128
    background_type = "light" if avg_brightness > 128 else "dark"
    
    return {
        "dimensions": f"{width}x{height}",
        "background": background_type,
        "text": text,
        "brightness": avg_brightness
    }

def main():
    slides_dir = Path(r"c:\Users\user\OneDrive\Merck\Athinia\Slide Makers\ath_slide_generator\ath_ppt_generator\output\jpgs\knime_converter_presentation")
    
    results = {}
    
    for i in range(1, 16):
        slide_file = slides_dir / f"Slide{i}.JPG"
        if slide_file.exists():
            print(f"Processing {slide_file.name}...")
            results[f"Slide{i}"] = analyze_slide(slide_file)
        else:
            print(f"Slide{i}.JPG not found")
    
    # Save results
    output_file = Path(r"c:\Users\user\OneDrive\Merck\Athinia\Slide Makers\ath_slide_generator\ath_ppt_generator\slide_analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nAnalysis complete! Results saved to {output_file}")
    
    # Also print a summary
    print("\n=== SUMMARY ===")
    for slide_name, data in sorted(results.items()):
        print(f"\n{slide_name}:")
        print(f"  Background: {data['background']}")
        print(f"  Dimensions: {data['dimensions']}")
        print(f"  Text preview: {data['text'][:200]}...")

if __name__ == "__main__":
    main()
