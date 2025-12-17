"""
3D Turtle Graphics Interpreter

Converts L-system strings to 3D line segments for rendering.
Implements the HLU (Heading, Left, Up) orientation system with ABOP enhancements.
"""

import math
import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, NamedTuple

# Try to use numpy for faster computation, fall back to pure Python
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# Golden angle for phyllotaxis
GOLDEN_ANGLE = 137.5077


# =============================================================================
# Pure Python 3D Math (fallback when numpy not available)
# =============================================================================

def _normalize_py(v: List[float]) -> List[float]:
    """Normalize a 3D vector (pure Python)."""
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length < 1e-10:
        return [0.0, 0.0, 0.0]
    return [v[0]/length, v[1]/length, v[2]/length]


def _dot_py(a: List[float], b: List[float]) -> float:
    """Dot product of two 3D vectors (pure Python)."""
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def _cross_py(a: List[float], b: List[float]) -> List[float]:
    """Cross product of two 3D vectors (pure Python)."""
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]


def _mat_vec_mul_py(m: List[List[float]], v: List[float]) -> List[float]:
    """Matrix-vector multiplication (pure Python)."""
    return [
        m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]*v[2],
        m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]*v[2],
        m[2][0]*v[0] + m[2][1]*v[1] + m[2][2]*v[2]
    ]


def _rotation_matrix_py(axis: List[float], angle_deg: float) -> List[List[float]]:
    """Create rotation matrix for rotation around arbitrary axis (pure Python)."""
    axis = _normalize_py(axis)
    angle = math.radians(angle_deg)
    c = math.cos(angle)
    s = math.sin(angle)
    t = 1 - c
    x, y, z = axis
    
    return [
        [t*x*x + c,    t*x*y - s*z,  t*x*z + s*y],
        [t*x*y + s*z,  t*y*y + c,    t*y*z - s*x],
        [t*x*z - s*y,  t*y*z + s*x,  t*z*z + c]
    ]


# =============================================================================
# NumPy 3D Math (faster)
# =============================================================================

def _rotation_matrix_np(axis, angle_deg: float):
    """Create rotation matrix for rotation around arbitrary axis (numpy)."""
    axis = axis / np.linalg.norm(axis)
    angle = np.radians(angle_deg)
    c, s = np.cos(angle), np.sin(angle)
    t = 1 - c
    x, y, z = axis
    return np.array([
        [t*x*x + c,    t*x*y - s*z,  t*x*z + s*y],
        [t*x*y + s*z,  t*y*y + c,    t*y*z - s*x],
        [t*x*z - s*y,  t*y*z + s*x,  t*z*z + c]
    ])


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Segment3D:
    """A 3D line segment with position, depth, and width information."""
    x1: float
    y1: float
    z1: float
    x2: float
    y2: float
    z2: float
    depth: int
    width: float
    index: int = 0  # Order in which segment was created
    heading: Tuple[float, float, float] = (0, 1, 0)  # For cylinder orientation
    color_index: int = 0  # For color cycling with ' symbol
    
    def length(self) -> float:
        """Calculate segment length."""
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        dz = self.z2 - self.z1
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def partial(self, visibility: float) -> 'Segment3D':
        """Create a partial segment drawn to the given visibility percentage."""
        if visibility >= 1.0:
            return self
        if visibility <= 0.0:
            return Segment3D(
                self.x1, self.y1, self.z1,
                self.x1, self.y1, self.z1,
                self.depth, self.width, self.index, self.heading, self.color_index
            )
        
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        dz = self.z2 - self.z1
        return Segment3D(
            self.x1, self.y1, self.z1,
            self.x1 + dx * visibility,
            self.y1 + dy * visibility,
            self.z1 + dz * visibility,
            self.depth, self.width, self.index, self.heading, self.color_index
        )
    
    def to_2d_segment(self) -> 'Segment':
        """Convert to 2D segment (XY projection)."""
        from turtle.interpreter import Segment
        return Segment(
            self.x1, self.y1, self.x2, self.y2,
            self.depth, self.width, self.index, self.color_index
        )


@dataclass
class Polygon3D:
    """A filled 3D polygon for leaf/petal shapes."""
    vertices: List[Tuple[float, float, float]]
    depth: int
    color_index: int = 0
    index: int = 0  # Creation order for animation
    normal: Optional[Tuple[float, float, float]] = None  # Surface normal
    
    def is_valid(self) -> bool:
        """Check if polygon has enough vertices."""
        return len(self.vertices) >= 3
    
    def calculate_normal(self) -> Tuple[float, float, float]:
        """Calculate surface normal from vertices."""
        if len(self.vertices) < 3:
            return (0.0, 0.0, 1.0)
        
        # Use first three vertices
        v0, v1, v2 = self.vertices[:3]
        e1 = [v1[i] - v0[i] for i in range(3)]
        e2 = [v2[i] - v0[i] for i in range(3)]
        
        normal = _cross_py(e1, e2)
        return tuple(_normalize_py(normal))


@dataclass
class BoundingBox3D:
    """3D bounding box for a set of segments."""
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    
    @property
    def width(self) -> float:
        return self.max_x - self.min_x
    
    @property
    def height(self) -> float:
        return self.max_y - self.min_y
    
    @property
    def depth(self) -> float:
        return self.max_z - self.min_z
    
    @property
    def center(self) -> Tuple[float, float, float]:
        return (
            (self.min_x + self.max_x) / 2,
            (self.min_y + self.max_y) / 2,
            (self.min_z + self.max_z) / 2
        )
    
    @property
    def max_dimension(self) -> float:
        return max(self.width, self.height, self.depth)
    
    def with_padding_percent(self, percent: float) -> 'BoundingBox3D':
        """Return a new bounding box with percentage-based padding."""
        pad_x = self.width * percent
        pad_y = self.height * percent
        pad_z = self.depth * percent
        return BoundingBox3D(
            self.min_x - pad_x, self.min_y - pad_y, self.min_z - pad_z,
            self.max_x + pad_x, self.max_y + pad_y, self.max_z + pad_z
        )


class TurtleState3D:
    """Current state of the 3D turtle with HLU orientation."""
    
    def __init__(self, use_numpy: bool = True):
        self.use_numpy = use_numpy and HAS_NUMPY
        
        if self.use_numpy:
            self.position = np.array([0.0, 0.0, 0.0])
            self.H = np.array([0.0, 1.0, 0.0])   # Heading (forward/up)
            self.L = np.array([-1.0, 0.0, 0.0])  # Left
            self.U = np.array([0.0, 0.0, 1.0])   # Up (orthogonal to H and L)
        else:
            self.position = [0.0, 0.0, 0.0]
            self.H = [0.0, 1.0, 0.0]
            self.L = [-1.0, 0.0, 0.0]
            self.U = [0.0, 0.0, 1.0]
        
        self.depth = 0
        self.width = 1.0
        self.step_size = 10.0
        self.color_index = 0  # For color cycling
        
        # Polygon mode
        self.in_polygon = False
        self.polygon_vertices: List[Tuple[float, float, float]] = []
    
    def rotate_yaw(self, angle_deg: float) -> None:
        """Rotate around U axis (turn left/right in local frame)."""
        if self.use_numpy:
            R = _rotation_matrix_np(self.U, angle_deg)
            self.H = R @ self.H
            self.L = R @ self.L
        else:
            R = _rotation_matrix_py(self.U, angle_deg)
            self.H = _mat_vec_mul_py(R, self.H)
            self.L = _mat_vec_mul_py(R, self.L)
    
    def rotate_pitch(self, angle_deg: float) -> None:
        """Rotate around L axis (pitch up/down)."""
        if self.use_numpy:
            R = _rotation_matrix_np(self.L, angle_deg)
            self.H = R @ self.H
            self.U = R @ self.U
        else:
            R = _rotation_matrix_py(self.L, angle_deg)
            self.H = _mat_vec_mul_py(R, self.H)
            self.U = _mat_vec_mul_py(R, self.U)
    
    def rotate_roll(self, angle_deg: float) -> None:
        """Rotate around H axis (roll)."""
        if self.use_numpy:
            R = _rotation_matrix_np(self.H, angle_deg)
            self.L = R @ self.L
            self.U = R @ self.U
        else:
            R = _rotation_matrix_py(self.H, angle_deg)
            self.L = _mat_vec_mul_py(R, self.L)
            self.U = _mat_vec_mul_py(R, self.U)
    
    def turn_around(self) -> None:
        """Turn 180 degrees around U axis."""
        self.rotate_yaw(180)
    
    def roll_to_horizontal(self) -> None:
        """
        Roll turtle so L vector is horizontal ($ symbol).
        Projects L onto horizontal plane and recalculates U.
        Used to keep leaves/branches oriented properly relative to gravity.
        """
        # Gravity vector points down in Y
        gravity = [0.0, -1.0, 0.0]
        
        if self.use_numpy:
            gravity = np.array(gravity)
            # L should be orthogonal to H
            # Project L onto the horizontal plane (perpendicular to gravity)
            # New L = H × gravity (normalized)
            new_L = np.cross(self.H, -gravity)
            if np.linalg.norm(new_L) > 1e-6:
                self.L = new_L / np.linalg.norm(new_L)
                self.U = np.cross(self.H, self.L)
        else:
            # H × gravity
            new_L = _cross_py(self.H, [-g for g in gravity])
            length = math.sqrt(sum(x*x for x in new_L))
            if length > 1e-6:
                self.L = [x/length for x in new_L]
                self.U = _cross_py(self.H, self.L)
    
    def orthonormalize(self) -> None:
        """Re-orthonormalize HLU vectors to prevent numerical drift."""
        if self.use_numpy:
            self.H = self.H / np.linalg.norm(self.H)
            self.L = self.L - np.dot(self.H, self.L) * self.H
            self.L = self.L / np.linalg.norm(self.L)
            self.U = np.cross(self.H, self.L)
        else:
            self.H = _normalize_py(self.H)
            proj = _dot_py(self.H, self.L)
            self.L = [self.L[i] - proj * self.H[i] for i in range(3)]
            self.L = _normalize_py(self.L)
            self.U = _cross_py(self.H, self.L)
    
    def copy(self) -> 'TurtleState3D':
        """Create a deep copy of the state."""
        new_state = TurtleState3D(self.use_numpy)
        if self.use_numpy:
            new_state.position = self.position.copy()
            new_state.H = self.H.copy()
            new_state.L = self.L.copy()
            new_state.U = self.U.copy()
        else:
            new_state.position = self.position.copy()
            new_state.H = self.H.copy()
            new_state.L = self.L.copy()
            new_state.U = self.U.copy()
        new_state.depth = self.depth
        new_state.width = self.width
        new_state.step_size = self.step_size
        new_state.color_index = self.color_index
        new_state.in_polygon = self.in_polygon
        new_state.polygon_vertices = self.polygon_vertices.copy()
        return new_state


def apply_tropism(heading, tropism_vector, elasticity: float = 0.2):
    """
    Bend heading toward tropism direction.
    
    Uses the ABOP torque formula: α = e|H × T|
    
    Args:
        heading: Current heading vector
        tropism_vector: Direction of environmental stimulus
        elasticity: Bend strength (0.1-0.3 subtle, 0.5+ dramatic)
        
    Returns:
        New heading vector bent toward tropism
    """
    if HAS_NUMPY:
        # H' = normalize(H + e * (T - (T·H)H))
        dot = np.dot(tropism_vector, heading)
        bent = heading + elasticity * (tropism_vector - dot * heading)
        return bent / np.linalg.norm(bent)
    else:
        dot = _dot_py(tropism_vector, heading)
        bent = [heading[i] + elasticity * (tropism_vector[i] - dot * heading[i]) 
                for i in range(3)]
        return _normalize_py(bent)


class InterpretResult3D(NamedTuple):
    """Result of interpreting a 3D L-system string."""
    segments: List[Segment3D]
    polygons: List[Polygon3D]


class TurtleInterpreter3D:
    """
    Interprets L-system strings using 3D turtle graphics.
    
    Supports full 3D orientation with HLU vectors and ABOP symbols:
    
    Movement:
    - F: Move forward and draw line segment
    - f: Move forward without drawing
    - G: Move forward without drawing (for polygon edges)
    
    Rotations:
    - +: Turn left (yaw positive)
    - -: Turn right (yaw negative)
    - &: Pitch down
    - ^: Pitch up
    - /: Roll right
    - \\: Roll left
    - |: Turn around (180°)
    
    Stack operations:
    - [: Push state (start branch)
    - ]: Pop state (end branch)
    
    ABOP extensions:
    - !: Decrement diameter (explicit width control)
    - $: Roll to horizontal (align L with gravity)
    - ': Increment color index
    - {: Start polygon mode
    - }: End polygon mode
    - .: Mark current position as polygon vertex
    - %: Cut off remainder of branch
    """
    
    def __init__(
        self,
        angle_delta: float = 25.0,
        roll_angle: Optional[float] = None,
        pitch_angle: Optional[float] = None,
        step_size: float = 10.0,
        initial_width: float = 1.0,
        width_decay: float = 0.7,
        length_decay: float = 0.9,
        width_decrement: float = 0.9,  # Factor for ! symbol
        tropism_vector: Optional[Tuple[float, float, float]] = None,
        tropism_strength: float = 0.0,
        angle_variance: float = 0.0,
        length_variance: float = 0.0,
        random_seed: Optional[int] = None
    ):
        """
        Initialize 3D turtle interpreter.
        
        Args:
            angle_delta: Turning angle in degrees for + and -
            roll_angle: Roll angle for / and \\ (defaults to angle_delta)
            pitch_angle: Pitch angle for & and ^ (defaults to angle_delta)
            step_size: Base length of each F segment
            initial_width: Starting line width
            width_decay: Multiplier for width at each depth level (used with [])
            length_decay: Multiplier for length at each depth level
            width_decrement: Multiplier for ! symbol (explicit width control)
            tropism_vector: Direction of environmental stimulus
            tropism_strength: How strongly to bend toward tropism
            angle_variance: Random variance in angles (0.1 = ±10%)
            length_variance: Random variance in length (0.1 = ±10%)
            random_seed: Seed for reproducible randomness
        """
        self.angle_delta = angle_delta
        self.roll_angle = roll_angle if roll_angle is not None else angle_delta
        self.pitch_angle = pitch_angle if pitch_angle is not None else angle_delta
        self.step_size = step_size
        self.initial_width = initial_width
        self.width_decay = width_decay
        self.length_decay = length_decay
        self.width_decrement = width_decrement
        
        # Tropism
        self.tropism_strength = tropism_strength
        if tropism_vector is not None:
            if HAS_NUMPY:
                self.tropism_vector = np.array(tropism_vector, dtype=float)
                self.tropism_vector = self.tropism_vector / np.linalg.norm(self.tropism_vector)
            else:
                self.tropism_vector = _normalize_py(list(tropism_vector))
        else:
            self.tropism_vector = None
        
        # Stochastic variation
        self.angle_variance = angle_variance
        self.length_variance = length_variance
        
        if random_seed is not None:
            random.seed(random_seed)
    
    def _vary_angle(self, base_angle: float) -> float:
        """Apply random variance to angle."""
        if self.angle_variance > 0:
            variance = base_angle * self.angle_variance
            return base_angle + random.uniform(-variance, variance)
        return base_angle
    
    def _vary_length(self, base_length: float) -> float:
        """Apply random variance to length."""
        if self.length_variance > 0:
            variance = base_length * self.length_variance
            return max(0.1, base_length + random.uniform(-variance, variance))
        return base_length
    
    def interpret(
        self, 
        lsystem_string: str,
        return_polygons: bool = True
    ) -> InterpretResult3D:
        """
        Interpret an L-system string and return 3D segments and polygons.
        
        Args:
            lsystem_string: The L-system string to interpret
            return_polygons: If True, include polygon data in result
            
        Returns:
            InterpretResult3D with segments and polygons lists
        """
        segments = []
        polygons = []
        stack = []
        segment_index = 0
        polygon_index = 0
        
        state = TurtleState3D(use_numpy=HAS_NUMPY)
        state.width = self.initial_width
        state.step_size = self.step_size
        
        i = 0
        while i < len(lsystem_string):
            char = lsystem_string[i]
            
            if char == 'F':
                # Move forward and draw
                step = self._vary_length(state.step_size)
                
                if HAS_NUMPY:
                    new_pos = state.position + step * state.H
                    segment = Segment3D(
                        x1=state.position[0], y1=state.position[1], z1=state.position[2],
                        x2=new_pos[0], y2=new_pos[1], z2=new_pos[2],
                        depth=state.depth,
                        width=state.width,
                        index=segment_index,
                        heading=tuple(state.H),
                        color_index=state.color_index
                    )
                    state.position = new_pos
                else:
                    new_pos = [state.position[j] + step * state.H[j] for j in range(3)]
                    segment = Segment3D(
                        x1=state.position[0], y1=state.position[1], z1=state.position[2],
                        x2=new_pos[0], y2=new_pos[1], z2=new_pos[2],
                        depth=state.depth,
                        width=state.width,
                        index=segment_index,
                        heading=tuple(state.H),
                        color_index=state.color_index
                    )
                    state.position = new_pos
                
                segments.append(segment)
                segment_index += 1
                
                # Apply tropism after movement
                if self.tropism_strength > 0 and self.tropism_vector is not None:
                    state.H = apply_tropism(state.H, self.tropism_vector, self.tropism_strength)
                    state.orthonormalize()
                
            elif char == 'f' or char == 'G':
                # Move forward without drawing
                step = self._vary_length(state.step_size)
                if HAS_NUMPY:
                    state.position = state.position + step * state.H
                else:
                    state.position = [state.position[j] + step * state.H[j] for j in range(3)]
                
            elif char == '+':
                # Turn left (positive yaw)
                state.rotate_yaw(self._vary_angle(self.angle_delta))
                
            elif char == '-':
                # Turn right (negative yaw)
                state.rotate_yaw(self._vary_angle(-self.angle_delta))
                
            elif char == '&':
                # Pitch down
                state.rotate_pitch(self._vary_angle(-self.pitch_angle))
                
            elif char == '^':
                # Pitch up
                state.rotate_pitch(self._vary_angle(self.pitch_angle))
                
            elif char == '\\':
                # Roll left
                state.rotate_roll(self._vary_angle(-self.roll_angle))
                
            elif char == '/':
                # Roll right
                state.rotate_roll(self._vary_angle(self.roll_angle))
                
            elif char == '|':
                # Turn around (180 degrees)
                state.turn_around()
                
            elif char == '[':
                # Push state onto stack
                stack.append(state.copy())
                state.depth += 1
                state.width *= self.width_decay
                state.step_size *= self.length_decay
                
            elif char == ']':
                # Pop state from stack
                if stack:
                    # IMPORTANT: Preserve polygon context across push/pop
                    # In ABOP, polygons can span across branches - the polygon
                    # collects vertices as the turtle moves, regardless of push/pop
                    was_in_polygon = state.in_polygon
                    polygon_verts = state.polygon_vertices
                    color_idx = state.color_index
                    
                    state = stack.pop()
                    
                    # Restore polygon context if we were recording
                    if was_in_polygon:
                        state.in_polygon = True
                        state.polygon_vertices = polygon_verts
                        state.color_index = color_idx
            
            # ABOP extension symbols
            elif char == '!':
                # Decrement diameter
                state.width *= self.width_decrement
                
            elif char == '$':
                # Roll to horizontal
                state.roll_to_horizontal()
                
            elif char == "'":
                # Increment color index
                state.color_index += 1
                
            elif char == '{':
                # Start polygon mode (don't add vertex - use . for that)
                state.in_polygon = True
                state.polygon_vertices = []
                    
            elif char == '}':
                # End polygon mode
                if state.in_polygon:
                    poly = Polygon3D(
                        vertices=state.polygon_vertices.copy(),
                        depth=state.depth,
                        color_index=state.color_index,
                        index=polygon_index
                    )
                    if poly.is_valid():
                        poly.normal = poly.calculate_normal()
                        polygons.append(poly)
                        polygon_index += 1
                    state.in_polygon = False
                    state.polygon_vertices = []
                    
            elif char == '.':
                # Mark current position as polygon vertex
                if state.in_polygon:
                    if HAS_NUMPY:
                        state.polygon_vertices.append(tuple(state.position))
                    else:
                        state.polygon_vertices.append(tuple(state.position))
                        
            elif char == '%':
                # Cut off remainder of branch - skip to matching ]
                bracket_depth = 1
                i += 1
                while i < len(lsystem_string) and bracket_depth > 0:
                    if lsystem_string[i] == '[':
                        bracket_depth += 1
                    elif lsystem_string[i] == ']':
                        bracket_depth -= 1
                    i += 1
                i -= 1  # Adjust because outer loop will increment
            
            # Periodically orthonormalize to prevent drift
            if segment_index > 0 and segment_index % 100 == 0:
                state.orthonormalize()
            
            i += 1
        
        return InterpretResult3D(segments=segments, polygons=polygons)
    
    def interpret_legacy(self, lsystem_string: str) -> List[Segment3D]:
        """
        Legacy interpret method for backward compatibility.
        
        Returns only segments list, ignoring polygons.
        """
        result = self.interpret(lsystem_string, return_polygons=False)
        return result.segments
    
    def get_bounding_box(
        self, 
        segments: List[Segment3D],
        polygons: Optional[List[Polygon3D]] = None
    ) -> BoundingBox3D:
        """Calculate 3D bounding box for segments and polygons."""
        if not segments and (not polygons or not any(p.vertices for p in polygons)):
            return BoundingBox3D(0, 0, 0, 1, 1, 1)
        
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')
        
        for seg in segments:
            min_x = min(min_x, seg.x1, seg.x2)
            min_y = min(min_y, seg.y1, seg.y2)
            min_z = min(min_z, seg.z1, seg.z2)
            max_x = max(max_x, seg.x1, seg.x2)
            max_y = max(max_y, seg.y1, seg.y2)
            max_z = max(max_z, seg.z1, seg.z2)
        
        if polygons:
            for poly in polygons:
                for x, y, z in poly.vertices:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    min_z = min(min_z, z)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
                    max_z = max(max_z, z)
        
        # Ensure minimum size
        for min_val, max_val in [(min_x, max_x), (min_y, max_y), (min_z, max_z)]:
            if max_val - min_val < 1:
                mid = (max_val + min_val) / 2
                if min_val == min_x:
                    min_x, max_x = mid - 0.5, mid + 0.5
                elif min_val == min_y:
                    min_y, max_y = mid - 0.5, mid + 0.5
                else:
                    min_z, max_z = mid - 0.5, mid + 0.5
        
        return BoundingBox3D(min_x, min_y, min_z, max_x, max_y, max_z)
    
    def get_max_depth(self, segments: List[Segment3D]) -> int:
        """Get the maximum depth level from segments."""
        if not segments:
            return 0
        return max(seg.depth for seg in segments)
    
    def get_max_color_index(self, segments: List[Segment3D]) -> int:
        """Get the maximum color index from segments."""
        if not segments:
            return 0
        return max(seg.color_index for seg in segments)
    
    def to_2d_segments(self, segments_3d: List[Segment3D]) -> List:
        """Convert 3D segments to 2D (XY projection)."""
        return [seg.to_2d_segment() for seg in segments_3d]


def detect_3d_symbols(lsystem_string: str) -> bool:
    """
    Detect if an L-system string contains 3D-specific symbols.
    
    Args:
        lsystem_string: The L-system string to check
        
    Returns:
        True if 3D symbols are present
    """
    symbols_3d = {'&', '^', '/', '\\', '|', '$'}
    return bool(symbols_3d.intersection(set(lsystem_string)))


def detect_3d_rules(rules: dict) -> bool:
    """
    Detect if L-system rules contain 3D-specific symbols.
    
    Args:
        rules: Dictionary of production rules
        
    Returns:
        True if 3D symbols are present in any rule
    """
    for replacement in rules.values():
        if detect_3d_symbols(replacement):
            return True
    return False
