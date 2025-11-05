import pygame

# Inisialisasi modul font lebih awal
pygame.font.init()

# --- Ukuran Layar ---
DIS_WIDTH = 800
DIS_HEIGHT = 600

# --- BARU: Pengaturan Dunia (Chunk) ---
SNAKE_BLOCK = 20  # Ukuran 1 tile
CHUNK_SIZE = 16   # Ukuran 1 chunk (dalam tile) (16x16 tiles)
# (WORLD_WIDTH dan WORLD_HEIGHT dihapus karena dunia tak terbatas)

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

# --- Tipe Terrain (untuk konsistensi) ---
T_STONE = "stone"
T_DIRT = "dirt"
T_GRASS = "grass"
T_SAND = "sand"
T_WATER = "water"

# --- Pengaturan Kecepatan Terrain ---
TERRAIN_SPEEDS = {
    T_GRASS: 1,
    T_SAND: 1,
    T_DIRT: 2,
    T_STONE: 3,
    T_WATER: 4,
}

# --- Pemetaan Warna Partikel Terrain ---
TERRAIN_PARTICLE_COLORS = {
    T_GRASS: GRASS_COLOR,
    T_SAND: SAND_COLOR,
    T_DIRT: DIRT_COLOR,
    T_STONE: STONE_COLOR,
    T_WATER: WATER_COLOR
}

# --- PENGATURAN MINIMAP (DINONAKTIFKAN) ---
# Minimap statis tidak berfungsi dengan dunia tak terbatas.
# Fitur ini perlu dibangun ulang dari awal (secara dinamis).
# MINIMAP_WIDTH = DIS_WIDTH // 5 
# MINIMAP_HEIGHT = int((DIS_HEIGHT / DIS_WIDTH) * MINIMAP_WIDTH)
# MINIMAP_X_POS = DIS_WIDTH - MINIMAP_WIDTH - 10
# MINIMAP_Y_POS = 10
# MINIMAP_BORDER_WIDTH = 2
# MINIMAP_BLIP_SIZE = 3 
# MINIMAP_PLAYER_COLOR = WHITE
# MINIMAP_ENEMY_COLOR = ENEMY_COLOR
# MINIMAP_RUSHER_COLOR = RUSHER_COLOR
# MINIMAP_FOOD_COLOR = FOOD_COLOR
# MINIMAP_BOMB_COLOR = BOMB_COLOR

# --- Font ---
TITLE_FONT = pygame.font.SysFont("impact", 75) 
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)
STATS_FONT = pygame.font.SysFont("consolas", 20)