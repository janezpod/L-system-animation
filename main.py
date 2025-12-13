#!/usr/bin/env python3
"""
L-System Plant Growth Animation Generator

Generates animated GIFs of L-system plant growth using POV-Ray for rendering.
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from lsystem.engine import LSystem, parse_rules
from lsystem.presets import PRESETS, get_preset, list_presets
from turtle.interpreter import TurtleInterpreter
from povray.generator import POVRayGenerator
from povray.renderer import POVRayRenderer, check_povray_available
from animation.controller import AnimationController


def print_progress(current: int, total: int, prefix: str = "", width: int = 40):
    """Print a progress bar."""
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r{prefix} [{bar}] {current}/{total} ({percent*100:.1f}%)", end="", flush=True)
    if current >= total:
        print()


def create_gif(
    frame_dir: str,
    output_file: str,
    fps: int = 15,
    loop: int = 0
) -> bool:
    """
    Create GIF from PNG frames using Pillow.
    
    Args:
        frame_dir: Directory containing frame_*.png files
        output_file: Output GIF filename
        fps: Frames per second
        loop: Loop count (0 = infinite)
        
    Returns:
        True if successful
    """
    import glob
    
    try:
        from PIL import Image
    except ImportError:
        print("\nError: Pillow not installed.")
        print("Install it with: pip install Pillow")
        return False
    
    # Get list of frame files
    frame_dir = os.path.abspath(frame_dir)
    output_file = os.path.abspath(output_file)
    frame_pattern = os.path.join(frame_dir, "frame_*.png")
    frame_files = sorted(glob.glob(frame_pattern))
    
    if not frame_files:
        print(f"No frame files found matching: {frame_pattern}")
        return False
    
    print(f"\nCreating GIF with {fps} FPS from {len(frame_files)} frames...")
    
    try:
        # Load all frames
        frames = []
        skipped = 0
        for i, f in enumerate(frame_files):
            try:
                img = Image.open(f)
                img.load()  # Force load to catch truncated files early
                # Convert to RGBA then to palette for GIF
                img = img.convert('RGBA')
                # Create a white background
                background = Image.new('RGBA', img.size, (255, 255, 255, 255))
                # Composite the image onto white background
                composite = Image.alpha_composite(background, img)
                # Convert to palette mode
                composite = composite.convert('P', palette=Image.ADAPTIVE, colors=256)
                frames.append(composite)
            except Exception as e:
                print(f"\n  Warning: Skipping corrupted frame {os.path.basename(f)}: {e}")
                skipped += 1
                continue
            
            # Progress indicator
            if (i + 1) % 10 == 0 or i == len(frame_files) - 1:
                print(f"\r  Loading frames: {i + 1}/{len(frame_files)}", end="", flush=True)
        
        print()  # New line after progress
        
        if skipped > 0:
            print(f"  Skipped {skipped} corrupted frames")
        
        if not frames:
            print("No valid frames loaded")
            return False
        
        if len(frames) < 2:
            print("Need at least 2 frames for animation")
            return False
        
        # Calculate duration in milliseconds
        duration = int(1000 / fps)
        
        # Save as GIF
        print("  Saving GIF...")
        frames[0].save(
            output_file,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop,
            optimize=False
        )
        
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"Created: {output_file} ({size_mb:.2f} MB)")
            return True
        else:
            print("GIF creation failed - file not created")
            return False
            
    except Exception as e:
        print(f"Error creating GIF: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate animated L-system plant growth GIFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using a preset
  python main.py --preset fern --output fern_growth.gif

  # Custom L-system
  python main.py --axiom "F" --rules "F:F[-F][+F]" --angle 25 --iterations 5 --output tree.gif

  # Options
  python main.py --preset bush --frames 120 --fps 15 --width 800 --height 600 --output bush.gif

Available presets: """ + ", ".join(list_presets())
    )
    
    # L-System parameters
    parser.add_argument("--preset", "-p", choices=list_presets(),
                       help="Use a predefined plant preset")
    parser.add_argument("--axiom", "-a", help="Starting string (axiom)")
    parser.add_argument("--rules", "-r", 
                       help="Production rules as 'A:replacement,B:replacement'")
    parser.add_argument("--angle", "-d", type=float, default=None,
                       help="Turning angle in degrees (default: 25, or preset value)")
    parser.add_argument("--iterations", "-i", type=int, default=None,
                       help="Number of L-system iterations (default: 5, or preset value)")
    
    # Animation parameters
    parser.add_argument("--frames", "-f", type=int, default=100,
                       help="Total animation frames (default: 100)")
    parser.add_argument("--fps", type=int, default=15,
                       help="Frames per second for GIF (default: 15)")
    
    # Output parameters
    parser.add_argument("--width", "-W", type=int, default=800,
                       help="Image width in pixels (default: 800)")
    parser.add_argument("--height", "-H", type=int, default=600,
                       help="Image height in pixels (default: 600)")
    parser.add_argument("--output", "-o", default="plant_growth.gif",
                       help="Output GIF filename (default: plant_growth.gif)")
    
    # Turtle parameters
    parser.add_argument("--step-size", type=float, default=10.0,
                       help="Base segment length (default: 10)")
    parser.add_argument("--width-decay", type=float, default=0.7,
                       help="Width multiplier per depth (default: 0.7)")
    parser.add_argument("--length-decay", type=float, default=0.9,
                       help="Length multiplier per depth (default: 0.9)")
    
    # Other options
    parser.add_argument("--workers", "-w", type=int, default=4,
                       help="Parallel render workers (default: 4)")
    parser.add_argument("--keep-frames", action="store_true",
                       help="Keep intermediate PNG frames")
    parser.add_argument("--skip-render", action="store_true",
                       help="Skip POV-Ray rendering (generate .pov files only)")
    parser.add_argument("--skip-gif", action="store_true",
                       help="Skip GIF creation (render frames only)")
    parser.add_argument("--output-dir", default="output",
                       help="Output directory (default: output)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--list-presets", action="store_true",
                       help="List available presets and exit")
    
    args = parser.parse_args()
    
    # List presets and exit
    if args.list_presets:
        print("Available plant presets:\n")
        for name, preset in PRESETS.items():
            print(f"  {name}:")
            print(f"    Axiom: {preset['axiom']}")
            print(f"    Rules: {preset['rules']}")
            print(f"    Angle: {preset['angle']}°")
            print(f"    Iterations: {preset['iterations']}")
            if 'description' in preset:
                print(f"    Description: {preset['description']}")
            print()
        return
    
    # Check POV-Ray availability
    if not args.skip_render:
        available, message = check_povray_available()
        if not available:
            print(f"Error: {message}")
            sys.exit(1)
        if args.verbose:
            print(message)
    
    # Get L-system parameters
    if args.preset:
        preset = get_preset(args.preset)
        axiom = preset['axiom']
        rules = preset['rules']
        # Use CLI args if provided, otherwise use preset values
        angle = args.angle if args.angle is not None else preset['angle']
        iterations = args.iterations if args.iterations is not None else preset['iterations']
        print(f"Using preset: {args.preset}")
        if args.iterations is not None:
            print(f"  (overriding iterations: {iterations})")
        if args.angle is not None:
            print(f"  (overriding angle: {angle})")
    elif args.axiom and args.rules:
        axiom = args.axiom
        rules = parse_rules(args.rules)
        angle = args.angle if args.angle is not None else 25
        iterations = args.iterations if args.iterations is not None else 5
        print(f"Using custom L-system: {axiom} with rules {rules}")
    else:
        parser.error("Either --preset or both --axiom and --rules are required")
    
    # Setup output directories
    output_dir = args.output_dir
    pov_dir = os.path.join(output_dir, "pov")
    frames_dir = os.path.join(output_dir, "frames")
    
    # Clear old files to avoid mixing with previous runs
    if not args.skip_render:
        if os.path.exists(pov_dir):
            for f in os.listdir(pov_dir):
                if f.endswith('.pov'):
                    os.remove(os.path.join(pov_dir, f))
        if os.path.exists(frames_dir):
            for f in os.listdir(frames_dir):
                if f.endswith('.png'):
                    os.remove(os.path.join(frames_dir, f))
    
    os.makedirs(pov_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)
    
    start_time = time.time()
    
    # Step 1: Generate L-system string
    print(f"\n[1/5] Generating L-system ({iterations} iterations)...")
    lsystem = LSystem(axiom, rules, iterations)
    
    try:
        lsystem_string = lsystem.generate()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    segment_count = lsystem_string.count('F')
    print(f"  String length: {len(lsystem_string):,} characters")
    print(f"  Segment count: {segment_count:,}")
    
    # Step 2: Interpret as turtle graphics
    print(f"\n[2/5] Interpreting turtle graphics...")
    interpreter = TurtleInterpreter(
        angle_delta=angle,
        step_size=args.step_size,
        width_decay=args.width_decay,
        length_decay=args.length_decay
    )
    
    segments = interpreter.interpret(lsystem_string)
    bbox = interpreter.get_bounding_box(segments)
    max_depth = interpreter.get_max_depth(segments)
    
    print(f"  Segments: {len(segments):,}")
    print(f"  Max depth: {max_depth}")
    print(f"  Bounding box: ({bbox.min_x:.1f}, {bbox.min_y:.1f}) to ({bbox.max_x:.1f}, {bbox.max_y:.1f})")
    
    # Step 3: Generate animation frames
    print(f"\n[3/5] Generating {args.frames} animation frames...")
    
    generator = POVRayGenerator(
        output_dir=pov_dir,
        width=args.width,
        height=args.height
    )
    
    controller = AnimationController(total_frames=args.frames)
    suggested_frames = controller.auto_configure(len(segments), respect_total_frames=True)
    
    if args.verbose and suggested_frames > args.frames:
        print(f"  Note: Suggested minimum frames for smooth animation: {suggested_frames}")
    
    def pov_progress(current, total):
        print_progress(current, total, "  POV-Ray scenes")
    
    pov_files = controller.generate_frames(
        segments, bbox, generator,
        progress_callback=pov_progress
    )
    
    # Step 4: Render with POV-Ray
    if args.skip_render:
        print(f"\n[4/5] Skipping POV-Ray render (--skip-render)")
        print(f"  POV files in: {pov_dir}")
    else:
        print(f"\n[4/5] Rendering {len(pov_files)} frames with POV-Ray...")
        
        renderer = POVRayRenderer(
            output_dir=frames_dir,
            width=args.width,
            height=args.height,
            max_workers=args.workers
        )
        
        def render_progress(completed, total, filename):
            print_progress(completed, total, "  Rendering")
        
        results = renderer.render_batch(pov_files, progress_callback=render_progress)
        
        # Check for errors
        errors = [(f, m) for f, s, m in results if not s]
        if errors:
            print(f"\n  Warning: {len(errors)} frames failed to render")
            if args.verbose:
                for f, m in errors[:5]:
                    print(f"    {os.path.basename(f)}: {m}")
    
    # Step 5: Create GIF
    if args.skip_gif:
        print(f"\n[5/5] Skipping GIF creation")
        print(f"  Frames in: {frames_dir}")
    else:
        print(f"\n[5/5] Assembling GIF...")
        
        gif_path = args.output
        if not os.path.isabs(gif_path):
            gif_path = os.path.join(output_dir, gif_path)
        
        success = create_gif(frames_dir, gif_path, fps=args.fps)
        
        if success and not args.keep_frames:
            # Clean up intermediate files
            if args.verbose:
                print("  Cleaning up intermediate files...")
            # Keep the GIF, but we could optionally clean frames
    
    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"Complete! Total time: {elapsed:.1f} seconds")
    
    if not args.skip_gif:
        gif_path = args.output if os.path.isabs(args.output) else os.path.join(output_dir, args.output)
        if os.path.exists(gif_path):
            print(f"Output: {gif_path}")
    
    print(f"\nFiles:")
    print(f"  POV scenes: {pov_dir}")
    if not args.skip_render:
        print(f"  PNG frames: {frames_dir}")


if __name__ == "__main__":
    main()