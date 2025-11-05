import pygame
import math  
import random
from . import config
from . import terrain
from . import snake
from . import food
from . import camera
from . import ui
from . import enemy  
from . import rusher 

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.DIS_WIDTH, config.DIS_HEIGHT))
        pygame.display.set_caption('Game Ular vs Musuh') 
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        self.background = terrain.create_terrain_background(
            config.WORLD_WIDTH, config.WORLD_HEIGHT, config.SNAKE_BLOCK
        )
        self.camera = camera.Camera()
        
        self.all_creatures = [] 
        
        self.reset_game() 

    def reset_game(self):
        """Mengatur ulang game ke status awal."""
        self.game_over = False
        self.snake = snake.Snake(config.WORLD_WIDTH / 2, config.WORLD_HEIGHT / 2)
        self.food = food.Food()
        self.score = 0
        
        self.all_creatures = []
        start_x, start_y = self.snake.get_head_pos()
        
        print(f"Game dimulai! {config.NUM_ENEMIES} cacing dan {config.NUM_RUSHERS} rusher muncul.")
        
        # Spawn Cacing Lambat (Enemy)
        for _ in range(config.NUM_ENEMIES):
            while True:
                enemy_x = round(random.randrange(0, config.WORLD_WIDTH - config.SNAKE_BLOCK) 
                                / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
                enemy_y = round(random.randrange(0, config.WORLD_HEIGHT - config.SNAKE_BLOCK) 
                                / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
                dist = math.sqrt((enemy_x - start_x)**2 + (enemy_y - start_y)**2)
                
                if dist > config.ENEMY_MIN_SPAWN_DIST:
                    new_enemy = enemy.Enemy(enemy_x, enemy_y) 
                    self.all_creatures.append(new_enemy) 
                    break 
        
        # Spawn Rusher Cepat
        for _ in range(config.NUM_RUSHERS):
            while True:
                rusher_x = round(random.randrange(0, config.WORLD_WIDTH - config.SNAKE_BLOCK) 
                                 / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
                rusher_y = round(random.randrange(0, config.WORLD_HEIGHT - config.SNAKE_BLOCK) 
                                 / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
                dist = math.sqrt((rusher_x - start_x)**2 + (rusher_y - start_y)**2)
                
                if dist > config.ENEMY_MIN_SPAWN_DIST:
                    new_rusher = rusher.Rusher(rusher_x, rusher_y) 
                    self.all_creatures.append(new_rusher) 
                    break
            
    def run(self):
        """Loop game utama."""
        while self.running:
            
            # --- MODIFIKASI: Logika Loop ---
            if self.game_over:
                # Jika game over, kita HANYA proses input
                self.handle_game_over_events()
                # Kita TIDAK memanggil self.update()
                # Ini "membekukan" game di frame terakhir
            else:
                # Jika game masih jalan, proses input DAN update
                self.handle_events()
                self.update()
            
            # 'draw()' dipanggil SETIAP frame, 
            # baik game over atau tidak
            self.draw() 
            # ----------------------------------
            
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
        
        for creature in self.all_creatures:
            creature.update(snake_head_x, snake_head_y, self.all_creatures)
        
        # Cek tabrakan
        if self.snake.check_collision_self() or self.snake.check_collision_walls():
            self.game_over = True
            print("Game Over! Menabrak diri sendiri atau dinding.")
            return

        for creature in self.all_creatures:
            if creature.check_collision(snake_head_x, snake_head_y):
                self.game_over = True
                print(f"Game Over! Tertangkap musuh ({type(creature).__name__}).")
                return 

        # Cek makan makanan
        food_x, food_y = self.food.get_pos()
        if snake_head_x == food_x and snake_head_y == food_y:
            self.snake.grow()
            self.food.spawn()
            self.score = self.snake.length - 1
            print(f"Makan! Skor sekarang: {self.score}")

    # --- MODIFIKASI: Fungsi 'draw' ---
    def draw(self):
        """
        Menggambar semua elemen game ke layar.
        Sekarang juga menangani penggambaran UI Game Over.
        """
        cam_x, cam_y = self.camera.get_offset()
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        
        # 1. Gambar semua elemen game (selalu digambar)
        self.screen.blit(self.background, (0 - cam_x, 0 - cam_y))
        self.food.draw(self.screen, self.camera, snake_head_x, snake_head_y)
        for creature in self.all_creatures:
            creature.draw(self.screen, cam_x, cam_y)
        self.snake.draw(self.screen, cam_x, cam_y)
        
        # 2. Logika UI
        if self.game_over:
            # Jika game over, gambar UI overlay
            ui.draw_game_over_overlay(self.screen, self.score)
        else:
            # Jika masih main, gambar skor normal
            ui.draw_score(self.screen, self.score)
        
        # 3. Update layar
        pygame.display.update()

    # --- FUNGSI LAMA DIHAPUS ---
    # def draw_game_over(self):
    #     ... (Hapus fungsi ini, logikanya sudah pindah ke draw() dan ui.py) ...


# --- Titik Masuk Program ---
if __name__ == "__main__":
    game = Game()
    game.run()