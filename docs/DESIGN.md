# AI-Powered PowerPoint Generator - Design Document

**Version**: 0.1.0  
**Date**: February 12, 2026  
**Status**: Phase 1 MVP Implemented

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Phase Implementation Plan](#phase-implementation-plan)
4. [Data Flow](#data-flow)
5. [Core Components](#core-components)
6. [LLM Integration Strategy](#llm-integration-strategy)
7. [Visual Feedback Loop](#visual-feedback-loop)
8. [File Formats & Standards](#file-formats--standards)
9. [Configuration](#configuration)
10. [Testing Strategy](#testing-strategy)

---

## Executive Summary

The AI-Powered PowerPoint Generator is a system that creates professional PowerPoint presentations from multi-modal inputs (text, images, videos) using AI to intelligently organize content, select appropriate layouts, and ensure high-quality output through visual feedback loops.

### Key Capabilities

- **Input Processing**: Parse text (.txt, .md), images (.jpg, .png), videos (.mp4)
- **AI Planning**: Use GPT-4o to organize content into coherent slide structure
- **Layout Intelligence**: Match content to appropriate slide layouts from template
- **Visual Quality Assurance**: LLM reviews generated slides for aesthetics and alignment
- **Complete Coverage**: Ensures ALL input content is utilized in final presentation

### Technology Stack

- **Core**: Python 3.10+
- **PowerPoint**: python-pptx (0.6.23)
- **LLM**: OpenAI GPT-4o (text + vision)
- **Image**: Pillow, OpenCV
- **Config**: YAML, dotenv

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                               │
├─────────────┬─────────────┬─────────────┬──────────────────────┤
│ Text Files  │  Images     │  Videos     │  Design Templates    │
│ (.txt, .md) │ (.jpg, .png)│  (.mp4)     │  (.md)               │
└──────┬──────┴──────┬──────┴──────┬──────┴──────────┬───────────┘
       │             │              │                 │
       ▼             ▼              ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CONTENT PROCESSOR                              │
│  - Parse text (headings, bullets, paragraphs)                   │
│  - Extract image metadata (dimensions, format)                  │
│  - Analyze video frames                                         │
│  - Load design instructions                                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LLM PLANNER (GPT-4o)                        │
│  Input: Content inventory + Available layouts + Instructions    │
│  Output: Slide-by-slide plan with layout assignments           │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SLIDE GENERATOR                              │
│  For each slide in plan:                                        │
│    1. Select template layout                                    │
│    2. Generate placement instructions                           │
│    3. Create slide with python-pptx                             │
│    4. Add text and images                                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              VISUAL REVIEW LOOP (Phase 4)                       │
│  1. Export slide as PNG                                         │
│  2. Send to GPT-4o Vision                                       │
│  3. Check: alignment, overlaps, readability, aesthetics         │
│  4. If issues → adjust and regenerate                           │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FINAL PRESENTATION (.pptx)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase Implementation Plan

### Phase 1: MVP ✅ (COMPLETED)

**Goal**: Basic text-to-slides conversion without AI

**Components**:
- ✅ Project structure setup
- ✅ Template inspector tool
- ✅ MVP generator (text → PowerPoint)
- ✅ Example content
- ✅ Documentation

**Capabilities**:
- Parse markdown/text files
- Split content by headings
- Create slides with "Title and Content" layout
- Save to PowerPoint

**Limitations**:
- No AI/LLM integration
- Single layout type
- No images or videos
- No intelligent content organization

---

### Phase 2: LLM Intelligence (NEXT)

**Goal**: Smart layout selection and content planning

**Components to Build**:
1. **LLM Client** (`src/llm/client.py`)
   - OpenAI API integration
   - Rate limiting and error handling
   - Token usage tracking

2. **Content Planner** (`src/llm/planner.py`)
   - Send content + layouts to GPT-4o
   - Receive structured slide plan
   - Validate plan completeness

3. **Prompt Templates** (`src/llm/prompts.py`)
   - System prompts for content organization
   - Few-shot examples
   - Layout selection guidelines

4. **Smart Generator** (`src/smart_generator.py`)
   - Replace MVP's mechanical splitting
   - Use LLM plan for slide creation
   - Match layouts intelligently

**Deliverables**:
- Presentations with varied layouts
- Better content organization
- Headings placed on appropriate slide types

**Testing**:
- Complex multi-section documents
- Various content types (bullets, paragraphs, mixed)
- Edge cases (very long/short content)

---

### Phase 3: Image Support

**Goal**: Handle images with AI-powered placement

**Components to Build**:
1. **Image Analyzer** (`src/llm/image_analyzer.py`)
   - Use GPT-4o Vision to analyze images
   - Extract: content type, suggested layout, aspect ratio
   - Return placement recommendations

2. **Image Processor** (`src/core/image_processor.py`)
   - Load images with Pillow
   - Extract metadata
   - Resize/optimize for PowerPoint

3. **Content Inventory** (`src/core/content_inventory.py`)
   - Unified structure for all content types
   - Track text, images, videos
   - Mark content as used/unused

4. **Enhanced Generator**
   - Add images to slides
   - Position in placeholders
   - Handle image-heavy vs text-heavy layouts

**Deliverables**:
- Presentations with images
- Intelligent image-to-slide mapping
- Proper image sizing and placement

---

### Phase 4: Visual Feedback Loop

**Goal**: LLM reviews slides for quality

**Components to Build**:
1. **Slide Exporter** (`src/core/slide_exporter.py`)
   - **Manual export workflow** (implemented - most reliable)
   - User-guided PowerPoint export to PNG
   - Metadata storage for review context
   - Export verification and confirmation
   - Fallback: LibreOffice headless or PowerPoint COM

2. **Visual Reviewer** (`src/llm/visual_reviewer.py`)
   - Send slide images to GPT-4o Vision
   - Prompt: "Check for overlaps, alignment, readability"
   - Parse feedback

3. **Adjustment Engine** (`src/core/adjuster.py`)
   - Apply corrections based on feedback
   - Adjust: text size, image position, layout choice
   - Retry mechanism (max 2-3 attempts)

4. **Feedback Loop Integration**
   - After presentation complete → manual export → batch review
   - Log issues and adjustments
   - Track quality metrics

**Deliverables**:
- Reliable cross-platform slide export
- High quality batch review
- Detailed quality logs

---

### Phase 5: Full Feature Set

**Goal**: All inputs, templates, comprehensive generation

**Components to Build**:
1. **Video Support**
   - Extract frames with OpenCV
   - Analyze with GPT-4o Vision
   - Embed videos in slides

2. **Design Templates**
   - Markdown template parser
   - Schema validation
   - Integration into LLM prompts

3. **Purpose Templates**
   - Purpose-driven generation
   - Tone and style adjustments
   - Audience-specific optimization

4. **Coverage Validator**
   - Track all input content
   - Detect unused assets
   - Trigger revision if needed

5. **CLI Interface**
   - Click-based commands
   - `generate`, `validate`, `review` commands
   - Progress indicators

**Deliverables**:
- Complete feature set
- Production-ready tool
- Comprehensive documentation

---

## Data Flow

### Phase 1 MVP (Current)

```
Input File (.md)
    ↓
Parse markdown (split by headings)
    ↓
For each section:
    Create slide with "Title and Content"
    Populate title and bullets
    ↓
Save presentation (.pptx)
```

### Phase 2+ (With LLM)

```
Input Files (text, images, videos)
    ↓
Content Processor
    ↓
Content Inventory {text: [...], images: [...], videos: [...]}
    ↓
LLM Planner (GPT-4o)
    Input: Content + Available Layouts + Design Instructions
    ↓
Slide Plan: [{slide_num, layout, title, content, images, ...}]
    ↓
For each slide in plan:
    ├─ Select layout from template
    ├─ Generate placement instructions (LLM)
    ├─ Create slide (python-pptx)
    ├─ Export as PNG
    ├─ Visual review (GPT-4o Vision)
    ├─ If issues → Adjust → Regenerate
    └─ Add to presentation
    ↓
Validate all content used
    ↓
If unused content → Revision pass
    ↓
Final presentation (.pptx)
```

---

## Core Components

### Template Inspector

**File**: `src/template_inspector.py`

**Purpose**: Discover available slide layouts in PowerPoint template

**Key Methods**:
- `get_slide_layouts()` → List all layouts with metadata
- `print_layouts()` → Display to console
- `save_layout_info()` → Export to text file

**Usage**:
```powershell
python src/template_inspector.py templates/base_template.pptx
```

---

### MVP Generator

**File**: `src/mvp_generator.py`

**Purpose**: Convert text content to basic PowerPoint slides

**Key Methods**:
- `parse_markdown_content()` → Split text into slide sections
- `get_layout_by_name()` → Find layout in template
- `create_slide()` → Generate single slide with content
- `generate_from_file()` → End-to-end generation

**Usage**:
```powershell
python src/mvp_generator.py templates/base_template.pptx examples/sample.md
```

---

### Content Processor (Phase 2)

**File**: `src/core/content_processor.py`

**Purpose**: Parse all input files into unified structure

**Key Methods**:
- `load_text_files()` → Parse .txt/.md files
- `load_images()` → Extract image metadata
- `load_videos()` → Analyze video files
- `chunk_text_content()` → Intelligent text splitting

**Output**: `ContentInventory` object

---

### LLM Planner (Phase 2)

**File**: `src/llm/planner.py`

**Purpose**: Generate slide-by-slide plan using GPT-4o

**Input**:
- Content inventory
- Available layouts
- Design instructions
- Purpose template

**Output**:
```python
[
    {
        "slide_num": 1,
        "layout_name": "Title Slide",
        "title": "Q1 Update",
        "content": [],
        "images": [],
        "notes": "Opening slide"
    },
    {
        "slide_num": 2,
        "layout_name": "Title and Content",
        "title": "Executive Summary",
        "content": ["Point 1", "Point 2", "Point 3"],
        "images": [],
        "notes": "High-level overview"
    },
    # ... more slides
]
```

---

## LLM Integration Strategy

### Prompt Engineering

**Content Planning Prompt**:
```
You are an expert presentation designer. Given the following content and 
available slide layouts, create a comprehensive slide-by-slide plan.

CRITICAL REQUIREMENT: Use ALL provided content across the slides.

Content:
{content_inventory}

Available Layouts:
{layout_list}

Design Instructions:
{design_template}

Purpose:
{purpose_template}

Output a structured plan with:
- slide_num
- layout_name (must match available layouts)
- title
- content (bullets or text)
- image_ids (from content inventory)
- notes

Ensure:
1. Every piece of content is assigned to a slide
2. Layouts match content type appropriately
3. Logical flow and progression
4. Professional structure (intro, body, conclusion)
```

**Image Analysis Prompt**:
```
Analyze this image for PowerPoint slide placement.

Provide:
1. Content description (what does the image show?)
2. Suggested layout type (full image, image+text, etc.)
3. Optimal position (left, right, center, full)
4. Aspect ratio and quality assessment
5. Any text present (OCR)

Output JSON format.
```

**Visual Review Prompt**:
```
Review this PowerPoint slide image for quality issues.

Check for:
1. Overlapping text or images
2. Alignment problems
3. Text readability (size, contrast)
4. Visual balance and aesthetics
5. Spacing issues

Rate: APPROVED or NEEDS_REVISION

If revision needed, specify:
- Issues found
- Suggested fixes
```

---

## Visual Feedback Loop

### Workflow

```
Create Slide
    ↓
Export as PNG (slide_01.png)
    ↓
Send to GPT-4o Vision
    ↓
Parse Feedback
    ↓
Issues Found?
    ├─ Yes → Adjust parameters → Regenerate (max 3 attempts)
    └─ No → Accept slide → Move to next
```

### Adjustments Based on Feedback

| Issue Detected | Adjustment Action |
|----------------|-------------------|
| Overlapping text | Reduce font size or reflow content |
| Image too large | Resize image, adjust placeholder |
| Poor contrast | Change text color or add background |
| Misalignment | Adjust placeholder positions |
| Wrong layout | Switch to different layout template |

### Retry Logic

```python
MAX_RETRIES = 3
attempt = 0

while attempt < MAX_RETRIES:
    slide = create_slide(spec)
    image = export_slide_to_png(slide)
    feedback = review_slide(image)
    
    if feedback.status == "APPROVED":
        break
    
    # Apply adjustments
    spec = adjust_spec(spec, feedback.issues)
    attempt += 1

if attempt == MAX_RETRIES:
    log_warning("Max retries reached, using best attempt")
```

---

## File Formats & Standards

### Input Formats

**Text**:
- `.txt` - Plain text
- `.md` - Markdown (preferred for structured content)

**Images**:
- `.jpg`, `.jpeg` - Photos, compressed images
- `.png` - Diagrams, screenshots (supports transparency)
- `.gif`, `.bmp` - Also supported

**Videos**:
- `.mp4` - Primary format
- `.avi`, `.mov` - Also supported
- Max recommended size: 100MB per video

### Template Formats

**Design Instructions Template** (`design_instructions.md`):
```markdown
---
slides_count_range: 10-15
agenda_required: true
theme_colors:
  primary: "#1E3A8A"
  secondary: "#3B82F6"
  accent: "#EF4444"
font_preferences:
  heading_size: 32pt
  body_size: 18pt
image_placement: centered
spacing_density: balanced
---

# Additional Notes
Place emphasis on visual content over text-heavy slides.
```

**Purpose Template** (`purpose.md`):
```markdown
---
presentation_type: quarterly_update
audience: executive
tone: professional
key_message: "Strong Q1 performance with growth trajectory"
call_to_action: "Approve Phase 2 funding"
---

# Context
This presentation will be delivered to the executive committee
during the Q1 review meeting.
```

### Output Format

- `.pptx` - PowerPoint XML format (Office 2007+)
- Filename pattern: `presentation_YYYYMMDD_HHMMSS.pptx`
- Saved to `output/` directory

---

## Configuration

### Settings File: `config/settings.yaml`

```yaml
template:
  path: "templates/base_template.pptx"
  theme_file: "Themes/Theme1.thmx"

llm:
  provider: "openai"
  model: "gpt-4o"
  max_tokens: 4096
  temperature: 0.7

content:
  text_formats: [".txt", ".md"]
  image_formats: [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
  video_formats: [".mp4", ".avi", ".mov"]

slides:
  default_slides_per_section: 3
  max_bullets_per_slide: 5
  max_chars_per_bullet: 120

output:
  default_directory: "output"
  timestamp_filenames: true
```

### Environment Variables: `.env`

```ini
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
```

---

## Testing Strategy

### Unit Tests

**Test Files**:
- `tests/test_template_inspector.py` - Layout discovery
- `tests/test_content_processor.py` - Text parsing, image loading
- `tests/test_layout_selector.py` - Layout matching logic
- `tests/test_slide_generator.py` - Slide creation

**Coverage Targets**:
- Core modules: 80%+
- Critical paths: 95%+

### Integration Tests

**End-to-End Scenarios**:
1. Text-only presentation
2. Text + images
3. Complex multi-layout presentation
4. Edge cases (empty sections, very long content)

### Manual Testing

**Test Cases**:
- [ ] Template with 5+ layouts
- [ ] Markdown with headings and bullets
- [ ] Multiple images (various sizes)
- [ ] Video embedding
- [ ] Design template parsing
- [ ] Visual review feedback loop

---

## Future Enhancements

### v0.2.0
- Batch processing (multiple presentations)
- Custom layout creation
- Theme extraction and application automation

### v0.3.0
- Web interface
- Real-time preview
- Collaborative editing

### v0.4.0
- Advanced analytics (readability scores, engagement metrics)
- Multi-language support
- Export to PDF/HTML

---

## References

### Libraries Documentation
- [python-pptx](https://python-pptx.readthedocs.io/)
- [OpenAI API](https://platform.openai.com/docs)
- [Pillow](https://pillow.readthedocs.io/)

### Standards
- [Office Open XML (ECMA-376)](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)
- [PowerPoint File Format](https://learn.microsoft.com/en-us/openspecs/office_standards/)

---

**Document Version**: 1.0  
**Last Updated**: February 12, 2026  
**Author**: AI PowerPoint Generator Team
