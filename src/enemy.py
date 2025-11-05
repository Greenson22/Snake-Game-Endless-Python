import pygame
import random
import math
from . import config

class Enemy:
    def __init__(self, start_x, start_y):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.ENEMY_COLOR
        
        # Tentukan panjang acak untuk musuh ini
        self.length = random.randint(config.ENEMY_MIN_LENGTH, config.ENEMY_MAX_LENGTH)
        
        # Logika tubuh, sama seperti Snake
        self.head = [start_x, start_y]
        self.body = []
        # Inisialisasi tubuh dengan panjang penuh
        for i in range(self.length):
            self.body.append([start_x, start_y])
            
        self.x_change = 0
        self.y_change = 0
        
        # Kontrol kecepatan
        self.move_timer = 0
        self.move_delay = config.ENEMY_MOVE_DELAY

    def _decide_move(self, target_x, target_y):
        """AI Sederhana: Tentukan arah gerak (greedy)"""
        
        # Hitung jarak
        dx = target_x - self.head[0]
        dy = target_y - self.head[1]
        
        ideal_x_change = 0
        ideal_y_change = 0

        # Tentukan arah prioritas (horizontal atau vertikal)
        if abs(dx) > abs(dy):
            # Prioritas gerak horizontal
            if dx > 0: ideal_x_change = self.block_size
            else: ideal_x_change = -self.block_size
        else:
            # Prioritas gerak vertikal
            if dy > 0: ideal_y_change = self.block_size
            else: ideal_y_change = -self.block_size
            
        # Hindari putar balik 180 derajat
        if ideal_x_change != 0 and self.x_change != -ideal_x_change:
            self.x_change = ideal_x_change
            self.y_change = 0
        elif ideal_y_change != 0 and self.y_change != -ideal_y_change:
            self.x_change = 0
            self.y_change = ideal_y_change
        else:
            # Jika "terjebak" (target ada di belakang), belok saja
            if self.x_change != 0: # Jika sedang gerak horizontal
                self.x_change = 0 # Belok vertikal
                self.y_change = self.block_size if dy > 0 else -self.block_size
            elif self.y_change != 0: # Jika sedang gerak vertikal
                self.x_change = self.block_size if dx > 0 else -self.block_size
                self.y_change = 0 # Belok horizontal
            else: # Jika diam, mulai bergerak
                self.x_change = ideal_x_change
                self.y_change = ideal_y_change

    def _move(self):
        """Perbarui posisi tubuh (logika internal)"""
        
        new_head_x = self.head[0] + self.x_change
        new_head_y = self.head[1] + self.y_change
        
        # Cek tabrakan dinding dunia
        if (new_head_x >= config.WORLD_WIDTH or new_head_x < 0 or
            new_head_y >= config.WORLD_HEIGHT or new_head_y < 0):
            # Jika menabrak dinding, jangan bergerak & reset arah
            self.x_change = 0
            self.y_change = 0
            return # Batal bergerak

        # Perbarui kepala dan tubuh
        self.head[0] = new_head_x
        self.head[1] = new_head_y
        
        self.body.append(list(self.head)) # Tambah kepala baru
        
        # Hapus ekor
        if len(self.body) > self.length:
            del self.body[0]

    def update(self, target_x, target_y):
        """
        Fungsi update utama. Dipanggil setiap frame.
        Memutuskan kapan harus bergerak.
        """
        self.move_timer += 1
        
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self._decide_move(target_x, target_y) # Tentukan arah
            self._move() # Pindahkan tubuh

    def draw(self, surface, camera_x, camera_y):
        """Menggambar seluruh tubuh musuh."""
        outline_color = config.BLACK
        border_size = 2
        inner_size = self.block_size - (border_size * 2)

        for segment in self.body:
            screen_x = int(segment[0] - camera_x)
            screen_y = int(segment[1] - camera_y)
            
            # 1. Gambar outline
            pygame.draw.rect(surface, outline_color, [screen_x, screen_y, self.block_size, self.block_size])
            
            # 2. Gambar isi
            inner_x = screen_x + border_size
            inner_y = screen_y + border_size
            pygame.draw.rect(surface, self.color, [inner_x, inner_y, inner_size, inner_size])

    def check_collision(self, player_head_x, player_head_y):
        """
        Memeriksa tabrakan antara KEPALA PEMAIN dan
        SELURUH TUBUH musuh.
        """
        player_head_rect = pygame.Rect(player_head_x, player_head_y, self.block_size, self.block_size)
        
        # Cek tabrakan dengan setiap segmen tubuh musuh
        for segment in self.body:
            enemy_segment_rect = pygame.Rect(segment[0], segment[1], self.block_size, self.block_size)
            if player_head_rect.colliderect(enemy_segment_rect):
                return True
        return False