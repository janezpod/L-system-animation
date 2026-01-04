# L-Sistem Generator Animacij Rasti Rastlin

Python okvir za generiranje animiranih GIF-ov botaničnih struktur z uporabo L-sistemov in POV-Raya. Ustvarjo vizualno privlačne, botanično animacije rasti rastlin.

## Funkcionalnosti

- **2D in 3D upodabljanje** - od preprostih fraktalov do kompleksnih botaničnih struktur
- **Parametrični L-sistemi** - kontekstno občutljiva pravila z matematičnimi parametri
- **Stohastične variacije** - naključna rast za naraven videz
- **Tropizem** - simulacija gravitacije
- **Upodabljanje poligonov** - šesterokotni listi, cvetni listi in površinske zaplate
- **Animirana kamera** - 360° vrteča se perspektiva za 3D modele
- **Več načinov rasti** - linearna, sigmoidna in apikalna dominanca

## Hiter Začetek

### Predpogoji

1. **Python 3.8+** s pip
2. **POV-Ray 3.7+** - [Prenos](http://www.povray.org/download/)
   - Windows: dodajte v PATH med namestitvijo
   - Linux: `sudo apt install povray`
   - macOS: `brew install povray`

### Namestitev

```bash
# Klonirajte repozitorij
git clone https://github.com/yourusername/lsystem-animation.git
cd lsystem-animation

# Namestite Python odvisnosti
pip install Pillow numpy
```

### Generirajte Prvo Animacijo

```bash
# Preprosta 2D rastlina
python main.py --preset abop_1_24f -o moja_prva_rastlina.gif

# 3D grm z listi
python main.py --preset abop_1_25 --3d --animate-camera --render-polygons -o grm.gif

# Kreativni bonsai
python main.py --preset twisted_bonsai --3d --parametric --animate-camera --render-polygons -o bonsai.gif
```

## Uporaba

### Osnovna Struktura Ukaza

```bash
python main.py --preset <IME_PREDNASTAVITVE> [MOŽNOSTI] -o <IZHOD.gif>
```

### Osnovne Možnosti

| Možnost | Opis | Privzeto |
|---------|------|----------|
| `--preset IME` | Prednastavitev za uporabo | Obvezno |
| `-o, --output DATOTEKA` | Ime izhodne GIF datoteke | `output.gif` |
| `--3d` | Omogoči 3D način upodabljanja | Izklopljeno |
| `--parametric` | Uporabi parametrični L-sistem | Izklopljeno |
| `--iterations N` | Število iteracij L-sistema | Privzeto prednastavitve |
| `--frames N` | Število sličic animacije | 100 |
| `--fps N` | Sličic na sekundo | 15 |

### Možnosti 3D Upodabljanja

| Možnost | Opis | Privzeto |
|---------|------|----------|
| `--animate-camera` | Vrti kamero 360° okoli modela | Izklopljeno |
| `--render-polygons` | Omogoči upodabljanje listov/cvetov | Izklopljeno |
| `--camera-height F` | Množilnik višine kamere | 1.0 |
| `--camera-distance F` | Množilnik razdalje kamere | 2.0 |

### Možnosti Animacije

| Možnost | Opis | Privzeto |
|---------|------|----------|
| `--growth-mode NAČIN` | `linear`, `sigmoid` ali `apical` | `sigmoid` |
| `--width N` | Širina izhoda v pikslih | 800 |
| `--height N` | Višina izhoda v pikslih | 600 |
| `--workers N` | Vzporedni delavci za upodabljanje | 4 |

### Napredne Možnosti

| Možnost | Opis |
|---------|------|
| `--seed N` | Naključno seme za stohastične prednastavitve |
| `--angle F` | Prepiši kot vejanja |
| `--list-presets` | Prikaži vse razpoložljive prednastavitve |

## Kategorije Prednastavitev

### 2D Klasične Rastline (ABOP Slika 1.24)
```bash
abop_1_24a    # Klasični grm
abop_1_24b    # Vertikalno vejanje  
abop_1_24c    # Bilateralna simetrija
abop_1_24d    # Asimetrično drevo
abop_1_24e    # Simpodijalna rast
abop_1_24f    # Elegantna rastlina
```

### 2D Fraktali
```bash
dragon_curve        # Zmajeva krivulja
hilbert_curve       # Prostorsko polnilna krivulja
koch_snowflake      # Kochova snežinka
quadratic_snowflake # Kvadratna različica
```

### 3D ABOP Rastline
```bash
abop_1_25    # Grm s šesterokotnimi listi
abop_1_26    # Cvetoča rastlina s cvetnimi listi
```

### 3D Drevesa s Tropizmom
```bash
tree_gravity_0_none      # Brez gravitacij
tree_gravity_1_moderate  # Zmeren povešeni učinek
tree_gravity_2_strong    # Povešeni stil
```

### 3D Simpodijalna in Ternarna (ABOP Sl. 2.7, 2.8)
```bash
sympodial_2_7a/b/c/d  # Simpodijalne variacije
ternary_2_8a/b/c/d    # Vzorci ternarnega vejanja
```

### Parametrična Drevesa
```bash
monopodial_tree   # Ena glavna os (iglavci)
ternary_tree      # Trosmerno vejanje
honda_symmetric_3 # Hondin model, 3-smerna simetrija
honda_symmetric_4 # Hondin model, 4-smerna simetrija
honda_symmetric_5 # Hondin model, 5-smerna
```

### Kreativne Stilizirane Rastline
```bash
umbrella_tree      # Ploska krošnja akacije
coral_branch       # Gosta bifurkirajoča struktura
flowering_burst    # Rožnati cvetovi na konicah
twisted_bonsai     # Asimetričen, od vetra upognjen
palm_fan           # Tropski povešeni listi palme
crystal_tree       # Geometrično 6-smerno vejanje
vine_spiral        # Spiralno vzpenjajoča se trta z listi
fern_unfurl        # Razvijajoči se praprot
explosion_bush     # Dramatična radialna rast
weeping_canopy     # Gost povešeni stil vrbe
```

## Primeri Ukazov

### Hiter Test (Nizka Ločljivost)
```bash
python main.py --preset abop_1_24f --frames 60 --width 480 --height 480 -o test.gif
```

### Visokokakovosten 3D Render
```bash
python main.py --preset abop_1_25 --3d --animate-camera --render-polygons \
    --frames 120 --width 1080 --height 1080 --fps 30 -o hq_grm.gif
```

### Parametrično Drevo s Prilagojenimi Iteracijami
```bash
python main.py --preset honda_symmetric_3 --3d --parametric --iterations 8 \
    --animate-camera --render-polygons -o honda_drevo.gif
```

### Stil Žalostne Vrbe
```bash
python main.py --preset weeping_canopy --3d --parametric --iterations 12 \
    --animate-camera --render-polygons --camera-height 0.6 -o vrba.gif
```

## Arhitektura Projekta

```
lsystem-animation/
├── main.py                    # CLI vstopna točka
│
├── lsystem/                   # Jedro L-Sistema
│   ├── engine.py              # Osnovni L-sistem prepisovanje nizov
│   ├── parametric.py          # Parametrična in kontekstno občutljiva pravila
│   ├── timed.py               # Časovno osnovana zvezna rast
│   ├── presets.py             # Definicije prednastavitev
│   └── surfaces/              # Definicije Bézierjevih površin
│
├── turtle/                    # Interpretacija Turtle Grafike
│   ├── interpreter.py         # 2D turtle interpreter
│   ├── interpreter3d.py       # 3D turtle s HLU vektorji
│   └── tropism.py             # Odziv na gravitacijo/svetlobo
│
├── povray/                    # POV-Ray Upodabljanje
│   ├── generator.py           # Generiranje 2D scen
│   ├── generator3d.py         # Generiranje 3D scen
│   └── renderer.py            # Upravljanje POV-Ray procesa
│
├── animation/                 # Nadzor Animacije
│   └── controller.py          # Časovnica rasti in generiranje sličic
│
└── output/                    # Generirane datoteke
    ├── pov/                   # POV-Ray datoteke scen
    └── frames/                # Upodobljene PNG sličice
```

## Referenca Simbolov L-Sistema

### Premikanje
| Simbol | Opis |
|--------|------|
| `F` | Premik naprej, riši črto |
| `f` | Premik naprej brez risanja |
| `G` | Premik naprej brez risanja (alias) |

### Rotacija (2D in 3D)
| Simbol | Opis |
|--------|------|
| `+` | Obrat levo za kot |
| `-` | Obrat desno za kot |
| `&` | Nagib dol |
| `^` | Nagib gor |
| `\` | Zvitek levo |
| `/` | Zvitek desno |
| `|` | Obrat (180°) |

### Vejanje
| Simbol | Opis |
|--------|------|
| `[` | Shrani stanje (začni vejo) |
| `]` | Povrni stanje (končaj vejo) |

### Širina in Barva
| Simbol | Opis |
|--------|------|
| `!` | Nastavi/zmanjšaj širino črte |
| `'` | Povečaj indeks barve |

### Poligoni (Listi/Cvetni listi)
| Simbol | Opis |
|--------|------|
| `{` | Začni poligon |
| `}` | Končaj poligon |
| `.` | Zabeleži oglišče poligona |

### Posebno
| Simbol | Opis |
|--------|------|
| `$` | Zvitek v navpično (dolariziraj) |
| `%` | Odreži preostanek veje |

### Parametrična Sintaksa
```
F(dolzina)     # Naprej z določeno dolžino
!(sirina)      # Nastavi določeno širino
+(kot)         # Obrat levo za določen kot
A(l,w)         # Modul s parametri
```