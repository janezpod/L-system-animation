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
    "honda_realistic": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.707)F(50)[&(35)$B][/(137.5)&(35)$B][/(275)&(35)$B]/(137.5)A",
            "B": "!(0.707)F(40)[+(30)$CL][-(30)$CL]",
            "C": "!(0.707)F(30)L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 30,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.15,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Honda realistic conifer with tropism"
    },
    
    "honda_weeping": {
        "axiom": "!(1)F(200)A",
        "rules": {
            "A": "!(0.707)F(50)[&(45)$B][/(137.5)&(45)$B][/(275)&(45)$B]/(137.5)A",
            "B": "!(0.707)F(40)[+(35)$CL][-(35)$CL]",
            "C": "!(0.707)F(30)L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 30,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.35,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Honda weeping variant - strong droop"
    },
    
    # =========================================================================
    # Realistic Species Trees
    # Based on ABOP principles with species-specific characteristics
    # =========================================================================
    "oak_realistic": {
        "axiom": "!(1)F(250)A",
        "rules": {
            "A": "!(0.707)F(60)[&(45)$BL][/(90)&(50)$BL][/(180)&(45)$BL][/(270)&(50)$BL]/(45)A",
            "B": "!(0.707)F(50)[+(35)$CL][-(35)$CL]/(137.5)B",
            "C": "!(0.707)F(40)[&(30)$L]L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 35,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Oak - spreading crown with 4-way whorls"
    },
    
    "elm_realistic": {
        "axiom": "!(1)F(300)A",
        "rules": {
            "A": "!(0.707)F(55)[&(55)$BL][/(90)&(60)$BL][/(180)&(55)$BL][/(270)&(60)$BL]/(60)A",
            "B": "!(0.707)F(45)[&(40)$CL][/(180)&(40)$CL]/(137.5)B",
            "C": "!(0.707)F(35)[&(35)$L]L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 30,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.18,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Elm - vase-shaped with droop"
    },
    
    "willow_realistic": {
        "axiom": "!(1)F(350)A",
        "rules": {
            "A": "!(0.707)F(50)[&(60)$B][/(120)&(60)$B][/(240)&(60)$B]/(45)A",
            "B": "!(0.75)F(45)[&(50)$C]/(137.5)B",
            "C": "!(0.8)F(40)[&(45)$C]/(137.5)C",
            "L": "['''&&&{-f+f}]"
        },
        "angle": 25,
        "iterations": 6,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.45,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Willow - extreme droop, cascading [BEST WEEPING]"
    },
    
    "pine_realistic": {
        "axiom": "!(1)F(400)A",
        "rules": {
            "A": "!(0.85)F(40)[&(70)$B][/(72)&(70)$B][/(144)&(70)$B][/(216)&(70)$B][/(288)&(70)$B]/(36)A",
            "B": "!(0.80)F(60)[&(15)$C][/(180)&(15)$C]",
            "C": "!(0.75)F(50)",
            "L": "['''&&&{-f+f}]"
        },
        "angle": 20,
        "iterations": 8,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.05,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Pine - 5-way whorled branches, conical"
    },
    
    "spruce_realistic": {
        "axiom": "!(1)F(450)A",
        "rules": {
            "A": "!(0.88)F(35)[&(75)$B][/(72)&(75)$B][/(144)&(75)$B][/(216)&(75)$B][/(288)&(75)$B]/(36)A",
            "B": "!(0.82)F(55)[&(10)$C][/(120)&(10)$C][/(240)&(10)$C]",
            "C": "!(0.78)F(45)",
            "L": "['''&&&{-f+f}]"
        },
        "angle": 18,
        "iterations": 9,
        "is_3d": True,
        "render_polygons": False,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "growth_mode": "sigmoid",
        "description": "Spruce - dense whorled conifer"
    },
    
    "bonsai_realistic": {
        "axiom": "!(1)F(150)&(10)A",
        "rules": {
            "A": "!(0.65)F(40)[&(50)$BL][/(100)&(35)$BL]/(160)A",
            "B": "!(0.65)F(35)[+(40)$CL][-(50)$CL]",
            "C": "!(0.65)F(25)L",
            "L": "['''&&&{-f+f+f-|-f+f+f}]"
        },
        "angle": 40,
        "iterations": 7,
        "is_3d": True,
        "render_polygons": True,
        "tropism_strength": 0.20,
        "tropism_direction": [0, -1, 0.2],
        "growth_mode": "sigmoid",
        "description": "Bonsai - asymmetric artistic form"
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