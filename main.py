"""Quick start script for DasaMaker"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ppt_analyzer import PPTAnalyzer
from src.taco_generator import TacoGenerator
from src.content_transformer import ContentTransformer
from pptx import Presentation


def main():
    """Main entry point for command-line usage"""
    
    parser = argparse.ArgumentParser(
        description='DasaMaker - Generate tacky PowerPoint presentations'
    )
    parser.add_argument('input_file', help='Input PPTX file path')
    parser.add_argument('-o', '--output', help='Output file path (default: input_TACKY.pptx)')
    parser.add_argument('-d', '--design', type=int, default=7, 
                       help='Design tackiness level (1-10, default=7)')
    parser.add_argument('-c', '--content', type=int, default=7,
                       help='Content transformation intensity (1-10, default=7)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--seed', type=int,
                       help='Deterministic seed for repeatable output (optional)')
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.INFO)
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        return 1
    
    if not args.input_file.lower().endswith('.pptx'):
        print("Error: File must be PPTX format")
        return 1
    
    # Determine output file
    if args.output:
        output_file = args.output
    else:
        base_name = Path(args.input_file).stem
        output_file = f"{base_name}_TACKY.pptx"
    
    try:
        print(f"📂 Loading: {args.input_file}")
        
        # Step 1: Analyze
        print("📊 Analyzing presentation...")
        analyzer = PPTAnalyzer(args.input_file)
        analysis = analyzer.analyze()
        print(f"   ✓ Slides: {analysis.total_slides}")
        print(f"   ✓ Fonts: {len(analysis.fonts)}")
        print(f"   ✓ Colors: {len(analysis.colors)}")
        
        # Step 2: Load for modification
        print("🔧 Loading for modifications...")
        presentation = Presentation(args.input_file)
        
        # Step 3: Apply tacky design
        print(f"🎨 Applying tacky design (level {args.design})...")
        generator = TacoGenerator(presentation, tacky_level=args.design, seed=args.seed)
        generator.apply_tacky_design()
        
        # Step 4: Apply content transformation
        print(f"✍️  Transforming content (intensity {args.content})...")
        transformer = ContentTransformer(presentation, intensity=args.content, seed=args.seed)
        transformer.transform_all_content()
        
        # Step 5: Save
        print(f"💾 Saving: {output_file}")
        presentation.save(output_file)
        
        print(f"\n✨ Complete! Generated: {output_file}")
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
