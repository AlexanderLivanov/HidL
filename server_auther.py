import webbrowser
from flask import Flask, request
import threading
import json

# --- Локальный сервер для callback ---
app = Flask(__name__)
user_data = {}

@app.route("/callback")
def callback():
    user_id = request.args.get("user_id")
    if user_id:
        user_data["user_id"] = int(user_id)
        # сохраняем в JSON
        with open("userdata.json", "w") as f:
            json.dump(user_data, f)
        return "Login successful! You can close this page."
    return "No user_id provided"

def run_server():
    # слушаем только локально
    app.run(host="127.0.0.1", port=5000)

# --- Функция логина ---
def on_login():
    # запускаем сервер в фоне
    threading.Thread(target=run_server, daemon=True).start()
    
    # открываем страницу авторизации на сайте
    # сайт после логина делает redirect на http://127.0.0.1:5000/callback?user_id=...
    webbrowser.open("http://127.0.0.1/login")

    # ждём пока пользователь войдёт
    print("Please log in in your browser...")
    while "user_id" not in user_data:
        pass  # можно добавить sleep(0.5), чтобы не нагружать CPU
    
    print("User logged in! ID =", user_data["user_id"])
    # дальше можно подтягивать профиль через API

# --- Запуск ---
if __name__ == "__main__":
    on_login()
