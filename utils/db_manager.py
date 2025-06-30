import psycopg2
from datetime import datetime
import os

def get_db_connection():
    """Membuka koneksi ke database PostgreSQL."""
    # Prioritaskan DATABASE_URL jika tersedia
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        try:
            conn = psycopg2.connect(database_url)
            return conn
        except psycopg2.OperationalError as e:
            print(f"⚠️ Gagal terhubung ke database menggunakan DATABASE_URL: {e}")
            return None
    else:
        # Fallback ke individual variables jika DATABASE_URL tidak ada
        host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        port = os.getenv("DB_PORT")

        # Pastikan kredensial penting ada
        if not user or not password or not host or not db_name:
            print("Error: Kredensial database (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD) belum disetel di variabel lingkungan.")
            return None

        try:
            conn = psycopg2.connect(
                host=host,
                database=db_name,
                user=user,
                password=password,
                port=port
            )
            return conn
        except psycopg2.OperationalError as e:
            print(f"⚠️ Gagal terhubung ke database: {e}")
            return None

def create_tables(conn):
    """Membuat tabel 'chats' dan 'messages' jika belum ada."""
    if not conn:
        print("Error: Koneksi database tidak tersedia untuk membuat tabel.")
        return False
    try:
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
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False
    # finally: # Jangan tutup koneksi di sini karena conn akan di-cache di app.py
    #     if conn:
    #         conn.close()

def create_new_chat(conn, topic): 
    """Membuat obrolan baru dan mengembalikan chat_id."""
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chats (topic) VALUES (%s) RETURNING chat_id;",
            (topic,)
        )
        chat_id = cur.fetchone()[0]
        conn.commit()
        return chat_id
    except Exception as e:
        print(f"Error creating new chat: {e}")
        return None
    # finally:
    #     if conn:
    #         conn.close()

def get_all_chats(conn):
    """Mengambil semua obrolan yang ada."""
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT chat_id, start_time, topic FROM chats ORDER BY last_active_time DESC;")
        chats = cur.fetchall()
        return chats
    except Exception as e:
        print(f"Error getting all chats: {e}")
        return []
    # finally:
    #     if conn:
    #         conn.close()

def get_chat_messages(conn, chat_id):
    """Mengambil semua pesan untuk chat_id tertentu."""
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT sender, content, timestamp FROM messages WHERE chat_id = %s ORDER BY timestamp ASC;",
            (chat_id,)
        )
        messages = cur.fetchall()
        return messages
    except Exception as e:
        print(f"Error getting chat messages: {e}")
        return []
    # finally:
    #     if conn:
    #         conn.close()

def add_message(conn, chat_id, sender, content):
    """Menambahkan pesan ke obrolan tertentu."""
    if not conn: return
    try:
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
    # finally:
    #     if conn:
    #         conn.close()