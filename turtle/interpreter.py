"""
Turtle Graphics Interpreter

Converts L-system strings to 2D line segments for rendering.
Supports ABOP (The Algorithmic Beauty of Plants) symbols.
"""

import math
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, NamedTuple


@dataclass
class Segment:
    """A line segment with position, depth, and width information."""
    x1: float
    y1: float
    x2: float
    y2: float
    depth: int
    width: float
    index: int = 0  # Order in which segment was created (for animation)
    color_index: int = 0  # For color cycling with ' symbol
    
    def length(self) -> float:
        """Calculate segment length."""
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return math.sqrt(dx * dx + dy * dy)
    
    def partial(self, visibility: float) -> 'Segment':
        """
        Create a partial segment drawn to the given visibility percentage.
        
        Args:
            visibility: 0.0 to 1.0 representing how much of segment to show
            
        Returns:
            New Segment with endpoint adjusted
        """
        if visibility >= 1.0:
            return self
        if visibility <= 0.0:
            return Segment(self.x1, self.y1, self.x1, self.y1, 
                          self.depth, self.width, self.index, self.color_index)
        
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return Segment(
            self.x1, self.y1,
            self.x1 + dx * visibility,
            self.y1 + dy * visibility,
            self.depth,
            self.width,
            self.index,
            self.color_index
        )


@dataclass
class Polygon:
    """A filled polygon for leaf/petal shapes."""
    vertices: List[Tuple[float, float]]
    depth: int
    color_index: int = 0
    index: int = 0  # Creation order for animation
    
    def is_valid(self) -> bool:
        """Check if polygon has enough vertices."""
        return len(self.vertices) >= 3


@dataclass
class BoundingBox:
    """Bounding box for a set of segments."""
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    
    @property
    def width(self) -> float:
        return self.max_x - self.min_x
    
    @property
    def height(self) -> float:
        return self.max_y - self.min_y
    
    @property
    def center_x(self) -> float:
        return (self.min_x + self.max_x) / 2
    
    @property
    def center_y(self) -> float:
        return (self.min_y + self.max_y) / 2
    
    def with_padding(self, padding: float) -> 'BoundingBox':
        """Return a new bounding box with padding added."""
        return BoundingBox(
            self.min_x - padding,
            self.min_y - padding,
            self.max_x + padding,
            self.max_y + padding
        )
    
    def with_padding_percent(self, percent: float) -> 'BoundingBox':
        """Return a new bounding box with percentage-based padding."""
        pad_x = self.width * percent
        pad_y = self.height * percent
        return BoundingBox(
            self.min_x - pad_x,
            self.min_y - pad_y,
            self.max_x + pad_x,
            self.max_y + pad_y
        )


@dataclass
class TurtleState:
    """Current state of the turtle."""
    x: float
    y: float
    angle: float  # In degrees, 0 = right, 90 = up
    depth: int
    width: float
    step_size: float
    color_index: int = 0  # For color cycling
    in_polygon: bool = False  # Whether currently recording polygon vertices
    polygon_vertices: List[Tuple[float, float]] = field(default_factory=list)
    
    def copy(self) -> 'TurtleState':
        """Create a deep copy of the state."""
        return TurtleState(
            x=self.x,
            y=self.y,
            angle=self.angle,
            depth=self.depth,
            width=self.width,
            step_size=self.step_size,
            color_index=self.color_index,
            in_polygon=self.in_polygon,
            polygon_vertices=self.polygon_vertices.copy()
        )


class InterpretResult(NamedTuple):
    """Result of interpreting an L-system string."""
    segments: List[Segment]
    polygons: List[Polygon]


class TurtleInterpreter:
    """
    Interprets L-system strings using turtle graphics.
    
    Converts L-system strings into a list of line segments and filled polygons.
    
    Supported ABOP symbols:
    - F: Move forward and draw line segment
    - f: Move forward without drawing
    - +: Turn left by angle delta
    - -: Turn right by angle delta
    - [: Push current state (start branch)
    - ]: Pop state (end branch)
    - !: Decrement diameter (multiply width by decay factor)
    - ': Increment color index
    - {: Start polygon mode (begin recording vertices)
    - }: End polygon mode (close and store polygon)
    - .: Mark current position as polygon vertex
    - %: Cut off remainder of branch (skip to matching ])
    - G: Move forward without drawing (alias for f, used in polygon mode)
    """
    
    def __init__(
        self,
        angle_delta: float = 25.0,
        step_size: float = 10.0,
        initial_width: float = 1.0,
        width_decay: float = 0.7,
        length_decay: float = 0.9,
        width_decrement: float = 0.9  # Factor for ! symbol
    ):
        """
        Initialize turtle interpreter.
        
        Args:
            angle_delta: Turning angle in degrees for + and -
            step_size: Base length of each F segment
            initial_width: Starting line width
            width_decay: Multiplier for width at each depth level (used with [])
            length_decay: Multiplier for length at each depth level
            width_decrement: Multiplier for ! symbol (explicit width control)
        """
        self.angle_delta = angle_delta
        self.step_size = step_size
        self.initial_width = initial_width
        self.width_decay = width_decay
        self.length_decay = length_decay
        self.width_decrement = width_decrement
    
    def interpret(
        self, 
        lsystem_string: str,
        return_polygons: bool = True
    ) -> InterpretResult:
        """
        Interpret an L-system string and return segments and polygons.
        
        Args:
            lsystem_string: The L-system string to interpret
            return_polygons: If True, include polygon data in result
            
        Returns:
            InterpretResult with segments and polygons lists
        """
        segments = []
        polygons = []
        stack = []
        segment_index = 0
        polygon_index = 0
        
        # Initial state: at origin, pointing up (90 degrees)
        state = TurtleState(
            x=0.0,
            y=0.0,
            angle=90.0,
            depth=0,
            width=self.initial_width,
            step_size=self.step_size,
            color_index=0,
            in_polygon=False,
            polygon_vertices=[]
        )
        
        i = 0
        while i < len(lsystem_string):
            char = lsystem_string[i]
            
            if char == 'F':
                # Move forward and draw
                rad = math.radians(state.angle)
                new_x = state.x + state.step_size * math.cos(rad)
                new_y = state.y + state.step_size * math.sin(rad)
                
                # Create segment
                segment = Segment(
                    x1=state.x,
                    y1=state.y,
                    x2=new_x,
                    y2=new_y,
                    depth=state.depth,
                    width=state.width,
                    index=segment_index,
                    color_index=state.color_index
                )
                segments.append(segment)
                segment_index += 1
                
                # Update position
                state.x = new_x
                state.y = new_y
                
            elif char == 'f' or char == 'G':
                # Move forward without drawing
                rad = math.radians(state.angle)
                state.x += state.step_size * math.cos(rad)
                state.y += state.step_size * math.sin(rad)
                
                # In ABOP polygon mode, f movements automatically add vertices
                if state.in_polygon:
                    state.polygon_vertices.append((state.x, state.y))
                
            elif char == '+':
                # Turn left (counter-clockwise)
                state.angle += self.angle_delta
                
            elif char == '-':
                # Turn right (clockwise)
                state.angle -= self.angle_delta
                
            elif char == '|':
                # Turn around 180 degrees (ABOP symbol)
                state.angle += 180
                
            elif char == '[':
                # Push state onto stack and increase depth
                stack.append(state.copy())
                # Update state for new branch
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
                    
            elif char == '!':
                # Decrement diameter (ABOP width control)
                state.width *= self.width_decrement
                
            elif char == "'":
                # Increment color index
                state.color_index += 1
                
            elif char == '{':
                # Start polygon mode - add current position as first vertex (ABOP style)
                state.in_polygon = True
                state.polygon_vertices = [(state.x, state.y)]
                
            elif char == '}':
                # End polygon mode
                if state.in_polygon:
                    # Close and store polygon
                    poly = Polygon(
                        vertices=state.polygon_vertices.copy(),
                        depth=state.depth,
                        color_index=state.color_index,
                        index=polygon_index
                    )
                    if poly.is_valid():
                        polygons.append(poly)
                        polygon_index += 1
                    state.in_polygon = False
                    state.polygon_vertices = []
                    
            elif char == '.':
                # Mark current position as polygon vertex
                if state.in_polygon:
                    state.polygon_vertices.append((state.x, state.y))
                    
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
                # Adjust i because outer loop will increment
                i -= 1
            
            # Characters like X, Y, A, B are ignored (placeholders)
            i += 1
        
        return InterpretResult(segments=segments, polygons=polygons)
    
    def interpret_legacy(self, lsystem_string: str) -> List[Segment]:
        """
        Legacy interpret method for backward compatibility.
        
        Returns only segments list, ignoring polygons.
        """
        result = self.interpret(lsystem_string, return_polygons=False)
        return result.segments
    
    def get_bounding_box(
        self, 
        segments: List[Segment],
        polygons: Optional[List[Polygon]] = None
    ) -> BoundingBox:
        """
        Calculate bounding box for segments and polygons.
        
        Args:
            segments: List of Segment objects
            polygons: Optional list of Polygon objects
            
        Returns:
            BoundingBox containing all geometry
        """
        if not segments and (not polygons or not any(p.vertices for p in polygons)):
            return BoundingBox(0, 0, 1, 1)
        
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        
        for seg in segments:
            min_x = min(min_x, seg.x1, seg.x2)
            min_y = min(min_y, seg.y1, seg.y2)
            max_x = max(max_x, seg.x1, seg.x2)
            max_y = max(max_y, seg.y1, seg.y2)
        
        if polygons:
            for poly in polygons:
                for x, y in poly.vertices:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
        
        # Ensure minimum size
        if max_x - min_x < 1:
            mid = (max_x + min_x) / 2
            min_x = mid - 0.5
            max_x = mid + 0.5
        if max_y - min_y < 1:
            mid = (max_y + min_y) / 2
            min_y = mid - 0.5
            max_y = mid + 0.5
        
        return BoundingBox(min_x, min_y, max_x, max_y)
    
    def get_max_depth(self, segments: List[Segment]) -> int:
        """Get the maximum depth level from segments."""
        if not segments:
            return 0
        return max(seg.depth for seg in segments)
    
    def get_max_color_index(self, segments: List[Segment]) -> int:
        """Get the maximum color index from segments."""
        if not segments:
            return 0
        return max(seg.color_index for seg in segments)