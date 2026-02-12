"""
Prompt templates for LLM-powered slide generation
Contains engineered prompts for content planning and layout selection
"""

from typing import List, Dict


class PromptTemplates:
    """Collection of prompt templates for slide generation"""
    
    @staticmethod
    def content_planning_prompt(
        content: str,
        available_layouts: List[str],
        target_slides: int = None,
        design_preferences: Dict = None
    ) -> str:
        """
        Generate prompt for content planning
        
        Args:
            content: Raw text content to organize
            available_layouts: List of layout names from template
            target_slides: Optional target number of slides
            design_preferences: Optional design preferences
            
        Returns:
            Formatted prompt string
        """
        layouts_text = "\n".join(f"  - {layout}" for layout in available_layouts)
        
        target_text = f"\nTarget approximately {target_slides} slides." if target_slides else ""
        
        prompt = f"""You are an expert presentation designer. Analyze the following content and create a comprehensive slide-by-slide plan for a professional PowerPoint presentation.

CRITICAL REQUIREMENTS:
1. Use ALL provided content - every section, point, and detail must appear in the presentation
2. Select appropriate layouts from the available list for each slide
3. Organize content logically with clear flow and progression
4. Create professional structure: introduction, body sections, conclusion

CONTENT TO ORGANIZE:
{content}

AVAILABLE SLIDE LAYOUTS:
{layouts_text}
{target_text}

OUTPUT FORMAT (JSON):
Return a JSON array of slide objects. Each slide must have:
{{
  "slide_number": <number>,
  "layout_name": "<exact layout name from available list>",
  "title": "<slide title>",
  "content": ["<bullet 1>", "<bullet 2>", ...],
  "notes": "<presenter notes or rationale>"
}}

LAYOUT SELECTION GUIDELINES:
- "Title Slide" or "1_Title Slide": Opening/title slides
- Layouts with "Title and Content": Standard content slides with bullets
- Layouts with "Two Column" or numbered variants: Comparisons, side-by-side content
- Layouts with "Picture" placeholders: Image-heavy slides (for later phases)
- "Title Only" variants: Section headers, transitions

QUALITY STANDARDS:
- Maximum 5-6 bullets per slide
- Keep bullets concise (under 120 characters)
- Logical grouping of related content
- Smooth transitions between topics
- Professional pacing and flow

Generate the complete slide plan now:"""
        
        return prompt
    
    @staticmethod
    def layout_selection_prompt(
        slide_content: str,
        available_layouts: List[str]
    ) -> str:
        """
        Generate prompt for selecting best layout for specific content
        
        Args:
            slide_content: Content for a single slide
            available_layouts: List of available layout names
            
        Returns:
            Formatted prompt string
        """
        layouts_text = "\n".join(f"  - {layout}" for layout in available_layouts)
        
        prompt = f"""Select the most appropriate slide layout for this content.

CONTENT:
{slide_content}

AVAILABLE LAYOUTS:
{layouts_text}

Respond with ONLY the exact layout name from the list above. Choose based on:
- Content type (title, bullets, comparison, etc.)
- Amount of content
- Visual balance

Layout name:"""
        
        return prompt
    
    @staticmethod
    def content_chunking_prompt(
        text: str,
        max_slides: int = 15
    ) -> str:
        """
        Generate prompt for chunking text into slide-sized sections
        
        Args:
            text: Raw text to chunk
            max_slides: Maximum number of slides
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Organize this text content into {max_slides} or fewer slide-sized chunks.

CONTENT:
{text}

For each chunk, provide:
1. A descriptive title
2. 3-5 key points or bullets
3. Any supporting details

Make chunks logical and balanced. Group related information together.

Return as JSON array with format:
[
  {{
    "title": "<slide title>",
    "bullets": ["<point 1>", "<point 2>", ...],
    "details": "<optional supporting text>"
  }},
  ...
]

Generate chunks now:"""
        
        return prompt
    
    @staticmethod
    def image_analysis_prompt() -> str:
        """
        Generate prompt for image analysis with Vision API
        
        Returns:
            Formatted prompt string
        """
        prompt = """Analyze this image for PowerPoint slide placement.

Provide a JSON response with:
{
  "content_type": "<photo|diagram|chart|screenshot|other>",
  "description": "<what the image shows>",
  "suggested_layout": "<full_image|image_left|image_right|image_top>",
  "text_present": <true|false>,
  "text_content": "<OCR text if present>",
  "dominant_colors": ["<color 1>", "<color 2>"],
  "aspect_ratio": "<landscape|portrait|square>",
  "quality": "<high|medium|low>",
  "placement_notes": "<suggestions for slide placement>"
}

Analyze the image:"""
        
        return prompt
    
    @staticmethod
    def slide_quality_review_prompt() -> str:
        """
        Generate prompt for visual slide quality review
        
        Returns:
            Formatted prompt string
        """
        prompt = """Review this PowerPoint slide image for quality and design issues.

Check for:
1. Overlapping text or images
2. Alignment problems (text, images, elements)
3. Text readability (size, contrast, font)
4. Visual balance and aesthetics
5. Spacing issues (too cramped or too sparse)
6. Professional appearance

Provide JSON response:
{
  "status": "APPROVED" or "NEEDS_REVISION",
  "issues": [
    {
      "type": "<overlap|alignment|readability|spacing|other>",
      "severity": "<high|medium|low>",
      "description": "<specific issue>",
      "location": "<where on slide>"
    }
  ],
  "suggestions": [
    "<specific fix 1>",
    "<specific fix 2>"
  ],
  "overall_score": <1-10>
}

Review the slide:"""
        
        return prompt
    
    @staticmethod
    def system_message(role: str = "presentation_designer") -> Dict[str, str]:
        """
        Generate system message for chat completion
        
        Args:
            role: Role type (presentation_designer, content_organizer, etc.)
            
        Returns:
            Message dict with role and content
        """
        messages = {
            "presentation_designer": {
                "role": "system",
                "content": "You are an expert presentation designer with extensive experience creating professional PowerPoint presentations. You understand visual design, content organization, and audience engagement. You always ensure comprehensive content coverage and logical flow."
            },
            "content_organizer": {
                "role": "system",
                "content": "You are a content organization expert who excels at structuring information for maximum clarity and impact. You create logical flows and ensure all information is properly categorized and presented."
            },
            "quality_reviewer": {
                "role": "system",
                "content": "You are a meticulous design reviewer who identifies visual issues, alignment problems, and readability concerns in presentations. You provide specific, actionable feedback."
            }
        }
        
        return messages.get(role, messages["presentation_designer"])


# Convenience functions
def get_planning_prompt(content: str, layouts: List[str], **kwargs) -> str:
    """Shortcut for content planning prompt"""
    return PromptTemplates.content_planning_prompt(content, layouts, **kwargs)


def get_image_analysis_prompt() -> str:
    """Shortcut for image analysis prompt"""
    return PromptTemplates.image_analysis_prompt()


def get_quality_review_prompt() -> str:
    """Shortcut for quality review prompt"""
    return PromptTemplates.slide_quality_review_prompt()
