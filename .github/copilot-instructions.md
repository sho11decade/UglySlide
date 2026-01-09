# DasaMaker - AI Coding Assistant Instructions

## Project Overview
**DasaMaker** (UglySlide) is a humor-driven utility that analyzes PowerPoint presentations and generates intentionally "uncool" versions. The project aims to raise design awareness through satire.

### Core Value Proposition
- Input: User's PowerPoint file (PPTX)
- Process: Analyze design elements and content structure
- Output: Generate a "tacky" version with intentional poor design choices and satirical content modifications

## Architecture & Data Flow

### Three-Layer Architecture
1. **UI Layer**: Tkinter (desktop) or Flask (web application)
2. **Processing Layer**: PPT analysis and generation logic using python-pptx
3. **File Handling**: PPTX parsing and creation

### Key Processing Pipeline
```
User uploads PPTX → Analyze design elements → Generate "uncool" variations → Return modified PPTX
```

### Design Analysis Components
- **Font Analysis**: Identify current fonts and intentionally replace with unflattering alternatives
- **Color Extraction**: Extract color schemes and apply exaggerated/clashing palettes
- **Layout Parsing**: Understand slide layouts to introduce awkward positioning
- **Animation Detection**: Note existing animations to add excessive/jarring effects

### Content Transformation Rules
- Add redundant/verbose explanations to every point
- Introduce unnecessary corporate jargon or outdated language
- Insert irrelevant information or tangentially related facts
- Modify tone to be overly casual or inappropriately formal

## Tech Stack

### Core Dependencies
- **python-pptx**: For PPTX file parsing and generation
- **Tkinter** or **Flask**: UI layer (choose one per deployment)
- **Python 3.8+**: Base language

### Key Files to Create
- `src/ppt_analyzer.py`: Core PPT parsing and design element extraction
- `src/taco_generator.py`: Logic for generating "uncool" design variations
- `src/content_transformer.py`: Satirical content modification functions
- `ui/app.py` (Tkinter) or `web/app.py` (Flask): User interface entry point

## Developer Patterns & Conventions

### PPT Element Handling
Use python-pptx's object model:
- Access slide layouts: `presentation.slides[i]`
- Modify text: `shape.text_frame.paragraphs[0].text`
- Change colors: Use `RGBColor(r, g, b)` for explicit color tuples
- Access font properties: `paragraph.runs[0].font`

### Design "Uncoolness" Strategy
- **Before modifying**: Log original design specs (fonts, colors, sizes) for comparison
- **Exaggeration principle**: Take good design choices and push them to extremes
  - Professional sans-serif → Comic Sans or Papyrus
  - Subtle color scheme → High-contrast neon combinations
  - Minimal animation → Every element animates with sound effects
  
### File Management
- Store uploaded files in a temporary directory with UUID-based naming
- Always generate output files with clear naming: `original_name_TACKY.pptx`
- Clean up temporary files after download to prevent disk bloat

### Error Handling
- Validate PPTX structure before processing (corrupted files should fail gracefully)
- Preserve original file integrity—always work on copies
- Log specific slide/element failures for debugging but continue processing other slides

## Development Workflow

### Getting Started
1. Install dependencies: `pip install python-pptx flask` (or skip Flask if using Tkinter)
2. Create sample test PPTX files with various design patterns for testing
3. Start with `src/ppt_analyzer.py` to validate PPT parsing

### Testing Strategy
- Create test presentations with known design patterns
- Validate that design elements are correctly extracted
- Manual review of generated "tacky" versions to ensure satire is effective
- Test with edge cases: very large presentations, unusual fonts, complex animations

### Build & Deployment Notes
- For Tkinter: Single-file desktop executable; can be packaged with PyInstaller
- For Flask: Run with `flask run` in development; deploy with Gunicorn or similar in production
- PPTX file size can impact performance—implement progress indication for large files

## Important Considerations

### Humor & Appropriateness
- The "uncool" transformations should be clearly satirical, not genuinely harmful
- Avoid offensive stereotypes or targeting specific groups
- Maintain the educational purpose (raising design awareness) over pure mockery

### Performance
- PPT analysis scales with slide count—implement progress callbacks for UX feedback
- Color palette generation should be deterministic for reproducibility
- Cache design analysis results if generating multiple versions

### User Experience
- Provide clear before/after comparison in output
- Allow customization level (mild vs. extreme tackiness)
- Handle various PPTX template structures gracefully

## References
- See [ProjectProposal.md](../ProjectProposal.md) for detailed feature specifications
- python-pptx documentation: https://python-pptx.readthedocs.io/
