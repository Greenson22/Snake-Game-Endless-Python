import pygame
import math  
import random
from . import config
# from . import terrain (Tidak perlu impor terrain lagi di main)
from . import snake
from . import food
from . import camera
from . import ui
from . import enemy  
from . import rusher 
from . import bomb
from . import particle
from . import world # <-- IMPOR BARU: ChunkManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.DIS_WIDTH, config.DIS_HEIGHT))
        pygame.display.set_caption('Game Ular vs Musuh') 
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # --- LOGIKA BACKGROUND LAMA DIHAPUS ---
        
        # --- LOGIKA BARU: ChunkManager ---
        self.world = world.ChunkManager()
        # -----------------------------------
        
        self.camera = camera.Camera()
        
        self.all_creatures = [] 
        self.particles = [] 
        
        # --- LOGIKA MINIMAP LAMA DIHAPUS ---
        
        self.reset_game() 

    def spawn_new_creature(self, creature_class):
        """Helper untuk spawn satu musuh (Relatif terhadap pemain)"""
        start_x, start_y = self.snake.get_head_pos()
        
        # Coba spawn di area "kotak" di sekitar pemain (di luar layar)
        spawn_x = start_x + random.randint(int(config.DIS_WIDTH * 0.6), config.DIS_WIDTH)
        spawn_x = spawn_x if random.random() < 0.5 else -spawn_x
        
        spawn_y = start_y + random.randint(int(config.DIS_HEIGHT * 0.6), config.DIS_HEIGHT)
        spawn_y = spawn_y if random.random() < 0.5 else -spawn_y

        # Bulatkan ke grid
        spawn_x = round(spawn_x / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
        spawn_y = round(spawn_y / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
            
        # Cek jarak MINIMUM (tetap berguna)
        dist = math.sqrt((spawn_x - start_x)**2 + (spawn_y - start_y)**2)
        
        if dist > config.ENEMY_MIN_SPAWN_DIST:
            new_creature = creature_class(spawn_x, spawn_y)
            if isinstance(new_creature, enemy.Enemy):
                new_creature.move_delay = self.current_enemy_delay
            self.all_creatures.append(new_creature) 
        else:
            # Gagal spawn (terlalu dekat), coba lagi di frame berikutnya
            pass

    def reset_game(self):
        """Mengatur ulang game ke status awal."""
        self.game_over = False
        
        # Mulai ular di pusat dunia (0, 0)
        self.snake = snake.Snake(0, 0)
        self.food = food.Food()
        self.food.spawn(0, 0) # Spawn makanan pertama di dekat pemain
        
        self.score = 0
        
        # Pengaturan Level dan Waktu
        self.level = 1
        self.start_time = pygame.time.get_ticks()
        self.game_time = 0
        self.next_level_time = config.LEVEL_UP_TIME
        
        # Pengaturan Bom
        self.bomb_powerup = None
        self.last_bomb_spawn_time = 0
        
        # Pengaturan Kesulitan
        self.current_enemy_delay = config.ENEMY_MOVE_DELAY
        
        # Timer untuk gerakan ular berbasis terrain
        self.snake_move_timer = 0
        
        # Kosongkan entitas
        self.all_creatures = []
        self.particles = [] 
        
        print(f"Game dimulai! Level {self.level}")
        
        # Spawn musuh awal di dekat pemain
        for _ in range(config.NUM_ENEMIES):
            self.spawn_new_creature(enemy.Enemy)
        for _ in range(config.NUM_RUSHERS):
            self.spawn_new_creature(rusher.Rusher)
            
    def activate_bomb(self, bomb_center_x, bomb_center_y):
        """Menghapus musuh di sekitar titik ledakan."""
        creatures_to_remove = []
        radius = config.BOMB_RADIUS_AFFECTED
        
        print(f"BOM meledak di ({bomb_center_x}, {bomb_center_y})!")

        for creature in self.all_creatures:
            creature_head_x, creature_head_y = creature.head[0], creature.head[1]
            dist = math.sqrt(
                (creature_head_x - bomb_center_x)**2 + 
                (creature_head_y - bomb_center_y)**2
            )
            
            if dist <= radius:
                creatures_to_remove.append(creature)

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
                self.update()
            
            self.draw() 
            self.clock.tick(config.SNAKE_SPEED)
        
        # --- BARU: Simpan dunia saat keluar ---
        self.world.save_world()
        
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
        """Memperbarui semua logika game (gerakan, tabrakan, waktu, level)."""
        
        # 1. Update Waktu dan Level
        self.game_time = (pygame.time.get_ticks() - self.start_time) // 1000
        
        if self.game_time >= self.next_level_time:
            self.level += 1
            self.next_level_time += config.LEVEL_UP_TIME
            print(f"Naik Level! Selamat datang di Level {self.level}")
            
            # Tingkatkan Kesulitan: Spawn musuh baru
            self.spawn_new_creature(enemy.Enemy)
            if self.level % config.RUSHER_SPAWN_PER_LEVEL == 0:
                self.spawn_new_creature(rusher.Rusher)
            
            # Percepat musuh yang ada
            new_delay = max(1, int(self.current_enemy_delay * config.ENEMY_SPEED_INCREASE))
            if new_delay < self.current_enemy_delay:
                self.current_enemy_delay = new_delay
                print(f"Cacing dipercepat! Delay baru: {self.current_enemy_delay}")
                for creature in self.all_creatures:
                    if isinstance(creature, enemy.Enemy):
                        creature.move_delay = self.current_enemy_delay

        # 2. Update Gerakan Ular
        self.snake_move_timer += 1
        
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        
        # --- MODIFIKASI: Ambil tipe tile dari World ---
        current_terrain_type = self.world.get_tile_type_at_world_pos(
            snake_head_x, snake_head_y
        )
        
        move_delay = config.TERRAIN_SPEEDS.get(current_terrain_type, 1)
        
        if self.snake_move_timer >= move_delay:
            self.snake_move_timer = 0
            self.snake.move()
            
            # (Logika partikel tetap sama)
            part_color = config.TERRAIN_PARTICLE_COLORS.get(
                current_terrain_type, config.GRASS_COLOR
            )
            new_head_x, new_head_y = self.snake.get_head_pos()
            for _ in range(3):
                self.particles.append(particle.Particle(
                    new_head_x + config.SNAKE_BLOCK // 2,
                    new_head_y + config.SNAKE_BLOCK // 2,
                    part_color
                ))
        
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        
        # 3. Update Kamera, Musuh, dan Partikel
        self.camera.update(snake_head_x, snake_head_y)
        
        for creature in self.all_creatures:
            creature.update(snake_head_x, snake_head_y, self.all_creatures)
        
        self.particles = [p for p in self.particles if p.update()]

        # 4. Cek Tabrakan
        # --- MODIFIKASI: Hapus tabrakan dinding ---
        if self.snake.check_collision_self():
            self.game_over = True
            print("Game Over! Menabrak diri sendiri.")
            return

        for creature in self.all_creatures:
            if creature.check_collision(snake_head_x, snake_head_y):
                self.game_over = True
                print(f"Game Over! Tertangkap musuh ({type(creature).__name__}).")
                return 

        # 5. Cek Makan Makanan
        food_x, food_y = self.food.get_pos()
        if snake_head_x == food_x and snake_head_y == food_y:
            self.snake.grow()
            # Spawn makanan baru di dekat pemain
            self.food.spawn(snake_head_x, snake_head_y)
            self.score = self.snake.length - 1
            print(f"Makan! Skor sekarang: {self.score}")

        # 6. Logika Power-up Bom
        if self.bomb_powerup is None:
            if (self.game_time - self.last_bomb_spawn_time) >= config.BOMB_SPAWN_TIME:
                # Spawn bom baru di dekat pemain
                self.bomb_powerup = bomb.Bomb(snake_head_x, snake_head_y)
                self.last_bomb_spawn_time = self.game_time
                print("Power-up Bom muncul!")
        
        if self.bomb_powerup:
            bomb_x, bomb_y = self.bomb_powerup.get_pos()
            if snake_head_x == bomb_x and snake_head_y == bomb_y:
                self.activate_bomb(snake_head_x, snake_head_y)
                self.bomb_powerup = None
                self.last_bomb_spawn_time = self.game_time 

    # --- FUNGSI MINIMAP LAMA DIHAPUS ---

    # --- MODIFIKASI TOTAL: Fungsi draw ---
    def draw(self):
        """
        Menggambar semua elemen game ke layar.
        """
        cam_x_f, cam_y_f = self.camera.x, self.camera.y
        cam_x, cam_y = int(cam_x_f), int(cam_y_f)
        
        # 1. Gambar Dunia (Chunk)
        self.screen.fill(config.BLACK) # Latar belakang default
        
        chunk_size_pixels = config.CHUNK_SIZE * config.SNAKE_BLOCK
        
        # Hitung koordinat chunk di pojok kiri atas kamera
        start_cx, start_cy = self.world.get_chunk_coords_from_world_pos(
            cam_x_f, cam_y_f
        )
        
        # Hitung berapa banyak chunk yang muat di layar
        num_chunks_x = int(config.DIS_WIDTH / chunk_size_pixels) + 2
        num_chunks_y = int(config.DIS_HEIGHT / chunk_size_pixels) + 2
        
        # Loop dari kiri atas ke kanan bawah layar
        for y in range(num_chunks_y):
            for x in range(num_chunks_x):
                chunk_to_draw_x = start_cx + x
                chunk_to_draw_y = start_cy + y
                
                # Ambil (atau buat) surface chunk
                chunk_surface = self.world.get_or_generate_chunk_surface(
                    chunk_to_draw_x, chunk_to_draw_y
                )
                
                # Hitung posisi pixel dunia chunk ini
                world_px = chunk_to_draw_x * chunk_size_pixels
                world_py = chunk_to_draw_y * chunk_size_pixels
                
                # Hitung posisi layar (setelah digeser kamera)
                screen_px = world_px - cam_x
                screen_py = world_py - cam_y
                
                # Gambar chunk ke layar
                self.screen.blit(chunk_surface, (screen_px, screen_py))

        # 2. Gambar Entitas (Partikel, Bom, Makanan, Musuh, Ular)
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        
        for p in self.particles:
            p.draw(self.screen, cam_x, cam_y)

        if self.bomb_powerup:
            self.bomb_powerup.draw(self.screen, self.camera) 
            
        self.food.draw(self.screen, self.camera, snake_head_x, snake_head_y)
        
        for creature in self.all_creatures:
            creature.draw(self.screen, cam_x, cam_y)
        self.snake.draw(self.screen, cam_x, cam_y)
        
        # 3. Logika UI
        if self.game_over:
            ui.draw_game_over_overlay(
                self.screen, self.score, self.level, self.game_time
            )
        else:
            ui.draw_score(self.screen, self.score)
            ui.draw_game_stats(self.screen, self.game_time, self.level)
            
            # Panggilan _draw_minimap() dihapus
        
        # 4. Update layar
        pygame.display.update()

# --- Titik Masuk Program ---
if __name__ == "__main__":
    game = Game()
    game.run()