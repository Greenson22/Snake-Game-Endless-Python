from . import config

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.screen_width = config.DIS_WIDTH
        self.screen_height = config.DIS_HEIGHT
        self.world_width = config.WORLD_WIDTH
        self.world_height = config.WORLD_HEIGHT

    def update(self, target_x, target_y):
        """Pusatkan kamera pada target (ular) dan jepit ke batas dunia."""
        # 1. Pusatkan pada target
        self.x = target_x - (self.screen_width / 2)
        self.y = target_y - (self.screen_height / 2)
        
        # 2. "Jepit" (Clamp) kamera agar tidak keluar batas
        self.x = max(0, self.x) # Jangan terlalu ke kiri
        self.y = max(0, self.y) # Jangan terlalu ke atas
        self.x = min(self.x, self.world_width - self.screen_width) # Jangan terlalu ke kanan
        self.y = min(self.y, self.world_height - self.screen_height) # Jangan terlalu ke bawah

    def get_offset(self):
        """Mendapatkan offset kamera untuk rendering."""
        return (self.x, self.y)