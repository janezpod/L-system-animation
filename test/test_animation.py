"""Test the animation controller."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from animation.controller import AnimationController, ease_out_cubic

print("=" * 50)
print("Animation Controller Test")
print("=" * 50)

# Test easing function
print("\n1. Ease-out-cubic function")
print("-" * 40)
print("This makes growth feel natural (fast start, slow finish)\n")

print("  Input → Output")
for t in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
    print(f"  {t:.2f}  →  {ease_out_cubic(t):.3f}")


# Test visibility calculation
print("\n\n2. Segment visibility over time")
print("-" * 40)

controller = AnimationController(
    total_frames=60,
    growth_frames=8
)

num_segments = 100  # Imagine a plant with 100 segments

print(f"Total frames: {controller.total_frames}")
print(f"Growth frames per segment: {controller.growth_frames}")
print(f"Total segments: {num_segments}\n")

print("Frame | Visible | Avg Visibility | Progress")
print("-" * 50)

for frame in [0, 10, 20, 30, 40, 50, 59]:
    visibilities = [
        controller.calculate_visibility(i, frame, num_segments)
        for i in range(num_segments)
    ]
    visible = sum(1 for v in visibilities if v > 0)
    avg = sum(visibilities) / num_segments
    progress = visible / num_segments * 100
    
    print(f"{frame:5d} | {visible:7d} | {avg:14.2f} | {progress:6.1f}%")


# Show individual segment timing
print("\n\n3. When do specific segments start growing?")
print("-" * 40)

for seg_index in [0, 25, 50, 75, 99]:
    # Find first frame where visibility > 0
    for frame in range(controller.total_frames):
        vis = controller.calculate_visibility(seg_index, frame, num_segments)
        if vis > 0:
            print(f"Segment {seg_index:3d}: starts at frame {frame}")
            break
