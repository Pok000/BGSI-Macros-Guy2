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
import mss
import pyautogui
import tkinter as tk

# DESCRIPTION: Automatically does the fishing board quests (works on v10003) with UI overlay
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

# auto res
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
if screen_width == 2560 and screen_height == 1440:
    quest_tl = (1026, 0)
    quest_br = (1597, 143)
    center = (1280, 720)
    teleport_winter = (1425, 353)
    teleport_jungle = (1198, 344)
    teleport_volcano = (984, 449)
    teleport_atlantis = (856, 645)
    tp = (1285, 1366)
    current_quest = (1137, 73)
    fish_gp = (1277, 1033)
    fish = (909, 988)
    rod = (2476, 1220) #
    rod_select = (1128, 1261)
    quests = [
        "blizzard.png",
        "Poison.png",
        "Volcano.png"
    ]
elif screen_width == 1920 and screen_height == 1080:
    quest_tl = (769, 0)
    quest_br = (1160, 144)
    center = (960, 540)
    teleport_winter = (1094, 212)
    teleport_jungle = (885, 208)
    teleport_volcano = (704, 296)
    teleport_atlantis = (598, 468)
    tp = (962, 1017)
    current_quest = (831, 67)
    fish_gp = (962, 719)
    fish = (749, 782)
    rod = (1846, 886) #
    rod_select = (828, 923)
    quests = [
        "blizzard2.png",
        "Poison2.png",
        "Volcano2.png"
    ]
elif screen_width in [1366, 1364] and screen_height == 768:
    quest_tl = (535, 1)
    quest_br = (846, 109)
    center = (683, 384)
    teleport_winter = (784, 141)
    teleport_jungle = (627, 132)
    teleport_volcano = (481, 200)
    teleport_atlantis = (387, 334)
    tp = (682, 713)
    current_quest = (583, 50)
    fish_gp = (681, 489)
    fish = (556, 571)
    rod = (1310, 619) #
    rod_select = (580, 646)
    quests = [
        "blizzard3.png",
        "Poison3.png",
        "Volcano3.png"
    ]
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

# global names
TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3

# others
running_flag = False    
total_time = ""
current_quest_col = (127, 89, 66)
camera_adjust = False
white = (255, 255, 255)
rod_col = (199, 27, 4)
rod_select_col = (225, 243, 255)
current_location = None
last_detected_quest = None
quest_change_cooldown = 0
prevent_loop = 0
gui = None
exit_flag = False
area_None = 4 
area_names = ["Blizzard Hills", "Poison Jungle", "Infernite Volcano", "Atlantis", "Spawn"]
quest_names = ["Blizzard Hills", "Poison Jungle", "Infernite Volcano", "Any-World"]

class QuestTrackerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quest Tracker")
        self.root.geometry("260x70+0+0")
        self.root.configure(bg='#F5F5DC')
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.offset_x = 0
        self.offset_y = 0

        self.main_frame = tk.Frame(
            self.root,
            bg='#F5F5DC',
            relief='solid',
            bd=2,
            highlightbackground='#D2B48C',
            highlightthickness=2
        )
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.info_frame = tk.Frame(self.main_frame, bg='#F5F5DC')
        self.info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)

        self.quest_label = tk.Label(
            self.info_frame, 
            text="Current Quest: None", 
            font=("Arial", 8, "bold"),
            bg='#F5F5DC', 
            fg='#8B4513',
            anchor='w'
        )
        self.quest_label.pack(anchor='w', pady=10)

        self.close_btn = tk.Label(
            self.main_frame,
            text="×",
            font=("Arial", 8, "bold"),
            bg='#CD5C5C',
            fg='white',
            cursor='hand2',
            width=2,
            height=1
        )
        self.close_btn.pack(side='right', padx=5)
        self.close_btn.bind('<Button-1>', self.close)

        for widget in [self.main_frame, self.info_frame, self.quest_label, self.root]:
            widget.bind('<Button-1>', self.s_drag)
            widget.bind('<B1-Motion>', self.drag)
    
    def s_drag(self, event):
        self.offset_x = event.x_root - self.root.winfo_x()
        self.offset_y = event.y_root - self.root.winfo_y()
    
    def drag(self, event):
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.root.geometry(f"+{x}+{y}")
    
    def update_quest_info(self, current_quest_type):
        if self.root and self.quest_label:
            try:
                if current_quest_type is not None:
                    quest_text = f"Current Quest: {quest_names[current_quest_type]}"
                else:
                    quest_text = "Current Quest: None"
                
                self.quest_label.config(text=quest_text)
                self.root.update_idletasks()
            except tk.TclError:
                pass
    
    def close(self, event):
        global exit_flag
        exit_flag = True
        self.root.quit()
        self.root.destroy()

# function to format elapsed time into hh:mm:ss
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# function to update session time in the background
def update_session_time():
    global total_time, exit_flag
    start_time = time.time()
    while not exit_flag:
        elapsed_time = time.time() - start_time
        total_time = format_time(elapsed_time)
        time.sleep(1)

# Start the session time update thread
session_time_thread = threading.Thread(target=update_session_time, daemon=True)
session_time_thread.start()

# clearing the cmd
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

def wait_for_rod_ready():
    while not detect_color(rod, rod_col, 15) and running_flag and not exit_flag:
        time.sleep(0.2)

def check_rod_cast():
    if not detect_color(rod_select, rod_select_col, 5):
        pydirectinput.press('1')
        time.sleep(0.5)
        if not detect_color(rod_select, rod_select_col, 5):
            print("Failed to equip rod")
            return False
    if not detect_color(rod, rod_col, 15):
        wait_for_rod_ready()
    return True

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

    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        raise FileNotFoundError(f"Could not load template: {template_path}")

    if template.shape[2] == 4:
        template_bgr = template[:, :, :3]
        alpha = template[:, :, 3]
        _, mask = cv2.threshold(alpha, 0, 255, cv2.THRESH_BINARY)
    else:
        template_bgr = template
        mask = None

    if mask is not None:
        result = cv2.matchTemplate(screenshot_bgr, template_bgr, cv2.TM_CCOEFF_NORMED, mask=mask)
    else:
        result = cv2.matchTemplate(screenshot_bgr, template_bgr, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        template_height, template_width = template_bgr.shape[:2]
        absolute_x = max_loc[0] + x1 + template_width // 2
        absolute_y = max_loc[1] + y1 + template_height // 2
        return (absolute_x, absolute_y)
    else:
        return None

def quest_type_now():
    for idx, quest_image in enumerate(quests):
        location = image(quest_tl, quest_br, quest_image, threshold=0.9)
        if location:
            return idx
    return None

def quest_change():
    global last_detected_quest, quest_change_cooldown
    current_time = time.time()
    if current_time < quest_change_cooldown:
        return False
    
    current_quest_type = quest_type_now()
    
    if current_quest_type != last_detected_quest:
        print(f"Quest changed! Old: {last_detected_quest}, New: {current_quest_type}")
        
        last_detected_quest = current_quest_type
        quest_change_cooldown = current_time + 2
        return True
    
    return False

def go_to_location(quest_type):
    global current_location, prevent_loop
    
    if not running_flag or exit_flag:
        return
        
    wait_for_rod_ready()
    
    if not running_flag or exit_flag:
        return
    
    if quest_type == 0:
        # Blizzard
        print("Going to Blizzard Hills...")
        pydirectinput.press('m')
        time.sleep(1.8)
        if not running_flag or exit_flag:
            return
        move(*teleport_winter)
        time.sleep(0.3)
        if not running_flag or exit_flag:
            return
        move(*tp)
        while not detect_color(rod, rod_col, 15) and prevent_loop < 5 and running_flag and not exit_flag:
            time.sleep(1)
            if not running_flag or exit_flag:
                return
            move(*tp)
            prevent_loop += 1
        prevent_loop = 0
        if not running_flag or exit_flag:
            return
        pydirectinput.keyDown('d')
        time.sleep(2)
        pydirectinput.keyUp('d')
        current_location = 0
        
    elif quest_type == 1:
        # Poison
        print("Going to Poison Jungle...")
        pydirectinput.press('m')
        time.sleep(1.8)
        if not running_flag or exit_flag:
            return
        move(*teleport_jungle)
        time.sleep(0.3)
        if not running_flag or exit_flag:
            return
        move(*tp)
        while not detect_color(rod, rod_col, 15) and prevent_loop < 5 and running_flag and not exit_flag:
            time.sleep(1)
            if not running_flag or exit_flag:
                return
            move(*tp)
            prevent_loop += 1
        prevent_loop = 0
        if not running_flag or exit_flag:
            return
        pydirectinput.keyDown('s')
        time.sleep(0.1)
        pydirectinput.keyDown('d')
        time.sleep(0.5)
        pydirectinput.keyUp('s')
        time.sleep(2)
        pydirectinput.keyUp('d')
        current_location = 1
        
    elif quest_type == 2:
        # Volcano
        print("Going to Infernite Volcano...")
        pydirectinput.press('m')
        time.sleep(1.8)
        if not running_flag or exit_flag:
            return
        move(*teleport_volcano)
        time.sleep(0.3)
        if not running_flag or exit_flag:
            return
        move(*tp)
        while not detect_color(rod, rod_col, 15) and prevent_loop < 5 and running_flag and not exit_flag:
            time.sleep(1)
            if not running_flag or exit_flag:
                return
            move(*tp)
            prevent_loop += 1
        prevent_loop = 0
        if not running_flag or exit_flag:
            return
        pydirectinput.keyDown('s')
        time.sleep(0.1)
        pydirectinput.keyDown('d')
        time.sleep(0.5)
        pydirectinput.keyUp('s')
        time.sleep(1.3)
        pydirectinput.keyUp('d')
        current_location = 2

    elif quest_type == 3:
        # Atlantis
        print("Going to Atlantis...")
        pydirectinput.press('m')
        time.sleep(1.8)
        if not running_flag or exit_flag:
            return
        move(*teleport_atlantis)
        time.sleep(0.3)
        if not running_flag or exit_flag:
            return
        move(*tp)
        while not detect_color(rod, rod_col, 15) and prevent_loop < 5 and running_flag and not exit_flag:
            time.sleep(1)
            if not running_flag or exit_flag:
                return
            move(*tp)
            prevent_loop += 1
        prevent_loop = 0
        if not running_flag or exit_flag:
            return
        pydirectinput.keyDown('d')
        time.sleep(4)
        pydirectinput.keyUp('d')
        current_location = 3
    
    elif quest_type == 4:
        # Spawn
        print("Going to Spawn...")
        pydirectinput.press('m')
        time.sleep(1.8)
        if not running_flag or exit_flag:
            return
        move(*center)
        time.sleep(0.3)
        if not running_flag or exit_flag:
            return
        move(*tp)
        while not detect_color(rod, rod_col, 15) and prevent_loop < 5 and running_flag and not exit_flag:
            time.sleep(1)
            if not running_flag or exit_flag:
                return
            move(*tp)
            prevent_loop += 1
        prevent_loop = 0
        if not running_flag or exit_flag:
            return
        pydirectinput.keyDown('d')
        time.sleep(2)
        pydirectinput.keyUp('d')
        current_location = 4
    
    if running_flag and not exit_flag:
        time.sleep(0.4)

def free_fish():
    global current_location, prevent_loop
    if not check_rod_cast():
        return "failed"
    
    while running_flag and not exit_flag:
        if not running_flag or exit_flag:
            pydirectinput.mouseUp()
            return "paused"
            
        pydirectinput.mouseDown()
        time.sleep(0.25)
        pydirectinput.mouseUp()
        no_afk = time.time() + 15
        quest_checked = False
        
        while not detect_color(rod, rod_col, 15) and time.time() < no_afk and running_flag and not exit_flag:
            if not running_flag or exit_flag:
                pydirectinput.mouseUp()
                return "paused"
                
            if not quest_checked:
                time.sleep(1)

                if not detect_color(current_quest, current_quest_col, 10):
                    pydirectinput.mouseUp()
                    time.sleep(1)
                    return "quest_completed"

                if quest_change():
                    pydirectinput.mouseUp()
                    time.sleep(1)
                    return "quest_changed"
                
                quest_checked = True
            
            pydirectinput.mouseDown()
            if not detect_color(fish, white):
                time.sleep(0.05)
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

            if not running_flag or exit_flag:
                return "paused"

            if not detect_color(current_quest, current_quest_col, 10):
                time.sleep(2.5)
                if not detect_color(current_quest, current_quest_col, 10):
                    print('Quest completed!')
                    return "quest_completed"

def scroll(direction, amount):
    if direction == 'up':
        pyautogui.scroll(amount)
    elif direction == 'down':
        pyautogui.scroll(-amount)

def detect_color(coords, target_color, tolerance=20):
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    bgr_color = img[coords[1], coords[0]]
    target_color_bgr = (target_color[2], target_color[1], target_color[0])
    diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
    return np.all(diff <= tolerance)

def gui_update():
    if gui:
        try:
            display_quest = last_detected_quest if last_detected_quest is not None else 4
            gui.update_quest_info(display_quest)
        except Exception:
            pass

cls()

print(f"Auto Quest Board {version} by Lisek_guy2\nSelect default area for ANY-WORLD quests:\n1. Blizzard Hills\n2. Poison Jungle\n3. Infernite Volcano\n4. Atlantis\n5. Spawn (Default)")
while True:
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            area_None = int(choice) - 1
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
    except (ValueError, KeyboardInterrupt):
        print("Invalid input. Please enter 1, 2, 3, 4, or 5.")

cls()
print(f'Auto Quest Board {version} by Lisek_guy2\n\nDefault area for ANY-WORLD quests: {area_names[area_None]}\n\nMacro running correctly\nTo start press F2, to stop press F3')

def action_loop():
    global camera_adjust, current_location, last_detected_quest, prevent_loop, area_None
    while not exit_flag:
        if running_flag and not exit_flag:
            if not camera_adjust:
                nomove(center[0], 400)
                pydirectinput.mouseDown(button='right')
                time.sleep(0.4)
                nomove(center[0], 1000)
                pydirectinput.mouseUp(button='right')
                scroll('down', 5000)
                camera_adjust = True

            if detect_color(current_quest, current_quest_col, 10):
                current_quest_type = quest_type_now()
                last_detected_quest = current_quest_type

                gui_update()
                
                if current_quest_type is not None:
                    if current_location != current_quest_type:
                        print(f"World-specific quest detected: {quests[current_quest_type]}")
                        if not detect_color(rod_select, rod_select_col, 5) and running_flag and not exit_flag:
                            pydirectinput.press('1')
                            time.sleep(0.5)
                        if running_flag and not exit_flag:
                            go_to_location(current_quest_type)
                else:
                    if current_location != area_None:
                        print(f"Any-world quest detected, going to {area_names[area_None]}")
                        if running_flag and not exit_flag:
                            wait_for_rod_ready()
                        if not detect_color(rod_select, rod_select_col, 5) and running_flag and not exit_flag:
                            pydirectinput.press('1')
                            time.sleep(0.5)
                        if running_flag and not exit_flag:
                            go_to_location(area_None)

                if running_flag and not exit_flag:
                    result = free_fish()
                    if result == "quest_completed":
                        print("Quest completed")
                        current_location = None
                        last_detected_quest = None
                        gui_update()
                        time.sleep(2)
                    elif result == "quest_changed":
                        gui_update()
                        continue
                    elif result == "paused":
                        print("Script paused during fishing")
                        continue
                    
            else:
                if running_flag and not exit_flag:
                    print("No active quest detected, waiting...")
                    current_location = None
                    last_detected_quest = None
                    gui_update()
                    time.sleep(2)
        else:
            time.sleep(0.4)

def toggle_switch(key):
    global running_flag, total_time, exit_flag
    if key == ON_switch:
        running_flag = not running_flag
        if running_flag:
            print(f"Script started...".ljust(80), end="\r")
            auto_f11()
            time.sleep(1)
        else:
            print(f"Script paused...".ljust(60), end="\r")
    elif key == OFF_switch:
        print(f"Script stopped".ljust(60), end="\r")
        exit_flag = True
        running_flag = False
        if gui and gui.root:
            try:
                gui.root.quit()
                gui.root.destroy()
            except:
                pass
        sys.exit()
    elif key == TIME_switch:
        print(f"Time elapsed: {total_time}")

def setup_gui():
    global gui
    try:
        gui = QuestTrackerGUI()
        return gui
    except Exception as e:
        print(f"GUI Error: {e}")
        return None
    
gui = setup_gui()
if gui:
    action_thread = threading.Thread(target=action_loop, daemon=True)
    action_thread.start()

    def run_keyboard_listener():
        try:
            with keyboard.Listener(on_press=toggle_switch) as listener:
                listener.join()
        except:
            pass
    
    listener_thread = threading.Thread(target=run_keyboard_listener, daemon=True)
    listener_thread.start()
    try:
        gui.root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        exit_flag = True
        sys.exit()
else:
    action_thread = threading.Thread(target=action_loop, daemon=True)
    action_thread.start()
    
    try:
        with keyboard.Listener(on_press=toggle_switch) as listener:
            listener.join()
    except KeyboardInterrupt:
        pass
    finally:
        exit_flag = True
        sys.exit()