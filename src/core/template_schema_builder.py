"""
Template Schema Builder - Analyze and create schemas for all slide layouts
Generates structured schemas that define fields, constraints, and requirements
"""

import sys
from pathlib import Path

# Add parent directory to path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import json
from typing import Dict, List, Any
from collections import defaultdict

from src.template_inspector import TemplateInspector


class TemplateSchemaBuilder:
    """Build comprehensive schemas for all template layouts"""
    
    def __init__(self, template_path: str):
        """
        Initialize schema builder
        
        Args:
            template_path: Path to PowerPoint template
        """
        self.template_path = template_path
        self.inspector = TemplateInspector(template_path)
        self.layouts = self.inspector.get_slide_layouts()
        
    def build_all_schemas(self) -> Dict[str, Dict[str, Any]]:
        """
        Build schemas for all layouts in template
        
        Returns:
            Dictionary mapping layout names to their schemas
        """
        schemas = {}
        
        for layout in self.layouts:
            schema = self.build_layout_schema(layout)
            schemas[layout['name']] = schema
        
        return schemas
    
    def build_layout_schema(self, layout: Dict) -> Dict[str, Any]:
        """
        Build schema for a single layout
        
        Args:
            layout: Layout info from template inspector
            
        Returns:
            Schema dictionary with fields, constraints, metadata
        """
        placeholders = layout.get('placeholders', [])
        
        # Categorize placeholders
        fields = []
        required_fields = []
        field_metadata = {}
        
        for ph in placeholders:
            ph_type = str(ph.get('type', ''))  # Convert enum to string
            ph_name = ph.get('name', '')
            ph_idx = ph.get('index', 0)
            
            # Determine field name and type
            if 'TITLE' in ph_type:
                field_name = 'title' if 'title' not in fields else f'subtitle'
                fields.append(field_name)
                required_fields.append(field_name)
                field_metadata[field_name] = {
                    'type': 'text',
                    'placeholder_type': ph_type,
                    'max_length': 80,
                    'purpose': 'Main slide title' if field_name == 'title' else 'Secondary title'
                }
                
            elif 'BODY' in ph_type or 'OBJECT' in ph_type:
                # Check for specific content types
                if 'content' not in fields:
                    field_name = 'content'
                    fields.append(field_name)
                    field_metadata[field_name] = {
                        'type': 'bullets',
                        'placeholder_type': ph_type,
                        'max_bullets': 6,
                        'max_bullet_length': 120,
                        'purpose': 'Main slide content'
                    }
                    
            elif 'PICTURE' in ph_type:
                # Count picture placeholders
                pic_count = sum(1 for f in fields if f.startswith('image'))
                field_name = f'image{pic_count + 1}'
                fields.append(field_name)
                field_metadata[field_name] = {
                    'type': 'image',
                    'placeholder_type': ph_type,
                    'purpose': f'Image placeholder {pic_count + 1}'
                }
                
            elif 'TABLE' in ph_type:
                field_name = 'table_data'
                if field_name not in fields:
                    fields.append(field_name)
                    field_metadata[field_name] = {
                        'type': 'table',
                        'placeholder_type': ph_type,
                        'purpose': 'Tabular data'
                    }
                    
            elif 'CHART' in ph_type:
                field_name = 'chart_data'
                if field_name not in fields:
                    fields.append(field_name)
                    field_metadata[field_name] = {
                        'type': 'chart',
                        'placeholder_type': ph_type,
                        'purpose': 'Chart/graph data'
                    }
        
        # Detect layout category
        category = self._categorize_layout(layout['name'], fields)
        
        # Build complete schema
        schema = {
            'layout_name': layout['name'],
            'category': category,
            'fields': fields,
            'required_fields': required_fields,
            'field_metadata': field_metadata,
            'placeholder_count': len(placeholders),
            'supports_images': any(f.startswith('image') for f in fields),
            'supports_charts': 'chart_data' in fields,
            'supports_tables': 'table_data' in fields,
            'complexity': self._calculate_complexity(fields, field_metadata)
        }
        
        return schema
    
    def _categorize_layout(self, name: str, fields: List[str]) -> str:
        """
        Categorize layout by its purpose
        
        Args:
            name: Layout name
            fields: List of field names
            
        Returns:
            Category string
        """
        name_lower = name.lower()
        
        # Title slides
        if 'title' in name_lower and 'subtitle' in fields and 'content' not in fields:
            return 'title_slide'
        
        # Agenda/TOC
        if 'agenda' in name_lower or 'toc' in name_lower:
            return 'agenda'
        
        # Section headers
        if 'section' in name_lower or ('title' in fields and len(fields) == 1):
            return 'section_header'
        
        # Content slides
        if 'content' in fields and not any(f.startswith('image') for f in fields):
            return 'text_content'
        
        # Image-focused
        if sum(1 for f in fields if f.startswith('image')) >= 2:
            return 'image_focused'
        
        # Mixed content
        if 'content' in fields and any(f.startswith('image') for f in fields):
            return 'mixed_content'
        
        # Comparison/two-column
        if 'two' in name_lower or 'comparison' in name_lower:
            return 'comparison'
        
        # Blank/custom
        if len(fields) == 0 or 'blank' in name_lower:
            return 'blank'
        
        return 'general'
    
    def _calculate_complexity(self, fields: List[str], metadata: Dict) -> str:
        """
        Calculate layout complexity
        
        Args:
            fields: List of fields
            metadata: Field metadata
            
        Returns:
            Complexity level: simple, moderate, complex
        """
        field_count = len(fields)
        
        if field_count <= 2:
            return 'simple'
        elif field_count <= 4:
            return 'moderate'
        else:
            return 'complex'
    
    def group_similar_schemas(self, schemas: Dict) -> Dict[str, List[str]]:
        """
        Group layouts with similar schemas
        
        Args:
            schemas: All layout schemas
            
        Returns:
            Dictionary mapping schema signature to layout names
        """
        groups = defaultdict(list)
        
        for layout_name, schema in schemas.items():
            # Create signature from fields
            signature = (
                tuple(sorted(schema['fields'])),
                schema['category']
            )
            groups[str(signature)].append(layout_name)
        
        return dict(groups)
    
    def save_schemas(self, output_path: str, include_groups: bool = True):
        """
        Save schemas to JSON file
        
        Args:
            output_path: Path to save JSON file
            include_groups: Whether to include grouping info
        """
        schemas = self.build_all_schemas()
        
        output = {
            'template_path': self.template_path,
            'total_layouts': len(schemas),
            'schemas': schemas
        }
        
        if include_groups:
            groups = self.group_similar_schemas(schemas)
            output['schema_groups'] = groups
            output['unique_schema_count'] = len(groups)
        
        # Statistics
        categories = defaultdict(int)
        for schema in schemas.values():
            categories[schema['category']] += 1
        
        output['statistics'] = {
            'by_category': dict(categories),
            'with_images': sum(1 for s in schemas.values() if s['supports_images']),
            'with_charts': sum(1 for s in schemas.values() if s['supports_charts']),
            'with_tables': sum(1 for s in schemas.values() if s['supports_tables']),
            'complexity_distribution': {
                'simple': sum(1 for s in schemas.values() if s['complexity'] == 'simple'),
                'moderate': sum(1 for s in schemas.values() if s['complexity'] == 'moderate'),
                'complex': sum(1 for s in schemas.values() if s['complexity'] == 'complex')
            }
        }
        
        # Save to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved schemas to: {output_path}")
        print(f"  Total layouts: {len(schemas)}")
        print(f"  Unique schema patterns: {output.get('unique_schema_count', 'N/A')}")
        print(f"  Categories: {', '.join(f'{k}={v}' for k, v in categories.items())}")
        
        return output_path
    
    def print_summary(self):
        """Print summary of all layouts and their schemas"""
        schemas = self.build_all_schemas()
        
        print(f"\n{'='*70}")
        print(f"TEMPLATE SCHEMA ANALYSIS")
        print(f"{'='*70}\n")
        
        print(f"Template: {self.template_path}")
        print(f"Total Layouts: {len(schemas)}\n")
        
        # Group by category
        by_category = defaultdict(list)
        for name, schema in schemas.items():
            by_category[schema['category']].append((name, schema))
        
        for category, items in sorted(by_category.items()):
            print(f"\n{category.upper().replace('_', ' ')} ({len(items)} layouts):")
            print("-" * 70)
            
            for name, schema in sorted(items):
                fields_str = ', '.join(schema['fields']) if schema['fields'] else 'none'
                print(f"  {name}")
                print(f"    Fields: {fields_str}")
                print(f"    Complexity: {schema['complexity']}")
                if schema['supports_images']:
                    img_count = sum(1 for f in schema['fields'] if f.startswith('image'))
                    print(f"    Images: {img_count}")


def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python template_schema_builder.py <template.pptx> [output.json]")
        sys.exit(1)
    
    template_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "config/template_schemas.json"
    
    builder = TemplateSchemaBuilder(template_path)
    
    # Print summary
    builder.print_summary()
    
    # Save schemas
    print()
    builder.save_schemas(output_path)


if __name__ == "__main__":
    main()
