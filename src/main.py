import pygame
import time
import random
import noise  # Membutuhkan 'pip install noise'

# Inisialisasi Pygame
pygame.init()

# --- BARU: Ukuran Dunia vs Ukuran Layar ---
# Ukuran layar (viewport)
dis_width = 800
dis_height = 600

# Ukuran total dunia game (misal: 3x lebih besar dari layar)
world_width = dis_width * 3
world_height = dis_height * 3
# ------------------------------------

# Definisi Warna
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
blue = (50, 153, 213)
snake_color = (0, 200, 0)
food_color = (213, 50, 80)
grass_color = (34, 139, 34)
dirt_color = (139, 69, 19)
sand_color = (244, 164, 96)
stone_color = (128, 128, 128)

# Membuat layar display (seukuran viewport)
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Game Ular (Snake) dengan Kamera')

clock = pygame.time.Clock()
snake_block = 20
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def create_terrain_background(width, height, block_size):
    """
    Membuat Surface background dengan terrain noise.
    Perhatikan: width dan height sekarang adalah ukuran DUNIA.
    """
    # Buat surface baru seukuran DUNIA
    background_surface = pygame.Surface((width, height))
    
    num_tiles_x = width // block_size
    num_tiles_y = height // block_size
    
    SCALE = 0.05 
    OCTAVES = 6
    PERSISTENCE = 0.5
    LACUNARITY = 2.0
    BASE = random.randint(0, 1000)
    
    print("Generating large terrain map...")
    
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            noise_val = noise.pnoise2(
                (x * SCALE) + BASE, 
                (y * SCALE) + BASE,
                octaves=OCTAVES,
                persistence=PERSISTENCE,
                lacunarity=LACUNARITY
            )
            
            if noise_val < -0.2:
                tile_color = stone_color
            elif noise_val < 0.1:
                tile_color = dirt_color
            elif noise_val < 0.5:
                tile_color = grass_color
            else:
                tile_color = sand_color
            
            px = x * block_size
            py = y * block_size
            pygame.draw.rect(background_surface, tile_color, [px, py, block_size, block_size])
            
    print("Terrain map generated.")
    return background_surface


def Your_score(score):
    """Menampilkan skor di layar (koordinat layar tetap)."""
    value = score_font.render("Skor Anda: " + str(score), True, yellow)
    # Digambar di [0, 0] layar, tidak terpengaruh kamera
    dis.blit(value, [0, 0])


# --- MODIFIKASI: Membutuhkan info kamera ---
def our_snake(snake_block, snake_list, camera_x, camera_y):
    """Menggambar ular relatif terhadap kamera."""
    for x in snake_list:
        # Posisi di layar = Posisi di dunia - Posisi kamera
        screen_x = x[0] - camera_x
        screen_y = x[1] - camera_y
        pygame.draw.rect(dis, snake_color, [screen_x, screen_y, snake_block, snake_block])


def message(msg, color):
    """Menampilkan pesan di layar (koordinat layar tetap)."""
    mesg = font_style.render(msg, True, color)
    # Digambar di tengah layar, tidak terpengaruh kamera
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    # --- BARU: Kamera dimulai dari 0, 0 ---
    camera_x, camera_y = 0, 0

    # --- MODIFIKASI: Mulai di tengah DUNIA ---
    x1 = world_width / 2
    y1 = world_height / 2
    x1_change = 0
    y1_change = 0
    
    snake_List = []
    Length_of_snake = 1

    # --- MODIFIKASI: Makanan spawn di dalam DUNIA ---
    foodx = round(random.randrange(0, world_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, world_height - snake_block) / 20.0) * 20.0

    # --- MODIFIKASI: Buat background seukuran DUNIA ---
    background_surface = create_terrain_background(world_width, world_height, snake_block)

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Anda Kalah! Tekan 'C' untuk Main Lagi atau 'Q' untuk Keluar", food_color)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # --- MODIFIKASI: Cek tabrakan dengan batas DUNIA ---
        if x1 >= world_width or x1 < 0 or y1 >= world_height or y1 < 0:
            game_close = True

        # Update posisi ular (koordinat dunia)
        x1 += x1_change
        y1 += y1_change

        # --- BARU: Logika Kamera ---
        # 1. Buat kamera berpusat pada ular
        camera_x = x1 - (dis_width / 2)
        camera_y = y1 - (dis_height / 2)
        
        # 2. "Jepit" (Clamp) kamera agar tidak keluar batas dunia
        # Jangan biarkan kamera bergerak terlalu ke kiri atau atas
        camera_x = max(0, camera_x)
        camera_y = max(0, camera_y)
        
        # Jangan biarkan kamera bergerak terlalu ke kanan atau bawah
        camera_x = min(camera_x, world_width - dis_width)
        camera_y = min(camera_y, world_height - dis_height)
        # ----------------------------

        # --- MODIFIKASI: Logika Menggambar ---
        # 1. Bersihkan layar (opsional, tapi baik untuk jaga-jaga)
        dis.fill(black)
        
        # 2. Gambar background terrain, digeser oleh kamera
        dis.blit(background_surface, (0 - camera_x, 0 - camera_y))
        
        # 3. Gambar makanan, digeser oleh kamera
        pygame.draw.rect(dis, food_color, [foodx - camera_x, foody - camera_y, snake_block, snake_block])
        
        # Logika tubuh ular (masih dalam koordinat dunia)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 4. Gambar ular, digeser oleh kamera (via fungsi)
        our_snake(snake_block, snake_List, camera_x, camera_y)
        
        # 5. Gambar UI (Skor) - TIDAK digeser kamera
        Your_score(Length_of_snake - 1)

        # 6. Update tampilan
        pygame.display.update()

        # Cek makan makanan (logika dunia)
        if x1 == foodx and y1 == foody:
            # --- MODIFIKASI: Spawn di dalam DUNIA ---
            foodx = round(random.randrange(0, world_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, world_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


# Memulai game
gameLoop()