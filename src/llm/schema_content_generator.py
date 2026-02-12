"""
Schema-Guided Content Generator - Generate slide content matching exact template schemas
Stage 2: Detailed content generation per schema
"""

import json
from typing import Dict, Any, Optional, List

from src.llm.client import LLMClient


class SchemaGuidedGenerator:
    """Generate slide content based on template schemas"""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize schema-guided generator
        
        Args:
            llm_client: LLM client instance
        """
        self.llm = llm_client
    
    def generate_slide_content(
        self,
        slide_spec: Dict[str, Any],
        schema: Dict[str, Any],
        full_context: str
    ) -> Dict[str, Any]:
        """
        Generate detailed content for a slide based on its schema
        
        Args:
            slide_spec: Slide specification from outline (purpose, key_content, etc.)
            schema: Template schema defining required fields
            full_context: Full original content for reference
            
        Returns:
            Dictionary with all fields populated per schema
        """
        # Build prompt for this slide
        prompt = self._create_content_prompt(slide_spec, schema, full_context)
        
        # Get schema for response format
        response_schema = self._create_response_schema(schema)
        
        # Call LLM
        messages = [
            {
                "role": "system",
                "content": "You are an expert content writer creating detailed, professional slide content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.llm.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "slide_content",
                    "strict": True,
                    "schema": response_schema
                }
            }
        )
        
        # Parse and return
        content = json.loads(response['content'])
        return content
    
    def _create_content_prompt(
        self,
        slide_spec: Dict,
        schema: Dict,
        full_context: str
    ) -> str:
        """Create prompt for generating slide content"""
        
        fields = schema.get('fields', [])
        field_metadata = schema.get('field_metadata', {})
        
        # Build field requirements
        field_reqs = "\n"
        for field in fields:
            metadata = field_metadata.get(field, {})
            field_type = metadata.get('type', 'text')
            purpose = metadata.get('purpose', '')
            
            if field_type == 'bullets':
                max_bullets = metadata.get('max_bullets', 6)
                max_length = metadata.get('max_bullet_length', 120)
                field_reqs += f"  - {field}: Array of {max_bullets} detailed bullet points (max {max_length} chars each)\n"
            elif field_type == 'text':
                max_length = metadata.get('max_length', 80)
                field_reqs += f"  - {field}: Text string (max {max_length} chars) - {purpose}\n"
            elif field_type == 'image':
                field_reqs += f"  - {field}: Image description for placeholder - {purpose}\n"
            else:
                field_reqs += f"  - {field}: {field_type.upper()} - {purpose}\n"
        
        # Get relevant context snippet
        key_content_str = "\n".join(f"  • {item}" for item in slide_spec.get('key_content', []))
        
        prompt = f"""Generate detailed content for Slide #{slide_spec['slide_number']}.

SLIDE PURPOSE:
{slide_spec['purpose']}

KEY CONTENT TO COVER:
{key_content_str}

DESIGN NOTES:
{slide_spec.get('notes', 'N/A')}

TEMPLATE: {schema['layout_name']}
CATEGORY: {schema['category']}
COMPLEXITY: {schema['complexity']}

REQUIRED FIELDS:
{field_reqs}

VERBOSITY REQUIREMENTS:
- Provide COMPREHENSIVE, DETAILED content
- For bullet point fields: Always provide 4-6 substantial bullets unless it's a title/section slide
- Each bullet should be informative and complete (not just keywords)
- Expand on key points from the source material
- Include supporting details, context, and examples where relevant
- Don't oversimplify or summarize too much

FULL CONTEXT (for reference):
{full_context[:2000]}...

Generate content that matches the exact schema and fully utilizes the slide's capacity."""
        
        return prompt
    
    def _create_response_schema(self, schema: Dict) -> Dict:
        """Create JSON schema for response based on template schema"""
        
        fields = schema.get('fields', [])
        field_metadata = schema.get('field_metadata', {})
        
        properties = {}
        required_fields = []
        
        for field in fields:
            metadata = field_metadata.get(field, {})
            field_type = metadata.get('type', 'text')
            
            if field_type == 'bullets' or field == 'content':
                properties[field] = {
                    "type": "array",
                    "description": metadata.get('purpose', 'Slide content bullets'),
                    "items": {"type": "string"},
                    "minItems": 1
                }
                required_fields.append(field)
            elif field_type == 'text':
                properties[field] = {
                    "type": "string",
                    "description": metadata.get('purpose', f'{field} text')
                }
                if field in schema.get('required_fields', []):
                    required_fields.append(field)
            elif field_type == 'image':
                # Image placeholder description
                properties[field] = {
                    "type": "string",
                    "description": f"Description of image content for {field}"
                }
            elif field_type in ['chart', 'table']:
                # For now, placeholder text
                properties[field] = {
                    "type": "string",
                    "description": f"{field_type.capitalize()} data description"
                }
        
        # Add notes field
        properties['notes'] = {
            "type": "string",
            "description": "Presenter notes or additional context"
        }
        required_fields.append('notes')
        
        return {
            "type": "object",
            "properties": properties,
            "required": required_fields,
            "additionalProperties": False
        }
    
    def generate_all_slide_content(
        self,
        outline: Dict[str, Any],
        schemas: Dict[str, Dict],
        full_context: str
    ) -> List[Dict[str, Any]]:
        """
        Generate content for all slides in outline
        
        Args:
            outline: Full presentation outline
            schemas: All template schemas
            full_context: Full original content
            
        Returns:
            List of slide content dictionaries
        """
        print(f"\nStage 2: Generating detailed content for {len(outline['slides'])} slides...")
        
        all_content = []
        
        for i, slide_spec in enumerate(outline['slides'], 1):
            layout_name = slide_spec['layout_name']
            schema = schemas.get(layout_name, {})
            
            if not schema:
                print(f"  Warning: No schema for layout '{layout_name}', skipping")
                continue
            
            print(f"  [{i}/{len(outline['slides'])}] Generating: {slide_spec['purpose'][:50]}...")
            
            try:
                content = self.generate_slide_content(slide_spec, schema, full_context)
                content['slide_number'] = slide_spec['slide_number']
                content['layout_name'] = layout_name
                all_content.append(content)
            except Exception as e:
                print(f"    Error: {e}")
                # Create minimal fallback content
                all_content.append({
                    'slide_number': slide_spec['slide_number'],
                    'layout_name': layout_name,
                    'title': f"Slide {slide_spec['slide_number']}",
                    'content': slide_spec.get('key_content', []),
                    'notes': slide_spec.get('notes', '')
                })
        
        print(f"✓ Generated content for {len(all_content)} slides")
        
        return all_content
