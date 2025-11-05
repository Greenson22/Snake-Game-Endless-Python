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
SNAKE_SPEED = 15
# Atur ini kembali ke 1.0 jika Anda ingin kamera instan/kaku
CAMERA_SMOOTHING = 1.0

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

# --- Definisi Warna ---
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)

SNAKE_COLOR = (0, 200, 0) 
FOOD_COLOR = (213, 50, 80)
ENEMY_COLOR = (255, 100, 0) 
RUSHER_COLOR = (255, 0, 255) 

GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 69, 19)
SAND_COLOR = (244, 164, 96)
STONE_COLOR = (128, 128, 128)

# --- Font ---
# BARU: Font besar untuk judul "Game Over"
TITLE_FONT = pygame.font.SysFont("impact", 75) 
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)