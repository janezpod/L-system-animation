# Paket Animacija

Nadzoruje časovnico animacije rasti in generiranje sličic za vizualizacije L-sistemov.

## Moduli

### `controller.py` - Nadzornik Animacije

Orkestrira animacije: generiranje L-sistema, interpretacija, upodabljanje in sestavljanje GIF-a.

```python
from animation.controller import AnimationController, GrowthMode

controller = AnimationController(
    width=800,
    height=600,
    num_frames=100,
    fps=15,
    growth_mode=GrowthMode.SIGMOID
)

# Generiraj animacijo
controller.generate_animation(
    lsystem_result=result,
    interpreter=interpreter,
    generator=generator,
    renderer=renderer,
    output_path="rast_rastline.gif"
)
```

## Načini Rasti

Nadzornik animacije podpira tri načine rasti, ki nadzorujejo kako rastlina "raste" skozi animacijo:

### `GrowthMode.LINEAR`

Preprosto linearno razkrivanje - segmenti se pojavljajo s konstantno hitrostjo.

```
Vidnost = sličica / skupno_sličic
```

**Najboljše za:**
- Fraktale (zmajeva krivulja, Hilbertova krivulja)
- Matematične vzorce
- Hitre predoglede

### `GrowthMode.SIGMOID`

S-krivulja rasti z naravnim pospeševanjem in pojemanjem.

```
Vidnost = sigmoid(sličica / skupno_sličic)

sigmoid(t) = 1 / (1 + exp(-12 * (t - 0.5)))
```

**Značilnosti:**
- Počasen začetek (kalitev semena)
- Hitra sredina (aktivna rast)
- Počasen konec (zrelost)

**Najboljše za:**
- Naravno rast rastlin
- Drevesa in grme
- Večino botaničnih prednastavitev

### `GrowthMode.APICAL_DOMINANCE`

Glavno deblo raste najprej, nato sledijo veje po vrstnem redu.

```
Vidnost veje bazirana na:
1. Globina v drevesu (deblo najprej)
2. Vrstni red nastanka (starejši segmenti najprej)
3. Razdalja od vrha
```

**Značilnosti:**
- Deblo se pojavi najprej
- Primarne veje sledijo
- Sekundarne veje nazadnje
- Listi se pojavijo na koncu

**Najboljše za:**
- Drevesa z jasno hierarhijo
- Realistične sekvence rasti
- Izobraževalne demonstracije

## Vidnost Segmentov

Vsak segment ima lastnost `visibility` (0.0 do 1.0), ki nadzoruje koliko je narisan:

```python
# Poln segment
segment.visibility = 1.0  # Nariši cel segment

# Polovičen segment  
segment.visibility = 0.5  # Nariši od začetka do sredine

# Skrit
segment.visibility = 0.0  # Ne nariši
```

### Delno Upodabljanje Segmentov

Za gladko animacijo rasti se segmenti lahko delno upodabljajo:

```python
@dataclass
class Segment:
    x1, y1: float  # Začetek (vedno viden ko visibility > 0)
    x2, y2: float  # Konec (povsem viden ko visibility = 1.0)
    
    def partial(self, visibility: float) -> 'Segment':
        """Vrni segment skrajšan na delež vidnosti."""
        return Segment(
            x1=self.x1,
            y1=self.y1,
            x2=self.x1 + (self.x2 - self.x1) * visibility,
            y2=self.y1 + (self.y2 - self.y1) * visibility,
            ...
        )
```

## Časovnica Sličic

### Zadržane Sličice

Nadzornik samodejno doda "zadržane sličice" na konec za premor na dokončani sliki:

```python
hold_frames = fps  # Zadrži 1 sekundo na koncu

# Animacija: 100 sličic rasti + 15 zadržanih = 115 skupno
```

### Vidiki Hitrosti Sličic

| FPS | Uporaba |
|-----|---------|
| 10 | Majhna velikost datoteke, trgano |
| 15 | Dobro ravnovesje (privzeto) |
| 24 | Gladko, filmsko |
| 30 | Zelo gladko, večje datoteke |

## API Referenca

### AnimationController

```python
class AnimationController:
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        num_frames: int = 100,
        fps: int = 15,
        growth_mode: GrowthMode = GrowthMode.SIGMOID,
        output_dir: str = "output"
    ):
        """
        Inicializiraj nadzornik animacije.
        
        Argumenti:
            width: Širina izhodne slike v pikslih
            height: Višina izhodne slike v pikslih
            num_frames: Število sličic animacije
            fps: Sličic na sekundo za GIF
            growth_mode: Način časovnice animacije
            output_dir: Direktorij za vmesne datoteke
        """
```

### Ključne Metode

```python
def calculate_visibility(
    self,
    segment_index: int,
    total_segments: int,
    frame: int,
    total_frames: int,
    depth: int = 0,
    max_depth: int = 1
) -> float:
    """
    Izračunaj vidnost segmenta za trenutno sličico.
    
    Vrne:
        float: Vidnost od 0.0 (skrit) do 1.0 (povsem viden)
    """

def generate_frame(
    self,
    segments: List[Segment],
    frame: int,
    total_frames: int,
    ...
) -> str:
    """
    Generiraj eno sličico animacije.
    
    Vrne:
        str: Pot do generirane PNG sličice
    """

def assemble_gif(
    self,
    frame_paths: List[str],
    output_path: str,
    fps: int = 15,
    hold_frames: int = None
) -> bool:
    """
    Sestavi PNG sličice v animiran GIF.
    
    Vrne:
        bool: True če uspešno
    """
```

## Primer Integracije

```python
from lsystem.engine import LSystemEngine
from turtle.interpreter import TurtleInterpreter
from povray.generator import POVRayGenerator
from povray.renderer import POVRayRenderer
from animation.controller import AnimationController, GrowthMode

# Nastavi komponente
engine = LSystemEngine(axiom="F", rules={"F": "FF+[+F-F-F]-[-F+F+F]"})
interpreter = TurtleInterpreter(angle=22.5)
generator = POVRayGenerator(width=800, height=600)
renderer = POVRayRenderer()

controller = AnimationController(
    width=800,
    height=600,
    num_frames=100,
    fps=15,
    growth_mode=GrowthMode.SIGMOID
)

# Generiraj L-sistem
lsystem_string = engine.generate(iterations=5)

# Interpretiraj v segmente
result = interpreter.interpret(lsystem_string)

# Animiraj
controller.generate_animation(
    segments=result.segments,
    bbox=result.bounding_box,
    generator=generator,
    renderer=renderer,
    output_path="moja_rastlina.gif"
)
```

## Struktura Direktorija

```
animation/
├── __init__.py
└── controller.py    # Orkestracija animacije in časovnica
```
