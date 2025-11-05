import pygame
from . import config

def draw_score(surface, score):
    """Menampilkan skor di layar (koordinat layar tetap)."""
    value = config.SCORE_FONT.render("Skor Anda: " + str(score), True, config.YELLOW)
    surface.blit(value, [0, 0])

def draw_game_over_message(surface):
    """Menampilkan pesan di layar (koordinat layar tetap)."""
    msg = "Anda Kalah! 'C' untuk Main Lagi, 'Q' untuk Keluar"
    mesg = config.FONT_STYLE.render(msg, True, config.FOOD_COLOR)
    
    # Hitung posisi tengah
    text_rect = mesg.get_rect(center=(config.DIS_WIDTH / 2, config.DIS_HEIGHT / 2))
    surface.blit(mesg, text_rect)