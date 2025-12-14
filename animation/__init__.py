"""Animation controller module."""
from .controller import (
    AnimationController,
    GrowthMode,
    GrowthPreview,
    ease_out_cubic,
    ease_out_quad,
    ease_in_out_cubic,
    sigmoid_growth
)

__all__ = [
    'AnimationController',
    'GrowthMode',
    'GrowthPreview',
    'ease_out_cubic',
    'ease_out_quad',
    'ease_in_out_cubic',
    'sigmoid_growth'
]
