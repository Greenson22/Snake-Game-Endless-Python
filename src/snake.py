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
        self.body.append(list(self.head))
        if len(self.body) > self.length:
            del self.body[0]

    def grow(self, score_value):
        """
        Menambah panjang ular berdasarkan skor makanan.
        Setiap FOOD_SCORE_BASE poin menambah 1 panjang.
        """
        growth_amount = max(1, (score_value // config.FOOD_SCORE_BASE))
        self.length += growth_amount

    def check_collision_self(self):
        """Memeriksa apakah ular menabrak dirinya sendiri."""
        for segment in self.body[:-1]:
            if segment == self.head:
                return True
        return False

    def draw(self, surface, camera_x, camera_y):
        """Menggambar ular ke layar, disesuaikan dengan kamera (dengan outline)."""
        outline_color = config.BLACK
        border_size = 2 
        inner_size = self.block_size - (border_size * 2) 

        for segment in self.body:
            screen_x = segment[0] - camera_x
            screen_y = segment[1] - camera_y
            pygame.draw.rect(surface, outline_color, [screen_x, screen_y, self.block_size, self.block_size])
            inner_x = screen_x + border_size
            inner_y = screen_y + border_size
            pygame.draw.rect(surface, self.color, [inner_x, inner_y, inner_size, inner_size])

    def get_head_pos(self):
        """Mendapatkan posisi kepala ular (koordinat dunia)."""
        return (self.head[0], self.head[1])