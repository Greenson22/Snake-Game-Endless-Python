import pygame

# Inisialisasi modul font lebih awal
pygame.font.init()

# --- Ukuran Layar dan Dunia ---
DIS_WIDTH = 800
DIS_HEIGHT = 600
WORLD_WIDTH = DIS_WIDTH * 3
WORLD_HEIGHT = DIS_HEIGHT * 3

# --- Pengaturan Game ---
SNAKE_BLOCK = 20
SNAKE_SPEED = 15 # Ini sekarang menjadi "tick rate" atau FPS game
CAMERA_SMOOTHING = 1.0

# --- BARU: Pengaturan Level & Waktu ---
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

# --- BARU: Pengaturan Power-up Bom ---
BOMB_SPAWN_TIME = 15 # Detik antara spawn bom
BOMB_RADIUS_AFFECTED = 350 # Radius ledakan (pixel)

# --- Definisi Warna ---
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)

SNAKE_COLOR = (0, 200, 0) 
FOOD_COLOR = (213, 50, 80)
ENEMY_COLOR = (255, 100, 0) 
RUSHER_COLOR = (255, 0, 255) 
BOMB_COLOR = (100, 100, 100) # BARU: Warna bom

GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 69, 19)
SAND_COLOR = (244, 164, 96)
STONE_COLOR = (128, 128, 128)

# --- BARU: Tipe Terrain (untuk konsistensi) ---
T_STONE = "stone"
T_DIRT = "dirt"
T_GRASS = "grass"
T_SAND = "sand"

# --- BARU: Pengaturan Kecepatan Terrain ---
# (Angka = jumlah frame/tick per 1 gerakan.)
# (1 = normal/cepat, 2 = 50% speed, 3 = 33% speed)
TERRAIN_SPEEDS = {
    T_GRASS: 1,  # Cepat (bergerak setiap 1 tick)
    T_SAND: 1,   # Cepat (bergerak setiap 1 tick)
    T_DIRT: 2,   # Lambat (bergerak setiap 2 tick)
    T_STONE: 3,  # Sangat lambat (bergerak setiap 3 tick)
}

# --- Font ---
TITLE_FONT = pygame.font.SysFont("impact", 75) 
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)
# BARU: Font untuk statistik (Waktu/Level)
STATS_FONT = pygame.font.SysFont("consolas", 20)