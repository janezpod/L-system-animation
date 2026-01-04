# Paket Turtle Grafika

Interpretira nize L-sistemov z uporabo turtle grafike za generiranje geometrijskih struktur v 2D in 3D.

## Moduli

### `interpreter.py` - 2D Turtle Interpreter

Pretvarja nize L-sistemov v 2D segmente črt z uporabo klasične turtle grafike.

```python
from turtle.interpreter import TurtleInterpreter

interpreter = TurtleInterpreter(
    angle=25.7,
    step_size=10.0,
    initial_width=3.0
)

result = interpreter.interpret("F[+F]F[-F]F")

for segment in result.segments:
    print(f"Črta od ({segment.x1}, {segment.y1}) do ({segment.x2}, {segment.y2})")
```

**Izhodna Struktura:**
```python
@dataclass
class Segment:
    x1, y1: float        # Začetna točka
    x2, y2: float        # Končna točka
    depth: int           # Globina rekurzije
    width: float         # Širina črte
    index: int           # Vrstni red nastanka (za animacijo)
    color_index: int     # Indeks barvne palete
```

### `interpreter3d.py` - 3D Turtle Interpreter

Polna 3D turtle grafika z uporabo HLU (Heading-Left-Up) orientacijskih vektorjev iz ABOP.

```python
from turtle.interpreter3d import TurtleInterpreter3D

interpreter = TurtleInterpreter3D(
    angle=22.5,
    step_size=1.0,
    initial_width=10.0
)

result = interpreter.interpret(
    lsystem_string="!(10)F(1)[&(45)F(0.7)]F(0.5)",
    tropism_vector=[0, -1, 0],
    tropism_strength=0.2
)

print(f"Generirano {len(result.segments)} segmentov")
print(f"Generirano {len(result.polygons)} poligonov")
```

**3D Struktura Segmenta:**
```python
@dataclass
class Segment3D:
    x1, y1, z1: float    # Začetna točka
    x2, y2, z2: float    # Končna točka
    depth: int           # Globina rekurzije
    width: float         # Polmer valja
    index: int           # Vrstni red
    heading: Tuple       # Vektor smeri
    color_index: int     # Indeks barvne palete
```

**3D Struktura Poligona (za liste/cvetne liste):**
```python
@dataclass
class Polygon3D:
    vertices: List[Tuple[float, float, float]]
    depth: int
    color_index: int
    index: int           # Vrstni red
    normal: Tuple        # Normala površine (izračunana)
```

### `tropism.py` - Učinki Tropizma

Simulira gravitotropizem (odziv na gravitacijo) in fototropizem (odziv na svetlobo).

```python
from turtle.tropism import apply_tropism

# Upogni vektor smeri proti/stran od smeri tropizma
new_heading = apply_tropism(
    heading=[0, 1, 0],       # Trenutna smer
    tropism_vector=[0, -1, 0], # Gravitacija (navzdol)
    strength=0.3             # Intenzivnost učinka
)
```

**Algoritem (iz ABOP):**
```
H' = normalize(H + e * (T - (T·H)H))

Kjer:
- H = trenutni vektor smeri
- T = smer tropizma (normalizirana)
- e = jakost tropizma (tipično 0.0 do 0.5)
```

## Referenca Simbolov

### Ukazi Premikanja

| Simbol | 2D | 3D | Opis |
|--------|:--:|:--:|------|
| `F` | Da | Da | Premik naprej, riši črto |
| `F(x)` | Da | Da | Premik naprej za x enot |
| `f` | Da | Da | Premik naprej, brez črte |
| `f(x)` | Da | Da | Premik naprej za x enot, brez črte |
| `G` | Da | Da | Alias za `f` |

### Ukazi Rotacije

| Simbol | 2D | 3D | Opis |
|--------|:--:|:--:|------|
| `+` | Da | Da | Obrat levo (zasuk) |
| `+(x)` | Da | Da | Obrat levo za x stopinj |
| `-` | Da | Da | Obrat desno (zasuk) |
| `-(x)` | Da | Da | Obrat desno za x stopinj |
| `&` | - | Da | Nagib dol |
| `&(x)` | - | Da | Nagib dol za x stopinj |
| `^` | - | Da | Nagib gor |
| `^(x)` | - | Da | Nagib gor za x stopinj |
| `\` | - | Da | Zvitek levo |
| `\(x)` | - | Da | Zvitek levo za x stopinj |
| `/` | - | Da | Zvitek desno |
| `/(x)` | - | Da | Zvitek desno za x stopinj |
| `|` | Da | Da | Obrat (180°) |

### Ukazi Sklada

| Simbol | Opis |
|--------|------|
| `[` | Shrani trenutno stanje na sklad |
| `]` | Povrni stanje s sklada |

### Širina in Stil

| Simbol | Opis |
|--------|------|
| `!` | Zmanjšaj širino s faktorjem razpada |
| `!(x)` | Nastavi širino na x |
| `'` | Povečaj indeks barve |

### Način Poligonov (Listi/Cvetni listi)

| Simbol | Opis |
|--------|------|
| `{` | Začni definicijo poligona |
| `}` | Končaj poligon, ustvari zapolnjeno obliko |
| `.` | Zabeleži trenutni položaj kot oglišče |

### Posebni Ukazi

| Simbol | 3D | Opis |
|--------|:--:|------|
| `$` | Da | Zvitek v navpično (poravnaj L z vodoravno) |
| `%` | Da | Odreži preostanek veje |

## Koordinatni Sistemi

### 2D Sistem
- **X**: Vodoravno (pozitivno = desno)
- **Y**: Navpično (pozitivno = gor)
- **Začetna smer**: Gor (0, 1)
- **Začetni položaj**: Izhodišče (0, 0)

### 3D Sistem (ABOP Konvencija)
- **X**: Vodoravno (pozitivno = desno)
- **Y**: Navpično (pozitivno = gor)  
- **Z**: Globina (pozitivno = proti opazovalcu)
- **Začetna smer (H)**: Gor (0, 1, 0)
- **Začetna leva (L)**: Levo (-1, 0, 0)
- **Začetna gor (U)**: Naprej (0, 0, 1)

## Primeri Poligonov

### Šesterokotni List (ABOP stil)
```
{-f+f+f-|-f+f+f}
```
Ustvari 6-stranski poligon primeren za liste.

### Diamantni List
```
{-f+f-|-f+f}
```
Ustvari 4-stransko diamantno obliko.

### Z Barvo
```
''''''''^^{-f(0.02)+f(0.02)-|-f(0.02)+f(0.02)}
```
- 8 apostrofov (`'`) = barvni indeks 8 (temno zelena)
- `^^` = nagib gor proti svetlobi
- `f(0.02)` = majhni koraki za drobne liste

## Struktura Direktorija

```
turtle/
├── __init__.py
├── interpreter.py     # 2D turtle interpreter
├── interpreter3d.py   # 3D turtle s HLU vektorji
└── tropism.py         # Odziv na gravitacijo/svetlobo
```
