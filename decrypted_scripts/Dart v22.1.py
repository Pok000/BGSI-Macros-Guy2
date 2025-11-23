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
import mss
import pygetwindow as gw
import win32gui, win32con, win32api
from pywinauto import Application
import tkinter as tk
from tkinter import ttk
# DESCRIPTION: NUKES all the balloons in the dart minigame
# VERSIONS: all

version = "v22.1"

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

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
if screen_width == 2560 and screen_height == 1440:
    claim = ['claim800.png']
    skip = ['skip800.png', 'skip_hover.png']
    insane = ['insane800.png']
elif screen_width == 1920 and screen_height == 1080:
    claim = ['claim8002.png']
    skip = ['skip8002.png']
    insane = ['insane8002.png']
elif screen_width in [1366, 1364] and screen_height == 768:
    claim = ['claim8003.png']
    skip = ['skip8003.png']
    insane = ['insane8003.png']
else:
    print('Your resolution isn\'t 2560x1440, 1920x1080 or 1366x768 (possibly lower/higher)\nPlease select the 1366x768 resolution in the launcher and redownload the macro\nfor it to correctly work.')
    claim = ['claim8003.png']
    skip = ['skip8003.png']
    insane = ['insane8003.png']

top_left = (30, 150)
bottom_right = (800, 650)
absolute_bottom_right = (800, 660)
insane_btn = (404, 514)
game_run = (730, 95)
center = (400, 323)
hard = (251, 506)
freeze = (694, 15)
nuke = [(403, 630), (575, 630), (237, 630), (726, 630), (106, 630)]
find_btn_tl = (155, 392)
find_btn_br = (479, 533)
exit_gui = (652, 166)
settings = (208, 323)
jump_adjust = (461, 339)
tab_close = (495, 104)
settings_exit = (584, 198)
claim_backup = (329, 474)

print = functools.partial(print, flush=True)
pydirectinput.FAILSAFE = False

TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3

running_flag = False
total_time = ""
minigame = 0
warning_window = None
consecutive_runs = 0
no_detection_runs = 0
monitoring_mode = False
monitoring_games = 0
stop_adjusting = False
second_no_detection_phase = False
balloons = [
    (0, 210, 0),
    (183, 0, 251),
    (0, 232, 232)
]
white = (255, 255, 255)
gray = (61, 59, 57)
game_menu_col = (246, 111, 199)
adjust = 30
quick_fix = 0

def create_warning_window():
    global warning_window, running_flag
    
    def run_warning():
        warning_window = tk.Tk()
        warning_window.title("IMPORTANT WARNING")
        warning_window.geometry("400x300+820+50")
        warning_window.configure(bg='white')
        warning_window.attributes('-topmost', True)
        warning_window.resizable(False, False)

        def start_move(event):
            warning_window.x = event.x
            warning_window.y = event.y

        def stop_move(event):
            warning_window.x = None
            warning_window.y = None

        def do_move(event):
            if hasattr(warning_window, 'x') and warning_window.x is not None:
                deltax = event.x - warning_window.x
                deltay = event.y - warning_window.y
                x = warning_window.winfo_x() + deltax
                y = warning_window.winfo_y() + deltay
                warning_window.geometry(f"+{x}+{y}")

        warning_window.bind('<Button-1>', start_move)
        warning_window.bind('<ButtonRelease-1>', stop_move)
        warning_window.bind('<B1-Motion>', do_move)

        warning_label = tk.Label(
            warning_window,
            text="⚠️ WARNING ⚠️\n\nThis macro is supposed to\nFREEZE your game when\nentering the minigame!",
            font=("Arial", 14, "bold"),
            fg="red",
            bg="white",
            justify="center",
            padx=20,
            pady=20
        )
        warning_label.pack(expand=True, fill='both')

        warning_label.bind('<Button-1>', start_move)
        warning_label.bind('<ButtonRelease-1>', stop_move)
        warning_label.bind('<B1-Motion>', do_move)
        warning_window.lift()
        warning_window.focus_force()
        try:
            while not running_flag:
                if warning_window:
                    warning_window.update()
                time.sleep(0.01)
        except (tk.TclError, RuntimeError):
            pass
        finally:
            if warning_window:
                try:
                    warning_window.destroy()
                except:
                    pass
    
    warning_thread = threading.Thread(target=run_warning, daemon=True)
    warning_thread.start()
    time.sleep(0.5)

def setup_roblox_window():
    rblx = [w for w in gw.getWindowsWithTitle('Roblox') if w.title == 'Roblox']
    if len(rblx) != 1:
        print("More than 1 roblox game running or no Roblox window found close all other instances" if len(rblx) > 1 else "No Roblox window found")
        return False
    
    try:
        window = rblx[0]
        hwnd = window._hWnd
        win32gui.SetForegroundWindow(hwnd)

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        if not (style & win32con.WS_CAPTION):
            Application().connect(handle=hwnd).window(handle=hwnd).type_keys('{F11}')
            time.sleep(1)

        new_style = win32con.WS_OVERLAPPEDWINDOW
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)

        rect = win32gui.GetClientRect(hwnd)
        window_rect = win32gui.GetWindowRect(hwnd)
        border_height = (window_rect[3] - window_rect[1]) - (rect[3] - rect[1])
        
        total_width = 800
        total_height = 630 + border_height

        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOP,
            0, 0,
            total_width, total_height,
            win32con.SWP_SHOWWINDOW
        )
        return True
        
    except Exception as e:
        print(f"Error setting up Roblox window: {e}")
        return False

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
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    bgr_color = img[coords[1], coords[0]]
    target_color_bgr = (target_color[2], target_color[1], target_color[0])
    diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
    return np.all(diff <= tolerance)

def detect_color2(target_colors, area, tolerance=10, step=5):
    screenshot = ImageGrab.grab(bbox=area)
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    for y in range(0, img.shape[0], step):
        for x in range(0, img.shape[1], step):
            pixel = img[y, x]
            for color in target_colors:
                target_bgr = (color[2], color[1], color[0])
                diff = np.abs(np.array(pixel, dtype=int) - np.array(target_bgr, dtype=int))
                if np.all(diff <= tolerance):
                    absolute_x = area[0] + x
                    absolute_y = area[1] + y
                    return (absolute_x, absolute_y)
    return None

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

cls()
difficulty = input("1 - HARD MODE\n2 - INSANE MODE\n\nChoose difficulty: ")
if difficulty not in ['1', '2']:
    ans = 2
else:
    ans = int(difficulty)

cls()
print(f'Auto Dart v{version} by Lisek_guy2\n')
if not setup_roblox_window():
    print("Failed to setup Roblox window. Please make sure only 1 Roblox instance is running.")
    input("Press Enter to continue anyway...")

create_warning_window()
print("Macro running correctly\nTo start press F2, to stop press F3")

def action_loop():
    global minigame, center, adjust, running_flag, quick_fix, consecutive_runs
    global no_detection_runs, monitoring_mode, monitoring_games, stop_adjusting, second_no_detection_phase
    while True:
        if not running_flag:
            time.sleep(0.25)
        else:
            if not detect_color(game_run, (255, 255, 255), 5):
                move(center[0], 300)
                timeout = time.time() + 15
                while time.time() < timeout:
                    found_claim = image(top_left, absolute_bottom_right, claim[0])
                    if found_claim:
                        minigame += 1
                        move(*found_claim)
                        pydirectinput.press('space')
                        time.sleep(0.5)
                    found_skip = image(find_btn_tl, find_btn_br, skip[0])
                    if found_skip:
                        move(found_skip[0] + 6, found_skip[1])
                        cls()
                        print(f'Auto Dart {version} by Lisek_guy2\n\nTotal Playtime: {total_time}\nGames won: {minigame}\nWait period: {adjust} seconds')
                        time.sleep(0.4)
                    found_insane = image(find_btn_tl, find_btn_br, insane[0])
                    if found_insane:
                        if ans == 1:
                            move(*hard)
                        else:
                            move(*found_insane)
                            quick_fix = 0
                        time.sleep(0.2)
                        if ans == 1:
                            move(*hard)
                        else:
                            move(*insane_btn)
                            quick_fix = 0
                        break
                else:
                    print('Issue found, attempting to fix...')
                    quick_fix += 1
                    if quick_fix == 1:
                        nomove(*claim_backup)
                        time.sleep(0.1)
                        nomove(*center)
                        continue
                    if quick_fix >= 2:
                        move(*tab_close)
                        time.sleep(0.5)
                        move(*exit_gui)
                        time.sleep(0.5)
                        move(*settings)
                        time.sleep(0.5)
                        if quick_fix == 2:
                            move(*jump_adjust)
                            time.sleep(0.5)
                            move(*settings_exit)
                            pydirectinput.press('space')
                            time.sleep(1)
                            continue
                        elif quick_fix == 3:
                            move(jump_adjust[0] + 10, jump_adjust[1])
                            time.sleep(0.5)
                            move(*settings_exit)
                            pydirectinput.press('space')
                            time.sleep(1.5)
                            continue
                    elif quick_fix == 4:
                        print('Quick fixes failed, dude i have no idea what happened')
                        continue

            pydirectinput.click()
            nomove(*freeze)
            pydirectinput.mouseDown(button='right')
            time.sleep(adjust)
            pydirectinput.mouseUp(button='right')
            time.sleep(0.3)
            move(*center)
            for idx in nuke:
                move(*idx)
                time.sleep(0.25)
            balloon_detected = False
            while detect_color(game_run, (255, 255, 255), 5):
                pydirectinput.mouseDown()
                coords = detect_color2(balloons, (top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
                if coords:
                    nomove(coords[0], coords[1] - 40)
                balloon_detected = True

            if not stop_adjusting:
                if balloon_detected:
                    if monitoring_mode:
                        if adjust < 38:
                            adjust += 1
                        monitoring_games = 0
                    elif second_no_detection_phase:
                        if adjust < 38:
                            adjust += 1
                        monitoring_mode = True
                        monitoring_games = 0
                        second_no_detection_phase = False
                    else:
                        consecutive_runs += 1
                        if consecutive_runs >= 2 and adjust < 38:
                            adjust += 1
                            consecutive_runs = 0
                    no_detection_runs = 0
                else:
                    consecutive_runs = 0
                    no_detection_runs += 1
                    if no_detection_runs >= 3:
                        if second_no_detection_phase:
                            stop_adjusting = True
                        elif monitoring_mode:
                            monitoring_mode = False
                            second_no_detection_phase = True
                            no_detection_runs = 0
                        else:
                            adjust = max(20, adjust - 0.5)
                            no_detection_runs = 0

                if monitoring_mode:
                    monitoring_games += 1
                    if monitoring_games >= 4:
                        stop_adjusting = True
                        monitoring_mode = False
            
            time.sleep(0.05)
            if not running_flag:
                break
        pydirectinput.mouseUp()

def toggle_switch(key):
    global running_flag, total_time, warning_window
    if key == ON_switch:
        running_flag = not running_flag
        if running_flag:
            print(f"Script started...".ljust(60), end="\r")
        if not running_flag:
            pydirectinput.mouseUp()
            pydirectinput.mouseUp(button='right')
            print(f"Script paused...".ljust(60), end="\r")
    elif key == OFF_switch:
        print(f"Script stopped".ljust(60), end="\r")
        running_flag = False
        pydirectinput.mouseUp()
        pydirectinput.mouseUp(button='right')
        elapsed_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_time.split(":"))))
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
        os._exit(0)
    elif key == TIME_switch:
        print(f"Time elapsed: {total_time}")

try:
    with keyboard.Listener(on_press=toggle_switch) as listener:
        action_thread = threading.Thread(target=action_loop)
        action_thread.daemon = True
        action_thread.start()
        listener.join()
except KeyboardInterrupt:
    running_flag = True
    os._exit(0)