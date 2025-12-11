"""
Plant Presets

Classic L-system plant definitions ready for use.
"""

PRESETS = {
    "fern": {
        "axiom": "X",
        "rules": {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        "angle": 25,
        "iterations": 6,
        "description": "Fractal fern (Barnsley-like)"
    },
    "tree": {
        "axiom": "F",
        "rules": {"F": "F[-F][+F]"},
        "angle": 25,
        "iterations": 5,
        "description": "Simple binary tree"
    },
    "bush": {
        "axiom": "F",
        "rules": {"F": "FF+[+F-F-F]-[-F+F+F]"},
        "angle": 22.5,
        "iterations": 4,
        "description": "Dense bush structure"
    },
    "seaweed": {
        "axiom": "F",
        "rules": {"F": "FF-[XY]+[XY]", "X": "+FY", "Y": "-FX"},
        "angle": 22.5,
        "iterations": 5,
        "description": "Swaying seaweed pattern"
    },
    "tree2": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 20,
        "iterations": 5,
        "description": "Alternate tree structure"
    },
    "weed": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": 25.7,
        "iterations": 4,
        "description": "Simple weed/grass"
    }
}


def get_preset(name: str) -> dict:
    """
    Get a preset by name.
    
    Args:
        name: Preset name (case-insensitive)
        
    Returns:
        Preset dictionary with axiom, rules, angle, iterations
        
    Raises:
        KeyError: If preset not found
    """
    name_lower = name.lower()
    if name_lower not in PRESETS:
        available = ', '.join(PRESETS.keys())
        raise KeyError(f"Unknown preset '{name}'. Available presets: {available}")
    return PRESETS[name_lower].copy()


def list_presets() -> list:
    """Return list of available preset names."""
    return list(PRESETS.keys())
