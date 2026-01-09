"""Taco Generator module - Generate "uncool" design variations"""

import logging
import random
from typing import List, Tuple, Optional, Dict, Any

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE

logger = logging.getLogger(__name__)


# Tacky font replacement strategy
TACKY_FONTS = [
    "Comic Sans MS",
    "Papyrus",
    "Impact",
    "Curlz MT",
    "Jokerman",
    "Brush Script MT",
    "Chiller",
    "Lucida Handwriting",
]

# Neon color palette for tacky transformations
NEON_COLORS = [
    (255, 0, 127),    # Hot pink
    (0, 255, 255),    # Cyan
    (255, 255, 0),    # Bright yellow
    (0, 255, 0),      # Lime green
    (255, 127, 0),    # Bright orange
    (255, 0, 0),      # Bright red
    (148, 0, 211),    # Blue-violet
    (255, 192, 203),  # Light pink
]


class TacoGenerator:
    """Generate intentionally uncool design variations of PowerPoint presentations"""
    
    def __init__(self, presentation: Presentation, tacky_level: int = 7, seed: int | None = None):
        """
        Initialize tacky design generator
        
        Args:
            presentation: python-pptx Presentation object
            tacky_level: Intensity of tackiness (1-10), default=7
        """
        self.presentation = presentation
        self.tacky_level = max(1, min(10, tacky_level))  # Clamp to 1-10
        # Deterministic RNG if seed provided
        self._rand = random.Random(seed) if seed is not None else random.Random()
        logger.info(f"TacoGenerator initialized with tackiness level: {self.tacky_level}")
    
    def apply_tacky_design(self) -> None:
        """Apply all tacky design transformations to the presentation"""
        logger.info(f"Applying tacky design transformations (level {self.tacky_level})")
        
        for slide_idx, slide in enumerate(self.presentation.slides):
            logger.info(f"Processing slide {slide_idx + 1}/{len(self.presentation.slides)}")
            self._make_slide_tacky(slide)
    
    def _make_slide_tacky(self, slide) -> None:
        """Apply tacky transformations to a single slide"""
        
        # Apply tacky fonts and colors to text
        for shape in slide.shapes:
            if hasattr(shape, "text_frame"):
                self._tacky_text_transform(shape)
            
            # Apply tacky fill colors to shapes
            if hasattr(shape, "fill") and shape.shape_type != MSO_SHAPE_TYPE.PICTURE:
                self._tacky_fill_transform(shape)
        
        # Apply background color if tackiness is high
        if self.tacky_level >= 6:
            self._apply_tacky_background(slide)
    
    def _tacky_text_transform(self, shape) -> None:
        """Transform text with tacky fonts and colors"""
        
        try:
            text_frame = shape.text_frame
            
            for paragraph in text_frame.paragraphs:
                for run in paragraph.runs:
                    # Replace with tacky font
                    if self.tacky_level >= 3:
                        run.font.name = self._rand.choice(TACKY_FONTS)
                    
                    # Apply tacky color
                    if self.tacky_level >= 5:
                        run.font.color.rgb = RGBColor(*self._rand.choice(NEON_COLORS))
                    
                    # Increase font size for emphasis
                    if self.tacky_level >= 7 and run.font.size:
                        current_size = run.font.size.pt
                        run.font.size = Pt(current_size * 1.3)
                    
                    # Make everything bold and italic for extra tackiness
                    if self.tacky_level >= 8:
                        run.font.bold = True
                        run.font.italic = True
        except Exception as e:
            logger.debug(f"Could not transform text in shape: {e}")
    
    def _tacky_fill_transform(self, shape) -> None:
        """Transform shape fill with tacky colors"""
        
        try:
            if self.tacky_level >= 6:
                shape.fill.solid()
                shape.fill.fore_color.rgb = RGBColor(*self._rand.choice(NEON_COLORS))
        except Exception as e:
            logger.debug(f"Could not transform shape fill: {e}")
    
    def _apply_tacky_background(self, slide) -> None:
        """Apply tacky background color to slide"""
        
        try:
            background = slide.background
            fill = background.fill
            fill.solid()
            # Use a less intense color for background
            fill.fore_color.rgb = RGBColor(200 + self._rand.randint(-50, 50), 
                                          100 + self._rand.randint(-50, 50),
                                          150 + self._rand.randint(-50, 50))
        except Exception as e:
            logger.debug(f"Could not apply background: {e}")
    
    def get_tacky_level(self) -> int:
        """Get current tackiness level (1-10)"""
        return self.tacky_level
    
    def set_tacky_level(self, level: int) -> None:
        """Set tackiness level (1-10)"""
        self.tacky_level = max(1, min(10, level))
        logger.info(f"Tackiness level set to: {self.tacky_level}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Example usage
    # presentation = Presentation("sample.pptx")
    # generator = TacoGenerator(presentation, tacky_level=7)
    # generator.apply_tacky_design()
    # presentation.save("sample_TACKY.pptx")
