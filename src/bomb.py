# src/bomb.py
import pygame
import random
from . import config

class Bomb:
    def __init__(self):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.BOMB_COLOR
        self.x = 0
        self.y = 0
        self.spawn() # Langsung spawn saat dibuat

    def spawn(self):
        """Memindahkan bom ke posisi acak di dalam dunia."""
        self.x = round(random.randrange(0, config.WORLD_WIDTH - self.block_size) / self.block_size) * self.block_size
        self.y = round(random.randrange(0, config.WORLD_HEIGHT - self.block_size) / self.block_size) * self.block_size

    def get_pos(self):
        """Mendapatkan posisi bom (koordinat dunia)."""
        return (self.x, self.y)

    def draw(self, surface, camera):
        """
        Menggambar bom jika di layar.
        """
        cam_x, cam_y = camera.get_offset()
        screen_width = camera.screen_width
        screen_height = camera.screen_height

        # Hitung posisi bom relatif di layar
        bomb_screen_x = self.x - cam_x
        bomb_screen_y = self.y - cam_y

        # Cek apakah bom ada di dalam layar
        is_on_screen = (0 < bomb_screen_x < screen_width) and (0 < bomb_screen_y < screen_height)

        if is_on_screen:
            # Gambar bom (kotak abu-abu)
            pygame.draw.rect(surface, self.color, [bomb_screen_x, bomb_screen_y, self.block_size, self.block_size])