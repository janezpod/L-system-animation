"""Turtle graphics interpreter module."""
from .interpreter import (
    TurtleInterpreter, 
    Segment, 
    BoundingBox, 
    Polygon,
    TurtleState,
    InterpretResult
)

# Import 3D components
try:
    from .interpreter3d import (
        TurtleInterpreter3D, 
        Segment3D, 
        BoundingBox3D,
        Polygon3D,
        TurtleState3D,
        InterpretResult3D,
        detect_3d_symbols,
        detect_3d_rules,
        GOLDEN_ANGLE,
        apply_tropism
    )
    HAS_3D = True
except ImportError:
    HAS_3D = False

__all__ = [
    'TurtleInterpreter', 
    'Segment', 
    'BoundingBox',
    'Polygon',
    'TurtleState',
    'InterpretResult'
]

if HAS_3D:
    __all__.extend([
        'TurtleInterpreter3D', 
        'Segment3D', 
        'BoundingBox3D',
        'Polygon3D',
        'TurtleState3D',
        'InterpretResult3D',
        'detect_3d_symbols',
        'detect_3d_rules',
        'GOLDEN_ANGLE',
        'apply_tropism'
    ])
