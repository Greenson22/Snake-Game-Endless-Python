import pygame
import noise
import random
# Menggunakan impor relatif dari dalam paket 'src'
from . import config 

def create_terrain_background(width, height, block_size):
    """
    Membuat Surface background DAN data grid terrain.
    """
    background_surface = pygame.Surface((width, height))
    
    # Simpan data grid di sini
    terrain_grid = {}
    
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
            
            # --- MODIFIKASI: Menambahkan rentang untuk Air ---
            # Air akan ada di dataran terendah (nilai noise terendah)
            
            if noise_val < -0.5:  # Paling rendah: Air
                tile_color = config.WATER_COLOR
                tile_type = config.T_WATER
            elif noise_val < -0.3: # Sedikit lebih tinggi: Stone
                tile_color = config.STONE_COLOR
                tile_type = config.T_STONE
            elif noise_val < -0.0: # Transisi: Dirt
                tile_color = config.DIRT_COLOR
                tile_type = config.T_DIRT
            elif noise_val < 0.6:  # Dominan: Rumput
                tile_color = config.GRASS_COLOR
                tile_type = config.T_GRASS
            else: # Dataran tinggi: Pasir
                tile_color = config.SAND_COLOR
                tile_type = config.T_SAND
            # -------------------------------------------------
            
            # Simpan tipe data ke grid
            terrain_grid[(x, y)] = tile_type
            
            # Gambar ke surface
            px = x * block_size
            py = y * block_size
            pygame.draw.rect(background_surface, tile_color, [px, py, block_size, block_size])
            
    print("Terrain map generated.")
    
    # Kembalikan KEDUA-nya
    return background_surface, terrain_grid