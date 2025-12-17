# L-System Plant Growth Animation Generator

Generate beautiful animated GIFs of L-system plant growth using POV-Ray for high-quality rendering.

![Example Fern Growth](https://upload.wikimedia.org/wikipedia/commons/4/4b/Fractal_Farn.gif)

## Features

- **Classic L-system presets**: Fern, tree, bush, seaweed, and more
- **Custom L-systems**: Define your own axiom and production rules
- **Smooth growth animation**: Plants appear to grow organically from seed to full form
- **High-quality rendering**: POV-Ray produces beautiful anti-aliased output
- **Depth-based coloring**: Trunk to tip color gradients for visual depth

## Requirements

- **Python 3.8+** (no external packages needed)
- **POV-Ray 3.7+** for rendering
- **ImageMagick** for GIF assembly (optional but recommended)

### Installing Dependencies

**Linux (Ubuntu/Debian):**
```bash
sudo apt install povray imagemagick
```

**macOS:**
```bash
brew install povray imagemagick
```

**Windows:**
- POV-Ray: Download from http://www.povray.org/download/
- ImageMagick: Download from https://imagemagick.org/script/download.php

## Quick Start

```bash
# Generate a fractal fern
python main.py --preset fern --output fern_growth.gif

# Generate a binary tree
python main.py --preset tree --output tree_growth.gif

# Generate a bush
python main.py --preset bush --output bush_growth.gif

# Generate seaweed
python main.py --preset seaweed --output seaweed_growth.gif
```

## Usage

### Using Presets

```bash
python main.py --preset <preset_name> [options]
```

Available presets:
- `fern` - Fractal fern (Barnsley-like)
- `tree` - Simple binary tree
- `bush` - Dense bush structure  
- `seaweed` - Swaying seaweed pattern
- `tree2` - Alternate tree structure
- `weed` - Simple weed/grass

### Custom L-Systems

```bash
python main.py --axiom "F" --rules "F:F[-F][+F]" --angle 25 --iterations 5 --output custom.gif
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--preset`, `-p` | | Use a predefined plant |
| `--axiom`, `-a` | | Starting string |
| `--rules`, `-r` | | Production rules as "A:replacement,B:replacement" |
| `--angle`, `-d` | 25 | Turning angle in degrees |
| `--iterations`, `-i` | 5 | Number of L-system iterations |
| `--frames`, `-f` | 100 | Total animation frames |
| `--fps` | 15 | Frames per second for GIF |
| `--width`, `-W` | 800 | Image width in pixels |
| `--height`, `-H` | 600 | Image height in pixels |
| `--output`, `-o` | plant_growth.gif | Output filename |
| `--workers`, `-w` | 4 | Parallel render workers |
| `--keep-frames` | | Keep intermediate PNG frames |
| `--skip-render` | | Generate .pov files only |
| `--skip-gif` | | Render frames, skip GIF |
| `--verbose`, `-v` | | Verbose output |

## L-System Symbol Reference

| Symbol | Action |
|--------|--------|
| `F` | Move forward and draw |
| `f` | Move forward without drawing |
| `+` | Turn left by angle |
| `-` | Turn right by angle |
| `[` | Push state (branch start) |
| `]` | Pop state (branch end) |
| `X`, `Y`, `A`, `B` | Placeholders for rule expansion |

## Examples

### High-Resolution Fern
```bash
python main.py --preset fern --width 1920 --height 1080 --frames 150 --output fern_hd.gif
```

### Detailed Bush with More Iterations
```bash
python main.py --preset bush --iterations 5 --frames 200 --output detailed_bush.gif
```

### Custom Fractal Plant
```bash
python main.py \
    --axiom "X" \
    --rules "X:F[+X][-X]FX,F:FF" \
    --angle 30 \
    --iterations 5 \
    --output custom_plant.gif
```

## Project Structure

```
lsystem_plant/
├── main.py                 # CLI entry point
├── lsystem/
│   ├── __init__.py
│   ├── engine.py          # L-System processor with memoization
│   └── presets.py         # Plant preset definitions
├── turtle/
│   ├── __init__.py
│   └── interpreter.py     # Turtle graphics interpreter
├── povray/
│   ├── __init__.py
│   ├── generator.py       # POV-Ray scene generator
│   └── renderer.py        # Batch renderer
├── animation/
│   ├── __init__.py
│   └── controller.py      # Smooth animation controller
└── output/                # Generated files
    ├── pov/               # .pov scene files
    └── frames/            # Rendered PNG frames
```

## How It Works

1. **L-System Generation**: Expands the axiom using production rules for N iterations
2. **Turtle Interpretation**: Converts the L-system string to 2D line segments
3. **Animation Planning**: Calculates visibility for each segment across frames using ease-out-cubic interpolation
4. **POV-Ray Scene Generation**: Creates .pov files with partially-drawn geometry
5. **Rendering**: POV-Ray renders each frame to PNG with anti-aliasing
6. **GIF Assembly**: ImageMagick combines frames into an animated GIF

## Tips

- **Start with fewer iterations** (2-3) during experimentation
- **More frames = smoother animation** but longer render time
- **Increase workers** (`-w`) on multi-core systems for faster rendering
- **Use `--skip-gif`** to just get PNG frames if you prefer video output
- **Color depth** is automatic based on bracket nesting depth

## Creating Video Instead of GIF

If you prefer video output, render frames and use FFmpeg:

```bash
# Generate frames only
python main.py --preset fern --skip-gif

# Create MP4 with FFmpeg
ffmpeg -framerate 15 -i output/frames/frame_%05d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

## License

MIT License - feel free to use and modify!
