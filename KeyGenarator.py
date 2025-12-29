import os
import hashlib
import time
import base64
from dotenv import load_dotenv  # .env dosyasını okumak için gerekli kütüphane

# .env dosyasındaki değişkenleri sisteme yükle
load_dotenv()

class ProfessionalKeyGenerator:
    """
    Kriptografik olarak güvenli rastgele anahtarlar üreten sınıf.
    """
    def __init__(self):
        # Tuzu kodun içine yazmak yerine .env dosyasından çekiyoruz.
        # 'MY_APP_SALT' değişkenini bulamazsa varsayılan bir değer atar.
        self.salt = os.getenv("MY_APP_SALT", "varsayilan_yedek_tuz_degeri")

    def generate_secure_key(self, length=32):
        # 1. ADIM: Donanımsal Rastgelelik (Entropy)
        # os.urandom, işletim sisteminin CSPRNG çekirdeğinden gerçek rastgelelik çeker.
        random_bytes = os.urandom(64)
        
        # 2. ADIM: Zaman Faktörü
        # Nanosaniye hassasiyeti, aynı anda üretilen anahtarların çakışmasını engeller.
        timestamp = str(time.time_ns()).encode()
        
        # 3. ADIM: Verileri Birleştirme ve Karma (Hashing)
        # Rastgele veriyi, zamanı ve .env'den gelen gizli tuzu harmanlıyoruz.
        hash_input = random_bytes + timestamp + self.salt.encode()
        
        # SHA-256 ile veriyi geri döndürülemez ve tahmin edilemez bir özete çeviriyoruz.
        secure_hash = hashlib.sha256(hash_input).digest()
        
        # 4. ADIM: Okunabilir Formata Dönüştürme
        # URL-safe Base64 kullanarak (+ / gibi sorunlu karakterler olmadan) metne çeviriyoruz.
        key = base64.urlsafe_b64encode(secure_hash).decode('utf-8')
        
        # Kullanıcının istediği uzunlukta kesiyoruz.
        return key[:length]

# --- UYGULAMA BÖLÜMÜ ---

if __name__ == "__main__":
    # Jeneratörü başlatıyoruz (Tuz artık otomatik olarak .env'den alınıyor)
    generator = ProfessionalKeyGenerator()

    # Örnek: 24 karakterli güvenli bir anahtar üret
    new_key = generator.generate_secure_key(24)

    print(f"--- Güvenli Anahtar Sistemi ---")
    print(f"Kullanılan Tuz Kaynağı: {'.env dosyası' if os.getenv('MY_APP_SALT') else 'Varsayılan değer'}")
    print(f"Üretilen Key: {new_key}")
    print(f"Uzunluk: {len(new_key)} karakter")