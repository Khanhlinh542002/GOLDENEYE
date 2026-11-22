"""app.py - Ứng dụng Flask chính: định nghĩa các đường dẫn (route).
Chạy: pip install flask  ->  python app.py  ->  mở http://127.0.0.1:5000
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import database as db

app = Flask(__name__, instance_path=db.INSTANCE_DIR)
app.secret_key = os.environ.get("SECRET_KEY", "hay-doi-khoa-bi-mat-nay")

# Tạo bảng ngay khi ứng dụng khởi động (cần cho gunicorn trên Render)
db.init_db()

# Số lượng cộng mỗi lần bấm nút "+"
REWARDS = {"coins": 100, "cash": 5}


def current_player():
    """Lấy người chơi đang đăng nhập (None nếu chưa đăng nhập)."""
    pid = session.get("player_id")
    return db.get_player(pid) if pid else None


@app.route("/")
def index():
    player = current_player()
    if not player:
        return redirect(url_for("login"))
    return render_template("index.html", player=player)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()[:20]
        if name:
            session["player_id"] = db.get_or_create_player(name)["id"]
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/api/add", methods=["POST"])
def api_add():
    """JavaScript gọi vào đây khi bấm nút '+' để lưu xu/tiền vào database."""
    player = current_player()
    kind = (request.get_json(silent=True) or {}).get("type")
    if not player or kind not in REWARDS:
        return jsonify(error="Yêu cầu không hợp lệ"), 400
    updated = db.add_resource(player["id"], kind, REWARDS[kind])
    return jsonify(coins=updated["coins"], cash=updated["cash"], added=REWARDS[kind])


if __name__ == "__main__":
    app.run(debug=True)
