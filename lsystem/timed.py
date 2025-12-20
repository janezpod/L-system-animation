"""
Timed L-Systems for Continuous Growth Animation

Based on ABOP Chapter 6: Animation of Plant Development

Key concepts:
- Modules have age (τ) and lifetime (α, β)
- Productions fire when age reaches terminal value β
- Growth functions control continuous size changes

This module provides smooth, biologically-accurate plant growth animations
by tracking continuous time rather than discrete derivation steps.
"""

import math
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Callable
from enum import Enum


class GrowthFunctionType(Enum):
    """Available growth function types from ABOP."""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    POLYNOMIAL = "polynomial"
    SIGMOIDAL = "sigmoidal"


@dataclass
class TimedModule:
    """
    Module with continuous age tracking (ABOP 6.1).
    
    A timed letter (a, τ) where:
    - a: symbol from alphabet V
    - τ: current age satisfying α ≤ τ ≤ β
    
    Attributes:
        symbol: The L-system symbol
        age: Current age τ
        params: Additional numeric parameters
        min_age: Minimum age α_min (usually initial age)
        terminal_age: Terminal age β when production fires
        growth_function: Type of growth function for size interpolation
    """
    symbol: str
    age: float
    params: Tuple[float, ...] = field(default_factory=tuple)
    min_age: float = 0.0  # α_min
    terminal_age: float = 1.0  # β
    growth_function: GrowthFunctionType = GrowthFunctionType.EXPONENTIAL
    
    def is_terminal(self) -> bool:
        """Check if module has reached terminal age."""
        return self.age >= self.terminal_age
    
    def remaining_time(self) -> float:
        """Time until terminal age."""
        return max(0, self.terminal_age - self.age)
    
    def age_fraction(self) -> float:
        """Get normalized age in [0, 1] range."""
        if self.terminal_age <= self.min_age:
            return 1.0
        return (self.age - self.min_age) / (self.terminal_age - self.min_age)
    
    def get_size(self, base_size: float = 1.0) -> float:
        """
        Calculate current size based on growth function.
        
        ABOP 6.2: g(a, τ) specifies length as function of age.
        
        Args:
            base_size: Maximum size at terminal age
            
        Returns:
            Current size based on age and growth function
        """
        if self.growth_function == GrowthFunctionType.LINEAR:
            return linear_growth(self.age, self.min_age, self.terminal_age, base_size)
        elif self.growth_function == GrowthFunctionType.EXPONENTIAL:
            return exponential_growth(self.age, base_size)
        elif self.growth_function == GrowthFunctionType.SIGMOIDAL:
            return sigmoidal_growth(self.age, self.min_age, self.terminal_age, base_size)
        elif self.growth_function == GrowthFunctionType.POLYNOMIAL:
            return polynomial_growth(self.age, 2, base_size)
        return base_size
    
    def __repr__(self) -> str:
        params_str = f"({','.join(f'{p:.2f}' for p in self.params)})" if self.params else ""
        return f"{self.symbol}{params_str}[τ={self.age:.2f}/{self.terminal_age:.2f}]"


@dataclass
class TimedProduction:
    """
    Timed production: (a, β) → (b₁, α₁)(b₂, α₂)...(bₙ, αₙ)
    
    ABOP Equation 6.1 format.
    
    Attributes:
        predecessor: Symbol that this production matches
        terminal_age: β - age when production fires
        successors: List of (symbol, initial_age, params) for daughter modules
        condition: Optional condition string for conditional productions
        successor_terminal_ages: Optional custom terminal ages for successors
    """
    predecessor: str
    terminal_age: float  # β - when production fires
    successors: List[Tuple[str, float, Tuple[float, ...]]]  # [(symbol, initial_age, params), ...]
    condition: Optional[str] = None
    successor_terminal_ages: Optional[List[float]] = None  # Custom terminal ages
    
    def matches(self, module: TimedModule) -> bool:
        """Check if production applies to module."""
        if module.symbol != self.predecessor:
            return False
        if not module.is_terminal():
            return False
        return True
    
    def apply(self, parent_growth_function: GrowthFunctionType = GrowthFunctionType.EXPONENTIAL) -> List[TimedModule]:
        """
        Generate successor modules.
        
        Args:
            parent_growth_function: Growth function to inherit (if not specified)
            
        Returns:
            List of new TimedModule instances
        """
        result = []
        for i, (sym, age, params) in enumerate(self.successors):
            # Determine terminal age for this successor
            if self.successor_terminal_ages and i < len(self.successor_terminal_ages):
                term_age = self.successor_terminal_ages[i]
            else:
                term_age = self.terminal_age  # Inherit parent's terminal age
            
            result.append(TimedModule(
                symbol=sym,
                age=age,
                params=params,
                min_age=age,
                terminal_age=term_age,
                growth_function=parent_growth_function
            ))
        return result


# =============================================================================
# Growth Functions (ABOP 6.2)
# =============================================================================

def linear_growth(
    age: float, 
    min_age: float, 
    max_age: float, 
    max_size: float
) -> float:
    """
    Linear growth: g(a, τ) = A*τ + B
    
    ABOP Equation 6.5
    
    Size increases linearly from 0 at min_age to max_size at max_age.
    
    Args:
        age: Current age τ
        min_age: Starting age
        max_age: Terminal age
        max_size: Size at terminal age
        
    Returns:
        Current size
    """
    if max_age <= min_age:
        return max_size
    t = (age - min_age) / (max_age - min_age)
    t = max(0.0, min(1.0, t))  # Clamp to [0, 1]
    return max_size * t


def exponential_growth(age: float, scale: float = 1.0) -> float:
    """
    Exponential growth: g(a, τ) = A*e^(B*τ)
    
    ABOP Equation 6.7-6.9:
    B = ln((1 + √5)/2) ≈ 0.4812
    
    This specific value of B (related to the golden ratio) provides 
    first-order continuity for cell division - when a cell divides,
    the sum of daughter cell sizes equals the parent cell size.
    
    Args:
        age: Current age τ
        scale: Base scale factor
        
    Returns:
        Current size
    """
    B = math.log((1 + math.sqrt(5)) / 2)  # ≈ 0.4812, golden ratio connection
    return scale * math.exp(B * age)


def sigmoidal_growth(
    age: float,
    min_age: float,
    max_age: float, 
    max_size: float
) -> float:
    """
    Sigmoidal (S-curve) growth for realistic plant development.
    
    ABOP Equation 1.4: Uses delay chain for S-shaped curve.
    
    Provides smooth acceleration at start and deceleration at end,
    mimicking real plant growth patterns. Uses Hermite interpolation
    for C1 continuity.
    
    Args:
        age: Current age τ
        min_age: Starting age
        max_age: Terminal age
        max_size: Maximum size
        
    Returns:
        Current size following S-curve
    """
    if max_age <= min_age:
        return max_size
    
    t = (age - min_age) / (max_age - min_age)
    t = max(0, min(1, t))  # Clamp to [0, 1]
    
    # Hermite basis function h(t) = 3t² - 2t³ (smooth S-curve)
    # Satisfies: h(0)=0, h(1)=1, h'(0)=0, h'(1)=0
    h = 3 * t * t - 2 * t * t * t
    return max_size * h


def polynomial_growth(
    age: float,
    degree: int,
    scale: float = 1.0
) -> float:
    """
    Polynomial growth of arbitrary degree.
    
    ABOP: Based on Pascal triangle distribution.
    Growth is proportional to binomial coefficient C(n, degree).
    
    Args:
        age: Current age (integer component used)
        degree: Polynomial degree
        scale: Scale factor
        
    Returns:
        Growth value
    """
    n = int(age)
    if n < degree:
        return scale * (age ** degree) / math.factorial(degree)
    
    # Binomial coefficient for integer ages
    coeff = math.comb(n, degree)
    return scale * coeff


def delayed_sigmoidal_growth(
    age: float,
    delay_k: int = 5,
    rise_l: int = 10,
    max_size: float = 1.0
) -> float:
    """
    Delayed sigmoidal growth using ABOP delay chain.
    
    ABOP Section 1.3.3: Two-stage growth with delay.
    Stage 1: a_i → a_{i+1} b_0 for i < k (delay period)
    Stage 2: b_j → b_{j+1} F for j < l (growth period)
    
    Args:
        age: Current time step
        delay_k: Number of delay steps before growth starts
        rise_l: Number of steps for growth period
        max_size: Final size
        
    Returns:
        Current size
    """
    if age < delay_k:
        return 0.0
    
    growth_age = age - delay_k
    if growth_age >= rise_l:
        return max_size
    
    # Linear rise during growth period
    return max_size * (growth_age / rise_l)


# =============================================================================
# Timed DOL-System
# =============================================================================

class TimedDOLSystem:
    """
    Deterministic timed L-system (tDOL).
    
    ABOP Definition: G = <V, ω, P> with timed letters and productions.
    
    Key property (Theorem 6.1):
    D(D((a₀, τ₀), tₐ), tᵦ) = D((a₀, τ₀), tₐ + tᵦ)
    
    Derivation of duration t starting from state s gives same result
    regardless of how we partition t. This enables smooth interpolation
    between any two time points.
    
    Attributes:
        axiom: Initial list of timed modules
        productions: List of timed productions
        time_step: Default time increment for derivation
        default_growth_function: Growth function for new modules
    """
    
    def __init__(
        self,
        axiom: List[TimedModule],
        productions: List[TimedProduction],
        time_step: float = 0.1,
        default_growth_function: GrowthFunctionType = GrowthFunctionType.EXPONENTIAL
    ):
        self.axiom = axiom
        self.productions = productions
        self.time_step = time_step
        self.default_growth_function = default_growth_function
        
        # Build production index for fast lookup
        self._prod_index: Dict[str, List[TimedProduction]] = {}
        for prod in productions:
            if prod.predecessor not in self._prod_index:
                self._prod_index[prod.predecessor] = []
            self._prod_index[prod.predecessor].append(prod)
    
    def derive(self, duration: float) -> List[List[TimedModule]]:
        """
        Continuous derivation over time duration.
        
        Returns sequence of states at each time step, suitable for
        generating animation frames.
        
        Args:
            duration: Total time to simulate
            
        Returns:
            List of module lists, one per time step
        """
        states = []
        current = list(self.axiom)
        elapsed = 0.0
        
        while elapsed < duration:
            states.append([m for m in current])  # Copy current state
            
            # Advance time
            dt = min(self.time_step, duration - elapsed)
            current = self._advance_time(current, dt)
            
            # Apply productions to terminal modules
            current = self._apply_productions(current)
            
            elapsed += dt
        
        # Add final state
        states.append([m for m in current])
        
        return states
    
    def derive_to_iteration(self, target_iterations: int) -> List[List[TimedModule]]:
        """
        Derive until reaching target number of production applications.
        
        Useful for matching discrete L-system iterations.
        
        Args:
            target_iterations: Number of production firings to reach
            
        Returns:
            List of states
        """
        states = []
        current = list(self.axiom)
        iterations = 0
        
        while iterations < target_iterations:
            states.append([m for m in current])
            
            # Check how many modules will fire
            will_fire = sum(1 for m in current if m.is_terminal() and m.symbol in self._prod_index)
            
            if will_fire == 0:
                # Advance time until at least one module becomes terminal
                min_remaining = min(
                    (m.remaining_time() for m in current if not m.is_terminal()),
                    default=self.time_step
                )
                current = self._advance_time(current, max(min_remaining, self.time_step))
            
            current = self._apply_productions(current)
            iterations += 1
        
        states.append([m for m in current])
        return states
    
    def _advance_time(
        self, 
        modules: List[TimedModule], 
        dt: float
    ) -> List[TimedModule]:
        """Advance age of all modules by dt."""
        return [
            TimedModule(
                symbol=m.symbol,
                age=m.age + dt,
                params=m.params,
                min_age=m.min_age,
                terminal_age=m.terminal_age,
                growth_function=m.growth_function
            )
            for m in modules
        ]
    
    def _apply_productions(
        self, 
        modules: List[TimedModule]
    ) -> List[TimedModule]:
        """Apply matching productions to terminal modules."""
        result = []
        
        for module in modules:
            if not module.is_terminal():
                result.append(module)
                continue
            
            # Find matching production
            matched = False
            if module.symbol in self._prod_index:
                for prod in self._prod_index[module.symbol]:
                    if prod.matches(module):
                        result.extend(prod.apply(module.growth_function))
                        matched = True
                        break
            
            if not matched:
                # Identity production - module persists with reset age
                result.append(TimedModule(
                    symbol=module.symbol,
                    age=module.min_age,  # Reset age
                    params=module.params,
                    min_age=module.min_age,
                    terminal_age=module.terminal_age,
                    growth_function=module.growth_function
                ))
        
        return result
    
    def get_interpolated_state(
        self, 
        modules: List[TimedModule]
    ) -> List[Tuple[str, float, Tuple[float, ...]]]:
        """
        Get modules with interpolated sizes based on age.
        
        Used for smooth animation between discrete states.
        
        Args:
            modules: Current module list
            
        Returns:
            List of (symbol, current_size, params) tuples
        """
        return [
            (m.symbol, m.get_size(), m.params)
            for m in modules
        ]
    
    def to_lstring(self, modules: List[TimedModule]) -> str:
        """
        Convert timed modules to standard L-system string.
        
        Args:
            modules: List of timed modules
            
        Returns:
            String representation for turtle interpretation
        """
        return ''.join(m.symbol for m in modules)
    
    def get_module_sizes(
        self, 
        modules: List[TimedModule],
        base_size: float = 10.0
    ) -> Dict[int, float]:
        """
        Get size for each F module based on growth function.
        
        Args:
            modules: Current module list
            base_size: Maximum segment length
            
        Returns:
            Dictionary mapping module index to size
        """
        sizes = {}
        for i, m in enumerate(modules):
            if m.symbol in ('F', 'f', 'G'):
                sizes[i] = m.get_size(base_size)
        return sizes


# =============================================================================
# Continuity Verification (ABOP 6.2.1)
# =============================================================================

def verify_continuity(
    production: TimedProduction,
    growth_funcs: Dict[str, Callable[[float], float]],
    order: int = 0
) -> Tuple[bool, str]:
    """
    Verify continuity requirements R1 and R2.
    
    ABOP Equation 6.3: g(a, β) = Σᵢ g(bᵢ, αᵢ)
    
    For order N, equation 6.6:
    g⁽ᵏ⁾(a, β) = Σᵢ g⁽ᵏ⁾(bᵢ, αᵢ) for k = 0, 1, ..., N
    
    Args:
        production: Production to verify
        growth_funcs: Dictionary of growth functions by symbol
        order: Continuity order to check (0 = size, 1 = velocity, etc.)
        
    Returns:
        Tuple of (is_valid, message)
    """
    predecessor_symbol = production.predecessor
    terminal_age = production.terminal_age
    
    if predecessor_symbol not in growth_funcs:
        return True, "No growth function defined for predecessor"
    
    parent_value = growth_funcs[predecessor_symbol](terminal_age)
    
    child_sum = 0.0
    for symbol, initial_age, _ in production.successors:
        if symbol in growth_funcs:
            child_sum += growth_funcs[symbol](initial_age)
    
    # Check if parent length equals sum of children
    epsilon = 1e-6
    if abs(parent_value - child_sum) < epsilon:
        return True, f"Continuity verified: parent={parent_value:.4f}, children_sum={child_sum:.4f}"
    else:
        return False, f"Continuity violation: parent={parent_value:.4f}, children_sum={child_sum:.4f}"


# =============================================================================
# Example Systems (ABOP Chapter 6)
# =============================================================================

def create_anabaena_system() -> TimedDOLSystem:
    """
    ABOP timed L-system for Anabaena catenula (blue-green algae).
    
    From Figure 6.3 and equation 6.2:
    ω: (aᵣ, 1)
    p₁: (aᵣ, 2) → (aₗ, 1)(bᵣ, 0)
    p₂: (aₗ, 2) → (bₗ, 0)(aᵣ, 1)
    p₃: (bᵣ, 1) → (aᵣ, 0)
    p₄: (bₗ, 1) → (aₗ, 0)
    
    Models the asymmetric cell division pattern in this filamentous organism.
    'a' cells are larger vegetative cells, 'b' cells are smaller heterocysts.
    Subscripts r/l indicate division polarity.
    
    Returns:
        Configured TimedDOLSystem
    """
    axiom = [
        TimedModule('ar', age=1.0, terminal_age=2.0, 
                   growth_function=GrowthFunctionType.LINEAR)
    ]
    
    productions = [
        TimedProduction(
            predecessor='ar',
            terminal_age=2.0,
            successors=[('al', 1.0, ()), ('br', 0.0, ())],
            successor_terminal_ages=[2.0, 1.0]
        ),
        TimedProduction(
            predecessor='al', 
            terminal_age=2.0,
            successors=[('bl', 0.0, ()), ('ar', 1.0, ())],
            successor_terminal_ages=[1.0, 2.0]
        ),
        TimedProduction(
            predecessor='br',
            terminal_age=1.0,
            successors=[('ar', 0.0, ())],
            successor_terminal_ages=[2.0]
        ),
        TimedProduction(
            predecessor='bl',
            terminal_age=1.0,
            successors=[('al', 0.0, ())],
            successor_terminal_ages=[2.0]
        ),
    ]
    
    return TimedDOLSystem(axiom, productions, time_step=0.1)


def create_simple_tree_system(
    growth_time: float = 5.0,
    branch_angle: float = 25.0
) -> TimedDOLSystem:
    """
    Simple timed tree system for demonstrating growth animation.
    
    Axiom: A(0)
    A reaching terminal age produces: F A [+A] [-A]
    
    Args:
        growth_time: Time for each segment to fully grow
        branch_angle: Branching angle in degrees
        
    Returns:
        Configured TimedDOLSystem
    """
    axiom = [
        TimedModule('A', age=0.0, terminal_age=growth_time,
                   growth_function=GrowthFunctionType.SIGMOIDAL)
    ]
    
    productions = [
        TimedProduction(
            predecessor='A',
            terminal_age=growth_time,
            successors=[
                ('F', 0.0, ()),
                ('A', 0.0, ()),
                ('[', 0.0, ()),
                ('+', 0.0, (branch_angle,)),
                ('A', 0.0, ()),
                (']', 0.0, ()),
                ('[', 0.0, ()),
                ('-', 0.0, (branch_angle,)),
                ('A', 0.0, ()),
                (']', 0.0, ()),
            ],
            successor_terminal_ages=[growth_time] * 10
        ),
    ]
    
    return TimedDOLSystem(axiom, productions, time_step=0.1,
                         default_growth_function=GrowthFunctionType.SIGMOIDAL)


def create_continuous_growth_tree(
    terminal_age: float = 1.0,
    elongation_rate: float = 1.109,
    width_ratio: float = 0.707
) -> TimedDOLSystem:
    """
    Continuous growth tree based on ABOP Figure 2.8.
    
    Uses exponential growth with golden-ratio-based parameters
    for botanically realistic development.
    
    Args:
        terminal_age: Base terminal age for modules
        elongation_rate: Length growth rate
        width_ratio: Width decay ratio (0.707 = Leonardo's rule)
        
    Returns:
        Configured TimedDOLSystem
    """
    axiom = [
        TimedModule('!', age=0.0, params=(1.0,), terminal_age=terminal_age),
        TimedModule('F', age=0.0, params=(10.0,), terminal_age=terminal_age),
        TimedModule('/', age=0.0, params=(45.0,), terminal_age=0.01),
        TimedModule('A', age=0.0, terminal_age=terminal_age),
    ]
    
    # A → !(vr)F(50)[&(a)F(50)A]/(d1)[&(a)F(50)A]/(d2)[&(a)F(50)A]
    branch_successors = [
        ('!', 0.0, (width_ratio,)),
        ('F', 0.0, (50.0,)),
        ('[', 0.0, ()),
        ('&', 0.0, (18.95,)),
        ('F', 0.0, (50.0,)),
        ('A', 0.0, ()),
        (']', 0.0, ()),
        ('/', 0.0, (94.74,)),
        ('[', 0.0, ()),
        ('&', 0.0, (18.95,)),
        ('F', 0.0, (50.0,)),
        ('A', 0.0, ()),
        (']', 0.0, ()),
        ('/', 0.0, (132.63,)),
        ('[', 0.0, ()),
        ('&', 0.0, (18.95,)),
        ('F', 0.0, (50.0,)),
        ('A', 0.0, ()),
        (']', 0.0, ()),
    ]
    
    productions = [
        TimedProduction(
            predecessor='A',
            terminal_age=terminal_age,
            successors=branch_successors
        ),
        # F grows continuously
        TimedProduction(
            predecessor='F',
            terminal_age=terminal_age,
            successors=[('F', 0.0, ())]  # F persists
        ),
    ]
    
    return TimedDOLSystem(axiom, productions, time_step=0.05,
                         default_growth_function=GrowthFunctionType.EXPONENTIAL)


# =============================================================================
# Animation Utilities
# =============================================================================

def interpolate_states(
    state1: List[TimedModule],
    state2: List[TimedModule],
    t: float
) -> List[TimedModule]:
    """
    Interpolate between two timed states.
    
    For animation frames between discrete derivation steps.
    
    Args:
        state1: Earlier state
        state2: Later state
        t: Interpolation factor in [0, 1]
        
    Returns:
        Interpolated state
    """
    # Simple approach: interpolate ages of matching modules
    if len(state1) != len(state2):
        # States have different structure - return weighted choice
        return state1 if t < 0.5 else state2
    
    result = []
    for m1, m2 in zip(state1, state2):
        if m1.symbol == m2.symbol:
            interpolated_age = m1.age + t * (m2.age - m1.age)
            result.append(TimedModule(
                symbol=m1.symbol,
                age=interpolated_age,
                params=m1.params,  # Keep params from first state
                min_age=m1.min_age,
                terminal_age=m1.terminal_age,
                growth_function=m1.growth_function
            ))
        else:
            result.append(m2 if t > 0.5 else m1)
    
    return result


def timed_to_parametric_modules(
    modules: List[TimedModule],
    base_length: float = 10.0
) -> List[Tuple[str, Tuple[float, ...]]]:
    """
    Convert timed modules to parametric format for turtle interpretation.
    
    Args:
        modules: Timed modules with growth information
        base_length: Base segment length
        
    Returns:
        List of (symbol, params) tuples where F has length based on growth
    """
    result = []
    for m in modules:
        if m.symbol in ('F', 'f', 'G'):
            # Use growth function to determine current length
            length = m.get_size(base_length)
            result.append((m.symbol, (length,)))
        elif m.params:
            result.append((m.symbol, m.params))
        else:
            result.append((m.symbol, ()))
    return result
