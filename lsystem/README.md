# Paket L-Sistem

Modul za prepisovanje nizov, ki implementira različne modele rasti iz "The Algorithmic Beauty of Plants" (ABOP).

## Moduli

### `engine.py` - Osnovni L-Sistem

Temeljni modul za prepisovanje nizov za kontekstno neodvisne L-sisteme.

```python
from lsystem.engine import LSystemEngine

engine = LSystemEngine(
    axiom="F",
    rules={"F": "F[+F]F[-F]F"},
    angle=25.7
)

result = engine.generate(iterations=4)
print(result)  # Razširjen L-sistem niz
```

**Funkcionalnosti:**
- Preprosto prepisovanje nizov na osnovi pravil
- Podpora za deterministična in stohastična pravila
- Nastavljivo število iteracij

### `parametric.py` - Parametrični L-Sistem

Napreden mehanizem s podporo za parametrična pravila s pogoji in matematičnimi izrazi.

```python
from lsystem.parametric import ParametricLSystem

lsystem = ParametricLSystem(
    axiom="A(1,10)",
    productions=[
        "A(l,w) : l > 0.5 -> !(w)F(l)[&(45)B(l*0.7,w*0.707)]A(l*0.9,w*0.707)",
        "A(l,w) : l <= 0.5 -> !(w)F(l)L",
        "B(l,w) -> !(w)F(l)[-(45)$C(l*0.8,w*0.707)][+(45)$C(l*0.8,w*0.707)]",
    ],
    constants={"r1": 0.9, "r2": 0.7}
)

result = lsystem.generate(iterations=7)
```

**Sintaksa Produkcijskih Pravil:**
```
predhodnik : pogoj -> naslednik

Primeri:
A(l,w) : l > 0.1 -> F(l)A(l*0.9,w*0.707)   # Pogojno
A(l,w) -> F(l)[+B(l*0.8,w*0.7)][-B]        # Nepogojno
B < A > C -> F                              # Kontekstno občutljivo
```

**Podprti Operatorji:**
- Aritmetični: `+`, `-`, `*`, `/`, `**` (potenca)
- Primerjalni: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Funkcije: `sin`, `cos`, `tan`, `sqrt`, `abs`, `min`, `max`
- Konstante: `pi`, `e` in uporabniško definirane

### `timed.py` - Časovni L-Sistem

Model zvezne rasti, kjer segmenti rastejo skozi čas namesto da se pojavijo takoj.

```python
from lsystem.timed import TimedLSystem

timed = TimedLSystem(
    axiom="A(1,10)",
    productions=[...],
    growth_rate=0.1
)

# Pridobi stanje ob določenem času
state = timed.get_state(time=5.0)
```

### `presets.py` - Definicije Prednastavitev

Vsebuje konfiguracij prednastavitev organiziranih po kategorijah:

```python
from lsystem.presets import PRESETS, PRESETS_3D, PARAMETRIC_PRESETS

# 2D prednastavitve
plant = PRESETS["abop_1_24f"]

# 3D prednastavitve
bush = PRESETS_3D["abop_1_25"]

# Parametrične prednastavitve
tree = PARAMETRIC_PRESETS["honda_symmetric_3"]
```

**Struktura Prednastavitve:**
```python
{
    "axiom": "A(1,10)",           # Začetni niz
    "rules": {...},               # Za osnovne prednastavitve
    "productions": [...],         # Za parametrične prednastavitve
    "angle": 22.5,                # Privzeti kot vejanja
    "iterations": 7,              # Privzeto število iteracij
    "is_3d": True,                # 3D način upodabljanja
    "render_polygons": True,      # Omogoči upodabljanje listov
    "growth_mode": "sigmoid",     # Stil animacije
    "tropism_strength": 0.0,      # Učinek gravitacije
    "tropism_direction": [0,-1,0], # Vektor gravitacije
    "description": "..."          # Berljiv opis
}
```

## Matematično Ozadje

### Leonardovo Pravilo (Širina Vej)
Širina vej sledi da Vincijevemu opažanju, da je skupna presečna površina ohranjena:
```
w_starsevska² = w_otrok1² + w_otrok2²
```
Implementirano kot: `w_otrok = w_starsevska * 0.707` (pribl. 1/√2)

### Hondini Parametri Dreves
Bazirano na Hondinih (1971) matematičnih modelih dreves:
- `r1`: Razmerje krčenja za nadaljevanje debla
- `r2`: Razmerje krčenja za stranske veje
- `a1`: Kot vejanja za glavno os
- `a2`: Kot vejanja za stranske veje

## Struktura Direktorija

```
lsystem/
├── __init__.py
├── engine.py       # Osnovni L-sistem
├── parametric.py   # Parametrični L-sistem
├── timed.py        # Časovno osnovana rast
├── presets.py      # Vse definicije prednastavitev
└── surfaces/       # Definicije Bézierjevih površin
```
