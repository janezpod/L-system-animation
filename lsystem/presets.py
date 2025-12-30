"""
L-System Plant Presets - IMPROVED VERSION

Research-based improvements from ABOP and Honda (1971) model:
- Removed excessive initial trunks (F(200) -> proportional growth)
- Added polygon leaves to all parametric trees
- Fixed abop_1_26 typo and added visible flowers
- Proper Leonardo's rule width decay (0.707 for binary, 1.732 for ternary)
- Moderate tropism values (0.04-0.12 range)

Contains ~35 production-ready presets:
- 2D Classics (ABOP 1.24 series, fractals, ferns)
- 3D Trees with leaves (IMPROVED)
- Parametric trees with leaves (IMPROVED)
"""

from typing import Dict, Any

# =============================================================================
# 2D PRESETS - ABOP Classics (unchanged - these work well)
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
        "description": "ABOP 1.24f - ICONIC elegant plant [BEST]"
    },
    
    # =========================================================================
    # 2D Trees - FIXED
    # =========================================================================
    "tree_elm_vase": {
        "axiom": "X",  # FIXED: was "FFX" - removed excessive initial trunk
        "rules": {
            "X": "F[++FX][+FX][-FX][--FX]",
            "F": "FF"
        },
        "angle": 20,
        "iterations": 5,
        "base_width": 1.4,
        "description": "Elm - vase-shaped crown (FIXED)"
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
        "description": "Hilbert space-filling curve [BEST]"
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
# 3D PRESETS - IMPROVED with leaves and proportional growth
# =============================================================================

PRESETS_3D: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # ABOP 3D - THE BEST! (unchanged - already works well)
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
        "description": "ABOP 1.25 - Bush with hexagonal leaves [BEST]"
    },
    
    # =========================================================================
    # ABOP 1.26 - FIXED: typo removed, larger flowers, visible petals
    # =========================================================================
    "abop_1_26": {
        "axiom": "A",
        "rules": {
            "A": "[&FPLA]/////'[&FPLA]/////'[&FPLA]",  # FIXED: removed space typo
            "P": "['''&{--f++f++f--|--f++f++f}]",  # Larger flower polygon
            "L": "[''''^^{-f+f+f-|-f+f+f}]",  # Hexagonal leaf
            "F": "S/////F",
            "S": "FL"
        },
        "angle": 22.5,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "width_decay": 0.85,
        "description": "ABOP 1.26 - Flowering plant (FIXED with visible petals) [BEST]"
    },
    
    # =========================================================================
    # Honda Tree - IMPROVED: No F(200) trunk, with leaves
    # =========================================================================
    "honda_tree": {
        "axiom": "A",  # FIXED: was "!(1)F(200)A"
        "rules": {
            "A": "!(0.707)F[&(50)$BL][/(137.5)&(50)$BL][/(275)&(50)$BL]/(137.5)FA",
            "B": "!(0.707)F[+(35)$CL][-(35)$CL]C",
            "C": "!(0.707)FL",
            "L": "['''^^{-f+f+f-|-f+f+f}]",
            "F": "F"
        },
        "angle": 35,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.06,
        "tropism_direction": [0, -1, 0],
        "description": "Honda tree (IMPROVED: no long trunk, with leaves)"
    },
    
    # =========================================================================
    # Simple 3D Tree - IMPROVED: Compact with leaves
    # =========================================================================
    "tree_3d_simple": {
        "axiom": "FA",  # FIXED: was "!(1)F(200)/(45)A"
        "rules": {
            "A": "!(0.707)[&(30)$FL]/(120)[&(30)$FL]/(120)[&(30)$FL]FA",
            "L": "['''^^{-f+f+f-|-f+f+f}]",
            "F": "F"
        },
        "angle": 30,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "description": "Simple whorled tree (IMPROVED: compact with leaves)"
    },
    
    # =========================================================================
    # Birch Tree - IMPROVED: Graceful with foliage
    # =========================================================================
    "tree_3d_birch": {
        "axiom": "FFA",  # FIXED: was "!(1)F(300)A"
        "rules": {
            "A": "!(0.9)F[&(35)$BL][/(137.5)&(30)$CL]/(137.5)A",
            "B": "!(0.8)F[&(30)$BL][+(25)$L]/(137.5)B",
            "C": "!(0.8)F[&(25)$CL][-(25)$L]/(137.5)C",
            "L": "['''^^{-f+f+f}]",
            "F": "F"
        },
        "angle": 30,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.10,  # Reduced from 0.18
        "tropism_direction": [0, -1, 0],
        "description": "Birch (IMPROVED: graceful droop with foliage)"
    },
    
    # =========================================================================
    # Maple Tree - IMPROVED: Opposite branching with leaves
    # =========================================================================
    "tree_3d_maple": {
        "axiom": "FA",  # FIXED: was "!(1)F(200)X"
        "rules": {
            "A": "!(0.9)F[&(35)$BL]/(180)[&(35)$BL]/(137.5)FA",
            "B": "!(0.8)F[+(25)$CL][-(25)$CL]B",
            "C": "!(0.7)FL",
            "L": "['''^^{-f+f+f-f+f+f}]",
            "F": "F"
        },
        "angle": 35,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.05,
        "tropism_direction": [0, -1, 0],
        "description": "Maple (IMPROVED: decussate branching with leaves)"
    },
    
    # =========================================================================
    # Bush with Leaves - Dense variant
    # =========================================================================
    "bush_3d_with_leaves": {
        "axiom": "A",
        "rules": {
            "A": "[&FL]/////'[&FLA]/////'[&FL]/////'[&FLA]",
            "F": "S//F",
            "S": "FFL",
            "L": "['''^^{-f+f+f-|-f+f+f}]"
        },
        "angle": 18,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "width_decay": 0.85,
        "description": "Dense bush with lots of leaves [BEST]"
    },
    
    # =========================================================================
    # Gravity Series - IMPROVED: Shorter trunks
    # =========================================================================
    "tree_gravity_none": {
        "axiom": "FFA",  # FIXED: was "!(1)F(200)/(45)A"
        "rules": {
            "A": "!(0.707)[&(30)$BL][/(120)&(30)$BL][/(240)&(30)$BL]/(45)FA",
            "B": "!(0.707)F[+(25)$L][-(25)$L]B",
            "L": "['''^^{-f+f+f-|-f+f+f}]",
            "F": "F"
        },
        "angle": 30,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.0,
        "description": "Symmetric tree (IMPROVED: no gravity, compact)"
    },
    
    "tree_gravity_moderate": {
        "axiom": "FFA",
        "rules": {
            "A": "!(0.707)[&(30)$BL][/(120)&(30)$BL][/(240)&(30)$BL]/(45)FA",
            "B": "!(0.707)F[+(25)$L][-(25)$L]B",
            "L": "['''^^{-f+f+f-|-f+f+f}]",
            "F": "F"
        },
        "angle": 30,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.10,  # Reduced
        "tropism_direction": [0, -1, 0],
        "description": "Tree (IMPROVED: moderate gravity droop)"
    },
    
    "tree_gravity_strong": {
        "axiom": "FFA",
        "rules": {
            "A": "!(0.707)[&(30)$BL][/(120)&(30)$BL][/(240)&(30)$BL]/(45)FA",
            "B": "!(0.707)F[+(25)$L][-(25)$L]B",
            "L": "['''^^{-f+f+f-|-f+f+f}]",
            "F": "F"
        },
        "angle": 30,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.18,  # Reduced from 0.28
        "tropism_direction": [0, -1, 0],
        "description": "Weeping tree (IMPROVED: strong gravity)"
    },

    # =========================================================================
    # Coral - compact variant
    # =========================================================================
    "coral_branch": {
        "axiom": "FA",
        "rules": {"F": "F[&+F][^/F][&-F]", "A": "FA"},
        "angle": 35,
        "iterations": 6,
        "is_3d": True,
        "description": "Coral-like branching - compact"
    },
    
    # =========================================================================
    # Crystal Growth - IMPROVED: No long initial trunk
    # =========================================================================
    "crystal_growth": {
        "axiom": "A",  # FIXED: was "!(1)F(200)/(45)A"
        "rules": {
            "A": "!(0.8)FF[&(28)$B][^(28)$C][+(25)$B][-(25)$C]/(137.5)A",
            "B": "!(0.7)F[&(25)$B][+(20)$B]/(137.5)B",
            "C": "!(0.7)F[^(25)$C][-(20)$C]/(137.5)C",
            "F": "F"
        },
        "angle": 28,
        "iterations": 7,
        "is_3d": True,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "description": "Crystal-organic hybrid (IMPROVED: proportional)"
    },
    
    # =========================================================================
    # Tree with leaves - IMPROVED
    # =========================================================================
    "tree_with_leaves_berries": {
        "axiom": "FA",  # FIXED: was "!(1)F(200)A"
        "rules": {
            "A": "!(0.9)F[&(35)$BL]/(137.5)[&(35)$BL]/(137.5)FA",
            "B": "!(0.8)F[+(20)$CL][-(20)$CL]B",
            "C": "!(0.7)FL",
            "L": "['''^^{-f+f+f-|-f+f+f}]",
            "F": "F"
        },
        "angle": 25,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.06,
        "tropism_direction": [0, -1, 0],
        "description": "Tree with polygon leaves (IMPROVED)"
    },
    
    # =========================================================================
    # Phyllotaxis (unchanged - works well)
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
        "description": "Sunflower - golden angle spiral [BEST]"
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
# PARAMETRIC PRESETS - IMPROVED with leaves
# =============================================================================

PARAMETRIC_PRESETS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # Monopodial Trees - IMPROVED: With leaves, no long trunk
    # Based on ABOP Figure 2.6
    # =========================================================================
    "monopodial_tree": {
        "type": "parametric",
        "axiom": "A(1,10)",  # FIXED: was "!(1)F(200)/(45)A(1,10)"
        "productions": [
            "A(l,w) -> !(w)FF(l)[&(45)$B(l*0.6,w*0.707)L]/(137.5)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$C(l*0.6,w*0.707)L]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(45)$B(l*0.6,w*0.707)L]B(l*0.9,w*0.707)",
            "L -> ['''^^{-f+f+f-|-f+f+f}]"  # Added leaves!
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"r1": 0.9, "r2": 0.6, "a0": 45, "wr": 0.707},
        "angle": 45,
        "iterations": 9,
        "tropism_strength": 0.06,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "description": "ABOP 2.6 Monopodial (IMPROVED: with leaves) [BEST]"
    },
    
    "monopodial_narrow": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)FF(l)[&(30)$B(l*0.5,w*0.707)L]/(137.5)A(l*0.95,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(30)$C(l*0.5,w*0.707)L]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(30)$B(l*0.5,w*0.707)L]B(l*0.9,w*0.707)",
            "L -> ['''^^{-f+f+f}]"
        ],
        "rules": {"info": "Parametric narrow variant"},
        "constants": {},
        "angle": 30,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.04,
        "tropism_direction": [0, -1, 0],
        "description": "Monopodial narrow crown - conifer-like"
    },
    
    "monopodial_spreading": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)FF(l)[&(60)$B(l*0.7,w*0.707)L]/(137.5)A(l*0.85,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(50)$C(l*0.7,w*0.707)L]C(l*0.85,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(50)$B(l*0.7,w*0.707)L]B(l*0.85,w*0.707)",
            "L -> ['''^^{-f+f+f-|-f+f+f}]"
        ],
        "rules": {"info": "Parametric spreading variant"},
        "constants": {},
        "angle": 50,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "description": "Monopodial spreading crown - cedar-like"
    },
    
    # =========================================================================
    # Sympodial Trees - IMPROVED: With leaves, forking pattern
    # Based on ABOP Figure 2.7 - BEST RESULTS!
    # =========================================================================
    "sympodial_tree": {
        "type": "parametric",
        "axiom": "A(1,10)",  # FIXED: was "!(1)F(200)A(1,10)"
        "productions": [
            "A(l,w) -> !(w)FF(l)[&(15)$B(l*0.9,w*0.707)L]/(180)[&(50)$B(l*0.7,w*0.707)L]",
            "B(l,w) -> !(w)F(l)[+(15)$B(l*0.9,w*0.707)L][-(50)$B(l*0.7,w*0.707)L]",
            "L -> ['''^^{-f+f+f-|-f+f+f}]"  # Added leaves!
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"r1": 0.9, "r2": 0.7, "a1": 15, "a2": 50, "wr": 0.707},
        "angle": 35,
        "iterations": 9,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "description": "ABOP 2.7 Sympodial (IMPROVED: forking with leaves) [BEST]"
    },
    
    "sympodial_balanced": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)FF(l)[&(35)$B(l*0.8,w*0.707)L]/(180)[&(35)$B(l*0.8,w*0.707)L]",
            "B(l,w) -> !(w)F(l)[+(35)$B(l*0.8,w*0.707)L][-(35)$B(l*0.8,w*0.707)L]",
            "L -> ['''^^{-f+f+f-|-f+f+f}]"
        ],
        "rules": {"info": "Balanced forking"},
        "constants": {},
        "angle": 35,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.06,
        "tropism_direction": [0, -1, 0],
        "description": "Sympodial balanced - oak-like crown [BEST]"
    },
    
    "sympodial_weeping": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)FF(l)[&(20)$B(l*0.85,w*0.707)L]/(180)[&(70)$B(l*0.6,w*0.707)L]",
            "B(l,w) -> !(w)F(l)[+(20)$B(l*0.85,w*0.707)L][-(70)$B(l*0.6,w*0.707)L]",
            "L -> ['''^^{-f+f}]"
        ],
        "rules": {"info": "Weeping form"},
        "constants": {},
        "angle": 45,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.15,
        "tropism_direction": [0, -1, 0],
        "description": "Sympodial weeping - willow-like"
    },
    
    # =========================================================================
    # Ternary Trees - IMPROVED: With leaves, moderate tropism
    # Based on ABOP Figure 2.8
    # =========================================================================
    "ternary_tree": {
        "type": "parametric",
        "axiom": "A",  # FIXED: was "!(1)F(200)/(45)A"
        "productions": [
            "A -> !(1.732)F[&(35)$FL]/(94.74)[&(35)$FL]/(132.63)[&(35)$FL]A",
            "F(l) -> F(l*1.05)",
            "L -> ['''^^{-f+f+f-|-f+f+f}]"  # Added leaves!
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"d1": 94.74, "d2": 132.63, "a": 35, "lr": 1.05, "vr": 1.732},
        "angle": 20,
        "iterations": 7,
        "tropism_strength": 0.04,  # FIXED: was 0.15
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "description": "ABOP 2.8 Ternary (IMPROVED: with leaves)"
    },
    
    "ternary_golden": {
        "type": "parametric",
        "axiom": "A",
        "productions": [
            "A -> !(1.732)FF[&(19)$FL]/(137.5)[&(19)$FL]/(137.5)[&(19)$FL]A",
            "F(l) -> F(l*1.109)",
            "L -> ['''^^{-f+f+f-|-f+f+f}]"
        ],
        "rules": {"info": "Golden angle divergence"},
        "constants": {},
        "angle": 20,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.05,
        "tropism_direction": [0, -1, 0],
        "description": "Ternary golden angle - phyllotactic spiral"
    },
    
    "ternary_pine": {
        "type": "parametric",
        "axiom": "A",
        "productions": [
            "A -> !(1.732)FF[&(36)$FL]/(180)[&(36)$FL]/(252)[&(36)$FL]A",
            "F(l) -> F(l*1.07)",
            "L -> ['''^^{-f+f}]"
        ],
        "rules": {"info": "Pine-like"},
        "constants": {},
        "angle": 36,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "description": "Ternary pine - drooping needles"
    },
    
    # =========================================================================
    # Special Forms - NEW
    # =========================================================================
    "umbrella_tree": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)FFFF(l)B(l*0.8,w*0.707)",
            "B(l,w) -> [&(70)$C(l,w*0.707)L]/(72)[&(70)$C(l,w*0.707)L]/(72)[&(70)$C(l,w*0.707)L]/(72)[&(70)$C(l,w*0.707)L]/(72)[&(70)$C(l,w*0.707)L]",
            "C(l,w) -> !(w)F(l)[+(30)$D(l*0.7,w*0.707)L][-(30)$D(l*0.7,w*0.707)L]",
            "D(l,w) -> !(w)F(l)L",
            "L -> ['''^^{-f+f+f-|-f+f+f}]"
        ],
        "rules": {"info": "Umbrella shape"},
        "constants": {},
        "angle": 70,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "description": "Umbrella/parasol tree - flat canopy"
    },
    
    "bonsai_tree": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(60)$B(l*0.5,w*0.707)L]/(90)[&(45)$B(l*0.6,w*0.707)L]/(180)[&(70)$B(l*0.4,w*0.707)L]A(l*0.8,w*0.707)",
            "B(l,w) -> !(w)F(l)[+(40)$C(l*0.6,w*0.707)L][-(50)$C(l*0.5,w*0.707)L]",
            "C(l,w) -> !(w)F(l)L",
            "L -> ['''^^{-f+f+f-|-f+f+f}]"
        ],
        "rules": {"info": "Asymmetric bonsai"},
        "constants": {},
        "angle": 50,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.10,
        "tropism_direction": [0, -1, 0],
        "description": "Bonsai - asymmetric artistic form"
    },
    
    # =========================================================================
    # Stochastic (unchanged)
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
    # Ferns (unchanged - work well)
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
        "description": "Simple pinnate fern"
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
        "description": "Fern with apical delay [BEST]"
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
        "description": "Complex fern - high apical delay [BEST]"
    },
}

# =============================================================================
# Helper Functions
# =============================================================================

def get_preset(name: str, include_3d=True):
    """Get a preset by name from any category."""
    name_lower = name.lower()
    
    for key in PRESETS_2D:
        if key.lower() == name_lower:
            return PRESETS_2D[key]
    
    if not include_3d:
        return None
    
    for key in PRESETS_3D:
        if key.lower() == name_lower:
            return PRESETS_3D[key]
    
    for key in PARAMETRIC_PRESETS:
        if key.lower() == name_lower:
            preset = PARAMETRIC_PRESETS[key].copy()
            preset['is_parametric'] = True
            if 'productions' in preset and 'rules' not in preset:
                preset['rules'] = {'parametric': str(preset['productions'])}
            return preset
    
    return None


def list_presets(include_3d=True):
    """Return list of preset names."""
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