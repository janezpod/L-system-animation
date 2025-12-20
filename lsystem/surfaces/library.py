"""
Predefined Surface Library for L-System Plant Organs

Based on ABOP Chapter 5: Models of Plant Organs

Supports:
- Bicubic Bézier patches for petals/leaves
- Procedural shapes (disks, cones)
- Developmental surface models
- POV-Ray generation for surfaces

The ~ symbol in L-systems incorporates predefined surfaces from this library.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from abc import ABC, abstractmethod

# Try to use numpy for faster computation
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    # Provide fallback
    class np:
        @staticmethod
        def array(x):
            return list(x) if not isinstance(x, list) else x
        @staticmethod
        def zeros(shape):
            if isinstance(shape, int):
                return [0.0] * shape
            return [[0.0] * shape[1] for _ in range(shape[0])]


@dataclass
class ControlPoint:
    """3D control point with optional normal."""
    x: float
    y: float
    z: float
    nx: float = 0.0
    ny: float = 0.0
    nz: float = 1.0
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)
    
    def normal_tuple(self) -> Tuple[float, float, float]:
        return (self.nx, self.ny, self.nz)


class Surface(ABC):
    """Abstract base for predefined surfaces."""
    
    def __init__(self, name: str, color_index: int = 0):
        self.name = name
        self.color_index = color_index
    
    @abstractmethod
    def sample(self, u: float, v: float) -> Tuple[float, float, float]:
        """Sample point on surface at (u, v) in [0, 1]²."""
        pass
    
    def sample_normal(self, u: float, v: float, epsilon: float = 0.001) -> Tuple[float, float, float]:
        """Calculate surface normal at (u, v) using finite differences."""
        p = self.sample(u, v)
        
        # Partial derivatives
        pu = self.sample(min(1, u + epsilon), v)
        pv = self.sample(u, min(1, v + epsilon))
        
        # Tangent vectors
        tu = [pu[i] - p[i] for i in range(3)]
        tv = [pv[i] - p[i] for i in range(3)]
        
        # Cross product for normal
        nx = tu[1] * tv[2] - tu[2] * tv[1]
        ny = tu[2] * tv[0] - tu[0] * tv[2]
        nz = tu[0] * tv[1] - tu[1] * tv[0]
        
        # Normalize
        length = math.sqrt(nx*nx + ny*ny + nz*nz)
        if length < 1e-10:
            return (0.0, 0.0, 1.0)
        return (nx/length, ny/length, nz/length)
    
    def to_mesh(self, resolution: int = 10) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
        """
        Generate triangle mesh representation.
        
        Args:
            resolution: Number of samples in each direction
            
        Returns:
            Tuple of (vertices, faces) where faces are vertex index triples
        """
        vertices = []
        faces = []
        
        # Sample surface
        for i in range(resolution + 1):
            for j in range(resolution + 1):
                u = i / resolution
                v = j / resolution
                vertices.append(self.sample(u, v))
        
        # Create triangles
        for i in range(resolution):
            for j in range(resolution):
                idx = i * (resolution + 1) + j
                # Two triangles per quad
                faces.append((idx, idx + 1, idx + resolution + 2))
                faces.append((idx, idx + resolution + 2, idx + resolution + 1))
        
        return vertices, faces
    
    @abstractmethod
    def to_povray(self) -> str:
        """Generate POV-Ray representation."""
        pass


class DiskSurface(Surface):
    """
    Circular disk (ABOP Figure 4.11).
    
    Used for sunflower florets, capitulum components.
    Simple parametric surface where u is radial and v is angular.
    """
    
    def __init__(
        self, 
        name: str = "disk",
        radius: float = 1.0,
        color_index: int = 0
    ):
        super().__init__(name, color_index)
        self.radius = radius
    
    def sample(self, u: float, v: float) -> Tuple[float, float, float]:
        """Sample point: u = radial [0,1], v = angular [0,1] maps to [0, 2π]."""
        r = u * self.radius
        theta = v * 2 * math.pi
        return (r * math.cos(theta), r * math.sin(theta), 0.0)
    
    def to_povray(self) -> str:
        """Generate POV-Ray disc object."""
        return f"""disc {{
    <0, 0, 0>, <0, 0, 1>, {self.radius}
    texture {{ plant_texture_{self.color_index} }}
}}"""


class ConeSurface(Surface):
    """
    Conical surface for thorns, spines, and tapered structures.
    """
    
    def __init__(
        self,
        name: str = "cone",
        base_radius: float = 0.5,
        height: float = 1.0,
        color_index: int = 0
    ):
        super().__init__(name, color_index)
        self.base_radius = base_radius
        self.height = height
    
    def sample(self, u: float, v: float) -> Tuple[float, float, float]:
        """u = height [0,1], v = angular [0,1]."""
        r = self.base_radius * (1 - u)  # Radius decreases with height
        theta = v * 2 * math.pi
        z = u * self.height
        return (r * math.cos(theta), r * math.sin(theta), z)
    
    def to_povray(self) -> str:
        return f"""cone {{
    <0, 0, 0>, {self.base_radius},
    <0, 0, {self.height}>, 0
    texture {{ plant_texture_{self.color_index} }}
}}"""


class BezierPatchSurface(Surface):
    """
    Bicubic Bézier patch for organic shapes.
    
    ABOP Section 5.1: Used for petals, leaves, thorns.
    
    16 control points arranged in a 4x4 grid define a smooth surface
    using Bernstein polynomials of degree 3.
    """
    
    def __init__(
        self,
        name: str,
        control_points,  # Shape (4, 4, 3) - can be numpy array or nested list
        color_index: int = 0
    ):
        super().__init__(name, color_index)
        if HAS_NUMPY:
            self.control_points = np.array(control_points)
        else:
            self.control_points = control_points
    
    @staticmethod
    def bernstein(n: int, i: int, t: float) -> float:
        """
        Bernstein polynomial B_{i,n}(t).
        
        B_{i,n}(t) = C(n,i) * t^i * (1-t)^(n-i)
        """
        return math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
    
    def sample(self, u: float, v: float) -> Tuple[float, float, float]:
        """
        Evaluate Bézier surface at (u, v).
        
        S(u,v) = Σᵢ Σⱼ Bᵢ,₃(u) Bⱼ,₃(v) Pᵢⱼ
        """
        if HAS_NUMPY:
            point = np.zeros(3)
            for i in range(4):
                for j in range(4):
                    b = self.bernstein(3, i, u) * self.bernstein(3, j, v)
                    point += b * self.control_points[i, j]
            return tuple(point)
        else:
            point = [0.0, 0.0, 0.0]
            for i in range(4):
                for j in range(4):
                    b = self.bernstein(3, i, u) * self.bernstein(3, j, v)
                    for k in range(3):
                        point[k] += b * self.control_points[i][j][k]
            return tuple(point)
    
    def to_povray(self) -> str:
        """Generate POV-Ray bicubic patch."""
        lines = [f"bicubic_patch {{"]
        lines.append("    type 1  // Bezier patch")
        lines.append("    flatness 0.001")
        lines.append("    u_steps 4  v_steps 4")
        
        # Output control points
        for i in range(4):
            row = []
            for j in range(4):
                if HAS_NUMPY:
                    p = self.control_points[i, j]
                else:
                    p = self.control_points[i][j]
                row.append(f"<{p[0]}, {p[1]}, {p[2]}>")
            lines.append("    " + ", ".join(row) + ("," if i < 3 else ""))
        
        lines.append(f"    texture {{ plant_texture_{self.color_index} }}")
        lines.append("}")
        return "\n".join(lines)


# =============================================================================
# Botanical Leaf Shapes (ABOP Figure 5.4)
# =============================================================================

def create_cordate_leaf(scale: float = 1.0, color_index: int = 2) -> BezierPatchSurface:
    """
    Heart-shaped (cordate) leaf.
    
    ABOP Figure 5.4a: Common in many plants like violets, morning glories.
    The characteristic heart shape is created by indentation at the base.
    
    Args:
        scale: Size multiplier
        color_index: Color for POV-Ray texture
        
    Returns:
        BezierPatchSurface with cordate shape
    """
    # Control points define the heart shape with slight curvature
    cp = [
        [[0, 0, 0], [0.2, 0.1, 0.05], [0.4, 0.1, 0.05], [0.5, 0, 0]],
        [[0, 0.3, 0], [0.3, 0.35, 0.1], [0.45, 0.3, 0.08], [0.5, 0.25, 0]],
        [[0, 0.6, 0], [0.25, 0.65, 0.08], [0.4, 0.6, 0.05], [0.5, 0.5, 0]],
        [[0, 0.8, 0], [0.1, 0.85, 0.02], [0.2, 0.9, 0.01], [0.3, 1, 0]],
    ]
    
    # Apply scale
    if HAS_NUMPY:
        cp = np.array(cp) * scale
    else:
        cp = [[[c * scale for c in p] for p in row] for row in cp]
    
    return BezierPatchSurface("leaf_cordate", cp, color_index)


def create_lanceolate_leaf(scale: float = 1.0, color_index: int = 2) -> BezierPatchSurface:
    """
    Lance-shaped (lanceolate) leaf.
    
    ABOP Figure 5.4: Narrow elongated shape typical of grasses and willows.
    Widest near the middle, tapering to points at both ends.
    
    Args:
        scale: Size multiplier
        color_index: Color for POV-Ray texture
        
    Returns:
        BezierPatchSurface with lanceolate shape
    """
    cp = [
        [[0, 0, 0], [0.1, 0.05, 0.02], [0.15, 0.05, 0.02], [0.2, 0, 0]],
        [[0, 0.3, 0], [0.15, 0.35, 0.05], [0.2, 0.32, 0.04], [0.25, 0.3, 0]],
        [[0, 0.6, 0], [0.12, 0.65, 0.04], [0.18, 0.62, 0.03], [0.22, 0.6, 0]],
        [[0, 1.0, 0], [0.02, 1.0, 0.01], [0.03, 1.0, 0.01], [0.05, 1.0, 0]],
    ]
    
    if HAS_NUMPY:
        cp = np.array(cp) * scale
    else:
        cp = [[[c * scale for c in p] for p in row] for row in cp]
    
    return BezierPatchSurface("leaf_lanceolate", cp, color_index)


def create_ovate_leaf(scale: float = 1.0, color_index: int = 2) -> BezierPatchSurface:
    """
    Egg-shaped (ovate) leaf.
    
    Broadest below the middle, common in many deciduous trees.
    
    Args:
        scale: Size multiplier
        color_index: Color for POV-Ray texture
        
    Returns:
        BezierPatchSurface with ovate shape
    """
    cp = [
        [[0, 0, 0], [0.15, 0.05, 0.03], [0.25, 0.05, 0.03], [0.35, 0, 0]],
        [[0, 0.25, 0], [0.25, 0.3, 0.08], [0.35, 0.28, 0.06], [0.4, 0.25, 0]],
        [[0, 0.55, 0], [0.2, 0.6, 0.06], [0.3, 0.58, 0.04], [0.35, 0.55, 0]],
        [[0, 0.9, 0], [0.08, 0.95, 0.02], [0.12, 0.98, 0.01], [0.15, 1.0, 0]],
    ]
    
    if HAS_NUMPY:
        cp = np.array(cp) * scale
    else:
        cp = [[[c * scale for c in p] for p in row] for row in cp]
    
    return BezierPatchSurface("leaf_ovate", cp, color_index)


def create_palmate_leaf(scale: float = 1.0, color_index: int = 2) -> BezierPatchSurface:
    """
    Palm-shaped (palmate) leaf lobe.
    
    One lobe of a maple-like leaf. Multiple can be combined.
    
    Args:
        scale: Size multiplier
        color_index: Color for POV-Ray texture
    """
    cp = [
        [[0, 0, 0], [0.1, 0.1, 0.02], [0.2, 0.1, 0.02], [0.3, 0, 0]],
        [[0.05, 0.3, 0.01], [0.15, 0.35, 0.05], [0.25, 0.32, 0.04], [0.35, 0.3, 0.01]],
        [[0.1, 0.6, 0.02], [0.18, 0.65, 0.04], [0.28, 0.62, 0.03], [0.4, 0.6, 0.02]],
        [[0.15, 1.0, 0], [0.2, 1.0, 0.01], [0.25, 1.0, 0.01], [0.3, 1.0, 0]],
    ]
    
    if HAS_NUMPY:
        cp = np.array(cp) * scale
    else:
        cp = [[[c * scale for c in p] for p in row] for row in cp]
    
    return BezierPatchSurface("leaf_palmate", cp, color_index)


# =============================================================================
# Petal Shapes (ABOP Figure 4.10)
# =============================================================================

def create_rose_petal(scale: float = 1.0, color_index: int = 3) -> BezierPatchSurface:
    """
    Rose petal shape.
    
    ABOP Figure 4.10: Curved petal with cupped center.
    The z-coordinates create the characteristic curved shape.
    
    Args:
        scale: Size multiplier
        color_index: Color for POV-Ray texture
        
    Returns:
        BezierPatchSurface with rose petal shape
    """
    cp = [
        [[0, 0, 0], [0.15, 0.05, 0.1], [0.3, 0.05, 0.1], [0.5, 0, 0]],
        [[0, 0.2, 0.1], [0.2, 0.25, 0.15], [0.35, 0.22, 0.12], [0.5, 0.2, 0.05]],
        [[0, 0.5, 0.15], [0.18, 0.55, 0.12], [0.32, 0.52, 0.08], [0.5, 0.5, 0.02]],
        [[0, 0.8, 0.05], [0.1, 0.85, 0.03], [0.25, 0.9, 0.01], [0.4, 1.0, 0]],
    ]
    
    if HAS_NUMPY:
        cp = np.array(cp) * scale
    else:
        cp = [[[c * scale for c in p] for p in row] for row in cp]
    
    return BezierPatchSurface("petal_rose", cp, color_index)


def create_tulip_petal(scale: float = 1.0, color_index: int = 3) -> BezierPatchSurface:
    """
    Tulip petal with characteristic cup shape.
    
    More elongated and cupped than rose petals.
    """
    cp = [
        [[0, 0, 0], [0.1, 0.05, 0.15], [0.2, 0.05, 0.15], [0.3, 0, 0]],
        [[0, 0.3, 0.2], [0.12, 0.35, 0.25], [0.22, 0.32, 0.22], [0.3, 0.3, 0.15]],
        [[0, 0.6, 0.15], [0.1, 0.65, 0.18], [0.2, 0.62, 0.15], [0.3, 0.6, 0.08]],
        [[0, 1.0, 0], [0.05, 1.0, 0.02], [0.15, 1.0, 0.01], [0.2, 1.0, 0]],
    ]
    
    if HAS_NUMPY:
        cp = np.array(cp) * scale
    else:
        cp = [[[c * scale for c in p] for p in row] for row in cp]
    
    return BezierPatchSurface("petal_tulip", cp, color_index)


def create_daisy_petal(scale: float = 1.0, color_index: int = 4) -> BezierPatchSurface:
    """
    Flat, elongated daisy/sunflower ray floret petal.
    """
    cp = [
        [[0, 0, 0], [0.05, 0.02, 0.01], [0.1, 0.02, 0.01], [0.15, 0, 0]],
        [[0, 0.35, 0], [0.06, 0.38, 0.02], [0.12, 0.36, 0.02], [0.15, 0.35, 0]],
        [[0, 0.7, 0], [0.05, 0.72, 0.01], [0.1, 0.71, 0.01], [0.15, 0.7, 0]],
        [[0.02, 1.0, 0], [0.05, 1.0, 0], [0.1, 1.0, 0], [0.13, 1.0, 0]],
    ]
    
    if HAS_NUMPY:
        cp = np.array(cp) * scale
    else:
        cp = [[[c * scale for c in p] for p in row] for row in cp]
    
    return BezierPatchSurface("petal_daisy", cp, color_index)


# =============================================================================
# Developmental Surface Model (ABOP 5.2)
# =============================================================================

class DevelopmentalLeaf:
    """
    Developmental leaf model growing from tip to base.
    
    ABOP Figure 5.5: Leaf develops recursively.
    
    Axiom: A(0)
    p1: A(t) : t < max_t → F(t)[+A(t)][-A(t)]
    
    This model captures how real leaves develop, with the tip
    forming first and the base developing last. Growth proceeds
    acropetally (toward the apex).
    """
    
    def __init__(
        self,
        max_age: float = 5.0,
        branch_angle: float = 45.0,
        length_scale: float = 1.0,
        width_scale: float = 0.3
    ):
        self.max_age = max_age
        self.branch_angle = branch_angle
        self.length_scale = length_scale
        self.width_scale = width_scale
    
    def generate_at_age(self, age: float) -> List[Tuple[str, float, float]]:
        """
        Generate leaf structure at given developmental age.
        
        Args:
            age: Current developmental age
            
        Returns:
            List of (type, length, angle) tuples representing the structure
        """
        if age <= 0:
            return [('apex', 0, 0)]
        
        segments = []
        self._recurse(age, segments, 0)
        return segments
    
    def _recurse(
        self, 
        age: float, 
        segments: List, 
        depth: int
    ):
        """Recursive structure generation."""
        if age <= 0 or depth > 10:
            segments.append(('apex', 0.01 * self.length_scale, 0))
            return
        
        # Main segment grows with age
        seg_length = min(age, 1.0) * self.length_scale
        segments.append(('segment', seg_length, 0))
        
        if age > 1:
            # Branch left
            segments.append(('branch_start', 0, self.branch_angle))
            self._recurse(age - 1, segments, depth + 1)
            segments.append(('branch_end', 0, 0))
            
            # Branch right  
            segments.append(('branch_start', 0, -self.branch_angle))
            self._recurse(age - 1, segments, depth + 1)
            segments.append(('branch_end', 0, 0))
            
            # Continue main axis
            self._recurse(age - 1, segments, depth)
    
    def to_lstring(self, age: float) -> str:
        """
        Generate L-system string representation at given age.
        
        Args:
            age: Developmental age
            
        Returns:
            L-system string for turtle interpretation
        """
        segments = self.generate_at_age(age)
        lstring = []
        
        for seg_type, length, angle in segments:
            if seg_type == 'segment':
                lstring.append('F')
            elif seg_type == 'apex':
                lstring.append('.')  # Mark apex position
            elif seg_type == 'branch_start':
                if angle > 0:
                    lstring.append('[+')
                else:
                    lstring.append('[-')
            elif seg_type == 'branch_end':
                lstring.append(']')
        
        return ''.join(lstring)


# =============================================================================
# Surface Library Manager
# =============================================================================

class SurfaceLibrary:
    """
    Manager for predefined surfaces.
    
    ABOP ~ symbol incorporates surface from library.
    
    Usage:
        library = SurfaceLibrary()
        leaf_surface = library.get('L')
        
    Standard symbols:
        D - Disk
        K - Flower center
        L - Leaf (cordate)
        P - Petal (rose)
    """
    
    def __init__(self):
        self.surfaces: Dict[str, Surface] = {}
        self._register_defaults()
    
    def _register_defaults(self):
        """Register standard botanical surfaces."""
        # Basic shapes
        self.surfaces['D'] = DiskSurface("disk", radius=0.5, color_index=1)
        self.surfaces['K'] = DiskSurface("flower_center", radius=0.3, color_index=5)
        
        # Leaves
        self.surfaces['L'] = create_cordate_leaf(scale=1.0, color_index=2)
        self.surfaces['Ll'] = create_lanceolate_leaf(scale=1.0, color_index=2)
        self.surfaces['Lo'] = create_ovate_leaf(scale=1.0, color_index=2)
        self.surfaces['Lp'] = create_palmate_leaf(scale=1.0, color_index=2)
        
        # Petals
        self.surfaces['P'] = create_rose_petal(scale=1.0, color_index=3)
        self.surfaces['Pt'] = create_tulip_petal(scale=1.0, color_index=3)
        self.surfaces['Pd'] = create_daisy_petal(scale=1.0, color_index=4)
        
        # Structural
        self.surfaces['C'] = ConeSurface("thorn", base_radius=0.2, height=0.8, color_index=1)
    
    def get(self, name: str) -> Optional[Surface]:
        """
        Get surface by name.
        
        Args:
            name: Surface identifier
            
        Returns:
            Surface instance or None if not found
        """
        return self.surfaces.get(name)
    
    def register(self, name: str, surface: Surface):
        """
        Register custom surface.
        
        Args:
            name: Identifier for the surface
            surface: Surface instance
        """
        self.surfaces[name] = surface
    
    def list_surfaces(self) -> List[str]:
        """Get list of registered surface names."""
        return list(self.surfaces.keys())
    
    def to_povray_include(self) -> str:
        """
        Generate POV-Ray include file with all surfaces.
        
        Returns:
            POV-Ray code declaring all surfaces
        """
        lines = [
            "// Predefined surfaces for L-system",
            "// Generated by ABOP Surface Library",
            ""
        ]
        
        for name, surface in self.surfaces.items():
            lines.append(f"#declare Surface_{name} = {surface.to_povray()}")
            lines.append("")
        
        return "\n".join(lines)
    
    def create_scaled(self, name: str, scale: float) -> Optional[Surface]:
        """
        Create a scaled copy of an existing surface.
        
        Args:
            name: Surface to copy
            scale: Scale factor
            
        Returns:
            New scaled surface or None
        """
        original = self.get(name)
        if original is None:
            return None
        
        # For Bezier patches, scale control points
        if isinstance(original, BezierPatchSurface):
            if HAS_NUMPY:
                new_cp = original.control_points * scale
            else:
                new_cp = [[[c * scale for c in p] for p in row] 
                         for row in original.control_points]
            return BezierPatchSurface(
                f"{original.name}_scaled",
                new_cp,
                original.color_index
            )
        elif isinstance(original, DiskSurface):
            return DiskSurface(
                f"{original.name}_scaled",
                original.radius * scale,
                original.color_index
            )
        elif isinstance(original, ConeSurface):
            return ConeSurface(
                f"{original.name}_scaled",
                original.base_radius * scale,
                original.height * scale,
                original.color_index
            )
        
        return None


# Global library instance
SURFACE_LIBRARY = SurfaceLibrary()


# =============================================================================
# Utility Functions
# =============================================================================

def create_flower_head(
    num_petals: int = 5,
    petal_type: str = 'rose',
    center_radius: float = 0.3,
    petal_scale: float = 1.0
) -> List[Tuple[str, float, Surface]]:
    """
    Create a flower head with center and petals.
    
    Args:
        num_petals: Number of petals
        petal_type: Type of petal ('rose', 'tulip', 'daisy')
        center_radius: Radius of flower center
        petal_scale: Scale factor for petals
        
    Returns:
        List of (position_angle, distance, surface) tuples
    """
    components = []
    
    # Center
    components.append((0, 0, DiskSurface("center", center_radius, color_index=5)))
    
    # Create petal surface
    if petal_type == 'tulip':
        petal = create_tulip_petal(petal_scale)
    elif petal_type == 'daisy':
        petal = create_daisy_petal(petal_scale)
    else:
        petal = create_rose_petal(petal_scale)
    
    # Position petals
    angle_step = 360.0 / num_petals
    for i in range(num_petals):
        angle = i * angle_step
        components.append((angle, center_radius * 1.2, petal))
    
    return components


def phyllotaxis_surface_positions(
    n: int,
    divergence_angle: float = 137.5,
    c: float = 1.0
) -> List[Tuple[float, float]]:
    """
    Generate positions for surfaces using Vogel's phyllotaxis model.
    
    ABOP Equation 4.1:
    φ = n × divergence_angle
    r = c × √n
    
    Args:
        n: Number of positions
        divergence_angle: Angle between successive elements (137.5° = golden angle)
        c: Radial scale factor
        
    Returns:
        List of (x, y) positions
    """
    positions = []
    for i in range(n):
        angle_rad = math.radians(i * divergence_angle)
        r = c * math.sqrt(i + 1)
        x = r * math.cos(angle_rad)
        y = r * math.sin(angle_rad)
        positions.append((x, y))
    return positions
