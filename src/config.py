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
CAMERA_SMOOTHING = 1.0

# --- MODIFIKASI: Pengaturan Musuh ---
NUM_ENEMIES = 3

# HAPUS INI:
# ENEMY_SPEED = 8 

# BARU: Panjang min/maks musuh (dalam blok)
ENEMY_MIN_LENGTH = 3
ENEMY_MAX_LENGTH = 7

# BARU: Musuh bergerak 1 blok setiap X frame.
# (Pemain bergerak 1 blok setiap 1 frame).
# Nilai lebih tinggi = musuh lebih lambat.
ENEMY_MOVE_DELAY = 3 # Musuh 3x lebih lambat dari pemain

ENEMY_MIN_SPAWN_DIST = 400 

# --- Definisi Warna ---
WHITE = (255, 255, 255)
# ... (sisa file)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)

SNAKE_COLOR = (0, 200, 0) 
FOOD_COLOR = (213, 50, 80)
ENEMY_COLOR = (255, 100, 0) # Oranye Terang

GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 69, 19)
SAND_COLOR = (244, 164, 96)
STONE_COLOR = (128, 128, 128)

# --- Font ---
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)