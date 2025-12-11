"""Test the L-system engine."""

# Add parent folder to path so imports work
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lsystem.engine import LSystem, parse_rules

print("=" * 50)
print("L-System Engine Test")
print("=" * 50)

# Test 1: Simple tree
print("\n1. Simple binary tree (F → F[-F][+F])")
print("-" * 40)

tree = LSystem(
    axiom="F",
    rules={"F": "F[-F][+F]"},
    iterations=3
)

for i in range(4):
    result = tree.generate(iterations=i)
    print(f"Iteration {i}: {result}")
    print(f"  Length: {len(result)}, Segments: {result.count('F')}\n")


# Test 2: Fern (more complex)
print("\n2. Fern preview (X → F+[[X]-X]-F[-FX]+X, F → FF)")
print("-" * 40)

fern = LSystem(
    axiom="X",
    rules={"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
    iterations=3
)

for i in range(4):
    result = fern.generate(iterations=i)
    print(f"Iteration {i}: length={len(result)}, segments={result.count('F')}")


# Test 3: Parse rules from string
print("\n3. Parsing rules from command-line format")
print("-" * 40)

rules_string = "F:F[-F][+F],X:FX"
parsed = parse_rules(rules_string)
print(f"Input:  '{rules_string}'")
print(f"Parsed: {parsed}")
