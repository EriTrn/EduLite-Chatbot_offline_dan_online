# EduLite: Pembelajaran Cerdas dan Offline untuk Semua

**EduLite** adalah aplikasi pembelajaran interaktif berbasis AI yang dirancang untuk berjalan secara **offline**, membantu siswa di daerah dengan koneksi internet terbatas agar tetap bisa belajar dengan pengalaman cerdas, menyenangkan, dan modern.

---

## 🎯 Tujuan Proyek

- Menyediakan **aplikasi pembelajaran lokal** yang ringan dan mudah digunakan.
- Menggunakan model AI lokal (contoh: **Gemma 3n**) untuk memberikan pengalaman tanya-jawab dan pembelajaran adaptif.
- Memastikan semua fitur berjalan **tanpa koneksi internet**.
- Bisa dijalankan di laptop standar (RAM 8 GB).

---

## 🧠 Fitur Utama

- 🔹 Materi pelajaran interaktif berbasis teks dan media
- 🔹 Tanya-jawab cerdas menggunakan AI lokal
- 🔹 Antarmuka sederhana dengan Streamlit
- 🔹 Penyimpanan materi dan prompt dalam folder lokal
- 🔹 Desain siap dikembangkan lebih lanjut (kuis, evaluasi, pelacakan belajar)

---

## 🗂️ Struktur Folder

EduLite/
├── app.py # Entry point Streamlit (Frontend + Backend)
├── requirements.txt # Daftar library Python
├── assets/ # Folder gambar, ikon, audio lokal
│ └── logo.png
├── prompts/ # Template pertanyaan atau materi pelajaran
│ └── edukasi_bahasa.txt
├── data/ # Konten pelajaran (bisa ditambah)
│ └── materi_kelas1.json
├── utils/ # Fungsi bantu
│ └── ai_client.py # Interaksi ke model Gemma lokal
│ └── loader.py # Loader materi
├── README.md # Deskripsi proyek
