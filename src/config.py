import pygame
import random 

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
TEMP_SCALE = 0.01
MOISTURE_SCALE = 0.012
TEMP_BASE = random.randint(1001, 2000)
MOISTURE_BASE = random.randint(2001, 3000)

# --- Pengaturan Game ---
SNAKE_SPEED = 15 # Ini sekarang menjadi "tick rate" atau FPS game
CAMERA_SMOOTHING = 1.0

# --- BARU: Pengaturan Makanan ---
MAX_FOOD_COUNT = 40 # Dinaikkan dari 30
FOOD_SCORE_BASE = 10 # Skor dasar (skor 10 = tumbuh 1 segmen)

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
ENEMY_MIN_SPAWN_DIST = 400 

# --- Pengaturan Musuh (Rusher Cepat) ---
NUM_RUSHERS = 2 
RUSHER_MIN_LENGTH = 4
RUSHER_MAX_LENGTH = 4
RUSHER_TURN_CHANCE = 0.05 

# --- Pengaturan Power-up Bom ---
BOMB_SPAWN_TIME = 15 # Detik antara spawn bom
BOMB_RADIUS_AFFECTED = 350 # Radius ledakan (pixel)
ITEM_SPAWN_RADIUS_MIN = 300
ITEM_SPAWN_RADIUS_MAX = 800

# --- Definisi Warna ---
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)

SNAKE_COLOR = (0, 200, 0) 
ENEMY_COLOR = (255, 100, 0) 
RUSHER_COLOR = (255, 0, 255) 
BOMB_COLOR = (100, 100, 100)

# --- Warna Makanan (BARU) ---
FOOD_APPLE_COLOR = (213, 50, 80) # Apel (Rumput)
FOOD_BERRY_COLOR = (100, 0, 200) # Berry (Hutan)
FOOD_CACTUS_COLOR = (255, 165, 0) # Kaktus (Gurun)
FOOD_MUSHROOM_COLOR = (150, 75, 0) # Jamur (Tanah)
FOOD_CRYSTAL_COLOR = (200, 230, 255) # Kristal (Batu)
FOOD_ICE_BERRY_COLOR = (0, 200, 255) # Berry Es (Salju)

# --- Warna Terrain ---
GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 69, 19)
SAND_COLOR = (244, 164, 96)
STONE_COLOR = (128, 128, 128)
WATER_COLOR = BLUE 
SNOW_COLOR = (240, 240, 240)
DEEP_GRASS_COLOR = (0, 100, 0) 
SCORCHED_COLOR = (80, 80, 80) 

# --- Tipe Terrain (untuk konsistensi) ---
T_STONE = "stone"
T_DIRT = "dirt"
T_GRASS = "grass"
T_SAND = "sand"
T_WATER = "water"
T_SNOW = "snow" 
T_DEEP_GRASS = "deep_grass" 
T_SCORCHED = "scorched"

# --- BARU: Aturan Spawn Makanan Bioma (dengan Probabilitas) ---
# Format: TIPE_TERRAIN: (WARNA_MAKANAN, SKOR, PROBABILITAS_SPAWN)
BIOME_FOOD_RULES = {
    # Terrain Cepat (Spawn Sangat Jarang)
    T_GRASS: (FOOD_APPLE_COLOR, 10, 0.1), # 10%
    T_DEEP_GRASS: (FOOD_BERRY_COLOR, 15, 0.15), # 15%
    T_SAND: (FOOD_CACTUS_COLOR, 20, 0.1), # 10%

    # Terrain Lambat (Spawn Sangat Sering)
    T_DIRT: (FOOD_MUSHROOM_COLOR, 10, 0.95), # 95%
    T_SCORCHED: (FOOD_MUSHROOM_COLOR, 15, 0.95), # 95%
    T_STONE: (FOOD_CRYSTAL_COLOR, 25, 1.0), # 100% (Selalu spawn)
    T_SNOW: (FOOD_ICE_BERRY_COLOR, 20, 1.0), # 100% (Selalu spawn)
    
    # Terrain Invalid
    T_WATER: None,
}

# --- Pengaturan Kecepatan Terrain ---
TERRAIN_SPEEDS = {
    T_GRASS: 1,
    T_SAND: 1,
    T_DIRT: 2,
    T_STONE: 3,
    T_WATER: 4,
    T_SNOW: 3, 
    T_DEEP_GRASS: 1, 
    T_SCORCHED: 2, 
}

# --- Pemetaan Warna Partikel Terrain ---
TERRAIN_PARTICLE_COLORS = {
    T_GRASS: GRASS_COLOR,
    T_SAND: SAND_COLOR,
    T_DIRT: DIRT_COLOR,
    T_STONE: STONE_COLOR,
    T_WATER: WATER_COLOR,
    T_SNOW: SNOW_COLOR, 
    T_DEEP_GRASS: DEEP_GRASS_COLOR, 
    T_SCORCHED: SCORCHED_COLOR, 
}

# --- Pengaturan Minimap (DINAMIS/RADAR) ---
MINIMAP_WIDTH = 150  
MINIMAP_HEIGHT = 150 
MINIMAP_X_POS = DIS_WIDTH - MINIMAP_WIDTH - 10 
MINIMAP_Y_POS = 10
MINIMAP_BORDER_WIDTH = 2

MINIMAP_VIEW_RADIUS_WORLD = 1000 
MINIMAP_RADIUS_PIXELS = MINIMAP_WIDTH // 2 
MINIMAP_TERRAIN_SAMPLES = 30 

# Warna untuk 'blip' (titik)
MINIMAP_PLAYER_COLOR = WHITE
MINIMAP_ENEMY_COLOR = ENEMY_COLOR
MINIMAP_RUSHER_COLOR = RUSHER_COLOR
MINIMAP_FOOD_COLOR = FOOD_APPLE_COLOR # Gunakan satu warna default untuk minimap
MINIMAP_BOMB_COLOR = BOMB_COLOR

# Latar belakang minimap
MINIMAP_BG_COLOR = (0, 0, 0) 
MINIMAP_BG_ALPHA = 120 

# --- Font ---
TITLE_FONT = pygame.font.SysFont("impact", 75) 
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)
STATS_FONT = pygame.font.SysFont("consolas", 20)