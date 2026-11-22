"""database.py - Xử lý cơ sở dữ liệu SQLite (file nằm trong thư mục instance/)."""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "game.db")

# Chỉ cho phép cộng vào các cột này (tránh SQL injection)
RESOURCE_FIELDS = {"coins", "cash"}


def get_conn():
    """Mở kết nối tới database, kết quả trả về dạng dict-like."""
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Tạo bảng người chơi nếu chưa có."""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                xp INTEGER DEFAULT 19,
                xp_max INTEGER DEFAULT 35,
                population INTEGER DEFAULT 40,
                pop_max INTEGER DEFAULT 150,
                coins INTEGER DEFAULT 606,
                cash INTEGER DEFAULT 36
            )""")


def get_or_create_player(name):
    """Tìm người chơi theo tên, chưa có thì tạo mới. Trả về dòng dữ liệu."""
    with get_conn() as conn:
        conn.execute("INSERT OR IGNORE INTO players (name) VALUES (?)", (name,))
        return conn.execute("SELECT * FROM players WHERE name=?", (name,)).fetchone()


def get_player(player_id):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM players WHERE id=?", (player_id,)).fetchone()


def add_resource(player_id, field, amount):
    """Cộng thêm xu hoặc tiền cho người chơi, trả về dòng dữ liệu mới."""
    if field not in RESOURCE_FIELDS:
        raise ValueError("Cột không hợp lệ")
    with get_conn() as conn:
        conn.execute(f"UPDATE players SET {field} = {field} + ? WHERE id=?", (amount, player_id))
        return conn.execute("SELECT * FROM players WHERE id=?", (player_id,)).fetchone()
