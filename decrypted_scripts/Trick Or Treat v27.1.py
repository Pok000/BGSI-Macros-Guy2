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
import tkinter as tk

# DESCRIPTION: Automatic trick-or-treating
# VERSIONS: all
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
    res_info = 2560
    center = (1280, 720)
    area = {
        'top_left': (679, 430),
        'bottom_right': (2131, 1155)
    }
    min_size = 150
    exclude_radius = 150
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    center = (960, 540)
    area = {
        'top_left': (476, 362),
        'bottom_right': (1531, 773)
    }
    min_size = 100
    exclude_radius = 80
elif screen_width in [1366, 1364] and screen_height == 768:
    res_info = 1366
    center = (683, 384)
    area = {
        'top_left': (362, 229),
        'bottom_right': (1137, 616)
    }
    min_size = 50
    exclude_radius = 70
else:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"Please either use 2560x1440, 1920x1080 or 1366x768 resolution and set your scale to 100% for this macro to work.\nCurrent resolution: {screen_width}x{screen_height}",
        "Invalid resolution",
        0x10
    )
    sys.exit()

print = functools.partial(print, flush=True)

class OverlayWindow:
    def __init__(self, area_coords):
        self.area = area_coords
        self.root = None
        self.canvas = None
        self.should_close = False
        
    def run_overlay_thread(self):
        try:
            self.root = tk.Tk()
            self.root.title("Transparent Overlay")
            self.root.attributes('-topmost', True)
            self.root.overrideredirect(True)
            try:
                self.root.wm_attributes("-transparentcolor", "white")
            except:
                pass
                
            x1, y1 = self.area['top_left']
            x2, y2 = self.area['bottom_right']
            
            padding = 10
            overlay_x = x1 - padding
            overlay_y = y1 - padding
            overlay_width = (x2 - x1) + (padding * 2)
            overlay_height = (y2 - y1) + (padding * 2)
            
            self.root.geometry(f"{overlay_width}x{overlay_height}+{overlay_x}+{overlay_y}")
            
            self.canvas = tk.Canvas(self.root, bg='white', highlightthickness=0)
            self.canvas.pack(fill='both', expand=True)
            
            search_width = x2 - x1
            search_height = y2 - y1
            
            exclusion_width_percent = 0.15
            exclusion_height_percent = 0.5
            
            left_edge = padding
            right_edge = overlay_width - padding
            top_edge = padding
            bottom_edge = overlay_height - padding
            
            exclusion_right = left_edge + (search_width * exclusion_width_percent)
            exclusion_top = top_edge + (search_height * exclusion_height_percent)
            
            self.canvas.create_line(left_edge, top_edge, right_edge, top_edge, fill='lime', width=2)
            self.canvas.create_line(right_edge, top_edge, right_edge, bottom_edge, fill='lime', width=2)
            self.canvas.create_line(exclusion_right, bottom_edge, right_edge, bottom_edge, fill='lime', width=2)
            self.canvas.create_line(left_edge, top_edge, left_edge, exclusion_top, fill='lime', width=2)
            self.canvas.create_line(left_edge, exclusion_top, exclusion_right, exclusion_top, fill='lime', width=2)
            self.canvas.create_line(exclusion_right, exclusion_top, exclusion_right, bottom_edge, fill='lime', width=2)

            self.canvas.create_text(
                left_edge + 5, top_edge - 5,
                text="SEARCH AREA",
                fill='lime',
                font=('Arial', 10, 'bold'),
                anchor='sw'
            )
            
            def check_close():
                if self.should_close:
                    try:
                        self.root.quit()
                        self.root.destroy()
                    except:
                        pass
                    return
                self.root.after(100, check_close)
            
            self.root.after(100, check_close)
            
            self.root.mainloop()
            
        except Exception as e:
            print(f"Overlay thread error: {e}")
        
    def close(self):
        self.should_close = True

overlay = None
overlay_thread = None
overlay_destroyed = False

def hide_overlay():
    global overlay, overlay_destroyed
    try:
        if overlay and not overlay_destroyed:
            def close_overlay():
                overlay.close()
                overlay_destroyed = True
                print("Overlay hidden permanently")
            overlay.root.after(0, close_overlay)
    except Exception as e:
        print(f"Failed to hide overlay: {e}")

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
    time.sleep(1.5)

# global names
TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3
DEBUG_switch = keyboard.Key.f5

# others
running_flag = False    
total_time = ""
houses_visited = 0
color = (254, 134, 18)
tolerance = 5
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

log_queue = []
webhook_link = None
_lock = threading.Lock()
message_id = None
last_sent_houses = -1
def get_status_header():
    try:
        header_lines = [
            f"Houses visited: {houses_visited}",
            f"Time elapsed: {total_time}",
        ]
        return "\n".join(header_lines)
    except Exception:
        return (
            "Houses visited: 0\n"
            "Time elapsed: 00:00:00"
        )

webhook_path = os.path.join(os.path.expanduser("~"), "GUY2 Macros", "Macros", "webhook.txt")
if os.path.exists(webhook_path):
    try:
        with open(webhook_path, 'r') as file:
            webhook_link = file.read().strip()
    except Exception as e:
        print(f"Failed to read webhook file: {e}")

if webhook_link:
    webhook = True
    print(f"Webhook loaded and active: {webhook_link}")
else:
    print("No webhook loaded. Skipping webhook setup.")

def webhook_link_batch():
    global message_id, last_sent_houses

    if not webhook_link:
        return

    if message_id is None:
        try:
            initial = f"```text\n{get_status_header()}\n```"
            response = requests.post(webhook_link + "?wait=true", json={"content": initial})
            if response.status_code == 200:
                message_id = response.json()["id"]
                last_sent_houses = houses_visited
            else:
                print(f"[Webhook] Failed to send initial message: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"[Webhook] Exception sending initial message: {e}")
            return

    while True:
        time.sleep(0.5)
        with _lock:
            filtered = [line for line in log_queue if not line.startswith("Visited ")]
            log_queue.clear()
        should_update = filtered or (houses_visited != last_sent_houses)
        if not should_update:
            continue

        if filtered:
            content = f"```text\n{get_status_header()}\n\n{"\n".join(filtered)}\n```"
        else:
            content = f"```text\n{get_status_header()}\n```"

        try:
            edit_url = f"{webhook_link}/messages/{message_id}"
            response = requests.patch(edit_url, json={"content": content})
            if response.status_code not in [200, 204]:
                print(f"[Webhook] Failed to edit message: {response.status_code} - {response.text}")
            else:
                last_sent_houses = houses_visited
        except Exception as e:
            print(f"[Webhook] Exception while editing message: {e}")

def save_msg(msg, type='print'):
    if type == 'print':
        print(msg)
    with _lock:
        log_queue.append(msg)
threading.Thread(target=webhook_link_batch, daemon=True).start()

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

def detect_color(coords, target_color, tolerance=5):
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

def find_house():
    global area
    left = min(area['top_left'][0], area['bottom_right'][0])
    top = min(area['top_left'][1], area['bottom_right'][1])
    right = max(area['top_left'][0], area['bottom_right'][0])
    bottom = max(area['top_left'][1], area['bottom_right'][1])

    screen_center_x = (area['top_left'][0] + area['bottom_right'][0]) // 2
    screen_center_y = (area['top_left'][1] + area['bottom_right'][1]) // 2
    
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    img_array = np.array(screenshot)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    target_bgr = np.array([color[2], color[1], color[0]])
    lower = np.clip(target_bgr - tolerance, 0, 255)
    upper = np.clip(target_bgr + tolerance, 0, 255)
    mask = cv2.inRange(img_bgr, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    house_circle = []
    for contour in contours:
        house_area = cv2.contourArea(contour)
        if house_area >= min_size:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"]) + left
                center_y = int(M["m01"] / M["m00"]) + top

                x_distance_from_center = abs(center_x - screen_center_x)
                y_distance_from_center = abs(center_y - screen_center_y)
                
                area_width = right - left
                area_height = bottom - top
                relative_x = center_x - left
                relative_y = center_y - top
                
                in_bottom_left = (relative_x < area_width * 0.15 and relative_y > area_height * 0.5)
                in_center_exclusion = (x_distance_from_center <= exclude_radius and y_distance_from_center <= exclude_radius)
                
                if not in_center_exclusion and not in_bottom_left:
                    house_circle.append((center_x, center_y, house_area))
    
    return house_circle

def goto_house():
    global houses_visited
    house = find_house()
    
    if not house:
        return 0

    center_x = (area['top_left'][0] + area['bottom_right'][0]) // 2
    center_y = (area['top_left'][1] + area['bottom_right'][1]) // 2
    closest_blob = min(house, key=lambda blob: (blob[0] - center_x) ** 2 + (blob[1] - center_y) ** 2)
    
    area_x, area_y, house_area = closest_blob
    distance = ((area_x - center_x) ** 2 + (area_y - center_y) ** 2) ** 0.5

    nomove(area_x, area_y)
    time.sleep(0.1)
    pydirectinput.rightClick(area_x, area_y)
    houses_visited += 1

    if res_info == 2560:
        distance_threshold = 400
    elif res_info == 1920:
        distance_threshold = 300
    else:
        distance_threshold = 213

    if distance > distance_threshold:
        return 2
    return 1

def start_overlay():
    global overlay
    try:
        overlay = OverlayWindow(area)
        overlay.run_overlay_thread()
    except Exception as e:
        print(f"Overlay error: {e}")

overlay_thread = threading.Thread(target=start_overlay, daemon=True)
overlay_thread.start()
time.sleep(0.3)


cls()
print(f'Trick or Treat {version} by Lisek_guy2\n\nMacro running correctly\nTo start press F2, to stop press F3')
print('\nMake sure the 4 trick or treat houses are visible on the screen within the green outlined area.\n')
def action_loop():
    while True:
        if running_flag:
            try:
                house_result = goto_house()
                if house_result > 0:
                    cls()
                    if webhook:
                        save_msg(f"Visited {houses_visited} houses in {total_time}")
                    else:
                        print(f"Visited {houses_visited} houses in {total_time}")
                    if house_result == 2:
                        time.sleep(4.0)
                    else:
                        time.sleep(3.0)
                else:
                    time.sleep(0.25)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(0.25)
        else:
            time.sleep(0.4)

# on/off switch with f2 and f3 keys
def toggle_switch(key):
    global running_flag, total_time, houses_visited
    if key == ON_switch:
        if not running_flag:
            running_flag = True
            houses_visited = 0
            print(f"Script started... Houses visited: 0".ljust(60), end="\r")
            hide_overlay()
            auto_f11()
        else:
            running_flag = False
            print(f"Script paused... Houses visited: {houses_visited}".ljust(60), end="\r")
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
    elif key == DEBUG_switch:
        print("Webhook setup skipped as it's now automated.")

with keyboard.Listener(on_press=toggle_switch) as listener:
    action_thread = threading.Thread(target=action_loop)
    action_thread.daemon = True
    action_thread.start()
    listener.join()