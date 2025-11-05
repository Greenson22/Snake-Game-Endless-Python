import pygame
from . import config

class Snake:
    def __init__(self, start_x, start_y):
        self.block_size = config.SNAKE_BLOCK
        self.color = config.SNAKE_COLOR
        self.head = [start_x, start_y]
        self.body = [[start_x, start_y]]
        self.length = 1
        self.x_change = 0
        self.y_change = 0

    def handle_input(self, event):
        """Mengubah arah berdasarkan input tombol."""
        if event.key == pygame.K_LEFT and self.x_change == 0:
            self.x_change = -self.block_size
            self.y_change = 0
        elif event.key == pygame.K_RIGHT and self.x_change == 0:
            self.x_change = self.block_size
            self.y_change = 0
        elif event.key == pygame.K_UP and self.y_change == 0:
            self.y_change = -self.block_size
            self.x_change = 0
        elif event.key == pygame.K_DOWN and self.y_change == 0:
            self.y_change = self.block_size
            self.x_change = 0

    def move(self):
        """Memperbarui posisi ular."""
        self.head[0] += self.x_change
        self.head[1] += self.y_change

        # Tambahkan kepala baru ke tubuh
        self.body.append(list(self.head)) # Salin list kepala
        
        # Hapus ekor jika ular tidak bertambah panjang
        if len(self.body) > self.length:
            del self.body[0]

    def grow(self):
        """Menambah panjang ular."""
        self.length += 1

    def check_collision_self(self):
        """Memeriksa apakah ular menabrak dirinya sendiri."""
        # Periksa jika kepala ada di segmen tubuh lainnya
        for segment in self.body[:-1]:
            if segment == self.head:
                return True
        return False

    def check_collision_walls(self):
        """Memeriksa tabrakan dengan batas dunia."""
        if (self.head[0] >= config.WORLD_WIDTH or self.head[0] < 0 or
            self.head[1] >= config.WORLD_HEIGHT or self.head[1] < 0):
            return True
        return False

    def draw(self, surface, camera_x, camera_y):
        """Menggambar ular ke layar, disesuaikan dengan kamera."""
        for segment in self.body:
            screen_x = segment[0] - camera_x
            screen_y = segment[1] - camera_y
            pygame.draw.rect(surface, self.color, [screen_x, screen_y, self.block_size, self.block_size])

    def get_head_pos(self):
        """Mendapatkan posisi kepala ular (koordinat dunia)."""
        return (self.head[0], self.head[1])