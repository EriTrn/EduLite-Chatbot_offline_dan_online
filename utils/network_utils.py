import requests

def check_internet_connection(timeout=3):
    """
    Memeriksa koneksi internet dengan mencoba menghubungi Google.
    Mengembalikan True jika ada koneksi, False jika tidak.
    """
    try:
        requests.get("http://www.google.com", timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    except Exception: # Tangani error lain, misal DNS error
        return False