import pygame
import random
from . import config

class Food:
    def __init__(self):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.FOOD_COLOR
        self.x = 0
        self.y = 0
        self.spawn() # Langsung spawn saat dibuat

    def spawn(self):
        """Memindahkan makanan ke posisi acak di dalam dunia."""
        self.x = round(random.randrange(0, config.WORLD_WIDTH - self.block_size) / self.block_size) * self.block_size
        self.y = round(random.randrange(0, config.WORLD_HEIGHT - self.block_size) / self.block_size) * self.block_size

    def draw(self, surface, camera_x, camera_y):
        """Menggambar makanan ke layar, disesuaikan dengan kamera."""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        pygame.draw.rect(surface, self.color, [screen_x, screen_y, self.block_size, self.block_size])

    def get_pos(self):
        """Mendapatkan posisi makanan (koordinat dunia)."""
        return (self.x, self.y)