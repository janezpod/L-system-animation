"""
ABOP Preset Collection

Direct recreations of figures from "The Algorithmic Beauty of Plants"
by Prusinkiewicz & Lindenmayer.

These presets are organized by:
1. Figure recreations (direct from the book)
2. Tree models (Honda, Aono-Kunii)
3. Inflorescence patterns (Chapter 3)
4. Phyllotaxis patterns (Chapter 4)

Each preset includes:
- Proper ABOP attribution
- Botanical context
- Recommended parameters
"""

from typing import Dict, Any

# Golden angle for phyllotaxis (ABOP equation 4.1)
GOLDEN_ANGLE = 137.5077

# Leonardo's width decay ratio (ABOP Section 2.1)
LEONARDO_RATIO = 0.707  # √2⁻¹ ≈ 0.707

# =============================================================================
# ABOP Figure Recreations - Chapter 1
# =============================================================================

ABOP_FIGURE_PRESETS: Dict[str, Dict[str, Any]] = {
    
    # ABOP Figure 1.24a - Basic binary tree with alternating branches
    'abop_fig_1_24a': {
        'axiom': 'F',
        'rules': {'F': 'F[+F]F[-F]F'},
        'angle': 25.7,
        'iterations': 5,
        'description': 'ABOP Figure 1.24a - Basic branching structure',
        'category': 'abop_figures'
    },
    
    # ABOP Figure 1.24b - More complex branching
    'abop_fig_1_24b': {
        'axiom': 'F',
        'rules': {'F': 'F[+F]F[-F][F]'},
        'angle': 20,
        'iterations': 5,
        'description': 'ABOP Figure 1.24b - Extended branching',
        'category': 'abop_figures'
    },
    
    # ABOP Figure 1.24c - Asymmetric tree
    'abop_fig_1_24c': {
        'axiom': 'F',
        'rules': {'F': 'FF-[-F+F+F]+[+F-F-F]'},
        'angle': 22.5,
        'iterations': 4,
        'description': 'ABOP Figure 1.24c - Asymmetric branching',
        'category': 'abop_figures'
    },
    
    # ABOP Figure 1.24d - Symmetric binary tree
    'abop_fig_1_24d': {
        'axiom': 'X',
        'rules': {'X': 'F[+X][-X]FX', 'F': 'FF'},
        'angle': 25.7,
        'iterations': 6,
        'description': 'ABOP Figure 1.24d - Symmetric binary tree',
        'category': 'abop_figures'
    },
    
    # ABOP Figure 1.24e - Asymmetric growth
    'abop_fig_1_24e': {
        'axiom': 'X',
        'rules': {'X': 'F[+X]F[-X]+X', 'F': 'FF'},
        'angle': 20,
        'iterations': 7,
        'description': 'ABOP Figure 1.24e - Asymmetric growth pattern',
        'category': 'abop_figures'
    },
    
    # ABOP Figure 1.24f - Most elegant plant form (highlighted in research)
    'abop_fig_1_24f': {
        'axiom': 'X',
        'rules': {
            'X': 'F-[[X]+X]+F[+FX]-X',
            'F': 'FF'
        },
        'angle': 22.5,
        'iterations': 5,
        'description': 'ABOP Figure 1.24f - Elegant plant (most beautiful 2D form)',
        'category': 'abop_figures'
    },
    
    # ABOP Figure 1.25 - 3D bush with leaves
    'abop_fig_1_25': {
        'axiom': 'A',
        'rules': {
            'A': '[&FL!A]////\'[&FL!A]//////\'[&FL!A]',
            'F': 'S/////F',
            'S': 'FL',
            'L': '[\'\'\'^^{-f+f+f-|-f+f+f}]'
        },
        'angle': 22.5,
        'iterations': 7,
        'is_3d': True,
        'width_decay': 0.9,
        'description': 'ABOP Figure 1.25 - 3D bush with polygon leaves',
        'category': 'abop_figures'
    },
    
    # ABOP Figure 1.26 - Plant with flowers
    'abop_fig_1_26': {
        'axiom': 'plant',
        'rules': {
            'plant': 'internode+[plant+flower]--//[--leaf]internode[++leaf]-[plantflower]++plantflower',
            'internode': 'Fseg[//&&leaf][//^^leaf]Fseg',
            'seg': 'segFseg',
            'leaf': '[\'\'\'^^{-f+f-f+f-|+f-f+f-f}]',
            'flower': '[&&&pedicel\'/wedge////wedge////wedge////wedge////wedge]',
            'pedicel': 'FF',
            'wedge': '[\'\'^^F][{&&&&-f+f|-f+f}]'
        },
        'angle': 18,
        'iterations': 5,
        'is_3d': True,
        'description': 'ABOP Figure 1.26 - Flowering plant with leaves',
        'category': 'abop_figures'
    },
}

# =============================================================================
# Tree Models - Chapter 2
# =============================================================================

ABOP_TREE_PRESETS: Dict[str, Dict[str, Any]] = {
    
    # ABOP Figure 2.7a - Sympodial tree (Aono-Kunii model)
    'abop_sympodial_tree': {
        'type': 'parametric',
        'axiom': 'A(1,10)',
        'productions': [
            'A(l,w) -> !(w)F(l)[&(a1)B(l*r1,w*wr)]/(180)[&(a2)B(l*r2,w*wr)]',
            'B(l,w) -> !(w)F(l)[+(a1)$B(l*r1,w*wr)][-(a2)$B(l*r2,w*wr)]'
        ],
        'constants': {
            'r1': 0.9,      # Length ratio main
            'r2': 0.7,      # Length ratio lateral
            'a1': 5,        # Branching angle 1
            'a2': 65,       # Branching angle 2
            'wr': 0.707     # Width ratio (Leonardo's rule)
        },
        'iterations': 10,
        'is_3d': True,
        'description': 'ABOP Figure 2.7 - Sympodial tree (Aono-Kunii)',
        'category': 'abop_trees'
    },
    
    # ABOP Figure 2.8a - Ternary branching tree
    'abop_ternary_tree': {
        'type': 'parametric',
        'axiom': '!(1)F(200)/(45)A',
        'productions': [
            'A -> !(vr)F(50)[&(a)F(50)A]/(d1)[&(a)F(50)A]/(d2)[&(a)F(50)A]',
            'F(l) -> F(l*lr)',
            '!(w) -> !(w*vr)'
        ],
        'constants': {
            'd1': 94.74,    # Divergence angle 1
            'd2': 132.63,   # Divergence angle 2
            'a': 18.95,     # Branching angle
            'lr': 1.109,    # Length growth rate
            'vr': 1.732     # Width increase rate (√3 for ternary)
        },
        'iterations': 6,
        'tropism_strength': 0.22,
        'tropism_direction': [0, -1, 0],
        'is_3d': True,
        'description': 'ABOP Figure 2.8a - Ternary tree with tropism',
        'category': 'abop_trees'
    },
    
    # ABOP Table 2.3 variant b - Golden angle divergence
    'abop_tree_variant_b': {
        'type': 'parametric',
        'axiom': '!(1)F(200)/(45)A',
        'productions': [
            'A -> !(vr)F(50)[&(a)F(50)A]/(d1)[&(a)F(50)A]/(d2)[&(a)F(50)A]',
            'F(l) -> F(l*lr)',
            '!(w) -> !(w*vr)'
        ],
        'constants': {
            'd1': 137.5,    # Golden angle
            'd2': 137.5,    # Golden angle
            'a': 18.95,
            'lr': 1.109,
            'vr': 1.732
        },
        'iterations': 8,
        'tropism_strength': 0.14,
        'tropism_direction': [0, -1, 0],
        'is_3d': True,
        'description': 'ABOP Table 2.3 variant b - Golden angle divergence',
        'category': 'abop_trees'
    },
    
    # ABOP Table 2.3 variant c - Different tropism
    'abop_tree_variant_c': {
        'type': 'parametric',
        'axiom': '!(1)F(200)/(45)A',
        'productions': [
            'A -> !(vr)F(50)[&(a)F(50)A]/(d1)[&(a)F(50)A]/(d2)[&(a)F(50)A]',
            'F(l) -> F(l*lr)',
            '!(w) -> !(w*vr)'
        ],
        'constants': {
            'd1': 112.5,
            'd2': 157.5,
            'a': 22.5,
            'lr': 1.079,
            'vr': 1.732
        },
        'iterations': 8,
        'tropism_strength': 0.27,
        'tropism_direction': [0, -1, 0],
        'is_3d': True,
        'description': 'ABOP Table 2.3 variant c - Stronger tropism',
        'category': 'abop_trees'
    },
    
    # Honda's original tree model parameters
    'honda_tree': {
        'type': 'parametric',
        'axiom': 'A(100,10)',
        'productions': [
            'A(l,w) -> !(w)F(l)[&(a1)B(l*r1,w*wr)]/(d)[&(a2)B(l*r2,w*wr)]',
            'B(l,w) -> !(w)F(l)[+(a1)$B(l*r1,w*wr)][-(a2)$B(l*r2,w*wr)]'
        ],
        'constants': {
            'r1': 0.9,
            'r2': 0.8,
            'a1': 25,
            'a2': 45,
            'wr': 0.707,
            'd': 137.5      # Golden angle
        },
        'iterations': 8,
        'is_3d': True,
        'description': 'Honda tree model with standard parameters',
        'category': 'abop_trees'
    },
}

# =============================================================================
# Inflorescence Models - Chapter 3
# =============================================================================

ABOP_INFLORESCENCE_PRESETS: Dict[str, Dict[str, Any]] = {
    
    # ABOP Figure 3.2 - Open raceme
    'abop_raceme_open': {
        'type': 'parametric',
        'axiom': 'A(15)',
        'productions': [
            'A(n) : n > 0 -> I(20)[-(30)K]/(d)A(n-1)',
            'A(n) : n == 0 -> K',
            'I(l) -> F(l)'
        ],
        'constants': {'d': 137.5},  # Golden angle
        'iterations': 15,
        'is_3d': True,
        'description': 'ABOP Figure 3.2 - Open raceme inflorescence',
        'category': 'inflorescence'
    },
    
    # ABOP Figure 3.2 - Closed raceme
    'abop_raceme_closed': {
        'type': 'parametric',
        'axiom': 'A(15)',
        'productions': [
            'A(n) : n > 0 -> I(15)[-(35)K]/(d)A(n-1)',
            'A(n) : n == 0 -> I(10)K',  # Terminal flower
            'I(l) -> F(l)'
        ],
        'constants': {'d': 137.5},
        'iterations': 15,
        'is_3d': True,
        'description': 'ABOP Figure 3.2 - Closed raceme (terminal flower)',
        'category': 'inflorescence'
    },
    
    # ABOP Figure 3.10 - Simple cyme
    'abop_cyme_simple': {
        'type': 'parametric',
        'axiom': 'A(8)',
        'productions': [
            'A(n) : n > 0 -> I(20)K[+(45)A(n-1)][-(45)A(n-1)]',
            'A(n) : n == 0 -> I(10)K',
            'I(l) -> F(l)'
        ],
        'constants': {},
        'iterations': 8,
        'is_3d': True,
        'description': 'ABOP Figure 3.10 - Simple cyme (dichasium)',
        'category': 'inflorescence'
    },
    
    # ABOP Figure 3.16 - Panicle
    'abop_panicle': {
        'type': 'parametric',
        'axiom': 'A(5)',
        'productions': [
            'A(n) : n > 0 -> I(30)[+(40)B(n-1)][-(40)B(n-1)]/(d)A(n-1)',
            'A(n) : n == 0 -> I(15)K',
            'B(n) : n > 0 -> I(20)[+(35)B(n-1)]K',
            'B(n) : n == 0 -> I(10)K',
            'I(l) -> F(l)'
        ],
        'constants': {'d': 137.5},
        'iterations': 5,
        'is_3d': True,
        'description': 'ABOP Figure 3.16 - Panicle (compound raceme)',
        'category': 'inflorescence'
    },
    
    # ABOP Figure 3.19 - Lilac
    'abop_lilac': {
        'type': 'parametric',
        'axiom': 'I(30)/(45)A',
        'productions': [
            'A -> [-(60)/K][+(60)/K]I(20)/(90)A',
            'I(l) : l < 30 -> FI(l+10)',
            'I(l) : l >= 30 -> I(l)[-(45)FFA][+(45)FFA]'
        ],
        'constants': {},
        'angle': 60,
        'iterations': 10,
        'is_3d': True,
        'description': 'ABOP Figure 3.19 - Lilac inflorescence',
        'category': 'inflorescence'
    },
    
    # Umbel (5-fold)
    'abop_umbel': {
        'type': 'parametric',
        'axiom': 'I(50)A',
        'productions': [
            'A -> [&(60)I(30)K]/(72)[&(60)I(30)K]/(72)[&(60)I(30)K]/(72)[&(60)I(30)K]/(72)[&(60)I(30)K]',
            'I(l) -> F(l)'
        ],
        'constants': {},
        'iterations': 2,
        'is_3d': True,
        'description': 'ABOP - Simple umbel (5-fold)',
        'category': 'inflorescence'
    },
    
    # Compound umbel
    'abop_umbel_compound': {
        'type': 'parametric',
        'axiom': 'I(80)A',
        'productions': [
            'A -> [&(55)I(40)B]/(72)[&(55)I(40)B]/(72)[&(55)I(40)B]/(72)[&(55)I(40)B]/(72)[&(55)I(40)B]',
            'B -> [&(50)I(20)K]/(72)[&(50)I(20)K]/(72)[&(50)I(20)K]/(72)[&(50)I(20)K]/(72)[&(50)I(20)K]',
            'I(l) -> F(l)'
        ],
        'constants': {},
        'iterations': 3,
        'is_3d': True,
        'description': 'ABOP - Compound umbel',
        'category': 'inflorescence'
    },
}

# =============================================================================
# Phyllotaxis Patterns - Chapter 4
# =============================================================================

ABOP_PHYLLOTAXIS_PRESETS: Dict[str, Dict[str, Any]] = {
    
    # ABOP Figure 4.11 - Cylindrical phyllotaxis
    'abop_phyllotaxis_cylinder': {
        'type': 'parametric',
        'axiom': 'A(100)',
        'productions': [
            'A(n) : n > 0 -> [&(90)f(r)K]f(h)/(a)A(n-1)'
        ],
        'constants': {
            'a': 137.5,  # Divergence angle (golden angle)
            'h': 5,      # Vertical displacement per element
            'r': 15      # Radial offset from central axis
        },
        'iterations': 100,
        'is_3d': True,
        'description': 'ABOP Figure 4.11 - Cylindrical phyllotaxis pattern',
        'category': 'phyllotaxis'
    },
    
    # ABOP - Disc phyllotaxis (sunflower head)
    'abop_phyllotaxis_disc': {
        'type': 'parametric',
        'axiom': 'A(200)',
        'productions': [
            'A(n) : n > 0 -> [f(c*sqrt(n))K]/(a)A(n-1)'
        ],
        'constants': {
            'a': 137.5,  # Golden angle
            'c': 2.0     # Spacing constant
        },
        'iterations': 200,
        'is_3d': False,
        'description': 'ABOP Equation 4.1 - Vogel disc phyllotaxis (sunflower)',
        'category': 'phyllotaxis'
    },
    
    # Conical phyllotaxis (pine cone)
    'abop_phyllotaxis_cone': {
        'type': 'parametric', 
        'axiom': 'A(50)',
        'productions': [
            'A(n) : n > 0 -> [&(cone_angle)f(r)K]f(h)/(a)A(n-1)'
        ],
        'constants': {
            'a': 137.5,
            'h': 3,
            'r': 10,
            'cone_angle': 75  # Angle from vertical
        },
        'iterations': 50,
        'is_3d': True,
        'description': 'ABOP - Conical phyllotaxis (pine cone pattern)',
        'category': 'phyllotaxis'
    },
    
    # Fibonacci spiral
    'abop_fibonacci_spiral': {
        'type': 'parametric',
        'axiom': 'A(34)',  # 34 is a Fibonacci number
        'productions': [
            'A(n) : n > 0 -> [f(c*sqrt(n))/(a*n)K]A(n-1)'
        ],
        'constants': {
            'a': 137.5,
            'c': 3.0
        },
        'iterations': 34,
        'is_3d': False,
        'description': 'ABOP - Fibonacci spiral pattern',
        'category': 'phyllotaxis'
    },
}

# =============================================================================
# Mycelis muralis and other specific plants
# =============================================================================

ABOP_PLANT_PRESETS: Dict[str, Dict[str, Any]] = {
    
    # ABOP L-system 3.5 - Mycelis muralis
    'mycelis_muralis': {
        'type': 'parametric',
        'axiom': '/(90)c(0)FA(0,0)',
        'productions': [
            'A(d,t) : d == 0 & t == 0 -> FA(0,1)',
            'A(d,t) : d > 0 & t == 0 -> A(d-1,1)',
            'A(d,t) : t == 1 -> [-(60)D(0)FK]S(0)FA(d,3)',
            'A(d,t) : t == 3 -> [+(60)D(0)FK]S(0)FA(d,1)',
            'D(t) : t < 5 -> D(t+1)',
            'D(t) : t == 5 -> FD(t+1)',
            'D(t) : t > 5 & t < 10 -> D(t+1)',
            'D(t) : t == 10 -> FFA(5,0)',
            'S(t) : t < 1 -> S(t+1)',
            'S(t) : t == 1 -> FS(2)',
            'S(t) : t > 1 -> S(t+1)',
            'c(t) -> c(t+1)'
        ],
        'constants': {},
        'angle': 60,
        'iterations': 20,
        'is_3d': False,
        'description': 'ABOP L-system 3.5 - Mycelis muralis (wall lettuce)',
        'category': 'abop_plants'
    },
    
    # ABOP - Anabaena (Chapter 6 example)
    'anabaena': {
        'axiom': 'ar',
        'rules': {
            'ar': 'albr',
            'al': 'blar',
            'br': 'ar',
            'bl': 'al'
        },
        'angle': 0,
        'iterations': 10,
        'is_3d': False,
        'description': 'ABOP Figure 6.3 - Anabaena catenula growth',
        'category': 'abop_plants'
    },
}

# =============================================================================
# Combined ABOP Presets
# =============================================================================

ABOP_PRESETS: Dict[str, Dict[str, Any]] = {}
ABOP_PRESETS.update(ABOP_FIGURE_PRESETS)
ABOP_PRESETS.update(ABOP_TREE_PRESETS)
ABOP_PRESETS.update(ABOP_INFLORESCENCE_PRESETS)
ABOP_PRESETS.update(ABOP_PHYLLOTAXIS_PRESETS)
ABOP_PRESETS.update(ABOP_PLANT_PRESETS)


def get_abop_preset(name: str) -> Dict[str, Any]:
    """
    Get an ABOP preset by name.
    
    Args:
        name: Preset name
        
    Returns:
        Preset dictionary
        
    Raises:
        KeyError: If preset not found
    """
    if name in ABOP_PRESETS:
        return ABOP_PRESETS[name].copy()
    raise KeyError(f"Unknown ABOP preset: {name}")


def list_abop_presets(category: str = None) -> list:
    """
    List available ABOP presets.
    
    Args:
        category: Optional category filter
        
    Returns:
        List of preset names
    """
    if category is None:
        return list(ABOP_PRESETS.keys())
    
    return [
        name for name, preset in ABOP_PRESETS.items()
        if preset.get('category') == category
    ]


def get_abop_categories() -> list:
    """Get list of ABOP preset categories."""
    categories = set()
    for preset in ABOP_PRESETS.values():
        if 'category' in preset:
            categories.add(preset['category'])
    return sorted(categories)


# =============================================================================
# Utility: Merge with existing presets
# =============================================================================

def merge_with_existing_presets(existing_presets: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge ABOP presets with existing preset dictionary.
    
    Args:
        existing_presets: Current PRESETS dictionary
        
    Returns:
        Combined dictionary
    """
    merged = dict(existing_presets)
    merged.update(ABOP_PRESETS)
    return merged
