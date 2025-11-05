# src/particle.py
import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        
        # Partikel akan bergerak acak ke arah luar
        self.vel_x = random.uniform(-1.5, 1.5)
        self.vel_y = random.uniform(-1.5, 1.5)
        
        # Kita gunakan radius sebagai "lifespan"
        # Partikel akan mulai besar lalu mengecil
        self.radius = random.randint(4, 7)

    def update(self):
        """Memperbarui posisi dan ukuran partikel."""
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Mengecilkan partikel setiap frame
        self.radius -= 0.25 
        
        # Mengembalikan True jika partikel masih "hidup"
        return self.radius > 0

    def draw(self, surface, camera_x, camera_y):
        """Menggambar partikel ke layar."""
        
        # Sesuaikan posisi dengan kamera
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Gambar sebagai lingkaran
        pygame.draw.circle(
            surface, 
            self.color, 
            (screen_x, screen_y), 
            int(self.radius)
        )