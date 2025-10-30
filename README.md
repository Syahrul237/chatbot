# 💬 Chatbot Konsultan UMKM

Aplikasi **Chatbot Konsultan UMKM** adalah asisten virtual berbasis **Streamlit** yang membantu pelaku usaha mikro, kecil, dan menengah (UMKM) dalam memberikan saran bisnis sesuai profil usaha mereka.  
Ditenagai oleh model **Gemini AI (Google Generative AI)**, chatbot ini dapat memberikan rekomendasi, menjawab tantangan bisnis, serta menyimpan riwayat percakapan untuk setiap pengguna.

---

## 🚀 Fitur Utama

### 🗂️ 1. Profil Bisnis Interaktif
Pengguna dapat mengisi:
- Nama usaha  
- Bidang usaha (makanan/minuman, fashion, kerajinan, jasa, pertanian, dll.)  
- Lokasi usaha  
- Rata-rata omzet bulanan  
- Tantangan utama bisnis  

Profil ini digunakan untuk menyesuaikan jawaban chatbot agar lebih relevan dengan konteks usaha pengguna.

---

### 💬 2. Chatbot Konsultan Cerdas
- Dibangun menggunakan **Gemini 2.5 Flash** dari Google Generative AI.  
- Memberikan jawaban yang **singkat, alami, dan mudah dipahami**.  
- Menolak pertanyaan di luar konteks bisnis UMKM.  
- Menyimpan **riwayat percakapan** secara otomatis berdasarkan nama usaha.

---

### 💾 3. Penyimpanan Riwayat Konsultasi
- Riwayat percakapan dan profil usaha disimpan ke file JSON di folder `riwayat_bisnis/`.
- Saat pengguna kembali membuka aplikasi, riwayat chat dan data profil akan otomatis dimuat.

---

### 🌓 4. Mode Gelap & Terang
- Pengguna dapat mengaktifkan **mode gelap (dark mode)** untuk tampilan nyaman di malam hari.
- Warna latar dan gaya chat bubble akan menyesuaikan secara otomatis.

---

### 🔄 5. Fitur Manajemen Chat
- **💾 Simpan Profil:** Menyimpan profil dan riwayat konsultasi.
- **🔄 Hapus Riwayat Chat:** Menghapus semua riwayat dan memulai sesi baru.

---

## 🧰 Teknologi yang Digunakan

| Komponen | Deskripsi |
|-----------|------------|
| **Streamlit** | Framework utama untuk UI dan interaktivitas web |
| **Google Generative AI (Gemini 2.5 Flash)** | Model AI untuk memahami konteks dan menjawab pertanyaan |
| **dotenv** | Mengelola API key dari file `.env` |
| **JSON** | Format penyimpanan riwayat percakapan |
| **Python 3.12** | Bahasa pemrograman utama |

---

## ⚙️ Cara Menjalankan di Lokal
### 1. Install VS Code + Miniconda
### 2. Clone Repository
### 3. Create environment : conda create -n nama-environtment python=3.12
### 4. conda activate nama-environtment
### 5. jalankan stremlit dengan cara ketik di terminal streamlit run nama_file.py
```bash

git clone https://github.com/username/chatbot-umkm.git
cd chatbot-umkm
