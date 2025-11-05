import pygame
import random
import math # Impor math
from . import config

class Bomb:
    def __init__(self, player_x, player_y):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.BOMB_COLOR
        self.x = 0
        self.y = 0
        self.spawn(player_x, player_y) # Langsung spawn saat dibuat

    def spawn(self, player_x, player_y):
        """Memindahkan bom ke posisi acak DI DEKAT PEMAIN."""
        
        # Tentukan jarak acak dari pemain
        spawn_dist = random.randint(config.ITEM_SPAWN_RADIUS_MIN, config.ITEM_SPAWN_RADIUS_MAX)
        # Tentukan sudut acak
        angle = random.uniform(0, 2 * math.pi)
        
        # Hitung posisi spawn baru
        spawn_x = player_x + (spawn_dist * math.cos(angle))
        spawn_y = player_y + (spawn_dist * math.sin(angle))
        
        # Bulatkan ke grid
        self.x = round(spawn_x / self.block_size) * self.block_size
        self.y = round(spawn_y / self.block_size) * self.block_size

    def get_pos(self):
        """Mendapatkan posisi bom (koordinat dunia)."""
        return (self.x, self.y)

    def draw(self, surface, camera):
        """Menggambar bom jika di layar."""
        cam_x, cam_y = camera.get_offset()
        screen_width = camera.screen_width
        screen_height = camera.screen_height
        bomb_screen_x = self.x - cam_x
        bomb_screen_y = self.y - cam_y
        is_on_screen = (0 < bomb_screen_x < screen_width) and (0 < bomb_screen_y < screen_height)

        if is_on_screen:
            pygame.draw.rect(surface, self.color, [bomb_screen_x, bomb_screen_y, self.block_size, self.block_size])