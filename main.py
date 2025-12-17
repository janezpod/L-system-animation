#!/usr/bin/env python3
"""
L-System Plant Growth Animation Generator

Generates animated GIFs of L-system plant growth using POV-Ray for rendering.
Supports both 2D and 3D plants with multiple growth animation styles.

Enhanced with ABOP features:
- Parametric L-systems with conditional and stochastic productions
- Sphere sweep rendering for smoother branches
- Polygon rendering for leaves and petals
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from lsystem.engine import LSystem, parse_rules
from lsystem.presets import (
    PRESETS, PRESETS_3D, get_preset, list_presets, list_presets_by_category,
    PARAMETRIC_PRESETS, get_parametric_preset, list_parametric_presets
)
from turtle.interpreter import TurtleInterpreter
from povray.generator import POVRayGenerator, ColorMode
from povray.renderer import POVRayRenderer, check_povray_available
from animation.controller import AnimationController, GrowthMode


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
    loop: int = 0,
    hold_frames: int = 15
) -> bool:
    """
    Create GIF from PNG frames using Pillow.
    
    Args:
        frame_dir: Directory containing frame_*.png files
        output_file: Output GIF filename
        fps: Frames per second
        loop: Loop count (0 = infinite)
        hold_frames: Number of times to repeat final frame
        
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
    
    frame_dir = os.path.abspath(frame_dir)
    output_file = os.path.abspath(output_file)
    frame_pattern = os.path.join(frame_dir, "frame_*.png")
    frame_files = sorted(glob.glob(frame_pattern))
    
    if not frame_files:
        print(f"No frame files found matching: {frame_pattern}")
        return False
    
    print(f"\nCreating GIF with {fps} FPS from {len(frame_files)} frames + {hold_frames} hold frames...")
    
    try:
        frames = []
        skipped = 0
        for i, f in enumerate(frame_files):
            try:
                img = Image.open(f)
                img.load()
                img = img.convert('RGBA')
                background = Image.new('RGBA', img.size, (255, 255, 255, 255))
                composite = Image.alpha_composite(background, img)
                composite = composite.convert('P', palette=Image.ADAPTIVE, colors=256)
                frames.append(composite)
            except Exception as e:
                print(f"\n  Warning: Skipping corrupted frame {os.path.basename(f)}: {e}")
                skipped += 1
                continue
            
            if (i + 1) % 10 == 0 or i == len(frame_files) - 1:
                print(f"\r  Loading frames: {i + 1}/{len(frame_files)}", end="", flush=True)
        
        print()
        
        if skipped > 0:
            print(f"  Skipped {skipped} corrupted frames")
        
        if not frames:
            print("No valid frames loaded")
            return False
        
        if len(frames) < 2:
            print("Need at least 2 frames for animation")
            return False
        
        if hold_frames > 0 and frames:
            final_frame = frames[-1]
            for _ in range(hold_frames):
                frames.append(final_frame)
        
        duration = int(1000 / fps)
        
        print(f"  Saving GIF ({len(frames)} total frames)...")
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


def parse_constants(constants_str: str) -> dict:
    """Parse constants string like 'R1:0.9,WR:0.707' into dict."""
    if not constants_str:
        return {}
    
    constants = {}
    for item in constants_str.split(','):
        if ':' in item:
            name, value = item.split(':', 1)
            try:
                constants[name.strip()] = float(value.strip())
            except ValueError:
                print(f"Warning: Invalid constant value '{item}', skipping")
    return constants


def main():
    parser = argparse.ArgumentParser(
        description="Generate animated L-system plant growth GIFs (2D and 3D)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 2D plants
  python main.py --preset fern --output fern_growth.gif
  python main.py --preset tree --growth-mode apical --show-leaves --output tree.gif
  
  # 3D plants
  python main.py --preset tree_3d_simple --3d --output tree3d.gif
  python main.py --preset spiral_plant_3d --3d --animate-camera --output spiral.gif
  
  # Parametric L-systems (ABOP-style)
  python main.py --preset growing_tree_param --parametric --output growing.gif
  python main.py --preset stochastic_bush_abop --parametric --seed 42 --output bush.gif
  python main.py --preset developmental_leaf --parametric --render-polygons --output leaf.gif
  
  # Rendering options
  python main.py --preset fern --sphere-sweep --output smooth_fern.gif
  python main.py --preset tree --sphere-sweep --render-polygons --output tree.gif
  
  # Custom L-system
  python main.py --axiom "F" --rules "F:F[-F][+F]" --angle 25 --iterations 5

Available 2D presets: """ + ", ".join(list_presets(include_3d=False)) + """

Available 3D presets: """ + ", ".join(PRESETS_3D.keys()) + """

Available parametric presets: """ + ", ".join(list_parametric_presets())
    )
    
    # === L-System parameters ===
    lsys_group = parser.add_argument_group('L-System Parameters')
    lsys_group.add_argument("--preset", "-p", 
                           help="Use a predefined plant preset")
    lsys_group.add_argument("--axiom", "-a", help="Starting string (axiom)")
    lsys_group.add_argument("--rules", "-r", 
                           help="Production rules as 'A:replacement,B:replacement'")
    lsys_group.add_argument("--angle", "-d", type=float, default=None,
                           help="Turning angle in degrees")
    lsys_group.add_argument("--iterations", "-i", type=int, default=None,
                           help="Number of L-system iterations")
    
    # === Parametric L-System parameters (NEW) ===
    param_group = parser.add_argument_group('Parametric L-System Options')
    param_group.add_argument("--parametric", action="store_true",
                            help="Use parametric L-system engine (for ABOP-style plants)")
    param_group.add_argument("--constants", type=str, default=None,
                            help="Named constants as 'R1:0.9,WR:0.707'")
    param_group.add_argument("--seed", type=int, default=None,
                            help="Random seed for stochastic productions")
    
    # === Animation parameters ===
    anim_group = parser.add_argument_group('Animation Parameters')
    anim_group.add_argument("--frames", "-f", type=int, default=100,
                           help="Total animation frames (default: 100)")
    anim_group.add_argument("--fps", type=int, default=15,
                           help="Frames per second for GIF (default: 15)")
    anim_group.add_argument("--hold-frames", type=int, default=15,
                           help="Frames to hold at end before looping (default: 15)")
    anim_group.add_argument("--growth-mode", choices=['linear', 'sigmoid', 'apical'],
                           default='sigmoid',
                           help="Growth animation style (default: sigmoid)")
    anim_group.add_argument("--padding", type=float, default=0.05,
                           help="Padding around plant as fraction (default: 0.05)")
    
    # === Visual parameters ===
    vis_group = parser.add_argument_group('Visual Parameters')
    vis_group.add_argument("--width", "-W", type=int, default=800,
                          help="Image width in pixels (default: 800)")
    vis_group.add_argument("--height", "-H", type=int, default=600,
                          help="Image height in pixels (default: 600)")
    vis_group.add_argument("--show-leaves", action="store_true",
                          help="Add leaf shapes at branch tips")
    vis_group.add_argument("--color-mode", choices=['depth', 'gradient', 'autumn', 'mono'],
                          default='depth',
                          help="Coloring style (default: depth)")
    
    # === Rendering parameters (NEW) ===
    render_group = parser.add_argument_group('Rendering Options')
    render_group.add_argument("--sphere-sweep", action="store_true",
                             help="Use sphere_sweep for smoother branches")
    render_group.add_argument("--render-polygons", action="store_true",
                             help="Render filled polygons for leaves (from { } notation)")
    
    # === Turtle parameters ===
    turtle_group = parser.add_argument_group('Turtle Parameters')
    turtle_group.add_argument("--step-size", type=float, default=10.0,
                             help="Base segment length (default: 10)")
    turtle_group.add_argument("--width-decay", type=float, default=0.7,
                             help="Width multiplier per depth (default: 0.7)")
    turtle_group.add_argument("--length-decay", type=float, default=0.9,
                             help="Length multiplier per depth (default: 0.9)")
    turtle_group.add_argument("--stochastic", type=float, default=0.0,
                             help="Random angle variation (0.1 = ±10%%, default: 0)")
    
    # === 3D parameters ===
    three_d_group = parser.add_argument_group('3D Parameters')
    three_d_group.add_argument("--3d", dest="three_d", action="store_true",
                              help="Enable 3D mode")
    three_d_group.add_argument("--camera-angle", type=float, default=30.0,
                              help="Camera orbit angle in degrees (default: 30)")
    three_d_group.add_argument("--camera-distance", type=float, default=2.0,
                              help="Camera distance multiplier (default: 2.0)")
    three_d_group.add_argument("--camera-height", type=float, default=0.5,
                              help="Camera height multiplier (default: 0.5)")
    three_d_group.add_argument("--animate-camera", action="store_true",
                              help="Rotate camera during animation")
    three_d_group.add_argument("--camera-rotation", type=float, default=360.0,
                              help="Total camera rotation over animation (default: 360)")
    three_d_group.add_argument("--roll-angle", type=float, default=None,
                              help="Roll angle for / and \\ (default: same as --angle)")
    three_d_group.add_argument("--tropism-strength", type=float, default=0.0,
                              help="Gravitropism strength 0-1 (default: 0)")
    three_d_group.add_argument("--tropism-direction", type=str, default="0,1,0",
                              help="Tropism vector X,Y,Z (default: 0,1,0)")
    
    # === Output parameters ===
    out_group = parser.add_argument_group('Output Parameters')
    out_group.add_argument("--output", "-o", default="plant_growth.gif",
                          help="Output GIF filename (default: plant_growth.gif)")
    out_group.add_argument("--output-dir", default="output",
                          help="Output directory (default: output)")
    out_group.add_argument("--workers", "-w", type=int, default=4,
                          help="Parallel render workers (default: 4)")
    out_group.add_argument("--keep-frames", action="store_true",
                          help="Keep intermediate PNG frames")
    out_group.add_argument("--skip-render", action="store_true",
                          help="Skip POV-Ray rendering (generate .pov files only)")
    out_group.add_argument("--skip-gif", action="store_true",
                          help="Skip GIF creation (render frames only)")
    out_group.add_argument("--verbose", "-v", action="store_true",
                          help="Verbose output")
    
    # === Info commands ===
    info_group = parser.add_argument_group('Information')
    info_group.add_argument("--list-presets", action="store_true",
                           help="List available presets and exit")
    info_group.add_argument("--list-categories", action="store_true",
                           help="List presets by category and exit")
    info_group.add_argument("--list-parametric", action="store_true",
                           help="List parametric presets and exit")
    
    args = parser.parse_args()
    
    # === Handle info commands ===
    if args.list_presets:
        print("Available 2D plant presets:\n")
        for name, preset in PRESETS.items():
            print(f"  {name}:")
            print(f"    Axiom: {preset['axiom']}")
            print(f"    Rules: {preset['rules']}")
            print(f"    Angle: {preset['angle']}°")
            print(f"    Iterations: {preset['iterations']}")
            if 'description' in preset:
                print(f"    Description: {preset['description']}")
            print()
        
        print("\nAvailable 3D plant presets:\n")
        for name, preset in PRESETS_3D.items():
            print(f"  {name}:")
            print(f"    Axiom: {preset['axiom']}")
            print(f"    Angle: {preset['angle']}°")
            if 'roll_angle' in preset:
                print(f"    Roll Angle: {preset['roll_angle']}°")
            if 'description' in preset:
                print(f"    Description: {preset['description']}")
            print()
        return
    
    if args.list_categories:
        categories = list_presets_by_category()
        for category, presets in categories.items():
            print(f"\n{category}:")
            for preset in presets:
                print(f"  - {preset}")
        return
    
    if args.list_parametric:
        print("Available Parametric Presets (ABOP-style):\n")
        for name in list_parametric_presets():
            preset = get_parametric_preset(name)
            print(f"  {name}:")
            print(f"    Axiom: {preset['axiom']}")
            if 'description' in preset:
                print(f"    Description: {preset['description']}")
            if 'constants' in preset:
                print(f"    Constants: {preset['constants']}")
            print()
        return
    
    # === Check POV-Ray availability ===
    if not args.skip_render:
        available, message = check_povray_available()
        if not available:
            print(f"Error: {message}")
            sys.exit(1)
        if args.verbose:
            print(message)
    
    # === Get L-system parameters ===
    is_3d = args.three_d
    is_parametric = args.parametric
    use_sphere_sweep = args.sphere_sweep
    render_polygons = args.render_polygons
    
    # Default biological parameters
    width_decay = args.width_decay
    length_decay = args.length_decay
    stochastic = args.stochastic
    constants = parse_constants(args.constants) if args.constants else {}
    
    # Variables for parametric mode
    parametric_lsystem = None
    productions_list = None
    
    if args.preset:
        # Check if it's a parametric preset
        if args.preset in PARAMETRIC_PRESETS or args.parametric:
            try:
                preset = get_parametric_preset(args.preset)
                is_parametric = True
            except KeyError:
                # Fall back to regular preset
                try:
                    preset = get_preset(args.preset, include_3d=True)
                except KeyError as e:
                    print(f"Error: {e}")
                    sys.exit(1)
        else:
            try:
                preset = get_preset(args.preset, include_3d=True)
            except KeyError as e:
                print(f"Error: {e}")
                sys.exit(1)
        
        axiom = preset['axiom']
        angle = args.angle if args.angle is not None else preset['angle']
        iterations = args.iterations if args.iterations is not None else preset['iterations']
        
        # Handle parametric preset
        if is_parametric and 'productions' in preset:
            productions_list = preset['productions']
            if 'constants' in preset:
                # Merge preset constants with CLI constants (CLI takes precedence)
                preset_constants = preset['constants'].copy()
                preset_constants.update(constants)
                constants = preset_constants
        else:
            rules = preset['rules']
        
        # Check if preset is 3D
        if preset.get('is_3d') or args.preset in PRESETS_3D:
            is_3d = True
        
        # Get optional 3D parameters from preset
        roll_angle = args.roll_angle
        if roll_angle is None and 'roll_angle' in preset:
            roll_angle = preset['roll_angle']
        
        tropism_strength = args.tropism_strength
        if 'tropism_strength' in preset and args.tropism_strength == 0:
            tropism_strength = preset['tropism_strength']
        
        # Get tropism direction from preset if specified
        tropism_direction_preset = None
        if 'tropism_direction' in preset:
            tropism_direction_preset = preset['tropism_direction']
        
        # Get biological parameters from preset
        if args.width_decay == 0.7 and 'width_decay' in preset:
            width_decay = preset['width_decay']
        
        if args.length_decay == 0.9 and 'length_decay' in preset:
            length_decay = preset['length_decay']
        
        if args.stochastic == 0 and 'stochastic' in preset:
            stochastic = preset['stochastic']
        
        print(f"Using preset: {args.preset}")
        if preset.get('description'):
            print(f"  Description: {preset['description']}")
        if is_parametric:
            print(f"  Type: Parametric L-system")
        if args.iterations is not None:
            print(f"  (overriding iterations: {iterations})")
        if args.angle is not None:
            print(f"  (overriding angle: {angle})")
        if is_3d:
            print(f"  Mode: 3D")
        if use_sphere_sweep:
            print(f"  Rendering: Sphere sweep (smooth branches)")
        if render_polygons:
            print(f"  Rendering: Polygons enabled")
        if width_decay != 0.7:
            print(f"  Width decay: {width_decay}")
        if length_decay != 0.9:
            print(f"  Length decay: {length_decay}")
        if tropism_strength > 0:
            print(f"  Tropism strength: {tropism_strength}")
        if stochastic > 0:
            print(f"  Stochastic variation: {stochastic}")
        if constants:
            print(f"  Constants: {constants}")
            
    elif args.axiom and args.rules:
        axiom = args.axiom
        rules = parse_rules(args.rules)
        angle = args.angle if args.angle is not None else 25
        iterations = args.iterations if args.iterations is not None else 5
        roll_angle = args.roll_angle
        tropism_strength = args.tropism_strength
        tropism_direction_preset = None  # No preset direction for custom
        print(f"Using custom L-system: {axiom} with rules {rules}")
        
        # Auto-detect 3D from rules
        from turtle.interpreter3d import detect_3d_rules
        if detect_3d_rules(rules):
            is_3d = True
            print("  (3D symbols detected in rules)")
    else:
        parser.error("Either --preset or both --axiom and --rules are required")
    
    # Parse tropism direction - prefer preset over CLI default
    if 'tropism_direction_preset' in dir() and tropism_direction_preset is not None:
        tropism_vector = tuple(tropism_direction_preset)
    else:
        tropism_vector = tuple(float(x) for x in args.tropism_direction.split(','))
    
    # === Setup output directories ===
    output_dir = args.output_dir
    pov_dir = os.path.join(output_dir, "pov")
    frames_dir = os.path.join(output_dir, "frames")
    
    # Clear old files
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
    
    # === Step 1: Generate L-system string ===
    print(f"\n[1/5] Generating L-system ({iterations} iterations)...")
    
    if is_parametric and productions_list is not None:
        # Use parametric L-system engine
        from lsystem.parametric import ParametricLSystem, parse_production_string, Production
        
        # Parse productions - handle both string and dict formats
        productions = []
        for prod_item in productions_list:
            if isinstance(prod_item, str):
                # Plain string format: "A(l,w) : l < 5 -> ..."
                productions.append(parse_production_string(prod_item))
            elif isinstance(prod_item, dict):
                # Dict format: {"rule": "...", "probability": 0.33}
                prod = parse_production_string(prod_item['rule'])
                if 'probability' in prod_item:
                    prod = Production(
                        predecessor=prod.predecessor,
                        formal_params=prod.formal_params,
                        condition=prod.condition,
                        successor=prod.successor,
                        probability=prod_item['probability'],
                        left_context=prod.left_context,
                        right_context=prod.right_context
                    )
                productions.append(prod)
            else:
                raise ValueError(f"Unknown production format: {type(prod_item)}")
        
        parametric_lsystem = ParametricLSystem(
            axiom=axiom,
            productions=productions,
            iterations=iterations,
            random_seed=args.seed,
            constants=constants
        )
        
        try:
            modules = parametric_lsystem.generate()
            lsystem_string = parametric_lsystem.to_string(modules)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        print(f"  Modules generated: {len(modules):,}")
        print(f"  String length: {len(lsystem_string):,} characters")
    else:
        # Use standard L-system engine
        lsystem = LSystem(axiom, rules, iterations)
        
        try:
            lsystem_string = lsystem.generate()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        print(f"  String length: {len(lsystem_string):,} characters")
    
    segment_count = lsystem_string.count('F')
    print(f"  Segment count: {segment_count:,}")
    
    # === Step 2: Interpret as turtle graphics ===
    print(f"\n[2/5] Interpreting {'3D' if is_3d else '2D'} turtle graphics...")
    
    polygons = []  # Will hold polygon data if any
    
    if is_3d:
        from turtle.interpreter3d import TurtleInterpreter3D
        interpreter = TurtleInterpreter3D(
            angle_delta=angle,
            roll_angle=roll_angle if roll_angle else angle,
            step_size=args.step_size,
            width_decay=width_decay,
            length_decay=length_decay,
            tropism_vector=tropism_vector if tropism_strength > 0 else None,
            tropism_strength=tropism_strength,
            angle_variance=stochastic,
            length_variance=stochastic * 0.5
        )
        result = interpreter.interpret(lsystem_string)
        
        # Handle new InterpretResult3D or legacy list format
        if hasattr(result, 'segments'):
            segments = result.segments
            polygons = result.polygons if hasattr(result, 'polygons') else []
        else:
            segments = result
        
        bbox = interpreter.get_bounding_box(segments)
        max_depth = interpreter.get_max_depth(segments)
        
        print(f"  Segments: {len(segments):,}")
        if polygons:
            print(f"  Polygons: {len(polygons):,}")
        print(f"  Max depth: {max_depth}")
        print(f"  3D Bounding box: "
              f"({bbox.min_x:.1f}, {bbox.min_y:.1f}, {bbox.min_z:.1f}) to "
              f"({bbox.max_x:.1f}, {bbox.max_y:.1f}, {bbox.max_z:.1f})")
    else:
        interpreter = TurtleInterpreter(
            angle_delta=angle,
            step_size=args.step_size,
            width_decay=width_decay,
            length_decay=length_decay
        )
        result = interpreter.interpret(lsystem_string)
        
        # Handle new InterpretResult or legacy list format
        if hasattr(result, 'segments'):
            segments = result.segments
            polygons = result.polygons if hasattr(result, 'polygons') else []
        else:
            segments = result
        
        bbox = interpreter.get_bounding_box(segments, polygons if polygons else None)
        max_depth = interpreter.get_max_depth(segments)
        
        print(f"  Segments: {len(segments):,}")
        if polygons:
            print(f"  Polygons: {len(polygons):,}")
        print(f"  Max depth: {max_depth}")
        print(f"  Bounding box: ({bbox.min_x:.1f}, {bbox.min_y:.1f}) to ({bbox.max_x:.1f}, {bbox.max_y:.1f})")
    
    # === Step 3: Generate animation frames ===
    print(f"\n[3/5] Generating {args.frames} animation frames...")
    
    # Setup generator
    color_mode = ColorMode(args.color_mode)
    
    if is_3d:
        from povray.generator3d import POVRayGenerator3D
        generator = POVRayGenerator3D(
            output_dir=pov_dir,
            width=args.width,
            height=args.height,
            padding_percent=args.padding,
            camera_angle=args.camera_angle,
            camera_distance=args.camera_distance,
            camera_height=args.camera_height,
            show_leaves=args.show_leaves,
            animate_camera=args.animate_camera,
            camera_rotation=args.camera_rotation
        )
    else:
        generator = POVRayGenerator(
            output_dir=pov_dir,
            width=args.width,
            height=args.height,
            padding_percent=args.padding,
            color_mode=color_mode,
            show_leaves=args.show_leaves,
            use_sphere_sweep=use_sphere_sweep,
            render_polygons=render_polygons
        )
    
    # Setup animation controller
    growth_mode = GrowthMode(args.growth_mode)
    controller = AnimationController(
        total_frames=args.frames,
        growth_mode=growth_mode
    )
    suggested_frames = controller.auto_configure(len(segments), respect_total_frames=True)
    
    if args.verbose and suggested_frames > args.frames:
        print(f"  Note: Suggested minimum frames for smooth animation: {suggested_frames}")
    
    def pov_progress(current, total):
        print_progress(current, total, "  POV-Ray scenes")
    
    # Generate frames
    if is_3d:
        # Need custom frame generation for 3D
        controller.prepare_segments(segments)
        pov_files = []
        terminal_indices = set(controller.get_terminal_segments(segments))
        
        for frame in range(args.frames):
            frame_segments = controller.get_frame_segments(segments, frame)
            frame_terminal = [seg for seg in frame_segments if seg.index in terminal_indices]
            
            pov_file = generator.generate_frame(
                frame_segments, bbox, frame, max_depth,
                terminal_segments=frame_terminal,
                total_frames=args.frames
            )
            pov_files.append(pov_file)
            pov_progress(frame + 1, args.frames)
    else:
        # Check if we should use enhanced generation with polygons
        if (use_sphere_sweep or render_polygons) and hasattr(generator, 'generate_scene_enhanced'):
            controller.prepare_segments(segments)
            pov_files = []
            terminal_indices = set(controller.get_terminal_segments(segments))
            
            # Calculate polygon visibility based on frame
            num_polygons = len(polygons) if polygons else 0
            
            for frame in range(args.frames):
                frame_segments = controller.get_frame_segments(segments, frame)
                frame_terminal = [seg for seg in frame_segments if seg.index in terminal_indices]
                
                # Animate polygons: reveal based on frame progress
                frame_polygons = None
                if render_polygons and polygons:
                    # Calculate which polygons should be visible
                    # Use same timing logic as segments
                    frame_progress = frame / (args.frames - 1) if args.frames > 1 else 1.0
                    growth_period = 0.8  # Use 80% of animation for growth
                    
                    frame_polygons = []
                    for poly in polygons:
                        # Calculate when this polygon should appear
                        poly_progress = poly.index / num_polygons if num_polygons > 0 else 0
                        start_time = poly_progress * growth_period
                        
                        # Polygon is visible if we've passed its start time
                        if frame_progress >= start_time:
                            frame_polygons.append(poly)
                
                # Use enhanced generation with polygons
                pov_file = generator.generate_frame_enhanced(
                    frame_segments, 
                    bbox, 
                    frame, 
                    max_depth,
                    frame_terminal,
                    frame_polygons
                )
                pov_files.append(pov_file)
                pov_progress(frame + 1, args.frames)
        else:
            pov_files = controller.generate_frames(
                segments, bbox, generator,
                progress_callback=pov_progress
            )
    
    # === Step 4: Render with POV-Ray ===
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
        
        errors = [(f, m) for f, s, m in results if not s]
        if errors:
            print(f"\n  Warning: {len(errors)} frames failed to render")
            if args.verbose:
                for f, m in errors[:5]:
                    print(f"    {os.path.basename(f)}: {m}")
    
    # === Step 5: Create GIF ===
    if args.skip_gif:
        print(f"\n[5/5] Skipping GIF creation")
        print(f"  Frames in: {frames_dir}")
    else:
        print(f"\n[5/5] Assembling GIF...")
        
        gif_path = args.output
        if not os.path.isabs(gif_path):
            gif_path = os.path.join(output_dir, gif_path)
        
        success = create_gif(frames_dir, gif_path, fps=args.fps, hold_frames=args.hold_frames)
    
    # === Summary ===
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
