"""POV-Ray rendering module."""
from .generator import POVRayGenerator, ColorMode, depth_to_color
from .renderer import POVRayRenderer, POVRayError, check_povray_available

# Import 3D generator
try:
    from .generator3d import POVRayGenerator3D, depth_to_color_3d
    HAS_3D = True
except ImportError:
    HAS_3D = False

__all__ = [
    'POVRayGenerator', 
    'POVRayRenderer', 
    'POVRayError',
    'ColorMode',
    'depth_to_color',
    'check_povray_available'
]

if HAS_3D:
    __all__.extend(['POVRayGenerator3D', 'depth_to_color_3d'])
