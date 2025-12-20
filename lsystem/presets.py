"""
L-System Plant Presets v2 - Complete Redesign

FIXES:
1. Removed all duplicates (oak/sympodial, honda/camera_orbit, etc.)
2. Palm - Now has 8-12 realistic fronds with pinnate structure
3. Sunflower - Dense Fibonacci spiral florets visible from above
4. Phyllotaxis - Bowl-shaped to show golden angle spiral properly
5. All trees have distinct silhouettes matching their species

Based on:
- "The Algorithmic Beauty of Plants" (Prusinkiewicz & Lindenmayer)
- Honda tree model research
- Fibonacci phyllotaxis patterns
- Real botanical growth patterns

Author: JP's L-System Generator Project
"""

from typing import Dict, Any, List

# =============================================================================
# 2D PRESETS
# =============================================================================

PRESETS_2D: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # ABOP Figure 1.24 - The Canonical Collection (Keep all - they're classics!)
    # =========================================================================
    "abop_1_24a": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": 25.7,
        "iterations": 5,
        "base_width": 1.5,
        "description": "ABOP 1.24a - Classic edge-rewriting bush"
    },
    "abop_1_24b": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F][F]"},
        "angle": 20.0,
        "iterations": 5,
        "base_width": 1.5,
        "description": "ABOP 1.24b - With vertical branch"
    },
    "abop_1_24c": {
        "axiom": "F",
        "rules": {"F": "FF-[-F+F+F]+[+F-F-F]"},
        "angle": 22.5,
        "iterations": 4,
        "base_width": 1.5,
        "description": "ABOP 1.24c - Beautiful bilateral bush"
    },
    "abop_1_24d": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 20.0,
        "iterations": 7,
        "base_width": 1.2,
        "description": "ABOP 1.24d - Asymmetric tree"
    },
    "abop_1_24e": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]FX", "F": "FF"},
        "angle": 25.7,
        "iterations": 7,
        "base_width": 1.2,
        "description": "ABOP 1.24e - Sympodial growth"
    },
    "abop_1_24f": {
        "axiom": "X",
        "rules": {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        "angle": 22.5,
        "iterations": 5,
        "base_width": 1.2,
        "description": "ABOP 1.24f - The elegant plant (ICONIC!)"
    },

    # =========================================================================
    # TREES - Distinct 2D Silhouettes
    # =========================================================================
    "tree_oak_spreading": {
        # Oak: WIDE spreading crown, branches go outward not up
        "axiom": "FX",
        "rules": {
            "X": "F[++X][+X][-X][--X]",  # 5-way split for spreading crown
            "F": "FF"
        },
        "angle": 35,  # Wide angles for horizontal spread
        "iterations": 5,
        "base_width": 1.8,
        "description": "Oak - wide spreading crown"
    },
    "tree_willow_weeping": {
        # Willow: Strong trunk then cascading droopy branches
        "axiom": "FFFFA",
        "rules": {
            "A": "[+B][-B]A",
            "B": "F[+F[+F]][-F[-F]]"  # Cascading droop pattern
        },
        "angle": 25,
        "iterations": 6,
        "base_width": 1.5,
        "description": "Willow - cascading branches"
    },
    "tree_poplar_columnar": {
        # Poplar: Narrow columnar shape, branches close to trunk
        "axiom": "FA",
        "rules": {
            "A": "F[+B][-B]FA",
            "B": "F[+F][-F]"
        },
        "angle": 12,  # Very narrow angles = columnar
        "iterations": 7,
        "base_width": 1.3,
        "description": "Poplar - tall columnar shape"
    },
    "tree_elm_vase": {
        # Elm: Vase-shaped, branches fan outward then up
        "axiom": "FFX",
        "rules": {
            "X": "[++FX][+FX][-FX][--FX]",
            "F": "F"
        },
        "angle": 20,
        "iterations": 6,
        "base_width": 1.4,
        "description": "Elm - vase-shaped crown"
    },

    # =========================================================================
    # FERNS - Realistic compound fronds
    # =========================================================================
    "fern_frond": {
        # Real fern: central rachis with alternating pinnae
        "axiom": "X",
        "rules": {
            "X": "F[+P]F[-P]X",
            "P": "F[+F][-F]F",  # Each pinna has sub-leaflets
            "F": "F"
        },
        "angle": 45,
        "iterations": 7,
        "base_width": 0.8,
        "description": "Fern - realistic frond with pinnae"
    },
    "fern_fractal": {
        # Classic fractal fern
        "axiom": "X",
        "rules": {
            "X": "F+[[X]-X]-F[-FX]+X",
            "F": "FF"
        },
        "angle": 25,
        "iterations": 6,
        "base_width": 1.0,
        "description": "Fern - fractal self-similar"
    },

    # =========================================================================
    # ARTISTIC - Abstract but beautiful
    # =========================================================================
    "dragon_curve": {
        "axiom": "FX",
        "rules": {"X": "X+YF+", "Y": "-FX-Y"},
        "angle": 90,
        "iterations": 12,
        "description": "Dragon curve - mathematical beauty"
    },
    "koch_snowflake": {
        "axiom": "F++F++F",
        "rules": {"F": "F-F++F-F"},
        "angle": 60,
        "iterations": 4,
        "description": "Koch snowflake"
    },
    "sierpinski": {
        "axiom": "F-G-G",
        "rules": {"F": "F-G+F+G-F", "G": "GG"},
        "angle": 120,
        "iterations": 6,
        "description": "Sierpinski triangle"
    },
}


# =============================================================================
# 3D PRESETS - All unique, no duplicates!
# =============================================================================

PRESETS_3D: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # ABOP 3D Figures - Research Validated
    # =========================================================================
    "abop_1_25": {
        # 3D bush with hexagonal polygon leaves
        "axiom": "A",
        "rules": {
            "A": "[&FL!A]/////'[&FL!A]///////'[&FL!A]",
            "F": "S/////F",
            "S": "FL",
            "L": "['''^^{-f+f+f-|-f+f+f}]"
        },
        "angle": 22.5,
        "roll_angle": 22.5,
        "iterations": 7,
        "base_width": 2.0,
        "width_decay": 0.707,
        "render_polygons": True,
        "description": "ABOP 1.25 - 3D bush with polygon leaves"
    },
    "abop_1_26": {
        # Flowering plant with polygon petals
        "axiom": "P",
        "rules": {
            "P": "I+[P+W]--//[--L]I[++L]-[PW]++PW",
            "I": "FS[//&&L][//^^L]FS",
            "S": "SFS",
            "L": "['{+f-ff-f+|+f-ff-f}]",
            "W": "[&&&K'/V////V////V////V////V]",
            "K": "FF",
            "V": "['^F][{&&&&-f+f|-f+f}]"
        },
        "angle": 18.0,
        "roll_angle": 18.0,
        "iterations": 5,
        "base_width": 2.0,
        "width_decay": 0.75,
        "render_polygons": True,
        "description": "ABOP 1.26 - Flowering plant with petals"
    },

    # =========================================================================
    # TREES - Each species has UNIQUE silhouette
    # =========================================================================
    
    # OAK - Wide spreading crown (NOT the umbrella/acacia pattern!)
    "tree_3d_oak": {
        "axiom": "FFFA",
        "rules": {
            # Crown starts with 4 main branches spreading outward
            "A": "[&&&B]/(90)[&&&B]/(90)[&&&B]/(90)[&&&B]",
            # Each branch splits into 3, creating dense crown
            "B": "FF[++C][+C][-C][--C]",
            "C": "F[+C][-C]"
        },
        "angle": 40,  # Wide angles for spreading
        "roll_angle": 90,
        "iterations": 5,
        "width_decay": 0.707,
        "length_decay": 0.7,
        "description": "Oak - wide spreading crown (NOT umbrella!)"
    },
    
    # PINE - Conical whorled structure
    "tree_3d_pine": {
        # Pine has whorled branches getting shorter toward top
        "axiom": "FWFWFWFWFWFWFWFWFWFWFWFW",
        "rules": {
            # 5 branches per whorl at 72° apart
            "W": "[/&&B][//&&B][///&&B][////&&B][/////&&B]",
            "B": "FF[+F][-F]"
        },
        "angle": 35,
        "roll_angle": 72,
        "iterations": 3,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "width_decay": 0.7,
        "length_decay": 0.85,
        "description": "Pine - conical with whorled branches"
    },
    
    # BIRCH - Graceful with upswept fine branches
    "tree_3d_birch": {
        "axiom": "FFXFFXFFXFFXFFXFFXFFXFFX",
        "rules": {
            "X": "[/&B][//&B][///&B]",
            "B": "FFF[+F[+F]][-F[-F]]"
        },
        "angle": 30,
        "roll_angle": 120,
        "iterations": 4,
        "tropism_strength": -0.05,  # Slight upward tendency
        "tropism_direction": [0, 1, 0],
        "width_decay": 0.65,
        "length_decay": 0.8,
        "description": "Birch - graceful upswept branches"
    },
    
    # MAPLE - Opposite decussate branching
    "tree_3d_maple": {
        "axiom": "FFFFA",
        "rules": {
            # Opposite pairs, each pair rotated 90° from previous
            "A": "[&+B][&-B]//[&+B][&-B]A",
            "B": "FF[+C][-C]",
            "C": "F[+C][-C]"
        },
        "angle": 35,
        "roll_angle": 90,
        "iterations": 5,
        "width_decay": 0.707,
        "length_decay": 0.75,
        "description": "Maple - opposite decussate branches"
    },
    
    # WILLOW - Weeping cascading branches
    "tree_3d_willow": {
        "axiom": "FFFFXFFXFFXFFXFFXFF",
        "rules": {
            "X": "[/&B][//&B][///&B][////&B]",
            # Branches droop then cascade
            "B": "FF[&F[&F[&F[&F]]]]"
        },
        "angle": 60,
        "roll_angle": 90,
        "iterations": 4,
        "tropism_strength": 0.2,
        "tropism_direction": [0, -1, 0],
        "width_decay": 0.75,
        "length_decay": 0.85,
        "description": "Willow - weeping cascading branches"
    },

    # CYPRESS - Narrow columnar
    "tree_3d_cypress": {
        "axiom": "FXFXFXFXFXFXFXFXFXFXFXFXFX",
        "rules": {
            "X": "[/&B][//&B][///&B][////&B]",
            "B": "F[+F][-F]"
        },
        "angle": 15,  # Narrow = columnar
        "roll_angle": 90,
        "iterations": 3,
        "width_decay": 0.8,
        "length_decay": 0.9,
        "description": "Cypress - narrow columnar shape"
    },

    # =========================================================================
    # PALM - COMPLETELY REDESIGNED!
    # Now has 8-12 large fronds with pinnate (feather-like) structure
    # =========================================================================
    "palm_3d": {
        # Tall trunk then crown of 10 large pinnate fronds
        "axiom": "FFFFFFFFFF[P][/P][//P][///P][////P][/////P][//////P][///////P][////////P][/////////P]",
        "rules": {
            # Each frond (P) is pinnate: central rachis with many pinnae
            "P": "&&&RRRRRRRRRR",  # Long arching rachis
            "R": "F[+L][++L][-L][--L]/",  # Pinnae on both sides, spiral slightly
            "L": "FF"  # Each pinna is a simple leaf segment
        },
        "angle": 25,
        "roll_angle": 36,  # 360/10 = 36° between fronds
        "iterations": 2,
        "tropism_strength": 0.15,
        "tropism_direction": [0, -1, 0],  # Fronds droop naturally
        "width_decay": 0.6,
        "length_decay": 0.85,
        "description": "Palm - 10 pinnate fronds with drooping tips"
    },

    # =========================================================================
    # PHYLLOTAXIS - REDESIGNED for visual impact!
    # Bowl/dome shape so golden angle spiral is visible
    # =========================================================================
    "phyllotaxis_bowl": {
        # Spiral arrangement where each leaf tilts outward to form bowl
        "axiom": "A",
        "rules": {
            "A": "F/[&&L]A",  # Each step: grow, roll by golden angle, add outward leaf
            "L": "F[+F][-F][++F][--F]"  # Fan of leaflets
        },
        "angle": 45,
        "roll_angle": 137.5,  # THE golden angle!
        "iterations": 40,
        "width_decay": 0.98,
        "length_decay": 0.98,
        "camera_angle": 75,  # View from above to see spiral!
        "description": "Phyllotaxis - golden angle bowl (view from above!)"
    },

    # =========================================================================
    # SUNFLOWER - Working shape with color support
    # Uses ' to set color_index for yellow florets
    # =========================================================================
    "sunflower_head": {
        # Dense spiral of florets - original working shape
        "axiom": "SLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSLSL",
        "rules": {
            "L": "[/&'F]",  # ' sets color_index=1 (yellow)
            "S": ""
        },
        "angle": 30,
        "roll_angle": 137.5077,
        "iterations": 1,
        "width_decay": 0.98,
        "length_decay": 0.99,
        "description": "Sunflower head - dense golden spiral"
    },

    # =========================================================================
    # SUCCULENT - Rosette with thick leaves
    # =========================================================================
    "succulent_rosette": {
        "axiom": "A",
        "rules": {
            "A": "[&&L]/A",
            "L": "FFF"  # Thick fleshy leaves
        },
        "angle": 60,
        "roll_angle": 137.5,
        "iterations": 21,  # Fibonacci number
        "width_decay": 0.95,
        "length_decay": 0.92,
        "description": "Succulent - golden angle rosette"
    },

    # =========================================================================
    # FERNS 3D - Realistic compound fronds
    # =========================================================================
    "fern_3d_frond": {
        # Single fern frond with alternating pinnae
        "axiom": "FFFFFFFFFFFFFA",
        "rules": {
            "A": "[/+P][/-P]FA",
            "P": "FF[++F][+F][-F][--F]"  # Each pinna has pinnules
        },
        "angle": 40,
        "roll_angle": 180,  # Alternate sides
        "iterations": 3,
        "width_decay": 0.6,
        "length_decay": 0.75,
        "description": "Fern - realistic pinnate frond"
    },
    "fern_3d_spiral": {
        # Fern with golden angle phyllotaxis
        "axiom": "FFFFFFFFFFA",
        "rules": {
            "A": "[/&P]A",
            "P": "F[++F][+F][-F][--F][+++F][---F]"
        },
        "angle": 50,
        "roll_angle": 137.5,
        "iterations": 4,
        "width_decay": 0.65,
        "length_decay": 0.8,
        "description": "Fern - golden angle spiral arrangement"
    },

    # =========================================================================
    # BAMBOO - Segmented culms with node branches
    # =========================================================================
    "bamboo_3d": {
        # Segmented stem (culm) with branches at nodes
        "axiom": "NCNCNCNCNCNCNCNCNCNCNCNC",
        "rules": {
            "N": "[/+B][/-B][/++B][/--B]",  # 4 branches at each node
            "C": "FF",  # Culm segment
            "B": "FF[+F][-F]"
        },
        "angle": 45,
        "roll_angle": 45,
        "iterations": 2,
        "width_decay": 0.98,  # Bamboo stays nearly same width
        "length_decay": 0.95,
        "description": "Bamboo - segmented with node branches"
    },

    # =========================================================================
    # ARTISTIC / ABSTRACT
    # =========================================================================
    "spiral_vine": {
        "axiom": "A",
        "rules": {
            "A": "F/[+L][-L]A",
            "L": "[&F]"
        },
        "angle": 30,
        "roll_angle": 30,
        "iterations": 30,
        "width_decay": 0.98,
        "length_decay": 0.98,
        "description": "Spiral vine - helical climbing"
    },
    "coral_branch": {
        "axiom": "FFA",
        "rules": {
            "A": "F[&/+A][&/-A][&//+A][&//-A]"
        },
        "angle": 30,
        "roll_angle": 60,
        "iterations": 6,
        "width_decay": 0.75,
        "length_decay": 0.8,
        "description": "Coral - multi-way branching"
    },
    "crystal_growth": {
        "axiom": "FA",
        "rules": {
            "A": "[+A][-A][&A][^A]F"
        },
        "angle": 90,
        "roll_angle": 90,
        "iterations": 5,
        "width_decay": 0.85,
        "length_decay": 0.85,
        "description": "Crystal - orthogonal growth"
    },

    # =========================================================================
    # HONDA TREE MODEL - Research validated
    # =========================================================================
    "honda_tree": {
        "axiom": "FFFFA",
        "rules": {
            "A": "F[&B]//[&B]//[&B]A",
            "B": "FF[+$C][-$C]",
            "C": "F[+$C][-$C]"
        },
        "angle": 35,
        "roll_angle": 120,
        "iterations": 7,
        "width_decay": 0.707,  # Leonardo's rule
        "length_decay": 0.8,
        "tropism_strength": 0.1,
        "description": "Honda tree - with Leonardo's rule"
    },
}


# =============================================================================
# COMBINED PRESETS DICTIONARY
# =============================================================================

PRESETS = PRESETS_2D  # PRESETS is just 2D presets (matching original structure)


# =============================================================================
# HELPER FUNCTIONS - Must match main.py's expected signatures
# =============================================================================

def get_preset(name: str, include_3d: bool = True) -> dict:
    """
    Get a preset by name.
    
    Args:
        name: Preset name (case-insensitive)
        include_3d: Whether to search 3D presets too
        
    Returns:
        Preset dictionary with axiom, rules, angle, iterations,
        and optional biological parameters
        
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


def is_3d_preset(name: str) -> bool:
    """Check if a preset is 3D."""
    return name.lower() in PRESETS_3D


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


# =============================================================================
# PRESET CATEGORIES for batch generator
# =============================================================================

PRESET_CATEGORIES = {
    "showcase": [
        "abop_1_24c",       # 2D - Beautiful bilateral
        "abop_1_24f",       # 2D - Elegant plant
        "abop_1_25",        # 3D - Bush with polygon leaves
        "abop_1_26",        # 3D - Flowering plant
        "tree_3d_oak",      # 3D - Spreading oak
        "palm_3d",          # 3D - Realistic palm
        "sunflower_head",   # 3D - Fibonacci spiral
        "phyllotaxis_bowl", # 3D - Golden angle visible
    ],
    "abop_figures": [
        "abop_1_24a", "abop_1_24b", "abop_1_24c",
        "abop_1_24d", "abop_1_24e", "abop_1_24f",
        "abop_1_25", "abop_1_26",
    ],
    "trees_2d": [
        "tree_oak_spreading", "tree_willow_weeping",
        "tree_poplar_columnar", "tree_elm_vase",
    ],
    "trees_3d": [
        "tree_3d_oak", "tree_3d_pine", "tree_3d_birch",
        "tree_3d_maple", "tree_3d_willow", "tree_3d_cypress",
        "honda_tree",
    ],
    "tropical": [
        "palm_3d", "bamboo_3d",
    ],
    "phyllotaxis": [
        "phyllotaxis_bowl", "sunflower_head", "succulent_rosette",
    ],
    "ferns": [
        "fern_frond", "fern_fractal",  # 2D
        "fern_3d_frond", "fern_3d_spiral",  # 3D
    ],
    "artistic": [
        "dragon_curve", "koch_snowflake", "sierpinski",  # 2D
        "spiral_vine", "coral_branch", "crystal_growth",  # 3D
    ],
}


# =============================================================================
# FUNCTIONS REQUIRED BY main.py
# =============================================================================

def list_presets_by_category() -> Dict[str, List[str]]:
    """
    Return presets organized by category.
    
    Returns:
        Dictionary mapping category names to lists of preset names
    """
    return {
        # 2D Categories
        "2D ABOP Classics": ["abop_1_24a", "abop_1_24b", "abop_1_24c",
                            "abop_1_24d", "abop_1_24e", "abop_1_24f"],
        "2D Trees": ["tree_oak_spreading", "tree_willow_weeping", 
                     "tree_poplar_columnar", "tree_elm_vase"],
        "2D Ferns": ["fern_frond", "fern_fractal"],
        "2D Artistic": ["dragon_curve", "koch_snowflake", "sierpinski"],
        
        # 3D Categories
        "3D ABOP Figures": ["abop_1_25", "abop_1_26"],
        "3D Trees": ["tree_3d_oak", "tree_3d_pine", "tree_3d_birch",
                     "tree_3d_maple", "tree_3d_willow", "tree_3d_cypress",
                     "honda_tree"],
        "3D Tropical": ["palm_3d", "bamboo_3d"],
        "3D Phyllotaxis": ["phyllotaxis_bowl", "sunflower_head", "succulent_rosette"],
        "3D Ferns": ["fern_3d_frond", "fern_3d_spiral"],
        "3D Artistic": ["spiral_vine", "coral_branch", "crystal_growth"],
    }


# =============================================================================
# PARAMETRIC PRESETS - For advanced L-system features
# =============================================================================

PARAMETRIC_PRESETS: Dict[str, Dict[str, Any]] = {
    # Growing trees with continuous segment elongation
    "growing_tree_param": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) : l < 5 -> !(w)F(l)[+A(l*R1,w*WR)][-A(l*R1,w*WR)]",
            "A(l,w) : l >= 5 -> !(w)F(l)",
            "F(l) -> F(l*1.15)",
        ],
        "constants": {"R1": 0.9, "WR": 0.707},
        "angle": 35,
        "iterations": 12,
        "description": "Tree with continuous growth and Leonardo's rule"
    },
    
    "parametric_bush": {
        "type": "parametric",
        "axiom": "A(1,5)",
        "productions": [
            "A(l,w) : l > 0 -> !(w)F(l)[+A(l*0.7,w*0.7)][-A(l*0.7,w*0.7)][A(l*0.8,w*0.8)]",
        ],
        "constants": {},
        "angle": 25.7,
        "iterations": 6,
        "description": "Parametric bush with variable segment lengths"
    },
    
    # Stochastic plants
    "stochastic_bush_abop": {
        "type": "parametric",
        "axiom": "F",
        "productions": [
            {"rule": "F -> F[+F]F[-F]F", "probability": 0.33},
            {"rule": "F -> F[+F]F", "probability": 0.33},
            {"rule": "F -> F[-F]F", "probability": 0.34},
        ],
        "angle": 25.7,
        "iterations": 5,
        "description": "Stochastic branching - ABOP Figure 1.27"
    },
    
    "stochastic_tree": {
        "type": "parametric",
        "axiom": "F",
        "productions": [
            {"rule": "F -> F[+F][-F]F", "probability": 0.4},
            {"rule": "F -> F[+F]F", "probability": 0.3},
            {"rule": "F -> F[-F]F", "probability": 0.3},
        ],
        "angle": 30,
        "iterations": 6,
        "description": "Stochastic tree with natural variation"
    },
    
    # Developmental leaves using polygon notation
    "developmental_leaf": {
        "type": "parametric",
        "axiom": "[A(0)][B(0)]",
        "productions": [
            "A(n) : n < 6 -> F{.+F.-F.}A(n+1)",
            "B(n) : n < 6 -> F{.-F.+F.}B(n+1)",
            "A(n) : n >= 6 -> F",
            "B(n) : n >= 6 -> F",
        ],
        "angle": 30,
        "iterations": 6,
        "description": "Cordate leaf with polygon filling"
    },
    
    "simple_polygon_leaf": {
        "type": "parametric", 
        "axiom": "A",
        "productions": [
            "A -> {.F.+F.+F.}",
        ],
        "angle": 120,
        "iterations": 1,
        "description": "Simple triangular polygon test"
    },
}


def get_parametric_preset(name: str):
    """
    Get a parametric preset by name.
    
    Args:
        name: Preset name (case-insensitive)
        
    Returns:
        Preset dictionary or None if not found
    """
    name_lower = name.lower()
    if name_lower in PARAMETRIC_PRESETS:
        preset = PARAMETRIC_PRESETS[name_lower].copy()
        preset['is_parametric'] = True
        return preset
    return None


def list_parametric_presets():
    """Return list of available parametric preset names."""
    return sorted(PARAMETRIC_PRESETS.keys())