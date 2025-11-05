import pygame
from . import config

def draw_score(surface, score):
    """Menampilkan skor di layar (koordinat layar tetap)."""
    value = config.SCORE_FONT.render("Skor: " + str(score), True, config.YELLOW)
    surface.blit(value, [10, 10]) # Beri sedikit padding

def draw_game_stats(surface, game_time, level):
    """Menampilkan Waktu dan Level di pojok kiri atas (di bawah Skor)."""
    
    # Format Waktu (MM:SS)
    minutes = game_time // 60
    seconds = game_time % 60
    time_str = f"Waktu: {minutes:02}:{seconds:02}"
    
    # Teks Level
    level_str = f"Level: {level}"
    
    # Render Teks
    time_text = config.STATS_FONT.render(time_str, True, config.WHITE)
    level_text = config.STATS_FONT.render(level_str, True, config.WHITE)
    
    # --- Posisi di KIRI ATAS ---
    # Dipindahkan agar tidak bertabrakan dengan minimap
    time_rect = time_text.get_rect(
        topleft=(10, 50)
    )
    level_rect = level_text.get_rect(
        topleft=(10, 50 + time_rect.height + 5)
    )
    # --------------------------
    
    surface.blit(time_text, time_rect)
    surface.blit(level_text, level_rect)


def draw_game_over_overlay(surface, score, level, game_time):
    """
    Menggambar overlay semi-transparan dan UI 'Game Over' di atas layar.
    """
    
    overlay = pygame.Surface(
        (config.DIS_WIDTH, config.DIS_HEIGHT), pygame.SRCALPHA
    )
    overlay.fill((0, 0, 0, 150)) 
    surface.blit(overlay, (0, 0)) 
    
    # 2. Gambar Teks "GAME OVER"
    # --- PERBAIKAN: Menggunakan FOOD_APPLE_COLOR (warna merah) ---
    title_text = config.TITLE_FONT.render("GAME OVER", True, config.FOOD_APPLE_COLOR)
    title_rect = title_text.get_rect(
        center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT / 4)
    )
    surface.blit(title_text, title_rect)
    
    # 3. Teks Statistik Akhir
    minutes = game_time // 60
    seconds = game_time % 60
    time_str = f"Bertahan: {minutes:02}:{seconds:02}"
    
    score_str = f"Skor Akhir: {score}"
    level_str = f"Level Tercapai: {level}"

    score_text = config.SCORE_FONT.render(score_str, True, config.WHITE)
    score_rect = score_text.get_rect(
        center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT / 2 - 20)
    )
    
    level_text = config.FONT_STYLE.render(level_str, True, config.WHITE)
    level_rect = level_text.get_rect(
        center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT / 2 + 30)
    )

    time_text = config.FONT_STYLE.render(time_str, True, config.WHITE)
    time_rect = time_text.get_rect(
        center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT / 2 + 60)
    )

    surface.blit(score_text, score_rect)
    surface.blit(level_text, level_rect)
    surface.blit(time_text, time_rect)
    
    # 4. Gambar Teks Instruksi
    instr_text = config.FONT_STYLE.render(
        "Tekan 'C' untuk Main Lagi  |  'Q' untuk Keluar", True, config.WHITE
    )
    instr_rect = instr_text.get_rect(
        center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT * 0.85)
    )
    surface.blit(instr_text, instr_rect)