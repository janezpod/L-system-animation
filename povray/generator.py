"""
POV-Ray Scene Generator

Generates .pov scene files from line segments with enhanced visual effects.
Supports gradient coloring, leaf tips, and improved lighting.
"""

import os
from enum import Enum
from typing import List, Optional, Tuple
from turtle.interpreter import Segment, BoundingBox


class ColorMode(Enum):
    """Coloring styles for plant rendering."""
    DEPTH = "depth"         # Color by branch depth
    GRADIENT = "gradient"   # Base-to-tip gradient
    AUTUMN = "autumn"       # Autumn color palette
    MONOCHROME = "mono"     # Single color (green)


def depth_to_color(depth: int, max_depth: int, color_mode: ColorMode = ColorMode.DEPTH) -> Tuple[float, float, float]:
    """
    Calculate RGB color based on depth level and color mode.
    
    Args:
        depth: Current depth level
        max_depth: Maximum depth in the plant
        color_mode: Coloring style to use
        
    Returns:
        Tuple of (r, g, b) values from 0.0 to 1.0
    """
    if max_depth == 0:
        max_depth = 1
    
    t = depth / max_depth
    
    if color_mode == ColorMode.DEPTH:
        # Trunk: dark brown-green (0.10, 0.30, 0.05)
        # Tips: bright green (0.40, 0.75, 0.30)
        r = 0.10 + t * (0.40 - 0.10)
        g = 0.30 + t * (0.75 - 0.30)
        b = 0.05 + t * (0.30 - 0.05)
    
    elif color_mode == ColorMode.GRADIENT:
        # Similar but with more gradual transition
        r = 0.15 + t * (0.35 - 0.15)
        g = 0.25 + t * (0.70 - 0.25)
        b = 0.08 + t * (0.25 - 0.08)
    
    elif color_mode == ColorMode.AUTUMN:
        # Trunk: brown
        # Tips: orange/red mix
        if t < 0.3:
            r = 0.35 + t * 0.5
            g = 0.20 + t * 0.3
            b = 0.05
        else:
            r = 0.50 + (t - 0.3) * 0.7
            g = 0.30 - (t - 0.3) * 0.25
            b = 0.05 + (t - 0.3) * 0.15
    
    else:  # MONOCHROME
        # All green, varying brightness
        r = 0.15 + t * 0.15
        g = 0.45 + t * 0.25
        b = 0.12 + t * 0.10
    
    return (min(1.0, r), min(1.0, g), min(1.0, b))


def leaf_color(base_color: Tuple[float, float, float], variation: float = 0.1) -> Tuple[float, float, float]:
    """
    Generate a slightly varied leaf color from base branch color.
    
    Args:
        base_color: Base RGB color
        variation: How much to vary the color
        
    Returns:
        Tuple of (r, g, b) for leaf color
    """
    r, g, b = base_color
    # Make leaves slightly yellower and brighter
    r = min(1.0, r + variation * 0.5)
    g = min(1.0, g + variation * 0.3)
    b = max(0.0, b - variation * 0.2)
    return (r, g, b)


class POVRayGenerator:
    """Generates POV-Ray scene files from segments with enhanced visuals."""
    
    POV_TEMPLATE = '''// L-System Plant - Generated Scene
#version 3.7;
global_settings {{ 
    assumed_gamma 1.0
    max_trace_level 5
}}

background {{ color rgb <{bg_r}, {bg_g}, {bg_b}> }}

camera {{
    orthographic
    location <{center_x}, {center_y}, -10>
    look_at <{center_x}, {center_y}, 0>
    up y * {cam_height}
    right x * {cam_width}
}}

// Soft key light (warm sunlight)
light_source {{
    <{light_x}, {light_y}, -30>
    color rgb <1.0, 0.95, 0.90>
    area_light <3, 0, 0>, <0, 3, 0>, 5, 5
    adaptive 1
    jitter
}}

// Cool fill light (sky ambient)
light_source {{
    <{fill_x}, {fill_y}, -15>
    color rgb <0.4, 0.45, 0.55>
    shadowless
}}

// Subtle ground bounce
light_source {{
    <{center_x}, {bbox_min_y}, -5>
    color rgb <0.15, 0.12, 0.10>
    shadowless
}}

// Plant geometry
union {{
{geometry}
}}
'''
    
    LEAF_TEMPLATE = '''    // Leaf at branch tip
    sphere {{
        <{x}, {y}, 0>, {size}
        scale <0.3, 1.0, 0.15>
        rotate <0, 0, {angle}>
        translate <{tx}, {ty}, 0>
        pigment {{ rgb <{r}, {g}, {b}> }}
        finish {{ ambient 0.4 diffuse 0.6 }}
    }}
'''
    
    def __init__(
        self,
        output_dir: str = "output/pov",
        width: int = 800,
        height: int = 600,
        padding_percent: float = 0.05,
        color_mode: ColorMode = ColorMode.DEPTH,
        show_leaves: bool = False,
        background_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ):
        """
        Initialize POV-Ray generator.
        
        Args:
            output_dir: Directory to write .pov files
            width: Image width in pixels
            height: Image height in pixels
            padding_percent: Padding around plant as percentage of size
            color_mode: Coloring style for branches
            show_leaves: Whether to add leaf shapes at branch tips
            background_color: RGB background color
        """
        self.output_dir = os.path.abspath(output_dir)
        self.width = width
        self.height = height
        self.padding_percent = padding_percent
        self.color_mode = color_mode
        self.show_leaves = show_leaves
        self.background_color = background_color
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _segment_to_povray(
        self,
        segment: Segment,
        max_depth: int,
        base_radius: float = 0.3
    ) -> str:
        """
        Convert a segment to POV-Ray geometry.
        
        Args:
            segment: Segment to convert
            max_depth: Maximum depth for color calculation
            base_radius: Base radius for cylinders
            
        Returns:
            POV-Ray SDL string for the segment
        """
        length = segment.length()
        if length < 0.001:
            return ""
        
        r, g, b = depth_to_color(segment.depth, max_depth, self.color_mode)
        
        # Calculate radius (decreases with depth)
        radius = base_radius * segment.width
        if radius < 0.05:
            radius = 0.05
        
        lines = []
        
        # Add cylinder for the segment
        lines.append(f"    cylinder {{ <{segment.x1:.6f}, {segment.y1:.6f}, 0>, "
                    f"<{segment.x2:.6f}, {segment.y2:.6f}, 0>, {radius:.4f} "
                    f"pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }} "
                    f"finish {{ ambient 0.3 diffuse 0.7 }} }}")
        
        # Add sphere at end point for smooth joints
        lines.append(f"    sphere {{ <{segment.x2:.6f}, {segment.y2:.6f}, 0>, {radius:.4f} "
                    f"pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }} "
                    f"finish {{ ambient 0.3 diffuse 0.7 }} }}")
        
        return '\n'.join(lines)
    
    def _leaf_to_povray(
        self,
        segment: Segment,
        max_depth: int,
        leaf_size_mult: float = 3.0
    ) -> str:
        """
        Generate a leaf shape at the tip of a segment.
        
        Args:
            segment: Terminal segment to add leaf to
            max_depth: Maximum depth for color calculation
            leaf_size_mult: Size multiplier for leaves
            
        Returns:
            POV-Ray SDL string for the leaf
        """
        import math
        
        # Get branch color and create leaf color
        branch_color = depth_to_color(segment.depth, max_depth, self.color_mode)
        lr, lg, lb = leaf_color(branch_color)
        
        # Calculate leaf size based on segment width
        leaf_size = segment.width * leaf_size_mult
        if leaf_size < 0.5:
            leaf_size = 0.5
        
        # Calculate angle of segment for leaf orientation
        dx = segment.x2 - segment.x1
        dy = segment.y2 - segment.y1
        angle = math.degrees(math.atan2(dy, dx)) - 90  # Perpendicular to branch
        
        return self.LEAF_TEMPLATE.format(
            x=0, y=0,  # Origin before translation
            size=leaf_size,
            angle=angle,
            tx=segment.x2,
            ty=segment.y2,
            r=lr, g=lg, b=lb
        )
    
    def generate_scene(
        self,
        segments: List[Segment],
        bbox: BoundingBox,
        filename: str,
        max_depth: Optional[int] = None,
        terminal_segments: Optional[List[Segment]] = None
    ) -> str:
        """
        Generate a POV-Ray scene file.
        
        Args:
            segments: List of segments to render
            bbox: Bounding box for camera framing
            filename: Output filename
            max_depth: Maximum depth for coloring (auto-calculated if None)
            terminal_segments: Segments to add leaves to (if show_leaves enabled)
            
        Returns:
            Full path to generated .pov file
        """
        if max_depth is None:
            max_depth = max((seg.depth for seg in segments), default=0)
        
        # Add padding to bounding box
        padded_bbox = bbox.with_padding_percent(self.padding_percent)
        
        # Calculate camera dimensions maintaining aspect ratio
        aspect_ratio = self.width / self.height
        bbox_aspect = padded_bbox.width / padded_bbox.height if padded_bbox.height > 0 else 1
        
        if bbox_aspect > aspect_ratio:
            cam_width = padded_bbox.width
            cam_height = cam_width / aspect_ratio
        else:
            cam_height = padded_bbox.height
            cam_width = cam_height * aspect_ratio
        
        # Calculate base radius proportional to scene size
        scene_scale = max(cam_width, cam_height)
        base_radius = scene_scale * 0.003
        
        # Generate geometry for all segments
        geometry_lines = []
        for segment in segments:
            pov_geom = self._segment_to_povray(segment, max_depth, base_radius)
            if pov_geom:
                geometry_lines.append(pov_geom)
        
        # Add leaves at terminal segments
        if self.show_leaves and terminal_segments:
            for segment in terminal_segments:
                # Only add leaf if segment is fully visible (has some length)
                if segment.length() > 0.1:
                    leaf_geom = self._leaf_to_povray(segment, max_depth, 
                                                     leaf_size_mult=scene_scale * 0.01)
                    geometry_lines.append(leaf_geom)
        
        # If no geometry, add a tiny invisible sphere
        if not geometry_lines:
            geometry_lines.append("    sphere { <0, 0, 0>, 0.001 pigment { rgb <1, 1, 1> } }")
        
        geometry = '\n'.join(geometry_lines)
        
        # Calculate light positions based on scene
        light_x = padded_bbox.center_x - cam_width * 0.3
        light_y = padded_bbox.center_y + cam_height * 0.4
        fill_x = padded_bbox.center_x + cam_width * 0.3
        fill_y = padded_bbox.center_y + cam_height * 0.2
        
        # Fill template
        scene = self.POV_TEMPLATE.format(
            center_x=padded_bbox.center_x,
            center_y=padded_bbox.center_y,
            cam_width=cam_width,
            cam_height=cam_height,
            geometry=geometry,
            light_x=light_x,
            light_y=light_y,
            fill_x=fill_x,
            fill_y=fill_y,
            bbox_min_y=padded_bbox.min_y,
            bg_r=self.background_color[0],
            bg_g=self.background_color[1],
            bg_b=self.background_color[2]
        )
        
        # Write file
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(scene)
        
        return filepath
    
    def generate_frame(
        self,
        segments: List[Segment],
        bbox: BoundingBox,
        frame_number: int,
        max_depth: Optional[int] = None,
        terminal_segments: Optional[List[Segment]] = None
    ) -> str:
        """
        Generate a single animation frame.
        
        Args:
            segments: Segments to render (may be partial)
            bbox: Bounding box (should be full plant bbox for consistent framing)
            frame_number: Frame number for filename
            max_depth: Maximum depth for coloring
            terminal_segments: Terminal segments for leaf rendering
            
        Returns:
            Full path to generated .pov file
        """
        filename = f"frame_{frame_number:05d}.pov"
        return self.generate_scene(segments, bbox, filename, max_depth, terminal_segments)
