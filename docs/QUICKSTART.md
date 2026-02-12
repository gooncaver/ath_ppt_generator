# Quick Start Guide

## Phase 1 MVP - Text to PowerPoint

This guide will help you get started with the basic text-to-slides generator.

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] PowerPoint template file (.pptx) with your desired layouts
- [ ] Virtual environment created

## Step-by-Step Setup

### 1. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Add Your Template

Place your PowerPoint template in the `templates/` folder:
- File name: `base_template.pptx`
- Should have Theme1.thmx applied
- Should contain layouts like "Title and Content", "Title Slide", etc.

### 4. Inspect Your Template

Verify what layouts are available:

```powershell
python src/template_inspector.py templates/base_template.pptx
```

This will output all available layouts and their placeholders.

### 5. Generate Your First Presentation

Use the sample content:

```powershell
python src/mvp_generator.py templates/base_template.pptx examples/sample.md
```

Or use your own markdown file:

```powershell
python src/mvp_generator.py templates/base_template.pptx path/to/your/content.md output/result.pptx
```

### 6. Open and Review

```powershell
start output/presentation_*.pptx
```

## Creating Your Own Content

Create a markdown file with this structure:

```markdown
# Main Title
This will be the first slide

## Section Heading
- Point 1
- Point 2
- Point 3

## Another Section
More content here.
Each line becomes a bullet point.

## Final Thoughts
Conclusion and next steps.
```

## Troubleshooting

### Template Not Found
Make sure your template file is named `base_template.pptx` and is in the `templates/` folder.

### Layout Not Found Warning
The MVP uses "Title and Content" layout by default. If your template doesn't have this exact name, you'll see a warning and it will use the first available layout.

Check available layouts with:
```powershell
python src/template_inspector.py templates/base_template.pptx
```

### Module Not Found
Make sure you've activated the virtual environment and installed dependencies:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## What's Next?

Once Phase 1 MVP is working:
- **Phase 2**: Add AI-powered layout selection with OpenAI GPT-4o
- **Phase 3**: Add image support and intelligent placement
- **Phase 4**: Implement visual feedback loop for quality assurance

## Need Help?

Check the main [README.md](../readme.md) for more detailed documentation.
