import pygame
import random
import math
from . import config

ARROW_RADIUS = 50

class Food:
    def __init__(self):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.FOOD_COLOR
        self.arrow_color = config.WHITE
        self.x = 0
        self.y = 0
        # HAPUS self.spawn() dari __init__

    def spawn(self, player_x, player_y):
        """Memindahkan makanan ke posisi acak DI DEKAT PEMAIN."""
        
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
        """Mendapatkan posisi makanan (koordinat dunia)."""
        return (self.x, self.y)

    def draw(self, surface, camera, snake_head_x, snake_head_y):
        # ... (Sisa fungsi draw tidak berubah) ...
        cam_x, cam_y = camera.get_offset()
        screen_width = camera.screen_width
        screen_height = camera.screen_height
        food_screen_x = self.x - cam_x
        food_screen_y = self.y - cam_y
        is_on_screen = (0 < food_screen_x < screen_width) and (0 < food_screen_y < screen_height)

        if is_on_screen:
            pygame.draw.rect(surface, self.color, [food_screen_x, food_screen_y, self.block_size, self.block_size])
        else:
            delta_x = self.x - snake_head_x
            delta_y = self.y - snake_head_y
            angle_rad = math.atan2(-delta_y, delta_x)
            snake_screen_x = snake_head_x - cam_x
            snake_screen_y = snake_head_y - cam_y
            arrow_anchor_x = snake_screen_x + math.cos(angle_rad) * ARROW_RADIUS
            arrow_anchor_y = snake_screen_y - math.sin(angle_rad) * ARROW_RADIUS
            arrow_size = 10
            points = [
                (arrow_size, 0),
                (-arrow_size, -arrow_size // 2),
                (-arrow_size, arrow_size // 2)
            ]
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            rotated_points = []
            for x, y in points:
                x_rot = x * cos_a - y * sin_a
                y_rot = x * sin_a + y * cos_a
                final_x = x_rot + arrow_anchor_x
                final_y = -y_rot + arrow_anchor_y 
                rotated_points.append((final_x, final_y))
            pygame.draw.polygon(surface, self.arrow_color, rotated_points)