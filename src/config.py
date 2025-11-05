import pygame
import random # <-- Pastikan ini diimpor

# Inisialisasi modul font lebih awal
pygame.font.init()

# --- Ukuran Layar ---
DIS_WIDTH = 800
DIS_HEIGHT = 600

# --- BARU: Pengaturan Dunia (Chunk) ---
SNAKE_BLOCK = 20  # Ukuran 1 tile
CHUNK_SIZE = 16   # Ukuran 1 chunk (dalam tile) (16x16 tiles)

# --- PENGATURAN NOISE (Dipindahkan dari terrain.py agar terpusat) ---
ELEVATION_SCALE = 0.05 
ELEVATION_OCTAVES = 6
ELEVATION_PERSISTENCE = 0.5
ELEVATION_LACUNARITY = 2.0
ELEVATION_BASE = random.randint(0, 1000)

# --- BARU: PENGATURAN NOISE BIOMA ---
# Gunakan SCALE kecil agar bioma berukuran besar
TEMP_SCALE = 0.01
MOISTURE_SCALE = 0.012

TEMP_BASE = random.randint(1001, 2000)
MOISTURE_BASE = random.randint(2001, 3000)
# (Octave, dll bisa disamakan dengan elevation untuk simpelnya)

# --- Pengaturan Game ---
SNAKE_SPEED = 15 # Ini sekarang menjadi "tick rate" atau FPS game
CAMERA_SMOOTHING = 1.0

# --- Pengaturan Level & Waktu ---
LEVEL_UP_TIME = 20 # Waktu dalam detik untuk naik level
ENEMY_SPAWN_PER_LEVEL = 1 # Tambah 1 cacing per level
RUSHER_SPAWN_PER_LEVEL = 2 # Tambah 1 rusher setiap 2 level
ENEMY_SPEED_INCREASE = 0.8 # Faktor pengali (delay * 0.8)

# --- Pengaturan Musuh (Cacing Lambat) ---
NUM_ENEMIES = 3
ENEMY_MIN_LENGTH = 3
ENEMY_MAX_LENGTH = 7
ENEMY_MOVE_DELAY = 3 
# Jarak spawn minimum (sekarang relatif terhadap pemain)
ENEMY_MIN_SPAWN_DIST = 400 

# --- Pengaturan Musuh (Rusher Cepat) ---
NUM_RUSHERS = 2 
RUSHER_MIN_LENGTH = 4
RUSHER_MAX_LENGTH = 4
RUSHER_TURN_CHANCE = 0.05 

# --- Pengaturan Power-up Bom ---
BOMB_SPAWN_TIME = 15 # Detik antara spawn bom
BOMB_RADIUS_AFFECTED = 350 # Radius ledakan (pixel)
# Jarak spawn item (relatif terhadap pemain)
ITEM_SPAWN_RADIUS_MIN = 300
ITEM_SPAWN_RADIUS_MAX = 800

# --- Definisi Warna ---
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)

SNAKE_COLOR = (0, 200, 0) 
FOOD_COLOR = (213, 50, 80)
ENEMY_COLOR = (255, 100, 0) 
RUSHER_COLOR = (255, 0, 255) 
BOMB_COLOR = (100, 100, 100)

GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 69, 19)
SAND_COLOR = (244, 164, 96)
STONE_COLOR = (128, 128, 128)
WATER_COLOR = BLUE 

# --- BARU: Definisi Warna Bioma ---
SNOW_COLOR = (240, 240, 240)
DEEP_GRASS_COLOR = (0, 100, 0) # Hutan Hujan
SCORCHED_COLOR = (80, 80, 80) # (Tidak terpakai di logika baru, tapi bisa)

# --- Tipe Terrain (untuk konsistensi) ---
T_STONE = "stone"
T_DIRT = "dirt"
T_GRASS = "grass"
T_SAND = "sand"
T_WATER = "water"
T_SNOW = "snow" # <-- BARU
T_DEEP_GRASS = "deep_grass" # <-- BARU
T_SCORCHED = "scorched" # <-- BARU (Opsional)

# --- Pengaturan Kecepatan Terrain ---
TERRAIN_SPEEDS = {
    T_GRASS: 1,
    T_SAND: 1,
    T_DIRT: 2,
    T_STONE: 3,
    T_WATER: 4,
    T_SNOW: 3, # <-- BARU (Salju = lambat seperti batu)
    T_DEEP_GRASS: 1, # <-- BARU (Hutan hujan = cepat)
    T_SCORCHED: 2, # <-- BARU
}

# --- Pemetaan Warna Partikel Terrain ---
TERRAIN_PARTICLE_COLORS = {
    T_GRASS: GRASS_COLOR,
    T_SAND: SAND_COLOR,
    T_DIRT: DIRT_COLOR,
    T_STONE: STONE_COLOR,
    T_WATER: WATER_COLOR,
    T_SNOW: SNOW_COLOR, # <-- BARU
    T_DEEP_GRASS: DEEP_GRASS_COLOR, # <-- BARU
    T_SCORCHED: SCORCHED_COLOR, # <-- BARU
}

# --- BARU: Pengaturan Minimap (DINAMIS/RADAR) ---
MINIMAP_WIDTH = 150  # Ukuran kotak minimap (pixel)
MINIMAP_HEIGHT = 150 # Ukuran kotak minimap (pixel)
MINIMAP_X_POS = DIS_WIDTH - MINIMAP_WIDTH - 10 # Pojok kanan atas
MINIMAP_Y_POS = 10
MINIMAP_BORDER_WIDTH = 2

# Radius pandang (seberapa jauh 'pixel dunia' yang diwakili oleh radius minimap)
MINIMAP_VIEW_RADIUS_WORLD = 1000 
MINIMAP_RADIUS_PIXELS = MINIMAP_WIDTH // 2 # Radius minimap di layar

MINIMAP_TERRAIN_SAMPLES = 30 # Detail terrain di minimap (Grid 30x30)

# Warna untuk 'blip' (titik)
MINIMAP_PLAYER_COLOR = WHITE
MINIMAP_ENEMY_COLOR = ENEMY_COLOR
MINIMAP_RUSHER_COLOR = RUSHER_COLOR
MINIMAP_FOOD_COLOR = FOOD_COLOR
MINIMAP_BOMB_COLOR = BOMB_COLOR

# Latar belakang minimap
MINIMAP_BG_COLOR = (0, 0, 0) # Hitam
MINIMAP_BG_ALPHA = 120 # Semi-transparan

# --- Font ---
TITLE_FONT = pygame.font.SysFont("impact", 75) 
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)
STATS_FONT = pygame.font.SysFont("consolas", 20)