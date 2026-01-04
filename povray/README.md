# Paket POV-Ray Upodabljanje

Generira POV-Ray datoteke scen iz izhoda turtle grafike.

## Moduli

### `generator.py` - Generator 2D Scen

Pretvarja 2D segmente v POV-Ray datoteke scen z ortografsko kamero.

```python
from povray.generator import POVRayGenerator

generator = POVRayGenerator(
    output_dir="output/pov",
    width=800,
    height=600,
    padding_percent=0.1
)

# Generiraj datoteko scene
scene_path = generator.generate_scene(
    segments=result.segments,
    bbox=result.bounding_box,
    filename="frame_001.pov",
    max_depth=6
)
```

**Funkcionalnosti:**
- Ortografska kamera za 2D upodabljanje
- Samodejni izračun omejitvene škatle
- Barvanje glede na globino (rjavo deblo -> zelene konice)
- Podpora za glajenje robov

### `generator3d.py` - Generator 3D Scen

Polno generiranje 3D scen s perspektivno kamero, osvetlitvijo in podporo za poligone.

```python
from povray.generator3d import POVRayGenerator3D

generator = POVRayGenerator3D(
    output_dir="output/pov",
    width=1080,
    height=1080,
    padding_percent=0.15,
    camera_angle=30.0,
    camera_distance=2.0,
    camera_height=0.5,
    use_perspective=True,
    fov=45.0
)

# Generiraj sceno s poligoni
scene_path = generator.generate_scene(
    segments=result.segments,
    bbox=bounding_box,
    filename="frame_001.pov",
    max_depth=7,
    frame=0,
    total_frames=100,
    polygons=result.polygons
)
```

**Funkcionalnosti:**
- Perspektivna ali ortografska kamera
- Animirana rotacija kamere (360°)
- Gradient ozadja neba
- Talna ploskev z odsevom
- Profesionalna tritočkovna osvetlitev
- Upodabljanje poligonov za liste/cvetne liste
- Dvostranska osvetlitev za tanke površine

### `renderer.py` - Upravljalnik POV-Ray Procesa

Upravlja izvajanje POV-Ray podprocesa s sledenjem napredka.

```python
from povray.renderer import POVRayRenderer

renderer = POVRayRenderer(
    povray_path="povray",  # ali polna pot na Windows
    width=800,
    height=600,
    antialias=True,
    quality=9
)

# Upodobi eno sličico
success = renderer.render(
    scene_path="output/pov/frame_001.pov",
    output_path="output/frames/frame_001.png"
)

# Upodobi več sličic z napredkom
renderer.render_batch(
    scene_paths=["frame_001.pov", "frame_002.pov", ...],
    output_dir="output/frames",
    workers=4
)
```

**Nastavitve Kakovosti:**
| Nivo | Opis |
|------|------|
| 0-3 | Hiter predogled |
| 4-6 | Srednja kakovost |
| 7-8 | Visoka kakovost |
| 9 | Maksimalna kakovost (privzeto) |

## Barvna Paleta

3D generator uporablja razširjeno barvno paleto dostopno preko simbola `'`:

| Indeks | Barva | RGB | Uporaba |
|--------|-------|-----|---------|
| 0 | Glede na globino | variira | Privzeto (rjava->zelena) |
| 1 | Sončnično rumena | (1.0, 0.85, 0.1) | Sredice cvetov |
| 2 | Rjava | (0.45, 0.3, 0.15) | Semena, lubje |
| 3 | Rdeča | (0.85, 0.15, 0.15) | Cvetovi, jagode |
| 4 | Rožnata | (1.0, 0.6, 0.7) | Cvetni listi |
| 5 | Oranžna | (1.0, 0.55, 0.1) | Jesenski listi |
| 6 | Vijolična | (0.7, 0.4, 0.8) | Cvetovi |
| 7 | Bela | (0.95, 0.95, 0.95) | Sneg, cvetovi |
| 8 | Temno zelena | (0.2, 0.45, 0.15) | Listi |
| 9 | Svetlo zelena | (0.55, 0.8, 0.3) | Mladi listi |
| 10 | Zlata | (0.8, 0.75, 0.2) | Jesen |

**Uporaba v L-sistemih:**
```
'''        # 3 povečanja = rdeča (indeks 3)
''''''''   # 8 povečanj = temno zelena (indeks 8)
```

## Animacija Kamere

3D generator podpira animirano rotacijo kamere:

```python
# V generate_scene():
frame=50,        # Trenutna sličica
total_frames=100 # Skupno sličic

# Kamera kroži 360° okoli modela
# Sličica 0: pogled od spredaj
# Sličica 25: stranski pogled  
# Sličica 50: pogled od zadaj
# Sličica 75: druga stran
# Sličica 100: nazaj na spredaj
```

## Optimizacija Zmogljivosti

### Vzporedno Upodabljanje
```python
renderer.render_batch(
    scene_paths=scenes,
    output_dir="output/frames",
    workers=4  # Uporabi 4 procesorska jedra
)
```

### Kakovost vs Hitrost
```python
# Hiter predogled
renderer = POVRayRenderer(quality=3, antialias=False)

# Produkcijska kakovost  
renderer = POVRayRenderer(quality=9, antialias=True)
```

### Ločljivost
```python
# Nizka ločljivost za testiranje
generator = POVRayGenerator3D(width=480, height=480)

# Visoka ločljivost za končno verzijo
generator = POVRayGenerator3D(width=1920, height=1080)
```

## Odpravljanje Težav

### POV-Ray Ni Najden
```bash
# Windows: Zagotovite da je POV-Ray v PATH ali podajte polno pot
renderer = POVRayRenderer(povray_path="C:/Program Files/POV-Ray/bin/pvengine64.exe")

# Linux
sudo apt install povray

# macOS
brew install povray
```

### Premalo Pomnilnika
- Zmanjšajte ločljivost
- Zmanjšajte število poligonov (manj iteracij)
- Upodobite manj sličic

### Počasno Upodabljanje
- Uporabite `--workers N` za vzporedno upodabljanje
- Zmanjšajte kakovost za testiranje
- Uporabite nižjo ločljivost

## Struktura Direktorija

```
povray/
├── __init__.py
├── generator.py      # Generiranje 2D POV-Ray scen
├── generator3d.py    # Generiranje 3D POV-Ray scen
└── renderer.py       # Upravljanje POV-Ray procesa
```
