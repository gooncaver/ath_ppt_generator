"""
Detailed slide analysis using computer vision
"""
from PIL import Image
import numpy as np
from pathlib import Path
import json

def analyze_slide_detailed(slide_path):
    """Detailed analysis of a slide image"""
    img = Image.open(slide_path)
    
    # Convert to numpy array for analysis
    img_array = np.array(img)
    width, height = img.size
    
    # Determine background color (sample from edges)
    edge_samples = []
    # Sample top edge
    edge_samples.extend(img_array[5:15, 5:15].reshape(-1, 3))
    # Sample bottom edge
    edge_samples.extend(img_array[height-15:height-5, 5:15].reshape(-1, 3))
    
    edge_samples = np.array(edge_samples)
    avg_color = np.mean(edge_samples, axis=0)
    avg_brightness = np.mean(avg_color)
    
    background_type = "light" if avg_brightness > 128 else "dark"
    bg_color_rgb = tuple(avg_color.astype(int))
    
    # Analyze content area (center region)
    content_region = img_array[int(height*0.2):int(height*0.9), int(width*0.1):int(width*0.9)]
    
    # Calculate text density by looking for dark text on light bg or light text on dark bg
    if background_type == "light":
        # Look for dark pixels (text)
        text_pixels = np.sum(np.mean(content_region, axis=2) < 100)
    else:
        # Look for light pixels (text)
        text_pixels = np.sum(np.mean(content_region, axis=2) > 155)
    
    total_pixels = content_region.shape[0] * content_region.shape[1]
    content_density = (text_pixels / total_pixels) * 100
    
    # Analyze vertical distribution to estimate number of sections/bullets
    vertical_profile = np.mean(content_region, axis=(1, 2))
    
    # Find regions with content (where brightness differs from background)
    if background_type == "light":
        content_rows = vertical_profile < (avg_brightness - 20)
    else:
        content_rows = vertical_profile > (avg_brightness + 20)
    
    # Count transitions as potential bullet points
    transitions = np.diff(content_rows.astype(int))
    bullet_count_estimate = max(1, np.sum(transitions == 1))
    
    # Analyze title area (top 20%)
    title_region = img_array[int(height*0.05):int(height*0.20), int(width*0.1):int(width*0.9)]
    title_brightness = np.mean(title_region)
    has_distinct_title = abs(title_brightness - avg_brightness) > 30
    
    return {
        "dimensions": f"{width}x{height}",
        "background_type": background_type,
        "background_color_rgb": bg_color_rgb,
        "background_brightness": float(avg_brightness),
        "content_density_pct": round(content_density, 2),
        "estimated_bullets": int(bullet_count_estimate),
        "has_distinct_title": bool(has_distinct_title),
        "verbosity": "High" if content_density > 15 else "Medium" if content_density > 8 else "Low"
    }

def main():
    slides_dir = Path(r"c:\Users\user\OneDrive\Merck\Athinia\Slide Makers\ath_slide_generator\ath_ppt_generator\output\jpgs\knime_converter_presentation")
    
    results = {}
    
    print("=== DETAILED SLIDE ANALYSIS ===\n")
    
    for i in range(1, 16):
        slide_file = slides_dir / f"Slide{i}.JPG"
        if slide_file.exists():
            analysis = analyze_slide_detailed(slide_file)
            results[f"Slide{i}"] = analysis
            
            print(f"Slide {i}:")
            print(f"  Background: {analysis['background_type']} (brightness: {analysis['background_brightness']:.1f})")
            print(f"  Content Density: {analysis['content_density_pct']}% ({analysis['verbosity']})")
            print(f"  Estimated Bullets/Sections: {analysis['estimated_bullets']}")
            print(f"  Has Distinct Title: {analysis['has_distinct_title']}")
            print()
    
    # Save detailed results
    output_file = Path(r"c:\Users\user\OneDrive\Merck\Athinia\Slide Makers\ath_slide_generator\ath_ppt_generator\detailed_slide_analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed analysis saved to {output_file}")
    
    # Summary statistics
    dark_count = sum(1 for r in results.values() if r['background_type'] == 'dark')
    light_count = sum(1 for r in results.values() if r['background_type'] == 'light')
    avg_density = np.mean([r['content_density_pct'] for r in results.values()])
    
    print("\n=== SUMMARY STATISTICS ===")
    print(f"Dark backgrounds: {dark_count}/15 ({dark_count/15*100:.1f}%)")
    print(f"Light backgrounds: {light_count}/15 ({light_count/15*100:.1f}%)")
    print(f"Average content density: {avg_density:.2f}%")
    print(f"Consistency: {'INCONSISTENT' if abs(dark_count - light_count) > 3 else 'CONSISTENT'}")

if __name__ == "__main__":
    main()
