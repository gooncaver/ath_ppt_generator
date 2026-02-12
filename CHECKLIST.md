# Getting Started Checklist

Follow these steps to get your AI PowerPoint Generator running:

## ✅ Setup (One-time)

- [x] Python 3.10+ installed ✓
- [x] Virtual environment created (.venv) ✓
- [x] Dependencies installed ✓
- [ ] PowerPoint template added to `templates/base_template.pptx`
- [ ] Template has Theme1.thmx applied
- [ ] Template has multiple slide layouts (10-20)

## ✅ Testing Phase 1 MVP

- [ ] Run template inspector:
  ```powershell
  python src/template_inspector.py templates/base_template.pptx
  ```
  
- [ ] Verify layouts listed (should see at least 5+ layouts)

- [ ] Generate sample presentation:
  ```powershell
  python src/mvp_generator.py templates/base_template.pptx examples/sample.md
  ```

- [ ] Open generated file:
  ```powershell
  start output/presentation_*.pptx
  ```

- [ ] Verify in PowerPoint:
  - [ ] Presentation opens without errors
  - [ ] Theme is correctly applied
  - [ ] Multiple slides created (~10 slides from sample.md)
  - [ ] Titles match content sections
  - [ ] Bullet points populated
  - [ ] Professional appearance

## ✅ Create Your Own Presentation

- [ ] Create your content file (markdown format)
- [ ] Run generator with your content:
  ```powershell
  python src/mvp_generator.py templates/base_template.pptx path/to/your/file.md output/my_presentation.pptx
  ```
- [ ] Review output
- [ ] Confirm it meets your needs

## ✅ Ready for Phase 2?

If Phase 1 MVP works for you:
- [ ] MVP successfully generates presentations
- [ ] Theme application works correctly
- [ ] Content organization is acceptable
- [ ] Ready to add AI-powered features

**Next**: Phase 2 will add GPT-4o integration for smart layout selection and content planning.

## 🆘 Need Help?

- **Documentation**: See [readme.md](../readme.md)
- **Quick Start**: See [docs/QUICKSTART.md](QUICKSTART.md)
- **Design Details**: See [docs/DESIGN.md](DESIGN.md)
- **Phase 1 Summary**: See [docs/PHASE1_COMPLETE.md](PHASE1_COMPLETE.md)

## 📝 Current Status

**Phase 1 MVP**: ✅ Complete  
**Your Progress**: ⏳ Add template → Test → Proceed

---

*Last updated: February 12, 2026*
