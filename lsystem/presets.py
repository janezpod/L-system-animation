"""
L-System Plant Presets - BEST OF THE BEST + ABOP Realistic Trees

Hand-picked, research-improved presets for beautiful plant renders.
All fixes from ABOP research applied.

Contains:
- 2D Classics (ABOP 1.24 series)
- 3D Trees with leaves
- ABOP Fig 2.7 - Sympodial trees (4 variants)
- ABOP Fig 2.8 - Ternary branching (4 variants)
- Realistic species trees (oak, elm, willow, pine, spruce, bonsai)
- Parametric trees (monopodial, sympodial, ternary)
- Stochastic/organic variations
- Fractals (dragon, hilbert)

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
        "growth_mode": "sigmoid",
        "description": "ABOP 1.24a - Classic bush"
    },
    
    "abop_1_24b": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F][F]"},
        "angle": 20.0,
        "iterations": 6,
        "base_width": 1.5,
        "growth_mode": "sigmoid",
        "description": "ABOP 1.24b - Vertical branch"
    },
    
    "abop_1_24c": {
        "axiom": "F",
        "rules": {"F": "FF-[-F+F+F]+[+F-F-F]"},
        "angle": 22.5,
        "iterations": 5,
        "base_width": 1.5,
        "growth_mode": "sigmoid",
        "description": "ABOP 1.24c - Bilateral symmetry"
    },
    
    "abop_1_24d": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 20.0,
        "iterations": 8,
        "base_width": 1.2,
        "growth_mode": "sigmoid",
        "description": "ABOP 1.24d - Asymmetric"
    },
    
    "abop_1_24e": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]FX", "F": "FF"},
        "angle": 25.7,
        "iterations": 8,
        "base_width": 1.2,
        "growth_mode": "sigmoid",
        "description": "ABOP 1.24e - Sympodial growth"
    },
    
    "abop_1_24f": {
        "axiom": "X",
        "rules": {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        "angle": 22.5,
        "iterations": 6,
        "base_width": 1.2,
        "growth_mode": "sigmoid",
        "description": "ABOP 1.24f - ICONIC elegant plant [BEST]"
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
        "growth_mode": "sigmoid",
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
        "growth_mode": "sigmoid",
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
        "growth_mode": "sigmoid",
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
        "growth_mode": "sigmoid",
        "description": "Hilbert space-filling curve [BEST]"
    },
    
    "koch_snowflake": {
        "axiom": "F++F++F",
        "rules": {"F": "F-F++F-F"},
        "angle": 60,
        "iterations": 5,
        "base_width": 1.0,
        "growth_mode": "sigmoid",
        "description": "Koch snowflake"
    },
    
    "quadratic_snowflake": {
        "axiom": "-F",
        "rules": {"F": "F+F-F-F+F"},
        "angle": 90,
        "iterations": 5,
        "growth_mode": "sigmoid",
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
        "growth_mode": "sigmoid",
        "description": "ABOP 1.25 - Bush with hexagonal leaves - THE BEST [BEST]"
    },
    
    "abop_1_26": {
        "axiom": "A",
        "rules": {
            "A": "[&FPLA]/////'[&FPLA]/////'[&FPLA]",
            "P": "F[++L][--L]",
            "L": "[{-f+f-f-f}]",
            "F": "FF"
        },
        "angle": 18,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
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
        "growth_mode": "sigmoid",
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
        "growth_mode": "sigmoid",
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
        "growth_mode": "sigmoid",
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
        "growth_mode": "sigmoid",
        "description": "Maple tree with balanced branching"
    },
    
    "bush_3d_with_leaves": {
        "axiom": "A",
        "rules": {
            "A": "[&(30)$FL]/(120)[&(30)$FL]/(120)[&(30)$FL]/(45)FA",
            "F": "S///F",
            "S": "F",
            "L": "['''^^{-f+f+f-|-f+f+f}]"
        },
        "angle": 25,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "3D bush with polygon leaves"
    },
    
    # =========================================================================
    # Tropism Demo
    # =========================================================================
    "tree_gravity_0_none": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.85)F(80)[&(25)$B][/(137.5)&(25)$B][/(275)&(25)$B]/(45)A",
            "B": "!(0.75)F(60)[+(30)$C][-(30)$C]/(137.5)B",
            "C": "!(0.65)F(40)L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 30,
        "iterations": 5,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.0,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Tropism comparison - NO gravity (0.0)"
    },
    
    "tree_gravity_1_moderate": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.85)F(80)[&(25)$B][/(137.5)&(25)$B][/(275)&(25)$B]/(45)A",
            "B": "!(0.75)F(60)[+(30)$C][-(30)$C]/(137.5)B",
            "C": "!(0.65)F(40)L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 30,
        "iterations": 5,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.15,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Tropism comparison - MODERATE gravity (0.15)"
    },
    
    "tree_gravity_2_strong": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.85)F(80)[&(25)$B][/(137.5)&(25)$B][/(275)&(25)$B]/(45)A",
            "B": "!(0.75)F(60)[+(30)$C][-(30)$C]/(137.5)B",
            "C": "!(0.65)F(40)L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 30,
        "iterations": 5,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.35,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Tropism comparison - STRONG gravity (0.35) [BEST]"
    },
    
    # =========================================================================
    # ABOP Figure 2.7 - Sympodial Trees (Aono & Kunii)
    # Research-validated parameters from Table 2.2
    # Uses Leonardo's rule: width_decay = 0.707 (sqrt(2)^-1)
    # =========================================================================
    "sympodial_2_7a": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.707)F(50)[&(5)$B][/(180)&(65)$B]",
            "B": "!(0.707)F(45)[&(5)$B][/(180)&(65)$B]",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 35,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "ABOP 2.7a - Tight main branch (a1=5, a2=65)"
    },
    
    "sympodial_2_7b": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.707)F(50)[&(10)$B][/(180)&(60)$B]",
            "B": "!(0.707)F(45)[&(10)$B][/(180)&(60)$B]",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 35,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.10,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "ABOP 2.7b - Moderate spread (a1=10, a2=60)"
    },
    
    "sympodial_2_7c": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.707)F(50)[&(20)$B][/(180)&(50)$B]",
            "B": "!(0.707)F(45)[&(20)$B][/(180)&(50)$B]",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 35,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "ABOP 2.7c - Balanced crown (a1=20, a2=50)"
    },
    
    "sympodial_2_7d": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.707)F(50)[&(35)$BL][/(180)&(35)$BL]",
            "B": "!(0.707)F(45)[&(35)$BL][/(180)&(35)$BL]",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 35,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.14,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "ABOP 2.7d - SYMMETRIC (a1=a2=35) [BEST]"
    },
    
    # =========================================================================
    # ABOP Figure 2.8 - Ternary Branching Trees
    # Research-validated parameters from Table 2.3
    # Uses da Vinci's rule: width_decay = 1.732 (sqrt(3)) for ternary
    # =========================================================================
    "ternary_2_8a": {
        "axiom": "!(1)F(200)/(45)A",
        "rules": {
            "A": "!(1.732)F(50)[&(19)$B]/(94.74)[&(19)$B]/(132.63)[&(19)$B]",
            "B": "!(1.732)F(45)[&(19)$B]/(94.74)[&(19)$B]/(132.63)[&(19)$B]",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 20,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.22,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "ABOP 2.8a - Conifer angles (d1=94.74, d2=132.63)"
    },
    
    "ternary_2_8b": {
        "axiom": "!(1)F(200)/(45)A",
        "rules": {
            "A": "!(1.732)F(50)[&(22)$BL]/(137.5)[&(22)$BL]/(137.5)[&(22)$BL]",
            "B": "!(1.732)F(45)[&(22)$BL]/(137.5)[&(22)$BL]/(137.5)[&(22)$BL]",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 20,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.14,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "ABOP 2.8b - Golden angle whorls (137.5) [BEST]"
    },
    
    "ternary_2_8c": {
        "axiom": "!(1)F(200)/(45)A",
        "rules": {
            "A": "!(1.732)F(60)[&(25)$B]/(120)[&(25)$B]/(120)[&(25)$B]",
            "B": "!(1.732)F(55)[&(25)$B]/(120)[&(25)$B]/(120)[&(25)$B]",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 20,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.27,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "ABOP 2.8c - Spreading (lr=1.79 high elongation)"
    },
    
    "ternary_2_8d": {
        "axiom": "!(1)F(200)/(45)A",
        "rules": {
            "A": "!(1.732)F(50)[&(18)$BL]/(100)[&(22)$BL]/(140)[&(15)$BL]",
            "B": "!(1.732)F(45)[&(18)$BL]/(100)[&(22)$BL]/(140)[&(15)$BL]",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 20,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.40,
        "tropism_direction": [-0.61, -0.77, -0.19],
        "growth_mode": "sigmoid",
        "description": "ABOP 2.8d - Windswept asymmetric tropism"
    },
    
    # =========================================================================
    # Honda's Models - Research Validated
    # =========================================================================
    # NOTE: honda_realistic moved to PARAMETRIC_PRESETS as "honda_param"
    # The original here was broken (used static values instead of recursive contraction)
    
    # =========================================================================
    # Simple Trees - Basic static versions for quick testing
    # For true ABOP accuracy, use the parametric versions in PARAMETRIC_PRESETS
    # =========================================================================
    "oak_simple": {
        "axiom": "F",
        "rules": {
            "F": "FF[&F][/&F][//&F][///&F]"
        },
        "angle": 30,
        "iterations": 5,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Simple oak-like branching (use oak_param for realistic)"
    },
    
    # =========================================================================
    # Stochastic Trees - Organic Variation
    # =========================================================================
    "stochastic_tree_3d": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.707)F(50)[&(35)$BL][/(137.5)&(35)$BL]/(137.5)A",
            "B": "!(0.707)F(40)[+(30)$CL][-(30)$CL]",
            "C": "!(0.707)F(30)L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 30,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Stochastic 3D tree - organic variation"
    },
    
    "stochastic_conifer": {
        "axiom": "!(1)F(300)/(45)A",
        "rules": {
            "A": "!(1.732)F(50)[&(20)$B]/(120)[&(22)$B]/(120)[&(18)$B]/(45)A",
            "B": "!(1.732)F(45)[&(20)$B]/(120)[&(22)$B]/(120)[&(18)$B]",
            "L": "['''&&&{-f+f}]"
        },
        "angle": 20,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.15,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Stochastic conifer - varied whorls"
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
        "growth_mode": "sigmoid",
        "description": "ABOP Fig 2.6 - Monopodial (FIXED 3D with roll) [BEST]"
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
        "growth_mode": "sigmoid",
        "description": "ABOP Fig 2.7 - Sympodial (FIXED z-growth) [BEST]"
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
        "growth_mode": "sigmoid",
        "description": "ABOP Fig 2.8 - Ternary (FIXED 3D whorls) [BEST]"
    },
    
    # =========================================================================
    # Parametric Sympodial Variants (ABOP 2.7)
    # =========================================================================
    "sympodial_param_a": {
        "type": "parametric",
        "axiom": "!(1)F(200)A(50,10)",
        "productions": [
            "A(l,w) -> !(w*0.707)F(l)[&(5)$B(l*0.9,w*0.707)]/(180)[&(65)$B(l*0.8,w*0.707)]",
            "B(l,w) -> !(w*0.707)F(l)[&(5)$B(l*0.9,w*0.707)]/(180)[&(65)$B(l*0.8,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 35,
        "iterations": 10,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "growth_mode": "sigmoid",
        "description": "Sympodial parametric a1=5, a2=65"
    },
    
    "sympodial_param_b": {
        "type": "parametric",
        "axiom": "!(1)F(200)A(50,10)",
        "productions": [
            "A(l,w) -> !(w*0.707)F(l)[&(10)$B(l*0.9,w*0.707)]/(180)[&(60)$B(l*0.8,w*0.707)]",
            "B(l,w) -> !(w*0.707)F(l)[&(10)$B(l*0.9,w*0.707)]/(180)[&(60)$B(l*0.8,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 35,
        "iterations": 10,
        "tropism_strength": 0.10,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "growth_mode": "sigmoid",
        "description": "Sympodial parametric a1=10, a2=60"
    },
    
    "sympodial_param_c": {
        "type": "parametric",
        "axiom": "!(1)F(200)A(50,10)",
        "productions": [
            "A(l,w) -> !(w*0.707)F(l)[&(20)$B(l*0.9,w*0.707)]/(180)[&(50)$B(l*0.8,w*0.707)]",
            "B(l,w) -> !(w*0.707)F(l)[&(20)$B(l*0.9,w*0.707)]/(180)[&(50)$B(l*0.8,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 35,
        "iterations": 10,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "growth_mode": "sigmoid",
        "description": "Sympodial parametric a1=20, a2=50"
    },
    
    "sympodial_param_d": {
        "type": "parametric",
        "axiom": "!(1)F(200)A(50,10)",
        "productions": [
            "A(l,w) -> !(w*0.707)F(l)[&(35)$B(l*0.9,w*0.707)L]/(180)[&(35)$B(l*0.8,w*0.707)L]",
            "B(l,w) -> !(w*0.707)F(l)[&(35)$B(l*0.9,w*0.707)L]/(180)[&(35)$B(l*0.8,w*0.707)L]",
            "L -> ['''&&&{-f+f+f-|-f+f+f}]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 35,
        "iterations": 10,
        "tropism_strength": 0.14,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Sympodial parametric SYMMETRIC a1=a2=35 [BEST]"
    },
    
    # =========================================================================
    # Parametric Ternary Variants (ABOP 2.8)
    # =========================================================================
    "ternary_param_a": {
        "type": "parametric",
        "axiom": "!(1)F(200)/(45)A(50)",
        "productions": [
            "A(l) -> !(1.732)F(l)[&(19)$B(l*0.9)]/(94.74)[&(19)$B(l*0.9)]/(132.63)[&(19)$B(l*0.9)]",
            "B(l) -> !(1.732)F(l)[&(19)$B(l*0.9)]/(94.74)[&(19)$B(l*0.9)]/(132.63)[&(19)$B(l*0.9)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 20,
        "iterations": 7,
        "tropism_strength": 0.22,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "growth_mode": "sigmoid",
        "description": "Ternary parametric d1=94.74, d2=132.63"
    },
    
    "ternary_param_b": {
        "type": "parametric",
        "axiom": "!(1)F(200)/(45)A(50)",
        "productions": [
            "A(l) -> !(1.732)F(l)[&(22)$B(l*0.9)L]/(137.5)[&(22)$B(l*0.9)L]/(137.5)[&(22)$B(l*0.9)L]",
            "B(l) -> !(1.732)F(l)[&(22)$B(l*0.9)L]/(137.5)[&(22)$B(l*0.9)L]/(137.5)[&(22)$B(l*0.9)L]",
            "L -> ['''&&&{-f+f+f-|-f+f+f}]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 20,
        "iterations": 7,
        "tropism_strength": 0.14,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Ternary parametric golden angle 137.5 [BEST]"
    },
    
    "ternary_param_c": {
        "type": "parametric",
        "axiom": "!(1)F(200)/(45)A(60)",
        "productions": [
            "A(l) -> !(1.732)F(l)[&(25)$B(l*1.1)]/(120)[&(25)$B(l*1.1)]/(120)[&(25)$B(l*1.1)]",
            "B(l) -> !(1.732)F(l)[&(25)$B(l*1.1)]/(120)[&(25)$B(l*1.1)]/(120)[&(25)$B(l*1.1)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 20,
        "iterations": 6,
        "tropism_strength": 0.27,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "growth_mode": "sigmoid",
        "description": "Ternary parametric spreading lr=1.79"
    },
    
    "ternary_param_d": {
        "type": "parametric",
        "axiom": "!(1)F(200)/(45)A(50)",
        "productions": [
            "A(l) -> !(1.732)F(l)[&(18)$B(l*0.95)L]/(100)[&(22)$B(l*0.95)L]/(140)[&(15)$B(l*0.95)L]",
            "B(l) -> !(1.732)F(l)[&(18)$B(l*0.95)L]/(100)[&(22)$B(l*0.95)L]/(140)[&(15)$B(l*0.95)L]",
            "L -> ['''&&&{-f+f+f-|-f+f+f}]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 20,
        "iterations": 7,
        "tropism_strength": 0.40,
        "tropism_direction": [-0.61, -0.77, -0.19],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Ternary parametric windswept asymmetric"
    },
    
    # =========================================================================
    # Parametric Honda/Realistic Species Trees (ABOP-accurate)
    # These use TRUE recursive contraction for realistic tree shapes
    # =========================================================================
    # =========================================================================
    # SYMMETRIC Honda Trees with TINY GREEN LEAVES ON ALL BRANCHES
    # Using f(0.02) for very small leaf polygons
    # =========================================================================
    
    "honda_symmetric_3": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l*0.3)[&(45)B(l*0.8,w*0.707)]/(120)[&(45)B(l*0.8,w*0.707)]/(120)[&(45)B(l*0.8,w*0.707)]F(l*0.7)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[''''''''^^{-f(0.02)+f(0.02)-|-f(0.02)+f(0.02)}][-(45)$B(l*0.8,w*0.707)][+(45)$B(l*0.8,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Honda SYMMETRIC 3-way - TINY green leaves [BEST]"
    },
    
    "honda_symmetric_4": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l*0.3)[&(50)B(l*0.75,w*0.707)]/(90)[&(50)B(l*0.75,w*0.707)]/(90)[&(50)B(l*0.75,w*0.707)]/(90)[&(50)B(l*0.75,w*0.707)]F(l*0.7)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[''''''''^^{-f(0.02)+f(0.02)-|-f(0.02)+f(0.02)}][-(40)$B(l*0.8,w*0.707)][+(40)$B(l*0.8,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Honda SYMMETRIC 4-way - TINY green leaves"
    },
    
    "honda_symmetric_5": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l*0.3)[&(35)B(l*0.7,w*0.707)]/(72)[&(35)B(l*0.7,w*0.707)]/(72)[&(35)B(l*0.7,w*0.707)]/(72)[&(35)B(l*0.7,w*0.707)]/(72)[&(35)B(l*0.7,w*0.707)]F(l*0.7)A(l*0.92,w*0.85)",
            "B(l,w) -> !(w)F(l)[''''''''^^{-f(0.015)+f(0.015)-|-f(0.015)+f(0.015)}][-(30)$B(l*0.75,w*0.707)][+(30)$B(l*0.75,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Honda SYMMETRIC 5-way pine - TINY green needles"
    },
    
    "honda_symmetric_full": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l*0.3)[&(55)B(l*0.9,w*0.707)]/(120)[&(55)B(l*0.9,w*0.707)]/(120)[&(55)B(l*0.9,w*0.707)]F(l*0.7)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[''''''''^^{-f(0.02)+f(0.02)-|-f(0.02)+f(0.02)}][-(50)$B(l*0.9,w*0.707)][+(50)$B(l*0.9,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Honda SYMMETRIC FULL - TINY dense green leaves [BEST]"
    },
    
    "honda_symmetric_weeping": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l*0.3)[&(55)B(l*0.85,w*0.707)]/(120)[&(55)B(l*0.85,w*0.707)]/(120)[&(55)B(l*0.85,w*0.707)]F(l*0.7)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[''''''''^^{-f(0.02)+f(0.02)-|-f(0.02)+f(0.02)}][-(45)$B(l*0.9,w*0.707)][+(45)$B(l*0.9,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 7,
        "tropism_strength": 0.40,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Honda SYMMETRIC WEEPING - TINY leaves + gravity [BEST]"
    },
    
    "honda_symmetric_bare": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l*0.3)[&(45)B(l*0.8,w*0.707)]/(120)[&(45)B(l*0.8,w*0.707)]/(120)[&(45)B(l*0.8,w*0.707)]F(l*0.7)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$B(l*0.8,w*0.707)][+(45)$B(l*0.8,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 45,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Honda SYMMETRIC bare branches (no leaves)"
    },
    
    # =========================================================================
    # CREATIVE STYLIZED PLANTS - Visually Interesting
    # =========================================================================
    
    # --- SPIRAL SUCCULENT ---
    # Tight spiral rosette like an aloe or agave
    "spiral_succulent": {
        "type": "parametric",
        "axiom": "A(1,8)",
        "productions": [
            # Each level: short stem + leaf, rotate by golden angle, continue smaller
            "A(l,w) -> !(w)F(l*0.1)[''''''''&(70){-f(0.015)+f(0.015)+f(0.015)-|-f(0.015)+f(0.015)+f(0.015)}]/(137.5)A(l*0.97,w*0.95)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 40,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "linear",
        "description": "Spiral succulent rosette - golden angle phyllotaxis"
    },
    
    # --- UMBRELLA TREE ---
    # Flat spreading canopy like an acacia
    "umbrella_tree": {
        "type": "parametric",
        "axiom": "!(10)F(1)A(0.5,6)",
        "productions": [
            # Tall trunk, then spreading flat branches at top
            "A(l,w) -> !(w)[&(85)B(l,w*0.7)]/(60)[&(85)B(l,w*0.7)]/(60)[&(85)B(l,w*0.7)]/(60)[&(85)B(l,w*0.7)]/(60)[&(85)B(l,w*0.7)]/(60)[&(85)B(l,w*0.7)]",
            "B(l,w) -> !(w)F(l)[''''''''^^{-f(0.008)+f(0.008)-|-f(0.008)+f(0.008)}][+(20)B(l*0.7,w*0.8)][-(20)B(l*0.7,w*0.8)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Umbrella/Acacia tree - flat spreading canopy"
    },
    
    # --- CORAL BRANCH ---
    # Dense branching coral-like structure
    "coral_branch": {
        "type": "parametric",
        "axiom": "A(1,8)",
        "productions": [
            # Bifurcating branches with slight randomness feel
            "A(l,w) -> !(w)F(l)[+(30)&(20)A(l*0.75,w*0.75)][-(30)&(20)A(l*0.75,w*0.75)][&(40)A(l*0.6,w*0.7)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 30,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Coral branch - dense bifurcating structure"
    },
    
    # --- FLOWERING BURST ---
    # Plant with colorful flower at branch tips
    "flowering_burst": {
        "type": "parametric",
        "axiom": "!(8)F(0.5)A(0.4,5)",
        "productions": [
            # Main branching structure
            "A(l,w) -> !(w)F(l)[&(45)B(l*0.7,w*0.707)]/(90)[&(50)B(l*0.7,w*0.707)]/(90)[&(45)B(l*0.7,w*0.707)]/(90)[&(50)B(l*0.7,w*0.707)]F(l*0.5)A(l*0.8,w*0.707)",
            # Branches with flowers (pink/red) at tips
            "B(l,w) : l > 0.1 -> !(w)F(l)[-(40)B(l*0.7,w*0.75)][+(40)B(l*0.7,w*0.75)]",
            "B(l,w) : l <= 0.1 -> !(w)F(l)[''''^^{-f(0.008)+f(0.008)+f(0.008)-|-f(0.008)+f(0.008)+f(0.008)}]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Flowering burst - pink flowers at branch tips"
    },
    
    # --- TWISTED BONSAI ---
    # Asymmetric windswept bonsai style
    "twisted_bonsai": {
        "type": "parametric",
        "axiom": "!(10)&(10)/(20)F(0.8)A(0.5,6)",
        "productions": [
            # Asymmetric branching with strong bias to one side
            "A(l,w) -> !(w)F(l)[&(60)/(30)B(l*0.8,w*0.707)][&(40)/(-60)B(l*0.5,w*0.6)]/(80)A(l*0.85,w*0.75)",
            "B(l,w) -> !(w)F(l)[''''''''^^{-f(0.008)+f(0.008)-|-f(0.008)+f(0.008)}][&(35)B(l*0.7,w*0.707)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 7,
        "tropism_strength": 0.15,
        "tropism_direction": [0.3, -1, 0.1],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Twisted bonsai - asymmetric windswept style"
    },
    
    # --- PALM FROND ---
    # Fan-like palm with long fronds
    "palm_fan": {
        "type": "parametric",
        "axiom": "!(12)F(1.2)A(0.8,8)",
        "productions": [
            # Crown of fronds spreading outward
            "A(l,w) -> [&(70)B(l,w*0.3)]/(51.4)[&(65)B(l,w*0.3)]/(51.4)[&(75)B(l,w*0.3)]/(51.4)[&(60)B(l,w*0.3)]/(51.4)[&(70)B(l,w*0.3)]/(51.4)[&(65)B(l,w*0.3)]/(51.4)[&(75)B(l,w*0.3)]",
            # Each frond with leaflets along its length
            "B(l,w) -> !(w)F(l*0.3)[''''''''+(60){-f(0.005)+f(0.005)-|-f(0.005)+f(0.005)}][''''''''-(60){-f(0.005)+f(0.005)-|-f(0.005)+f(0.005)}]F(l*0.25)[''''''''+(55){-f(0.006)+f(0.006)-|-f(0.006)+f(0.006)}][''''''''-(55){-f(0.006)+f(0.006)-|-f(0.006)+f(0.006)}]F(l*0.2)[''''''''+(50){-f(0.005)+f(0.005)-|-f(0.005)+f(0.005)}][''''''''-(50){-f(0.005)+f(0.005)-|-f(0.005)+f(0.005)}]F(l*0.15)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 3,
        "tropism_strength": 0.25,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Palm fan - tropical palm with drooping fronds"
    },
    
    # --- CRYSTAL TREE ---
    # Geometric crystalline branching structure
    "crystal_tree": {
        "type": "parametric",
        "axiom": "!(8)F(0.6)A(0.5,6)",
        "productions": [
            # 6-way symmetric branching like ice crystals
            "A(l,w) -> !(w)F(l)[&(60)B(l*0.6,w*0.7)]/(60)[&(60)B(l*0.6,w*0.7)]/(60)[&(60)B(l*0.6,w*0.7)]/(60)[&(60)B(l*0.6,w*0.7)]/(60)[&(60)B(l*0.6,w*0.7)]/(60)[&(60)B(l*0.6,w*0.7)]A(l*0.7,w*0.8)",
            "B(l,w) -> !(w)F(l)[&(60)B(l*0.5,w*0.7)][^(60)B(l*0.5,w*0.7)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 60,
        "iterations": 5,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "linear",
        "description": "Crystal tree - 6-way symmetric geometric branching"
    },
    
    # --- VINE SPIRAL ---
    # Climbing vine that spirals upward
    "vine_spiral": {
        "type": "parametric",
        "axiom": "A(1,5)",
        "productions": [
            # Spiral climb with leaves at each node
            "A(l,w) -> !(w)F(l*0.15)[''''''''&(70){-f(0.008)+f(0.008)-|-f(0.008)+f(0.008)}]/(90)&(5)A(l*0.98,w*0.98)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 35,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "linear",
        "description": "Vine spiral - climbing spiral with leaves"
    },
    
    # --- DANDELION PUFF ---
    # Spherical seed head
    "dandelion_puff": {
        "type": "parametric",
        "axiom": "!(6)F(0.8)A(0.3,4)",
        "productions": [
            # Radiating seeds in all directions using golden angle
            "A(l,w) -> [&(20)''''''''{-f(0.005)+f(0.005)-|-f(0.005)+f(0.005)}]/(137.5)[&(40)''''''''{-f(0.005)+f(0.005)-|-f(0.005)+f(0.005)}]/(137.5)[&(60)''''''''{-f(0.005)+f(0.005)-|-f(0.005)+f(0.005)}]/(137.5)[&(80)''''''''{-f(0.005)+f(0.005)-|-f(0.005)+f(0.005)}]/(137.5)^(5)A(l*0.95,w)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 15,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "apical",
        "description": "Dandelion puff - spherical seed head"
    },
    
    # --- MUSHROOM CAP ---
    # Umbrella-shaped mushroom
    "mushroom_cap": {
        "type": "parametric",
        "axiom": "!(10)F(0.6)A(0.5,8)",
        "productions": [
            # Radiating gills under cap
            "A(l,w) -> [&(95)''''''F(l*0.4)]/(20)[&(92)''''''F(l*0.45)]/(20)[&(88)''''''F(l*0.5)]/(20)[&(85)''''''F(l*0.52)]/(20)[&(82)''''''F(l*0.53)]/(20)[&(80)''''''F(l*0.54)]/(20)[&(78)''''''F(l*0.53)]/(20)[&(76)''''''F(l*0.52)]/(20)[&(75)''''''F(l*0.5)]/(20)[&(76)''''''F(l*0.48)]/(20)[&(78)''''''F(l*0.45)]/(20)[&(80)''''''F(l*0.42)]/(20)[&(83)''''''F(l*0.38)]/(20)[&(87)''''''F(l*0.33)]/(20)[&(92)''''''F(l*0.27)]/(20)[&(97)''''''F(l*0.2)]/(20)[&(100)''''''F(l*0.12)]/(20)[&(95)''''''F(l*0.4)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 2,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Mushroom cap - umbrella dome with gills"
    },
    
    # --- FERN UNFURL ---
    # Fern frond with curled tip (fiddlehead)
    "fern_unfurl": {
        "type": "parametric",
        "axiom": "!(6)&(15)A(0.8,5)",
        "productions": [
            # Main rachis with pinnae, curling at tip
            "A(l,w) -> !(w)F(l*0.12)[''''''''+(70){-f(0.006)+f(0.006)-|-f(0.006)+f(0.006)}][''''''''-(70){-f(0.006)+f(0.006)-|-f(0.006)+f(0.006)}]^(8)A(l*0.94,w*0.95)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 30,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Fern unfurl - curling fiddlehead frond"
    },
    
    # --- EXPLOSION BUSH ---  
    # Dramatic radiating growth from center
    "explosion_bush": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            # Multiple branches exploding outward at each level
            "A(l,w) -> !(w)F(l*0.2)[&(30)B(l*0.9,w*0.65)]/(72)[&(35)B(l*0.85,w*0.65)]/(72)[&(30)B(l*0.9,w*0.65)]/(72)[&(35)B(l*0.85,w*0.65)]/(72)[&(30)B(l*0.9,w*0.65)]A(l*0.7,w*0.707)",
            "B(l,w) -> !(w)F(l)[''''''''^^{-f(0.006)+f(0.006)-|-f(0.006)+f(0.006)}][&(25)B(l*0.75,w*0.707)][/(90)&(25)B(l*0.7,w*0.65)]"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "apical",
        "description": "Explosion bush - dramatic radiating growth"
    },
    
    # --- WEEPING CANOPY ---
    # Dense drooping branches like a weeping willow
    "weeping_canopy": {
        "type": "parametric",
        "axiom": "!(12)F(0.8)A(0.6,8)",
        "productions": [
            # Umbrella of drooping branches
            "A(l,w) -> !(w)[&(70)B(l,w*0.5)]/(45)[&(65)B(l,w*0.5)]/(45)[&(70)B(l,w*0.5)]/(45)[&(65)B(l,w*0.5)]/(45)[&(70)B(l,w*0.5)]/(45)[&(65)B(l,w*0.5)]/(45)[&(70)B(l,w*0.5)]/(45)[&(65)B(l,w*0.5)]",
            # Long trailing branches with small leaves
            "B(l,w) -> !(w)F(l*0.15)[''''''''^^{-f(0.004)+f(0.004)-|-f(0.004)+f(0.004)}]B(l*0.92,w*0.9)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 22.5,
        "iterations": 12,
        "tropism_strength": 0.5,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Weeping canopy - dense drooping willow style"
    },
    
    # --- SPIKY AGAVE ---
    # Thick pointed leaves in rosette
    "spiky_agave": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            # Thick pointed triangular leaves spiraling up
            "A(l,w) -> !(w*0.3)F(l*0.05)[''''''''&(75){-f(0.008)+f(0.025)+f(0.025)+f(0.008)-|-f(0.008)+f(0.008)}]/(137.5)A(l*0.98,w*0.97)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 30,
        "iterations": 25,
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "linear",
        "description": "Spiky agave - thick pointed rosette leaves"
    },
    
    # =========================================================================
    # ABOP Figure 2.6 - Honda's Original SPIRAL Trees (for reference)
    # These have the characteristic spiral phyllotaxis pattern
    # =========================================================================
    
    "honda_2_6a": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(45)B(l*0.6,w*0.707)]/(137.5)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$C(l*0.6,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(45)$B(l*0.6,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"r1": 0.9, "r2": 0.6, "a0": 45, "a2": 45, "d": 137.5, "wr": 0.707},
        "angle": 45,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "ABOP Fig 2.6a - Excurrent/conifer SPIRAL (r1=0.9, r2=0.6)"
    },
    
    "honda_2_6b": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(45)B(l*0.9,w*0.707)]/(137.5)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$C(l*0.9,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(45)$B(l*0.9,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"r1": 0.9, "r2": 0.9, "a0": 45, "a2": 45, "d": 137.5, "wr": 0.707},
        "angle": 45,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "ABOP Fig 2.6b - Decurrent/deciduous SPIRAL (r1=0.9, r2=0.9)"
    },
    
    "honda_2_6c": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(45)B(l*0.8,w*0.707)]/(137.5)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$C(l*0.8,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(45)$B(l*0.8,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"r1": 0.9, "r2": 0.8, "a0": 45, "a2": 45, "d": 137.5, "wr": 0.707},
        "angle": 45,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "ABOP Fig 2.6c - Intermediate SPIRAL (r1=0.9, r2=0.8)"
    },
    
    "honda_2_6d": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(30)B(l*0.7,w*0.707)]/(137.5)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(-30)$C(l*0.7,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(-30)$B(l*0.7,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {"r1": 0.9, "r2": 0.7, "a0": 30, "a2": -30, "d": 137.5, "wr": 0.707},
        "angle": 30,
        "iterations": 10,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "ABOP Fig 2.6d - Narrow columnar SPIRAL (r1=0.9, r2=0.7)"
    },
    
    # =========================================================================
    # WHORLED Honda Variants - Multiple branches per level (NO spiral look)
    # These look more like traditional "tree" silhouettes
    # =========================================================================
    
    "honda_whorled_3": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(45)B(l*0.8,w*0.707)][/(120)&(45)B(l*0.8,w*0.707)][/(240)&(45)B(l*0.8,w*0.707)]/(45)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$C(l*0.8,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(45)$B(l*0.8,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 45,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Honda 3-WHORLED - 3 branches per level (no spiral) [BEST]"
    },
    
    "honda_whorled_4": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(50)B(l*0.75,w*0.707)][/(90)&(50)B(l*0.75,w*0.707)][/(180)&(50)B(l*0.75,w*0.707)][/(270)&(50)B(l*0.75,w*0.707)]/(45)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(40)$C(l*0.8,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(40)$B(l*0.8,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 45,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Honda 4-WHORLED - 4 branches per level, spreading crown"
    },
    
    "honda_whorled_5": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(35)B(l*0.7,w*0.707)][/(72)&(35)B(l*0.7,w*0.707)][/(144)&(35)B(l*0.7,w*0.707)][/(216)&(35)B(l*0.7,w*0.707)][/(288)&(35)B(l*0.7,w*0.707)]/(36)A(l*0.92,w*0.85)",
            "B(l,w) -> !(w)F(l)[-(30)$C(l*0.75,w*0.707)]C(l*0.85,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(30)$B(l*0.75,w*0.707)]B(l*0.85,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 35,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Honda 5-WHORLED - conifer/pine style with 5 branches per level"
    },
    
    "honda_whorled_full": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(55)B(l*0.9,w*0.707)][/(120)&(55)B(l*0.9,w*0.707)][/(240)&(55)B(l*0.9,w*0.707)]/(60)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(50)$C(l*0.9,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(50)$B(l*0.9,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 50,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Honda WHORLED FULL - very dense deciduous crown (r2=0.9) [BEST]"
    },
    
    # =========================================================================
    # Honda Variants with Tropism (for weeping/gravity effects)
    # =========================================================================
    
    "honda_weeping": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(50)B(l*0.8,w*0.707)]/(137.5)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$C(l*0.85,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(45)$B(l*0.85,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 45,
        "iterations": 10,
        "tropism_strength": 0.35,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Honda with strong gravity - weeping willow effect"
    },
    
    "honda_whorled_weeping": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(55)B(l*0.85,w*0.707)][/(120)&(55)B(l*0.85,w*0.707)][/(240)&(55)B(l*0.85,w*0.707)]/(60)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[-(45)$C(l*0.9,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) -> !(w)F(l)[+(45)$B(l*0.9,w*0.707)]B(l*0.9,w*0.707)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 50,
        "iterations": 8,
        "tropism_strength": 0.40,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Honda WHORLED WEEPING - full crown with gravity droop [BEST]"
    },
    
    "oak_param": {
        "type": "parametric",
        "axiom": "!(12)F(250)A(60,8)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(45)$B(l*0.65,w*0.707)][/(90)&(50)$B(l*0.65,w*0.707)][/(180)&(45)$B(l*0.65,w*0.707)][/(270)&(50)$B(l*0.65,w*0.707)]/(45)A(l*0.85,w*0.707)",
            "B(l,w) -> !(w)F(l)[+(35)$C(l*0.7,w*0.707)][-(35)$C(l*0.7,w*0.707)]/(137.5)B(l*0.8,w*0.707)",
            "C(l,w) : l > 5 -> !(w)F(l)[&(30)$C(l*0.6,w*0.707)]",
            "C(l,w) : l <= 5 -> !(w)F(l)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 35,
        "iterations": 7,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Oak - spreading crown with 4-way whorls (parametric)"
    },
    
    "elm_param": {
        "type": "parametric",
        "axiom": "!(12)F(300)A(55,9)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(55)$B(l*0.7,w*0.707)][/(90)&(60)$B(l*0.65,w*0.707)][/(180)&(55)$B(l*0.7,w*0.707)][/(270)&(60)$B(l*0.65,w*0.707)]/(60)A(l*0.9,w*0.707)",
            "B(l,w) -> !(w)F(l)[&(40)$C(l*0.65,w*0.707)][/(180)&(40)$C(l*0.65,w*0.707)]/(137.5)B(l*0.85,w*0.707)",
            "C(l,w) : l > 8 -> !(w)F(l)[&(35)$C(l*0.6,w*0.707)]",
            "C(l,w) : l <= 8 -> !(w)F(l)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 30,
        "iterations": 7,
        "tropism_strength": 0.10,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Elm - vase-shaped crown (parametric)"
    },
    
    "willow_param": {
        "type": "parametric",
        "axiom": "!(12)F(200)A(70,8)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(60)$B(l*0.8,w*0.707)][/(90)&(70)$B(l*0.75,w*0.707)][/(180)&(60)$B(l*0.8,w*0.707)][/(270)&(70)$B(l*0.75,w*0.707)]/(137.5)A(l*0.85,w*0.707)",
            "B(l,w) -> !(w)F(l)[&(40)$C(l*0.85,w*0.707)][/(180)&(40)$C(l*0.85,w*0.707)]C(l*0.9,w*0.707)",
            "C(l,w) : l > 5 -> !(w)F(l)C(l*0.95,w*0.8)",
            "C(l,w) : l <= 5 -> !(w)F(l)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 25,
        "iterations": 6,
        "tropism_strength": 0.45,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Willow - extreme droop with long trailing branches"
    },
    
    "pine_param": {
        "type": "parametric",
        "axiom": "!(12)F(250)/(45)A(40,8)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(25)$B(l*0.5,w*0.707)][/(72)&(25)$B(l*0.5,w*0.707)][/(144)&(25)$B(l*0.5,w*0.707)][/(216)&(25)$B(l*0.5,w*0.707)][/(288)&(25)$B(l*0.5,w*0.707)]/(137.5)A(l*0.95,w*0.85)",
            "B(l,w) -> !(w)F(l)[&(15)$C(l*0.7,w*0.707)]C(l*0.8,w*0.707)",
            "C(l,w) : l > 8 -> !(w)F(l)C(l*0.85,w*0.707)",
            "C(l,w) : l <= 8 -> !(w)F(l)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 25,
        "iterations": 8,
        "tropism_strength": 0.05,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Pine - 5-way whorled conical conifer"
    },
    
    "spruce_param": {
        "type": "parametric",
        "axiom": "!(14)F(300)/(45)A(35,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(30)$B(l*0.45,w*0.707)][/(60)&(30)$B(l*0.45,w*0.707)][/(120)&(30)$B(l*0.45,w*0.707)][/(180)&(30)$B(l*0.45,w*0.707)][/(240)&(30)$B(l*0.45,w*0.707)][/(300)&(30)$B(l*0.45,w*0.707)]/(137.5)A(l*0.92,w*0.9)",
            "B(l,w) -> !(w)F(l)[&(20)$C(l*0.6,w*0.707)]C(l*0.75,w*0.707)",
            "C(l,w) : l > 6 -> !(w)F(l)C(l*0.8,w*0.707)",
            "C(l,w) : l <= 6 -> !(w)F(l)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 20,
        "iterations": 9,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "render_polygons": False,
        "growth_mode": "sigmoid",
        "description": "Spruce - dense 6-way whorled Christmas tree shape"
    },
    
    "bonsai_param": {
        "type": "parametric",
        "axiom": "!(8)F(150)&(15)/(30)A(50,6)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(50)$B(l*0.55,w*0.707)][/(120)&(60)$B(l*0.5,w*0.707)]/(200)A(l*0.7,w*0.707)",
            "B(l,w) -> !(w)F(l)[+(40)$C(l*0.6,w*0.707)][-(50)$C(l*0.55,w*0.707)]",
            "C(l,w) : l > 10 -> !(w)F(l)[&(35)$C(l*0.5,w*0.707)]",
            "C(l,w) : l <= 10 -> !(w)F(l)"
        ],
        "rules": {"info": "Parametric - see 'productions'"},
        "constants": {},
        "angle": 35,
        "iterations": 7,
        "tropism_strength": 0.25,
        "tropism_direction": [0.2, -1, 0.1],
        "is_3d": True,
        "render_polygons": True,
        "growth_mode": "sigmoid",
        "description": "Bonsai - asymmetric artistic windswept style"
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
        "growth_mode": "sigmoid",
        "description": "ABOP p.28 - Stochastic L-system with variation"
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