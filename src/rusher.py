import pygame
import random
import math
from . import config

class Rusher:
    def __init__(self, start_x, start_y):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.RUSHER_COLOR # Menggunakan warna Rusher
        
        # Panjang acak untuk Rusher
        self.length = random.randint(config.RUSHER_MIN_LENGTH, config.RUSHER_MAX_LENGTH)
        
        self.head = [start_x, start_y]
        self.body = []
        for i in range(self.length):
            self.body.append([start_x, start_y])
            
        self.x_change = 0
        self.y_change = 0
        
        # --- BARU: Tambahkan timer untuk kelambatan terrain ---
        self.move_timer = 0

    def _decide_move(self, target_x, target_y):
        """AI Rusher: Sangat ingin lurus, jarang belok."""
        
        # Cek apakah sedang bergerak DAN apakah RNG gagal (tetap lurus)
        is_moving = self.x_change != 0 or self.y_change != 0
        wants_to_turn = random.random() < config.RUSHER_TURN_CHANCE

        if is_moving and not wants_to_turn:
            return # Tetap lurus, jangan putuskan arah baru

        # Jika tidak bergerak ATAU ingin belok (5% chance):
        # Tentukan arah ideal baru (greedy pathfinding)
        dx = target_x - self.head[0]
        dy = target_y - self.head[1]
        
        ideal_x_change = 0
        ideal_y_change = 0

        if abs(dx) > abs(dy):
            if dx > 0: ideal_x_change = self.block_size
            else: ideal_x_change = -self.block_size
        else:
            if dy > 0: ideal_y_change = self.block_size
            else: ideal_y_change = -self.block_size
            
        # Hindari putar balik 180 derajat
        if ideal_x_change != 0 and self.x_change != -ideal_x_change:
            self.x_change = ideal_x_change
            self.y_change = 0
        elif ideal_y_change != 0 and self.y_change != -ideal_y_change:
            self.x_change = 0
            self.y_change = ideal_y_change
        elif not is_moving: # Jika sedang diam, ambil arah ideal
            self.x_change = ideal_x_change
            self.y_change = ideal_y_change
        # (Jika logika di atas gagal/terjebak, biarkan arah lama)

    def _move(self, all_creatures):
        """Perbarui posisi tubuh (logika dari Enemy.py)"""
        
        new_head_x = self.head[0] + self.x_change
        new_head_y = self.head[1] + self.y_change
        
        # 2. Cek tabrakan dengan semua musuh lain (Cacing dan Rusher)
        is_occupied = False
        for creature in all_creatures:
            for segment in creature.body:
                if new_head_x == segment[0] and new_head_y == segment[1]:
                    # Boleh menabrak ekor sendiri
                    if creature == self and segment == self.body[0]:
                        pass 
                    else:
                        is_occupied = True
                        break
            if is_occupied:
                break
        
        if is_occupied:
            self.x_change = 0 # Berhenti
            self.y_change = 0 # Akan memaksa _decide_move
            return 
        # -----------------------------------------------------------

        # 3. Jika lolos semua cek, baru bergerak
        self.head[0] = new_head_x
        self.head[1] = new_head_y
        
        self.body.append(list(self.head)) 
        
        if len(self.body) > self.length:
            del self.body[0]

    def update(self, target_x, target_y, all_creatures, world):
        """
        Fungsi update Rusher.
        (DIPERBARUI DENGAN TERRAIN)
        """
        # --- LOGIKA LAMA (DIHAPUS) ---
        # self._decide_move(target_x, target_y) # Tentukan (atau tidak) arah
        # self._move(all_creatures) # Selalu coba bergerak
        
        # --- LOGIKA BARU (DENGAN TERRAIN) ---
        # 1. Cek terrain di kepala rusher
        current_terrain_type = world.get_tile_type_at_world_pos(self.head[0], self.head[1])
        
        # 2. Dapatkan penalti kecepatan dari terrain (Rusher tidak punya delay dasar)
        terrain_delay = config.TERRAIN_SPEEDS.get(current_terrain_type, 1)
        
        self.move_timer += 1
        
        if self.move_timer >= terrain_delay:
            self.move_timer = 0
            self._decide_move(target_x, target_y) # Tentukan (atau tidak) arah
            self._move(all_creatures) # Coba bergerak

    def draw(self, surface, camera_x, camera_y):
        """Menggambar seluruh tubuh Rusher."""
        # Logika gambar ini identik dengan Enemy.draw
        outline_color = config.BLACK
        border_size = 2
        inner_size = self.block_size - (border_size * 2)

        for segment in self.body:
            screen_x = int(segment[0] - camera_x)
            screen_y = int(segment[1] - camera_y)
            
            pygame.draw.rect(surface, outline_color, [screen_x, screen_y, self.block_size, self.block_size])
            inner_x = screen_x + border_size
            inner_y = screen_y + border_size
            # Gunakan self.color (yang di set di __init__)
            pygame.draw.rect(surface, self.color, [inner_x, inner_y, inner_size, inner_size])

    def check_collision(self, player_head_x, player_head_y):
        """
        Memeriksa tabrakan antara KEPALA PEMAIN dan
        SELURUH TUBUH Rusher.
        """
        player_head_rect = pygame.Rect(player_head_x, player_head_y, self.block_size, self.block_size)
        
        for segment in self.body:
            enemy_segment_rect = pygame.Rect(segment[0], segment[1], self.block_size, self.block_size)
            if player_head_rect.colliderect(enemy_segment_rect):
                return True
        return False