"""
Enhanced Tropism Implementation

Based on ABOP Pages 57-58, Figure 2.9

Implements the exact ABOP tropism formula:
    α = e × |H × T|

Where:
- H: heading vector (turtle's forward direction)
- T: tropism direction (e.g., gravity = [0, -1, 0])
- e: susceptibility coefficient (elasticity)
- α: rotation angle

The rotation is around axis (H × T), which represents the torque
if T is interpreted as a force acting on the heading vector H.
"""

import math
from typing import Tuple, List, Optional

# Try to use numpy
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def apply_tropism_abop(
    H: 'np.ndarray',
    L: 'np.ndarray', 
    U: 'np.ndarray',
    T: 'np.ndarray',
    e: float
) -> Tuple['np.ndarray', 'np.ndarray', 'np.ndarray']:
    """
    Apply tropism following exact ABOP formula.
    
    ABOP Page 57-58, Figure 2.9:
    
    α = e × |H × T|
    
    Where:
    - H: heading vector
    - T: tropism direction (gravity = [0, -1, 0] for gravitropism)
    - e: susceptibility coefficient
    - α: rotation angle
    
    The rotation is around axis (H × T), which represents
    the torque if T is interpreted as a force on H.
    
    Args:
        H: Current heading vector (normalized)
        L: Current left vector (normalized)
        U: Current up vector (normalized)
        T: Tropism direction vector (normalized)
        e: Susceptibility coefficient (0.1-0.3 subtle, 0.5+ dramatic)
        
    Returns:
        Tuple of (new_H, new_L, new_U) after tropism rotation
    """
    if not HAS_NUMPY:
        return _apply_tropism_abop_py(H, L, U, T, e)
    
    # Cross product gives rotation axis and torque magnitude
    cross = np.cross(H, T)
    torque = np.linalg.norm(cross)
    
    if torque < 1e-10:
        return H, L, U  # No rotation if parallel (or anti-parallel)
    
    # ABOP formula: angle = e * torque
    alpha = e * torque
    
    # Normalize rotation axis
    axis = cross / torque
    
    # Apply rotation using Rodrigues' formula
    H_new = _rotate_around_axis_np(H, axis, alpha)
    L_new = _rotate_around_axis_np(L, axis, alpha)
    U_new = _rotate_around_axis_np(U, axis, alpha)
    
    # Orthonormalize to prevent drift
    H_new = H_new / np.linalg.norm(H_new)
    L_new = np.cross(U_new, H_new)
    L_new = L_new / np.linalg.norm(L_new)
    U_new = np.cross(H_new, L_new)
    
    return H_new, L_new, U_new


def _rotate_around_axis_np(v: 'np.ndarray', axis: 'np.ndarray', angle: float) -> 'np.ndarray':
    """
    Rotate vector v around axis by angle (radians).
    
    Uses Rodrigues' rotation formula:
    v' = v*cos(θ) + (axis × v)*sin(θ) + axis*(axis·v)*(1-cos(θ))
    
    Args:
        v: Vector to rotate
        axis: Rotation axis (normalized)
        angle: Rotation angle in radians
        
    Returns:
        Rotated vector
    """
    c = np.cos(angle)
    s = np.sin(angle)
    
    return (v * c + 
            np.cross(axis, v) * s + 
            axis * np.dot(axis, v) * (1 - c))


# =============================================================================
# Pure Python Fallback
# =============================================================================

def _apply_tropism_abop_py(
    H: List[float],
    L: List[float],
    U: List[float],
    T: List[float],
    e: float
) -> Tuple[List[float], List[float], List[float]]:
    """Pure Python implementation of ABOP tropism."""
    
    # Cross product H × T
    cross = [
        H[1] * T[2] - H[2] * T[1],
        H[2] * T[0] - H[0] * T[2],
        H[0] * T[1] - H[1] * T[0]
    ]
    
    # Torque magnitude
    torque = math.sqrt(cross[0]**2 + cross[1]**2 + cross[2]**2)
    
    if torque < 1e-10:
        return H, L, U
    
    # Rotation angle
    alpha = e * torque
    
    # Normalize axis
    axis = [c / torque for c in cross]
    
    # Rotate each vector
    H_new = _rotate_around_axis_py(H, axis, alpha)
    L_new = _rotate_around_axis_py(L, axis, alpha)
    U_new = _rotate_around_axis_py(U, axis, alpha)
    
    # Orthonormalize
    H_len = math.sqrt(sum(x**2 for x in H_new))
    H_new = [x / H_len for x in H_new]
    
    # L = U × H
    L_new = [
        U_new[1] * H_new[2] - U_new[2] * H_new[1],
        U_new[2] * H_new[0] - U_new[0] * H_new[2],
        U_new[0] * H_new[1] - U_new[1] * H_new[0]
    ]
    L_len = math.sqrt(sum(x**2 for x in L_new))
    if L_len > 1e-10:
        L_new = [x / L_len for x in L_new]
    
    # U = H × L
    U_new = [
        H_new[1] * L_new[2] - H_new[2] * L_new[1],
        H_new[2] * L_new[0] - H_new[0] * L_new[2],
        H_new[0] * L_new[1] - H_new[1] * L_new[0]
    ]
    
    return H_new, L_new, U_new


def _rotate_around_axis_py(v: List[float], axis: List[float], angle: float) -> List[float]:
    """Pure Python Rodrigues rotation."""
    c = math.cos(angle)
    s = math.sin(angle)
    
    # axis × v
    cross = [
        axis[1] * v[2] - axis[2] * v[1],
        axis[2] * v[0] - axis[0] * v[2],
        axis[0] * v[1] - axis[1] * v[0]
    ]
    
    # axis · v
    dot = axis[0] * v[0] + axis[1] * v[1] + axis[2] * v[2]
    
    return [
        v[i] * c + cross[i] * s + axis[i] * dot * (1 - c)
        for i in range(3)
    ]


# =============================================================================
# Tropism Types (ABOP Section 2.2)
# =============================================================================

class TropismType:
    """Common tropism direction vectors."""
    
    # Gravitropism - response to gravity
    GRAVITY_DOWN = [0.0, -1.0, 0.0]  # Negative gravitropism (shoots grow up)
    GRAVITY_UP = [0.0, 1.0, 0.0]     # Positive gravitropism (roots grow down)
    
    # Phototropism - response to light
    LIGHT_UP = [0.0, 1.0, 0.0]       # Toward overhead light
    LIGHT_SIDE = [1.0, 0.0, 0.0]     # Toward side light
    
    # Custom
    @staticmethod
    def custom(x: float, y: float, z: float) -> List[float]:
        """Create custom tropism direction (will be normalized)."""
        length = math.sqrt(x*x + y*y + z*z)
        if length < 1e-10:
            return [0.0, -1.0, 0.0]  # Default to gravity
        return [x/length, y/length, z/length]


def calculate_optimal_tropism(
    branch_type: str = 'shoot',
    sun_angle: float = 0.0
) -> Tuple[List[float], float]:
    """
    Calculate appropriate tropism parameters for branch type.
    
    Based on botanical observations in ABOP.
    
    Args:
        branch_type: 'shoot', 'branch', 'root', 'flower'
        sun_angle: Angle of sun from vertical (degrees)
        
    Returns:
        Tuple of (tropism_vector, susceptibility)
    """
    if branch_type == 'shoot':
        # Main shoots show negative gravitropism
        return TropismType.GRAVITY_DOWN, 0.22
    
    elif branch_type == 'branch':
        # Branches show weaker tropism, more horizontal growth
        return TropismType.GRAVITY_DOWN, 0.14
    
    elif branch_type == 'root':
        # Roots show positive gravitropism
        return TropismType.GRAVITY_UP, 0.3
    
    elif branch_type == 'flower':
        # Flowers often orient toward light
        sun_rad = math.radians(sun_angle)
        vec = [math.sin(sun_rad), math.cos(sun_rad), 0.0]
        return vec, 0.4
    
    else:
        # Default
        return TropismType.GRAVITY_DOWN, 0.2


# =============================================================================
# Integration with Turtle Interpreter
# =============================================================================

def create_tropism_callback(
    tropism_vector: List[float],
    susceptibility: float
):
    """
    Create a callback function for use with turtle interpreter.
    
    Args:
        tropism_vector: Direction of tropism
        susceptibility: Bend strength
        
    Returns:
        Function that applies tropism to turtle state
    """
    if HAS_NUMPY:
        T = np.array(tropism_vector)
        T = T / np.linalg.norm(T)
        
        def apply_tropism(H, L, U):
            return apply_tropism_abop(H, L, U, T, susceptibility)
    else:
        length = math.sqrt(sum(x**2 for x in tropism_vector))
        T = [x / length for x in tropism_vector]
        
        def apply_tropism(H, L, U):
            return _apply_tropism_abop_py(H, L, U, T, susceptibility)
    
    return apply_tropism


# =============================================================================
# Heading-Only Tropism (Simpler Version)
# =============================================================================

def apply_tropism_heading_only(
    heading: List[float],
    tropism_vector: List[float],
    elasticity: float = 0.2
) -> List[float]:
    """
    Simplified tropism that only modifies the heading vector.
    
    Uses the formula: H' = normalize(H + e * (T - (T·H)H))
    
    This projects the tropism vector onto the plane perpendicular to H,
    then blends toward it. Simpler but doesn't maintain full HLU frame.
    
    Args:
        heading: Current heading vector
        tropism_vector: Direction of tropism
        elasticity: Blend factor
        
    Returns:
        New heading vector
    """
    if HAS_NUMPY:
        H = np.array(heading)
        T = np.array(tropism_vector)
        
        dot = np.dot(T, H)
        bent = H + elasticity * (T - dot * H)
        return (bent / np.linalg.norm(bent)).tolist()
    else:
        dot = sum(tropism_vector[i] * heading[i] for i in range(3))
        bent = [
            heading[i] + elasticity * (tropism_vector[i] - dot * heading[i])
            for i in range(3)
        ]
        length = math.sqrt(sum(x**2 for x in bent))
        return [x / length for x in bent]


# =============================================================================
# Wind Effect (Extension of Tropism)
# =============================================================================

def apply_wind_effect(
    H: List[float],
    L: List[float],
    U: List[float],
    wind_direction: List[float],
    wind_strength: float,
    flexibility: float = 1.0
) -> Tuple[List[float], List[float], List[float]]:
    """
    Apply wind effect to turtle orientation.
    
    Wind is modeled as a horizontal tropism with time-varying strength.
    
    Args:
        H, L, U: Current turtle orientation
        wind_direction: Wind direction (horizontal)
        wind_strength: Base wind strength
        flexibility: Branch flexibility (younger branches bend more)
        
    Returns:
        Modified (H, L, U) orientation
    """
    effective_strength = wind_strength * flexibility
    
    if HAS_NUMPY:
        T = np.array(wind_direction)
        return apply_tropism_abop(
            np.array(H), np.array(L), np.array(U),
            T, effective_strength
        )
    else:
        return _apply_tropism_abop_py(H, L, U, wind_direction, effective_strength)
