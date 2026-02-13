"""
Run holistic review on exported slides using metadata
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm.client import LLMClient
from src.llm.holistic_reviewer import HolisticReviewer

def main():
    # Load metadata
    metadata_path = Path('output/knime_converter_slides/review_metadata.json')
    
    if not metadata_path.exists():
        print(f"Error: Metadata file not found: {metadata_path}")
        return
    
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Get slide images
    slide_dir = Path('output/knime_converter_slides')
    slide_images = sorted([str(p) for p in slide_dir.glob('Slide*.JPG')] + 
                         [str(p) for p in slide_dir.glob('Slide*.PNG')])
    
    if not slide_images:
        print(f"Error: No slides found in {slide_dir}")
        return
    
    print(f"{'='*70}")
    print(f"HOLISTIC PRESENTATION REVIEW")
    print(f"{'='*70}")
    print(f"\nFound {len(slide_images)} slides to review")
    print(f"Slide directory: {slide_dir}")
    print(f"Presentation: {metadata['presentation_file']}")
    print(f"\nStarting GPT-5 Vision review...\n")
    
    # Create LLM client and reviewer
    llm_client = LLMClient()
    reviewer = HolisticReviewer(llm_client)
    
    try:
        results = reviewer.review_presentation(
            slide_images=slide_images,
            original_content=metadata['original_content'],
            outline=metadata['outline']
        )
        
        print(f"\n{'='*70}")
        print(f"REVIEW COMPLETE")
        print(f"{'='*70}\n")
        
        # Save results
        results_path = slide_dir / 'review_results.json'
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {results_path}")
        
        # Display summary
        if 'slides' in results:
            print(f"\nReviewed {len(results['slides'])} slides")
            for slide_result in results['slides']:
                print(f"\n  Slide {slide_result.get('slide_number', '?')}:")
                print(f"    Score: {slide_result.get('score', 'N/A')}/10")
                if 'issues' in slide_result and slide_result['issues']:
                    print(f"    Issues: {len(slide_result['issues'])}")
                    for issue in slide_result['issues'][:3]:  # Show first 3
                        print(f"      - {issue}")
        
        if 'overall_feedback' in results:
            print(f"\n  Overall Feedback:")
            print(f"    {results['overall_feedback'][:200]}...")
        
    except Exception as e:
        print(f"\n[ERROR] Review failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
