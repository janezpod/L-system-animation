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
        background_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        use_sphere_sweep: bool = False,
        render_polygons: bool = True
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
            use_sphere_sweep: Use sphere_sweep for smoother branches (ABOP style)
            render_polygons: Render filled polygons for leaves
        """
        self.output_dir = os.path.abspath(output_dir)
        self.width = width
        self.height = height
        self.padding_percent = padding_percent
        self.color_mode = color_mode
        self.show_leaves = show_leaves
        self.background_color = background_color
        self.use_sphere_sweep = use_sphere_sweep
        self.render_polygons = render_polygons
        self._scene_scale = 1.0  # Updated during scene generation
        
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
    
    def _find_segment_chains(
        self,
        segments: List[Segment],
        tolerance: float = 0.001
    ) -> List[List[Segment]]:
        """
        Group segments into connected chains for sphere_sweep rendering.
        
        Segments are connected if one's endpoint matches another's startpoint.
        
        Args:
            segments: List of segments to group
            tolerance: Distance tolerance for connection matching
            
        Returns:
            List of segment chains
        """
        if not segments:
            return []
        
        used = set()
        chains = []
        
        for i, seg in enumerate(segments):
            if i in used:
                continue
            
            chain = [seg]
            used.add(i)
            
            # Extend forward
            current_end = (seg.x2, seg.y2)
            while True:
                found = False
                for j, other in enumerate(segments):
                    if j in used:
                        continue
                    if (abs(other.x1 - current_end[0]) < tolerance and
                        abs(other.y1 - current_end[1]) < tolerance):
                        chain.append(other)
                        used.add(j)
                        current_end = (other.x2, other.y2)
                        found = True
                        break
                if not found:
                    break
            
            chains.append(chain)
        
        return chains
    
    def _segments_to_sphere_sweep(
        self,
        chain: List[Segment],
        max_depth: int,
        base_radius: float = 0.3
    ) -> str:
        """
        Convert connected segment chain to sphere_sweep.
        
        Sphere sweeps produce smoother branches without visible joints.
        Uses cubic spline for chains of 4+ points, linear otherwise.
        
        Args:
            chain: Connected segments forming a branch
            max_depth: Maximum depth for coloring
            base_radius: Base radius multiplier
            
        Returns:
            POV-Ray SDL string for sphere_sweep
        """
        if len(chain) < 2:
            return self._segment_to_povray(chain[0], max_depth, base_radius)
        
        # Collect control points: (x, y, radius)
        points = [(chain[0].x1, chain[0].y1, chain[0].width)]
        for seg in chain:
            points.append((seg.x2, seg.y2, seg.width))
        
        # Get color from first segment
        r, g, b = depth_to_color(chain[0].depth, max_depth, self.color_mode)
        
        # Choose spline type based on point count
        spline = "cubic_spline" if len(points) >= 4 else "linear_spline"
        
        lines = [f"    sphere_sweep {{ {spline} {len(points)},"]
        for x, y, w in points:
            radius = max(0.02, w * base_radius)
            lines.append(f"        <{x:.4f}, {y:.4f}, 0>, {radius:.4f}")
        lines.append(f"        pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }}")
        lines.append(f"        finish {{ ambient 0.3 diffuse 0.7 }}")
        lines.append("    }")
        
        return '\n'.join(lines)
    
    def _polygon_to_povray(
        self,
        vertices: List[Tuple[float, float]],
        color: Tuple[float, float, float],
        depth: int = 0
    ) -> str:
        """
        Generate POV-Ray polygon from vertices for leaf/petal shapes.
        
        Args:
            vertices: List of (x, y) vertex coordinates
            color: RGB color tuple
            depth: Depth level (for slight z-offset to avoid z-fighting)
            
        Returns:
            POV-Ray SDL string for filled polygon
        """
        if len(vertices) < 3:
            return ""
        
        r, g, b = color
        z_offset = depth * 0.001  # Small offset based on depth
        
        lines = [f"    polygon {{ {len(vertices) + 1},"]
        for x, y in vertices:
            lines.append(f"        <{x:.4f}, {y:.4f}, {z_offset:.4f}>,")
        # Close polygon
        lines.append(f"        <{vertices[0][0]:.4f}, {vertices[0][1]:.4f}, {z_offset:.4f}>")
        lines.append(f"        pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }}")
        lines.append(f"        finish {{ ambient 0.4 diffuse 0.6 }}")
        lines.append("    }")
        
        return '\n'.join(lines)
    
    def _render_polygons_list(
        self,
        polygons: List,  # List[Polygon] from interpreter
        max_depth: int
    ) -> List[str]:
        """
        Render a list of polygons to POV-Ray geometry strings.
        
        Args:
            polygons: List of Polygon objects from turtle interpreter
            max_depth: Maximum depth for color calculation
            
        Returns:
            List of POV-Ray SDL strings for each polygon
        """
        geometry_lines = []
        
        for poly in polygons:
            if not hasattr(poly, 'vertices') or len(poly.vertices) < 3:
                continue
            
            # Get color based on depth and color_index
            depth = getattr(poly, 'depth', 0)
            color_index = getattr(poly, 'color_index', 0)
            
            # Base color from depth
            base_color = depth_to_color(depth, max_depth, self.color_mode)
            
            # Modify color based on color_index (cycle through greens/yellows)
            if color_index > 0:
                r, g, b = base_color
                # Add slight color variation
                hue_shift = (color_index % 5) * 0.05
                r = min(1.0, r + hue_shift)
                g = min(1.0, g + hue_shift * 0.5)
                base_color = (r, g, b)
            
            # Generate leaf-like color
            final_color = leaf_color(base_color, variation=0.15)
            
            pov_geom = self._polygon_to_povray(poly.vertices, final_color, depth)
            if pov_geom:
                geometry_lines.append(pov_geom)
        
        return geometry_lines
    
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
        # Increased from 0.003 to 0.008 for more visible ABOP-style branches
        scene_scale = max(cam_width, cam_height)
        self._scene_scale = scene_scale
        base_radius = scene_scale * 0.008
        
        # Generate geometry for all segments
        geometry_lines = []
        
        if self.use_sphere_sweep:
            # Group segments into chains and render as sphere sweeps
            chains = self._find_segment_chains(segments)
            for chain in chains:
                pov_geom = self._segments_to_sphere_sweep(chain, max_depth, base_radius)
                if pov_geom:
                    geometry_lines.append(pov_geom)
        else:
            # Traditional cylinder rendering
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
    
    def generate_scene_enhanced(
        self,
        segments: List[Segment],
        polygons: List,  # List[Polygon] from interpreter
        bbox: BoundingBox,
        filename: str,
        max_depth: Optional[int] = None,
        terminal_segments: Optional[List[Segment]] = None
    ) -> str:
        """
        Generate a POV-Ray scene with enhanced rendering including polygons.
        
        This is the ABOP-style rendering method that supports filled polygons
        for leaves and other botanical structures.
        
        Args:
            segments: Line segments for branches
            polygons: Filled polygons for leaves (from { } notation)
            bbox: Bounding box for camera framing
            filename: Output filename
            max_depth: Maximum depth for coloring
            terminal_segments: Additional leaf segments
            
        Returns:
            Full path to generated .pov file
        """
        if max_depth is None:
            max_depth = max((seg.depth for seg in segments), default=0)
            if polygons:
                polygon_depths = [getattr(p, 'depth', 0) for p in polygons]
                if polygon_depths:
                    max_depth = max(max_depth, max(polygon_depths))
        
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
        # Increased from 0.003 to 0.008 for more visible ABOP-style branches
        scene_scale = max(cam_width, cam_height)
        self._scene_scale = scene_scale
        base_radius = scene_scale * 0.008
        
        # Generate geometry for all segments
        geometry_lines = []
        
        if self.use_sphere_sweep:
            chains = self._find_segment_chains(segments)
            for chain in chains:
                pov_geom = self._segments_to_sphere_sweep(chain, max_depth, base_radius)
                if pov_geom:
                    geometry_lines.append(pov_geom)
        else:
            for segment in segments:
                pov_geom = self._segment_to_povray(segment, max_depth, base_radius)
                if pov_geom:
                    geometry_lines.append(pov_geom)
        
        # Render polygons (leaves from { } notation)
        if self.render_polygons and polygons:
            polygon_geoms = self._render_polygons_list(polygons, max_depth)
            geometry_lines.extend(polygon_geoms)
        
        # Add leaves at terminal segments
        if self.show_leaves and terminal_segments:
            for segment in terminal_segments:
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
    
    def generate_frame_enhanced(
        self,
        segments: List[Segment],
        bbox: BoundingBox,
        frame_number: int,
        max_depth: Optional[int] = None,
        terminal_segments: Optional[List[Segment]] = None,
        polygons: Optional[List] = None
    ) -> str:
        """Generate animation frame with polygon support."""
        filename = f"frame_{frame_number:05d}.pov"
        return self.generate_scene_enhanced(
            segments, polygons or [], bbox, filename, max_depth, terminal_segments
        )