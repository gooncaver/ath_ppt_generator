"""
Test script to demonstrate the manual export workflow
"""

from pathlib import Path
import json

# Simulate the manual export workflow
presentation_file = "output/knime_converter_guide.pptx"
export_dir = Path("output/knime_converter_guide_slides")
export_dir.mkdir(exist_ok=True)

# Create metadata
metadata = {
    "presentation_file": presentation_file,
    "num_slides": 15,
    "export_directory": str(export_dir.absolute()),
    "expected_files": [f"Slide{i+1}.PNG" for i in range(15)],
    "instructions": "Manual export workflow demonstration"
}

metadata_file = export_dir / "review_metadata.json"
with open(metadata_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)

print("="*70)
print("MANUAL EXPORT WORKFLOW TEST")
print("="*70)
print(f"\nMetadata saved to: {metadata_file}")
print(f"\nMetadata contents:")
print(json.dumps(metadata, indent=2))
print("\n" + "="*70)
print("EXPORT INSTRUCTIONS")
print("="*70)
print(f"\n1. Open: {Path(presentation_file).absolute()}")
print(f"\n2. File > Export > PNG")
print(f"\n3. Select 'All Slides'")
print(f"\n4. Save to: {export_dir.absolute()}")
print(f"\n5. Expected files: Slide1.PNG, Slide2.PNG, ..., Slide15.PNG")
print("\n" + "="*70)

# Check if files exist
existing_files = list(export_dir.glob("Slide*.PNG"))
if existing_files:
    print(f"\n✓ Found {len(existing_files)} slide images:")
    for f in sorted(existing_files)[:3]:
        print(f"  - {f.name}")
    if len(existing_files) > 3:
        print(f"  ... and {len(existing_files) - 3} more")
else:
    print("\n✗ No slide images found yet. Please export manually.")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
