import pygame
from . import config

def draw_score(surface, score):
    """Menampilkan skor di layar (koordinat layar tetap)."""
    value = config.SCORE_FONT.render("Skor Anda: " + str(score), True, config.YELLOW)
    surface.blit(value, [0, 0])


def draw_game_over_overlay(surface, score):
    """
    Menggambar overlay semi-transparan dan UI 'Game Over' di atas layar.
    """
    
    # 1. Buat surface overlay semi-transparan
    # pygame.SRCALPHA memungkinkan transparansi
    overlay = pygame.Surface(
        (config.DIS_WIDTH, config.DIS_HEIGHT), pygame.SRCALPHA
    )
    # Isi dengan warna hitam (R, G, B) dan Alpha (transparansi) 150
    # 0 = transparan penuh, 255 = solid
    overlay.fill((0, 0, 0, 150)) 
    surface.blit(overlay, (0, 0)) # Gambar overlay di atas layar
    
    # 2. Gambar Teks "GAME OVER"
    title_text = config.TITLE_FONT.render("GAME OVER", True, config.FOOD_COLOR)
    title_rect = title_text.get_rect(
        center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT / 3)
    )
    surface.blit(title_text, title_rect)
    
    # 3. Gambar Teks "Skor Akhir"
    score_text = config.SCORE_FONT.render(f"Skor Akhir: {score}", True, config.WHITE)
    score_rect = score_text.get_rect(
        center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT / 2)
    )
    surface.blit(score_text, score_rect)
    
    # 4. Gambar Teks Instruksi
    instr_text = config.FONT_STYLE.render(
        "Tekan 'C' untuk Main Lagi  |  'Q' untuk Keluar", True, config.WHITE
    )
    instr_rect = instr_text.get_rect(
        center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT * 0.75)
    )
    surface.blit(instr_text, instr_rect)