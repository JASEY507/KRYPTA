import os

class Config:
    APP_TITLE = "KRYPTA // SECURE_CORE"
    WIDTH = 1100
    HEIGHT = 700
    
    # Cyberpunk Renk Paleti
    COLOR_BG_DARK = "#0A0A0F"
    COLOR_BG_PANEL = "#12121A"
    COLOR_NEON_RED = "#FF003C"
    COLOR_NEON_GREEN = "#00FF66"
    COLOR_NEON_BLUE = "#00F0FF"
    COLOR_TEXT_MUTED = "#5A5A75"
    COLOR_TEXT_BODY = "#C0C0D0"
    
    FONT_TERMINAL = "Courier New"
    FONT_INTERFACE = "Segoe UI"
    
    DB_PATH = "krypta_secure.db"
    CHUNK_SIZE = 64 * 1024

    # DİL SÖZLÜKLERİ (LOCALIZATION REPOSITORY)
    LANGUAGES = {
        "TR": {
            "auth_title": "KRYPTA // ERİŞİM DOĞRULAMA",
            "placeholder_master": "ANA GÜVENLİK PAROLASI",
            "btn_enter": "ÇEKİRDEĞİ ÇÖZ & GİRİŞ YAP",
            "err_short": "HATA: GÜVENLİK ANAHTARI ÇOK KISA",
            "core_engine": "= KRYPTA KRİPTO MOTORLARI =",
            "lbl_session": "Dinamik Oturum Şifresi:",
            "cb_backup": "Otomatik Yedek (.bak)",
            "cb_shred": "Kaynak Dosyayı Güvenli Sil (Shred)",
            "btn_select": "DOSYA / KLASÖR SEÇ",
            "btn_encrypt": "🔒 VERİLERİ ŞİFRELE",
            "btn_decrypt": "🔓 ŞİFRELERİ ÇÖZ",
            "queue_title": "İŞLEM KUYRUĞU / METADATA TARGETS",
            "strength_analyzing": "ANALİZ EDİLİYOR...",
            "strength_lbl": "DURUM: ",
            "log_init": "Krypta Kriptografik Çekirdek Yapılandırıldı.",
            "log_ready": "AES-256-CBC standartları operasyona hazır.",
            "log_queue": "yeni öge işlem kuyruğuna alındı.",
            "err_empty_pool": "Hata: Hedef havuz boş.",
            "log_triggered": "Krypta Şifreleme Motoru tetiklendi...",
            "log_zip": "Dizin sıkıştırılıyor ve sarmalanıyor: ",
            "log_backup": "Yedek alındı: ",
            "log_shred": "Shred: Orijinal izler diskten kazındı.",
            "log_match": "Bütünlük doğrulaması kusursuz (SHA-256 MATCH).",
            "log_unlocked": "Kilit Açıldı: ",
            "err_decrypt": "Çözme Başarısız: Geçersiz anahtar veya veri bütünlüğü kaybı.",
            "err_manipulated": "KRİTİK HATA: Veri imzası uyuşmuyor! Dosya manipüle edilmiş olabilir.",
            "select_dest": "Çözülen Ögelerin Çıkarılacağı Dizini Seçin",
            "select_src": "Krypta - Hedef Ögeleri Seçin"
        },
        "EN": {
            "auth_title": "KRYPTA // ACCESS AUTHORIZATION",
            "placeholder_master": "MASTER SECURITY PHRASE",
            "btn_enter": "DECRYPT CORE & ENTER",
            "err_short": "ERR: SECURITY KEY TOO SHORT",
            "core_engine": "= KRYPTA CORE ENGINES =",
            "lbl_session": "Dynamic Session Password:",
            "cb_backup": "Automatic Backup (.bak)",
            "cb_shred": "Secure Shred Source File",
            "btn_select": "SELECT FILE / FOLDER",
            "btn_encrypt": "🔒 ENCRYPT TARGETS",
            "btn_decrypt": "🔓 DECRYPT TARGETS",
            "queue_title": "PROCESSING QUEUE / METADATA TARGETS",
            "strength_analyzing": "ANALYZING ENTROPY...",
            "strength_lbl": "STATUS: ",
            "log_init": "Krypta Cryptographic Core Initialized.",
            "log_ready": "AES-256-CBC standards ready for deployment.",
            "log_queue": "new items added to operational queue.",
            "err_empty_pool": "Error: Target pool is empty.",
            "log_triggered": "Krypta Encryption Engine triggered...",
            "log_zip": "Compressing and shielding directory: ",
            "log_backup": "Backup generated: ",
            "log_shred": "Shred: Original data wiped from sectors.",
            "log_match": "Integrity validation perfect (SHA-256 MATCH).",
            "log_unlocked": "Decrypted & Unlocked: ",
            "err_decrypt": "Decryption Failed: Invalid key or payload corruption.",
            "err_manipulated": "CRITICAL ERR: Signature mismatch! Payload might be manipulated.",
            "select_dest": "Select Destination Directory for Decrypted Files",
            "select_src": "Krypta - Select Target Items"
        }
    }
