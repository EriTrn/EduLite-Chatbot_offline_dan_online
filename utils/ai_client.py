import streamlit as st
import google.generativeai as genai
import os

# def query_gemma(prompt, model="gemma3n:e4b"):
#     url = "http://localhost:11434/api/generate"
#     payload = {
#         "model": model,
#         "prompt": prompt,
#         "stream": False
#     }
#     try:
#         response = requests.post(url, json=payload)
#         return response.json()['response'].strip()
#     except Exception as e:
#         return f"⚠️ Gagal menghubungi model lokal: {e}"

# --- Konfigurasi API Key ---
try:
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("GOOGLE_API_KEY tidak ditemukan. Harap atur di Streamlit secrets atau environment variables.")
except Exception as e:
    st.error(f"Terjadi kesalahan saat konfigurasi Google AI: {e}")


def query_gemma(prompt: str) -> str:
    """
    Mengirimkan prompt ke Google AI API menggunakan model yang ditentukan
    dan mengembalikan respons dalam bentuk teks.
    """
    if not genai.get_key():
        return "⚠️ Konfigurasi API Key Google AI gagal. Fungsi AI tidak dapat digunakan."
        
    try:
        model = genai.GenerativeModel('gemma2-9b-it')

        response = model.generate_content(prompt)

        return response.text.strip()
        
    except Exception as e:
        st.error(f"Terjadi kesalahan saat menghubungi Google AI API: {e}")
        return "Maaf, terjadi kesalahan saat mencoba menghubungi AI. Silakan coba lagi nanti."