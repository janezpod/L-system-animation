"""
L-System Engine

Implements a standard L-system processor with memoization and safety limits.
"""

from functools import lru_cache
from typing import Dict, Optional


class LSystemError(Exception):
    """Exception raised for L-system processing errors."""
    pass


class LSystem:
    """
    L-System processor.
    
    Supports standard L-system symbols:
    - F: move forward and draw
    - f: move forward without drawing
    - +: turn left by angle delta
    - -: turn right by angle delta
    - [: push current state to stack
    - ]: pop state from stack
    - X, Y, A, B: placeholder symbols for rule expansion
    """
    
    MAX_STRING_LENGTH = 10_000_000  # Safety limit: 10 million characters
    
    def __init__(self, axiom: str, rules: Dict[str, str], iterations: int = 1):
        """
        Initialize L-System.
        
        Args:
            axiom: Starting string
            rules: Production rules as dict {symbol: replacement}
            iterations: Number of iterations to apply
        """
        self.axiom = axiom
        self.rules = rules
        self.iterations = iterations
        self._cache: Dict[tuple, str] = {}
    
    def _apply_rules(self, string: str) -> str:
        """
        Apply production rules once to a string.
        
        Args:
            string: Input string to transform
            
        Returns:
            Transformed string with rules applied
            
        Raises:
            LSystemError: If result exceeds maximum length
        """
        result = []
        for char in string:
            # Apply rule if it exists, otherwise keep the character
            replacement = self.rules.get(char, char)
            result.append(replacement)
            
            # Check length periodically to avoid memory issues
            if len(result) > 1000 and sum(len(s) for s in result) > self.MAX_STRING_LENGTH:
                raise LSystemError(
                    f"L-system string exceeded maximum length of {self.MAX_STRING_LENGTH:,} characters. "
                    "Try reducing iterations."
                )
        
        return ''.join(result)
    
    def generate(self, iterations: Optional[int] = None) -> str:
        """
        Generate the L-system string after n iterations.
        
        Args:
            iterations: Number of iterations (uses self.iterations if not specified)
            
        Returns:
            Fully expanded L-system string
            
        Raises:
            LSystemError: If result exceeds maximum length
        """
        if iterations is None:
            iterations = self.iterations
        
        # Check cache
        cache_key = (self.axiom, tuple(sorted(self.rules.items())), iterations)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Build up from cached results if available
        current = self.axiom
        start_iteration = 0
        
        # Check if we have any intermediate results cached
        for i in range(iterations - 1, 0, -1):
            intermediate_key = (self.axiom, tuple(sorted(self.rules.items())), i)
            if intermediate_key in self._cache:
                current = self._cache[intermediate_key]
                start_iteration = i
                break
        
        # Apply rules for remaining iterations
        for i in range(start_iteration, iterations):
            current = self._apply_rules(current)
            
            # Check length after each iteration
            if len(current) > self.MAX_STRING_LENGTH:
                raise LSystemError(
                    f"L-system string exceeded maximum length of {self.MAX_STRING_LENGTH:,} characters "
                    f"at iteration {i + 1}. Try reducing iterations."
                )
            
            # Cache intermediate result
            intermediate_key = (self.axiom, tuple(sorted(self.rules.items())), i + 1)
            self._cache[intermediate_key] = current
        
        return current
    
    def get_drawing_symbols(self) -> set:
        """Return set of symbols that cause drawing (F)."""
        return {'F'}
    
    def get_move_symbols(self) -> set:
        """Return set of symbols that cause movement without drawing (f)."""
        return {'f'}
    
    def count_segments(self, string: Optional[str] = None) -> int:
        """
        Count the number of drawable segments (F symbols) in the string.
        
        Args:
            string: String to count (generates if not provided)
            
        Returns:
            Number of F symbols
        """
        if string is None:
            string = self.generate()
        return string.count('F')
    
    def __repr__(self) -> str:
        return (
            f"LSystem(axiom='{self.axiom}', "
            f"rules={self.rules}, "
            f"iterations={self.iterations})"
        )


def parse_rules(rules_string: str) -> Dict[str, str]:
    """
    Parse rules from command-line format.
    
    Args:
        rules_string: Rules in format "A:replacement,B:replacement"
        
    Returns:
        Dictionary of rules
        
    Example:
        >>> parse_rules("F:F[-F][+F],X:FX")
        {'F': 'F[-F][+F]', 'X': 'FX'}
    """
    rules = {}
    for rule in rules_string.split(','):
        if ':' in rule:
            symbol, replacement = rule.split(':', 1)
            rules[symbol.strip()] = replacement.strip()
    return rules
