import time
import zipfile
import threading
import requests
import psutil
import pystray
from PIL import Image, ImageDraw
import subprocess
import os
import json
import webbrowser


# -------------------
# tray icon
def create_image():
    # минималистичная иконка
    img = Image.new('RGB', (64, 64), color='black')
    d = ImageDraw.Draw(img)
    d.rectangle([16, 16, 48, 48], fill='green')
    return img

def on_quit(icon, item):
    icon.stop()
    
def get_user_id():
    try:
        res = requests.get("http://127.0.0.1/api/check_session")
        res_text = res.text.strip()  # убираем лишние пробелы/переводы строк
        user_id = int(res_text)
        if user_id > 0:
            print("User logged in! ID =", user_id)
            return user_id
        else:
            print("User not logged in")
            return None
    except Exception as e:
        print("Error:", e)
        return None


icon = pystray.Icon("hidl", create_image(), "HidL", menu=pystray.Menu(
    pystray.MenuItem("Отключиться", on_quit),
    pystray.MenuItem("Войти в аккаунт", get_user_id)
))
threading.Thread(target=icon.run, daemon=True).start()

# -------------------
# распаковка игры
def unpack_game(zip_path, out_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(out_dir)
    print(f"Game unpacked to {out_dir}")

# -------------------
# проверка запущенных игр
def check_running_games():
    for p in psutil.process_iter(['name']):
        if p.info['name'] in ["MyGame.exe", "MyGame"]:
            print(f"User is playing {p.info['name']}")

# -------------------
# отправка статистики на сервер
def send_stats(game_id, play_time):
    url = "https://127.0.0.1/api/game_stats"
    data = {"game_id": game_id, "play_time": play_time}
    try:
        requests.post(url, json=data)
    except:
        pass

# -------------------
# запуск игры через HidL
def launch_game(exe_path):
    subprocess.Popen([exe_path])
    print(f"Game {exe_path} launched")

# -------------------
# главный цикл
while True:
    check_running_games()
    # тут можно ставить игры в фоне, распаковывать, обновлять
    send_stats(game_id=123, play_time=5)
    time.sleep(60)  # раз в минуту
