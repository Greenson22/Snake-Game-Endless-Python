import pygame
import time
import random
import noise  # <-- BARU: Impor library noise

# Inisialisasi Pygame
pygame.init()

# Definisi Warna
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
blue = (50, 153, 213)

# Warna Game
snake_color = (0, 200, 0)   # Warna ular (hijau cerah)
food_color = (213, 50, 80)    # Warna makanan (merah)

# Warna Terrain untuk Background
grass_color = (34, 139, 34)   # Hijau tua
dirt_color = (139, 69, 19)    # Coklat
sand_color = (244, 164, 96)   # Coklat muda (pasir)
stone_color = (128, 128, 128) # Abu-abu

# Ukuran layar
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Game Ular (Snake) dengan Terrain Noise')

clock = pygame.time.Clock()
snake_block = 20
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


# --- MODIFIKASI: Fungsi background diubah total ---
def create_terrain_background(width, height, block_size):
    """
    Membuat satu Surface background dengan terrain acak
    menggunakan Perlin Noise untuk pola yang alami.
    """
    background_surface = pygame.Surface((width, height))
    
    num_tiles_x = width // block_size
    num_tiles_y = height // block_size
    
    # --- Kontrol Parameter Noise ---
    
    # SCALE: Mengontrol "zoom" dari noise. 
    # Nilai lebih kecil = pulau lebih besar. 
    # Nilai lebih besar = medan lebih acak/kecil.
    SCALE = 0.05 
    
    # OCTAVES: Jumlah lapisan noise yang digabungkan.
    # Lebih banyak oktaf = lebih detail (tapi lebih lambat).
    OCTAVES = 6
    
    # PERSISTENCE: Seberapa besar pengaruh oktaf detail.
    PERSISTENCE = 0.5
    
    # LACUNARITY: Seberapa cepat detail meningkat di tiap oktaf.
    LACUNARITY = 2.0
    
    # BASE: Seed acak agar peta berbeda setiap kali dimainkan
    BASE = random.randint(0, 1000)
    
    print("Generating terrain map...")
    
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            
            # Hitung nilai noise untuk koordinat (x, y) ini
            # Kita gunakan koordinat tile (x, y) dikalikan SCALE
            noise_val = noise.pnoise2(
                (x * SCALE) + BASE, 
                (y * SCALE) + BASE,
                octaves=OCTAVES,
                persistence=PERSISTENCE,
                lacunarity=LACUNARITY
            )
            # Nilai noise_val akan berada antara -1.0 dan 1.0
            
            # Tetapkan warna berdasarkan nilai noise (seperti "ketinggian")
            # Anda bisa mengubah ambang batas ini sesuai selera
            if noise_val < -0.2:
                tile_color = stone_color  # "Pegunungan" tinggi/batu
            elif noise_val < 0.1:
                tile_color = dirt_color   # "Tanah"
            elif noise_val < 0.5:
                tile_color = grass_color  # "Dataran" rumput
            else:
                tile_color = sand_color   # "Pantai"
            
            px = x * block_size
            py = y * block_size
            pygame.draw.rect(background_surface, tile_color, [px, py, block_size, block_size])
            
    print("Terrain map generated.")
    return background_surface
# ---------------------------------------------------


def Your_score(score):
    value = score_font.render("Skor Anda: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

    # Panggil fungsi background BARU
    background_surface = create_terrain_background(dis_width, dis_height, snake_block)

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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        # Gambar background terrain yang sudah jadi
        dis.blit(background_surface, (0, 0))
        
        # Gambar makanan
        pygame.draw.rect(dis, food_color, [foodx, foody, snake_block, snake_block])
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


# Memulai game
gameLoop()