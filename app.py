import streamlit as st
import sys
import os
from dotenv import load_dotenv
from utils.ai_client import query_gemma
from utils.loader import load_materi
from utils.network_utils import check_internet_connection

# Load variabel lingkungan
load_dotenv()

# create tables
create_tables()
# Coba impor db_manager hanya jika psycopg2 terinstal dan ada koneksi
try:
    from utils.db_manager import create_new_chat, get_all_chats, get_chat_messages, add_message, create_tables
    DB_ENABLED = True
except ImportError:
    DB_ENABLED = False
    st.warning("Peringatan: `psycopg2-binary` tidak ditemukan atau ada masalah impor. Fitur riwayat chat tidak akan aktif.")
except Exception as e:
    DB_ENABLED = False
    st.warning(f"Peringatan: Gagal memuat fitur database. Fitur riwayat chat tidak akan aktif. Error: {e}")


# UI
st.set_page_config(page_title="EduLite", page_icon="📚", layout="centered")

st.image("assets/logo.png", width=120)
st.title("EduLite: Pembelajaran Cerdas dan Offline")
st.caption("Ditenagai oleh Gemma - Dirancang untuk semua kondisi koneksi.")

# Deteksi status koneksi internet
has_internet = check_internet_connection()

if has_internet and DB_ENABLED:
    st.success("✅ Aplikasi berjalan dalam mode ONLINE. Fitur riwayat obrolan tersedia.")
    # Inisialisasi tabel database saat aplikasi dimulai dan ada koneksi
    if 'db_tables_created' not in st.session_state:
        st.session_state.db_tables_created = create_tables()
        if not st.session_state.db_tables_created:
            st.error("Gagal terhubung ke database. Fitur riwayat obrolan dinonaktifkan.")
            DB_ENABLED = False # Nonaktifkan DB jika gagal inisialisasi
else:
    st.info("🌐 Aplikasi berjalan dalam mode OFFLINE. Fitur riwayat obrolan tidak tersedia.")
    DB_ENABLED = False # Pastikan DB_ENABLED False jika tidak ada internet atau gagal impor

# Load materi
materi = load_materi("data/materi/materi_kelas1.json") # Pastikan path sesuai dengan struktur README.md

# Sidebar untuk manajemen chat
st.sidebar.header("Manajemen Obrolan")

# Pilihan topik untuk obrolan baru
new_chat_topic = st.sidebar.selectbox("Pilih topik pelajaran:", list(materi.keys())) # Pindahkan ke sini agar selalu tersedia

if st.sidebar.button("Mulai Obrolan Baru"):
    if has_internet and DB_ENABLED:
        new_chat_id = create_new_chat(new_chat_topic)
        if new_chat_id:
            st.session_state.current_chat_id = new_chat_id
            st.session_state.messages = [] # Reset pesan untuk obrolan baru
            st.session_state.current_topic = new_chat_topic
            st.sidebar.success(f"Obrolan baru dimulai (ID: {new_chat_id})")
        else:
            st.sidebar.error("Gagal memulai obrolan baru dan menyimpan ke database.")
    else:
        st.session_state.current_chat_id = None # Tidak ada ID chat yang disimpan
        st.session_state.messages = [] # Reset pesan untuk obrolan baru
        st.session_state.current_topic = new_chat_topic
        st.sidebar.info("Obrolan baru dimulai dalam mode OFFLINE. Riwayat tidak akan disimpan.")


st.sidebar.markdown("---")
st.sidebar.subheader("Riwayat Obrolan")

if has_internet and DB_ENABLED:
    existing_chats = get_all_chats()

    if existing_chats:
        chat_options = {f"ID: {chat[0]} - {chat[2]} ({chat[1].strftime('%Y-%m-%d %H:%M')})": chat[0] for chat in existing_chats}
        selected_chat_display = st.sidebar.selectbox("Lanjutkan obrolan yang sudah ada:", ["Pilih Obrolan"] + list(chat_options.keys()))

        if selected_chat_display != "Pilih Obrolan":
            selected_chat_id = chat_options[selected_chat_display]
            if st.sidebar.button("Lanjutkan Obrolan Ini"):
                st.session_state.current_chat_id = selected_chat_id
                loaded_messages = get_chat_messages(selected_chat_id)
                st.session_state.messages = [{"role": msg[0], "content": msg[1]} for msg in loaded_messages]
                for chat in existing_chats:
                    if chat[0] == selected_chat_id:
                        st.session_state.current_topic = chat[2]
                        break
                st.sidebar.success(f"Melanjutkan obrolan (ID: {selected_chat_id})")
    else:
        st.sidebar.info("Belum ada riwayat obrolan yang tersimpan.")
else:
    st.sidebar.warning("Riwayat obrolan hanya tersedia dalam mode ONLINE.")


# Inisialisasi session state untuk chat jika belum ada
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_topic" not in st.session_state:
    # Default topik jika belum ada chat, ambil dari materi yang dimuat
    st.session_state.current_topic = list(materi.keys())[0]

# Tampilkan topik aktif
st.subheader(f"Topik Aktif: {st.session_state.current_topic}")
st.write(f"**Materi:** {materi[st.session_state.current_topic]}")

# Tampilkan riwayat obrolan yang sedang aktif
st.markdown("---")
st.subheader("Riwayat Obrolan Saat Ini:")
if st.session_state.messages:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write(f"**Anda:** {msg['content']}")
        else:
            st.write(f"**AI:** {msg['content']}")
else:
    st.info("Belum ada percakapan dalam sesi ini.")
st.markdown("---")

# Input pertanyaan
user_q = st.text_input("Tanya sesuatu ke AI:", key="user_question_input")

if st.button("Tanya AI"):
    if not user_q:
        st.warning("Mohon masukkan pertanyaan Anda.")
    else:
        # Tambahkan pesan pengguna ke riwayat sesi (selalu)
        st.session_state.messages.append({"role": "user", "content": user_q})

        # Simpan ke database hanya jika online dan DB aktif
        if has_internet and DB_ENABLED and st.session_state.current_chat_id:
            add_message(st.session_state.current_chat_id, "user", user_q)
        elif not has_internet:
            st.info("Anda dalam mode OFFLINE. Riwayat obrolan tidak akan disimpan.")
        elif not DB_ENABLED:
             st.info("Fitur database tidak aktif. Riwayat obrolan tidak akan disimpan.")
        elif not st.session_state.current_chat_id:
            st.info("Obrolan belum tersimpan karena belum dimulai sebagai sesi database. Riwayat tidak disimpan.")


        with st.spinner("AI sedang berpikir..."):
            full_prompt = f"Ada pelajaran tentang {st.session_state.current_topic}. Jawab pertanyaan ini: {user_q}"
            conversation_history_for_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages[:-1]])
            if conversation_history_for_prompt:
                full_prompt = f"Percakapan sebelumnya:\n{conversation_history_for_prompt}\n\nTopik: {st.session_state.current_topic}. Pertanyaan baru: {user_q}"

            response = query_gemma(full_prompt)

            # Tambahkan jawaban AI ke riwayat sesi (selalu)
            st.session_state.messages.append({"role": "ai", "content": response})

            # Simpan ke database hanya jika online dan DB aktif
            if has_internet and DB_ENABLED and st.session_state.current_chat_id:
                add_message(st.session_state.current_chat_id, "ai", response)

        # Re-run Streamlit untuk menampilkan pesan baru
        st.rerun()