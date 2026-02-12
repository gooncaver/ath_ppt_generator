"""
Holistic Presentation Reviewer - Batch review with GPT-5 Vision
Reviews entire presentation with full context awareness
"""

import base64
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.llm.client import LLMClient


class HolisticReviewer:
    """Review entire presentation with full context using Vision API"""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize holistic reviewer
        
        Args:
            llm_client: LLM client instance
        """
        self.llm = llm_client
    
    def review_presentation(
        self,
        slide_images: List[str],
        original_content: str,
        outline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Comprehensively review entire presentation
        
        Args:
            slide_images: List of slide image file paths
            original_content: Original input content
            outline: Presentation outline
            
        Returns:
            Review results with issues, scores, and revision recommendations
        """
        print(f"\nHolistic Review: Analyzing {len(slide_images)} slides...")
        
        # Encode all images to base64
        encoded_images = []
        for img_path in slide_images:
            try:
                with open(img_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
                    encoded_images.append({
                        'path': img_path,
                        'data': img_data,
                        'slide_number': self._extract_slide_number(img_path)
                    })
            except Exception as e:
                print(f"  Warning: Could not encode {img_path}: {e}")
        
        # Create review prompt
        prompt = self._create_review_prompt(original_content, outline, len(encoded_images))
        
        # Build messages with images
        message_content = [
            {"type": "text", "text": prompt}
        ]
        
        # Add all slide images
        for img in sorted(encoded_images, key=lambda x: x['slide_number']):
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img['data']}"
                }
            })
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert presentation reviewer with a critical eye for quality, completeness, and design."
            },
            {
                "role": "user",
                "content": message_content
            }
        ]
        
        # Get review schema
        review_schema = self._get_review_schema()
        
        # Call Vision API
        print("  Sending to GPT-5 Vision for comprehensive analysis...")
        response = self.llm.chat_completion(
            messages=messages,
            temperature=0.3,  # Lower temperature for consistent reviews
            max_tokens=4096,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "presentation_review",
                    "strict": True,
                    "schema": review_schema
                }
            }
        )
        
        print(f"  Tokens used: {response['tokens']}, Cost: ${response['cost']:.4f}")
        
        # Parse review
        review = json.loads(response['content'])
        
        # Print summary
        self._print_review_summary(review)
        
        return review
    
    def _extract_slide_number(self, img_path: str) -> int:
        """Extract slide number from image filename"""
        filename = Path(img_path).stem
        # Try to extract number from filename like "Slide1", "slide_01", etc.
        import re
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else 0
    
    def _create_review_prompt(
        self,
        original_content: str,
        outline: Dict,
        slide_count: int
    ) -> str:
        """Create comprehensive review prompt"""
        
        outline_summary = outline.get('presentation_summary', 'N/A')
        
        prompt = f"""You are reviewing a {slide_count}-slide PowerPoint presentation. Analyze ALL slides comprehensively.

ORIGINAL INPUT CONTENT:
{original_content[:3000]}...

INTENDED OUTLINE:
{outline_summary}

YOUR REVIEW MUST EVALUATE:

1. CONTENT COVERAGE (Critical)
   - Does the presentation comprehensively cover ALL content from the original input?
   - Are any important points missing, oversimplified, or skipped?
   - Is the level of detail appropriate (not too sparse)?

2. CONTENT VERBOSITY
   - Are slides utilizing their full capacity (4-6 bullets for content slides)?
   - Are bullets detailed and informative, not just keywords?
   - Is text readable but comprehensive?

3. VISUAL CONSISTENCY
   - Are backgrounds consistent throughout (all dark or all light)?
   - Is layout usage appropriate and varied?
   - Are there any jarring visual transitions?

4. SLIDE FLOW & PROGRESSION
   - Do slides follow logical sequence?
   - Are transitions smooth?
   - Is the narrative arc clear?

5. LAYOUT APPROPRIATENESS
   - Are layouts chosen well for each slide's content?
   - Are there better layout choices available?

6. QUALITY ISSUES
   - Any text overlap, truncation, or alignment problems?
   - Any slides that are too empty or too crowded?
   - Any design inconsistencies?

Provide detailed, actionable feedback. Be CRITICAL - this is for quality assurance."""
        
        return prompt
    
    def  _get_review_schema(self) -> Dict:
        """Get JSON schema for review response"""
        return {
            "type": "object",
            "properties": {
                "overall_assessment": {
                    "type": "string",
                    "description": "High-level summary of presentation quality"
                },
                "content_coverage_score": {
                    "type": "integer",
                    "description": "Score 0-100 for how well all input content is covered",
                    "minimum": 0,
                    "maximum": 100
                },
                "verbosity_score": {
                    "type": "integer",
                    "description": "Score 0-100 for content detail and utilization",
                    "minimum": 0,
                    "maximum": 100
                },
                "consistency_score": {
                    "type": "integer",
                    "description": "Score 0-100 for visual consistency",
                    "minimum": 0,
                    "maximum": 100
                },
                "flow_score": {
                    "type": "integer",
                    "description": "Score 0-100 for logical flow and progression",
                    "minimum": 0,
                    "maximum": 100
                },
                "overall_score": {
                    "type": "integer",
                    "description": "Overall quality score 0-100",
                    "minimum": 0,
                    "maximum": 100
                },
                "needs_revision": {
                    "type": "boolean",
                    "description": "Whether presentation needs revisions"
                },
                "critical_issues": {
                    "type": "array",
                    "description": "List of critical issues that must be fixed",
                    "items": {
                        "type": "object",
                        "properties": {
                            "slide_numbers": {
                                "type": "array",
                                "description": "Affected slide numbers",
                                "items": {"type": "integer"}
                            },
                            "issue": {
                                "type": "string",
                                "description": "Description of the issue"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["critical", "moderate", "minor"],
                                "description": "Issue severity"
                            },
                            "recommendation": {
                                "type": "string",
                                "description": "How to fix this issue"
                            }
                        },
                        "required": ["slide_numbers", "issue", "severity", "recommendation"],
                        "additionalProperties": False
                    }
                },
                "missing_content": {
                    "type": "array",
                    "description": "Content from input that is missing in presentation",
                    "items": {"type": "string"}
                },
                "strengths": {
                    "type": "array",
                    "description": "What the presentation does well",
                    "items": {"type": "string"}
                },
                "improvement_suggestions": {
                    "type": "array",
                    "description": "Optional improvements (not critical but recommended)",
                    "items": {"type": "string"}
                }
            },
            "required": [
                "overall_assessment",
                "content_coverage_score",
                "verbosity_score",
                "consistency_score",
                "flow_score",
                "overall_score",
                "needs_revision",
                "critical_issues",
                "missing_content",
                "strengths",
                "improvement_suggestions"
            ],
            "additionalProperties": False
        }
    
    def _print_review_summary(self, review: Dict):
        """Print formatted review summary"""
        print(f"\n{'='*70}")
        print("REVIEW RESULTS")
        print(f"{'='*70}\n")
        
        print(f"Overall Score: {review['overall_score']}/100")
        print(f"Content Coverage: {review['content_coverage_score']}/100")
        print(f"Verbosity: {review['verbosity_score']}/100")
        print(f"Consistency: {review['consistency_score']}/100")
        print(f"Flow: {review['flow_score']}/100")
        
        print(f"\nNeeds Revision: {'YES' if review['needs_revision'] else 'NO'}")
        
        if review['critical_issues']:
            print(f"\nCritical Issues ({len(review['critical_issues'])}):")
            for issue in review['critical_issues']:
                slides_str = ', '.join(map(str, issue['slide_numbers']))
                print(f"  [{issue['severity'].upper()}] Slides {slides_str}: {issue['issue']}")
                print(f"    → {issue['recommendation']}")
        
        if review['missing_content']:
            print(f"\nMissing Content ({len(review['missing_content'])} items):")
            for item in review['missing_content'][:5]:
                print(f"  - {item}")
            if len(review['missing_content']) > 5:
                print(f"  ... and {len(review['missing_content'])-5} more")
        
        if review['strengths']:
            print(f"\nStrengths:")
            for strength in review['strengths'][:3]:
                print(f"  ✓ {strength}")
        
        print(f"\n{review['overall_assessment']}")
        print(f"{'='*70}\n")
