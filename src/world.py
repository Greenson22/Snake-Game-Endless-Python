# src/world.py
import pygame
import pickle  # Untuk menyimpan/memuat data dunia
import os
from . import config
from . import terrain

class ChunkManager:
    def __init__(self):
        self.chunk_size_pixels = config.SNAKE_BLOCK * config.CHUNK_SIZE
        
        # { (cx, cy): terrain_grid }
        # Ini adalah "data" dunia kita, hanya berisi tipe terrain
        self.chunk_data = {}
        
        # { (cx, cy): Surface }
        # Ini adalah "cache" untuk gambar/surface yang sudah di-render
        self.chunk_surfaces = {}

        # Nama file untuk menyimpan progres
        self.save_file = "world_save.dat"
        self.load_world() # Coba muat dunia yang ada saat start

    def get_chunk_coords_from_world_pos(self, world_x, world_y):
        """Konversi koordinat dunia (pixel) ke koordinat chunk."""
        cx = int(world_x // self.chunk_size_pixels)
        cy = int(world_y // self.chunk_size_pixels)
        return (cx, cy)

    def get_chunk_coords_from_tile_pos(self, grid_x, grid_y):
        """Konversi koordinat grid (tile) ke koordinat chunk."""
        cx = int(grid_x // config.CHUNK_SIZE)
        cy = int(grid_y // config.CHUNK_SIZE)
        return (cx, cy)

    def get_or_generate_chunk_surface(self, cx, cy):
        """
        Fungsi inti: Mendapatkan Surface chunk. Jika tidak ada di cache,
        buat (generate) atau muat dari data.
        """
        # 1. Cek di cache rendering (paling cepat)
        if (cx, cy) in self.chunk_surfaces:
            return self.chunk_surfaces[(cx, cy)]
            
        # 2. Cek apakah datanya ada (jika sudah di-generate tapi belum di-cache)
        if (cx, cy) not in self.chunk_data:
            # 3. Jika tidak ada, panggil terrain generator untuk membuatnya
            print(f"Generating new chunk: {(cx, cy)}")
            new_data, new_surface = terrain.generate_chunk_data_and_surface(cx, cy)
            
            # Simpan datanya
            self.chunk_data[(cx, cy)] = new_data
            # Simpan surfacenya di cache
            self.chunk_surfaces[(cx, cy)] = new_surface
            
            return new_surface
        
        # 4. Jika data ada tapi surface tidak (misal setelah load game)
        # Kita perlu me-render ulang surface dari data
        print(f"Re-rendering chunk from data: {(cx, cy)}")
        chunk_data = self.chunk_data[(cx, cy)]
        new_surface = terrain.render_chunk_surface_from_data(chunk_data)
        self.chunk_surfaces[(cx, cy)] = new_surface # Simpan ke cache
        return new_surface

    def get_tile_type_at_world_pos(self, world_x, world_y):
        """Mendapatkan tipe terrain (rumput, air) di koordinat pixel dunia."""
        
        # Konversi ke koordinat tile (grid)
        grid_x = int(world_x // config.SNAKE_BLOCK)
        grid_y = int(world_y // config.SNAKE_BLOCK)
        
        # Cari chunk mana
        cx, cy = self.get_chunk_coords_from_tile_pos(grid_x, grid_y)
        
        # Pastikan data chunk ada
        if (cx, cy) not in self.chunk_data:
            # Jika kita menanyakan tile di chunk yang belum dibuat,
            # kita harus membuatnya sekarang juga.
            self.get_or_generate_chunk_surface(cx, cy)
            
        # Hitung koordinat tile LOKAL di dalam chunk
        local_x = grid_x % config.CHUNK_SIZE
        local_y = grid_y % config.CHUNK_SIZE
        
        # Ambil data dari chunk
        chunk_data = self.chunk_data[(cx, cy)]
        
        # Beri nilai default T_GRASS jika (entah bagaimana) gagal
        return chunk_data.get((local_x, local_y), config.T_GRASS)

    def save_world(self):
        """Menyimpan SEMUA data chunk (bukan surface) ke file."""
        print(f"Saving world ({len(self.chunk_data)} chunks) to {self.save_file}...")
        try:
            with open(self.save_file, "wb") as f:
                pickle.dump(self.chunk_data, f)
            print("World saved.")
        except Exception as e:
            print(f"Error saving world: {e}")

    def load_world(self):
        """Memuat data chunk dari file saat game dimulai."""
        if not os.path.exists(self.save_file):
            print("No save file found. Starting new world.")
            return

        try:
            with open(self.save_file, "rb") as f:
                self.chunk_data = pickle.load(f)
            print(f"World loaded: {len(self.chunk_data)} chunks found.")
        except Exception as e:
            print(f"Error loading world: {e}")