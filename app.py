import streamlit as st
import sys
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import datetime
import pyttsx3


# === Konfigurasi dasar ===
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="Chatbot Konsultan UMKM",
    page_icon="💬",
    layout="wide"
)

# === Fungsi bantu ===
def get_user_filename():
    """Buat nama file unik untuk menyimpan riwayat berdasarkan nama usaha"""
    folder = "riwayat_bisnis"
    os.makedirs(folder, exist_ok=True)
    nama_file = st.session_state.nama_usaha.replace(" ", "_").lower()
    return os.path.join(folder, f"{nama_file}.json")

def save_chat_history():
    """Simpan profil dan riwayat chat ke file JSON"""
    data = {
        "timestamp": str(datetime.datetime.now()),
        "messages": st.session_state.messages,
        "profile": {
            "nama": st.session_state.nama_usaha,
            "bidang": st.session_state.bidang_usaha,
            "lokasi": st.session_state.lokasi_usaha,
            "omzet": st.session_state.omzet_usaha,
            "tantangan": st.session_state.tantangan,
        },
    }
    with open(get_user_filename(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_chat_history():
    """Muat riwayat chat dan profil jika file sudah ada"""
    try:
        with open(get_user_filename(), "r", encoding="utf-8") as f:
            data = json.load(f)
            st.session_state.messages = data.get("messages", [])
            profile = data.get("profile", {})
            st.session_state.nama_usaha = profile.get("nama", "")
            st.session_state.bidang_usaha = profile.get("bidang", "")
            st.session_state.lokasi_usaha = profile.get("lokasi", "")
            st.session_state.omzet_usaha = profile.get("omzet", "")
            st.session_state.tantangan = profile.get("tantangan", "")
    except FileNotFoundError:
        pass

# === Sidebar Profil Bisnis ===
st.sidebar.title("🗂️ Profil Usaha Anda")
st.sidebar.markdown("Isi profil bisnis agar saran lebih relevan:")

st.session_state.nama_usaha = st.sidebar.text_input(
    "Nama Usaha", 
    value=st.session_state.get("nama_usaha", "Belum diisi")
)
st.session_state.bidang_usaha = st.sidebar.selectbox(
    "Bidang Usaha",
    ["Makanan/Minuman", "Fashion", "Kerajinan", "Jasa", "Pertanian", "Lainnya"],
    index=0
)
st.session_state.lokasi_usaha = st.sidebar.text_input(
    "Lokasi Usaha", 
    value=st.session_state.get("lokasi_usaha", "Belum diisi")
)
st.session_state.omzet_usaha = st.sidebar.text_input(
    "Rata-rata Omzet (per bulan)", 
    value=st.session_state.get("omzet_usaha", "Belum diisi")
)
st.session_state.tantangan = st.sidebar.text_area(
    "Tantangan utama bisnis Anda", 
    value=st.session_state.get("tantangan", "Belum diisi")
)

if st.sidebar.button("💾 Simpan Profil"):
    save_chat_history()
    st.sidebar.success("Profil dan riwayat chat berhasil disimpan!")

# === Tema Gelap/Terang ===
dark_mode = st.sidebar.toggle("🌙 Aktifkan Mode Gelap")
if dark_mode:
    bg = "#1e1e1e"
    txt = "#f1f1f1"
    user_bubble = "#3b82f6"
    bot_bubble = "#2b2b2b"
else:
    bg = "#f8f9fa"
    txt = "#2f2f2f"
    user_bubble = "#d1e7ff"
    bot_bubble = "#ffffff"

st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg};
            color: {txt};
            font-family: 'Segoe UI', sans-serif;
        }}
        .chat-bubble-user {{
            background-color: {user_bubble};
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            color: white;
        }}
        .chat-bubble-bot {{
            background-color: {bot_bubble};
            border: 1px solid #ccc;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            color: {txt};
        }}
    </style>
""", unsafe_allow_html=True)
st.sidebar.markdown("Create By: Moch Syahrul Masaid")
# === Header ===
st.markdown(f"""
<div style='text-align:center'>
    <h1>💬 Chatbot Konsultan UMKM</h1>
    <p style='color:{txt}; font-size:1.1em;'>Asisten cerdas untuk bantu kelola dan kembangkan usaha Anda.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# === Inisialisasi State ===
if "messages" not in st.session_state:
    load_chat_history()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya siap bantu konsultasi bisnis kamu. Ada tantangan apa hari ini?"}
    ]
if "known_answers" not in st.session_state:
    st.session_state.known_answers = {}

# === Tampilkan Riwayat Chat ===
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# === Input Chat ===
if prompt := st.chat_input("Tulis pertanyaanmu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='chat-bubble-user'>👤 {prompt}</div>", unsafe_allow_html=True)

    normalized = prompt.strip().lower()
    if normalized in st.session_state.known_answers:
        bot_reply = st.session_state.known_answers[normalized]
    else:
        context = (
            f"Kamu adalah konsultan bisnis UMKM di Indonesia. "
            f"Gunakan profil pengguna berikut: "
            f"Nama Usaha: {st.session_state.nama_usaha}, "
            f"Bidang: {st.session_state.bidang_usaha}, "
            f"Lokasi: {st.session_state.lokasi_usaha}, "
            f"Omzet: {st.session_state.omzet_usaha}, "
            f"Tantangan: {st.session_state.tantangan}. "
            "Jawaban harus singkat, natural, dan mudah dipahami. "
            "Hindari bahasa terlalu formal atau paragraf panjang. "
            "Jika pertanyaan tidak relevan dengan UMKM, jawab: "
            "'Maaf, saya hanya bisa membantu seputar konsultasi bisnis UMKM.'"
        )
        response = model.generate_content(f"{context}\n\nPertanyaan: {prompt}")
        bot_reply = response.text.strip()
        st.session_state.known_answers[normalized] = bot_reply

    # Tampilkan jawaban bot
    st.markdown(f"<div class='chat-bubble-bot'>🤖 {bot_reply}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    save_chat_history()

# === Tombol Reset ===
if st.button("🔄 Hapus Riwayat Chat"):
    st.session_state.messages = []
    st.session_state.known_answers = {}
    save_chat_history()
    st.success("Riwayat chat berhasil dihapus.")
    st.rerun()

# Debug info
st.write("Python version:", sys.version)
st.write("Installed packages:")
subprocess.run(["pip", "list"])
