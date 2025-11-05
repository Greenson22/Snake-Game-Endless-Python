import pygame
import math  # <-- Pastikan math diimpor
# Menggunakan impor relatif untuk semua modul kita
from . import config
from . import terrain
from . import snake
from . import food
from . import camera
from . import ui
from . import enemy  
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.DIS_WIDTH, config.DIS_HEIGHT))
        pygame.display.set_caption('Game Ular vs Cacing') # Judul baru!
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        self.background = terrain.create_terrain_background(
            config.WORLD_WIDTH, config.WORLD_HEIGHT, config.SNAKE_BLOCK
        )
        self.camera = camera.Camera()
        self.enemies = [] 
        
        self.reset_game() 

    def reset_game(self):
        """Mengatur ulang game ke status awal."""
        self.game_over = False
        self.snake = snake.Snake(config.WORLD_WIDTH / 2, config.WORLD_HEIGHT / 2)
        self.food = food.Food()
        self.score = 0
        
        # --- MODIFIKASI: Logika Spawn Musuh ---
        self.enemies = []
        start_x, start_y = self.snake.get_head_pos()
        
        print(f"Game dimulai! {config.NUM_ENEMIES} musuh muncul. Hati-hati!")
        
        for _ in range(config.NUM_ENEMIES):
            while True:
                # 1. Pilih posisi acak yang TERKAIT GRID
                enemy_x = round(random.randrange(0, config.WORLD_WIDTH - config.SNAKE_BLOCK) 
                                / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
                enemy_y = round(random.randrange(0, config.WORLD_HEIGHT - config.SNAKE_BLOCK) 
                                / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
                
                # 2. Hitung jarak dari pemain
                dist = math.sqrt((enemy_x - start_x)**2 + (enemy_y - start_y)**2)
                
                # 3. Jika jarak aman, buat musuh
                if dist > config.ENEMY_MIN_SPAWN_DIST:
                    # Buat musuh baru di posisi grid
                    new_enemy = enemy.Enemy(enemy_x, enemy_y) 
                    self.enemies.append(new_enemy)
                    break # Lanjut ke musuh berikutnya
        # ---------------------------------------------
            
    def run(self):
        """Loop game utama."""
        while self.running:
            if self.game_over:
                self.handle_game_over_events()
                self.draw_game_over()
            else:
                self.handle_events()
                self.update()
                self.draw()
            
            self.clock.tick(config.SNAKE_SPEED)
        
        pygame.quit()
        quit()

    def handle_events(self):
        """Menangani input saat game berjalan."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.snake.handle_input(event)

    def handle_game_over_events(self):
        """Menangani input saat layar 'Game Over'."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                if event.key == pygame.K_c:
                    self.reset_game()

    def update(self):
        """Memperbarui semua logika game (gerakan, tabrakan)."""
        self.snake.move()
        
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        
        self.camera.update(snake_head_x, snake_head_y)
        
        # --- MODIFIKASI: Panggil 'update' musuh ---
        # (Fungsi 'move' sekarang dipanggil secara internal oleh 'update')
        for e in self.enemies:
            e.update(snake_head_x, snake_head_y)
        # -----------------------------------------
        
        # Cek tabrakan
        if self.snake.check_collision_self() or self.snake.check_collision_walls():
            self.game_over = True
            print("Game Over! Menabrak diri sendiri atau dinding.")
            return

        # Cek tabrakan dengan musuh
        for e in self.enemies:
            # check_collision sekarang memeriksa kepala pemain vs seluruh tubuh musuh
            if e.check_collision(snake_head_x, snake_head_y):
                self.game_over = True
                print("Game Over! Tertangkap musuh.")
                return 

        # Cek makan makanan
        food_x, food_y = self.food.get_pos()
        if snake_head_x == food_x and snake_head_y == food_y:
            self.snake.grow()
            self.food.spawn()
            self.score = self.snake.length - 1
            print(f"Makan! Skor sekarang: {self.score}")

    def draw(self):
        """Menggambar semua elemen game ke layar."""
        cam_x, cam_y = self.camera.get_offset()
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        
        # 1. Gambar background
        self.screen.blit(self.background, (0 - cam_x, 0 - cam_y))
        
        # 2. Gambar makanan (atau panah indikator)
        self.food.draw(self.screen, self.camera, snake_head_x, snake_head_y)
        
        # 3. Gambar musuh (sekarang menggambar seluruh tubuh)
        for e in self.enemies:
            e.draw(self.screen, cam_x, cam_y)
        
        # 4. Gambar ular (di atas musuh)
        self.snake.draw(self.screen, cam_x, cam_y)
        
        # 5. Gambar UI (skor)
        ui.draw_score(self.screen, self.score)
        
        pygame.display.update()

    def draw_game_over(self):
        """Menggambar layar 'Game Over'."""
        self.screen.fill(config.BLUE)
        ui.draw_game_over_message(self.screen)
        ui.draw_score(self.screen, self.score) 
        pygame.display.update()

# --- Titik Masuk Program ---
if __name__ == "__main__":
    game = Game()
    game.run()