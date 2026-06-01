import os
import zlib
import zipfile
import hashlib
import shutil
from concurrent.futures import ThreadPoolExecutor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from config import Config

class CryptoEngine:
    @staticmethod
    def calculate_sha256(file_path: str) -> str:
        """Büyük dosyaları bellek dostu şekilde chunk'lar halinde hash'ler."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(Config.CHUNK_SIZE):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        return kdf.derive(password.encode())

    @staticmethod
    def generate_rsa_keys() -> tuple[bytes, bytes]:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
        public_key = private_key.public_key()
        
        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        pub_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return priv_pem, pub_pem

    @classmethod
    def encrypt_file(cls, input_path: str, output_path: str, password: str, progress_callback=None) -> str:
        if not os.path.exists(input_path):
            raise FileNotFoundError("Kaynak dosya bulunamadı.")
            
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = cls.derive_key(password, salt)
        
        file_size = os.path.getsize(input_path)
        bytes_processed = 0
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # Orijinal uzantıyı meta veri olarak saklamak üzere hazırlarız
        orig_ext = os.path.splitext(input_path)[1].encode('utf-8').zfill(16)[:16]
        
        with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
            f_out.write(salt)
            f_out.write(iv)
            f_out.write(orig_ext)
            
            while chunk := f_in.read(Config.CHUNK_SIZE):
                bytes_processed += len(chunk)
                if len(chunk) % 16 != 0:
                    padding_length = 16 - (len(chunk) % 16)
                    chunk += bytes([padding_length]) * padding_length
                
                f_out.write(encryptor.update(chunk))
                if progress_callback:
                    progress_callback(bytes_processed / file_size)
                    
            f_out.write(encryptor.finalize())
        return cls.calculate_sha256(output_path)

    @classmethod
    def decrypt_file(cls, input_path: str, output_dir: str, password: str, progress_callback=None) -> str:
        file_size = os.path.getsize(input_path)
        bytes_processed = 32 + 16 # Salt + IV + Ext offsetleri
        
        with open(input_path, "rb") as f_in:
            salt = f_in.read(16)
            iv = f_in.read(16)
            orig_ext = f_in.read(16).decode('utf-8').strip('\x00')
            
            key = cls.derive_key(password, salt)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            
            out_filename = os.path.splitext(os.path.basename(input_path))[0] + "_decrypted" + orig_ext
            output_path = os.path.join(output_dir, out_filename)
            
            with open(output_path, "wb") as f_out:
                while chunk := f_in.read(Config.CHUNK_SIZE):
                    bytes_processed += len(chunk)
                    decrypted_chunk = decryptor.update(chunk)
                    
                    # Eğer dosyanın son bloğu ise padding temizlenir
                    if bytes_processed >= file_size:
                        decrypted_chunk += decryptor.finalize()
                        if decrypted_chunk:
                            padding_len = decrypted_chunk[-1]
                            if padding_len <= 16:
                                decrypted_chunk = decrypted_chunk[:-padding_len]
                                
                    f_out.write(decrypted_chunk)
                    if progress_callback:
                        progress_callback(min(bytes_processed / file_size, 1.0))
                        
        return output_path

    @classmethod
    def secure_zip_and_encrypt(cls, folder_path: str, output_enc_path: str, password: str, progress_callback=None) -> str:
        temp_zip = folder_path + ".temp.zip"
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, os.path.dirname(folder_path))
                    zipf.write(full_path, rel_path)
        
        if progress_callback: progress_callback(0.5)
        enc_hash = cls.encrypt_file(temp_zip, output_enc_path, password, progress_callback)
        
        if os.path.exists(temp_zip):
            cls.secure_shred(temp_zip)
        return enc_hash

    @staticmethod
    def secure_shred(file_path: str):
        """Bellek ve disk üzerinde kalıntı bırakmamak için dosyayı üzerine yazarak yok eder."""
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            with open(file_path, "ba+", buffering=0) as f:
                f.seek(0)
                f.write(os.urandom(size))
            os.remove(file_path)

    @staticmethod
    def analyze_password_strength(password: str) -> tuple[float, str, str]:
        """Entropy tabanlı şifre gücü analizi yapar."""
        if not password: return 0.0, "YOK", "#FF003C"
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_spec = any(not c.isalnum() for c in password)
        
        score = sum([has_upper, has_lower, has_digit, has_spec])
        entropy = length * (score * 0.5)
        
        if entropy < 12: return min(entropy/30, 0.3), "ZAYIF", "#FF003C"
        if entropy < 25: return min(entropy/30, 0.6), "ORTA", "#00F0FF"
        return 1.0, "GÜÇLÜ (MILITARY-GRADE)", "#00FF66"
