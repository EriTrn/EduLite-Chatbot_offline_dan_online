import psycopg2
from datetime import datetime
import os

# Konfigurasi database
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", 52285)
}

def get_db_connection():
    """Membuka koneksi ke database PostgreSQL."""
    # Pastikan kredensial penting ada
    if not DB_CONFIG["user"] or not DB_CONFIG["password"]:
        print("Error: Kredensial database (DB_USER, DB_PASSWORD) belum disetel di variabel lingkungan.")
        return None

    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"⚠️ Gagal terhubung ke database: {e}")
        return None

def create_tables():
    """Membuat tabel 'chats' dan 'messages' jika belum ada."""
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id SERIAL PRIMARY KEY,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    topic VARCHAR(255)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id SERIAL PRIMARY KEY,
                    chat_id INTEGER REFERENCES chats(chat_id),
                    sender VARCHAR(50), -- 'user' or 'ai'
                    content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("Tabel database berhasil dibuat atau sudah ada.")
            return True
        return False
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        if conn:
            conn.close()

def create_new_chat(topic):
    """Membuat obrolan baru dan mengembalikan chat_id."""
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO chats (topic) VALUES (%s) RETURNING chat_id;",
                (topic,)
            )
            chat_id = cur.fetchone()[0]
            conn.commit()
            return chat_id
        return None
    except Exception as e:
        print(f"Error creating new chat: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_chats():
    """Mengambil semua obrolan yang ada."""
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT chat_id, start_time, topic FROM chats ORDER BY last_active_time DESC;")
            chats = cur.fetchall()
            return chats
        return []
    except Exception as e:
        print(f"Error getting all chats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_chat_messages(chat_id):
    """Mengambil semua pesan untuk chat_id tertentu."""
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT sender, content, timestamp FROM messages WHERE chat_id = %s ORDER BY timestamp ASC;",
                (chat_id,)
            )
            messages = cur.fetchall()
            return messages
        return []
    except Exception as e:
        print(f"Error getting chat messages: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_message(chat_id, sender, content):
    """Menambahkan pesan ke obrolan tertentu."""
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO messages (chat_id, sender, content) VALUES (%s, %s, %s);",
                (chat_id, sender, content)
            )
            cur.execute(
                "UPDATE chats SET last_active_time = CURRENT_TIMESTAMP WHERE chat_id = %s;",
                (chat_id,)
            )
            conn.commit()
    except Exception as e:
        print(f"Error adding message: {e}")
    finally:
        if conn:
            conn.close()