"""
Content Planner - Uses LLM to create intelligent slide plans
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from .client import LLMClient
from .prompts import PromptTemplates


class ContentPlanner:
    """Plans slide structure using LLM intelligence"""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize content planner
        
        Args:
            llm_client: LLMClient instance for API calls
        """
        self.llm = llm_client
        self.prompts = PromptTemplates()
        
    def create_slide_plan(
        self,
        content: str,
        available_layouts: List[str],
        target_slides: Optional[int] = None,
        design_preferences: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Create comprehensive slide plan from content
        
        Args:
            content: Raw text content to organize
            available_layouts: List of layout names from template
            target_slides: Optional target number of slides
            design_preferences: Optional design preferences
            
        Returns:
            List of slide dicts with structure:
            [
                {
                    "slide_number": 1,
                    "layout_name": "Title Slide",
                    "title": "Presentation Title",
                    "content": [],
                    "notes": "Opening slide"
                },
                ...
            ]
        """
        print("Planning slides with AI...")
        
        # Generate prompt
        prompt = self.prompts.content_planning_prompt(
            content=content,
            available_layouts=available_layouts,
            target_slides=target_slides,
            design_preferences=design_preferences
        )
        
        # Create messages
        messages = [
            self.prompts.system_message("presentation_designer"),
            {"role": "user", "content": prompt}
        ]
        
        # Call LLM
        try:
            response = self.llm.chat_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=4096,
                response_format={"type": "json_object"}
            )
            
            print(f"  Tokens used: {response['tokens']}, Cost: ${response['cost']:.4f}")
            
            # Parse JSON response
            content_text = response['content']
            
            # Handle different JSON formats
            try:
                # Try parsing as complete JSON object
                result = json.loads(content_text)
                
                # If it's wrapped in a slides key, extract it
                if isinstance(result, dict) and 'slides' in result:
                    slide_plan = result['slides']
                elif isinstance(result, list):
                    slide_plan = result
                else:
                    # Try to extract array from object
                    slide_plan = list(result.values())[0] if result else []
                    
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse JSON response: {e}")
                print(f"Response: {content_text[:500]}")
                raise ValueError("LLM did not return valid JSON")
            
            # Validate and clean plan
            slide_plan = self._validate_plan(slide_plan, available_layouts)
            
            print(f"✓ Created plan for {len(slide_plan)} slides")
            
            return slide_plan
            
        except Exception as e:
            print(f"Error creating slide plan: {e}")
            raise
    
    def _validate_plan(
        self,
        plan: List[Dict],
        available_layouts: List[str]
    ) -> List[Dict]:
        """
        Validate and clean slide plan
        
        Args:
            plan: Raw slide plan from LLM
            available_layouts: List of valid layout names
            
        Returns:
            Validated and cleaned plan
        """
        validated = []
        
        for idx, slide in enumerate(plan, 1):
            # Ensure required fields
            if not isinstance(slide, dict):
                continue
            
            # Normalize field names (handle variations)
            slide_normalized = {
                "slide_number": slide.get("slide_number", idx),
                "layout_name": slide.get("layout_name", slide.get("layout", "")),
                "title": slide.get("title", f"Slide {idx}"),
                "content": slide.get("content", slide.get("bullets", [])),
                "notes": slide.get("notes", slide.get("note", ""))
            }
            
            # Ensure content is a list
            if isinstance(slide_normalized["content"], str):
                slide_normalized["content"] = [slide_normalized["content"]]
            elif not isinstance(slide_normalized["content"], list):
                slide_normalized["content"] = []
            
            # Validate layout name
            layout = slide_normalized["layout_name"]
            if layout not in available_layouts:
                # Try to find close match
                layout_found = self._find_closest_layout(layout, available_layouts)
                if layout_found:
                    print(f"  Note: Mapping '{layout}' → '{layout_found}'")
                    slide_normalized["layout_name"] = layout_found
                else:
                    # Use default
                    default_layout = available_layouts[3] if len(available_layouts) > 3 else available_layouts[0]
                    print(f"  Warning: Layout '{layout}' not found, using '{default_layout}'")
                    slide_normalized["layout_name"] = default_layout
            
            validated.append(slide_normalized)
        
        return validated
    
    def _find_closest_layout(
        self,
        target: str,
        available: List[str]
    ) -> Optional[str]:
        """
        Find closest matching layout name
        
        Args:
            target: Target layout name from LLM
            available: List of available layouts
            
        Returns:
            Closest match or None
        """
        target_lower = target.lower()
        
        # Direct substring match
        for layout in available:
            if target_lower in layout.lower() or layout.lower() in target_lower:
                return layout
        
        # Keyword matching
        keywords = target_lower.split()
        for layout in available:
            layout_lower = layout.lower()
            matches = sum(1 for kw in keywords if kw in layout_lower)
            if matches >= len(keywords) // 2:
                return layout
        
        return None
    
    def chunk_content(
        self,
        text: str,
        max_slides: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Chunk content into slide-sized sections
        
        Args:
            text: Raw text to chunk
            max_slides: Maximum number of slides
            
        Returns:
            List of content chunks
        """
        print(f"Chunking content (max {max_slides} slides)...")
        
        prompt = self.prompts.content_chunking_prompt(text, max_slides)
        
        messages = [
            self.prompts.system_message("content_organizer"),
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat_completion(
            messages=messages,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response['content'])
        
        # Extract chunks (handle different formats)
        if isinstance(result, list):
            chunks = result
        elif 'chunks' in result:
            chunks = result['chunks']
        else:
            chunks = list(result.values())[0] if result else []
        
        print(f"✓ Created {len(chunks)} content chunks")
        
        return chunks


# Convenience function
def create_planner(api_key: Optional[str] = None) -> ContentPlanner:
    """
    Create content planner instance
    
    Args:
        api_key: Optional OpenAI API key
        
    Returns:
        ContentPlanner instance
    """
    llm_client = LLMClient(api_key=api_key)
    return ContentPlanner(llm_client)
