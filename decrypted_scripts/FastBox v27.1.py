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

# VERSIONS: all
# DESCRIPTION: Opens 75 mystery boxes at once
version = "v27.1"

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
    use = (800, 965)
    use12 = (1238, 836)
    use25 = (1535, 839)
    pet_present_check = (2475, 1347)
elif screen_width == 1920 and screen_height == 1080:
    use = (540, 751)
    use12 = (925, 638)
    use25 = (1186, 643)
    pet_present_check = (1848, 1002)
elif screen_width in [1366, 1364] and screen_height == 768:
    use = (359, 546)
    use12 = (655, 463)
    use25 = (857, 464)
    pet_present_check = (1311, 708)
else:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"Please either use 2560x1440 or 1920x1080 resolution and set your scale to 100% for this macro to work.\nCurrent resolution: {screen_width}x{screen_height}",
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

# global names
TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3

# others
running_flag = False    
total_time = ""
pet_color1 = (70, 2, 27)
pet_color2 = (35, 1, 13)
box_count = 0
time_avg = None

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

def move(target_x, target_y):
    pydirectinput.moveTo(target_x, target_y)
    ahk.mouse_move(target_x + 4, target_y + 4)
    pydirectinput.click()

def nomove(target_x, target_y):
    pydirectinput.moveTo(target_x, target_y)
    ahk.mouse_move(target_x + 4, target_y + 4)

def detect_color(coords, target_color, tolerance=20):
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    bgr_color = img[coords[1], coords[0]]
    target_color_bgr = (target_color[2], target_color[1], target_color[0])
    diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
    return np.all(diff <= tolerance)

cls()
print(f'FastBox {version} by Lisek_guy2\nMacro running correctly\nTo start press F2, to stop press F3')
def action_loop():
    global delay, box_count
    while True:
        if not running_flag:
            time.sleep(0.4)
        else:
            move(*use)
            move(*use12)
            pydirectinput.keyDown('f')
            pydirectinput.keyUp('f')
            move(*use)
            move(*use25)
            #time.sleep(0.3) # in case of high ping - remove the "#" symbol before time.sleep(0.3) if you want delay (keyword to find this line: bonus delay)
            for _ in range(14):
                pydirectinput.click()
                time.sleep(0.06)
            pydirectinput.keyDown('f')
            pydirectinput.keyUp('f')
            box_count += 75
            minutes = (time.time() - time_avg) / 60
            average = box_count / minutes if minutes > 0 else 0
            print(f"{box_count} boxes opened in {total_time} with an average of {average:.2f} boxes per minute".ljust(60), end="\r")
            if not detect_color(pet_present_check, pet_color1) and not detect_color(pet_present_check, pet_color2):
                pydirectinput.keyDown('shift')
                pydirectinput.keyDown('l')
                pydirectinput.keyUp('l')
                pydirectinput.keyUp('shift')
                pydirectinput.keyDown('f')
                pydirectinput.keyUp('f')

# on/off switch with f2 and f3 keys
def toggle_switch(key):
    global running_flag, total_time, time_avg
    if key == ON_switch:
        running_flag = not running_flag
        if running_flag:
            print(f"Script started...".ljust(60), end="\r")
            if time_avg is None:
                time_avg = time.time()
            auto_f11()
        if not running_flag:
            print(f"Script paused...".ljust(60), end="\r")
    elif key == OFF_switch:
        print(f"Script stopped".ljust(60), end="\r")
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
