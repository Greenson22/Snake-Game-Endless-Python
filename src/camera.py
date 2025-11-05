from . import config

class Camera:
    def __init__(self):
        # --- MODIFIKASI: Ubah ke float (desimal) ---
        self.x = 0.0
        self.y = 0.0
        # ----------------------------------------
        self.screen_width = config.DIS_WIDTH
        self.screen_height = config.DIS_HEIGHT
        self.world_width = config.WORLD_WIDTH
        self.world_height = config.WORLD_HEIGHT

    # --- MODIFIKASI: Logika update diubah total ---
    def update(self, target_x, target_y):
        """Pusatkan kamera pada target (ular) dengan smoothing (Lerp)."""
        
        # 1. Tentukan posisi TARGET kamera (di mana kamera INGIN berada)
        target_cam_x = target_x - (self.screen_width / 2)
        target_cam_y = target_y - (self.screen_height / 2)
        
        # 2. Hitung posisi BARU kamera menggunakan Lerp (Linear Interpolation)
        #    Rumus: pos_baru = pos_lama + (target - pos_lama) * faktor_smoothing
        lerp_factor = config.CAMERA_SMOOTHING
        self.x += (target_cam_x - self.x) * lerp_factor
        self.y += (target_cam_y - self.y) * lerp_factor

        # 3. "Jepit" (Clamp) kamera agar tidak keluar batas dunia
        self.x = max(0, self.x) # Jangan terlalu ke kiri
        self.y = max(0, self.y) # Jangan terlalu ke atas
        self.x = min(self.x, self.world_width - self.screen_width) # Jangan terlalu ke kanan
        self.y = min(self.y, self.world_height - self.screen_height) # Jangan terlalu ke bawah
    # --------------------------------------------

    # --- MODIFIKASI: Ubah ke int saat rendering ---
    def get_offset(self):
        """
        Mendapatkan offset kamera untuk rendering.
        Kita bulatkan ke integer HANYA saat akan menggambar.
        """
        return (int(self.x), int(self.y))
    # --------------------------------------------