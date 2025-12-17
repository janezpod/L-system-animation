"""L-System engine module."""
from .engine import LSystem, parse_rules, LSystemError
from .presets import (
    PRESETS, 
    PRESETS_3D, 
    PARAMETRIC_PRESETS,
    get_preset, 
    list_presets,
    get_parametric_preset,
    list_parametric_presets,
    list_presets_by_category,
    get_preset_info,
    GOLDEN_ANGLE,
    LEONARDO_WIDTH_DECAY,
    HONDA_BRANCHING_ANGLE
)

# Import parametric L-system components
try:
    from .parametric import (
        ParametricLSystem,
        ParametricLSystemError,
        Module,
        Production,
        parse_parametric_word,
        parse_production_string,
        parse_stochastic_production,
        create_parametric_lsystem_from_preset
    )
    HAS_PARAMETRIC = True
except ImportError:
    HAS_PARAMETRIC = False

__all__ = [
    'LSystem', 
    'parse_rules',
    'LSystemError',
    'PRESETS', 
    'PRESETS_3D', 
    'PARAMETRIC_PRESETS',
    'get_preset', 
    'list_presets',
    'get_parametric_preset',
    'list_parametric_presets',
    'list_presets_by_category',
    'get_preset_info',
    'GOLDEN_ANGLE',
    'LEONARDO_WIDTH_DECAY',
    'HONDA_BRANCHING_ANGLE'
]

if HAS_PARAMETRIC:
    __all__.extend([
        'ParametricLSystem',
        'ParametricLSystemError',
        'Module',
        'Production',
        'parse_parametric_word',
        'parse_production_string',
        'parse_stochastic_production',
        'create_parametric_lsystem_from_preset'
    ])
