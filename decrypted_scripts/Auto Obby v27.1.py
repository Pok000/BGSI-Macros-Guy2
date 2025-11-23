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
import pygetwindow as gw
import win32gui, win32con, win32api
from pywinauto import Application
import pyautogui

version = "v27.1"
# DESCRIPTION: Auto completes easy, medium and hard obbies
# VERSIONS: all

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
    leave = (1167, 854)
    leave_col = (214, 62, 196)
    chest_close = (1278, 853)
    chest_close_col = (193, 15, 77)
    minigame_cooldown = (1279, 856)
    minigame_cooldown_col = (189, 12, 77)
    fail = (1084, 94)
    daily = (68, 695)
    start = (1172, 1012)
    walk = (1279, 1037)
    walk2 = (1159, 851)
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    center = (960, 540)
    leave = (861, 658)
    leave_col = (213, 60, 195)
    chest_close = (960, 659)
    chest_close_col = (189, 11, 77)
    minigame_cooldown = (960, 657)
    minigame_cooldown_col = (191, 14, 77)
    fail = (796, 82)
    daily = (59, 514)
    start = (867, 793)
    walk = (959, 785)
    walk2 = (873, 641)
elif screen_width in [1366, 1364] and screen_height == 768:
    res_info = 1366
    center = (683, 384)
    leave = (607, 476)
    leave_col = (212, 60, 194)
    chest_close = (686, 475)
    chest_close_col = (191, 13, 77)
    minigame_cooldown = (683, 475)
    minigame_cooldown_col = (191, 13, 77)
    fail = (557, 63)
    daily = (47, 362)
    start = (610, 581)
    walk = (682, 558)
    walk2 = (621, 458)
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

# others
running_flag = False    
total_time = ""
daily_col = (238, 50, 94)
selected_obby = 1
open_chest = True
easy_cooldown_end = 0
medium_cooldown_end = 0
hard_cooldown_end = 0
current_difficulty = None
EASY_COOLDOWN = 175
MEDIUM_COOLDOWN = 290
HARD_COOLDOWN = 575
fail_col = (221, 46, 68)
minigames = 0
cam_pos = False

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

def start_cooldown(difficulty):
    global easy_cooldown_end, medium_cooldown_end, hard_cooldown_end
    current_time = time.time()
    
    if difficulty == "easy":
        easy_cooldown_end = current_time + EASY_COOLDOWN
    elif difficulty == "medium":
        medium_cooldown_end = current_time + MEDIUM_COOLDOWN
    elif difficulty == "hard":
        hard_cooldown_end = current_time + HARD_COOLDOWN

def get_cooldown(difficulty):
    global easy_cooldown_end, medium_cooldown_end, hard_cooldown_end
    current_time = time.time()
    
    if difficulty == "easy":
        return max(0, easy_cooldown_end - current_time)
    elif difficulty == "medium":
        return max(0, medium_cooldown_end - current_time)
    elif difficulty == "hard":
        return max(0, hard_cooldown_end - current_time)
    return 0

def cooldown_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def cooldown_print(in_waiting_area=False):
    easy_remaining = get_cooldown("easy")
    medium_remaining = get_cooldown("medium")
    hard_remaining = get_cooldown("hard")
    
    status = f"Cooldowns - Easy: {cooldown_time(easy_remaining)} | Medium: {cooldown_time(medium_remaining)} | Hard: {cooldown_time(hard_remaining)}"
    
    if current_difficulty:
        status += f" | Currently doing {current_difficulty.title()} mode obby"
    elif in_waiting_area:
        status += f" | Hatching while waiting"
    print(f"{status}".ljust(60), end="\r", flush=True)

def cooldown_remain():
    return [
        get_cooldown("easy"),
        get_cooldown("medium"), 
        get_cooldown("hard")
    ]

def cooldown_above(seconds):
    return all(remaining > seconds for remaining in cooldown_remain())

def any_cooldown_above_seconds(seconds):
    return any(remaining > seconds for remaining in cooldown_remain())

def hatch():
    pydirectinput.keyDown('a')
    time.sleep(0.3)
    pydirectinput.keyUp('a')
    pydirectinput.keyDown('w')
    time.sleep(2.6)
    pydirectinput.keyUp('w')
    pydirectinput.keyDown('d')
    time.sleep(0.3)
    pydirectinput.keyUp('d')

def hatch_end():
    while not detect_color(daily, daily_col, 10):
        time.sleep(1)
    time.sleep(3)
    statistics()
    pydirectinput.keyDown('a')
    time.sleep(0.3)
    pydirectinput.keyUp('a')
    pydirectinput.keyDown('s')
    time.sleep(2.6)
    pydirectinput.keyUp('s')
    pydirectinput.keyDown('d')
    time.sleep(0.3)
    pydirectinput.keyUp('d')

def get_available_difficulty():
    if current_difficulty is not None:
        return None
    if selected_obby == 1:
        if get_cooldown("easy") == 0:
            return "easy"
        elif get_cooldown("medium") == 0:
            return "medium"
        elif get_cooldown("hard") == 0:
            return "hard"
    elif selected_obby == 2:
        if get_cooldown("medium") == 0:
            return "medium"
        elif get_cooldown("hard") == 0:
            return "hard"
    
    return None

# clearing the cmd
def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def move(target_x, target_y):
    pydirectinput.moveTo(target_x + 4, target_y + 4)
    ahk.mouse_move(target_x, target_y)
    pydirectinput.click(target_x, target_y)

def nomove(x, y):
    ahk.mouse_move(x, y)

def rmove(x, y):
    pydirectinput.moveTo(x + 4, y + 4)
    ahk.mouse_move(x, y)
    pydirectinput.rightClick()

def detect_color(coords, target_color, tolerance=20):
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    bgr_color = img[coords[1], coords[0]]
    target_color_bgr = (target_color[2], target_color[1], target_color[0])
    diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
    return np.all(diff <= tolerance)

def scroll(direction, amount):
    if direction == 'up':
        pyautogui.scroll(amount)
    elif direction == 'down':
        pyautogui.scroll(-amount)

def align_camera():
    nomove(*center)
    time.sleep(0.1)
    pydirectinput.mouseDown(button='right')
    nomove(center[0], center[1] + 100)
    pydirectinput.mouseUp(button='right')
    scroll('down', 1000)

def easy_obby():
    global open_chest
    nomove(*walk)
    pydirectinput.rightClick()
    time.sleep(3.3)
    pydirectinput.keyDown('d')
    time.sleep(0.503)
    pydirectinput.keyUp('d')
    pydirectinput.keyDown('s')
    time.sleep(0.539)
    pydirectinput.keyUp('s')
    pydirectinput.keyDown('a')
    time.sleep(0.372)
    pydirectinput.keyUp('a')
    pydirectinput.keyDown('s')
    time.sleep(0.452)
    pydirectinput.keyUp('s')
    pydirectinput.keyDown('a')
    time.sleep(1.099)
    pydirectinput.keyUp('a')
    pydirectinput.keyDown('s')
    time.sleep(0.782)
    pydirectinput.keyUp('s')
    pydirectinput.keyDown('d')
    time.sleep(0.401)
    pydirectinput.keyUp('d')
    time.sleep(0.2)
    nomove(*walk2)
    pydirectinput.rightClick()
    time.sleep(3.5)
    if detect_color(fail, fail_col, 10):
        print("Easy obby failed, retrying...")
        return
    elif open_chest:
        start_time = time.time()
        while time.time() - start_time <= 60:
            pydirectinput.press('e')
            if detect_color(chest_close, chest_close_col, 10):
                move(*chest_close)
                for _ in range(3):
                    pydirectinput.click()
                break
            time.sleep(0.25)
    pydirectinput.keyDown('d')
    time.sleep(1)
    pydirectinput.keyUp('d')

def medium_obby():
    global open_chest
    pydirectinput.keyDown('s')
    time.sleep(0.15)
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.4)
    pydirectinput.keyUp('s')
    time.sleep(0.2)
    pydirectinput.keyDown('d')
    time.sleep(0.13)
    pydirectinput.keyUp('d')
    pydirectinput.keyDown('s')
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.35)
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.1)
    pydirectinput.keyUp('s')
    time.sleep(0.4)
    pydirectinput.keyDown('s')
    time.sleep(0.08)
    pydirectinput.keyUp('s')
    pydirectinput.keyDown('d')
    time.sleep(0.39)
    pydirectinput.keyUp('d')
    time.sleep(0.15)
    pydirectinput.keyDown('s')
    time.sleep(0.1)
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.3)
    pydirectinput.keyUp('s')
    time.sleep(0.3)
    pydirectinput.keyDown('a')
    time.sleep(0.1)
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.05)
    pydirectinput.keyUp('a')
    time.sleep(0.2)
    pydirectinput.keyDown('a')
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.15)
    pydirectinput.keyUp('a')
    time.sleep(0.5)
    pydirectinput.keyDown('s')
    time.sleep(1)
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.1)
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.1)
    pydirectinput.keyUp('s')
    pydirectinput.keyDown('s')
    time.sleep(0.15)
    pydirectinput.keyUp('s')
    pydirectinput.keyDown('d')
    time.sleep(0.08)
    pydirectinput.keyDown('space')
    pydirectinput.keyUp('space')
    time.sleep(0.9)
    pydirectinput.keyUp('d')
    time.sleep(1)
    if detect_color(fail, fail_col, 10):
        print("Medium obby failed, retrying...")
        return
    elif open_chest:
        start_time = time.time()
        while time.time() - start_time <= 60:
            pydirectinput.press('e')
            if detect_color(chest_close, chest_close_col, 10):
                move(*chest_close)
                for _ in range(3):
                    pydirectinput.click()
                break
            time.sleep(0.25)
    pydirectinput.keyDown('w')
    time.sleep(1)
    pydirectinput.keyUp('w')

def hard_obby():
    global open_chest
    pydirectinput.keyDown('s')
    time.sleep(0.05)
    pydirectinput.keyDown('space')
    time.sleep(0.1)
    pydirectinput.keyUp('s')
    time.sleep(0.3)
    pydirectinput.keyDown('s')
    time.sleep(0.05)
    pydirectinput.keyUp('space')
    time.sleep(0.2)
    pydirectinput.keyUp('s')
    time.sleep(0.3)
    pydirectinput.keyDown('s')
    pydirectinput.press('space')
    time.sleep(0.3)
    pydirectinput.keyUp('s')
    pydirectinput.keyDown('space')
    pydirectinput.keyDown('a')
    time.sleep(0.2)
    pydirectinput.keyUp('space')
    pydirectinput.keyUp('a')
    time.sleep(0.3)
    pydirectinput.keyDown('s')
    time.sleep(2)
    pydirectinput.keyUp('s')
    time.sleep(0.143)
    pydirectinput.keyUp('s')
    if detect_color(fail, fail_col, 10):
        print("Hard obby failed, retrying...")
        return
    elif open_chest:
        start_time = time.time()
        while time.time() - start_time <= 60:
            pydirectinput.press('e')
            if detect_color(chest_close, chest_close_col, 10):
                move(*chest_close)
                for _ in range(3):
                    pydirectinput.click()
                break
            time.sleep(0.25)
    time.sleep(0.330)
    pydirectinput.keyDown('d')
    time.sleep(0.7)
    pydirectinput.keyUp('d')

def walk_easy():
    pydirectinput.keyDown('d')
    time.sleep(0.453)
    pydirectinput.keyUp('d')
    pydirectinput.keyDown('s')
    time.sleep(0.454)
    pydirectinput.keyUp('s')
    time.sleep(0.5)
    if detect_color(minigame_cooldown, minigame_cooldown_col, 10):
        move(*minigame_cooldown)
        global easy_cooldown_end
        easy_cooldown_end = time.time() + 60
        pydirectinput.keyDown('w')
        time.sleep(0.454)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('a')
        time.sleep(0.453)
        pydirectinput.keyUp('a')
        return False
    else:
        move(*start)
        time.sleep(3)
        return True

def walk_normal():
    pydirectinput.keyDown('s')
    time.sleep(0.454)
    pydirectinput.keyUp('s')
    time.sleep(0.5)
    if detect_color(minigame_cooldown, minigame_cooldown_col, 10):
        move(*minigame_cooldown)
        global medium_cooldown_end
        medium_cooldown_end = time.time() + 60
        pydirectinput.keyDown('w')
        time.sleep(0.454)
        pydirectinput.keyUp('w')
        return False
    else:
        move(*start)
        time.sleep(3)
        return True

def walk_hard():
    pydirectinput.keyDown('a')
    time.sleep(0.453)
    pydirectinput.keyUp('a')
    pydirectinput.keyDown('s')
    time.sleep(0.454)
    pydirectinput.keyUp('s')
    time.sleep(0.5)
    if detect_color(minigame_cooldown, minigame_cooldown_col, 10):
        move(*minigame_cooldown)
        global hard_cooldown_end
        hard_cooldown_end = time.time() + 60
        pydirectinput.keyDown('w')
        time.sleep(0.454)
        pydirectinput.keyUp('w')
        pydirectinput.keyDown('d')
        time.sleep(0.453)
        pydirectinput.keyUp('d')
        return False
    else:
        move(*start)
        time.sleep(3)
        return True

def settings():
    global selected_obby, open_chest, easy_cooldown_end
    print("What obby do you want to do?\n   1. All (default)\n   2. Skip Easy\n")
    while True:
        obby_choice = input("Enter your choice (1-2, press Enter for default): ").strip()
        
        if obby_choice == "":
            selected_obby = 1
            break
        elif obby_choice in ["1", "2"]:
            selected_obby = int(obby_choice)
            if selected_obby == 2:
                easy_cooldown_end = time.time() + 31536000
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    cls()

    print("Do you want to open the chest at the end of the obby? (yes or no)\n")
    while True:
        chest_choice = input("Enter your choice, press Enter for default: ").strip().lower()
        
        if chest_choice == "" or chest_choice in ["y", "yes"]:
            open_chest = True
            break
        elif chest_choice in ["n", "no"]:
            open_chest = False
            break
        else:
            print("Invalid choice. Please enter yes or no.")
    cls()

def statistics():
    cls()
    print(f"Statistics:\n\nTotal time spent: {total_time}\nGames completed: {minigames}\n\n")
    
cls()
settings()
print(f'Auto Obby {version} by Lisek_guy2\n\nMacro running correctly\nTo start press F2, to stop press F3')
def action_loop():
    global running_flag, selected_obby, open_chest, current_difficulty, minigames
    while True:
        if running_flag:
            cooldown_print()
            available_difficulty = get_available_difficulty()
            
            if available_difficulty:
                current_difficulty = available_difficulty
                # if not cam_pos:
                #     align_camera()
                #     time.sleep(1)

                if available_difficulty == "easy":
                    if walk_easy():
                        start_cooldown("easy")
                        
                        while True:
                            scroll('down', 1000)
                            time.sleep(0.5)
                            easy_obby()
                            time.sleep(0.5)
                            if detect_color(leave, leave_col, 10):
                                move(*leave)
                                minigames += 1
                                statistics()
                                time.sleep(2)
                                break
                            else:
                                pydirectinput.keyDown('a')
                                time.sleep(1)
                                pydirectinput.keyUp('a')
                                time.sleep(1)
                                pydirectinput.keyDown('a')
                                time.sleep(0.5)
                                pydirectinput.keyUp('a')
                                time.sleep(1)
                
                elif available_difficulty == "medium":
                    if walk_normal():
                        start_cooldown("medium")
                        
                        while True:
                            scroll('down', 1000)
                            time.sleep(0.5)
                            medium_obby()
                            time.sleep(0.5)
                            if detect_color(leave, leave_col, 10):
                                move(*leave)
                                minigames += 1
                                statistics()
                                time.sleep(2)
                                break
                            else:
                                pydirectinput.keyDown('a')
                                time.sleep(1)
                                pydirectinput.keyUp('a')
                                time.sleep(1)
                                pydirectinput.keyDown('a')
                                time.sleep(0.5)
                                pydirectinput.keyUp('a')
                                time.sleep(1)
                
                elif available_difficulty == "hard":
                    if walk_hard():
                        start_cooldown("hard")
                        
                        while True:
                            scroll('down', 1000)
                            time.sleep(0.5)
                            hard_obby()
                            time.sleep(0.5)
                            if detect_color(leave, leave_col, 10):
                                move(*leave)
                                minigames += 1
                                statistics()
                                time.sleep(2)
                                break
                            else:
                                pydirectinput.keyDown('a')
                                time.sleep(1)
                                pydirectinput.keyUp('a')
                                time.sleep(1)
                                pydirectinput.keyDown('a')
                                time.sleep(0.5)
                                pydirectinput.keyUp('a')
                                time.sleep(1)

                current_difficulty = None
            else:
                if cooldown_above(10):
                    hatch()
                    status_upd = 0
                    while cooldown_above(5) and running_flag:
                        pydirectinput.press('e')
                        current_time = time.time()
                        if current_time - status_upd >= 1.0:
                            cooldown_print(in_waiting_area=True)
                            status_upd = current_time
                        time.sleep(0.25)
                    if running_flag:
                        hatch_end()
                else:
                    time.sleep(1)
        else:
            time.sleep(0.4)

# on/off switch with f2 and f3 keys
def toggle_switch(key):
    global running_flag, total_time
    if key == ON_switch:
        running_flag = not running_flag
        if running_flag:
            print(f"Script started...".ljust(80), end="\r")
            auto_f11()
        if not running_flag:
            print(f"Script paused...".ljust(80), end="\r")
    elif key == OFF_switch:
        print(f"Script stopped".ljust(80), end="\r")
        elapsed_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_time.split(":"))))
        running_flag = False
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

with keyboard.Listener(on_press=toggle_switch) as listener:
    action_thread = threading.Thread(target=action_loop)
    action_thread.daemon = True
    action_thread.start()
    listener.join()