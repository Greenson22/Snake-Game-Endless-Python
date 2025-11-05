import pygame
import random
import math
from . import config

class Enemy:
    def __init__(self, start_x, start_y):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.ENEMY_COLOR
        
        self.length = random.randint(config.ENEMY_MIN_LENGTH, config.ENEMY_MAX_LENGTH)
        
        self.head = [start_x, start_y]
        self.body = []
        for i in range(self.length):
            self.body.append([start_x, start_y])
            
        self.x_change = 0
        self.y_change = 0
        
        self.move_timer = 0
        self.move_delay = config.ENEMY_MOVE_DELAY

    def _decide_move(self, target_x, target_y):
        """AI Sederhana: Tentukan arah gerak (greedy)"""
        
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
            
        # Logika anti-putar balik (tetap sama)
        if ideal_x_change != 0 and self.x_change != -ideal_x_change:
            self.x_change = ideal_x_change
            self.y_change = 0
        elif ideal_y_change != 0 and self.y_change != -ideal_y_change:
            self.x_change = 0
            self.y_change = ideal_y_change
        else:
            if self.x_change != 0: 
                self.x_change = 0
                self.y_change = self.block_size if dy > 0 else -self.block_size
            elif self.y_change != 0: 
                self.x_change = self.block_size if dx > 0 else -self.block_size
                self.y_change = 0
            else: 
                self.x_change = ideal_x_change
                self.y_change = ideal_y_change

    # --- MODIFIKASI: _move() sekarang butuh 'all_enemies' ---
    def _move(self, all_enemies):
        """Perbarui posisi tubuh dengan cek tabrakan musuh."""
        
        new_head_x = self.head[0] + self.x_change
        new_head_y = self.head[1] + self.y_change
        
        # 1. Cek tabrakan dinding dunia
        if (new_head_x >= config.WORLD_WIDTH or new_head_x < 0 or
            new_head_y >= config.WORLD_HEIGHT or new_head_y < 0):
            self.x_change = 0
            self.y_change = 0
            return # Batal bergerak

        # --- BARU: Cek tabrakan dengan musuh lain (dan diri sendiri) ---
        is_occupied = False
        for enemy in all_enemies:
            for segment in enemy.body:
                # Cek jika kotak tujuan (new_head) sudah ditempati segmen musuh
                if new_head_x == segment[0] and new_head_y == segment[1]:
                    # Pengecualian: Boleh bergerak ke ekor diri sendiri
                    # (jika ekor itu akan bergeser di frame ini)
                    # Kita sederhanakan: anggap saja semua terisi.
                    # Jika musuh ini adalah diri sendiri DAN segmen ini adalah ekor
                    if enemy == self and segment == self.body[0]:
                        pass # Boleh, ekor akan pindah
                    else:
                        is_occupied = True
                        break
            if is_occupied:
                break
        
        if is_occupied:
            # Kotak tujuan sudah terisi, batalkan gerakan
            # Reset arah agar _decide_move bisa cari jalan lain
            self.x_change = 0
            self.y_change = 0
            return # Batal bergerak
        # -----------------------------------------------------------

        # 3. Jika lolos semua cek, baru bergerak
        self.head[0] = new_head_x
        self.head[1] = new_head_y
        
        self.body.append(list(self.head)) 
        
        if len(self.body) > self.length:
            del self.body[0]

    # --- MODIFIKASI: update() sekarang menerima 'all_enemies' ---
    def update(self, target_x, target_y, all_enemies):
        """
        Fungsi update utama. Dipanggil setiap frame.
        Memutuskan kapan harus bergerak.
        """
        self.move_timer += 1
        
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self._decide_move(target_x, target_y) # Tentukan arah
            self._move(all_enemies) # Pindahkan tubuh (dengan cek tabrakan)

    def draw(self, surface, camera_x, camera_y):
        """Menggambar seluruh tubuh musuh."""
        outline_color = config.BLACK
        border_size = 2
        inner_size = self.block_size - (border_size * 2)

        for segment in self.body:
            screen_x = int(segment[0] - camera_x)
            screen_y = int(segment[1] - camera_y)
            
            pygame.draw.rect(surface, outline_color, [screen_x, screen_y, self.block_size, self.block_size])
            inner_x = screen_x + border_size
            inner_y = screen_y + border_size
            pygame.draw.rect(surface, self.color, [inner_x, inner_y, inner_size, inner_size])

    def check_collision(self, player_head_x, player_head_y):
        """
        Memeriksa tabrakan antara KEPALA PEMAIN dan
        SELURUH TUBUH musuh.
        """
        player_head_rect = pygame.Rect(player_head_x, player_head_y, self.block_size, self.block_size)
        
        for segment in self.body:
            enemy_segment_rect = pygame.Rect(segment[0], segment[1], self.block_size, self.block_size)
            if player_head_rect.colliderect(enemy_segment_rect):
                return True
        return False