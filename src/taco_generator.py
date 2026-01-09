"""Taco Generator module - Generate "uncool" design variations"""

import logging
import random
from typing import List, Tuple, Optional, Dict, Any

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.dml import MSO_FILL_TYPE

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

# Extreme neon color combinations for gradients
EXTREME_NEON_PAIRS = [
    [(255, 0, 127), (0, 255, 255)],      # Hot pink to cyan
    [(255, 255, 0), (255, 0, 0)],        # Yellow to red
    [(0, 255, 0), (148, 0, 211)],        # Lime to blue-violet
    [(255, 127, 0), (255, 0, 127)],      # Orange to pink
    [(0, 255, 255), (255, 255, 0)],      # Cyan to yellow
    [(148, 0, 211), (255, 0, 0)],        # Blue-violet to red
    [(255, 192, 203), (0, 255, 0)],      # Light pink to lime
    [(255, 0, 0), (0, 255, 255)],        # Red to cyan
    [(255, 255, 0), (148, 0, 211)],      # Yellow to blue-violet
    [(255, 127, 0), (0, 255, 0)],        # Orange to lime
]


class TacoGenerator:
    """Generate intentionally uncool design variations of PowerPoint presentations"""
    
    def __init__(self, presentation: Presentation, tacky_level: int = 7, seed: Optional[int] = None):
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
                
                # Apply extreme gradient transformations
                if self.tacky_level >= 5:
                    self._apply_extreme_gradient(shape)
        
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
    
    def _apply_extreme_gradient(self, shape) -> None:
        """Apply extreme gradient fills to shapes with leveled intensity"""
        
        try:
            fill = shape.fill
            
            # Level 5-6: Simple two-color gradients
            if self.tacky_level in [5, 6]:
                self._apply_simple_gradient(fill)
            
            # Level 7-8: More intense multi-color gradients
            elif self.tacky_level in [7, 8]:
                self._apply_multi_color_gradient(fill)
            
            # Level 9-10: Absolutely crazy extreme gradients
            elif self.tacky_level >= 9:
                self._apply_extreme_multi_gradient(fill)
                
            logger.debug(f"Applied gradient (level {self.tacky_level}) to shape")
        except Exception as e:
            logger.debug(f"Could not apply gradient: {e}")
    
    def _apply_simple_gradient(self, fill) -> None:
        """Apply simple two-color gradient (level 5-6)"""
        
        try:
            fill.gradient()
            fill.gradient_angle = self._rand.choice([0, 45, 90, 135, 180, 225, 270, 315])
            
            # Get random extreme color pair
            color_pair = self._rand.choice(EXTREME_NEON_PAIRS)
            
            fill.gradient_stops[0].color.rgb = RGBColor(*color_pair[0])
            fill.gradient_stops[1].color.rgb = RGBColor(*color_pair[1])
            
            logger.debug(f"Applied simple gradient: {color_pair[0]} to {color_pair[1]}")
        except Exception as e:
            logger.debug(f"Could not apply simple gradient: {e}")
    
    def _apply_multi_color_gradient(self, fill) -> None:
        """Apply multi-color gradient with 3-4 color stops (level 7-8)"""
        
        try:
            fill.gradient()
            fill.gradient_angle = self._rand.choice([0, 45, 90, 135, 180, 225, 270, 315])
            
            # Select 3-4 neon colors
            num_colors = self._rand.choice([3, 4])
            colors = self._rand.sample(NEON_COLORS, min(num_colors, len(NEON_COLORS)))
            
            # Clear existing stops and add new ones
            while len(fill.gradient_stops) > 2:
                # Remove extra stops (keep first 2)
                try:
                    fill._element.remove(fill.gradient_stops[2]._element)
                except:
                    break
            
            # Set first two stops
            fill.gradient_stops[0].color.rgb = RGBColor(*colors[0])
            fill.gradient_stops[1].color.rgb = RGBColor(*colors[-1])
            
            # Try to add intermediate stops
            try:
                for i in range(1, len(colors) - 1):
                    # Add gradient stop at position
                    position = i / (len(colors) - 1)
                    try:
                        new_stop = fill.gradient_stops._insert_stop(position)
                        new_stop.color.rgb = RGBColor(*colors[i])
                    except:
                        pass
            except Exception as e:
                logger.debug(f"Could not add intermediate gradient stops: {e}")
            
            logger.debug(f"Applied multi-color gradient with {len(colors)} colors")
        except Exception as e:
            logger.debug(f"Could not apply multi-color gradient: {e}")
    
    def _apply_extreme_multi_gradient(self, fill) -> None:
        """Apply absolutely extreme multi-color gradient (level 9-10)"""
        
        try:
            fill.gradient()
            
            # Randomize angle
            fill.gradient_angle = self._rand.choice([0, 45, 90, 135, 180, 225, 270, 315])
            
            # Use all neon colors in extreme combinations
            colors = NEON_COLORS.copy()
            self._rand.shuffle(colors)
            
            # Set gradient stops
            fill.gradient_stops[0].color.rgb = RGBColor(*colors[0])
            fill.gradient_stops[1].color.rgb = RGBColor(*colors[-1])
            
            # Try to add even more gradient stops for maximum effect
            try:
                for i in range(1, len(colors) - 1):
                    position = i / (len(colors) - 1)
                    try:
                        new_stop = fill.gradient_stops._insert_stop(position)
                        new_stop.color.rgb = RGBColor(*colors[i])
                    except:
                        pass
            except:
                pass
            
            # Extra extreme: apply multiple gradient angles
            if self.tacky_level == 10:
                try:
                    fill.gradient_angle = self._rand.randint(0, 360)
                except:
                    pass
            
            logger.debug(f"Applied extreme multi-gradient with {len(colors)} colors")
        except Exception as e:
            logger.debug(f"Could not apply extreme gradient: {e}")
    
    
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
