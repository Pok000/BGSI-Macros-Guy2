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
import gc
# DESCRIPTION: Fishes fish in fishing simulator infinity (bgsi)
# VERSIONS: all

version = "v17.1"

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

res_info = 0
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
if screen_width == 2560 and screen_height == 1440:
    res_info = 2560
    fish = (909, 988)
    rod = (2476, 1220) #
    fish_top = (899, 495)
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    fish = (749, 782)
    rod = (1846, 886) #
    fish_top = (721, 344)
elif screen_width in [1366, 1364] and screen_height == 768:
    res_info = 1920
    fish = (556, 571)
    rod = (1310, 619) #
    fish_top = (537, 232)
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

TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3

running_flag = False    
total_time = ""
white = (255, 255, 255)
rod_col = (199, 27, 4)
fish_color = (18, 180, 242)
cycle_count = 0
e_thread = None

def format_time_ignore(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def update_session_time_ignore():
    global total_time
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        total_time = format_time_ignore(elapsed_time)
        time.sleep(1)

session_time_thread = threading.Thread(target=update_session_time_ignore, daemon=True)
session_time_thread.start()

def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def move(target_x, target_y):
    ahk.mouse_move(target_x, target_y)
    pydirectinput.click(target_x, target_y)

def nomove(x, y):
    ahk.mouse_move(x, y)

def detect_color(coords, target_color, tolerance=20):
    x, y = coords
    bbox = (x-5, y-5, x+5, y+5)
    screenshot = ImageGrab.grab(bbox)
    pixel_color = screenshot.getpixel((5, 5))
    
    diff = abs(pixel_color[0] - target_color[0]) + \
           abs(pixel_color[1] - target_color[1]) + \
           abs(pixel_color[2] - target_color[2])
    
    return diff <= tolerance * 3

def open_egg():
    while True:
        if running_flag:
            pydirectinput.press('r')
        time.sleep(0.01)

cls()
print("What would you like to do?\n1 - Only Fish\n2 - Hatch and Fish (you must position yourself)")
while True:
    try:
        choice = int(input("\nEnter your choice (1 or 2): "))
        if choice == 1:
            print("You chose Option 1.")
            break
        elif choice == 2:
            print("You chose Option 2.")
            e_thread = threading.Thread(target=open_egg, daemon=True)
            e_thread.start()
            break
        else:
            print("Please enter either 1 or 2.")
    except ValueError:
        print("Please enter either 1 or 2.")

cls()
print(f'AutoFish {version} by Lisek_guy2\n\nMacro running correctly\nTo start press F2, to stop press F3')
def action_loop():
    global cycle_count
    while True:
        if not running_flag:
            time.sleep(0.4)
        else:
            cycle_count += 1
            if cycle_count % 100 == 0:
                gc.collect()
                
            if choice == 1:
                pydirectinput.mouseDown()
                time.sleep(0.25)
                pydirectinput.mouseUp()
                no_afk = time.time() + 15
                while not detect_color(rod, rod_col, 15) and time.time() < no_afk and running_flag:
                    pydirectinput.mouseDown()
                    if not detect_color(fish, white):
                        time.sleep(0.1)
                    else:
                        pydirectinput.mouseUp()
                        for _ in range(2):
                            pydirectinput.click()
                        pydirectinput.mouseDown()
                        if detect_color(fish, white):
                            pydirectinput.mouseUp()
                        pydirectinput.mouseDown()
                else:
                    pydirectinput.mouseUp()
                    time.sleep(0.1)
            elif choice == 2:
                pydirectinput.mouseDown()
                time.sleep(0.25)
                pydirectinput.mouseUp()
                no_afk = time.time() + 15
                while not detect_color(fish_top, fish_color, 15) and time.time() < no_afk and running_flag:
                    pydirectinput.mouseDown()
                    if not detect_color(fish, white):
                        time.sleep(0.1)
                    else:
                        pydirectinput.mouseUp()
                        for _ in range(2):
                            pydirectinput.click()
                        pydirectinput.mouseDown()
                        if detect_color(fish, white):
                            pydirectinput.mouseUp()
                        pydirectinput.mouseDown()
                else:
                    time.sleep(0.2)
                    pydirectinput.mouseUp()
                    time.sleep(0.1)

def toggle_switch(key):
    global running_flag, total_time
    if key == ON_switch:
        running_flag = not running_flag
        if running_flag:
            print(f"Script started...".ljust(60), end="\r")
            auto_f11()
        if not running_flag:
            print(f"Script paused...".ljust(60), end="\r")
    elif key == OFF_switch:
        print(f"Script stopped".ljust(60), end="\r")
        elapsed_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_time.split(":"))))
        pydirectinput.mouseUp()
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