"""
Turtle Graphics Interpreter

Converts L-system strings to 2D line segments for rendering.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


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
                          self.depth, self.width, self.index)
        
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return Segment(
            self.x1, self.y1,
            self.x1 + dx * visibility,
            self.y1 + dy * visibility,
            self.depth,
            self.width,
            self.index
        )


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


class TurtleInterpreter:
    """
    Interprets L-system strings using turtle graphics.
    
    Converts L-system strings into a list of line segments.
    """
    
    def __init__(
        self,
        angle_delta: float = 25.0,
        step_size: float = 10.0,
        initial_width: float = 1.0,
        width_decay: float = 0.7,
        length_decay: float = 0.9
    ):
        """
        Initialize turtle interpreter.
        
        Args:
            angle_delta: Turning angle in degrees for + and -
            step_size: Base length of each F segment
            initial_width: Starting line width
            width_decay: Multiplier for width at each depth level
            length_decay: Multiplier for length at each depth level
        """
        self.angle_delta = angle_delta
        self.step_size = step_size
        self.initial_width = initial_width
        self.width_decay = width_decay
        self.length_decay = length_decay
    
    def interpret(self, lsystem_string: str) -> List[Segment]:
        """
        Interpret an L-system string and return list of segments.
        
        Args:
            lsystem_string: The L-system string to interpret
            
        Returns:
            List of Segment objects in the order they were drawn
        """
        segments = []
        stack = []
        segment_index = 0
        
        # Initial state: at origin, pointing up (90 degrees)
        state = TurtleState(
            x=0.0,
            y=0.0,
            angle=90.0,
            depth=0,
            width=self.initial_width,
            step_size=self.step_size
        )
        
        for char in lsystem_string:
            if char == 'F':
                # Move forward and draw
                # Calculate new position
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
                    index=segment_index
                )
                segments.append(segment)
                segment_index += 1
                
                # Update position
                state.x = new_x
                state.y = new_y
                
            elif char == 'f':
                # Move forward without drawing
                rad = math.radians(state.angle)
                state.x += state.step_size * math.cos(rad)
                state.y += state.step_size * math.sin(rad)
                
            elif char == '+':
                # Turn left (counter-clockwise)
                state.angle += self.angle_delta
                
            elif char == '-':
                # Turn right (clockwise)
                state.angle -= self.angle_delta
                
            elif char == '[':
                # Push state onto stack and increase depth
                stack.append(TurtleState(
                    x=state.x,
                    y=state.y,
                    angle=state.angle,
                    depth=state.depth,
                    width=state.width,
                    step_size=state.step_size
                ))
                # Update state for new branch
                state.depth += 1
                state.width *= self.width_decay
                state.step_size *= self.length_decay
                
            elif char == ']':
                # Pop state from stack
                if stack:
                    state = stack.pop()
            
            # Characters like X, Y, A, B are ignored (placeholders)
        
        return segments
    
    def get_bounding_box(self, segments: List[Segment]) -> BoundingBox:
        """
        Calculate bounding box for a list of segments.
        
        Args:
            segments: List of Segment objects
            
        Returns:
            BoundingBox containing all segments
        """
        if not segments:
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
