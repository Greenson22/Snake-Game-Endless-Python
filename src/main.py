import pygame
import math  
import random
from . import config
# (impor terrain tidak perlu)
from . import snake
from . import food # <-- Kelas Food sekarang sederhana
from . import camera
from . import ui
from . import enemy  
from . import rusher 
from . import bomb
from . import particle
from . import world # <-- IMPOR PENTING

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.DIS_WIDTH, config.DIS_HEIGHT))
        pygame.display.set_caption('Game Ular vs Musuh') 
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # --- LOGIKA BARU: ChunkManager ---
        self.world = world.ChunkManager()
        
        self.camera = camera.Camera()
        
        self.all_creatures = [] 
        self.particles = [] 
        
        # --- BARU: List Makanan ---
        self.foods = [] # Mengganti self.food
        
        # --- Inisialisasi Minimap (Radar) ---
        self.minimap_rect = pygame.Rect(
            config.MINIMAP_X_POS,
            config.MINIMAP_Y_POS,
            config.MINIMAP_WIDTH,
            config.MINIMAP_HEIGHT
        )
        self.minimap_surface = pygame.Surface(
            (config.MINIMAP_WIDTH, config.MINIMAP_HEIGHT), pygame.SRCALPHA
        )
        # (Warna diisi di _draw_minimap)
        # -------------------------------------------
        
        self.reset_game() 

    def spawn_new_creature(self, creature_class):
        """Helper untuk spawn satu musuh (Relatif terhadap pemain)"""
        start_x, start_y = self.snake.get_head_pos()
        
        # Coba spawn di area "kotak" di sekitar pemain (di luar layar)
        spawn_x = start_x + random.randint(int(config.DIS_WIDTH * 0.6), config.DIS_WIDTH)
        spawn_x = spawn_x if random.random() < 0.5 else -spawn_x
        
        spawn_y = start_y + random.randint(int(config.DIS_HEIGHT * 0.6), config.DIS_HEIGHT)
        spawn_y = spawn_y if random.random() < 0.5 else -spawn_y

        spawn_x = round(spawn_x / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
        spawn_y = round(spawn_y / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
            
        dist = math.sqrt((spawn_x - start_x)**2 + (spawn_y - start_y)**2)
        
        if dist > config.ENEMY_MIN_SPAWN_DIST:
            new_creature = creature_class(spawn_x, spawn_y)
            if isinstance(new_creature, enemy.Enemy):
                new_creature.move_delay = self.current_enemy_delay
            self.all_creatures.append(new_creature) 
        else:
            pass

    # --- FUNGSI BARU: Spawn makanan dengan cek bioma ---
    def _spawn_one_food(self):
        """Mencari lokasi valid dan men-spawn satu makanan."""
        player_x, player_y = self.snake.get_head_pos()
        
        spawn_attempts = 0
        while spawn_attempts < 50: # Coba 50x untuk cari tempat
            spawn_attempts += 1
            
            # 1. Tentukan Jarak & Sudut acak (logika dari food.py lama)
            spawn_dist = random.randint(config.ITEM_SPAWN_RADIUS_MIN, config.ITEM_SPAWN_RADIUS_MAX)
            angle = random.uniform(0, 2 * math.pi)
            
            spawn_x = player_x + (spawn_dist * math.cos(angle))
            spawn_y = player_y + (spawn_dist * math.sin(angle))
            
            # 2. Bulatkan ke grid
            spawn_x = round(spawn_x / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
            spawn_y = round(spawn_y / config.SNAKE_BLOCK) * config.SNAKE_BLOCK
            
            # 3. Cek Bioma di lokasi tsb
            tile_type = self.world.get_tile_type_at_world_pos(spawn_x, spawn_y)
            
            # 4. Cek Aturan Makanan
            food_rule = config.BIOME_FOOD_RULES.get(tile_type)
            
            # --- LOGIKA DIPERBARUI: Cek Probabilitas ---
            if food_rule is not None:
                # 1. Ambil 3 nilai (termasuk probabilitas)
                food_color, food_score, spawn_chance = food_rule
                
                # 2. Lakukan 'lemparan dadu'
                if random.random() < spawn_chance:
                    # Sukses! (Misal: 0.05 < 0.1 di Rumput)
                    # Buat objek Food baru dan tambahkan ke list
                    new_food = food.Food(spawn_x, spawn_y, food_color, food_score)
                    self.foods.append(new_food)
                    return # Hentikan fungsi
                
                # Jika gagal (Misal: 0.5 > 0.1 di Rumput),
                # 'if' ini dilewati, dan loop 'while' berlanjut
                # untuk mencari titik baru.
            
            # Jika food_rule == None (misal: Air),
            # 'if' utama dilewati, dan loop 'while' berlanjut.

        # Jika loop gagal 50x
        pass

    # --- FUNGSI BARU: Menjaga populasi makanan ---
    def _maintain_food_population(self):
        """Memastikan jumlah makanan di dunia sesuai config."""
        while len(self.foods) < config.MAX_FOOD_COUNT:
            self._spawn_one_food()

    def reset_game(self):
        """Mengatur ulang game ke status awal."""
        self.game_over = False
        
        self.snake = snake.Snake(0, 0)
        
        # --- DIPERBARUI: Makanan ---
        self.foods = [] # Kosongkan list makanan
        
        self.score = 0
        
        # Pengaturan Level dan Waktu
        self.level = 1
        self.start_time = pygame.time.get_ticks()
        self.game_time = 0
        self.next_level_time = config.LEVEL_UP_TIME
        
        self.bomb_powerup = None
        self.last_bomb_spawn_time = 0
        self.current_enemy_delay = config.ENEMY_MOVE_DELAY
        self.snake_move_timer = 0
        
        self.all_creatures = []
        self.particles = [] 
        
        print(f"Game dimulai! Level {self.level}")
        
        # Spawn musuh awal
        for _ in range(config.NUM_ENEMIES):
            self.spawn_new_creature(enemy.Enemy)
        for _ in range(config.NUM_RUSHERS):
            self.spawn_new_creature(rusher.Rusher)
            
        # Spawn makanan awal
        self._maintain_food_population()
            
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
            
            self.spawn_new_creature(enemy.Enemy)
            if self.level % config.RUSHER_SPAWN_PER_LEVEL == 0:
                self.spawn_new_creature(rusher.Rusher)
            
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
        
        current_terrain_type = self.world.get_tile_type_at_world_pos(
            snake_head_x, snake_head_y
        )
        move_delay = config.TERRAIN_SPEEDS.get(current_terrain_type, 1)
        
        if self.snake_move_timer >= move_delay:
            self.snake_move_timer = 0
            self.snake.move()
            
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
        
        # 3. Update Kamera, Musuh, Partikel
        self.camera.update(snake_head_x, snake_head_y)
        
        # --- PERUBAHAN DI SINI ---
        for creature in self.all_creatures:
            # Berikan 'self.world' agar musuh bisa cek terrain
            creature.update(snake_head_x, snake_head_y, self.all_creatures, self.world)
        # ------------------------
        
        self.particles = [p for p in self.particles if p.update()]

        # 4. Cek Tabrakan
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
        food_eaten = None
        for f in self.foods:
            food_x, food_y = f.get_pos()
            if snake_head_x == food_x and snake_head_y == food_y:
                food_eaten = f
                break 

        if food_eaten:
            self.snake.grow(food_eaten.score) 
            self.score += food_eaten.score 
            self.foods.remove(food_eaten) 
            print(f"Makan! Skor sekarang: {self.score}")

        # 6. Panggil Maintainer Makanan (BARU)
        self._maintain_food_population()

        # 7. Logika Power-up Bom
        if self.bomb_powerup is None:
            if (self.game_time - self.last_bomb_spawn_time) >= config.BOMB_SPAWN_TIME:
                self.bomb_powerup = bomb.Bomb(snake_head_x, snake_head_y)
                self.last_bomb_spawn_time = self.game_time
                print("Power-up Bom muncul!")
        
        if self.bomb_powerup:
            bomb_x, bomb_y = self.bomb_powerup.get_pos()
            if snake_head_x == bomb_x and snake_head_y == bomb_y:
                self.activate_bomb(snake_head_x, snake_head_y)
                self.bomb_powerup = None
                self.last_bomb_spawn_time = self.game_time 

    def _draw_minimap(self, player_x, player_y):
        """Menggambar radar minimap dinamis, TERMASUK TERRAIN."""
        
        # --- Bagian 1: Menggambar Latar (Terrain) ke Surface ---
        self.minimap_surface.fill(
            (config.MINIMAP_BG_COLOR[0], 
             config.MINIMAP_BG_COLOR[1], 
             config.MINIMAP_BG_COLOR[2], 
             config.MINIMAP_BG_ALPHA)
        )

        color_map = config.TERRAIN_PARTICLE_COLORS 
        sample_grid_size = config.MINIMAP_TERRAIN_SAMPLES
        pixel_size_x = self.minimap_rect.width / sample_grid_size
        pixel_size_y = self.minimap_rect.height / sample_grid_size
        world_radius = config.MINIMAP_VIEW_RADIUS_WORLD
        world_diameter = world_radius * 2
        world_step = world_diameter / sample_grid_size
        start_world_x = player_x - world_radius
        start_world_y = player_y - world_radius

        for y_step in range(sample_grid_size):
            for x_step in range(sample_grid_size):
                current_world_x = start_world_x + (x_step * world_step)
                current_world_y = start_world_y + (y_step * world_step)
                tile_type = self.world.get_tile_type_at_world_pos(
                    current_world_x, current_world_y
                )
                tile_color = color_map.get(tile_type, config.GRASS_COLOR)
                draw_x = x_step * pixel_size_x
                draw_y = y_step * pixel_size_y
                pygame.draw.rect(
                    self.minimap_surface,
                    tile_color,
                    (draw_x, draw_y, math.ceil(pixel_size_x), math.ceil(pixel_size_y))
                )
        
        # --- Bagian 2: Menggambar ke Layar (Screen) ---
        self.screen.blit(self.minimap_surface, self.minimap_rect.topleft)
        pygame.draw.rect(
            self.screen, 
            config.WHITE, 
            self.minimap_rect, 
            config.MINIMAP_BORDER_WIDTH
        )
        
        map_center_x = self.minimap_rect.centerx
        map_center_y = self.minimap_rect.centery
        world_radius_blip = config.MINIMAP_VIEW_RADIUS_WORLD
        map_radius = config.MINIMAP_RADIUS_PIXELS

        # --- FUNGSI HELPER 'draw_blip' (Menghilangkan blip di luar jangkauan) ---
        def draw_blip(world_x, world_y, color):
            delta_x = world_x - player_x
            delta_y = world_y - player_y
            dist = math.sqrt(delta_x**2 + delta_y**2)
            
            if dist > world_radius_blip:
                 return 

            norm_x = delta_x / world_radius_blip
            norm_y = delta_y / world_radius_blip
            blip_x = map_center_x + (norm_x * map_radius)
            blip_y = map_center_y + (norm_y * map_radius)

            blip_x = max(self.minimap_rect.left + 2, min(self.minimap_rect.right - 2, blip_x))
            blip_y = max(self.minimap_rect.top + 2, min(self.minimap_rect.bottom - 2, blip_y))
            
            pygame.draw.rect(self.screen, color, (blip_x, blip_y, 2, 2))

        # a. Gambar Makanan
        for f in self.foods:
            draw_blip(f.x, f.y, config.MINIMAP_FOOD_COLOR) 
        
        # b. Gambar Bom
        if self.bomb_powerup:
            draw_blip(self.bomb_powerup.x, self.bomb_powerup.y, config.MINIMAP_BOMB_COLOR)

        # c. Gambar Musuh
        for creature in self.all_creatures:
            color = config.MINIMAP_ENEMY_COLOR
            if isinstance(creature, rusher.Rusher):
                color = config.MINIMAP_RUSHER_COLOR
            draw_blip(creature.head[0], creature.head[1], color)
            
        # d. Gambar Pemain (selalu di tengah)
        pygame.draw.rect(
            self.screen, 
            config.MINIMAP_PLAYER_COLOR, 
            (map_center_x - 1, map_center_y - 1, 3, 3) 
        )

    def draw(self):
        """
        Menggambar semua elemen game ke layar.
        """
        cam_x_f, cam_y_f = self.camera.x, self.camera.y
        cam_x, cam_y = int(cam_x_f), int(cam_y_f)
        
        # 1. Gambar Dunia (Chunk)
        self.screen.fill(config.BLACK) 
        chunk_size_pixels = config.CHUNK_SIZE * config.SNAKE_BLOCK
        start_cx, start_cy = self.world.get_chunk_coords_from_world_pos(cam_x_f, cam_y_f)
        num_chunks_x = int(config.DIS_WIDTH / chunk_size_pixels) + 2
        num_chunks_y = int(config.DIS_HEIGHT / chunk_size_pixels) + 2
        
        for y in range(num_chunks_y):
            for x in range(num_chunks_x):
                chunk_to_draw_x = start_cx + x
                chunk_to_draw_y = start_cy + y
                chunk_surface = self.world.get_or_generate_chunk_surface(
                    chunk_to_draw_x, chunk_to_draw_y
                )
                world_px = chunk_to_draw_x * chunk_size_pixels
                world_py = chunk_to_draw_y * chunk_size_pixels
                screen_px = world_px - cam_x
                screen_py = world_py - cam_y
                self.screen.blit(chunk_surface, (screen_px, screen_py))

        # 2. Gambar Entitas
        snake_head_x, snake_head_y = self.snake.get_head_pos()
        
        for p in self.particles:
            p.draw(self.screen, cam_x, cam_y)

        if self.bomb_powerup:
            self.bomb_powerup.draw(self.screen, self.camera) 
            
        for f in self.foods:
            f.draw(self.screen, self.camera)
        
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
            self._draw_minimap(snake_head_x, snake_head_y)
        
        # 4. Update layar
        pygame.display.update()

# --- Titik Masuk Program ---
if __name__ == "__main__":
    game = Game()
    game.run()