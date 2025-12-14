"""
POV-Ray Scene Generator

Generates .pov scene files from line segments.
"""

import os
from typing import List, Optional, Tuple
from turtle.interpreter import Segment, BoundingBox


def depth_to_color(depth: int, max_depth: int) -> Tuple[float, float, float]:
    """
    Calculate RGB color based on depth level.
    
    Args:
        depth: Current depth level
        max_depth: Maximum depth in the plant
        
    Returns:
        Tuple of (r, g, b) values from 0.0 to 1.0
    """
    if max_depth == 0:
        max_depth = 1
    
    # Interpolate from trunk color to tip color
    t = depth / max_depth
    
    # Trunk: dark brown-green (0.10, 0.30, 0.05)
    # Tips: bright green (0.40, 0.75, 0.30)
    r = 0.10 + t * (0.40 - 0.10)
    g = 0.30 + t * (0.75 - 0.30)
    b = 0.05 + t * (0.30 - 0.05)
    
    return (r, g, b)


class POVRayGenerator:
    """Generates POV-Ray scene files from segments."""
    
    POV_TEMPLATE = '''// L-System Plant - Generated Scene
#version 3.7;
global_settings {{ assumed_gamma 1.0 }}

background {{ color rgb <1, 1, 1> }}

camera {{
    orthographic
    location <{center_x}, {center_y}, -10>
    look_at <{center_x}, {center_y}, 0>
    up y * {cam_height}
    right x * {cam_width}
}}

light_source {{ <0, 100, -100> color rgb <1, 1, 1> shadowless }}
light_source {{ <{center_x}, {center_y}, -50> color rgb <0.5, 0.5, 0.5> shadowless }}

// Plant geometry
union {{
{geometry}
    // No transformation needed - already in world coordinates
}}
'''
    
    def __init__(
        self,
        output_dir: str = "output/pov",
        width: int = 800,
        height: int = 600,
        padding_percent: float = 0.05
    ):
        """
        Initialize POV-Ray generator.
        
        Args:
            output_dir: Directory to write .pov files
            width: Image width in pixels
            height: Image height in pixels
            padding_percent: Padding around plant as percentage of size
        """
        # Convert to absolute path for Windows compatibility
        self.output_dir = os.path.abspath(output_dir)
        self.width = width
        self.height = height
        self.padding_percent = padding_percent
        
        # Ensure output directory exists
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
        # Skip zero-length segments
        length = segment.length()
        if length < 0.001:
            return ""
        
        # Calculate color based on depth
        r, g, b = depth_to_color(segment.depth, max_depth)
        
        # Calculate radius (decreases with depth)
        radius = base_radius * segment.width
        if radius < 0.05:
            radius = 0.05
        
        lines = []
        
        # Add cylinder for the segment
        lines.append(f"    cylinder {{ <{segment.x1:.6f}, {segment.y1:.6f}, 0>, "
                    f"<{segment.x2:.6f}, {segment.y2:.6f}, 0>, {radius:.4f} "
                    f"pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }} finish {{ ambient 0.3 diffuse 0.7 }} }}")
        
        # Add sphere at end point for smooth joints
        lines.append(f"    sphere {{ <{segment.x2:.6f}, {segment.y2:.6f}, 0>, {radius:.4f} "
                    f"pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }} finish {{ ambient 0.3 diffuse 0.7 }} }}")
        
        return '\n'.join(lines)
    
    def generate_scene(
        self,
        segments: List[Segment],
        bbox: BoundingBox,
        filename: str,
        max_depth: Optional[int] = None
    ) -> str:
        """
        Generate a POV-Ray scene file.
        
        Args:
            segments: List of segments to render
            bbox: Bounding box for camera framing
            filename: Output filename
            max_depth: Maximum depth for coloring (auto-calculated if None)
            
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
            # Wider than tall - fit to width
            cam_width = padded_bbox.width
            cam_height = cam_width / aspect_ratio
        else:
            # Taller than wide - fit to height
            cam_height = padded_bbox.height
            cam_width = cam_height * aspect_ratio
        
        # Calculate base radius proportional to scene size
        scene_scale = max(cam_width, cam_height)
        base_radius = scene_scale * 0.003  # 0.3% of scene size
        
        # Generate geometry for all segments
        geometry_lines = []
        for segment in segments:
            pov_geom = self._segment_to_povray(segment, max_depth, base_radius)
            if pov_geom:
                geometry_lines.append(pov_geom)
        
        # If no geometry, add a tiny invisible sphere to prevent POV-Ray errors
        if not geometry_lines:
            geometry_lines.append("    sphere { <0, 0, 0>, 0.001 pigment { rgb <1, 1, 1> } }")
        
        geometry = '\n'.join(geometry_lines)
        
        # Fill template
        scene = self.POV_TEMPLATE.format(
            center_x=padded_bbox.center_x,
            center_y=padded_bbox.center_y,
            cam_width=cam_width,
            cam_height=cam_height,
            geometry=geometry
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
        max_depth: Optional[int] = None
    ) -> str:
        """
        Generate a single animation frame.
        
        Args:
            segments: Segments to render (may be partial)
            bbox: Bounding box (should be full plant bbox for consistent framing)
            frame_number: Frame number for filename
            max_depth: Maximum depth for coloring
            
        Returns:
            Full path to generated .pov file
        """
        filename = f"frame_{frame_number:05d}.pov"
        return self.generate_scene(segments, bbox, filename, max_depth)