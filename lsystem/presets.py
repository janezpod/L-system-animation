"""
Plant Presets

Botanically accurate L-system plant definitions based on:
- "The Algorithmic Beauty of Plants" (Prusinkiewicz & Lindenmayer)
- Honda's ternary tree model
- Fibonacci phyllotaxis research

Includes 2D and 3D preset collections with research-validated parameters.
"""

from typing import Dict, Any, List

# =============================================================================
# 2D Plant Presets - Research Validated
# =============================================================================

PRESETS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # TREES - 2D
    # =========================================================================
    "tree_binary": {
        "axiom": "F",
        "rules": {"F": "FF-[-F+F+F]+[+F-F-F]"},
        "angle": 22.5,
        "iterations": 4,
        "description": "Symmetric binary tree - ABOP Figure 1.24d"
    },
    "tree_elegant": {
        "axiom": "X",
        "rules": {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        "angle": 22.5,
        "iterations": 5,
        "description": "Elegant plant - ABOP Figure 1.24f (most beautiful 2D form)"
    },
    "tree_asymmetric": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 20,
        "iterations": 7,
        "description": "Asymmetric branching tree - ABOP Figure 1.24e"
    },
    "tree_stochastic": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": 25.7,
        "iterations": 5,
        "stochastic": 0.15,
        "description": "Stochastic-style branching (use with --stochastic 0.15)"
    },
    "oak_2d": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]FX", "F": "FF"},
        "angle": 35,
        "iterations": 6,
        "description": "Oak-like spreading crown"
    },
    "willow_2d": {
        "axiom": "F",
        "rules": {"F": "FF-[-F+F]+[+F-F-F]"},
        "angle": 22.5,
        "iterations": 5,
        "description": "Weeping willow drooping branches"
    },
    
    # Legacy aliases for backward compatibility
    "tree": {
        "axiom": "F",
        "rules": {"F": "F[-F][+F]"},
        "angle": 25,
        "iterations": 5,
        "description": "Simple binary tree (legacy)"
    },
    "tree2": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 20,
        "iterations": 5,
        "description": "Alternate tree structure (legacy)"
    },
    "tree_oak": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]FX", "F": "FF"},
        "angle": 30,
        "iterations": 5,
        "description": "Oak tree branching (legacy)"
    },
    "tree_willow": {
        "axiom": "F",
        "rules": {"F": "FF-[-F+F+F]+[+F-F-F]"},
        "angle": 22.5,
        "iterations": 4,
        "description": "Weeping willow (legacy)"
    },
    "bonsai": {
        "axiom": "F",
        "rules": {"F": "FF[++F][-FF][+F][-F]"},
        "angle": 30,
        "iterations": 4,
        "description": "Stylized bonsai tree"
    },
    "dragon_tree": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]F[+X]FX", "F": "FF"},
        "angle": 25.7,
        "iterations": 5,
        "description": "Dragon tree branching pattern"
    },
    
    # =========================================================================
    # FERNS - 2D (Research Validated)
    # =========================================================================
    "fern_classic": {
        "axiom": "X",
        "rules": {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        "angle": 22.5,
        "iterations": 5,
        "description": "Classic fern - ABOP canonical form"
    },
    "fern_dense": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 20,
        "iterations": 7,
        "description": "Dense fern fronds"
    },
    "fern_naturalistic": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]FX", "F": "FF"},
        "angle": 25.7,
        "iterations": 7,
        "description": "Naturalistic fern pattern - optimal angle from research"
    },
    "fern_simple": {
        "axiom": "Y",
        "rules": {"X": "X[-FFF][+FFF]FX", "Y": "YFX[+Y][-Y]"},
        "angle": 25.7,
        "iterations": 5,
        "description": "Simple pinnate fern"
    },
    "fern_bipinnate": {
        "axiom": "A",
        "rules": {"A": "F[+B]F[-B]A", "B": "F[+F][-F]F"},
        "angle": 45,
        "iterations": 6,
        "description": "Bipinnate (twice-divided) fern frond"
    },
    
    # Legacy fern aliases
    "fern": {
        "axiom": "X",
        "rules": {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        "angle": 25,
        "iterations": 6,
        "description": "Fractal fern (Barnsley-like, legacy)"
    },
    "fern_barnsley": {
        "axiom": "X",
        "rules": {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        "angle": 25,
        "iterations": 6,
        "description": "Classic Barnsley fern"
    },
    "fern_maidenhair": {
        "axiom": "Y",
        "rules": {"Y": "F[-X][+X]FY", "X": "F[-X]+X"},
        "angle": 30,
        "iterations": 6,
        "description": "Delicate maidenhair fern pattern"
    },
    "feather": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]F[+X]", "F": "F"},
        "angle": 85,
        "iterations": 6,
        "description": "Feather or leaf vein pattern"
    },
    
    # =========================================================================
    # BUSHES AND SHRUBS - 2D
    # =========================================================================
    "bush_abop": {
        "axiom": "F",
        "rules": {"F": "FF+[+F-F-F]-[-F+F+F]"},
        "angle": 22.5,
        "iterations": 4,
        "description": "ABOP bush structure"
    },
    "shrub_dense": {
        "axiom": "X",
        "rules": {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        "angle": 25,
        "iterations": 5,
        "description": "Dense shrub"
    },
    
    # Legacy bush aliases
    "bush": {
        "axiom": "F",
        "rules": {"F": "FF+[+F-F-F]-[-F+F+F]"},
        "angle": 22.5,
        "iterations": 4,
        "description": "Dense bush structure (legacy)"
    },
    "bush_dense": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F][F]"},
        "angle": 20,
        "iterations": 5,
        "description": "Very dense bush"
    },
    "weed": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": 25.7,
        "iterations": 4,
        "description": "Simple weed/grass"
    },
    "grass": {
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": 25.7,
        "iterations": 4,
        "description": "Grass or wheat stalk"
    },
    
    # =========================================================================
    # AQUATIC AND SPECIAL - 2D
    # =========================================================================
    "seaweed_wave": {
        "axiom": "F",
        "rules": {"F": "FF-[XY]+[XY]", "X": "+FY", "Y": "-FX"},
        "angle": 22.5,
        "iterations": 6,
        "description": "Swaying seaweed with wave motion"
    },
    "kelp_tall": {
        "axiom": "F",
        "rules": {"F": "FF[-F++F][+F--F]++F--F"},
        "angle": 15,
        "iterations": 5,
        "description": "Tall kelp fronds"
    },
    "coral_branch": {
        "axiom": "F",
        "rules": {"F": "FF+[+F-F-F]-[-F+F+F]"},
        "angle": 25,
        "iterations": 5,
        "description": "Branching coral structure"
    },
    
    # Legacy aquatic aliases
    "seaweed": {
        "axiom": "F",
        "rules": {"F": "FF-[XY]+[XY]", "X": "+FY", "Y": "-FX"},
        "angle": 22.5,
        "iterations": 5,
        "description": "Swaying seaweed pattern (legacy)"
    },
    "kelp": {
        "axiom": "F",
        "rules": {"F": "FF[-F++F][+F--F]++F--F"},
        "angle": 15,
        "iterations": 4,
        "description": "Wavy kelp/seaweed"
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
    
    # =========================================================================
    # VINES AND CLIMBERS - 2D
    # =========================================================================
    "vine": {
        "axiom": "X",
        "rules": {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        "angle": 22.5,
        "iterations": 5,
        "description": "Climbing vine pattern"
    },
    "ivy": {
        "axiom": "FX",
        "rules": {"X": "X[-FFF][+FFF]FX", "F": "FF"},
        "angle": 25,
        "iterations": 5,
        "description": "Ivy climbing pattern"
    },
    
    # =========================================================================
    # FLOWERS AND SUCCULENTS - 2D
    # =========================================================================
    "flower_simple": {
        "axiom": "X",
        "rules": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angle": 25,
        "iterations": 5,
        "description": "Simple flowering plant"
    },
    "succulent": {
        "axiom": "X",
        "rules": {"X": "F[-X][+X]", "F": "FF"},
        "angle": 45,
        "iterations": 6,
        "description": "Succulent/cactus branching"
    },
    
    # =========================================================================
    # STRUCTURAL / ABSTRACT - 2D
    # =========================================================================
    "sympodial": {
        "axiom": "X",
        "rules": {"X": "F[-X]F[+X]+X", "F": "FF"},
        "angle": 20,
        "iterations": 5,
        "description": "Sympodial branching (zigzag growth)"
    },
    "dichotomous": {
        "axiom": "X",
        "rules": {"X": "F[+X][-X]", "F": "FF"},
        "angle": 30,
        "iterations": 7,
        "description": "Equal dichotomous branching"
    },
    "crystal": {
        "axiom": "F+F+F+F+F+F",
        "rules": {"F": "F+F-F-F+F"},
        "angle": 60,
        "iterations": 4,
        "description": "Crystal/snowflake pattern"
    },
    "pine": {
        "axiom": "F",
        "rules": {"F": "F[+F][-F]F[+F][-F]"},
        "angle": 35,
        "iterations": 4,
        "description": "Pine branch pattern"
    },
}


# =============================================================================
# 3D Plant Presets - Research Validated with Biological Parameters
# =============================================================================

PRESETS_3D: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # REALISTIC 3D TREES - Based on ABOP Chapter 2 with practical fixes
    # =========================================================================
    
    # -------------------------------------------------------------------------
    # OAK - Sympodial structure (ABOP Fig 2.7)
    # Both daughter branches fork from parent (no single dominant trunk)
    # Creates wide spreading crown
    # -------------------------------------------------------------------------
    "oak_3d": {
        "axiom": "FFFFA",
        "rules": {
            # Fork into two branches at 180° apart, each continues forking
            # & pitches down (away from trunk), / rotates around trunk
            "A": "F[&B]/(180)[&B]",
            # Sub-branches: grow, fork into two, $ keeps branches horizontal
            "B": "FF[+$B][-$B]",
        },
        "angle": 35,  # Symmetric angles create dome shape (ABOP Table 2.2d)
        "roll_angle": 180,
        "iterations": 9,
        "tropism_strength": 0.0,  # Oak doesn't droop significantly
        "width_decay": 0.707,  # Leonardo's rule
        "length_decay": 0.80,  # Slightly shorter branches for density
        "stochastic": 0.15,  # Natural variation
        "description": "Spreading oak - ABOP sympodial (Fig 2.7d)"
    },
    
    # -------------------------------------------------------------------------
    # MAPLE - Sympodial with opposite/decussate branching
    # Similar to oak but branches at 90° rotation each level
    # -------------------------------------------------------------------------
    "maple_3d": {
        "axiom": "FFFFA",
        "rules": {
            # Fork into two opposite branches
            "A": "F[&B]/(180)[&B]",
            # Sub-branches fork, alternating sides
            "B": "FF[+$C][-$C]",
            "C": "F[+$B][-$B]"
        },
        "angle": 40,
        "roll_angle": 90,  # 90° rotation between levels (decussate)
        "iterations": 8,
        "tropism_strength": 0.0,
        "width_decay": 0.707,
        "length_decay": 0.78,
        "stochastic": 0.12,
        "description": "Maple - sympodial with decussate branching"
    },
    
    # -------------------------------------------------------------------------
    # BIRCH - Monopodial (ABOP Fig 2.6)
    # Single dominant trunk with lateral branches
    # FIXED: Branch develops BEFORE trunk continues (avoids bare top)
    # -------------------------------------------------------------------------
    "birch_3d": {
        "axiom": "FFFFA",
        "rules": {
            # Trunk: branch first, then grow trunk segment, then continue
            # This ensures branches develop at same rate as trunk
            "A": "[&B]/FA",
            # Branches fork on both sides
            "B": "F[-B][+B]",
        },
        "angle": 35,
        "roll_angle": 137.5,  # Golden angle divergence
        "iterations": 9,
        "tropism_strength": 0.08,  # Slight natural droop
        "tropism_direction": [0, -1, 0],
        "width_decay": 0.65,
        "length_decay": 0.85,
        "stochastic": 0.12,
        "description": "Birch - ABOP monopodial (Fig 2.6)"
    },
    
    # -------------------------------------------------------------------------
    # WILLOW - Monopodial with drooping branches
    # FIXED: Branches start HORIZONTAL (single &), tropism bends them down
    # Not too much droop to avoid going underground
    # -------------------------------------------------------------------------
    "willow_3d": {
        "axiom": "FFFFFFA",  # Tall trunk
        "rules": {
            # Trunk: emit branch at moderate angle (near horizontal)
            "A": "[&B]/FA",
            # Branches grow outward and cascade, creating curtain effect
            "B": "F[+B][-B]FB",
        },
        "angle": 60,  # Nearly horizontal start (90-60=30° from horizontal)
        "roll_angle": 137.5,
        "iterations": 8,
        "tropism_strength": 0.20,  # Moderate droop (not too extreme)
        "tropism_direction": [0, -1, 0],  # Bend downward
        "width_decay": 0.75,
        "length_decay": 0.88,
        "stochastic": 0.08,
        "description": "Weeping willow - branches start horizontal, droop via tropism"
    },
    
    # -------------------------------------------------------------------------
    # PINE - Honda's Ternary Model (ABOP Fig 2.8a)
    # Three branches per node, specific divergence angles
    # -------------------------------------------------------------------------
    "pine_honda": {
        "axiom": "FFFFA",
        "rules": {
            # Ternary: three branches per whorl with Honda's angles
            "A": "[&B]/(94.74)[&B]/(132.63)[&B]/(132.63)FA",
            "B": "FF[-B][+B]",
        },
        "angle": 25,  # Branch angle from trunk
        "roll_angle": 94.74,  # Honda's first divergence
        "iterations": 7,
        "tropism_strength": 0.12,
        "tropism_direction": [0, -1, 0],
        "width_decay": 0.65,
        "length_decay": 0.85,
        "description": "Pine - Honda's ternary model (ABOP Fig 2.8a)"
    },
    
    # -------------------------------------------------------------------------
    # CONIFER - Whorled branches with golden angle
    # Multiple branches per level in a spiral pattern
    # -------------------------------------------------------------------------
    "conifer_realistic": {
        "axiom": "FFFFT",
        "rules": {
            # Four branches per whorl, golden angle spiral up trunk
            "T": "[&L]/(137.5)[&L]/(137.5)[&L]/(137.5)[&L]/(137.5)FT",
            "L": "FF[-F][+F]"
        },
        "angle": 25,
        "roll_angle": 137.5,
        "iterations": 8,
        "tropism_strength": 0.10,
        "tropism_direction": [0, -1, 0],
        "width_decay": 0.70,
        "length_decay": 0.88,
        "description": "Conifer - whorled branches, golden angle"
    },
    
    # =========================================================================
    # TREE ARCHITECTURE TYPES - ABOP Reference Models
    # =========================================================================
    
    "monopodial_tree": {
        # ABOP Figure 2.6 - Single dominant trunk with laterals
        "axiom": "FFFFA",
        "rules": {
            "A": "[&B]/FA",  # Branch, rotate, grow trunk, continue
            "B": "F[-B][+B]"  # Branches fork
        },
        "angle": 45,
        "roll_angle": 137.5,
        "iterations": 9,
        "tropism_strength": 0.05,
        "tropism_direction": [0, -1, 0],
        "width_decay": 0.707,
        "length_decay": 0.85,
        "description": "Monopodial - ABOP Fig 2.6 (single trunk, laterals)"
    },
    
    "sympodial_tree": {
        # ABOP Figure 2.7 - Bifurcating branches, no single trunk
        "axiom": "FFFFA",
        "rules": {
            "A": "F[&B]/(180)[&B]",  # Fork into two
            "B": "FF[+$B][-$B]"  # Each branch forks again
        },
        "angle": 35,
        "roll_angle": 180,
        "iterations": 9,
        "tropism_strength": 0.0,
        "width_decay": 0.707,
        "length_decay": 0.82,
        "stochastic": 0.10,
        "description": "Sympodial - ABOP Fig 2.7 (forking branches)"
    },
    
    # =========================================================================
    # 3D FERNS (Delicate Forms)
    # =========================================================================
    "fern_3d_alternating": {
        "axiom": "A",
        "rules": {
            # Alternating pinnae with roll
            "A": "F[&+P]//[&-P]//A",
            "P": "F[+F]/[-F]F"
        },
        "angle": 45,
        "roll_angle": 137.5,
        "iterations": 7,
        "width_decay": 0.75,
        "length_decay": 0.88,
        "description": "3D fern with alternating pinnae arrangement"
    },
    
    "fern_3d_spiral": {
        "axiom": "A",
        "rules": {
            # Spiral arrangement with golden angle
            "A": "F[&P]/A",
            "P": "F[+F][-F]"
        },
        "angle": 50,
        "roll_angle": 137.5,  # Golden angle spiral
        "iterations": 15,
        "width_decay": 0.78,
        "length_decay": 0.92,
        "description": "Spiral fern frond with golden angle phyllotaxis"
    },
    
    "fern_3d_bipinnate": {
        "axiom": "A",
        "rules": {
            # Bipinnate with roll distribution
            "A": "F[&+B]//[&-B]//A",
            "B": "F[+L]/[-L]B",
            "L": "F"
        },
        "angle": 45,
        "roll_angle": 137.5,
        "iterations": 5,
        "width_decay": 0.72,
        "length_decay": 0.85,
        "description": "Bipinnate 3D fern (twice-divided fronds)"
    },
    
    "fern_3d_maidenhair": {
        "axiom": "FFFA",
        "rules": {
            # Delicate fronds with roll
            "A": "F[&+L]//[&-L]//A",
            "L": "F[+F]/F[-F]"
        },
        "angle": 35,
        "roll_angle": 137.5,
        "iterations": 7,
        "width_decay": 0.68,
        "length_decay": 0.90,
        "description": "Delicate maidenhair fern structure"
    },
    
    "fiddlehead_3d": {
        "axiom": "A",
        "rules": {
            "A": "F&A",  # Gradually unfurling spiral
            "F": "FF"
        },
        "angle": 15,  # Tight initial curl
        "roll_angle": 20,
        "iterations": 12,
        "width_decay": 0.92,
        "length_decay": 0.95,
        "description": "Fiddlehead/crozier unfurling fern"
    },
    
    # =========================================================================
    # GOLDEN ANGLE PHYLLOTAXIS PLANTS
    # =========================================================================
    "phyllotaxis_spiral": {
        "axiom": "A",
        "rules": {
            "A": "F[&L]/A",
            "L": "[^^F]"
        },
        "angle": 40,
        "roll_angle": 137.5077,  # Precise golden angle
        "iterations": 21,  # Fibonacci number for best spirals
        "width_decay": 0.95,
        "length_decay": 0.97,
        "description": "Pure golden angle spiral - shows Fibonacci patterns"
    },
    
    "sunflower_head": {
        "axiom": "A",
        "rules": {
            "A": "F[&S]/A",
            "S": "F"
        },
        "angle": 30,
        "roll_angle": 137.5077,
        "iterations": 55,  # Fibonacci number
        "width_decay": 0.98,
        "length_decay": 0.99,
        "description": "Sunflower-like spiral arrangement"
    },
    
    "succulent_rosette": {
        "axiom": "A",
        "rules": {
            "A": "[&L]/A",
            "L": "F[+F][-F]"
        },
        "angle": 60,
        "roll_angle": 137.5,
        "iterations": 13,  # Fibonacci
        "width_decay": 0.90,
        "length_decay": 0.92,
        "description": "Succulent rosette with golden spiral"
    },
    
    # =========================================================================
    # PALM AND TROPICAL
    # =========================================================================
    "palm_3d_realistic": {
        "axiom": "FFFFFFFFA",  # Long trunk
        "rules": {
            "A": "[&&&F[+F][-F]F]/////A"  # Radiating fronds
        },
        "angle": 35,
        "roll_angle": 72,  # 5 fronds per whorl (360/5)
        "iterations": 8,
        "tropism_strength": 0.20,
        "width_decay": 0.80,
        "length_decay": 0.88,
        "description": "Palm tree with 5-fold radial fronds"
    },
    
    "bamboo_3d": {
        "axiom": "FA",
        "rules": {
            "A": "F[/+L][/-L]FA",
            "L": "FF",
            "F": "F"
        },
        "angle": 55,
        "roll_angle": 180,
        "iterations": 12,
        "width_decay": 0.92,
        "length_decay": 0.95,
        "description": "Bamboo with segmented culm and alternating branches"
    },
    
    # =========================================================================
    # ARTISTIC / ABSTRACT 3D
    # =========================================================================
    "helix_vine": {
        "axiom": "A",
        "rules": {
            # Helical pattern with leaves on all sides
            "A": "F/[&+L]A",
            "L": "F[+F][-F]"
        },
        "angle": 30,
        "roll_angle": 36,  # 10-fold helix (360/10)
        "iterations": 30,
        "width_decay": 0.95,
        "length_decay": 0.98,
        "description": "Helical climbing vine"
    },
    
    "crystal_tree": {
        "axiom": "FA",
        "rules": {
            # Orthogonal branching with roll
            "A": "F[+A]/[-A]/[&A]/[^A]/",
            "F": "F"
        },
        "angle": 90,
        "roll_angle": 90,
        "iterations": 4,
        "width_decay": 0.707,
        "length_decay": 0.75,
        "description": "Crystalline orthogonal branching"
    },
    
    "bush_3d_dense": {
        "axiom": "A",
        "rules": {
            "A": "[&FL!A]////[&FL!A]//////[&FL!A]",
            "F": "S//F",
            "S": "F",
            "L": "[+F][-F]F"
        },
        "angle": 22.5,
        "roll_angle": 22.5,
        "iterations": 7,
        "width_decay": 0.70,
        "length_decay": 0.85,
        "description": "Dense 3D bush - ABOP style"
    },
    
    # =========================================================================
    # LEGACY 3D PRESETS (backward compatibility)
    # =========================================================================
    "tree_3d_simple": {
        "axiom": "F",
        "rules": {"F": "F[+F]/[-F]/[&F]/[^F]/"},
        "angle": 25,
        "roll_angle": 90,
        "iterations": 4,
        "description": "Simple 3D branching tree (legacy)"
    },
    
    "bush_3d": {
        "axiom": "A",
        "rules": {
            "A": "[&FL!A]////[&FL!A]//////[&FL!A]",
            "F": "S//F",
            "S": "F",
            "L": "[-F]/[+F]F"
        },
        "angle": 22.5,
        "roll_angle": 22.5,
        "iterations": 6,
        "description": "3D bush with spiral branching (legacy)"
    },
    
    "tree_3d_realistic": {
        "axiom": "FA",
        "rules": {
            "A": "F[&+B]//[&-B]//[&B]//FA",
            "B": "F[+B]/[-B]",
            "F": "FF"
        },
        "angle": 25,
        "roll_angle": 137.5,
        "iterations": 4,
        "tropism_strength": 0.15,
        "description": "Realistic 3D tree with gravitropism (legacy)"
    },
    
    "spiral_plant_3d": {
        "axiom": "A",
        "rules": {
            "A": "F[&+L]/A",
            "L": "[+F][-F]"
        },
        "angle": 35,
        "roll_angle": 137.5,
        "iterations": 12,
        "description": "Phyllotactic spiral plant (legacy)"
    },
    
    "fern_3d": {
        "axiom": "X",
        "rules": {
            "X": "F[&+X]//[&-X]//X",
            "F": "FF"
        },
        "angle": 25,
        "roll_angle": 137.5,
        "iterations": 5,
        "description": "3D fern with alternating fronds (legacy)"
    },
    
    "palm_3d": {
        "axiom": "FFFFFFA",
        "rules": {
            "A": "[+F[+F][-F]F]/////A"
        },
        "angle": 35,
        "roll_angle": 72,
        "iterations": 6,
        "description": "Palm tree with radial fronds (legacy)"
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
        "description": "Conifer/pine tree shape (legacy)"
    },
    
    "helix_3d": {
        "axiom": "A",
        "rules": {
            "A": "F/[+L]A",
            "L": "F"
        },
        "angle": 30,
        "roll_angle": 36,
        "iterations": 30,
        "description": "Helical climbing plant (legacy)"
    },
}


def get_preset(name: str, include_3d: bool = True) -> dict:
    """
    Get a preset by name.
    
    Args:
        name: Preset name (case-insensitive)
        include_3d: Whether to search 3D presets too
        
    Returns:
        Preset dictionary with axiom, rules, angle, iterations,
        and optional biological parameters (width_decay, length_decay,
        tropism_strength, stochastic, etc.)
        
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
    return {
        # 2D Categories
        "2D Trees": ["tree_binary", "tree_elegant", "tree_asymmetric", 
                     "tree_stochastic", "oak_2d", "willow_2d",
                     "tree", "tree2", "tree_oak", "tree_willow", "bonsai", "dragon_tree"],
        "2D Ferns": ["fern_classic", "fern_dense", "fern_naturalistic",
                     "fern_simple", "fern_bipinnate",
                     "fern", "fern_barnsley", "fern_maidenhair", "feather"],
        "2D Bushes": ["bush_abop", "shrub_dense",
                      "bush", "bush_dense", "weed", "grass"],
        "2D Aquatic": ["seaweed_wave", "kelp_tall", "coral_branch",
                       "seaweed", "kelp", "algae", "coral"],
        "2D Vines": ["vine", "ivy"],
        "2D Special": ["flower_simple", "succulent", "sympodial", 
                       "dichotomous", "crystal", "pine"],
        
        # 3D Categories
        "3D Realistic Trees": ["oak_3d", "maple_3d", "birch_3d", "willow_3d",
                               "pine_honda", "conifer_realistic"],
        "3D Tree Architecture": ["monopodial_tree", "sympodial_tree"],
        "3D Ferns": ["fern_3d_alternating", "fern_3d_spiral", "fern_3d_bipinnate",
                     "fern_3d_maidenhair", "fiddlehead_3d"],
        "3D Phyllotaxis": ["phyllotaxis_spiral", "sunflower_head", "succulent_rosette"],
        "3D Tropical": ["palm_3d_realistic", "bamboo_3d"],
        "3D Artistic": ["helix_vine", "crystal_tree", "bush_3d_dense"],
        "3D Legacy": ["tree_3d_simple", "bush_3d", "tree_3d_realistic",
                      "spiral_plant_3d", "fern_3d", "palm_3d", "conifer_3d", "helix_3d"]
    }


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
        f"  Angle: {preset['angle']}Â°",
        f"  Iterations: {preset['iterations']}"
    ]
    
    if 'description' in preset:
        info_lines.append(f"  Description: {preset['description']}")
    
    if preset.get('is_3d'):
        info_lines.append("  Type: 3D")
        if 'roll_angle' in preset:
            info_lines.append(f"  Roll Angle: {preset['roll_angle']}Â°")
        if 'tropism_strength' in preset:
            info_lines.append(f"  Tropism Strength: {preset['tropism_strength']}")
        if 'width_decay' in preset:
            info_lines.append(f"  Width Decay: {preset['width_decay']}")
        if 'length_decay' in preset:
            info_lines.append(f"  Length Decay: {preset['length_decay']}")
        if 'stochastic' in preset:
            info_lines.append(f"  Stochastic: {preset['stochastic']}")
    
    return '\n'.join(info_lines)


# Key biological constants for reference
GOLDEN_ANGLE = 137.5077  # Optimal phyllotaxis angle
LEONARDO_WIDTH_DECAY = 0.707  # âˆš2â»Â¹ - preserves cross-sectional area
HONDA_BRANCHING_ANGLE = 18.95  # Honda's optimal angle
HONDA_DIVERGENCE_D1 = 94.74  # Honda's first divergence angle
HONDA_DIVERGENCE_D2 = 132.63  # Honda's second divergence angle

# =============================================================================
# PARAMETRIC PRESETS - ABOP Advanced Features
# =============================================================================

PARAMETRIC_PRESETS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # GROWING TREES - Continuous segment elongation
    # =========================================================================
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
    
    # =========================================================================
    # STOCHASTIC PLANTS - Natural variation
    # =========================================================================
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
    
    # =========================================================================
    # DEVELOPMENTAL LEAVES - Using polygon notation
    # =========================================================================
    "developmental_leaf": {
        "type": "parametric",
        "axiom": "[A(0)][B(0)]",
        "productions": [
            # Left lobe: grows outward, creates wedge polygons
            "A(n) : n < 6 -> F{.+F.-F.}A(n+1)",
            # Right lobe: mirror image
            "B(n) : n < 6 -> F{.-F.+F.}B(n+1)",
            # Terminal
            "A(n) : n >= 6 -> F",
            "B(n) : n >= 6 -> F",
        ],
        "angle": 30,
        "iterations": 6,
        "description": "Cordate leaf with polygon filling - creates wedge-shaped polygons"
    },
    
    "simple_polygon_leaf": {
        "type": "parametric", 
        "axiom": "A",
        "productions": [
            # Simple triangular leaf shape
            "A -> {.F.+F.+F.}",
        ],
        "angle": 120,
        "iterations": 1,
        "description": "Simple triangular polygon test"
    },
    
    "growing_leaf": {
        "type": "parametric",
        "axiom": "A(1)",
        "productions": [
            "A(t) : t < 10 -> F(t){.+F(t).-..-F(t).+|+F(t).-..-.}A(t+1)",
            "A(t) : t >= 10 -> F(t)",
        ],
        "constants": {},
        "angle": 30,
        "iterations": 10,
        "description": "Growing leaf shape"
    },
    
    # =========================================================================
    # HONDA'S TREE MODEL - Research validated
    # =========================================================================
    "honda_tree_param": {
        "type": "parametric",
        "axiom": "A(100,20)",
        "productions": [
            "A(l,w) -> !(w)F(l)[&B(l*r1,w*wr)]/[&B(l*r2,w*wr)]",
            "B(l,w) -> !(w)F(l)[+B(l*r1,w*wr)][-B(l*r2,w*wr)]",
        ],
        "constants": {
            "r1": 0.9, "r2": 0.7,
            "wr": 0.707,
        },
        "angle": 45,
        "roll_angle": 137.5,
        "iterations": 10,
        "is_3d": True,
        "description": "Honda tree model - ABOP Chapter 2"
    },
    
    # =========================================================================
    # PHYLLOTAXIS PATTERNS - Golden angle
    # =========================================================================
    "sunflower_vogel": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(n) : n < 200 -> +(137.5)[f(2*sqrt(n)).]A(n+1)",
        ],
        "angle": 0,
        "iterations": 200,
        "description": "Sunflower head - Vogel's formula (ABOP Chapter 4)"
    },
    
    "phyllotaxis_rosette": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(n) : n < 55 -> [&F(3)']/(137.5)A(n+1)",
        ],
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 55,
        "is_3d": True,
        "description": "Rosette pattern with golden angle phyllotaxis"
    },
    
    # =========================================================================
    # SIGNAL-BASED GROWTH
    # =========================================================================
    "signal_tree": {
        "type": "parametric",
        "axiom": "A(0)",
        "productions": [
            "A(s) : s == 0 -> F[-B(1)]F[+B(1)]A(0)",
            "B(s) : s > 0 -> F[-B(s-1)][+B(s-1)]",
            "B(s) : s == 0 -> B(0)",
        ],
        "constants": {},
        "angle": 45,
        "iterations": 8,
        "description": "Tree with signal-based branch activation"
    },
    
    # =========================================================================
    # PARAMETRIC 3D PLANTS
    # =========================================================================
    "parametric_conifer_3d": {
        "type": "parametric",
        "axiom": "T(1,50)",
        "productions": [
            "T(age,l) : age < 10 -> F(l)[&B(l*0.4)]/(137.5)T(age+1,l*0.95)",
            "B(l) -> F(l)[+B(l*0.7)][-B(l*0.7)]",
        ],
        "constants": {},
        "angle": 30,
        "roll_angle": 137.5,
        "iterations": 10,
        "is_3d": True,
        "description": "Parametric conifer with golden angle"
    },
    
    "parametric_palm_3d": {
        "type": "parametric",
        "axiom": "T(0,10)",
        "productions": [
            "T(n,l) : n < 8 -> F(l)T(n+1,l*0.95)",
            "T(n,l) : n >= 8 -> F(l)W(0)",
            "W(a) : a < 5 -> [&&&F(30)[+F(10)][-F(10)]F(10)]/(72)W(a+1)",
        ],
        "constants": {},
        "angle": 35,
        "roll_angle": 72,
        "iterations": 15,
        "is_3d": True,
        "description": "Parametric palm tree with whorled fronds"
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