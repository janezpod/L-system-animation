"""
3D POV-Ray Scene Generator - Enhanced Version

KEY IMPROVEMENTS:
1. double_illuminate for visible leaf/petal polygons from both sides
2. Animation-safe lighting (no jitter = no flickering)
3. Top-down camera mode for phyllotaxis/sunflower spirals
4. Better materials with specular highlights
5. Gradient sky background for depth
6. Eased camera movement

Based on research from ABOP and POV-Ray best practices.
"""

import os
import math
from typing import List, Optional, Tuple
from turtle.interpreter3d import Segment3D, BoundingBox3D


def depth_to_color_3d(depth: int, max_depth: int) -> Tuple[float, float, float]:
    """
    Calculate RGB color based on depth level for 3D rendering.
    Improved gradient from rich brown trunk to vibrant green tips.
    """
    if max_depth == 0:
        max_depth = 1
    
    t = depth / max_depth
    
    # Trunk: rich brown (0.35, 0.20, 0.10)
    # Tips: vibrant green (0.35, 0.70, 0.25)
    r = 0.35 + t * (0.35 - 0.35)
    g = 0.20 + t * (0.70 - 0.20)
    b = 0.10 + t * (0.25 - 0.10)
    
    return (r, g, b)


def ease_in_out_sine(t: float) -> float:
    """Sinusoidal ease-in-out for smooth camera movement."""
    return (1 - math.cos(t * math.pi)) / 2


class POVRayGenerator3D:
    """Enhanced POV-Ray scene generator with improved rendering quality."""
    
    # Enhanced template with gradient sky, animation-safe lighting
    POV_TEMPLATE = '''// L-System 3D Plant - Enhanced Scene
#version 3.7;
global_settings {{ 
    assumed_gamma 1.0
    max_trace_level 10
    ambient_light rgb <0.2, 0.2, 0.2>
}}

// Gradient sky background for depth
sky_sphere {{
    pigment {{
        gradient y
        color_map {{
            [0.0 rgb <{bg_r}, {bg_g}, {bg_b}>]
            [0.3 rgb <{sky_mid_r}, {sky_mid_g}, {sky_mid_b}>]
            [1.0 rgb <{sky_top_r}, {sky_top_g}, {sky_top_b}>]
        }}
        scale 2
        translate -1
    }}
}}

{camera}

// Key light - warm sun (NO JITTER for animation stability!)
light_source {{
    <{sun_x}, {sun_y}, {sun_z}>
    color rgb <1.0, 0.95, 0.88>
    area_light <4, 0, 0>, <0, 0, 4>, 5, 5
    adaptive 1
    // No jitter - prevents flickering in animations
}}

// Sky fill light (cool blue from above)
light_source {{
    <{center_x}, {center_y} + {scene_scale} * 3, {center_z}>
    color rgb <0.30, 0.35, 0.50>
    shadowless
}}

// Ground bounce light (warm)
light_source {{
    <{center_x}, {bbox_min_y} - {scene_scale} * 0.5, {center_z}>
    color rgb <0.18, 0.15, 0.12>
    shadowless
}}

// Back rim light for edge definition
light_source {{
    <{center_x} - {scene_scale} * 1.2, {center_y}, {center_z} + {scene_scale} * 1.2>
    color rgb <0.20, 0.25, 0.30>
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
    
    # Top-down camera for phyllotaxis patterns
    TOPDOWN_CAMERA = '''camera {{
    location <{cam_x}, {cam_y}, {cam_z}>
    look_at <{look_x}, {look_y}, {look_z}>
    up <0, 0, -1>
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
    
    # Enhanced leaf template with double_illuminate for visibility from both sides
    LEAF_TEMPLATE = '''    // Leaf polygon
    triangle {{
        <{x1}, {y1}, {z1}>,
        <{x2}, {y2}, {z2}>,
        <{x3}, {y3}, {z3}>
        pigment {{ rgb <{r}, {g}, {b}> }}
        finish {{ 
            ambient 0.35 
            diffuse 0.65 
            specular 0.15
            roughness 0.02
        }}
        double_illuminate  // Critical: light both sides!
    }}
'''
    
    # Extended color palette
    COLOR_PALETTE = [
        None,                     # 0: use depth-based color
        (1.00, 0.85, 0.10),       # 1: sunflower yellow
        (0.45, 0.30, 0.15),       # 2: brown (seeds/center)
        (0.85, 0.15, 0.15),       # 3: red
        (1.00, 0.60, 0.70),       # 4: pink
        (1.00, 0.55, 0.10),       # 5: orange
        (0.70, 0.40, 0.80),       # 6: purple
        (0.95, 0.95, 0.95),       # 7: white
        (0.20, 0.45, 0.15),       # 8: dark green
        (0.55, 0.80, 0.30),       # 9: lime green
        (0.80, 0.75, 0.20),       # 10: gold
    ]
    
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
        camera_rotation: float = 360.0,
        top_down_view: bool = False,  # NEW: for phyllotaxis
        camera_tilt: float = 0.0,     # NEW: angle from horizontal (90 = top-down)
        use_eased_camera: bool = True  # NEW: smooth camera movement
    ):
        """
        Initialize enhanced 3D POV-Ray generator.
        
        New parameters:
            top_down_view: Use top-down camera for spiral patterns
            camera_tilt: Camera tilt angle (0=side, 90=top-down)
            use_eased_camera: Apply easing to camera rotation
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
        self.top_down_view = top_down_view
        self.camera_tilt = camera_tilt
        self.use_eased_camera = use_eased_camera
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _calculate_camera_position(
        self,
        bbox: BoundingBox3D,
        frame: int = 0,
        total_frames: int = 1
    ) -> Tuple[float, float, float, float, float, float]:
        """
        Calculate camera position with optional easing and tilt support.
        """
        center = bbox.center
        scene_scale = bbox.max_dimension
        
        # Calculate camera orbit angle with optional easing
        if self.animate_camera and total_frames > 1:
            t = frame / (total_frames - 1)
            if self.use_eased_camera:
                t = ease_in_out_sine(t)
            angle_offset = t * self.camera_rotation
        else:
            angle_offset = 0
        
        angle_rad = math.radians(self.camera_angle + angle_offset)
        
        # Camera distance
        distance = scene_scale * self.camera_distance
        
        if self.top_down_view or self.camera_tilt >= 80:
            # Top-down view for phyllotaxis patterns
            cam_x = center[0] + distance * 0.1 * math.sin(angle_rad)
            cam_z = center[2] + distance * 0.1 * math.cos(angle_rad)
            cam_y = center[1] + distance * 1.5
            look_x, look_y, look_z = center
        elif self.camera_tilt > 0:
            # Tilted view (useful for showing both spiral and structure)
            tilt_rad = math.radians(self.camera_tilt)
            horizontal_dist = distance * math.cos(tilt_rad)
            vertical_offset = distance * math.sin(tilt_rad)
            
            cam_x = center[0] + horizontal_dist * math.sin(angle_rad)
            cam_z = center[2] + horizontal_dist * math.cos(angle_rad)
            cam_y = center[1] + vertical_offset
            look_x, look_y, look_z = center
        else:
            # Standard side view
            cam_x = center[0] + distance * math.sin(angle_rad)
            cam_z = center[2] + distance * math.cos(angle_rad)
            cam_y = center[1] + scene_scale * self.camera_height
            look_x, look_y, look_z = center
        
        return (cam_x, cam_y, cam_z, look_x, look_y, look_z)
    
    def _segment_to_povray(
        self,
        segment: Segment3D,
        max_depth: int,
        base_radius: float = 0.3
    ) -> str:
        """Convert a 3D segment to POV-Ray geometry with enhanced materials."""
        length = segment.length()
        if length < 0.001:
            return ""
        
        # Check if segment has color_index set
        color_index = getattr(segment, 'color_index', 0)
        if color_index > 0 and color_index < len(self.COLOR_PALETTE) and self.COLOR_PALETTE[color_index]:
            r, g, b = self.COLOR_PALETTE[color_index]
        else:
            r, g, b = depth_to_color_3d(segment.depth, max_depth)
        
        # Calculate radius
        radius = base_radius * segment.width
        if radius < 0.02:
            radius = 0.02
        
        lines = []
        
        # Enhanced material with subtle specular
        lines.append(
            f"    cylinder {{ "
            f"<{segment.x1:.6f}, {segment.y1:.6f}, {segment.z1:.6f}>, "
            f"<{segment.x2:.6f}, {segment.y2:.6f}, {segment.z2:.6f}>, {radius:.4f} "
            f"pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }} "
            f"finish {{ ambient 0.25 diffuse 0.70 specular 0.08 roughness 0.05 }} }}"
        )
        
        # Sphere at endpoints for smooth joints
        lines.append(
            f"    sphere {{ "
            f"<{segment.x2:.6f}, {segment.y2:.6f}, {segment.z2:.6f}>, {radius:.4f} "
            f"pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }} "
            f"finish {{ ambient 0.25 diffuse 0.70 specular 0.08 roughness 0.05 }} }}"
        )
        
        return '\n'.join(lines)
    
    def _leaf_to_povray(
        self,
        segment: Segment3D,
        max_depth: int,
        leaf_size: float = 1.0
    ) -> str:
        """Generate enhanced leaf triangles with double_illuminate."""
        dx = segment.x2 - segment.x1
        dy = segment.y2 - segment.y1
        dz = segment.z2 - segment.z1
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        if length < 0.001:
            return ""
        
        dx, dy, dz = dx/length, dy/length, dz/length
        
        # Create perpendicular vectors for leaf plane
        px = -dz
        py = 0
        pz = dx
        p_len = math.sqrt(px*px + pz*pz)
        if p_len < 0.001:
            px, py, pz = 1, 0, 0
        else:
            px, py, pz = px/p_len, py/p_len, pz/p_len
        
        # Check for color_index
        color_index = getattr(segment, 'color_index', 0)
        if color_index > 0 and color_index < len(self.COLOR_PALETTE) and self.COLOR_PALETTE[color_index]:
            r, g, b = self.COLOR_PALETTE[color_index]
        else:
            r, g, b = 0.35, 0.70, 0.22
        
        # Triangle vertices
        tip_x = segment.x2 + dx * leaf_size
        tip_y = segment.y2 + dy * leaf_size
        tip_z = segment.z2 + dz * leaf_size
        
        left_x = segment.x2 + px * leaf_size * 0.35
        left_y = segment.y2 + py * leaf_size * 0.35
        left_z = segment.z2 + pz * leaf_size * 0.35
        
        right_x = segment.x2 - px * leaf_size * 0.35
        right_y = segment.y2 - py * leaf_size * 0.35
        right_z = segment.z2 - pz * leaf_size * 0.35
        
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
        color: Tuple[float, float, float],
        use_smooth: bool = False
    ) -> str:
        """
        Generate POV-Ray polygon with double_illuminate for leaf/petal visibility.
        Skips degenerate triangles to avoid POV-Ray warnings.
        """
        if len(vertices) < 3:
            return ""
        
        r, g, b = color
        
        # Calculate centroid for fan triangulation
        cx = sum(v[0] for v in vertices) / len(vertices)
        cy = sum(v[1] for v in vertices) / len(vertices)
        cz = sum(v[2] for v in vertices) / len(vertices)
        
        lines = []
        
        # Create triangles fanning from centroid, skip degenerate ones
        for i in range(len(vertices)):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % len(vertices)]
            
            # Check for degenerate triangle (vertices too close)
            def dist_sq(a, b):
                return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2
            
            min_dist = 0.0001  # Minimum distance squared
            if dist_sq(v1, v2) < min_dist or dist_sq(v1, (cx,cy,cz)) < min_dist or dist_sq(v2, (cx,cy,cz)) < min_dist:
                continue  # Skip degenerate triangle
            
            lines.append(f"    triangle {{")
            lines.append(f"        <{v1[0]:.4f}, {v1[1]:.4f}, {v1[2]:.4f}>,")
            lines.append(f"        <{v2[0]:.4f}, {v2[1]:.4f}, {v2[2]:.4f}>,")
            lines.append(f"        <{cx:.4f}, {cy:.4f}, {cz:.4f}>")
            lines.append(f"        pigment {{ rgb <{r:.4f}, {g:.4f}, {b:.4f}> }}")
            lines.append(f"        finish {{ ambient 0.35 diffuse 0.60 specular 0.12 roughness 0.02 }}")
            lines.append(f"        double_illuminate")  # KEY: visible from both sides!
            lines.append(f"    }}")
        
        return '\n'.join(lines)
    
    def _render_polygons_list_3d(
        self,
        polygons: List,
        max_depth: int
    ) -> List[str]:
        """Render 3D polygons with enhanced color palette and double_illuminate."""
        geometry_lines = []
        
        for poly in polygons:
            if not hasattr(poly, 'vertices') or len(poly.vertices) < 3:
                continue
            
            depth = getattr(poly, 'depth', 0)
            color_index = getattr(poly, 'color_index', 0)
            
            if color_index > 0 and color_index < len(self.COLOR_PALETTE) and self.COLOR_PALETTE[color_index]:
                r, g, b = self.COLOR_PALETTE[color_index]
            else:
                # Enhanced depth-based leaf coloring
                t = depth / max_depth if max_depth > 0 else 0
                r = 0.28 + t * 0.12
                g = 0.52 + t * 0.23
                b = 0.18 + t * 0.08
            
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
        """Generate an enhanced POV-Ray 3D scene file."""
        if max_depth is None:
            max_depth = max((seg.depth for seg in segments), default=0)
            if polygons:
                polygon_depths = [getattr(p, 'depth', 0) for p in polygons]
                if polygon_depths:
                    max_depth = max(max_depth, max(polygon_depths))
        
        padded_bbox = bbox.with_padding_percent(self.padding_percent)
        center = padded_bbox.center
        scene_scale = padded_bbox.max_dimension
        
        # Calculate camera
        cam_pos = self._calculate_camera_position(padded_bbox, frame, total_frames)
        
        if self.top_down_view or self.camera_tilt >= 80:
            camera = self.TOPDOWN_CAMERA.format(
                cam_x=cam_pos[0], cam_y=cam_pos[1], cam_z=cam_pos[2],
                look_x=cam_pos[3], look_y=cam_pos[4], look_z=cam_pos[5],
                fov=self.fov
            )
        elif self.use_perspective:
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
        
        # Calculate base radius
        base_radius = scene_scale * 0.012
        
        # Generate geometry
        geometry_lines = []
        for segment in segments:
            pov_geom = self._segment_to_povray(segment, max_depth, base_radius)
            if pov_geom:
                geometry_lines.append(pov_geom)
        
        # Add leaves
        if self.show_leaves and terminal_segments:
            leaf_size = scene_scale * 0.025
            for segment in terminal_segments:
                if segment.length() > 0.1:
                    leaf_geom = self._leaf_to_povray(segment, max_depth, leaf_size)
                    if leaf_geom:
                        geometry_lines.append(leaf_geom)
        
        # Add polygons (with double_illuminate)
        if polygons:
            polygon_geom = self._render_polygons_list_3d(polygons, max_depth)
            geometry_lines.extend(polygon_geom)
        
        geometry = '\n'.join(geometry_lines)
        
        # Enhanced sky gradient colors
        bg_r, bg_g, bg_b = self.background_color
        sky_mid_r = min(1.0, bg_r * 0.95)
        sky_mid_g = min(1.0, bg_g * 0.97)
        sky_mid_b = min(1.0, bg_b * 1.02)
        sky_top_r = max(0.0, bg_r * 0.6)
        sky_top_g = max(0.0, bg_g * 0.7)
        sky_top_b = min(1.0, bg_b * 1.15)
        
        # Sun position (offset from camera for nice shadows)
        angle_rad = math.radians(self.camera_angle + 45)
        sun_distance = scene_scale * 3
        sun_x = center[0] + sun_distance * math.sin(angle_rad)
        sun_y = center[1] + scene_scale * 2.5
        sun_z = center[2] + sun_distance * math.cos(angle_rad)
        
        scene = self.POV_TEMPLATE.format(
            bg_r=bg_r, bg_g=bg_g, bg_b=bg_b,
            sky_mid_r=sky_mid_r, sky_mid_g=sky_mid_g, sky_mid_b=sky_mid_b,
            sky_top_r=sky_top_r, sky_top_g=sky_top_g, sky_top_b=sky_top_b,
            camera=camera,
            sun_x=sun_x, sun_y=sun_y, sun_z=sun_z,
            center_x=center[0], center_y=center[1], center_z=center[2],
            scene_scale=scene_scale,
            bbox_min_y=padded_bbox.min_y,
            geometry=geometry
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