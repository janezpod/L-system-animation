"""
L-System Plant Presets - Complete Integrated Version

Includes:
- Original presets
- NEW: 60+ presets from Lsystems.pdf and ABOP book

Based on:
- "The Algorithmic Beauty of Plants" (Prusinkiewicz & Lindenmayer)
- Lsystems.pdf (Houdini L-Systems Tutorial)
- Vogel's formula for phyllotaxis
- Honda/Borchert tree models
"""

from typing import Dict, Any, List

# =============================================================================
# 2D PRESETS
# =============================================================================

PRESETS_2D: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # ABOP Figure 1.24 - The Classic Collection
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
        "axiom": "FX",
        "rules": {
            "X": "F[++X][+X][-X][--X]",
            "F": "FF"
        },
        "angle": 35,
        "iterations": 5,
        "base_width": 1.8,
        "description": "Oak - wide spreading crown"
    },
    "tree_willow_weeping": {
        "axiom": "FFFFA",
        "rules": {
            "A": "[+B][-B]A",
            "B": "F[+F[+F]][-F[-F]]"
        },
        "angle": 25,
        "iterations": 6,
        "base_width": 1.5,
        "description": "Willow - cascading branches"
    },
    "tree_poplar_columnar": {
        "axiom": "FA",
        "rules": {
            "A": "F[+B][-B]FA",
            "B": "F[+F][-F]"
        },
        "angle": 12,
        "iterations": 7,
        "base_width": 1.3,
        "description": "Poplar - tall columnar shape"
    },
    "tree_elm_vase": {
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
    # FERNS
    # =========================================================================
    "fern_frond": {
        "axiom": "X",
        "rules": {
            "X": "F[+P]F[-P]X",
            "P": "F[+F][-F]F",
            "F": "F"
        },
        "angle": 45,
        "iterations": 7,
        "base_width": 0.8,
        "description": "Fern - realistic frond with pinnae"
    },
    "fern_fractal": {
        "axiom": "X",
        "rules": {
            "X": "F+[[X]-X]-F[-FX]+X",
            "F": "FF"
        },
        "angle": 25,
        "iterations": 6,
        "base_width": 1.0,
        "description": "Fractal fern pattern"
    },

    # =========================================================================
    # ARTISTIC / FRACTALS (original)
    # =========================================================================
    "dragon_curve": {
        "axiom": "FX",
        "rules": {"X": "X+YF+", "Y": "-FX-Y"},
        "angle": 90,
        "iterations": 12,
        "base_width": 1.0,
        "description": "Dragon curve fractal"
    },
    "koch_snowflake": {
        "axiom": "F++F++F",
        "rules": {"F": "F-F++F-F"},
        "angle": 60,
        "iterations": 4,
        "base_width": 1.0,
        "description": "Koch snowflake"
    },
    "sierpinski": {
        "axiom": "F-G-G",
        "rules": {"F": "F-G+F+G-F", "G": "GG"},
        "angle": 120,
        "iterations": 6,
        "base_width": 1.0,
        "description": "Sierpinski triangle"
    },
    
    # =========================================================================
    # NEW FROM PDF: Koch Curve Variants
    # =========================================================================
    "quadratic_koch": {
        "axiom": "F-F-F-F",
        "rules": {"F": "F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"},
        "angle": 90,
        "iterations": 2,
        "description": "Quadratic Koch curve - ABOP p9",
        "category": "fractals"
    },
    
    "quadratic_snowflake": {
        "axiom": "-F",
        "rules": {"F": "F+F-F-F+F"},
        "angle": 90,
        "iterations": 4,
        "description": "Quadratic snowflake fractal",
        "category": "fractals"
    },
    
    "koch_curve_a": {
        "axiom": "F-F-F-F",
        "rules": {"F": "FF-F-F-F-F-F+F"},
        "angle": 90,
        "iterations": 4,
        "description": "Koch curve variant a - closed island",
        "category": "fractals"
    },
    
    "koch_curve_b": {
        "axiom": "F-F-F-F",
        "rules": {"F": "FF-F-F-F-FF"},
        "angle": 90,
        "iterations": 4,
        "description": "Koch curve variant b - square fill pattern",
        "category": "fractals"
    },
    
    "koch_curve_c": {
        "axiom": "F-F-F-F",
        "rules": {"F": "FF-F+F-F-FF"},
        "angle": 90,
        "iterations": 3,
        "description": "Koch curve variant c",
        "category": "fractals"
    },
    
    "koch_curve_d": {
        "axiom": "F-F-F-F",
        "rules": {"F": "FF-F--F-F"},
        "angle": 90,
        "iterations": 3,
        "description": "Koch curve variant d",
        "category": "fractals"
    },
    
    "koch_curve_e": {
        "axiom": "F-F-F-F",
        "rules": {"F": "F-FF--F-F"},
        "angle": 90,
        "iterations": 5,
        "description": "Koch curve variant e - dragon-like",
        "category": "fractals"
    },
    
    "koch_curve_f": {
        "axiom": "F-F-F-F",
        "rules": {"F": "F-F+F-F-F"},
        "angle": 90,
        "iterations": 5,
        "description": "Koch curve variant f - dense fill",
        "category": "fractals"
    },
    
    # =========================================================================
    # NEW FROM PDF: Diamond and Space-Filling Curves
    # =========================================================================
    "diamond_fractal": {
        "axiom": "F",
        "rules": {"F": "FF++F++F++F-F"},
        "angle": 60,
        "iterations": 4,
        "description": "Diamond-shaped recursive fractal",
        "category": "fractals"
    },
    
    "hilbert_curve": {
        "axiom": "A",
        "rules": {
            "A": "-BF+AFA+FB-",
            "B": "+AF-BFB-FA+"
        },
        "angle": 90,
        "iterations": 5,
        "description": "Hilbert space-filling curve",
        "category": "fractals"
    },
    
    "peano_curve": {
        "axiom": "F",
        "rules": {"F": "F+F-F-F-F+F+F+F-F"},
        "angle": 90,
        "iterations": 3,
        "description": "Peano space-filling curve",
        "category": "fractals"
    },
    
    "gosper_curve": {
        "axiom": "A",
        "rules": {
            "A": "A-B--B+A++AA+B-",
            "B": "+A-BB--B-A++A+B"
        },
        "angle": 60,
        "iterations": 4,
        "description": "Gosper curve (flowsnake) - hexagonal space filler",
        "category": "fractals"
    },
    
    "sierpinski_arrowhead": {
        "axiom": "A",
        "rules": {"A": "B-A-B", "B": "A+B+A"},
        "angle": 60,
        "iterations": 7,
        "description": "Sierpinski arrowhead curve",
        "category": "fractals"
    },
    
    # =========================================================================
    # NEW FROM PDF: ABOP Plants (alternative naming)
    # =========================================================================
    "abop_plant_a": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": 25.7,
        "iterations": 4,
        "base_width": 1.5,
        "description": "ABOP 1.24a - edge-rewriting plant",
        "category": "abop_plants"
    },
    
    "abop_plant_b": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F][F]"},
        "angle": 20,
        "iterations": 5,
        "base_width": 1.5,
        "description": "ABOP 1.24b - three-branch variant",
        "category": "abop_plants"
    },
    
    "abop_plant_c": {
        "axiom": "F",
        "rules": {"F": "FF-[-F+F+F]+[+F-F-F]"},
        "angle": 22.5,
        "iterations": 4,
        "base_width": 1.5,
        "description": "ABOP 1.24c - symmetrical branching",
        "category": "abop_plants"
    },
    
    "abop_plant_d": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 20,
        "iterations": 7,
        "base_width": 1.2,
        "description": "ABOP 1.24d - node-rewriting",
        "category": "abop_plants"
    },
    
    "abop_plant_e": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]FX", "F": "FF"},
        "angle": 25.7,
        "iterations": 7,
        "base_width": 1.2,
        "description": "ABOP 1.24e - node-rewriting with wider angle",
        "category": "abop_plants"
    },
    
    "abop_plant_f": {
        "axiom": "X",
        "rules": {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        "angle": 22.5,
        "iterations": 5,
        "base_width": 1.2,
        "description": "ABOP 1.24f - elegant plant (ICONIC!)",
        "category": "abop_plants"
    },
    
    # =========================================================================
    # NEW FROM PDF: Polygon Leaves (2D)
    # =========================================================================
    "leaf_cordate": {
        "axiom": "[A][B]",
        "rules": {
            "A": "[+A{.].C.}",
            "B": "[-B{.].C.}",
            "C": "FFFC"
        },
        "angle": 16,
        "iterations": 12,
        "render_polygons": True,
        "description": "ABOP Fig 5.5 - Cordate (heart-shaped) leaf",
        "category": "leaves"
    },
    
    "leaf_triangle": {
        "axiom": "{.+F.-F.-F.}",
        "rules": {},
        "angle": 120,
        "iterations": 1,
        "render_polygons": True,
        "description": "Simple triangular leaf",
        "category": "leaves"
    },
    
    "leaf_hexagon": {
        "axiom": "{.+F.+F.+F.+F.+F.+F.}",
        "rules": {},
        "angle": 60,
        "iterations": 1,
        "render_polygons": True,
        "description": "Hexagonal leaf shape",
        "category": "leaves"
    },
}


# =============================================================================
# 3D PRESETS - Enhanced with camera hints
# =============================================================================

PRESETS_3D: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # ABOP 3D - Polygon Leaves and Flowers
    # =========================================================================
    "abop_1_25": {
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
        "axiom": "P",
        "rules": {
            "P": "I+[P+W]--//[--L]I[++L]-[PW]++PW",
            "I": "FS[//&&L][//^^L]FS",
            "S": "SFS",
            "L": "['{+f-ff-f+|+f-ff-f}]",
            "W": "[&&&'''K'/W////W////W////W////W]",
            "K": "FF",
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
    # SUNFLOWER - FIXED! Dense golden spiral
    # =========================================================================
    "sunflower_head": {
        "axiom": "".join(["[/(137.5)&'F]" for _ in range(200)]),
        "rules": {},
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 1,
        "base_width": 0.3,
        "width_decay": 0.995,
        "length_decay": 0.997,
        "description": "Sunflower - 200 florets golden spiral (VIEW FROM ABOVE!)"
    },
    
    "sunflower_3d_bowl": {
        "axiom": "A",
        "rules": {
            "A": "/(137.5)[&&&'F]A",
        },
        "angle": 25,
        "roll_angle": 137.5,
        "iterations": 150,
        "base_width": 0.4,
        "width_decay": 0.997,
        "length_decay": 0.998,
        "description": "Sunflower bowl - visible from side and above"
    },
    
    # =========================================================================
    # PHYLLOTAXIS - FIXED! 3D spiral visible from any angle
    # =========================================================================
    "phyllotaxis_bowl": {
        "axiom": "A",
        "rules": {
            "A": "F/(137.5)[&&L]A",
            "L": "[++F][--F][+F][-F]F"
        },
        "angle": 35,
        "roll_angle": 137.5,
        "iterations": 50,
        "base_width": 0.8,
        "width_decay": 0.99,
        "length_decay": 0.98,
        "description": "Phyllotaxis - golden angle spiral dome"
    },
    
    "succulent_rosette": {
        "axiom": "A",
        "rules": {
            "A": "/(137.5)[&&&F'L]!A",
            "L": "{+f-f-f+|+f-f-f}"
        },
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 40,
        "base_width": 0.5,
        "width_decay": 0.995,
        "render_polygons": True,
        "description": "Phyllotaxis - succulent rosette pattern"
    },
    
    # =========================================================================
    # PALM - FIXED! True pinnate fronds with leaflets
    # =========================================================================
    "palm_3d": {
        "axiom": "TTTTTTTTTT" + "".join([f"[/({36*i})P]" for i in range(10)]),
        "rules": {
            "T": "F",
            "P": "&&&RRRRRRRRRRRRR",
            "R": "F[++L][+L][-L][--L]/",
            "L": "''FF"
        },
        "angle": 20,
        "roll_angle": 36,
        "iterations": 2,
        "base_width": 3.0,
        "width_decay": 0.6,
        "length_decay": 0.9,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "description": "Palm - 10 pinnate fronds with leaflets"
    },
    
    "bamboo_3d": {
        "axiom": "FA",
        "rules": {
            "A": "F[&&L][&&-L][&&+L]/(90)FA",
            "L": "F[+F][-F]"
        },
        "angle": 30,
        "roll_angle": 90,
        "iterations": 12,
        "base_width": 1.2,
        "width_decay": 0.95,
        "description": "Bamboo - segmented culm with branches"
    },

    # =========================================================================
    # TREES - Natural asymmetric shapes
    # =========================================================================
    "tree_3d_oak": {
        "axiom": "FFFFA",
        "rules": {
            "A": "[&&B]/(94)[&&C]/(87)[&&B]/(101)[&&C]",
            "B": "FFF[++D][+E][-E][--D]",
            "C": "FF[+D][-D]",
            "D": "F[+D][-D]",
            "E": "FF[++F][--F]"
        },
        "angle": 35,
        "roll_angle": 90,
        "iterations": 5,
        "base_width": 2.5,
        "width_decay": 0.68,
        "length_decay": 0.72,
        "description": "Oak - wide asymmetric crown"
    },
    
    "tree_3d_pine": {
        "axiom": "FA",
        "rules": {
            "A": "F[&&&W]/(90)[&&&W]/(90)[&&&W]/(90)[&&&W]A",
            "W": "F[+F][-F]F"
        },
        "angle": 25,
        "roll_angle": 90,
        "iterations": 8,
        "base_width": 1.8,
        "width_decay": 0.75,
        "length_decay": 0.9,
        "tropism_strength": 0.08,
        "tropism_direction": [0, -1, 0],
        "description": "Pine - conical with whorled branches"
    },
    
    "tree_3d_birch": {
        "axiom": "FXFXFXFXFXFXFX",
        "rules": {
            "X": "[/&B][//&B][///&B]",
            "B": "FFFF[^F[^F]][-F[-F]]"
        },
        "angle": 28,
        "roll_angle": 120,
        "iterations": 4,
        "base_width": 1.5,
        "width_decay": 0.62,
        "length_decay": 0.82,
        "tropism_strength": -0.06,
        "tropism_direction": [0, 1, 0],
        "description": "Birch - graceful upswept branches"
    },
    
    "tree_3d_willow": {
        "axiom": "FFFXFXFXFXFX",
        "rules": {
            "X": "[/&&B][//&&B][///&&B][////&&B]",
            "B": "FF[&F[&F[&F[&F[&F]]]]]"
        },
        "angle": 50,
        "roll_angle": 90,
        "iterations": 4,
        "base_width": 2.0,
        "width_decay": 0.72,
        "length_decay": 0.85,
        "tropism_strength": 0.25,
        "tropism_direction": [0, -1, 0],
        "description": "Willow - weeping cascading branches"
    },
    
    "tree_3d_maple": {
        "axiom": "FFFFA",
        "rules": {
            "A": "[&+B][&-B]//[&+C][&-C]FA",
            "B": "FF[+D][-D]",
            "C": "F[+D][-D]",
            "D": "F[+D][-D]"
        },
        "angle": 40,
        "roll_angle": 90,
        "iterations": 5,
        "base_width": 2.2,
        "width_decay": 0.70,
        "length_decay": 0.78,
        "description": "Maple - opposite decussate branches"
    },
    
    "tree_3d_cypress": {
        "axiom": "FXFXFXFXFXFXFXFXFXFXFXFXFX",
        "rules": {
            "X": "[/&B][//&B][///&B][////&B]",
            "B": "F[+F][-F]"
        },
        "angle": 15,
        "roll_angle": 90,
        "iterations": 3,
        "base_width": 1.5,
        "width_decay": 0.8,
        "length_decay": 0.9,
        "description": "Cypress - narrow columnar shape"
    },
    
    "honda_tree": {
        "axiom": "A",
        "rules": {
            "A": "!(1.0)F(50)[&(a0)B]/(d)[&(a1)B]",
            "B": "!(0.707)F(50)[+(a0)$C]/(d)[-(a1)$C]",
            "C": "!(0.707)F(50)[&(a0)B]/(d)[&(a1)B]"
        },
        "constants": {"a0": 45, "a1": 45, "d": 137.5},
        "angle": 45,
        "roll_angle": 137.5,
        "iterations": 10,
        "base_width": 2.0,
        "width_decay": 0.707,
        "description": "Honda tree - mathematical model"
    },

    # =========================================================================
    # FERNS 3D
    # =========================================================================
    "fern_3d_frond": {
        "axiom": "X",
        "rules": {
            "X": "F[&&P]/(90)[&&P]/(90)[&&P]/(90)[&&P]X",
            "P": "F[+F][-F]F"
        },
        "angle": 35,
        "roll_angle": 90,
        "iterations": 6,
        "base_width": 0.8,
        "width_decay": 0.75,
        "description": "3D fern frond"
    },
    
    "fern_3d_spiral": {
        "axiom": "A",
        "rules": {
            "A": "F[&&L]/(137.5)A",
            "L": "[+F][-F]F"
        },
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 30,
        "base_width": 0.6,
        "width_decay": 0.98,
        "description": "Spiral fern"
    },

    # =========================================================================
    # ARTISTIC
    # =========================================================================
    "spiral_vine": {
        "axiom": "FA",
        "rules": {
            "A": "F[&&&'L]/(137.5)!A",
            "L": "[++F][--F][+++F][---F]"
        },
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 80,
        "base_width": 1.2,
        "width_decay": 0.993,
        "length_decay": 0.995,
        "description": "Spiral vine - golden angle helix"
    },
    
    "coral_branch": {
        "axiom": "A",
        "rules": {
            "A": "F[&B]/(90)[&B]/(90)[&B]/(90)[&B]A",
            "B": "F[+B][-B]"
        },
        "angle": 30,
        "roll_angle": 90,
        "iterations": 5,
        "base_width": 1.5,
        "width_decay": 0.75,
        "description": "Coral-like branching"
    },
    
    "crystal_growth": {
        "axiom": "F",
        "rules": {
            "F": "F[+F][-F][&F][^F]"
        },
        "angle": 90,
        "roll_angle": 90,
        "iterations": 4,
        "base_width": 1.0,
        "width_decay": 0.7,
        "description": "Crystal-like orthogonal growth"
    },
    
    # =========================================================================
    # NEW FROM PDF: Simple 3D Tree
    # =========================================================================
    "tree_3d_simple": {
        "axiom": "FFFA",
        "rules": {
            "A": "[B]////[B]////[B]",
            "B": "&FFFA"
        },
        "angle": 28,
        "roll_angle": 72,
        "iterations": 5,
        "base_width": 2.0,
        "width_decay": 0.7,
        "description": "Simple 3D tree with 3-branch whorls",
        "category": "3d_trees"
    },
    
    # =========================================================================
    # NEW FROM PDF: Trees with Gravity/Tropism
    # =========================================================================
    "tree_gravity_none": {
        "axiom": "FA",
        "rules": {
            "A": 'T"[&FA]////[&FA]'
        },
        "angle": 45,
        "roll_angle": 72,
        "iterations": 10,
        "base_width": 2.0,
        "width_decay": 0.6,
        "length_decay": 0.6,
        "tropism_strength": 0.0,
        "tropism_direction": [0, -1, 0],
        "description": "Symmetric tree without gravity",
        "category": "3d_trees"
    },
    
    "tree_gravity_moderate": {
        "axiom": "FA",
        "rules": {
            "A": 'T"[&FA]////[&FA]'
        },
        "angle": 45,
        "roll_angle": 72,
        "iterations": 10,
        "base_width": 2.0,
        "width_decay": 0.6,
        "length_decay": 0.6,
        "tropism_strength": 0.2,
        "tropism_direction": [0, -1, 0],
        "description": "Tree with moderate gravity drooping",
        "category": "3d_trees"
    },
    
    "tree_gravity_strong": {
        "axiom": "FA",
        "rules": {
            "A": 'T"[&FA]////[&FA]'
        },
        "angle": 45,
        "roll_angle": 72,
        "iterations": 10,
        "base_width": 2.0,
        "width_decay": 0.6,
        "length_decay": 0.6,
        "tropism_strength": 0.5,
        "tropism_direction": [0, -1, 0],
        "description": "Weeping tree with strong gravity",
        "category": "3d_trees"
    },
    
    # =========================================================================
    # NEW FROM PDF: Tree with Leaves and Berries
    # =========================================================================
    "tree_leaves_berries": {
        "axiom": "FFFA",
        "rules": {
            "A": '!"[&&J][B]////[&&J][B]////[&&J]B',
            "B": "&FFFAK"
        },
        "angle": 28,
        "roll_angle": 72,
        "iterations": 5,
        "base_width": 2.5,
        "width_decay": 0.7,
        "render_polygons": True,
        "description": "Tree with polygon leaves (J) and berries (K)",
        "category": "3d_trees"
    },
    
    # =========================================================================
    # NEW FROM PDF: Bush with leaves
    # =========================================================================
    "bush_3d_with_leaves": {
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
        "description": "3D bush with polygon leaves",
        "category": "3d_trees"
    },
    
    # =========================================================================
    # NEW FROM PDF: Spiral patterns
    # =========================================================================
    "spiral_3d_helix": {
        "axiom": "A",
        "rules": {
            "A": "F/(137.5)[&&L]A",
            "L": "[+F][-F]F"
        },
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 50,
        "base_width": 0.6,
        "width_decay": 0.98,
        "description": "3D golden angle helix",
        "category": "spirals"
    },
    
    "spiral_tower": {
        "axiom": "FA",
        "rules": {
            "A": "F[&&&'L]/(137.5)!A",
            "L": "[++F][--F][+++F][---F]"
        },
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 80,
        "base_width": 1.2,
        "width_decay": 0.993,
        "length_decay": 0.995,
        "description": "Spiral vine tower - golden angle helix",
        "category": "spirals"
    },
}


# =============================================================================
# BACKWARD COMPATIBILITY
# =============================================================================

PRESETS = PRESETS_2D


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_preset(name: str, include_3d: bool = True) -> Dict[str, Any]:
    """Get a preset by name, searching both 2D and 3D collections."""
    name_lower = name.lower()
    
    if name_lower in PRESETS_2D:
        return PRESETS_2D[name_lower].copy()
    
    if include_3d and name_lower in PRESETS_3D:
        preset = PRESETS_3D[name_lower].copy()
        preset['is_3d'] = True
        return preset
    
    # Also check parametric presets
    if name_lower in PARAMETRIC_PRESETS:
        preset = PARAMETRIC_PRESETS[name_lower].copy()
        preset['is_parametric'] = True
        return preset
    
    all_presets = list(PRESETS_2D.keys())
    if include_3d:
        all_presets.extend(PRESETS_3D.keys())
    all_presets.extend(PARAMETRIC_PRESETS.keys())
    available = ', '.join(sorted(all_presets))
    raise KeyError(f"Unknown preset '{name}'. Available presets: {available}")


def list_presets(include_3d: bool = False) -> List[str]:
    """List all available preset names."""
    presets = list(PRESETS_2D.keys())
    if include_3d:
        presets.extend(PRESETS_3D.keys())
    return sorted(presets)


def is_3d_preset(name: str) -> bool:
    """Check if a preset is 3D."""
    return name.lower() in PRESETS_3D


def list_presets_by_category() -> Dict[str, List[str]]:
    """List presets organized by category."""
    return {
        "2D ABOP Classics": ["abop_1_24a", "abop_1_24b", "abop_1_24c",
                            "abop_1_24d", "abop_1_24e", "abop_1_24f"],
        "2D ABOP Plants (alt)": ["abop_plant_a", "abop_plant_b", "abop_plant_c",
                                 "abop_plant_d", "abop_plant_e", "abop_plant_f"],
        "2D Trees": ["tree_oak_spreading", "tree_willow_weeping", 
                     "tree_poplar_columnar", "tree_elm_vase"],
        "2D Ferns": ["fern_frond", "fern_fractal"],
        "2D Fractals": ["dragon_curve", "koch_snowflake", "sierpinski",
                       "quadratic_koch", "quadratic_snowflake",
                       "koch_curve_a", "koch_curve_b", "koch_curve_c",
                       "koch_curve_d", "koch_curve_e", "koch_curve_f",
                       "diamond_fractal", "hilbert_curve", "peano_curve",
                       "gosper_curve", "sierpinski_arrowhead"],
        "2D Leaves": ["leaf_cordate", "leaf_triangle", "leaf_hexagon"],
        "3D ABOP Figures": ["abop_1_25", "abop_1_26"],
        "3D Trees": ["tree_3d_oak", "tree_3d_pine", "tree_3d_birch",
                     "tree_3d_maple", "tree_3d_willow", "tree_3d_cypress",
                     "honda_tree", "tree_3d_simple"],
        "3D Trees (Tropism)": ["tree_gravity_none", "tree_gravity_moderate",
                               "tree_gravity_strong", "tree_leaves_berries"],
        "3D Tropical": ["palm_3d", "bamboo_3d"],
        "3D Phyllotaxis": ["phyllotaxis_bowl", "sunflower_head", 
                          "sunflower_3d_bowl", "succulent_rosette"],
        "3D Ferns": ["fern_3d_frond", "fern_3d_spiral"],
        "3D Spirals": ["spiral_vine", "spiral_3d_helix", "spiral_tower"],
        "3D Artistic": ["coral_branch", "crystal_growth", "bush_3d_with_leaves"],
        "Parametric Trees": ["monopodial_tree", "monopodial_tree_narrow",
                            "monopodial_tree_spreading", "sympodial_tree",
                            "sympodial_tree_weeping", "sympodial_tree_upright",
                            "ternary_tree", "ternary_tree_golden", "ternary_tree_dense"],
        "Parametric Stochastic": ["stochastic_plant", "stochastic_tree", 
                                  "stochastic_bush", "stochastic_bush_abop"],
        "Parametric Ferns": ["fern_simple", "fern_delayed", "fern_complex",
                            "compound_leaf_alternate", "compound_leaf_complex"],
    }


# =============================================================================
# PARAMETRIC PRESETS - For advanced L-system features
# =============================================================================

PARAMETRIC_PRESETS: Dict[str, Dict[str, Any]] = {
    # Original parametric presets
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
    
    # =========================================================================
    # NEW FROM PDF: Monopodial Tree (ABOP Figure 2.6)
    # =========================================================================
    "monopodial_tree": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(c)B(l*e,w*h)]/(m)A(l*b,w*h)",
            "B(l,w) -> !(w)F(l)[-(d)$C(l*e,w*h)]C(l*b,w*h)",
            "C(l,w) -> !(w)F(l)[+(d)$B(l*e,w*h)]B(l*b,w*h)"
        ],
        "constants": {
            "b": 0.9,
            "e": 0.6,
            "c": 45,
            "d": 45,
            "h": 0.707,
            "m": 137.5
        },
        "angle": 45,
        "iterations": 10,
        "is_3d": True,
        "description": "ABOP Fig 2.6 - Monopodial tree",
        "category": "parametric_trees"
    },
    
    "monopodial_tree_narrow": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(c)B(l*e,w*h)]/(m)A(l*b,w*h)",
            "B(l,w) -> !(w)F(l)[-(d)$C(l*e,w*h)]C(l*b,w*h)",
            "C(l,w) -> !(w)F(l)[+(d)$B(l*e,w*h)]B(l*b,w*h)"
        ],
        "constants": {
            "b": 0.9, "e": 0.9, "c": 45, "d": 50.6,
            "h": 0.707, "m": 137.5
        },
        "iterations": 10,
        "is_3d": True,
        "description": "Monopodial tree - narrow crown variant",
        "category": "parametric_trees"
    },
    
    "monopodial_tree_spreading": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(c)B(l*e,w*h)]/(m)A(l*b,w*h)",
            "B(l,w) -> !(w)F(l)[-(d)$C(l*e,w*h)]C(l*b,w*h)",
            "C(l,w) -> !(w)F(l)[+(d)$B(l*e,w*h)]B(l*b,w*h)"
        ],
        "constants": {
            "b": 0.9, "e": 0.7, "c": 30, "d": -30,
            "h": 0.707, "m": 137.5
        },
        "iterations": 10,
        "is_3d": True,
        "description": "Monopodial tree - spreading crown variant",
        "category": "parametric_trees"
    },
    
    # =========================================================================
    # NEW FROM PDF: Sympodial Tree (ABOP Figure 2.7)
    # =========================================================================
    "sympodial_tree": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(c)B(l*b,w*h)]/(180)[&(d)B(l*e,w*h)]",
            "B(l,w) -> !(w)F(l)[+(c)$B(l*b,w*h)][-(d)$B(l*e,w*h)]"
        ],
        "constants": {
            "b": 0.9,
            "e": 0.7,
            "c": 5,
            "d": 65,
            "h": 0.707
        },
        "angle": 45,
        "iterations": 10,
        "is_3d": True,
        "description": "ABOP Fig 2.7 - Sympodial tree",
        "category": "parametric_trees"
    },
    
    "sympodial_tree_weeping": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(c)B(l*b,w*h)]/(180)[&(d)B(l*e,w*h)]",
            "B(l,w) -> !(w)F(l)[+(c)$B(l*b,w*h)][-(d)$B(l*e,w*h)]"
        ],
        "constants": {
            "b": 0.9, "e": 0.7, "c": 10, "d": 60, "h": 0.707
        },
        "iterations": 10,
        "is_3d": True,
        "description": "Sympodial tree - weeping form",
        "category": "parametric_trees"
    },
    
    "sympodial_tree_upright": {
        "type": "parametric",
        "axiom": "A(1,10)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&(c)B(l*b,w*h)]/(180)[&(d)B(l*e,w*h)]",
            "B(l,w) -> !(w)F(l)[+(c)$B(l*b,w*h)][-(d)$B(l*e,w*h)]"
        ],
        "constants": {
            "b": 0.9, "e": 0.8, "c": 20, "d": 50, "h": 0.707
        },
        "iterations": 10,
        "is_3d": True,
        "description": "Sympodial tree - upright form",
        "category": "parametric_trees"
    },
    
    # =========================================================================
    # NEW FROM PDF: Ternary Tree (ABOP Figure 2.8)
    # =========================================================================
    "ternary_tree": {
        "type": "parametric",
        "axiom": "F(0.5,1)A",
        "productions": [
            "A -> F(0.5,1)[&(c)F(0.5,1)A]/(b)[&(c)F(0.5,1)A]/(e)[&(c)F(0.5,1)A]",
            "F(l,w) -> F(l*d,w*h)"
        ],
        "constants": {
            "b": 94.64,
            "e": 132.63,
            "c": 18.95,
            "d": 1.109,
            "h": 1.732
        },
        "angle": 20,
        "iterations": 8,
        "tropism_strength": 0.15,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "description": "ABOP Fig 2.8 - Ternary tree with tropism",
        "category": "parametric_trees"
    },
    
    "ternary_tree_golden": {
        "type": "parametric",
        "axiom": "F(0.5,1)A",
        "productions": [
            "A -> F(0.5,1)[&(c)F(0.5,1)A]/(b)[&(c)F(0.5,1)A]/(e)[&(c)F(0.5,1)A]",
            "F(l,w) -> F(l*d,w*h)"
        ],
        "constants": {
            "b": 137.5, "e": 137.5,
            "c": 18.95, "d": 1.109, "h": 1.452
        },
        "iterations": 8,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "description": "Ternary tree with golden angle divergence",
        "category": "parametric_trees"
    },
    
    "ternary_tree_dense": {
        "type": "parametric",
        "axiom": "F(0.5,1)A",
        "productions": [
            "A -> F(0.5,1)[&(c)F(0.5,1)A]/(b)[&(c)F(0.5,1)A]/(e)[&(c)F(0.5,1)A]",
            "F(l,w) -> F(l*d,w*h)"
        ],
        "constants": {
            "b": 112.5, "e": 157.5,
            "c": 22.5, "d": 1.079, "h": 1.653
        },
        "iterations": 8,
        "tropism_strength": 0.21,
        "tropism_direction": [0, -1, 0],
        "is_3d": True,
        "description": "Ternary tree - dense variant",
        "category": "parametric_trees"
    },
    
    # =========================================================================
    # NEW FROM PDF: Stochastic L-Systems
    # =========================================================================
    "stochastic_plant": {
        "type": "parametric",
        "axiom": "F",
        "productions": [
            {"rule": "F -> F[-F]F[+F]F", "probability": 0.33},
            {"rule": "F -> F[-F]F", "probability": 0.33},
            {"rule": "F -> F[+F]F", "probability": 0.34}
        ],
        "angle": 28,
        "iterations": 6,
        "description": "ABOP p.28 - Stochastic L-system",
        "category": "stochastic"
    },
    
    "stochastic_bush": {
        "type": "parametric",
        "axiom": "F",
        "productions": [
            {"rule": "F -> FF-[-F+F+F]+[+F-F-F]", "probability": 0.5},
            {"rule": "F -> FF-[-F+F]+[+F-F]", "probability": 0.3},
            {"rule": "F -> F[+F][-F]", "probability": 0.2}
        ],
        "angle": 22.5,
        "iterations": 4,
        "description": "Stochastic bush with varied branching",
        "category": "stochastic"
    },
    
    # =========================================================================
    # NEW FROM PDF: Ferns (ABOP Chapter 5)
    # =========================================================================
    "fern_simple": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(i) : i > 0 -> A(i-1)",
            "A(i) : i == 0 -> F(1)[+A(b)][-A(b)]F(1)A(0)",
            "F(a) -> F(a*c)"
        ],
        "constants": {
            "b": 0,
            "c": 2
        },
        "angle": 45,
        "iterations": 9,
        "description": "Simple pinnate fern",
        "category": "ferns"
    },
    
    "fern_delayed": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(i) : i > 0 -> A(i-1)",
            "A(i) : i == 0 -> F(1)[+A(b)][-A(b)]F(1)A(0)",
            "F(a) -> F(a*c)"
        ],
        "constants": {"b": 2, "c": 1.36},
        "angle": 45,
        "iterations": 18,
        "description": "Fern with apical delay",
        "category": "ferns"
    },
    
    "fern_complex": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(i) : i > 0 -> A(i-1)",
            "A(i) : i == 0 -> F(1)[+A(b)][-A(b)]F(1)A(0)",
            "F(a) -> F(a*c)"
        ],
        "constants": {"b": 7, "c": 1.17},
        "angle": 45,
        "iterations": 30,
        "description": "Complex fern with high delay",
        "category": "ferns"
    },
    
    "compound_leaf_alternate": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(i) : i > 0 -> A(i-1)",
            "A(i) : i == 0 -> F(1)[+A(b)]F(1)B(0)",
            "B(i) : i > 0 -> B(i-1)",
            "B(i) : i == 0 -> F(1)[-B(b)]F(1)A(0)",
            "F(a) -> F(a*c)"
        ],
        "constants": {"b": 1, "c": 1.36},
        "angle": 45,
        "iterations": 18,
        "description": "Compound leaf with alternating branching",
        "category": "ferns"
    },
    
    "compound_leaf_complex": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(i) : i > 0 -> A(i-1)",
            "A(i) : i == 0 -> F(1)[+A(b)]F(1)B(0)",
            "B(i) : i > 0 -> B(i-1)",
            "B(i) : i == 0 -> F(1)[-B(b)]F(1)A(0)",
            "F(a) -> F(a*c)"
        ],
        "constants": {"b": 7, "c": 1.13},
        "angle": 45,
        "iterations": 38,
        "description": "Complex compound leaf",
        "category": "ferns"
    },
    
    # =========================================================================
    # NEW FROM PDF: Phyllotaxis Patterns
    # =========================================================================
    "phyllotaxis_basic": {
        "type": "parametric",
        "axiom": "A(1)",
        "productions": [
            "A(n) -> +(137.5)f(n^0.5)JA(n+1)"
        ],
        "angle": 137.5,
        "iterations": 200,
        "description": "Basic Vogel spiral phyllotaxis",
        "category": "phyllotaxis"
    },
    
    "phyllotaxis_137_3": {
        "type": "parametric",
        "axiom": "A(1)",
        "productions": [
            "A(n) -> +(137.3)f(n^0.5)JA(n+1)"
        ],
        "iterations": 200,
        "description": "Phyllotaxis with 137.3° - shows spiral arms",
        "category": "phyllotaxis"
    },
    
    "phyllotaxis_137_6": {
        "type": "parametric",
        "axiom": "A(1)",
        "productions": [
            "A(n) -> +(137.6)f(n^0.5)JA(n+1)"
        ],
        "iterations": 200,
        "description": "Phyllotaxis with 137.6° - opposite spiral arms",
        "category": "phyllotaxis"
    },
    
    "phyllotaxis_dome": {
        "type": "parametric",
        "axiom": "A(1)",
        "productions": [
            "A(n) -> /(137.5)[&(pitch)f(n^0.5)K]A(n+1)"
        ],
        "constants": {"pitch": 60},
        "iterations": 100,
        "is_3d": True,
        "description": "3D dome phyllotaxis pattern",
        "category": "phyllotaxis"
    },
}


def get_parametric_preset(name: str):
    """Get a parametric preset by name."""
    name_lower = name.lower()
    if name_lower in PARAMETRIC_PRESETS:
        preset = PARAMETRIC_PRESETS[name_lower].copy()
        preset['is_parametric'] = True
        return preset
    return None


def list_parametric_presets():
    """Return list of available parametric preset names."""
    return sorted(PARAMETRIC_PRESETS.keys())