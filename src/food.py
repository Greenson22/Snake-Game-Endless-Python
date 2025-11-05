import pygame
from . import config

class Food:
    def __init__(self, x, y, color, score):
        """
        Mewakili SATU item makanan di dunia.
        Logika spawn dipindahkan ke main.py
        """
        self.block_size = config.SNAKE_BLOCK
        self.x = x
        self.y = y
        self.color = color
        self.score = score

    def get_pos(self):
        """Mendapatkan posisi makanan (koordinat dunia)."""
        return (self.x, self.y)

    def draw(self, surface, camera):
        """
        Menggambar makanan HANYA jika terlihat di layar.
        """
        cam_x, cam_y = camera.get_offset()
        screen_width = camera.screen_width
        screen_height = camera.screen_height
        food_screen_x = self.x - cam_x
        food_screen_y = self.y - cam_y
        
        # Hitung apakah makanan ada di dalam layar
        is_on_screen = (0 < food_screen_x < screen_width) and (0 < food_screen_y < screen_height)

        if is_on_screen:
            # Jika di layar, gambar makanan
            pygame.draw.rect(surface, self.color, [food_screen_x, food_screen_y, self.block_size, self.block_size])