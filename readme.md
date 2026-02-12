# AI-Powered PowerPoint Generator

An intelligent system for generating professional PowerPoint presentations from text, images, and videos using AI.

## 🚀 Project Status: Phase 1 MVP

Currently implementing the foundational text-to-slides conversion system.

## 📋 Features

### Phase 1: MVP ✅ COMPLETE
- ✅ Project structure setup
- ✅ Template inspection tool
- ✅ Basic text-to-slides conversion
- ✅ Clean generation (removes template slides)

### Phase 2: LLM Intelligence ✅ COMPLETE
- ✅ OpenAI GPT-4o integration
- ✅ Smart layout selection (AI-powered)
- ✅ Intelligent content organization
- ✅ Cost tracking and usage statistics
- ✅ Multiple layout support

### Planned Features
- **Phase 3**: Image support with AI-powered placement
- **Phase 4**: Visual feedback loop for slide quality assurance
- **Phase 5**: Full feature set (videos, templates, comprehensive generation)

## 🛠️ Setup

### Prerequisites
- Python 3.10 or higher
- PowerPoint template file (.pptx or .potx) with desired layouts
- OpenAI API key (for Phase 2+)

### Installation

1. **Clone or navigate to the repository**
```powershell
cd "c:\Users\user\OneDrive\Merck\Athinia\Slide Makers\ath_slide_generator\ath_ppt_generator"
```

2. **Create virtual environment**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment**
```powershell
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. **Add your PowerPoint template**
- Place your `.pptx` template file in the `templates/` folder
- Rename it to `base_template.pptx` or update `config/settings.yaml`

## 📖 Usage

### Inspect Template Layouts

Discover what slide layouts are available in your template:

```powershell
python src/template_inspector.py templates/base_template.pptx
```

Save layout info to file:
```powershell
python src/template_inspector.py templates/base_template.pptx docs/available_layouts.txt
```

### Generate Presentation (MVP)

Convert markdown or text file to PowerPoint:

```powershell
python src/mvp_generator.py templates/SavedTheme.pptx examples/sample.md
```

Specify output file:
```powershell
python src/mvp_generator.py templates/SavedTheme.pptx examples/sample.md output/my_presentation.pptx
```

### Generate with AI (Phase 2 - Smart Generator) ✨

**Requires OpenAI API key in `.env` file**

Convert with intelligent layout selection and content organization:

```powershell
python src/smart_generator.py templates/SavedTheme.pptx examples/sample.md
```

With custom output and target slide count:
```powershell
python src/smart_generator.py templates/SavedTheme.pptx examples/sample.md output/smart.pptx 12
```

Features:
- AI-powered layout selection from 74 available layouts
- Intelligent content organization
- Professional slide structure
- Cost tracking (~$0.02-0.05 per presentation)

## 📁 Project Structure

```2 Complete ✅ | Overall Progress: 40%

For detailed roadmap with tasks, timelines, and metrics, see **[docs/ROADMAP.md](docs/ROADMAP.md)**

### Phase 1: MVP ✅ COMPLETE (Feb 12)
- ✅ Basic text parsing and slide generation
- ✅ Template layout discovery
- ✅ Simple content-to-slide mapping
- ✅ Clean generation (removes template slides)

### Phase 2: LLM Intelligence ✅ COMPLETE (Feb 12)
- ✅ OpenAI GPT-4o integration
- ✅ Smart layout selection
- ✅ Content organization and planning
- ✅ Cost tracking

### Phase 3: Image Support 🔜 NEXT (Feb 13-16)
- Image analysis with GPT-4o Vision
- Intelligent image placement
- Multi-modal content integration

### Phase 4: Visual Feedback Loop (Feb 17-19)
- Slide-to-image conversion
- AI-powered quality review
- Automatic correction and refinement

### Phase 5: Full Feature Set (Feb 20
- ✅ Basic text parsing and slide generation
- ✅ Template layout discovery
- ✅ Simple content-to-slide mapping
- ✅ Clean generation (removes template slides)

### Phase 2: LLM Intelligence 🔜 NEXT (Feb 13-15)
- OpenAI GPT-4o integration
- Smart layout selection
- Content organization and planning

### Phase 3: Image Support (Feb 16-19)
- Image analysis with GPT-4o Vision
- Intelligent image placement
- Multi-modal content integration

### Phase 4: Visual Feedback Loop (Feb 20-22)
- Slide-to-image conversion
- AI-powered quality review
- Automatic correction and refinement

### Phase 5: Full Feature Set (Feb 23-28)
- Video content support
- Design instruction templates
- Purpose-driven generation
- Complete content coverage validation

**Target v1.0 Release**: March 1, 2026

## 🧪 Testing

Example test workflow:

```powershell
# 1. Inspect your template
python src/template_inspector.py templates/base_template.pptx

# 2. Generate from sample content
python src/mvp_generator.py templates/base_template.pptx examples/sample.md

# 3. Open the generated file
start output/presentation_*.pptx
```

## 📝 Input Format

The MVP generator supports markdown-style content:

```markdown
# Main Title

## Section 1
- Bullet point 1
- Bullet point 2
- Bullet point 3

## Section 2
Content can also be plain paragraphs.
Each line will become a bullet point on the slide.
```

## ⚙️ Configuration

Edit `config/settings.yaml` to customize:
- Template file paths
- LLM settings (for Phase 2+)
- Output preferences
- Supported file formats

## 🤝 Contributing

This is an internal Merck project. For questions or issues, contact the development team.

## 📄 License

Internal use only - Merck & Co., Inc.

## 🔜 Next Steps

1. **Add your template**: Place your PowerPoint template in `templates/base_template.pptx`
2. **Test MVP**: Run the example generation
3. **Provide feedback**: Help shape Phase 2 development

---
2.0 (Phase 2 Complete
**Current Version**: 0.1.0 (Phase 1 MVP)  
**Last Updated**: February 12, 2026
