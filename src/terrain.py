# src/terrain.py
import pygame
import noise
import random
from . import config 

# --- PENGATURAN NOISE (tetap) ---
SCALE = 0.05 
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0
BASE = random.randint(0, 1000)

def generate_chunk_data_and_surface(cx, cy):
    """
    Membuat data terrain DAN surface untuk SATU chunk.
    cx, cy = koordinat chunk (misal: 0, 1)
    """
    
    # Buat grid data lokal untuk chunk ini
    terrain_data = {}
    
    # Buat surface lokal untuk chunk ini
    chunk_surface = pygame.Surface(
        (config.CHUNK_SIZE * config.SNAKE_BLOCK, 
         config.CHUNK_SIZE * config.SNAKE_BLOCK)
    )
    
    # Hitung offset pixel dunia dari chunk ini
    world_offset_x = cx * config.CHUNK_SIZE
    world_offset_y = cy * config.CHUNK_SIZE
    
    for y in range(config.CHUNK_SIZE):
        for x in range(config.CHUNK_SIZE):
            
            # --- PENTING: Hitung koordinat GLOBAL ---
            # Ini memastikan noise-nya nyambung antar chunk
            global_x = world_offset_x + x
            global_y = world_offset_y + y
            
            # Ambil nilai noise Pnoise
            noise_val = noise.pnoise2(
                (global_x * SCALE) + BASE, 
                (global_y * SCALE) + BASE,
                octaves=OCTAVES,
                persistence=PERSISTENCE,
                lacunarity=LACUNARITY
            )
            
            # Logika pewarnaan (sama seperti sebelumnya)
            if noise_val < -0.5:
                tile_color = config.WATER_COLOR
                tile_type = config.T_WATER
            elif noise_val < -0.3:
                tile_color = config.STONE_COLOR
                tile_type = config.T_STONE
            elif noise_val < -0.0:
                tile_color = config.DIRT_COLOR
                tile_type = config.T_DIRT
            elif noise_val < 0.6:
                tile_color = config.GRASS_COLOR
                tile_type = config.T_GRASS
            else:
                tile_color = config.SAND_COLOR
                tile_type = config.T_SAND
            
            # 1. Simpan tipe data ke grid LOKAL
            terrain_data[(x, y)] = tile_type
            
            # 2. Gambar ke surface LOKAL
            px = x * config.SNAKE_BLOCK
            py = y * config.SNAKE_BLOCK
            pygame.draw.rect(chunk_surface, tile_color, [px, py, config.SNAKE_BLOCK, config.SNAKE_BLOCK])
            
    # Kembalikan KEDUA-nya
    return terrain_data, chunk_surface

def render_chunk_surface_from_data(chunk_data):
    """
    Membuat ulang Surface chunk dari data (misal: setelah load game).
    """
    chunk_surface = pygame.Surface(
        (config.CHUNK_SIZE * config.SNAKE_BLOCK, 
         config.CHUNK_SIZE * config.SNAKE_BLOCK)
    )
    
    # Gunakan mapping warna dari config
    color_map = {
        config.T_WATER: config.WATER_COLOR,
        config.T_STONE: config.STONE_COLOR,
        config.T_DIRT: config.DIRT_COLOR,
        config.T_GRASS: config.GRASS_COLOR,
        config.T_SAND: config.SAND_COLOR,
    }
    default_color = config.GRASS_COLOR
    
    for y in range(config.CHUNK_SIZE):
        for x in range(config.CHUNK_SIZE):
            
            tile_type = chunk_data.get((x,y), config.T_GRASS)
            tile_color = color_map.get(tile_type, default_color)
            
            px = x * config.SNAKE_BLOCK
            py = y * config.SNAKE_BLOCK
            pygame.draw.rect(chunk_surface, tile_color, [px, py, config.SNAKE_BLOCK, config.SNAKE_BLOCK])
            
    return chunk_surface