import sqlite3
from datetime import datetime
from config import Config

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # İşlem Logları Tablosu
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    action TEXT,
                    details TEXT,
                    status TEXT
                )
            """)
            # Dosya Bütünlük Tablosu
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS file_registry (
                    file_path TEXT PRIMARY KEY,
                    file_hash TEXT,
                    last_monitored TEXT
                )
            """)

    def log_action(self, action: str, details: str, status: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            self.conn.execute(
                "INSERT INTO audit_logs (timestamp, action, details, status) VALUES (?, ?, ?, ?)",
                (timestamp, action, details, status)
            )

    def register_file_hash(self, file_path: str, file_hash: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO file_registry (file_path, file_hash, last_monitored) VALUES (?, ?, ?)",
                (file_path, file_hash, timestamp)
            )

    def get_registered_hash(self, file_path: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT file_hash FROM file_registry WHERE file_path = ?", (file_path,))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_all_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp, action, status FROM audit_logs ORDER BY id DESC LIMIT 50")
        return cursor.fetchall()
