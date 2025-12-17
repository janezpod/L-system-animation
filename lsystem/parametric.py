"""
Parametric L-System Engine

Supports parameterized modules, conditional productions, and stochastic selection.
Based on ABOP (The Algorithmic Beauty of Plants) Chapter 1.10.

Features:
- Parameterized modules: A(x, y), F(length), +(angle)
- Conditional productions: A(l, w) : l > 1 → F(l)[+A(l*0.6, w*0.7)][-A(l*0.6, w*0.7)]
- Stochastic productions: Multiple rules with probabilities
- Named constants: R1, WR, etc.
- Context-sensitive productions: A < B > C → D (optional)

Example:
    axiom: A(1, 10)
    p1: A(l, w) : l > 1 → F(l)[+A(l*0.6, w*0.7)][-A(l*0.6, w*0.7)]
    p2: A(l, w) : l <= 1 → F(l)
    p3: F(l) → F(l * 1.1)
"""

import re
import random
import math
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any, Union
from functools import lru_cache


class ParametricLSystemError(Exception):
    """Exception raised for parametric L-system errors."""
    pass


@dataclass
class Module:
    """
    A parameterized L-system module.
    
    Represents a symbol with optional numeric parameters.
    Examples: A(1, 2), F(10.5), +, [-
    """
    symbol: str
    params: Tuple[float, ...] = field(default_factory=tuple)
    
    def __repr__(self) -> str:
        if self.params:
            params_str = ','.join(f'{p:.4g}' for p in self.params)
            return f"{self.symbol}({params_str})"
        return self.symbol
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Module):
            return False
        if self.symbol != other.symbol:
            return False
        if len(self.params) != len(other.params):
            return False
        # Use approximate comparison for floats
        for a, b in zip(self.params, other.params):
            if abs(a - b) > 1e-9:
                return False
        return True
    
    def __hash__(self) -> int:
        return hash((self.symbol, self.params))
    
    def matches_symbol(self, symbol: str, param_count: Optional[int] = None) -> bool:
        """Check if module matches a production predecessor."""
        if self.symbol != symbol:
            return False
        if param_count is not None and len(self.params) != param_count:
            return False
        return True


@dataclass
class Production:
    """
    A parametric L-system production rule.
    
    Format: predecessor(params) : condition → successor
    
    Attributes:
        predecessor: Symbol name (single character)
        formal_params: Parameter names tuple, e.g., ("l", "w")
        condition: Optional boolean expression, e.g., "l > 5"
        successor: Successor template string, e.g., "F(l)[+A(l*0.6)]"
        probability: Weight for stochastic selection (default 1.0)
        left_context: Optional left context symbol
        right_context: Optional right context symbol
    """
    predecessor: str
    formal_params: Tuple[str, ...] = field(default_factory=tuple)
    condition: Optional[str] = None
    successor: str = ""
    probability: float = 1.0
    left_context: Optional[str] = None
    right_context: Optional[str] = None
    
    def matches(self, module: Module, params_dict: Dict[str, float]) -> bool:
        """
        Check if this production matches the given module.
        
        Args:
            module: Module to match against
            params_dict: Dictionary mapping parameter names to values
            
        Returns:
            True if production matches
        """
        if module.symbol != self.predecessor:
            return False
        if len(module.params) != len(self.formal_params):
            return False
        if self.condition:
            return self._eval_condition(params_dict)
        return True
    
    def _eval_condition(self, params: Dict[str, float]) -> bool:
        """Safely evaluate condition expression."""
        if not self.condition:
            return True
        
        expr = self.condition
        # Replace parameter names with values
        for name, value in params.items():
            expr = re.sub(rf'\b{re.escape(name)}\b', str(value), expr)
        
        try:
            # Safe evaluation with math functions
            return bool(eval(expr, {"__builtins__": {}}, {
                "sqrt": math.sqrt, 
                "abs": abs, 
                "sin": math.sin,
                "cos": math.cos, 
                "tan": math.tan,
                "min": min, 
                "max": max,
                "pi": math.pi,
                "e": math.e
            }))
        except Exception:
            return False
    
    def apply(
        self, 
        params: Dict[str, float],
        constants: Optional[Dict[str, float]] = None
    ) -> List[Module]:
        """
        Apply production, substituting parameters.
        
        Args:
            params: Dictionary mapping formal parameter names to values
            constants: Optional dictionary of named constants
            
        Returns:
            List of Module objects representing the successor
        """
        all_params = dict(params)
        if constants:
            all_params.update(constants)
        return parse_parametric_word(self.successor, all_params)


# =============================================================================
# Parsing Functions
# =============================================================================

def _eval_expr(expr: str, params: Dict[str, float]) -> float:
    """
    Evaluate arithmetic expression with parameter substitution.
    
    Args:
        expr: Expression string, e.g., "l*0.9+w"
        params: Parameter values to substitute
        
    Returns:
        Evaluated numeric result
    """
    # Substitute parameter names with values
    result_expr = expr
    for name, value in params.items():
        result_expr = re.sub(rf'\b{re.escape(name)}\b', str(value), result_expr)
    
    try:
        return float(eval(result_expr, {"__builtins__": {}}, {
            "sqrt": math.sqrt,
            "abs": abs,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "exp": math.exp,
            "min": min,
            "max": max,
            "pi": math.pi,
            "e": math.e,
            "pow": pow
        }))
    except Exception:
        return 0.0


def parse_parametric_word(
    word: str, 
    params: Optional[Dict[str, float]] = None
) -> List[Module]:
    """
    Parse a parametric word string into modules.
    
    Args:
        word: String like "A(1,2)F(3)B" or "F(l*0.9)[+A(l,w)]"
        params: Parameter substitutions for expressions
    
    Returns:
        List of Module objects
        
    Examples:
        >>> parse_parametric_word("A(1,2)F(3)")
        [Module('A', (1.0, 2.0)), Module('F', (3.0,))]
        >>> parse_parametric_word("F(l*0.9)", {"l": 10})
        [Module('F', (9.0,))]
    """
    if params is None:
        params = {}
    
    modules = []
    i = 0
    
    while i < len(word):
        char = word[i]
        
        # Check for parameterized module: Symbol(expr, expr, ...)
        if char.isalpha() and i + 1 < len(word) and word[i + 1] == '(':
            symbol = char
            # Find matching closing parenthesis
            paren_depth = 1
            start = i + 2
            j = start
            while j < len(word) and paren_depth > 0:
                if word[j] == '(':
                    paren_depth += 1
                elif word[j] == ')':
                    paren_depth -= 1
                j += 1
            
            # Extract and parse parameters
            param_str = word[start:j-1]
            if param_str.strip():
                # Split by comma, respecting nested parentheses
                expr_list = _split_params(param_str)
                values = tuple(_eval_expr(e.strip(), params) for e in expr_list)
            else:
                values = ()
            
            modules.append(Module(symbol, values))
            i = j
            
        # Simple symbol (including special characters)
        elif char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            modules.append(Module(char))
            i += 1
        elif char in '+-[]&^/\\|!$.\'"{}%~':
            modules.append(Module(char))
            i += 1
        else:
            # Skip whitespace and unrecognized characters
            i += 1
    
    return modules


def _split_params(param_str: str) -> List[str]:
    """
    Split parameter string by commas, respecting nested parentheses.
    
    Args:
        param_str: String like "l*0.9, w*wr, sqrt(x)"
        
    Returns:
        List of parameter expression strings
    """
    result = []
    current = []
    paren_depth = 0
    
    for char in param_str:
        if char == '(':
            paren_depth += 1
            current.append(char)
        elif char == ')':
            paren_depth -= 1
            current.append(char)
        elif char == ',' and paren_depth == 0:
            result.append(''.join(current))
            current = []
        else:
            current.append(char)
    
    if current:
        result.append(''.join(current))
    
    return result


def parse_production_string(prod_str: str) -> Production:
    """
    Parse a production from ABOP-style string notation.
    
    Supported formats:
        "A(x,y) : x > 5 → B(x+1)C(y)"
        "F(l) → F(l*1.1)"
        "A → B[+A][-A]"
        "F → FF"
        
    The arrow can be either '→' (Unicode) or '->' (ASCII).
    
    Args:
        prod_str: Production string in ABOP notation
        
    Returns:
        Production object
        
    Raises:
        ValueError: If string cannot be parsed
    """
    # Normalize arrow notation
    prod_str = prod_str.replace('->', '→')
    
    parts = prod_str.split('→')
    if len(parts) != 2:
        raise ValueError(f"Invalid production (missing arrow): {prod_str}")
    
    left = parts[0].strip()
    successor = parts[1].strip()
    
    # Check for condition
    if ':' in left:
        pred_part, condition = left.split(':', 1)
        condition = condition.strip()
    else:
        pred_part = left
        condition = None
    
    # Check for context sensitivity: A < B > C
    left_context = None
    right_context = None
    
    if '<' in pred_part and '>' not in pred_part.split('<')[1].split('(')[0]:
        # Format: A < B
        ctx_parts = pred_part.split('<')
        left_context = ctx_parts[0].strip()
        pred_part = ctx_parts[1].strip()
    
    if '>' in pred_part:
        # Format: B > C
        ctx_parts = pred_part.split('>')
        pred_part = ctx_parts[0].strip()
        right_context = ctx_parts[1].strip()
    
    # Parse predecessor with parameters
    pred_match = re.match(r'([A-Za-z])\(([^)]*)\)', pred_part.strip())
    if pred_match:
        predecessor = pred_match.group(1)
        param_str = pred_match.group(2).strip()
        if param_str:
            formal_params = tuple(p.strip() for p in param_str.split(','))
        else:
            formal_params = ()
    else:
        predecessor = pred_part.strip()
        formal_params = ()
    
    return Production(
        predecessor=predecessor,
        formal_params=formal_params,
        condition=condition,
        successor=successor,
        left_context=left_context,
        right_context=right_context
    )


def parse_stochastic_production(
    rule_str: str, 
    probability: float = 1.0
) -> Production:
    """
    Parse a stochastic production with probability.
    
    Args:
        rule_str: Production string
        probability: Probability weight for this production
        
    Returns:
        Production object with probability set
    """
    prod = parse_production_string(rule_str)
    prod.probability = probability
    return prod


# =============================================================================
# Parametric L-System Class
# =============================================================================

class ParametricLSystem:
    """
    Parametric L-system processor.
    
    Supports all ABOP features:
    - Parameterized modules: A(x,y), F(length), +(angle)
    - Conditional productions: A(x) : x > 5 → B(x-1)
    - Stochastic selection: Multiple productions with probabilities
    - Named constants: R1, WR, etc.
    - Context-sensitive productions (optional)
    
    Example usage:
        >>> prods = [
        ...     Production("A", ("l",), "l < 10", "F(l)A(l+1)"),
        ...     Production("A", ("l",), "l >= 10", "F(l)"),
        ... ]
        >>> lsys = ParametricLSystem("A(1)", prods, iterations=5)
        >>> result = lsys.generate()
        >>> lsys.to_string(result)
        'FFFFFF'
    """
    
    MAX_MODULES = 1_000_000
    
    def __init__(
        self,
        axiom: str,
        productions: List[Union[Production, str, dict]],
        iterations: int = 1,
        random_seed: Optional[int] = None,
        constants: Optional[Dict[str, float]] = None,
        ignore_symbols: str = ""
    ):
        """
        Initialize parametric L-system.
        
        Args:
            axiom: Initial parametric word (e.g., "A(1,10)")
            productions: List of Production objects, strings, or dicts
            iterations: Number of derivation steps
            random_seed: For reproducible stochastic behavior
            constants: Named constants for expressions (e.g., {"R1": 0.9})
            ignore_symbols: Symbols to ignore in context matching
        """
        self.constants = constants or {}
        self.axiom = parse_parametric_word(axiom, self.constants)
        self.iterations = iterations
        self.ignore_symbols = set(ignore_symbols)
        
        # Parse productions into Production objects
        self.productions: List[Production] = []
        for p in productions:
            if isinstance(p, Production):
                self.productions.append(p)
            elif isinstance(p, str):
                self.productions.append(parse_production_string(p))
            elif isinstance(p, dict):
                # Dict format: {"rule": "...", "probability": 0.5}
                rule = p.get("rule", p.get("production", ""))
                prob = p.get("probability", 1.0)
                self.productions.append(parse_stochastic_production(rule, prob))
        
        if random_seed is not None:
            random.seed(random_seed)
        self._random_seed = random_seed
        
        # Index productions by predecessor for fast lookup
        self._prod_index: Dict[str, List[Production]] = {}
        for prod in self.productions:
            if prod.predecessor not in self._prod_index:
                self._prod_index[prod.predecessor] = []
            self._prod_index[prod.predecessor].append(prod)
    
    def _get_matching_productions(
        self, 
        module: Module,
        left_context: Optional[Module] = None,
        right_context: Optional[Module] = None
    ) -> List[Tuple[Production, Dict[str, float]]]:
        """
        Find all productions matching a module.
        
        Args:
            module: Module to find productions for
            left_context: Optional left neighbor for context-sensitive matching
            right_context: Optional right neighbor for context-sensitive matching
            
        Returns:
            List of (production, params_dict) tuples for matching productions
        """
        if module.symbol not in self._prod_index:
            return []
        
        matches = []
        for prod in self._prod_index[module.symbol]:
            if len(prod.formal_params) != len(module.params):
                continue
            
            # Check context if required
            if prod.left_context and (not left_context or 
                                      left_context.symbol != prod.left_context):
                continue
            if prod.right_context and (not right_context or 
                                       right_context.symbol != prod.right_context):
                continue
            
            # Build parameter dictionary
            params = dict(zip(prod.formal_params, module.params))
            params.update(self.constants)
            
            if prod.matches(module, params):
                matches.append((prod, params))
        
        return matches
    
    def _select_production(
        self, 
        matches: List[Tuple[Production, Dict[str, float]]]
    ) -> Optional[Tuple[Production, Dict[str, float]]]:
        """
        Select one production from matches (stochastic if multiple).
        
        Uses weighted random selection based on production probabilities.
        """
        if not matches:
            return None
        if len(matches) == 1:
            return matches[0]
        
        # Weighted random selection
        total = sum(p.probability for p, _ in matches)
        r = random.random() * total
        cumulative = 0.0
        for prod, params in matches:
            cumulative += prod.probability
            if r <= cumulative:
                return (prod, params)
        return matches[-1]
    
    def _get_context_neighbors(
        self, 
        modules: List[Module], 
        index: int
    ) -> Tuple[Optional[Module], Optional[Module]]:
        """
        Get left and right context neighbors, skipping ignored symbols.
        """
        left = None
        right = None
        
        # Find left neighbor
        for i in range(index - 1, -1, -1):
            if modules[i].symbol not in self.ignore_symbols:
                left = modules[i]
                break
        
        # Find right neighbor
        for i in range(index + 1, len(modules)):
            if modules[i].symbol not in self.ignore_symbols:
                right = modules[i]
                break
        
        return left, right
    
    def generate(self, iterations: Optional[int] = None) -> List[Module]:
        """
        Generate L-system after iterations.
        
        Args:
            iterations: Override default iteration count
            
        Returns:
            List of Module objects representing final state
            
        Raises:
            ParametricLSystemError: If maximum modules exceeded
        """
        if iterations is None:
            iterations = self.iterations
        
        current = list(self.axiom)
        
        for step in range(iterations):
            next_modules = []
            
            for i, module in enumerate(current):
                # Get context for context-sensitive matching
                left, right = self._get_context_neighbors(current, i)
                
                matches = self._get_matching_productions(module, left, right)
                selected = self._select_production(matches)
                
                if selected:
                    prod, params = selected
                    next_modules.extend(prod.apply(params, self.constants))
                else:
                    # No matching production - module persists
                    next_modules.append(module)
                
                if len(next_modules) > self.MAX_MODULES:
                    raise ParametricLSystemError(
                        f"Exceeded max modules ({self.MAX_MODULES}). "
                        "Try reducing iterations."
                    )
            
            current = next_modules
        
        return current
    
    def to_string(self, modules: Optional[List[Module]] = None) -> str:
        """
        Convert modules to string for turtle interpretation.
        
        For parametric modules, only the symbol is included in the string.
        Use get_module_params() to access parameter values.
        
        Args:
            modules: Modules to convert (generates if None)
            
        Returns:
            String suitable for turtle interpreter
        """
        if modules is None:
            modules = self.generate()
        
        return ''.join(m.symbol for m in modules)
    
    def get_module_params(
        self, 
        modules: Optional[List[Module]] = None
    ) -> Dict[int, Tuple[float, ...]]:
        """
        Get parameter values indexed by position.
        
        Useful for turtle interpreter to access F(length), +(angle) values.
        
        Args:
            modules: Modules to extract params from (generates if None)
            
        Returns:
            Dictionary mapping position to parameter tuple
        """
        if modules is None:
            modules = self.generate()
        
        return {i: m.params for i, m in enumerate(modules) if m.params}
    
    def count_symbols(
        self, 
        modules: Optional[List[Module]] = None,
        symbol: str = 'F'
    ) -> int:
        """Count occurrences of a symbol."""
        if modules is None:
            modules = self.generate()
        return sum(1 for m in modules if m.symbol == symbol)
    
    def reset_random(self) -> None:
        """Reset random seed for reproducible re-runs."""
        if self._random_seed is not None:
            random.seed(self._random_seed)


# =============================================================================
# Convenience Functions
# =============================================================================

def create_parametric_lsystem_from_preset(preset: dict) -> ParametricLSystem:
    """
    Create a ParametricLSystem from a preset dictionary.
    
    Expected preset format:
        {
            "type": "parametric",
            "axiom": "A(1,10)",
            "productions": [...],  # List of strings or dicts
            "constants": {"R1": 0.9},
            "iterations": 10
        }
    
    Args:
        preset: Preset dictionary
        
    Returns:
        Configured ParametricLSystem instance
    """
    return ParametricLSystem(
        axiom=preset["axiom"],
        productions=preset.get("productions", []),
        iterations=preset.get("iterations", 5),
        constants=preset.get("constants"),
        random_seed=preset.get("random_seed")
    )
