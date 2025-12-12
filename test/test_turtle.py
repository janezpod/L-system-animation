"""Test the turtle graphics interpreter."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lsystem.engine import LSystem
from turtle.interpreter import TurtleInterpreter, Segment

print("=" * 50)
print("Turtle Interpreter Test")
print("=" * 50)

# Generate a simple tree
tree = LSystem(
    axiom="F",
    rules={"F": "F[-F][+F]"},
    iterations=3
)
lsystem_string = tree.generate()

print(f"\nL-system string: {lsystem_string[:50]}...")
print(f"String length: {len(lsystem_string)}")

# Interpret it
interpreter = TurtleInterpreter(
    angle_delta=25,      # Turn 25 degrees
    step_size=10,        # Each F moves 10 units
    width_decay=0.7,     # Branches get thinner
    length_decay=0.9     # Branches get shorter
)

segments = interpreter.interpret(lsystem_string)
bbox = interpreter.get_bounding_box(segments)

print(f"\n{'-' * 40}")
print(f"Generated {len(segments)} segments")
print(f"Max depth: {interpreter.get_max_depth(segments)}")
print(f"Bounding box: ({bbox.min_x:.1f}, {bbox.min_y:.1f}) to ({bbox.max_x:.1f}, {bbox.max_y:.1f})")

# Show first few segments
print(f"\nFirst 5 segments:")
for i, seg in enumerate(segments[:5]):
    print(f"  {i}: ({seg.x1:.1f}, {seg.y1:.1f}) → ({seg.x2:.1f}, {seg.y2:.1f})  depth={seg.depth}, width={seg.width:.2f}")

# Show how partial segments work (for animation)
print(f"\nPartial segment demo (for animation):")
seg = segments[0]
print(f"  Full:    ({seg.x1:.1f}, {seg.y1:.1f}) → ({seg.x2:.1f}, {seg.y2:.1f})")
for visibility in [0.25, 0.5, 0.75]:
    partial = seg.partial(visibility)
    print(f"  {int(visibility*100)}%:     ({partial.x1:.1f}, {partial.y1:.1f}) → ({partial.x2:.1f}, {partial.y2:.1f})")
