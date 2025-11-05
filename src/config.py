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

# --- BARU: Faktor smoothing kamera ---
# Mengontrol seberapa "halus" kamera mengikuti.
# Nilai lebih kecil = lebih halus/lambat (misal: 0.05)
# Nilai lebih besar = lebih kaku/cepat (misal: 0.2)
# Nilai 1.0 = instan (tidak ada smoothing)
CAMERA_SMOOTHING = 1.0

# --- Definisi Warna ---
WHITE = (255, 255, 255)
# ... (sisa file config Anda tetap sama) ...
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)

SNAKE_COLOR = (0, 200, 0) 
FOOD_COLOR = (213, 50, 80)

GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 69, 19)
SAND_COLOR = (244, 164, 96)
STONE_COLOR = (128, 128, 128)

# --- Font ---
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)