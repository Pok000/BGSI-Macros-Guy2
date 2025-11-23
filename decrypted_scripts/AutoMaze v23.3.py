from pynput import keyboard
from PIL import ImageGrab
import pydirectinput
import numpy as np
import threading
import time
import cv2
import sys
import os
import functools
import ctypes
import requests
import pygetwindow as gw
import win32gui, win32con, win32api
from pywinauto import Application
import pyautogui
import mss

# DESCRIPTION: Completes the Maze Minigame
# VERSIONS: all

version = "v23.3"
try:
    from ahk import AHK
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    bundled_ahk = os.path.join(base_path, 'AutoHotkey.exe')
    installed_ahk = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"

    ahk_exe_path = bundled_ahk if os.path.exists(bundled_ahk) else installed_ahk
    ahk = AHK(executable_path=ahk_exe_path)
except Exception as e:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"AutoHotkey could not be loaded from either bundled or installed path.\n\nError: {e}",
        "AutoHotkey Error",
        0x10
    )
    sys.exit()

# auto res
res_info = 0
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
if screen_width == 2560 and screen_height == 1440:
    res_info = 2560
    center = (1280, 720)
    check_area1 = (277, 97, 878, 531)
    check_area2 = (761, 1, 1716, 505)
    check_area3 = (1198, 416, 1357, 553)
    claim = ['claim.png']
    skip = ['skip.png']
    insane = ['insane.png']
    top_left = (0, 300)
    bottom_right = (2188, 1000)
    absolute_bottom_right = (2560, 1440)
    insane_btn = (1264, 994)
    debug = (1045, 57)
    loading = (718, 1226, 1519, 1439)
    teleport = (1277, 1369)
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    center = (960, 540)
    check_area1 = (367, 88, 720, 315)
    check_area2 = (633, 1, 1182, 451)
    check_area3 = (905, 316, 1009, 420)
    claim = ['claim2.png']
    skip = ['skip2.png']
    insane = ['insane2.png']
    top_left = (0, 300)
    bottom_right = (1660, 759)
    absolute_bottom_right = (1920, 1080)
    insane_btn = (948, 778)
    debug = (756, 50)
    loading = (501, 845, 992, 1079)
    teleport = (966, 1017)
elif screen_width in [1366, 1364] and screen_height == 768:
    res_info = 1366
    center = (683, 384)
    check_area1 = (266, 66, 486, 218)
    check_area2 = (443, 1, 823, 244)
    check_area3 = (636, 222, 739, 303)
    claim = ['claim3.png']
    skip = ['skip3.png']
    insane = ['insane3.png']
    top_left = (0, 250)
    bottom_right = (1214, 667)
    absolute_bottom_right = (1366, 768)
    insane_btn = (672, 568)
    debug = (528, 39)
    loading = (353, 582, 682, 767)
    teleport = (686, 716)
else:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"Please either use 2560x1440, 1920x1080 or 1366x768 resolution and set your scale to 100% for this macro to work.\nCurrent resolution: {screen_width}x{screen_height}",
        "Invalid resolution",
        0x10
    )
    sys.exit()

print = functools.partial(print, flush=True)

def auto_f11():
    rblx = [w for w in gw.getWindowsWithTitle('Roblox') if w.title == 'Roblox']
    if len(rblx) != 1:
        print("More than 1 roblox game running" if rblx else "No Roblox window found")
        return

    hwnd = rblx[0]._hWnd
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    mon_rect = win32api.GetMonitorInfo(monitor)['Monitor']
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)

    is_fullscreen = (
        left <= mon_rect[0] and top <= mon_rect[1] and
        right >= mon_rect[2] and bottom >= mon_rect[3] and
        not (style & (win32con.WS_CAPTION | win32con.WS_THICKFRAME))
    )

    if not is_fullscreen:
        win32gui.SetForegroundWindow(hwnd)
        Application().connect(handle=hwnd).window(handle=hwnd).type_keys('{F11}')
        print("Toggled fullscreen for Roblox")
    time.sleep(1)

# coord recalculation
def convert(original_coords, original_resolution=(2560, 1440)):
    global user_width, user_height
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    user_width = root.winfo_screenwidth()
    user_height = root.winfo_screenheight()
    new_x = int(original_coords[0] * (user_width / original_resolution[0]))
    new_y = int(original_coords[1] * (user_height / original_resolution[1]))
    return new_x, new_y

# global names
TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3
DEBUG_switch = keyboard.Key.f5

# others
running_flag = False    
total_time = ""
lamp_color = (254, 247, 147)
first_skip = True
debug_col = (221, 46, 68)
area3_col = (3, 63, 0)
area3_col2 = (13, 89, 11)
loading_col = (12, 12, 3)
games_completed = 0
incomplete_games = 0
webhook = False

# function to format elapsed time into hh:mm:ss
def format_time_ignore(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# function to update session time in the background
def update_session_time_ignore():
    global total_time
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        total_time = format_time_ignore(elapsed_time)
        time.sleep(1)

# Start the session time update thread
session_time_thread = threading.Thread(target=update_session_time_ignore, daemon=True)
session_time_thread.start()

# clearing the cmd
def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def stats():
    cls()
    times = total_time.split(':')
    hrs = int(times[0]) + int(times[1])/60 + int(times[2])/3600
    if hrs > 0:
        avg = round((games_completed + incomplete_games) / hrs, 1)
    else:
        avg = 0
    
    stats_msg = f'Auto Maze {version} by Lisek_guy2\nTotal Time Spent: {total_time}\nGames Completed: {games_completed}\nGames Failed: {incomplete_games}\nGames per hour: {avg}'
    if webhook:
        save_msg(stats_msg)
    else:
        print(stats_msg)

log_queue = []
webhook_link = None
_lock = threading.Lock()
message_id = None

def webhook_link_batch():
    global message_id

    if not webhook_link:
        return

    if message_id is None:
        try:
            response = requests.post(webhook_link + "?wait=true", json={"content": "Starting..."})
            if response.status_code == 200:
                message_id = response.json()["id"]
            else:
                print(f"[Webhook] Failed to send initial message: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"[Webhook] Exception sending initial message: {e}")
            return

    while True:
        time.sleep(0.5)
        with _lock:
            if not log_queue:
                continue

            batch_content = "\n".join(log_queue)
            log_queue.clear()
            batch = f"```text\n{batch_content}\n```"

        try:
            edit_url = f"{webhook_link}/messages/{message_id}"
            response = requests.patch(edit_url, json={"content": batch})
            if response.status_code not in [200, 204]:
                print(f"[Webhook] Failed to edit message: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[Webhook] Exception while editing message: {e}")

def save_msg(msg, type='print'):
    if type == 'print':
        print(msg)
    with _lock:
        log_queue.append(msg)
            
threading.Thread(target=webhook_link_batch, daemon=True).start()

def auto_stats_update():
    while True:
        time.sleep(5)
        if webhook:
            stats()

threading.Thread(target=auto_stats_update, daemon=True).start()

def webhook_input():
    global webhook, webhook_link
    webhook_link_input = input("Enter your webhook: ").strip()
    if webhook_link_input:
        webhook_link = webhook_link_input
        webhook = True
        cls()
        print(f'Auto Maze {version} by Lisek_guy2\n\nMacro running correctly\nTo start press F2, to stop press F3\nPress F5 to add your webhook (optional but recommended)\n')
        webhook_link_batch()
    else:
        print("Invalid webhook")

def move(target_x, target_y):
    pydirectinput.moveTo(target_x + 4, target_y + 4)
    ahk.mouse_move(target_x, target_y)
    pydirectinput.click(target_x, target_y)

def nomove(x, y):
    ahk.mouse_move(x, y)

def image(region_top_left, region_bottom_right, template_path, threshold=0.8):
    x1, y1 = region_top_left
    x2, y2 = region_bottom_right
    width = x2 - x1
    height = y2 - y1

    with mss.mss() as sct:
        monitor = {"top": y1, "left": x1, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_BGRA2BGR)

    template = cv2.imread(template_path)
    if template is None:
        raise FileNotFoundError(f"Could not load template: {template_path}")

    result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        template_height, template_width = template.shape[:2]

        absolute_x = max_loc[0] + x1 + template_width // 2
        absolute_y = max_loc[1] + y1 + template_height // 2
        return (absolute_x, absolute_y)
    else:
        return None

def detect_color(coords, target_color, tolerance=20):
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    bgr_color = img[coords[1], coords[0]]
    target_color_bgr = (target_color[2], target_color[1], target_color[0])
    diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
    return np.all(diff <= tolerance)

def check(area, distance, color, tolerance=10):
    x1, y1, x2, y2 = area
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    target_color_bgr = (color[2], color[1], color[0])
    for y in range(y1, y2 + 1, distance):
        for x in range(x1, x2 + 1, distance):
            if y < img.shape[0] and x < img.shape[1]:
                bgr_color = img[y, x]
                diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
                if np.all(diff <= tolerance):
                    return True
    return False

def scroll(direction, amount):
    if direction == 'up':
        pyautogui.scroll(amount)
    elif direction == 'down':
        pyautogui.scroll(-amount)

def area(area):
    if area == 1:
        pydirectinput.keyDown('w')
        time.sleep(0.741)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.560)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(1.094)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(1.257)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.933)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.711)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.882)
        pydirectinput.keyUp('w')

    if area == 2:
        pydirectinput.keyDown('a')
        time.sleep(0.156)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(3.080)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.929)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.844)
        pydirectinput.keyUp('w')

    if area == 3:
        pydirectinput.keyDown('w')
        time.sleep(0.986)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.656)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.501)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(0.270)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.640)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(0.495)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(0.287)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(1.075)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(2.243)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.438)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(0.872)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(0.507)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(1.030)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('w')
        time.sleep(0.117)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(1.965)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.706)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(0.368)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(1.829)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.361)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(0.564)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.471)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.419)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.501)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.539)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(1.724)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(1.131)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.483)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.729)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(2.011)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(1.793)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(1.189)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(1.024)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(0.109)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(1.644)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(1.616)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.588)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.408)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(0.564)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.400)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(0.819)
        pydirectinput.keyUp('s')
        time.sleep(1)

    if area == 4:
        pydirectinput.keyDown('d')
        time.sleep(1.390)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(1.257)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(0.720)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(0.447)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.448)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(1.238)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(1.319)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.863)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(1.850)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(3.107)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.371)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.541)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.257)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(0.440)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.617)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(2.033)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.656)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(2.305)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.471)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(2.117)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(2.096)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(1.193)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.764)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(1.047)
        pydirectinput.keyUp('w')

    if area != 3:
        pydirectinput.keyDown('d')
        time.sleep(0.337)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(1.743)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(0.539)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(0.768)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(0.788)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.152)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(0.502)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.266)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.660)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.393)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(1.519)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.946)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.571)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.693)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(1.992)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('s')
        time.sleep(0.788)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(0.164)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(0.882)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(1.031)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(2.368)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(1.772)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('w')
        time.sleep(0.522)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.394)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('w')
        time.sleep(0.672)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.368)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('s')
        time.sleep(0.923)
        pydirectinput.keyUp('s')
        time.sleep(1)

def find_area():
    if check(check_area1, 3, lamp_color):
        print('Area 1 found')
        area(1)
        return
    if check(check_area3, 1, area3_col, 10) or check(check_area3, 1, area3_col2, 10):
        print('Area 3 found')
        area(3)
        return
    else:
        pydirectinput.keyDown('s')
        time.sleep(1.5)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(0.25)
        pydirectinput.keyUp('a')
        if check(check_area2, 8, lamp_color):
            print('Area 2 found')
            area(2)
            return
        else:
            print('Area 4 found')
            area(4)
            return
cls()
print(f'Auto Maze {version} by Lisek_guy2\n\nMacro running correctly\nTo start press F2, to stop press F3\nPress F5 to add your webhook (optional but recommended)\n')
def action_loop():
    global first_skip, games_completed, incomplete_games
    while True:
        if running_flag:
            if not first_skip:
                pydirectinput.keyDown('s')
                time.sleep(0.060)
                pydirectinput.keyUp('s')
                pydirectinput.keyDown('a')
                time.sleep(0.222)
                pydirectinput.keyUp('a')
                time.sleep(0.5)
                move(center[0], center[1] - 100)
                time.sleep(0.3)
            first_skip = False
            timeout = time.time() + 15
            while time.time() < timeout:
                found_claim = image(top_left, absolute_bottom_right, claim[0])
                if found_claim:
                    move(*found_claim)
                found_skip = image(top_left, absolute_bottom_right, skip[0])
                if found_skip:
                    move(*found_skip)
                    time.sleep(0.3)
                found_insane = image(top_left, absolute_bottom_right, insane[0])
                if found_insane:
                    move(*found_insane)
                    stats()
                    for _ in range(2):
                        time.sleep(0.2)
                        pydirectinput.click()
                    time.sleep(2)
                    timer = time.time() + 20
                    while time.time() < timer:
                        if not detect_color((center[0], 200), (17, 21, 22), 5):
                            print('Game loaded')
                            time.sleep(0.5)
                            break
                        time.sleep(0.5)
                    break
                else:
                    pydirectinput.press('space')
                    time.sleep(1.5)
            else:
                save_msg('Restarting your position, no claim/skip/insane buttons found')
                pydirectinput.keyDown('o')
                time.sleep(0.5)
                pydirectinput.keyUp('o')
                pydirectinput.press('m')
                time.sleep(2.5)
                move(*teleport)
                time.sleep(2)
                pydirectinput.keyDown('a')
                time.sleep(0.564)
                pydirectinput.keyUp('a')
                pydirectinput.keyDown('s')
                time.sleep(1.271)
                pydirectinput.keyUp('s')
                pydirectinput.keyDown('a')
                time.sleep(0.905)
                pydirectinput.keyUp('a')
                pydirectinput.keyDown('s')
                time.sleep(1.289)
                pydirectinput.keyUp('s')
                pydirectinput.keyDown('a')
                time.sleep(3.117)
                pydirectinput.keyUp('a')
                pydirectinput.keyDown('w')
                time.sleep(0.779)
                pydirectinput.keyUp('w')
                pydirectinput.keyDown('a')
                time.sleep(2.109)
                pydirectinput.keyUp('a')
                pydirectinput.keyDown('s')
                time.sleep(0.451)
                pydirectinput.keyUp('s')
                pydirectinput.keyDown('a')
                time.sleep(1.572)
                pydirectinput.keyUp('a')
                time.sleep(0.5)
                first_skip = True
                continue
            find_area()
            if detect_color(debug, debug_col):
                incomplete_games += 1
                save_msg('You messed up the maze at some point and idk why (waiting to restart)')
                while True:
                    if not detect_color(debug, debug_col):
                        time.sleep(14)
                        break
                    time.sleep(0.3)
            else:
                games_completed += 1
            stats()
            time.sleep(5)
        else:
            time.sleep(0.4)

# on/off switch with f2 and f3 keys
def toggle_switch(key):
    global running_flag, total_time
    if key == ON_switch:
        running_flag = not running_flag
        if running_flag:
            print(f"Script started...".ljust(60), end="\r")
            auto_f11()
        if not running_flag:
            print(f"Script paused...".ljust(60), end="\r")
            pydirectinput.keyUp('w')
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('s')
            pydirectinput.keyUp('d')
    elif key == OFF_switch:
        print(f"Script stopped".ljust(60), end="\r")
        elapsed_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_time.split(":"))))
        running_flag = False
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('a')
        pydirectinput.keyUp('s')
        pydirectinput.keyUp('d')
        if elapsed_seconds >= 3600:
            message = (
                f"Hello!\n\n"
                f"You have been using this macro for {total_time} hour(s).\n\n"
                f"These macros take me a long time to make, so I'd be grateful if you left a tip :)"
            )
            result = ctypes.windll.user32.MessageBoxW(
                0,
                message,
                "Thank you!",
                0x1044
            )
            if result == 6:
                import webbrowser
                webbrowser.open("https://ko-fi.com/lisek_guy2/tip")

        sys.exit()
    elif key == TIME_switch:
        print(f"Time elapsed: {total_time}")
    elif key == DEBUG_switch:
        print("Setting up Discord webhook...")
        webhook_thread = threading.Thread(target=webhook_input, daemon=True)
        webhook_thread.start()

with keyboard.Listener(on_press=toggle_switch) as listener:
    action_thread = threading.Thread(target=action_loop)
    action_thread.daemon = True
    action_thread.start()
    listener.join()