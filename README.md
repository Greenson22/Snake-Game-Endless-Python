# 🐍 Game Ular: Evolusi Dunia

Ini bukan permainan ular biasa. Selamat datang di dunia *infinite* yang hidup, penuh dengan bioma, musuh yang cerdas, dan sistem progresi tanpa batas. Bertahan hidup, tumbuh, dan capai level "Prestise" tertinggi\!

## ✨ Fitur Utama

  * **🌍 Dunia Tanpa Batas:** Peta *procedural* yang dibuat menggunakan *Chunk System* dan Perlin Noise. Dunia akan disimpan dan dimuat secara otomatis (`world_save.dat`).
  * **🏞️ Bioma Dinamis:** Lebih dari 8 bioma unik (rumput, gurun, hutan, salju, batu, dll.) yang dihasilkan berdasarkan ketinggian, suhu, dan kelembapan.
  * **🐌 Fisika Terrain:** Setiap bioma memengaruhi kecepatan gerak Anda dan musuh\! (misal: lebih lambat di salju, lebih cepat di rumput).
  * **👾 2 Tipe Musuh AI:**
      * **Cacing (Merah):** AI *greedy* yang melacak dan memburu Anda.
      * **Rusher (Ungu):** AI cepat yang bergerak lurus dan jarang berbelok, menciptakan bahaya tak terduga.
  * **🌟 Sistem Prestise (Prestige):** Setelah mencapai panjang maksimal (**12 segmen**), ular Anda tidak berhenti tumbuh. Sebaliknya, ia mulai mendapatkan level "Prestise", mengubah warnanya segmen per segmen (Emas, Perak, Rubi, dan seterusnya\!).
  * **🍒 Makanan Berbasis Bioma:** Makanan yang berbeda *spawn* di bioma yang berbeda dengan probabilitas dan skor yang unik (misal: Kaktus di Gurun, Kristal di Batu).
  * **💣 Power-up Bom:** Ambil bom untuk meledakkan dan menghancurkan semua musuh dalam radius besar.
  * **📡 Radar Dinamis:** Minimap canggih yang menunjukkan medan, musuh, makanan, dan bom di sekitar Anda secara *real-time*.
  * **🎥 Kamera Halus:** Kamera dengan *smoothing* (Lerp) yang mengikuti pergerakan ular dengan mulus.
  * **📈 Leveling Progresif:** Naik level berdasarkan waktu. Setiap level meningkatkan kecepatan musuh dan jumlah mereka di dunia.

-----

## 🕹️ Cara Bermain

1.  **Mulai Permainan:** Jalankan `main.py`.
2.  **Bergerak:** Gunakan **Tombol Panah** (Atas, Bawah, Kiri, Kanan) untuk mengarahkan ular.
3.  **Tujuan Utama:**
      * Makan makanan (berbagai warna) untuk menambah skor dan menumbuhkan ular Anda.
      * Hindari menabrak **tubuh Anda sendiri**.
      * Hindari **semua musuh** (Merah dan Ungu).
4.  **Strategi Terrain:** Gunakan medan untuk keuntungan Anda. Berlari di rumput (cepat) untuk kabur, dan pancing musuh ke salju atau batu (lambat) untuk memperlambat mereka.
5.  **Game Over:** Jika Anda menabrak, layar "Game Over" akan muncul.
      * Tekan **'C'** untuk bermain lagi.
      * Tekan **'Q'** untuk keluar.

-----

## 🐍 Mekanika Ular: Pertumbuhan & Prestise

Sistem pertumbuhan ular ini unik dan memiliki dua fase:

### Fase 1: Pertumbuhan Normal (Tier 0 - Hijau)

  * Setiap makanan yang dimakan akan menambah skor dan panjang ular Anda.
  * Fase ini berlanjut hingga ular mencapai panjang maksimal (`SNAKE_MAX_LENGTH` = 12 segmen).

### Fase 2: Pertumbuhan Prestise (Tier 1+)

  * Setelah panjang ular maksimal, makanan yang Anda makan sekarang akan mengisi "Level Prestise".
  * Saat Level Prestise terisi, ular akan pindah ke **Tier 1 (Emas)**.
  * Segmen ular akan mulai berubah warna menjadi Emas, **satu per satu, dimulai dari kepala**.
  * Setelah semua 12 segmen menjadi Emas, ular akan naik ke **Tier 2 (Perak)**, dan prosesnya berulang.
  * Daftar Tier Prestise:
    1.  🥇 Emas
    2.  🥈 Perak
    3.  ❤️ Rubi (Merah)
    4.  💙 Safir (Biru)
    5.  💜 Amethyst (Ungu)
    6.  ... dan seterusnya\!

-----

## 🌍 Dunia & Bioma

Dunia dihasilkan secara tak terbatas menggunakan *chunks*. Setiap *tile* di dunia memiliki tipe bioma yang ditentukan oleh 3 nilai noise:

1.  **Elevasi (Ketinggian):** Menentukan Air, Daratan, dan Gunung.
2.  **Temperatur (Suhu):** Menentukan iklim Panas, Sedang, atau Dingin.
3.  **Moisture (Kelembapan):** Menentukan iklim Kering atau Basah.

Kombinasi ini menciptakan bioma seperti:

  * **Rumput:** Cepat, makanan (Apel) jarang.
  * **Hutan (Deep Grass):** Cepat, makanan (Berry) agak jarang.
  * **Gurun (Pasir):** Cepat, makanan (Kaktus) jarang.
  * **Tanah (Dirt):** Lambat, makanan (Jamur) sering.
  * **Batu (Stone):** Sangat Lambat, makanan (Kristal) selalu ada.
  * **Salju:** Sangat Lambat, makanan (Berry Es) selalu ada.
  * **Air:** Paling Lambat, tidak ada makanan.

-----

## 🔧 Konfigurasi (`src/config.py`)

Hampir semua aspek game dapat diubah melalui file `config.py`:

  * `DIS_WIDTH`, `DIS_HEIGHT`: Ukuran layar.
  * `SNAKE_BLOCK`, `CHUNK_SIZE`: Ukuran dasar dunia.
  * `SNAKE_SPEED`: Kecepatan *tick* game (FPS).
  * `SNAKE_MAX_LENGTH`: Batas panjang ular sebelum Prestise.
  * `SNAKE_PRESTIGE_COLORS`: Daftar warna untuk semua tier prestise.
  * `MAX_FOOD_COUNT`: Jumlah total makanan di dunia.
  * `BIOME_FOOD_RULES`: Mengatur probabilitas, skor, dan warna makanan per bioma.
  * `TERRAIN_SPEEDS`: Mengatur penalti kecepatan untuk setiap tipe medan.
  * `NUM_ENEMIES`, `NUM_RUSHERS`: Jumlah musuh awal.
  * `LEVEL_UP_TIME`: Waktu (detik) untuk naik level.
  * `BOMB_SPAWN_TIME`, `BOMB_RADIUS_AFFECTED`: Pengaturan power-up bom.
  * `MINIMAP_...`: Semua pengaturan untuk tampilan radar/minimap.

-----

## 📁 Struktur Proyek

```
src/
│
├── main.py         # Loop utama game, event handling, dan logika inti
├── config.py       # Semua variabel konfigurasi & pengaturan (WARNA, KECEPATAN, UKURAN)
│
├── snake.py        # Kelas Ular (Pemain), logika gerak, tumbuh, dan prestise
├── enemy.py        # Kelas Musuh Cacing (AI Greedy)
├── rusher.py       # Kelas Musuh Rusher (AI Lurus)
│
├── world.py        # Manajer Chunk, memuat & menyimpan dunia
├── terrain.py      # Logika generasi noise untuk bioma & terrain
│
├── food.py         # Kelas untuk objek makanan
├── bomb.py         # Kelas untuk objek power-up bom
├── particle.py     # Kelas untuk efek partikel (saat ular bergerak)
│
├── camera.py       # Kelas Kamera (Logika smoothing/follow)
├── ui.py           # Fungsi untuk menggambar Skor, Waktu, Level, & Game Over
│
└── (file kosong)
```