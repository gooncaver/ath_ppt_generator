# Phase 2 Testing Guide

## Prerequisites

1. **OpenAI API Key Required**
   - Sign up at https://platform.openai.com/
   - Create an API key
   - Add to `.env` file: `OPENAI_API_KEY=sk-...`

2. **Template Ready**
   - SavedTheme.pptx in `templates/` folder  
   - 74 layouts available

## Quick Test

### 1. Set Up API Key

Edit `.env` file:
```ini
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4o
```

### 2. Run Smart Generator

```powershell
& "C:/Users/user/OneDrive/Merck/Athinia/Slide Makers/ath_slide_generator/ath_ppt_generator/.venv/Scripts/python.exe" src/smart_generator.py templates/SavedTheme.pptx examples/sample.md output/smart_test.pptx
```

### 3. Expected Output

```
======================================================================
SMART SLIDE GENERATION (Phase 2)
======================================================================

Removing 38 existing slides from template...

Available layouts: 74
Planning slides with AI...
  Tokens used: 2500, Cost: $0.0250

──────────────────────────────────────────────────────────────────────
Generating 14 slides...
──────────────────────────────────────────────────────────────────────

  [1/14] Q1 Athinia Update
      Layout: Title Slide
      Bullets: 0
  [2/14] Executive Summary
      Layout: 10_Title and Content
      Bullets: 3
  ...

======================================================================
✓ Presentation saved to: output/smart_test.pptx
======================================================================

AI Usage Stats:
  Total tokens: 2,500
  Total cost: $0.0250
  API calls: 1
```

## What to Verify

### ✅ AI Planning
- [ ] Multiple layout types used (not just one)
- [ ] Logical slide progression
- [ ] All content from sample.md appears
- [ ] Professional structure

### ✅ Layout Selection
- [ ] Title slide for opening
- [ ] Content layouts for body
- [ ] Appropriate layouts for content type

### ✅ Content Quality
- [ ] Titles are descriptive
- [ ] Bullets are concise
- [ ] Presenter notes added
- [ ] No content duplication

### ✅ Cost & Performance
- [ ] Generation completes in < 30 seconds
- [ ] Cost is < $0.50
- [ ] Token usage reasonable

## Comparison: MVP vs Smart

### MVP (Phase 1)
- Single layout type
- Mechanical section splitting
- No content analysis
- Same structure every time

### Smart (Phase 2)
- Multiple layouts intelligently selected
- AI-powered content organization
- Context-aware structuring
- Varied, professional output

## Troubleshooting

### "OpenAI API key not found"
- Check `.env` file exists
- Verify `OPENAI_API_KEY=sk-...` is set
- Restart terminal after editing .env

### "Layout not found" warnings  
- Normal if LLM suggests generic names
- System automatically maps to closest match
- Check console for mapping messages

### High API costs
- Typical cost: $0.02-0.05 per presentation
- Reduce with smaller `max_tokens`
- Use caching for repeated content

### JSON parse errors
- Rare - LLM occasionally returns invalid JSON
- Retry usually works
- Check prompt templates if persistent

## Advanced Testing

### Test with Different Content

```powershell
# Create your own markdown file
notepad test_content.md

# Generate with target slide count
python src/smart_generator.py templates/SavedTheme.pptx test_content.md output/custom.pptx 10
```

### Test Layout Variety

After generation, check output presentation:
1. Open in PowerPoint
2. View different slide layouts used
3. Compare to what MVP would have created
4. Note improvements in organization

## Success Criteria

✅ **Phase 2 Complete When:**
- [ ] AI planning generates valid slide structure
- [ ] 3+ different layouts used in output
- [ ] All content comprehensively covered
- [ ] Layout selection matches content appropriately
- [ ] Cost per presentation < $0.50
- [ ] Results better than MVP mechanical splitting

## Next Steps

Once Phase 2 validated:
- **Phase 3**: Add image analysis and placement
- **Phase 4**: Visual feedback loop
- **Phase 5**: Full feature set (videos, templates, CLI)

---

**Ready to test?** Set your API key and run the smart generator!
