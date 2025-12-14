"""
Plant Presets

Classic L-system plant definitions ready for use.
Includes 2D and 3D preset collections.
"""

from typing import Dict, Any, List

# 2D Plant Presets
PRESETS: Dict[str, Dict[str, Any]] = {
    # === Original Presets ===
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
    },
    
    # === New Enhanced Presets ===
    "fern_barnsley": {
        "axiom": "X",
        "rules": {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        "angle": 25,
        "iterations": 6,
        "description": "Classic Barnsley fern"
    },
    "fern_maidenhair": {
        "axiom": "Y",
        "rules": {
            "Y": "F[-X][+X]FY",
            "X": "F[-X]+X"
        },
        "angle": 30,
        "iterations": 6,
        "description": "Delicate maidenhair fern pattern"
    },
    "tree_willow": {
        "axiom": "F",
        "rules": {"F": "FF-[-F+F+F]+[+F-F-F]"},
        "angle": 22.5,
        "iterations": 4,
        "description": "Weeping willow-like drooping branches"
    },
    "tree_oak": {
        "axiom": "X",
        "rules": {
            "X": "F[+X][-X]FX",
            "F": "FF"
        },
        "angle": 30,
        "iterations": 5,
        "description": "Sturdy oak tree branching"
    },
    "bush_dense": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F][F]"},
        "angle": 20,
        "iterations": 5,
        "description": "Very dense bush"
    },
    "grass": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": 25.7,
        "iterations": 4,
        "description": "Grass or wheat stalk"
    },
    "algae": {
        "axiom": "F",
        "rules": {"F": "F[+F][-F]F[-F][+F]F"},
        "angle": 20,
        "iterations": 4,
        "description": "Branching algae pattern"
    },
    "coral": {
        "axiom": "F",
        "rules": {"F": "FF+[+F-F-F]-[-F+F+F]"},
        "angle": 25,
        "iterations": 4,
        "description": "Coral-like branching"
    },
    "vine": {
        "axiom": "X",
        "rules": {
            "X": "F-[[X]+X]+F[+FX]-X",
            "F": "FF"
        },
        "angle": 22.5,
        "iterations": 5,
        "description": "Climbing vine pattern"
    },
    "flower_simple": {
        "axiom": "X",
        "rules": {
            "X": "F[+X]F[-X]+X",
            "F": "FF"
        },
        "angle": 25,
        "iterations": 5,
        "description": "Simple flowering plant"
    },
    "succulent": {
        "axiom": "X",
        "rules": {
            "X": "F[-X][+X]",
            "F": "FF"
        },
        "angle": 45,
        "iterations": 6,
        "description": "Succulent/cactus branching"
    },
    "kelp": {
        "axiom": "F",
        "rules": {
            "F": "FF[-F++F][+F--F]++F--F"
        },
        "angle": 15,
        "iterations": 4,
        "description": "Wavy kelp/seaweed"
    },
    "dragon_tree": {
        "axiom": "X",
        "rules": {
            "X": "F[+X][-X]F[+X]FX",
            "F": "FF"
        },
        "angle": 25.7,
        "iterations": 5,
        "description": "Dragon tree branching pattern"
    },
    "bonsai": {
        "axiom": "F",
        "rules": {"F": "FF[++F][-FF][+F][-F]"},
        "angle": 30,
        "iterations": 4,
        "description": "Stylized bonsai tree"
    },
    "feather": {
        "axiom": "X",
        "rules": {
            "X": "F[+X]F[-X]F[+X]",
            "F": "F"
        },
        "angle": 85,
        "iterations": 6,
        "description": "Feather or leaf vein pattern"
    },
    "pine": {
        "axiom": "F",
        "rules": {"F": "F[+F][-F]F[+F][-F]"},
        "angle": 35,
        "iterations": 4,
        "description": "Pine branch pattern"
    },
    "crystal": {
        "axiom": "F+F+F+F+F+F",
        "rules": {"F": "F+F-F-F+F"},
        "angle": 60,
        "iterations": 4,
        "description": "Crystal/snowflake pattern"
    },
    "sympodial": {
        "axiom": "X",
        "rules": {
            "X": "F[-X]F[+X]+X",
            "F": "FF"
        },
        "angle": 20,
        "iterations": 5,
        "description": "Sympodial branching (zigzag growth)"
    },
    "dichotomous": {
        "axiom": "X",
        "rules": {
            "X": "F[+X][-X]",
            "F": "FF"
        },
        "angle": 30,
        "iterations": 7,
        "description": "Equal dichotomous branching"
    },
    "ivy": {
        "axiom": "FX",
        "rules": {
            "X": "X[-FFF][+FFF]FX",
            "F": "FF"
        },
        "angle": 25,
        "iterations": 5,
        "description": "Ivy climbing pattern"
    }
}

# 3D Plant Presets (uses additional symbols: &, ^, /, \, |)
PRESETS_3D: Dict[str, Dict[str, Any]] = {
    "tree_3d_simple": {
        "axiom": "F",
        "rules": {"F": "F[+F][-F][&F][^F]"},  # Branch in 4 directions
        "angle": 25,
        "iterations": 4,
        "description": "Simple 3D branching tree"
    },
    "bush_3d": {
        "axiom": "A",
        "rules": {
            "A": "[&FL!A]////[&FL!A]//////[&FL!A]",
            "F": "S//F",
            "S": "F",
            "L": "[-F][+F]F"
        },
        "angle": 22.5,
        "iterations": 6,
        "description": "3D bush with spiral branching"
    },
    "tree_3d_realistic": {
        "axiom": "FA",
        "rules": {
            "A": "F[&+B][&-B][&B]FA",
            "B": "F[+B][-B]",
            "F": "FF"
        },
        "angle": 25,
        "iterations": 4,
        "tropism": (0, 1, 0),
        "tropism_strength": 0.15,
        "description": "Realistic 3D tree with gravitropism"
    },
    "spiral_plant_3d": {
        "axiom": "A",
        "rules": {
            "A": "F[+L]/A",  # / = roll by golden angle
            "L": "[&FF]"     # Longer branches that pitch outward
        },
        "angle": 35,
        "roll_angle": 137.5,  # Golden angle!
        "iterations": 8,
        "description": "Phyllotactic spiral plant"
    },
    "fern_3d": {
        "axiom": "X",
        "rules": {
            "X": "F[+X][-X]/X",
            "F": "FF"
        },
        "angle": 25,
        "roll_angle": 180,  # Alternate sides
        "iterations": 5,
        "description": "3D fern with alternating fronds"
    },
    "palm_3d": {
        "axiom": "FFFFFFA",
        "rules": {
            "A": "[+F[+F][-F]F]/////A"
        },
        "angle": 35,
        "roll_angle": 72,  # 5 fronds per whorl (360/5)
        "iterations": 6,
        "description": "Palm tree with radial fronds"
    },
    "conifer_3d": {
        "axiom": "T",
        "rules": {
            "T": "F[^^^L][&&&L]//T",
            "L": "[-F][+F]F"
        },
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 8,
        "description": "Conifer/pine tree shape"
    },
    "helix_3d": {
        "axiom": "A",
        "rules": {
            "A": "F/[+L]A",
            "L": "F"
        },
        "angle": 30,
        "roll_angle": 36,  # Creates 10-fold helix
        "iterations": 30,
        "description": "Helical climbing plant"
    },
    "umbrella_3d": {
        "axiom": "FFFA",
        "rules": {
            "A": "[+F][/+F][//+F][///+F][////+F]"
        },
        "angle": 60,
        "roll_angle": 72,
        "iterations": 3,
        "description": "Umbrella/parasol tree shape"
    },
    "shrub_3d": {
        "axiom": "X",
        "rules": {
            "X": "F[+X][-X][/X][\\X]",
            "F": "F"
        },
        "angle": 30,
        "roll_angle": 90,
        "iterations": 5,
        "description": "3D shrub with quad branching"
    },
    "monopodial_3d": {
        "axiom": "A",
        "rules": {
            "A": "F/[+L][-L]A",
            "L": "F[-F][+F]F"
        },
        "angle": 45,
        "roll_angle": 137.5,
        "iterations": 10,
        "description": "Monopodial tree (single main trunk)"
    },
    "bamboo_3d": {
        "axiom": "FA",
        "rules": {
            "A": "F[/+L][/-L]FA",
            "L": "FF"
        },
        "angle": 60,
        "roll_angle": 180,
        "iterations": 8,
        "description": "Bamboo-like segmented growth"
    }
}


def get_preset(name: str, include_3d: bool = True) -> dict:
    """
    Get a preset by name.
    
    Args:
        name: Preset name (case-insensitive)
        include_3d: Whether to search 3D presets too
        
    Returns:
        Preset dictionary with axiom, rules, angle, iterations
        
    Raises:
        KeyError: If preset not found
    """
    name_lower = name.lower()
    
    # Check 2D presets first
    if name_lower in PRESETS:
        return PRESETS[name_lower].copy()
    
    # Check 3D presets
    if include_3d and name_lower in PRESETS_3D:
        preset = PRESETS_3D[name_lower].copy()
        preset['is_3d'] = True
        return preset
    
    # Not found
    all_presets = list(PRESETS.keys())
    if include_3d:
        all_presets.extend(PRESETS_3D.keys())
    available = ', '.join(sorted(all_presets))
    raise KeyError(f"Unknown preset '{name}'. Available presets: {available}")


def list_presets(include_3d: bool = False) -> List[str]:
    """
    Return list of available preset names.
    
    Args:
        include_3d: Whether to include 3D presets
        
    Returns:
        List of preset names
    """
    presets = list(PRESETS.keys())
    if include_3d:
        presets.extend(PRESETS_3D.keys())
    return sorted(presets)


def list_presets_by_category() -> Dict[str, List[str]]:
    """
    Return presets organized by category.
    
    Returns:
        Dictionary mapping category names to lists of preset names
    """
    categories = {
        "Trees": ["tree", "tree2", "tree_oak", "tree_willow", "bonsai", 
                  "pine", "dragon_tree"],
        "Ferns": ["fern", "fern_barnsley", "fern_maidenhair", "feather"],
        "Bushes": ["bush", "bush_dense", "weed", "grass"],
        "Aquatic": ["seaweed", "kelp", "algae", "coral"],
        "Vines & Climbers": ["vine", "ivy"],
        "Flowers & Succulents": ["flower_simple", "succulent"],
        "Structural": ["sympodial", "dichotomous", "crystal"],
        "3D Trees": ["tree_3d_simple", "tree_3d_realistic", "conifer_3d",
                     "umbrella_3d", "monopodial_3d", "palm_3d"],
        "3D Plants": ["bush_3d", "spiral_plant_3d", "fern_3d", 
                      "helix_3d", "shrub_3d", "bamboo_3d"]
    }
    return categories


def get_preset_info(name: str) -> str:
    """
    Get formatted information about a preset.
    
    Args:
        name: Preset name
        
    Returns:
        Formatted string with preset details
    """
    preset = get_preset(name, include_3d=True)
    info_lines = [
        f"Preset: {name}",
        f"  Axiom: {preset['axiom']}",
        f"  Rules: {preset['rules']}",
        f"  Angle: {preset['angle']}°",
        f"  Iterations: {preset['iterations']}"
    ]
    
    if 'description' in preset:
        info_lines.append(f"  Description: {preset['description']}")
    
    if preset.get('is_3d'):
        info_lines.append("  Type: 3D")
        if 'roll_angle' in preset:
            info_lines.append(f"  Roll Angle: {preset['roll_angle']}°")
        if 'tropism' in preset:
            info_lines.append(f"  Tropism: {preset['tropism']}")
    
    return '\n'.join(info_lines)
