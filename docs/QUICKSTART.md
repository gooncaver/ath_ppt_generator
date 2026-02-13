# Quick Start Guide

## Phase 3 - AI-Powered Slide Generation

This guide will help you get started with the enhanced AI slide generator featuring schema-guided generation and holistic review.

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

### 5. Set Up OpenAI API Key

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your-key-here
```

### 6. Generate Your First Presentation

Use the AI-powered generator:

```powershell
python src/smart_generator_v3.py templates/SavedTheme.pptx input/your_document.txt output/result.pptx
```7

Or disable holistic review for faster generation:

```powershell
python src/smart_generator_v3.py templates/SavedTheme.pptx input/your_document.txt output/result.pptx --no-review
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

### SSL Certificate Error (Corporate Networks)
If you see `CERTIFICATE_VERIFY_FAILED` or `self-signed certificate in certificate chain` errors:

**Option 1: Configure SSL Certificate Bundle (Recommended)**
Add to your `.env` file:
```
SSL_CERT_FILE=path/to/your/corporate/certificate.pem
REQUESTS_CA_BUNDLE=path/to/your/corporate/certificate.pem
```

**Option 2: Disable SSL Verification (Not Recommended for Production)**
Add to your `.env` file:
```
CURL_CA_BUNDLE=""
```

Or temporarily set environment variable:
```powershell
$env:CURL_CA_BUNDLE=""
python src/smart_generator_v3.py templates/SavedTheme.pptx input/your_document.txt output/result.pptx
```

**Option 3: Contact IT Support**
Request the corporate SSL certificate bundle or proxy configuration for Python development.

### OpenAI API Connection Issues
If you encounter connection errors:
- Verify your API key is correct in `.env`
- Check if you're behind a corporate proxy
- Ensure firewall allows outbound connections to `api.openai.com`
- Test API connectivity: `curl https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_API_KEY"`

### Spurious KeyboardInterrupt Errors
If you see `KeyboardInterrupt` exceptions without pressing any keys:
- **Cause**: Network timeouts or unstable connections causing the HTTP client to hang
- **Solution**: The application now includes automatic retry logic with exponential backoff
- **Workaround**: If the issue persists, try:
  - Using a more stable network connection
  - Reducing input document size to decrease API response time
  - Checking corporate firewall/proxy isn't blocking or throttling OpenAI API calls

### Corporate Firewall Blocking OpenAI
If you receive an HTML response from `appcontrol.merckgroup.com` or similar:
- Your corporate firewall is blocking AI services (category: `url_Cat_Everyday_AI`)
- **Solutions**:
  1. Request IT to whitelist `api.openai.com` for development purposes
  2. Use a personal network/hotspot temporarily
  3. Work with IT to configure approved AI service access

## What's Next?

Once Phase 1 MVP is working:
- **Phase 2**: Add AI-powered layout selection with OpenAI GPT-4o
- **Phase 3**: Add image support and intelligent placement
- **Phase 4**: Implement visual feedback loop for quality assurance

## Need Help?

Check the main [README.md](../readme.md) for more detailed documentation.
