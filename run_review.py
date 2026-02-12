"""
Run holistic review on existing knime_v3 slides
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.llm.client import LLMClient
from src.llm.holistic_reviewer import HolisticReviewer

def main():
    # Read original content with encoding detection
    input_file = Path('input/[KNIME Converter] Design and Vision Document.txt')
    
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    original_content = None
    
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as f:
                original_content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    if original_content is None:
        print(f"Error: Could not decode {input_file}")
        return
    
    # Get slide images
    slide_dir = Path('output/knime_v3_slides')
    slide_images = sorted([str(p) for p in slide_dir.glob('*.PNG')])
    
    if not slide_images:
        print(f"Error: No slides found in {slide_dir}")
        return
    
    print(f"{'='*70}")
    print(f"HOLISTIC PRESENTATION REVIEW")
    print(f"{'='*70}")
    print(f"\nFound {len(slide_images)} slides to review")
    print(f"Slide directory: {slide_dir}")
    print(f"\nStarting GPT-5 Vision review...\n")
    
    # Create minimal outline (we don't have the original)
    outline = {
        'presentation_summary': 'KNIME Converter: Design and Vision Document',
        'slides': [{'slide_number': i+1} for i in range(len(slide_images))]
    }
    
    # Run review
    llm_client = LLMClient()
    reviewer = HolisticReviewer(llm_client)
    
    review = reviewer.review_presentation(
        slide_images=slide_images,
        original_content=original_content,
        outline=outline
    )
    
    # Save review
    review_path = Path('output/knime_v3.review.json')
    with open(review_path, 'w', encoding='utf-8') as f:
        json.dump(review, f, indent=2)
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"REVIEW COMPLETE")
    print(f"{'='*70}\n")
    print(f"✓ Review saved: {review_path}")
    print(f"\n📊 SCORES:")
    print(f"  Content Coverage: {review.get('content_coverage_score', 'N/A')}/100")
    print(f"  Verbosity:        {review.get('verbosity_score', 'N/A')}/100")
    print(f"  Consistency:      {review.get('consistency_score', 'N/A')}/100")
    print(f"  Flow:             {review.get('flow_score', 'N/A')}/100")
    print(f"  Overall:          {review.get('overall_score', 'N/A')}/100")
    print(f"\n🎯 Needs Revision: {review.get('needs_revision', False)}")
    
    if review.get('critical_issues'):
        print(f"\n⚠️  CRITICAL ISSUES:")
        for issue in review['critical_issues']:
            print(f"  - {issue}")
    
    if review.get('strengths'):
        print(f"\n✅ STRENGTHS:")
        for strength in review['strengths'][:3]:  # Show top 3
            print(f"  - {strength}")
    
    if review.get('suggestions'):
        print(f"\n💡 SUGGESTIONS:")
        for suggestion in review['suggestions'][:5]:  # Show top 5
            print(f"  - {suggestion}")
    
    # Print API usage
    stats = llm_client.get_usage_stats()
    print(f"\n📈 API USAGE:")
    print(f"  Tokens: {stats['total_tokens']:,}")
    print(f"  Cost:   ${stats['total_cost']:.4f}")
    print()

if __name__ == "__main__":
    main()
