# import speech_recognition as sr
# # from pocketsphinx import LiveSpeech, get_model_path

# def get_audio_input(timeout=5, phrase_time_limit=5):
#     """
#     Merekam audio dari mikrofon dan mengonversinya menjadi teks menggunakan Google Speech Recognition.
#     Akan mencoba mengenali suara selama `timeout` detik, dan berhenti merekam setelah
#     `phrase_time_limit` detik jika tidak ada suara terdeteksi.

#     Mengembalikan string teks atau None jika gagal.
#     """
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Sesuaikan ambang batas kebisingan...")
#         r.adjust_for_ambient_noise(source) # Sesuaikan untuk kebisingan lingkungan
#         print("Silakan berbicara sekarang...")
#         try:
#             audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#             print("Merekam selesai, memproses...")
#         except sr.WaitTimeoutError:
#             print("Tidak ada suara terdeteksi.")
#             return "Tidak ada suara terdeteksi."
#         except Exception as e:
#             print(f"Error saat merekam audio: {e}")
#             return f"Error saat merekam audio: {e}"

#     try:
#         # Menggunakan Google Speech Recognition (membutuhkan internet)
#         text = r.recognize_google(audio, language="id-ID") # Gunakan bahasa Indonesia
#         print(f"Anda mengatakan: {text}")
#         return text
#     except sr.UnknownValueError:
#         print("Google Speech Recognition tidak dapat memahami audio.")
#         return "Google Speech Recognition tidak dapat memahami audio."
#     except sr.RequestError as e:
#         print(f"Tidak dapat meminta hasil dari Google Speech Recognition service; {e}")
#         return f"Tidak dapat meminta hasil dari layanan Google Speech Recognition; {e}. (Periksa koneksi internet Anda jika Anda ingin menggunakan fitur ini.)"
#     except Exception as e:
#         print(f"Error tak terduga saat pengenalan suara: {e}")
#         return f"Error tak terduga saat pengenalan suara: {e}"

# # def get_audio_input_offline():
# #     model_path = get_model_path()
#     # Anda perlu mengunduh model bahasa Indonesia untuk Sphinx.
#     # Ini bisa sangat besar dan instalasinya kompleks.
#     # Contoh sederhana (biasanya untuk bahasa Inggris default)
#     # speech = LiveSpeech(
#     #     verbose=False,
#     #     sampling_rate=16000,
#     #     buffer_size=2048,
#     #     no_search=False,
#     #     full_utt=False,
#     #     hmm=os.path.join(model_path, 'en-us'),
#     #     lm=os.path.join(model_path, 'en-us.lm.bin'),
#     #     dic=os.path.join(model_path, 'cmudict-en-us.dict')
#     # )
#     # Untuk Sphinx offline, ini akan lebih rumit dan mungkin memerlukan
#     # konfigurasi spesifik model bahasa Indonesia yang diunduh.
#     # Ini hanya placeholder untuk menunjukkan arahnya.
#     # print("Fitur pengenalan suara offline (CMU Sphinx) belum diimplementasikan sepenuhnya.")
#     # print("Membutuhkan model bahasa Indonesia dan konfigurasi yang lebih kompleks.")
#     # return "Pengenalan suara offline tidak aktif."
# speech input helper module (masih dikembangkan)

pass  # dummy baris agar dikenali git
