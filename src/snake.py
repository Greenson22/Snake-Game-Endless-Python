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
        
        # --- BARU: Level Prestise ---
        # `prestige_tier`: Level warna saat ini (0 = Hijau, 1 = Emas, 2 = Perak, dst.)
        self.prestige_tier = 0
        
        # `prestige_level`: Berapa banyak segmen (dari kepala) 
        #                   yang memiliki warna tier saat ini.
        self.prestige_level = 0

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
        Menambah panjang ular ATAU level prestise berlapis.
        Panjang dibatasi, tapi prestise tidak.
        """
        growth_amount = max(1, (score_value // config.FOOD_SCORE_BASE))
        
        # Proses setiap poin pertumbuhan satu per satu
        for _ in range(growth_amount):
            if self.length < config.SNAKE_MAX_LENGTH:
                # Kasus 1: Ular masih tumbuh normal
                self.length += 1
                
            elif self.prestige_level < config.SNAKE_MAX_LENGTH:
                # Kasus 2: Ular sudah maksimal, mulai isi 'prestige_level'
                self.prestige_level += 1
                if self.prestige_tier == 0:
                    # Ini adalah pertama kalinya kita mengisi,
                    # jadi kita pindah ke Tier 1 (Emas)
                    self.prestige_tier = 1
                    
            else:
                # Kasus 3: Ular sudah maksimal DAN prestige_level penuh
                # (Misal: 12 segmen Emas). Saatnya naik tier.
                
                max_tier = len(config.SNAKE_PRESTIGE_COLORS)
                
                if self.prestige_tier < max_tier:
                    # Masih ada tier warna berikutnya
                    self.prestige_tier += 1 # Pindah ke Tier 2 (Perak)
                    self.prestige_level = 1 # Reset level (segmen kepala)
                else:
                    # Sudah di tier terakhir (misal: Berlian)
                    # Biarkan saja, ular tetap di warna maksimal
                    pass


    def check_collision_self(self):
        """Memeriksa apakah ular menabrak dirinya sendiri."""
        for segment in self.body[:-1]:
            if segment == self.head:
                return True
        return False

    def draw(self, surface, camera_x, camera_y):
        """
        Menggambar ular ke layar (DIPERBARUI).
        Sekarang bisa menggambar 2 warna (tier saat ini dan tier sebelumnya).
        """
        outline_color = config.BLACK
        border_size = 2 
        inner_size = self.block_size - (border_size * 2) 

        # 1. Tentukan warna untuk tier saat ini dan sebelumnya
        current_color = config.SNAKE_COLOR
        previous_color = config.SNAKE_COLOR
        
        max_tier_index = len(config.SNAKE_PRESTIGE_COLORS) - 1

        if self.prestige_tier == 1:
            # Transisi dari Hijau (dasar) ke Emas (tier 1)
            current_color = config.SNAKE_PRESTIGE_COLORS[0]
            previous_color = config.SNAKE_COLOR
            
        elif self.prestige_tier > 1:
            # Transisi dari Emas ke Perak, atau Perak ke Rubi, dst.
            current_index = min(self.prestige_tier - 1, max_tier_index)
            prev_index = min(self.prestige_tier - 2, max_tier_index)
            
            current_color = config.SNAKE_PRESTIGE_COLORS[current_index]
            previous_color = config.SNAKE_PRESTIGE_COLORS[prev_index]


        # 2. Gambar segmen
        body_total_segments = len(self.body)

        for i, segment in enumerate(self.body):
            
            # Tentukan warna segmen
            # 'i' berjalan dari 0 (ekor) ke (panjang-1) (kepala)
            
            # Indeks di mana warna baru (prestise) dimulai
            prestige_start_index = body_total_segments - self.prestige_level
            
            if self.prestige_tier == 0:
                # Kasus 0: Ular masih hijau total
                segment_color = config.SNAKE_COLOR
            
            elif i >= prestige_start_index:
                # Segmen ini adalah bagian dari 'tier saat ini' (misal: Emas)
                segment_color = current_color
            else:
                # Segmen ini adalah bagian dari 'tier sebelumnya' (misal: Hijau)
                segment_color = previous_color

            # Gambar segmen
            screen_x = segment[0] - camera_x
            screen_y = segment[1] - camera_y
            pygame.draw.rect(surface, outline_color, [screen_x, screen_y, self.block_size, self.block_size])
            inner_x = screen_x + border_size
            inner_y = screen_y + border_size
            pygame.draw.rect(surface, segment_color, [inner_x, inner_y, inner_size, inner_size])

    def get_head_pos(self):
        """Mendapatkan posisi kepala ular (koordinat dunia)."""
        return (self.head[0], self.head[1])