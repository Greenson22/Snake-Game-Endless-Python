# src/main.py
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
from . import bomb # --- BARU: Impor bom ---

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

    # --- FUNGSI BARU: Helper untuk spawn musuh ---
    def spawn_new_creature(self, creature_class):
        """Helper untuk spawn satu musuh (Enemy atau Rusher)"""
        start_x, start_y = self.snake.get_head_pos()
        
        while True:
            # Tentukan posisi spawn acak
            spawn_x = round(random.randrange(0, config.WORLD_WIDTH - config.SNAKE_BLOCK) 
                            / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
            spawn_y = round(random.randrange(0, config.WORLD_HEIGHT - config.SNAKE_BLOCK) 
                            / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
            
            # Cek jarak dari pemain
            dist = math.sqrt((spawn_x - start_x)**2 + (spawn_y - start_y)**2)
            
            if dist > config.ENEMY_MIN_SPAWN_DIST:
                # Jika jarak aman, buat musuh baru dan tambahkan
                new_creature = creature_class(spawn_x, spawn_y)
                
                # Jika ini Cacing (Enemy), pastikan ia menggunakan delay terbaru
                if isinstance(new_creature, enemy.Enemy):
                    new_creature.move_delay = self.current_enemy_delay
                    
                self.all_creatures.append(new_creature) 
                break # Keluar dari loop while

    # --- FUNGSI reset_game DIMODIFIKASI ---
    def reset_game(self):
        """Mengatur ulang game ke status awal."""
        self.game_over = False
        self.snake = snake.Snake(config.WORLD_WIDTH / 2, config.WORLD_HEIGHT / 2)
        self.food = food.Food()
        self.score = 0
        
        # --- BARU: Pengaturan Level dan Waktu ---
        self.level = 1
        self.start_time = pygame.time.get_ticks() # Waktu awal game (ms)
        self.game_time = 0 # Waktu game dalam detik
        self.next_level_time = config.LEVEL_UP_TIME # Target waktu untuk level 2
        
        # --- BARU: Pengaturan Bom ---
        self.bomb_powerup = None # Awalnya tidak ada bom
        self.last_bomb_spawn_time = 0 # Waktu game (detik) saat bom terakhir spawn
        
        # --- BARU: Pengaturan Kesulitan ---
        self.current_enemy_delay = config.ENEMY_MOVE_DELAY
        
        # Spawn musuh awal
        self.all_creatures = []
        print(f"Game dimulai! Level {self.level}")
        
        for _ in range(config.NUM_ENEMIES):
            self.spawn_new_creature(enemy.Enemy)
        
        for _ in range(config.NUM_RUSHERS):
            self.spawn_new_creature(rusher.Rusher)
            
    # --- FUNGSI BARU: Aktivasi Bom ---
    def activate_bomb(self, bomb_center_x, bomb_center_y):
        """Menghapus musuh di sekitar titik ledakan."""
        creatures_to_remove = []
        radius = config.BOMB_RADIUS_AFFECTED
        
        print(f"BOM meledak di ({bomb_center_x}, {bomb_center_y})!")

        for creature in self.all_creatures:
            # Kita cek jarak dari pusat bom ke kepala musuh
            creature_head_x, creature_head_y = creature.head[0], creature.head[1]
            
            dist = math.sqrt(
                (creature_head_x - bomb_center_x)**2 + 
                (creature_head_y - bomb_center_y)**2
            )
            
            if dist <= radius:
                creatures_to_remove.append(creature)

        # Hapus musuh yang terkena (secara aman di luar loop)
        for creature in creatures_to_remove:
            self.all_creatures.remove(creature)
            
        print(f"{len(creatures_to_remove)} musuh hancur!")

    def run(self):
        """Loop game utama."""
        while self.running:
            if self.game_over:
                self.handle_game_over_events()
            else:
                self.handle_events()
                self.update() # Logika update (termasuk waktu)
            
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

    # --- FUNGSI update DIMODIFIKASI ---
    def update(self):
        """Memperbarui semua logika game (gerakan, tabrakan, waktu, level)."""
        
        # 1. Update Waktu dan Level
        self.game_time = (pygame.time.get_ticks() - self.start_time) // 1000
        
        if self.game_time >= self.next_level_time:
            self.level += 1
            self.next_level_time += config.LEVEL_UP_TIME
            print(f"Naik Level! Selamat datang di Level {self.level}")
            
            # Tingkatkan Kesulitan:
            # a. Tambah 1 Cacing
            self.spawn_new_creature(enemy.Enemy)
            
            # b. Tambah 1 Rusher setiap 2 level
            if self.level % config.RUSHER_SPAWN_PER_LEVEL == 0:
                self.spawn_new_creature(rusher.Rusher)
            
            # c. Percepat Cacing (Enemy)
            new_delay = max(1, int(self.current_enemy_delay * config.ENEMY_SPEED_INCREASE))
            if new_delay < self.current_enemy_delay:
                self.current_enemy_delay = new_delay
                print(f"Cacing dipercepat! Delay baru: {self.current_enemy_delay}")
                # Terapkan delay baru ke semua cacing yang ada
                for creature in self.all_creatures:
                    if isinstance(creature, enemy.Enemy):
                        creature.move_delay = self.current_enemy_delay

        # 2. Update Gerakan
        self.snake.move()
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        self.camera.update(snake_head_x, snake_head_y)
        
        for creature in self.all_creatures:
            creature.update(snake_head_x, snake_head_y, self.all_creatures)
        
        # 3. Cek Tabrakan (Game Over)
        if self.snake.check_collision_self() or self.snake.check_collision_walls():
            self.game_over = True
            return

        for creature in self.all_creatures:
            if creature.check_collision(snake_head_x, snake_head_y):
                self.game_over = True
                return 

        # 4. Cek Makan Makanan
        food_x, food_y = self.food.get_pos()
        if snake_head_x == food_x and snake_head_y == food_y:
            self.snake.grow()
            self.food.spawn()
            self.score = self.snake.length - 1

        # 5. Logika Power-up Bom
        # a. Spawn Bom
        if self.bomb_powerup is None:
            # Jika tidak ada bom, cek apakah sudah waktunya spawn
            if (self.game_time - self.last_bomb_spawn_time) >= config.BOMB_SPAWN_TIME:
                self.bomb_powerup = bomb.Bomb()
                self.last_bomb_spawn_time = self.game_time
                print("Power-up Bom muncul!")
        
        # b. Cek Makan Bom
        if self.bomb_powerup:
            bomb_x, bomb_y = self.bomb_powerup.get_pos()
            if snake_head_x == bomb_x and snake_head_y == bomb_y:
                self.activate_bomb(snake_head_x, snake_head_y)
                self.bomb_powerup = None # Bom hilang setelah dimakan
                # Reset timer agar bom berikutnya tidak langsung spawn
                self.last_bomb_spawn_time = self.game_time 

    # --- FUNGSI draw DIMODIFIKASI ---
    def draw(self):
        """
        Menggambar semua elemen game ke layar.
        """
        cam_x, cam_y = self.camera.get_offset()
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        
        # 1. Gambar semua elemen game
        self.screen.blit(self.background, (0 - cam_x, 0 - cam_y))
        
        # Gambar Bom (jika ada)
        if self.bomb_powerup:
            self.bomb_powerup.draw(self.screen, self.camera) 
            
        # Gambar Makanan (dengan panah)
        self.food.draw(self.screen, self.camera, snake_head_x, snake_head_y)
        
        for creature in self.all_creatures:
            creature.draw(self.screen, cam_x, cam_y)
        self.snake.draw(self.screen, cam_x, cam_y)
        
        # 2. Logika UI
        if self.game_over:
            # Tampilkan UI Game Over (skor, level, waktu)
            ui.draw_game_over_overlay(
                self.screen, self.score, self.level, self.game_time
            )
        else:
            # Tampilkan Skor, Waktu, dan Level saat bermain
            ui.draw_score(self.screen, self.score)
            ui.draw_game_stats(self.screen, self.game_time, self.level)
        
        # 3. Update layar
        pygame.display.update()


# --- Titik Masuk Program ---
if __name__ == "__main__":
    game = Game()
    game.run()