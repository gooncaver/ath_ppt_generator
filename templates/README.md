# IMPORTANT: Add your PowerPoint template here

Please add your PowerPoint template file (.pptx or .potx) to this folder and name it `base_template.pptx`.

## Requirements:

1. The template should have Theme1.thmx applied (from the Themes/ folder)
2. It should contain all the slide layouts you want to use:
   - Title Slide
   - Title and Content
   - Two Column
   - Title Only
   - Full Image
   - etc.

## How to create the template:

1. Open PowerPoint
2. Apply Theme1.thmx (Design tab → Themes → Browse for Themes)
3. Go to View → Slide Master
4. Create/customize the slide layouts you need
5. Save as `base_template.pptx` in this folder

## Verify your template:

Once added, you can inspect it using:
```powershell
python src/template_inspector.py templates/base_template.pptx
```

This will show you all available layouts and their placeholders.
