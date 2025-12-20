"""
3D POV-Ray Scene Generator

Generates .pov scene files from 3D line segments.
Supports 3D camera positioning, sphere sweeps, and camera animation.
"""

import os
import math
from typing import List, Optional, Tuple
from turtle.interpreter3d import Segment3D, BoundingBox3D


def depth_to_color_3d(depth: int, max_depth: int) -> Tuple[float, float, float]:
    """
    Calculate RGB color based on depth level for 3D rendering.
    
    Args:
        depth: Current depth level
        max_depth: Maximum depth in the plant
        
    Returns:
        Tuple of (r, g, b) values from 0.0 to 1.0
    """
    if max_depth == 0:
        max_depth = 1
    
    t = depth / max_depth
    
    # Trunk: dark brown (0.25, 0.15, 0.08)
    # Tips: bright green (0.30, 0.65, 0.20)
    r = 0.25 + t * (0.30 - 0.25)
    g = 0.15 + t * (0.65 - 0.15)
    b = 0.08 + t * (0.20 - 0.08)
    
    return (r, g, b)


class POVRayGenerator3D:
    """Generates POV-Ray scene files from 3D segments."""
    
    POV_TEMPLATE = '''// L-System 3D Plant - Generated Scene
#version 3.7;
global_settings {{ 
    assumed_gamma 1.0
    max_trace_level 8
    ambient_light rgb <0.3, 0.3, 0.3>
}}

background {{ 
    color rgb <{bg_r}, {bg_g}, {bg_b}>
}}

{camera}

// Sun-like key light (warm)
light_source {{
    <{sun_x}, {sun_y}, {sun_z}>
    color rgb <1.0, 0.95, 0.85>
    area_light <5, 0, 0>, <0, 0, 5>, 5, 5
    adaptive 1
    jitter
}}

// Sky ambient light (cool blue from above)
light_source {{
    <{center_x}, {center_y} + {scene_scale} * 2, {center_z}>
    color rgb <0.35, 0.40, 0.55>
    shadowless
}}

// Ground bounce light (warm from below)
light_source {{
    <{center_x}, {bbox_min_y}, {center_z}>
    color rgb <0.20, 0.15, 0.10>
    shadowless
}}

// Back fill light
light_source {{
    <{center_x} - {scene_scale}, {center_y}, {center_z} + {scene_scale}>
    color rgb <0.25, 0.30, 0.35>
    shadowless
}}

// Plant geometry
union {{
{geometry}
}}
'''
    
    PERSPECTIVE_CAMERA = '''camera {{
    location <{cam_x}, {cam_y}, {cam_z}>
    look_at <{look_x}, {look_y}, {look_z}>
    up y
    right x * (image_width/image_height)
    angle {fov}
}}'''
    
    ORTHOGRAPHIC_CAMERA = '''camera {{
    orthographic
    location <{cam_x}, {cam_y}, {cam_z}>
    look_at <{look_x}, {look_y}, {look_z}>
    up y * {cam_height}
    right x * {cam_width}
}}'''
    
    LEAF_TEMPLATE = '''    // Leaf at branch tip
    triangle {{
        <{x1}, {y1}, {z1}>,
        <{x2}, {y2}, {z2}>,
        <{x3}, {y3}, {z3}>
        pigment {{ rgb <{r}, {g}, {b}> }}
        finish {{ ambient 0.4 diffuse 0.6 }}
    }}
'''
    
    def __init__(
        self,
        output_dir: str = "output/pov",
        width: int = 800,
        height: int = 600,
        padding_percent: float = 0.1,
        camera_angle: float = 30.0,
        camera_distance: float = 2.0,
        camera_height: float = 0.5,
        use_perspective: bool = True,
        fov: float = 45.0,
        background_color: Tuple[float, float, float] = (0.85, 0.90, 0.95),
        show_leaves: bool = False,
        animate_camera: bool = False,
        camera_rotation: float = 360.0
    ):
        """
        Initialize 3D POV-Ray generator.
        
        Args:
            output_dir: Directory to write .pov files
            width: Image width in pixels
            height: Image height in pixels
            padding_percent: Padding around plant
            camera_angle: Initial camera orbit angle in degrees (horizontal)
            camera_distance: Camera distance multiplier
            camera_height: Camera height multiplier (0.5 = middle of plant)
            use_perspective: Use perspective camera (False = orthographic)
            fov: Field of view in degrees (perspective only)
            background_color: RGB background color
            show_leaves: Add leaf shapes at terminal segments
            animate_camera: Rotate camera during animation
            camera_rotation: Total camera rotation over animation (degrees)
        """
        self.output_dir = os.path.abspath(output_dir)
        self.width = width
        self.height = height
        self.padding_percent = padding_percent
        self.camera_angle = camera_angle
        self.camera_distance = camera_distance
        self.camera_height = camera_height
        self.use_perspective = use_perspective
        self.fov = fov
        self.background_color = background_color
        self.show_leaves = show_leaves
        self.animate_camera = animate_camera
        self.camera_rotation = camera_rotation
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _calculate_camera_position(
        self,
        bbox: BoundingBox3D,
        frame: int = 0,
        total_frames: int = 1
    ) -> Tuple[float, float, float, float, float, float]:
        """
        Calculate camera position for a given frame.
        
        Returns:
            Tuple of (cam_x, cam_y, cam_z, look_x, look_y, look_z)
        """
        center = bbox.center
        scene_scale = bbox.max_dimension
        
        # Calculate camera orbit angle
        if self.animate_camera and total_frames > 1:
            angle_offset = (frame / (total_frames - 1)) * self.camera_rotation
        else:
            angle_offset = 0
        
        angle_rad = math.radians(self.camera_angle + angle_offset)
        
        # Camera position
        distance = scene_scale * self.camera_distance
        cam_x = center[0] + distance * math.sin(angle_rad)
        cam_z = center[2] + distance * math.cos(angle_rad)
        cam_y = center[1] + scene_scale * self.camera_height
        
        # Look at plant center
        look_x, look_y, look_z = center
        
        return (cam_x, cam_y, cam_z, look_x, look_y, look_z)
    
    def _segment_to_povray(
        self,
        segment: Segment3D,
        max_depth: int,
        base_radius: float = 0.3
    ) -> str:
        """
        Convert a 3D segment to POV-Ray geometry.
        
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
        
        # Color palette for segments (matching polygon palette)
        COLOR_PALETTE = [
            None,                     # 0: use depth-based color
            (1.00, 0.85, 0.10),       # 1: sunflower yellow
            (0.45, 0.30, 0.15),       # 2: brown (seeds)
            (0.85, 0.15, 0.15),       # 3: red
            (1.00, 0.60, 0.70),       # 4: pink
            (1.00, 0.55, 0.10),       # 5: orange
            (0.70, 0.40, 0.80),       # 6: purple
            (0.95, 0.95, 0.95),       # 7: white
        ]
        
        # Check if segment has color_index set
        color_index = getattr(segment, 'color_index', 0)
        if color_index > 0 and color_index < len(COLOR_PALETTE) and COLOR_PALETTE[color_index]:
            r, g, b = COLOR_PALETTE[color_index]
        else:
            r, g, b = depth_to_color_3d(segment.depth, max_depth)
        
        # Calculate radius
        radius = base_radius * segment.width
        if radius < 0.02:
            radius = 0.02
        
        lines = []
        
        # Cylinder for segment
        lines.append(
            f"    cylinder {{ "
            f"<{segment.x1:.6f}, {segment.y1:.6f}, {segment.z1:.6f}>, "
            f"<{segment.x2:.6f}, {segment.y2:.6f}, {segment.z2:.6f}>, {radius:.4f} "
            f"pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }} "
            f"finish {{ ambient 0.25 diffuse 0.75 specular 0.1 }} }}"
        )
        
        # Sphere at endpoints for smooth joints
        lines.append(
            f"    sphere {{ "
            f"<{segment.x2:.6f}, {segment.y2:.6f}, {segment.z2:.6f}>, {radius:.4f} "
            f"pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }} "
            f"finish {{ ambient 0.25 diffuse 0.75 specular 0.1 }} }}"
        )
        
        return '\n'.join(lines)
    
    def _leaf_to_povray(
        self,
        segment: Segment3D,
        max_depth: int,
        leaf_size: float = 1.0
    ) -> str:
        """
        Generate a leaf triangle at the tip of a segment.
        
        Args:
            segment: Terminal segment to add leaf to
            max_depth: Maximum depth for color
            leaf_size: Size of leaf
            
        Returns:
            POV-Ray SDL string for the leaf
        """
        # Get direction of segment
        dx = segment.x2 - segment.x1
        dy = segment.y2 - segment.y1
        dz = segment.z2 - segment.z1
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        if length < 0.001:
            return ""
        
        # Normalize direction
        dx, dy, dz = dx/length, dy/length, dz/length
        
        # Create perpendicular vectors for leaf plane
        # Use cross product with up vector (0, 1, 0)
        px = -dz
        py = 0
        pz = dx
        p_len = math.sqrt(px*px + pz*pz)
        if p_len < 0.001:
            px, py, pz = 1, 0, 0
        else:
            px, py, pz = px/p_len, py/p_len, pz/p_len
        
        # Leaf color (slightly yellower green)
        r = 0.35
        g = 0.70
        b = 0.20
        
        # Triangle vertices
        tip_x = segment.x2 + dx * leaf_size
        tip_y = segment.y2 + dy * leaf_size
        tip_z = segment.z2 + dz * leaf_size
        
        left_x = segment.x2 + px * leaf_size * 0.3
        left_y = segment.y2 + py * leaf_size * 0.3
        left_z = segment.z2 + pz * leaf_size * 0.3
        
        right_x = segment.x2 - px * leaf_size * 0.3
        right_y = segment.y2 - py * leaf_size * 0.3
        right_z = segment.z2 - pz * leaf_size * 0.3
        
        return self.LEAF_TEMPLATE.format(
            x1=segment.x2, y1=segment.y2, z1=segment.z2,
            x2=tip_x, y2=tip_y, z2=tip_z,
            x3=left_x, y3=left_y, z3=left_z,
            r=r, g=g, b=b
        ) + self.LEAF_TEMPLATE.format(
            x1=segment.x2, y1=segment.y2, z1=segment.z2,
            x2=tip_x, y2=tip_y, z2=tip_z,
            x3=right_x, y3=right_y, z3=right_z,
            r=r, g=g, b=b
        )
    
    def _polygon_to_povray_3d(
        self,
        vertices: List[Tuple[float, float, float]],
        color: Tuple[float, float, float]
    ) -> str:
        """
        Generate POV-Ray polygon from 3D vertices for leaf/petal shapes.
        
        Args:
            vertices: List of (x, y, z) vertex coordinates
            color: RGB color tuple
            
        Returns:
            POV-Ray SDL string for filled polygon
        """
        if len(vertices) < 3:
            return ""
        
        r, g, b = color
        
        lines = [f"    polygon {{ {len(vertices) + 1},"]
        for x, y, z in vertices:
            lines.append(f"        <{x:.4f}, {y:.4f}, {z:.4f}>,")
        # Close polygon
        lines.append(f"        <{vertices[0][0]:.4f}, {vertices[0][1]:.4f}, {vertices[0][2]:.4f}>")
        lines.append(f"        pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }}")
        lines.append(f"        finish {{ ambient 0.4 diffuse 0.6 }}")
        lines.append("    }")
        
        return '\n'.join(lines)
    
    def _render_polygons_list_3d(
        self,
        polygons: List,  # List[Polygon3D] from interpreter3d
        max_depth: int
    ) -> List[str]:
        """
        Render a list of 3D polygons to POV-Ray geometry strings.
        
        Args:
            polygons: List of Polygon3D objects from turtle interpreter
            max_depth: Maximum depth for color calculation
            
        Returns:
            List of POV-Ray SDL strings for each polygon
        """
        geometry_lines = []
        
        # Color palette for different plant parts
        # color_index 0 = leaf green
        # color_index 1 = yellow (petals)
        # color_index 2 = brown (seeds/center)
        # color_index 3 = red (flowers)
        # color_index 4 = pink
        # color_index 5 = orange
        COLOR_PALETTE = [
            (0.30, 0.55, 0.20),  # 0: leaf green
            (1.00, 0.85, 0.10),  # 1: sunflower yellow
            (0.45, 0.30, 0.15),  # 2: brown (seeds)
            (0.85, 0.15, 0.15),  # 3: red
            (1.00, 0.60, 0.70),  # 4: pink
            (1.00, 0.55, 0.10),  # 5: orange
            (0.70, 0.40, 0.80),  # 6: purple
            (0.95, 0.95, 0.95),  # 7: white
        ]
        
        for poly in polygons:
            if not hasattr(poly, 'vertices') or len(poly.vertices) < 3:
                continue
            
            # Get depth and color_index
            depth = getattr(poly, 'depth', 0)
            color_index = getattr(poly, 'color_index', 0)
            
            # Use color palette if color_index is set, otherwise depth-based green
            if color_index > 0 and color_index < len(COLOR_PALETTE):
                r, g, b = COLOR_PALETTE[color_index]
            else:
                # Default depth-based leaf green
                t = depth / max_depth if max_depth > 0 else 0
                r = 0.25 + t * 0.15
                g = 0.50 + t * 0.25
                b = 0.15 + t * 0.10
            
            pov_geom = self._polygon_to_povray_3d(poly.vertices, (r, g, b))
            if pov_geom:
                geometry_lines.append(pov_geom)
        
        return geometry_lines
    
    def generate_scene(
        self,
        segments: List[Segment3D],
        bbox: BoundingBox3D,
        filename: str,
        max_depth: Optional[int] = None,
        terminal_segments: Optional[List[Segment3D]] = None,
        frame: int = 0,
        total_frames: int = 1,
        polygons: Optional[List] = None
    ) -> str:
        """
        Generate a POV-Ray 3D scene file.
        
        Args:
            segments: List of 3D segments to render
            bbox: Bounding box for camera framing
            filename: Output filename
            max_depth: Maximum depth for coloring
            terminal_segments: Segments for leaf rendering
            frame: Current frame number (for camera animation)
            total_frames: Total frames (for camera animation)
            polygons: List of Polygon3D objects for leaf/petal rendering
            
        Returns:
            Full path to generated .pov file
        """
        if max_depth is None:
            max_depth = max((seg.depth for seg in segments), default=0)
            # Also consider polygon depths
            if polygons:
                polygon_depths = [getattr(p, 'depth', 0) for p in polygons]
                if polygon_depths:
                    max_depth = max(max_depth, max(polygon_depths))
        
        padded_bbox = bbox.with_padding_percent(self.padding_percent)
        center = padded_bbox.center
        scene_scale = padded_bbox.max_dimension
        
        # Calculate camera
        cam_pos = self._calculate_camera_position(padded_bbox, frame, total_frames)
        
        if self.use_perspective:
            camera = self.PERSPECTIVE_CAMERA.format(
                cam_x=cam_pos[0], cam_y=cam_pos[1], cam_z=cam_pos[2],
                look_x=cam_pos[3], look_y=cam_pos[4], look_z=cam_pos[5],
                fov=self.fov
            )
        else:
            aspect_ratio = self.width / self.height
            cam_height = scene_scale * 1.2
            cam_width = cam_height * aspect_ratio
            camera = self.ORTHOGRAPHIC_CAMERA.format(
                cam_x=cam_pos[0], cam_y=cam_pos[1], cam_z=cam_pos[2],
                look_x=cam_pos[3], look_y=cam_pos[4], look_z=cam_pos[5],
                cam_height=cam_height, cam_width=cam_width
            )
        
        # Calculate base radius - increased for more visible ABOP-style branches
        base_radius = scene_scale * 0.010
        
        # Generate geometry
        geometry_lines = []
        for segment in segments:
            pov_geom = self._segment_to_povray(segment, max_depth, base_radius)
            if pov_geom:
                geometry_lines.append(pov_geom)
        
        # Add leaves
        if self.show_leaves and terminal_segments:
            leaf_size = scene_scale * 0.02
            for segment in terminal_segments:
                if segment.length() > 0.1:
                    leaf_geom = self._leaf_to_povray(segment, max_depth, leaf_size)
                    geometry_lines.append(leaf_geom)
        
        # Render polygons (leaves/petals from { } notation)
        if polygons:
            polygon_geoms = self._render_polygons_list_3d(polygons, max_depth)
            geometry_lines.extend(polygon_geoms)
        
        if not geometry_lines:
            geometry_lines.append("    sphere { <0, 0, 0>, 0.001 pigment { rgb <1, 1, 1> } }")
        
        geometry = '\n'.join(geometry_lines)
        
        # Light positions
        sun_x = center[0] + scene_scale * 1.5
        sun_y = center[1] + scene_scale * 2.0
        sun_z = center[2] - scene_scale * 2.0
        
        # Fill template
        scene = self.POV_TEMPLATE.format(
            camera=camera,
            center_x=center[0],
            center_y=center[1],
            center_z=center[2],
            scene_scale=scene_scale,
            bbox_min_y=padded_bbox.min_y,
            sun_x=sun_x, sun_y=sun_y, sun_z=sun_z,
            geometry=geometry,
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
        segments: List[Segment3D],
        bbox: BoundingBox3D,
        frame_number: int,
        max_depth: Optional[int] = None,
        terminal_segments: Optional[List[Segment3D]] = None,
        total_frames: int = 100,
        polygons: Optional[List] = None
    ) -> str:
        """
        Generate a single animation frame.
        
        Args:
            segments: Segments to render
            bbox: Bounding box for consistent framing
            frame_number: Frame number for filename
            max_depth: Maximum depth for coloring
            terminal_segments: Terminal segments for leaves
            total_frames: Total frames for camera animation
            polygons: Polygon objects for leaf/petal rendering
            
        Returns:
            Full path to generated .pov file
        """
        filename = f"frame_{frame_number:05d}.pov"
        return self.generate_scene(
            segments, bbox, filename, max_depth, terminal_segments,
            frame=frame_number, total_frames=total_frames,
            polygons=polygons
        )
    
    def generate_frame_enhanced(
        self,
        segments: List[Segment3D],
        bbox: BoundingBox3D,
        frame_number: int,
        max_depth: Optional[int],
        terminal_segments: Optional[List[Segment3D]] = None,
        polygons: Optional[List] = None
    ) -> str:
        """
        Enhanced frame generation with polygon support.
        
        This method is called when --render-polygons is used without --animate-camera.
        Provides full polygon rendering for ABOP-style leaves and petals.
        
        Args:
            segments: Segments to render
            bbox: Bounding box for consistent framing
            frame_number: Frame number for filename
            max_depth: Maximum depth for coloring
            terminal_segments: Terminal segments for leaves
            polygons: Polygon objects for leaf/petal rendering
            
        Returns:
            Full path to generated .pov file
        """
        filename = f"frame_{frame_number:05d}.pov"
        return self.generate_scene(
            segments, bbox, filename, max_depth, terminal_segments,
            frame=frame_number, total_frames=1,  # No camera animation in enhanced mode
            polygons=polygons
        )
    
    def generate_scene_enhanced(
        self,
        segments: List[Segment3D],
        bbox: BoundingBox3D,
        filename: str,
        max_depth: Optional[int] = None,
        terminal_segments: Optional[List[Segment3D]] = None,
        polygons: Optional[List] = None
    ) -> str:
        """
        Enhanced scene generation - wrapper for hasattr() check in main.py.
        
        This method exists to make hasattr(generator, 'generate_scene_enhanced')
        return True, enabling the polygon rendering code path.
        """
        return self.generate_scene(
            segments, bbox, filename, max_depth, terminal_segments,
            polygons=polygons
        )