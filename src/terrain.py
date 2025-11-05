# src/terrain.py
import pygame
import noise
import random
from . import config 

# --- PENGATURAN NOISE (DIHAPUS DARI SINI, PINDAH KE CONFIG) ---

def _get_biome_tile(elevation, temperature, moisture):
    """
    Fungsi helper baru untuk menentukan tipe tile dan warna
    berdasarkan 3 nilai noise.
    (Nilai noise berkisar -1.0 s.d 1.0)
    
    --- VERSI DIPERBARUI UNTUK KESEIMBANGAN BIOMA ---
    """
    
    # 1. Cek Ketinggian (Air dan Puncak Gunung)
    if elevation < -0.5:
        return config.T_WATER, config.WATER_COLOR
    if elevation > 0.7:
        # Puncak gunung tinggi selalu salju, tidak peduli suhu
        return config.T_SNOW, config.SNOW_COLOR 

    # 2. Logika Bioma Utama (Iklim)
    
    # --- BIOMA DINGIN (Suhu < -0.2) ---
    # Rentang sedikit diperluas dari -0.3
    if temperature < -0.2: 
        if moisture < 0.0:
            return config.T_STONE, config.STONE_COLOR # Dingin + Kering = Batu Tundra
        else:
            return config.T_SNOW, config.SNOW_COLOR # Dingin + Basah = Salju

    # --- BIOMA PANAS (Suhu > 0.3) ---
    # Rentang sedikit diperluas dari 0.4
    elif temperature > 0.3: 
        if moisture < -0.3:
            return config.T_SAND, config.SAND_COLOR # Panas + Sangat Kering = Gurun
        elif moisture < 0.3:
            return config.T_DIRT, config.DIRT_COLOR # Panas + Sedang = Savana (Tanah)
        else:
            return config.T_DEEP_GRASS, config.DEEP_GRASS_COLOR # Panas + Basah = Hutan Hujan
            
    # --- BIOMA SEDANG (Suhu antara -0.2 dan 0.3) ---
    else:
        # Ini adalah bioma "Temperate"
        if moisture < -0.3:
            return config.T_DIRT, config.DIRT_COLOR # Sedang + Kering = Tanah
        elif moisture > 0.6:
            # Jika sedang tapi sangat basah, buat jadi hutan/rumput lebat
            return config.T_DEEP_GRASS, config.DEEP_GRASS_COLOR 
        else:
            # HANYA jika sedang DAN kelembapan sedang, baru jadi rumput
            # (Range moisture -0.3 s.d 0.6)
            return config.T_GRASS, config.GRASS_COLOR


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
    
    # Ambil pengaturan noise dari config
    octaves = config.ELEVATION_OCTAVES
    persistence = config.ELEVATION_PERSISTENCE
    lacunarity = config.ELEVATION_LACUNARITY
    
    for y in range(config.CHUNK_SIZE):
        for x in range(config.CHUNK_SIZE):
            
            # --- PENTING: Hitung koordinat GLOBAL ---
            global_x = world_offset_x + x
            global_y = world_offset_y + y
            
            # 1. Ambil nilai noise ELEVASI (Ketinggian)
            elevation_val = noise.pnoise2(
                (global_x * config.ELEVATION_SCALE) + config.ELEVATION_BASE, 
                (global_y * config.ELEVATION_SCALE) + config.ELEVATION_BASE,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity
            )
            
            # 2. Ambil nilai noise SUHU (Temperature)
            temperature_val = noise.pnoise2(
                (global_x * config.TEMP_SCALE) + config.TEMP_BASE, 
                (global_y * config.TEMP_SCALE) + config.TEMP_BASE,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity
            )
            
            # 3. Ambil nilai noise KELEMBAPAN (Moisture)
            moisture_val = noise.pnoise2(
                (global_x * config.MOISTURE_SCALE) + config.MOISTURE_BASE, 
                (global_y * config.MOISTURE_SCALE) + config.MOISTURE_BASE,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity
            )
            
            # 4. Tentukan Tipe Tile berdasarkan 3 Nilai
            tile_type, tile_color = _get_biome_tile(
                elevation_val, temperature_val, moisture_val
            )
            
            # 5. Simpan tipe data ke grid LOKAL
            terrain_data[(x, y)] = tile_type
            
            # 6. Gambar ke surface LOKAL
            px = x * config.SNAKE_BLOCK
            py = y * config.SNAKE_BLOCK
            pygame.draw.rect(chunk_surface, tile_color, [px, py, config.SNAKE_BLOCK, config.SNAKE_BLOCK])
            
    # Kembalikan KEDUA-nya
    return terrain_data, chunk_surface

def render_chunk_surface_from_data(chunk_data):
    """
    Membuat ulang Surface chunk dari data (misal: setelah load game).
    (Diperbarui untuk menyertakan tile baru)
    """
    chunk_surface = pygame.Surface(
        (config.CHUNK_SIZE * config.SNAKE_BLOCK, 
         config.CHUNK_SIZE * config.SNAKE_BLOCK)
    )
    
    # Gunakan mapping warna dari config
    # (Kita ambil dari TERRAIN_PARTICLE_COLORS agar konsisten)
    color_map = config.TERRAIN_PARTICLE_COLORS
    default_color = config.GRASS_COLOR
    
    for y in range(config.CHUNK_SIZE):
        for x in range(config.CHUNK_SIZE):
            
            tile_type = chunk_data.get((x,y), config.T_GRASS)
            
            # Ambil warna dari color_map (yang sekarang identik dengan particle_colors)
            tile_color = color_map.get(tile_type, default_color)
            
            px = x * config.SNAKE_BLOCK
            py = y * config.SNAKE_BLOCK
            pygame.draw.rect(chunk_surface, tile_color, [px, py, config.SNAKE_BLOCK, config.SNAKE_BLOCK])
            
    return chunk_surface