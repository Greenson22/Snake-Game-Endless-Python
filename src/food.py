import pygame
import random
import math  # <-- BARU: Diperlukan untuk trigonometri (sudut)
from . import config

class Food:
    def __init__(self):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.FOOD_COLOR
        self.arrow_color = config.WHITE  # <-- BARU: Warna untuk panah
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

    # --- FUNGSI DRAW DIMODIFIKASI TOTAL ---
    def draw(self, surface, camera, snake_head_x, snake_head_y):
        """
        Menggambar makanan jika di layar, atau panah indikator jika di luar layar.
        """
        cam_x, cam_y = camera.get_offset()
        screen_width = camera.screen_width
        screen_height = camera.screen_height

        # Hitung posisi makanan relatif di layar
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y

        # Cek apakah makanan ada di dalam layar
        is_on_screen = (0 < screen_x < screen_width) and (0 < screen_y < screen_height)

        if is_on_screen:
            # Jika di layar, gambar makanan seperti biasa
            pygame.draw.rect(surface, self.color, [screen_x, screen_y, self.block_size, self.block_size])
        
        else:
            # --- Jika di luar layar, gambar panah indikator ---
            
            # 1. Hitung sudut dari ular (pemain) ke makanan
            # Kita gunakan koordinat dunia
            delta_x = self.x - snake_head_x
            delta_y = self.y - snake_head_y
            
            # math.atan2(y, x). Kita balik 'y' (-delta_y) karena sumbu Y pygame terbalik
            angle_rad = math.atan2(-delta_y, delta_x)
            
            # 2. Tentukan posisi panah di tepi layar
            # Kita "jepit" posisi makanan di layar, dengan sedikit margin
            margin = 30
            clamped_x = max(margin, min(screen_x + cam_x, screen_width - margin))
            clamped_y = max(margin, min(screen_y + cam_y, screen_height - margin))
            
            # Koreksi: Jika makanan ada di atas/bawah, jepit X ke tengah. Jika di kiri/kanan, jepit Y ke tengah.
            # Logika penjepitan yang lebih baik menggunakan sudut:
            center_x, center_y = screen_width / 2, screen_height / 2
            
            # Hitung titik potong di tepi layar dari pusat
            # Ini sedikit rumit, mari kita sederhanakan:
            # Jepit saja posisi layar relatifnya
            clamped_x = max(margin, min(screen_x, screen_width - margin))
            clamped_y = max(margin, min(screen_y, screen_height - margin))
            
            # 3. Buat titik-titik segitiga (panah)
            arrow_size = 10
            points = [
                (arrow_size, 0),             # Ujung panah
                (-arrow_size, -arrow_size // 2), # Belakang kiri
                (-arrow_size, arrow_size // 2)   # Belakang kanan
            ]

            # 4. Putar (rotasi) titik-titik panah sesuai sudut
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            
            rotated_points = []
            for x, y in points:
                # Rumus rotasi 2D
                x_rot = x * cos_a - y * sin_a
                y_rot = x * sin_a + y * cos_a
                
                # Geser (translasi) titik ke posisi tepi layar
                final_x = x_rot + clamped_x
                final_y = y_rot + clamped_y
                rotated_points.append((final_x, final_y))

            # 5. Gambar panah (sebagai poligon)
            pygame.draw.polygon(surface, self.arrow_color, rotated_points)