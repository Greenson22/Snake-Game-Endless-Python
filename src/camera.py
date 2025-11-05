from . import config

class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.screen_width = config.DIS_WIDTH
        self.screen_height = config.DIS_HEIGHT
        
        # HAPUS world_width dan world_height
        # self.world_width = config.WORLD_WIDTH 
        # self.world_height = config.WORLD_HEIGHT

    def update(self, target_x, target_y):
        """Pusatkan kamera pada target (ular) dengan smoothing (Lerp)."""
        
        # 1. Tentukan posisi TARGET kamera
        target_cam_x = target_x - (self.screen_width / 2)
        target_cam_y = target_y - (self.screen_height / 2)
        
        # 2. Hitung posisi BARU kamera menggunakan Lerp
        lerp_factor = config.CAMERA_SMOOTHING
        self.x += (target_cam_x - self.x) * lerp_factor
        self.y += (target_cam_y - self.y) * lerp_factor

        # 3. HAPUS LOGIKA "JEPIT" (CLAMP)
        # self.x = max(0, self.x) 
        # self.y = max(0, self.y) 
        # self.x = min(self.x, self.world_width - self.screen_width) 
        # self.y = min(self.y, self.world_height - self.screen_height)

    def get_offset(self):
        """
        Mendapatkan offset kamera untuk rendering.
        """
        return (int(self.x), int(self.y))