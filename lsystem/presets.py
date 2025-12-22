"""
L-System Plant Presets - BEST OF THE BEST

Hand-picked, research-improved presets for beautiful plant renders.
All fixes from ABOP research applied.

Contains only ~25 highest-quality presets:
- 2D Classics (ABOP 1.24 series)
- 3D Trees with leaves
- Parametric trees (monopodial, sympodial, ternary)
- Fractals (dragon, hilbert)
- Ferns

All presets are production-ready with proper 3D operators and leaves where needed.
"""

from typing import Dict, Any

# =============================================================================
# 2D PRESETS - ABOP Classics
# =============================================================================

PRESETS_2D: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # ABOP Figure 1.24 - The Gold Standard
    # =========================================================================
    "abop_1_24a": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": 25.7,
        "iterations": 6,
        "base_width": 1.5,
        "description": "ABOP 1.24a - Classic bush"
    },
    
    "abop_1_24b": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F][F]"},
        "angle": 20.0,
        "iterations": 6,
        "base_width": 1.5,
        "description": "ABOP 1.24b - Vertical branch"
    },
    
    "abop_1_24c": {
        "axiom": "F",
        "rules": {"F": "FF-[-F+F+F]+[+F-F-F]"},
        "angle": 22.5,
        "iterations": 5,
        "base_width": 1.5,
        "description": "ABOP 1.24c - Bilateral symmetry"
    },
    
    "abop_1_24d": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 20.0,
        "iterations": 8,
        "base_width": 1.2,
        "description": "ABOP 1.24d - Asymmetric"
    },
    
    "abop_1_24e": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]FX", "F": "FF"},
        "angle": 25.7,
        "iterations": 8,
        "base_width": 1.2,
        "description": "ABOP 1.24e - Sympodial growth"
    },
    
    "abop_1_24f": {
        "axiom": "X",
        "rules": {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        "angle": 22.5,
        "iterations": 6,
        "base_width": 1.2,
        "description": "ABOP 1.24f - ICONIC elegant plant ⭐"
    },
    
    # =========================================================================
    # 2D Trees
    # =========================================================================
    "tree_elm_vase": {
        "axiom": "FFX",
        "rules": {
            "X": "[++FX][+FX][-FX][--FX]",
            "F": "FF"
        },
        "angle": 20,
        "iterations": 5,
        "base_width": 1.4,
        "description": "Elm - vase-shaped crown"
    },
    
    # =========================================================================
    # 2D Ferns
    # =========================================================================
    "fern_fractal": {
        "axiom": "X",
        "rules": {
            "X": "F+[[X]-X]-F[-FX]+X",
            "F": "FF"
        },
        "angle": 25,
        "iterations": 7,
        "base_width": 1.0,
        "description": "Fractal fern pattern"
    },
    
    # =========================================================================
    # 2D Fractals
    # =========================================================================
    "dragon_curve": {
        "axiom": "FX",
        "rules": {"X": "X+YF+", "Y": "-FX-Y"},
        "angle": 90,
        "iterations": 13,
        "base_width": 1.0,
        "description": "Dragon curve fractal"
    },
    
    "hilbert_curve": {
        "axiom": "A",
        "rules": {
            "A": "-BF+AFA+FB-",
            "B": "+AF-BFB-FA+"
        },
        "angle": 90,
        "iterations": 6,
        "description": "Hilbert space-filling curve ⭐"
    },
    
    "koch_snowflake": {
        "axiom": "F++F++F",
        "rules": {"F": "F-F++F-F"},
        "angle": 60,
        "iterations": 5,
        "base_width": 1.0,
        "description": "Koch snowflake"
    },
    
    "quadratic_snowflake": {
        "axiom": "-F",
        "rules": {"F": "F+F-F-F+F"},
        "angle": 90,
        "iterations": 5,
        "description": "Quadratic snowflake"
    },
}

# =============================================================================
# 3D PRESETS - Trees with Leaves
# =============================================================================

PRESETS_3D: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # ABOP 3D - THE BEST!
    # =========================================================================
    "abop_1_25": {
        "axiom": "A",
        "rules": {
            "A": "[&FLA]/////'[&FLA]/////'[&FLA]",
            "F": "S/////F",
            "S": "FL",
            "L": "['''^^{-f+f+f-|-f+f+f}]"
        },
        "angle": 22.5,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "width_decay": 0.9,
        "description": "⭐⭐ ABOP 1.25 - Bush with hexagonal leaves - THE BEST!"
    },
    
    "abop_1_26": {
        "axiom": "A",
        "rules": {
            "A": "[&FPLA]/////'[&FPLA]/////'[&FPL A]",
            "P": "F[++L][--L]",
            "L": "[{-f+f-f-f}]",
            "F": "FF"
        },
        "angle": 18,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "description": "ABOP 1.26 - Flowering plant with petals"
    },
    
    # =========================================================================
    # 3D Trees - Fixed with Roll + Leaves
    # =========================================================================
    "tree_3d_simple": {
        "axiom": "!(1)F(200)/(45)A",
        "rules": {
            "A": "!(1.732)F(50)[&(22)$FL]/(120)[&(22)$FL]/(120)[&(22)$FL]/(45)A",
            "L": "['''&&&{-f+f+f-f+f+f}]",
            "F": "FF"
        },
        "angle": 22.5,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "description": "Simple whorled tree with leaves - FIXED 3D"
    },
    
    "honda_tree": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.707)F(50)[&(40)BL][/(137.5)&(40)BL][/(274)&(40)BL]/(137.5)A",
            "B": "!(0.707)F(40)[+(25)CL][-(25)CL]",
            "C": "!(0.707)F(30)L",
            "L": "['''&&&{-f+f+f-f+f+f}]",
            "F": "FF"
        },
        "angle": 30,
        "iterations": 11,
        "is_3d": True,
        "render_polygons": True,
        "description": "Honda tree with terminal leaves - FIXED 3D"
    },
    
    "tree_3d_birch": {
        "axiom": "!(1)F(300)A",
        "rules": {
            "A": "T(0.05)!(0.9)F(50)[T(0.20)&(35)$BL][T(0.20)^(25)$CL]/(137.5)A",
            "B": "T(0.25)!(0.8)F(40)[&(30)$BL][^(20)$CL]/(137.5)B",
            "C": "T(0.25)!(0.8)F(40)[&(25)$CL][^(25)$BL]/(137.5)C",
            "L": "['''&&&{-f+f}]",
            "F": "FF"
        },
        "angle": 30,
        "iterations": 5,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.18,
        "tropism_direction": [0, -1, 0],
        "description": "Birch with gradient tropism - graceful droop"
    },
    
    "tree_3d_maple": {
        "axiom": "!(1)F(200)X",
        "rules": {
            "X": "!(0.9)F(50)[&(30)BL]/(180)[&(30)BL]/(137.5)FX",
            "B": "!(0.8)F(40)[+(20)CL][-(20)CL]",
            "C": "!(0.7)F(30)L",
            "L": "['''&&&{-f+f+f}]",
            "F": "FF"
        },
        "angle": 30,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.05,
        "tropism_direction": [0, -1, 0],
        "description": "Maple with decussate branches and leaves"
    },
    
    # =========================================================================
    # Gravity Series - WITH LEAVES
    # =========================================================================
    "tree_gravity_none": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(1.732)F(50)[&(30)$BL][/(120)&(30)$BL][/(240)&(30)$BL]/(45)A",
            "B": "!(1.0)F(40)[+(25)$BL][-(25)$BL]B",
            "L": "['''&&&{-f+f+f-|-f+f+f}]",
            "F": "FF"
        },
        "angle": 30,
        "iterations": 11,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.0,
        "description": "Symmetric tree - NO gravity"
    },
    
    "tree_gravity_moderate": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(1.732)F(50)[&(30)$BL][/(120)&(30)$BL][/(240)&(30)$BL]/(45)A",
            "B": "!(1.0)F(40)[+(25)$BL][-(25)$BL]B",
            "L": "['''&&&{-f+f+f-|-f+f+f}]",
            "F": "FF"
        },
        "angle": 30,
        "iterations": 11,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "description": "Tree with MODERATE gravity droop"
    },
    
    "tree_gravity_strong": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(1.732)F(50)[&(30)$BL][/(120)&(30)$BL][/(240)&(30)$BL]/(45)A",
            "B": "!(1.0)F(40)[+(25)$BL][-(25)$BL]B",
            "L": "['''&&&{-f+f+f-|-f+f+f}]",
            "F": "FF"
        },
        "angle": 30,
        "iterations": 11,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.28,
        "tropism_direction": [0, -1, 0],
        "description": "⭐ Weeping tree - STRONG gravity"
    },
    
    "bush_3d_with_leaves": {
        "axiom": "A",
        "rules": {
            "A": "[&FLA]/////'[&FLA]/////'[&FLA]",
            "F": "S/////F",
            "S": "FL",
            "L": "['''^^{-f+f+f-|-f+f+f}]"
        },
        "angle": 22.5,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "width_decay": 0.9,
        "description": "3D bush with polygon leaves"
    },
    
    "tree_with_leaves_berries": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.9)F(50)[&(35)BL]/(137.5)[&(35)BL]/(137.5)A",
            "B": "!(0.8)F(30)[+(20)CL][-(20)CL]",
            "C": "!(0.7)F(20)L",
            "L": "['''&&&{-f+f}]",
            "F": "FF"
        },
        "angle": 25,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": True,
        "description": "Tree with SMALL leaves - fixed size"
    },
    
    # =========================================================================
    # Spirals & Artistic
    # =========================================================================
    "coral_branch": {
        "axiom": "F",
        "rules": {"F": "F[&+F][^/F][&-F]"},
        "angle": 45,
        "iterations": 6,
        "is_3d": True,
        "description": "Coral-like branching with combined operators"
    },
    
    "crystal_growth": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.8)F(50)[&(28)$B][^(28)$C][+(25)$B][-(25)$C]/(137.5)A",
            "B": "!(0.7)F(40)[&(25)$B][+(20)$B]/(137.5)B",
            "C": "!(0.7)F(40)[^(25)$C][-(20)$C]/(137.5)C",
            "F": "FF"
        },
        "angle": 28,
        "iterations": 6,
        "is_3d": True,
        "tropism_strength": 0.18,
        "tropism_direction": [0, -1, 0],
        "description": "Crystal-organic hybrid tree with tropism"
    },
    
    # =========================================================================
    # Phyllotaxis
    # =========================================================================
    "sunflower_head": {
        "type": "parametric",
        "axiom": "N(1)",
        "productions": [
            "N(i) : i <= 200 -> [/(i*137.5)&(90-atan(sqrt(i)/2)*180/3.14159)'F(sqrt(i)*0.1,0.8)]N(i+1)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 137.5,
        "iterations": 1,
        "is_3d": True,
        "description": "⭐⭐ Sunflower - golden angle spiral"
    },
    
    "succulent_rosette": {
        "type": "parametric",
        "axiom": "N(1)",
        "productions": [
            "N(i) : i <= 60 -> [/(i*137.5)&(75)'{-f+f+f-|-f+f+f}]N(i+1)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 137.5,
        "iterations": 1,
        "is_3d": True,
        "render_polygons": True,
        "description": "Succulent rosette with polygon leaves"
    },
}

# =============================================================================
# PARAMETRIC PRESETS
# =============================================================================

PARAMETRIC_PRESETS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # Parametric Trees - FIXED 3D
    # =========================================================================
    "monopodial_tree": {
        "type": "parametric",
        "axiom": "!(1)F(200)/(45)A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(45)B(l*0.6,w*0.707)]/(137.5)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$C(l*0.6,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(45)$B(l*0.6,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 45,
        "iterations": 11,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "description": "⭐ ABOP Fig 2.6 - Monopodial (FIXED 3D with roll)"
    },
    
    "sympodial_tree": {
        "type": "parametric",
        "axiom": "!(1)F(200)A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(10)$B(l*0.9,w*0.707)]/(180)[&(60)$B(l*0.7,w*0.707)]",
            "B(l,w) -> !(w)F(l)[+(10)$B(l*0.9,w*0.707)][-(60)$B(l*0.7,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 35,
        "iterations": 10,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "description": "⭐ ABOP Fig 2.7 - Sympodial (FIXED z-growth)"
    },
    
    "ternary_tree": {
        "type": "parametric",
        "axiom": "!(1)F(200)/(45)A",
        "productions": [
            "A -> !(1.732)F(50)[&(19)F(50)B]/(94.74)[&(19)F(50)B]/(132.63)[&(19)F(50)B]",
            "B -> !(1.732)F(50)[&(19)F(50)B]/(94.74)[&(19)F(50)B]/(132.63)[&(19)F(50)B]",
            "F(l) -> F(l*1.109)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {
            "b": 94.74,
            "c": 19,
            "d": 1.109,
            "h": 1.732
        },
        "angle": 20,
        "iterations": 9,
        "tropism_strength": 0.15,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "description": "⭐ ABOP Fig 2.8 - Ternary (FIXED 3D whorls)"
    },
    
    # =========================================================================
    # Stochastic
    # =========================================================================
    "stochastic_plant": {
        "type": "parametric",
        "axiom": "F",
        "productions": [
            {"rule": "F -> F[-F]F[+F]F", "probability": 0.33},
            {"rule": "F -> F[-F]F", "probability": 0.33},
            {"rule": "F -> F[+F]F", "probability": 0.34}
        ],
        "rules": {"info": "Stochastic - see 'productions'"},
        "angle": 28,
        "iterations": 6,
        "description": "ABOP p.28 - Stochastic L-system with variation"
    },
    
    # =========================================================================
    # Ferns - FIXED Alternating Branching
    # =========================================================================
    "fern_simple": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(i) : i > 0 -> A(i-1)",
            "A(i) : i == 0 -> F(1)[+A(2)]F(1)B(0)",
            "B(i) : i > 0 -> B(i-1)",
            "B(i) : i == 0 -> F(1)[-B(2)]F(1)A(0)",
            "F(a) -> F(a*1.23)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"b": 2, "c": 1.23},
        "angle": 45,
        "iterations": 12,
        "description": "Simple pinnate fern - FIXED alternating"
    },
    
    "fern_delayed": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(i) : i > 0 -> A(i-1)",
            "A(i) : i == 0 -> F(1)[+A(4)]F(1)B(0)",
            "B(i) : i > 0 -> B(i-1)",
            "B(i) : i == 0 -> F(1)[-B(4)]F(1)A(0)",
            "F(a) -> F(a*1.20)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"b": 4, "c": 1.20},
        "angle": 45,
        "iterations": 18,
        "description": "⭐ Fern with apical delay - FIXED"
    },
    
    "fern_complex": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(i) : i > 0 -> A(i-1)",
            "A(i) : i == 0 -> F(1)[+A(6)]F(1)B(0)",
            "B(i) : i > 0 -> B(i-1)",
            "B(i) : i == 0 -> F(1)[-B(6)]F(1)A(0)",
            "F(a) -> F(a*1.18)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"b": 6, "c": 1.18},
        "angle": 45,
        "iterations": 25,
        "description": "⭐ Complex fern - high apical delay - FIXED"
    },
}

# =============================================================================
# Helper Functions
# =============================================================================

def get_preset(name: str, include_3d=True):
    """Get a preset by name from any category.
    
    Args:
        name: Preset name
        include_3d: If True, search 3D and parametric. If False, only 2D.
    """
    name_lower = name.lower()
    
    # Check 2D
    for key in PRESETS_2D:
        if key.lower() == name_lower:
            return PRESETS_2D[key]
    
    if not include_3d:
        return None
    
    # Check 3D
    for key in PRESETS_3D:
        if key.lower() == name_lower:
            return PRESETS_3D[key]
    
    # Check parametric
    for key in PARAMETRIC_PRESETS:
        if key.lower() == name_lower:
            preset = PARAMETRIC_PRESETS[key].copy()
            preset['is_parametric'] = True
            # Add 'rules' key for display compatibility (main.py expects it)
            if 'productions' in preset and 'rules' not in preset:
                # Convert productions to simplified rules format for display
                preset['rules'] = {'parametric': str(preset['productions'])}
            return preset
    
    return None


def list_presets(include_3d=True):
    """Return list of preset names.
    
    Args:
        include_3d: If True, include 3D and parametric presets. If False, only 2D.
    """
    all_presets = []
    all_presets.extend(PRESETS_2D.keys())
    
    if include_3d:
        all_presets.extend(PRESETS_3D.keys())
        all_presets.extend(PARAMETRIC_PRESETS.keys())
    
    return sorted(all_presets)


def list_parametric_presets():
    """Return list of parametric preset names."""
    return sorted(PARAMETRIC_PRESETS.keys())


def get_parametric_preset(name: str):
    """Get a parametric preset by name."""
    return get_preset(name)


def list_presets_by_category():
    """Return presets organized by category."""
    categories = {}
    
    for name, preset in {**PRESETS_2D, **PRESETS_3D, **PARAMETRIC_PRESETS}.items():
        category = preset.get('category', 'other')
        if category not in categories:
            categories[category] = []
        categories[category].append(name)
    
    return {k: sorted(v) for k, v in sorted(categories.items())}


# Compatibility - for code that expects PRESETS dict
PRESETS = {**PRESETS_2D, **PRESETS_3D}