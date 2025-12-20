"""
Surfaces Module for L-System Plant Organs

Based on ABOP Chapter 5: Models of Plant Organs

This module provides predefined surface shapes for botanical modeling:
- Leaves (cordate, lanceolate, ovate, palmate)
- Petals (rose, tulip, daisy)
- Structural elements (disks, cones)

Usage:
    from lsystem.surfaces import SURFACE_LIBRARY, create_cordate_leaf
    
    # Get predefined surface
    leaf = SURFACE_LIBRARY.get('L')
    
    # Create custom leaf
    my_leaf = create_cordate_leaf(scale=2.0)
"""

from .library import (
    # Base classes
    Surface,
    ControlPoint,
    DiskSurface,
    ConeSurface,
    BezierPatchSurface,
    
    # Leaf creators
    create_cordate_leaf,
    create_lanceolate_leaf,
    create_ovate_leaf,
    create_palmate_leaf,
    
    # Petal creators
    create_rose_petal,
    create_tulip_petal,
    create_daisy_petal,
    
    # Developmental model
    DevelopmentalLeaf,
    
    # Library manager
    SurfaceLibrary,
    SURFACE_LIBRARY,
    
    # Utilities
    create_flower_head,
    phyllotaxis_surface_positions,
)

__all__ = [
    'Surface',
    'ControlPoint',
    'DiskSurface',
    'ConeSurface', 
    'BezierPatchSurface',
    'create_cordate_leaf',
    'create_lanceolate_leaf',
    'create_ovate_leaf',
    'create_palmate_leaf',
    'create_rose_petal',
    'create_tulip_petal',
    'create_daisy_petal',
    'DevelopmentalLeaf',
    'SurfaceLibrary',
    'SURFACE_LIBRARY',
    'create_flower_head',
    'phyllotaxis_surface_positions',
]
