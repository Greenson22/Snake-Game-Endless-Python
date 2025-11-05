import pygame
import random
import math  # Diperlukan untuk trigonometri (sudut)
from . import config

# --- BARU: Definisikan radius panah ---
ARROW_RADIUS = 50  # Jarak panah dari ular (dalam pixel)

class Food:
    def __init__(self):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.FOOD_COLOR
        self.arrow_color = config.WHITE  # Warna untuk panah
        self.x = 0
        self.y = 0
        self.spawn() # Langsung spawn saat dibuat

    def spawn(self):
        """Memindahkan makanan ke posisi acak di dalam dunia."""
        self.x = round(random.randrange(0, config.WORLD_WIDTH - self.block_size) / self.block_size) * self.block_size
        self.y = round(random.randrange(0, config.WORLD_HEIGHT - self.block_size) / self.block_size) * self.block_size

    def get_pos(self):
        """Mendapatkan posisi makanan (koordinat dunia)."""
        return (self.x, self.y)

    # --- FUNGSI DRAW DIMODIFIKASI ---
    def draw(self, surface, camera, snake_head_x, snake_head_y):
        """
        Menggambar makanan jika di layar, atau panah indikator jika di luar layar.
        """
        cam_x, cam_y = camera.get_offset()
        screen_width = camera.screen_width
        screen_height = camera.screen_height

        # Hitung posisi makanan relatif di layar
        food_screen_x = self.x - cam_x
        food_screen_y = self.y - cam_y

        # Cek apakah makanan ada di dalam layar
        is_on_screen = (0 < food_screen_x < screen_width) and (0 < food_screen_y < screen_height)

        if is_on_screen:
            # Jika di layar, gambar makanan seperti biasa
            pygame.draw.rect(surface, self.color, [food_screen_x, food_screen_y, self.block_size, self.block_size])
        
        else:
            # --- Jika di luar layar, gambar panah indikator ---
            
            # 1. Hitung sudut dari ular (pemain) ke makanan (koordinat dunia)
            delta_x = self.x - snake_head_x
            delta_y = self.y - snake_head_y
            angle_rad = math.atan2(-delta_y, delta_x) # -delta_y karena Y pygame terbalik
            
            # 2. Hitung posisi ular DI LAYAR (sebagai titik asal panah)
            #    Ini diperlukan karena kamera 'smooth' dan ular tidak selalu di tengah
            snake_screen_x = snake_head_x - cam_x
            snake_screen_y = snake_head_y - cam_y
            
            # 3. Tentukan posisi jangkar panah (titik pusat panah)
            #    Ini adalah titik di lingkaran (radius 50px) di sekitar ular, berdasarkan sudut
            arrow_anchor_x = snake_screen_x + math.cos(angle_rad) * ARROW_RADIUS
            arrow_anchor_y = snake_screen_y - math.sin(angle_rad) * ARROW_RADIUS # -sin karena Y pygame terbalik

            # 4. Buat titik-titik segitiga (panah) di sekitar titik (0,0)
            arrow_size = 10
            points = [
                (arrow_size, 0),             # Ujung panah
                (-arrow_size, -arrow_size // 2), # Belakang kiri
                (-arrow_size, arrow_size // 2)   # Belakang kanan
            ]

            # 5. Putar (rotasi) dan geser (translasi) titik-titik panah
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            
            rotated_points = []
            for x, y in points:
                # Rumus rotasi 2D standar
                x_rot = x * cos_a - y * sin_a
                y_rot = x * sin_a + y * cos_a # y_rot positif berarti 'ke atas'
                
                # Geser (translasi) ke posisi jangkar panah
                # DAN balik sumbu Y untuk y_rot (karena +y_rot adalah 'atas' di math)
                final_x = x_rot + arrow_anchor_x
                final_y = -y_rot + arrow_anchor_y 
                
                rotated_points.append((final_x, final_y))

            # 6. Gambar panah (sebagai poligon)
            pygame.draw.polygon(surface, self.arrow_color, rotated_points)