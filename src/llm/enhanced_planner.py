"""
Enhanced Content Planner - Two-stage planning with schema awareness
Stage 1: High-level outline (slide types, purposes, layout selection)
Stage 2: Detailed content generation per schema
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from src.llm.client import LLMClient
from src.llm.prompts import PromptTemplates


class EnhancedContentPlanner:
    """Two-stage content planning with template schema awareness"""
    
    def __init__(self, llm_client: LLMClient, schemas_path: str = "config/template_schemas.json"):
        """
        Initialize enhanced planner
        
        Args:
            llm_client: LLM client instance
            schemas_path: Path to template schemas JSON
        """
        self.llm = llm_client
        self.prompts = PromptTemplates()
        
        # Load template schemas
        with open(schemas_path, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)
            self.schemas = schema_data['schemas']
            self.statistics = schema_data.get('statistics', {})
    
    def create_outline(
        self,
        content: str,
        target_slides: Optional[int] = None,
        design_preferences: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Stage 1: Create high-level presentation outline
        
        Args:
            content: Raw text content to organize
            target_slides: Optional target number of slides
            design_preferences: Optional design preferences
            
        Returns:
            Outline with slide specifications (layout, purpose, key content)
        """
        print("Stage 1: Creating presentation outline...")
        
        # Get available layouts grouped by category
        layout_categories = self._get_layout_categories()
        
        # Create outline prompt
        prompt = self._create_outline_prompt(
            content, layout_categories, target_slides, design_preferences
        )
        
        # Get outline schema
        outline_schema = self._get_outline_schema()
        
        messages = [
            self.prompts.system_message("presentation_designer"),
            {"role": "user", "content": prompt}
        ]
        
        # Call LLM with structured output
        response = self.llm.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "presentation_outline",
                    "strict": True,
                    "schema": outline_schema
                }
            }
        )
        
        print(f"  Tokens used: {response['tokens']}, Cost: ${response['cost']:.4f}")
        
        # Parse outline
        outline = json.loads(response['content'])
        
        # Validate layouts exist
        outline = self._validate_outline(outline)
        
        print(f"✓ Created outline for {len(outline['slides'])} slides")
        
        return outline
    
    def _get_layout_categories(self) -> Dict[str, List[str]]:
        """Group layouts by category for better LLM selection"""
        categories = {}
        
        for layout_name, schema in self.schemas.items():
            category = schema['category']
            if category not in categories:
                categories[category] = []
            categories[category].append({
                'name': layout_name,
                'complexity': schema['complexity'],
                'supports_images': schema['supports_images']
            })
        
        return categories
    
    def _create_outline_prompt(
        self,
        content: str,
        layout_categories: Dict,
        target_slides: Optional[int],
        design_preferences: Optional[Dict]
    ) -> str:
        """Create prompt for outline generation"""
        
        target_text = f"Target approximately {target_slides} slides." if target_slides else ""
        
        # Format layout categories
        layouts_text = "\n\n"
        for category, layouts in sorted(layout_categories.items()):
            layouts_text += f"{category.upper().replace('_', ' ')}:\n"
            for layout in layouts[:5]:  # Show first 5 of each category
                img_note = " (supports images)" if layout['supports_images'] else ""
                layouts_text += f"  - {layout['name']}{img_note}\n"
            if len(layouts) > 5:
                layouts_text += f"  ... and {len(layouts)-5} more\n"
            layouts_text += "\n"
        
        prompt = f"""You are an expert presentation designer creating a strategic outline for a professional PowerPoint presentation.

CONTENT TO ORGANIZE:
{content}

AVAILABLE LAYOUT CATEGORIES:
{layouts_text}

{target_text}

YOUR TASK:
Create a comprehensive slide-by-slide outline that:
1. Covers ALL content from the input comprehensively
2. Selects appropriate layout types for each slide's purpose
3. Plans logical flow and progression
4. Balances content across slides (avoid overcrowding)
5. Uses varied layouts for visual interest

CRITICAL REQUIREMENTS:
- For each slide, specify:
  * slide_number: Sequential number starting from 1
  * layout_name: Exact layout name from the available list
  * purpose: What this slide accomplishes (1-2 sentences)
  * key_content: Array of key points to cover
  * notes: Design rationale or presenter notes
- Include presentation_summary: Brief overview of entire presentation's narrative arc
- Ensure COMPREHENSIVE coverage - don't skip or summarize important details
- Plan for detailed content (4-6 bullets per content slide)
- Choose layouts strategically (title slides, section headers, content, visuals)

OUTPUT FORMAT:
Return ONLY valid JSON matching the schema. No markdown, no explanations."""
        
        return prompt
    
    def _get_outline_schema(self) -> Dict:
        """Get JSON schema for outline response"""
        return {
            "type": "object",
            "properties": {
                "presentation_summary": {
                    "type": "string",
                    "description": "Brief overview of presentation's narrative and structure"
                },
                "slides": {
                    "type": "array",
                    "description": "Array of slide plan specifications",
                    "items": {
                        "type": "object",
                        "properties": {
                            "slide_number": {
                                "type": "integer",
                                "description": "Sequential slide number starting from 1"
                            },
                            "layout_name": {
                                "type": "string",
                                "description": "Exact layout name from available layouts"
                            },
                            "purpose": {
                                "type": "string",
                                "description": "What this slide accomplishes (strategic purpose)"
                            },
                            "key_content": {
                                "type": "array",
                                "description": "Key points or themes to cover on this slide",
                                "items": {"type": "string"}
                            },
                            "notes": {
                                "type": "string",
                                "description": "Design rationale or presenter notes"
                            }
                        },
                        "required": ["slide_number", "layout_name", "purpose", "key_content", "notes"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["presentation_summary", "slides"],
            "additionalProperties": False
        }
    
    def _validate_outline(self, outline: Dict) -> Dict:
        """Validate and clean outline"""
        # Validate layouts exist
        for slide in outline['slides']:
            layout_name = slide['layout_name']
            if layout_name not in self.schemas:
                # Try to find closest match
                closest = self._find_closest_layout(layout_name)
                if closest:
                    print(f"  Note: Mapping '{layout_name}' → '{closest}'")
                    slide['layout_name'] = closest
                else:
                    # Default to common layout
                    print(f"  Warning: Layout '{layout_name}' not found, using '10_Title and Content'")
                    slide['layout_name'] = '10_Title and Content'
        
        return outline
    
    def _find_closest_layout(self, target: str) -> Optional[str]:
        """Find closest matching layout name"""
        target_lower = target.lower()
        
        # Direct substring match
        for layout_name in self.schemas.keys():
            if target_lower in layout_name.lower() or layout_name.lower() in target_lower:
                return layout_name
        
        # Keyword matching
        keywords = target_lower.split()
        for layout_name in self.schemas.keys():
            layout_lower = layout_name.lower()
            matches = sum(1 for kw in keywords if kw in layout_lower)
            if matches >= len(keywords) // 2:
                return layout_name
        
        return None
    
    def get_layout_schema(self, layout_name: str) -> Dict[str, Any]:
        """
        Get schema for a specific layout
        
        Args:
            layout_name: Name of the layout
            
        Returns:
            Schema dictionary
        """
        return self.schemas.get(layout_name, {})


def create_enhanced_planner(api_key: Optional[str] = None, schemas_path: str = "config/template_schemas.json") -> EnhancedContentPlanner:
    """
    Create enhanced planner instance
    
    Args:
        api_key: Optional OpenAI API key
        schemas_path: Path to template schemas
        
    Returns:
        EnhancedContentPlanner instance
    """
    llm_client = LLMClient(api_key=api_key)
    return EnhancedContentPlanner(llm_client, schemas_path)
