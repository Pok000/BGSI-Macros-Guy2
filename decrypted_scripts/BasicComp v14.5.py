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
# DESCRIPTION: Plays the competetive thing idk
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
    left_area = ((980, 840), (1147, 940))
    right_area = ((1410, 840), (1557, 940))
    images_list = [
        (5, 'spike_egg.png'),
        (4, 'mythic.png'),
        (3, 'shiny.png'),
        (2, 'legendary.png'),
        (1, 'common.png'),
    ]
    competetive = (2479, 1100)
    tasks = (794, 671)
    gui_exit = (1654, 439)
    hatch_info = (68, 696)
    reroll_left = (919, 865)
    reroll_right = (1332, 864)
    mythic_pos = (1800, 15)
    gui_exit_backup = (1655, 466)
    items = (603, 722)
    center = (1280, 720)
    auto_open = (798, 1021)
    mystery_box = 'box.png'
    box_auto_button = (1227, 1070)
    box_auto_button_col = (195, 17, 77)
    left_orb_check = (888, 896)
    right_orb_check = (1301, 895)
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    left_area = ((703, 633), (836, 733))
    right_area = ((1068, 627), (1198, 736))
    images_list = [
        (5, 'spike_egg2.png'),
        (4, 'mythic2.png'),
        (3, 'shiny2.png'),
        (2, 'legendary2.png'),
        (1, 'common2.png'),
    ]
    competetive = (1851, 786)
    tasks = (535, 498)
    gui_exit = (1288, 297)
    hatch_info = (59, 514)
    reroll_left = (647, 665)
    reroll_right = (1004, 669)
    mythic_pos = (1533, 15)
    gui_exit_backup = (1288, 322)
    items = (371, 536)
    center = (960, 540)
    auto_open = (536, 805)
    mystery_box = 'box2.png'
    box_auto_button = (900, 800)
    box_auto_button_col = (197, 18, 77)
    left_orb_check = (616, 694)
    right_orb_check = (977, 694)
elif screen_width == 1366 and screen_height == 768:
    res_info = 1366
    left_area = ((493, 459), (586, 536))
    right_area = ((777, 467), (868, 535))
    images_list = [
        (5, 'spike_egg3.png'),
        (4, 'mythic3.png'),
        (3, 'shiny3.png'),
        (2, 'legendary3.png'),
        (1, 'common3.png'),
    ]
    competetive = (1312, 539)
    tasks = (350, 349)
    gui_exit = (934, 195)
    hatch_info = (47, 363)
    reroll_left = (440, 478)
    reroll_right = (717, 481)
    mythic_pos = (923, 10)
    gui_exit_backup = (938, 213)
    items = (224, 385)
    center = (683, 384)
    auto_open = (353, 587)
    mystery_box = 'box3.png'
    box_auto_button = (640, 568)
    box_auto_button_col = (197, 19, 77)
    left_orb_check = (417, 503)
    right_orb_check = (697, 504)
else:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"Please either use 2560x1440, 1920x1080 or 1366x768 resolution and set your scale to 100% for this macro to work.\nCurrent resolution: {screen_width}x{screen_height}",
        "Invalid resolution",
        0x10
    )
    sys.exit()

print = functools.partial(print, flush=True)

def scroll(direction, amount):
    if direction == 'up':
        pyautogui.scroll(amount)
    elif direction == 'down':
        pyautogui.scroll(-amount)

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
hatch_color = (238, 50, 94)
gui_skip = False
mythic_col = (0, 2, 254)
debug_counter = 0
no_orbs_gui_col = (187, 9, 78)
gui_exit_col = (194, 16, 77)
gui_exit_col_backup = (195, 45, 93)
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
    current_x, current_y = pyautogui.position()
    if (current_x, current_y) == (target_x, target_y):
        pydirectinput.click(target_x, target_y)
        time.sleep(delay)
    else:
        pydirectinput.moveTo(target_x, target_y)
        ahk.mouse_move(target_x + 4, target_y + 4)
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

def scroll(direction, amount):
    if direction == 'up':
        pyautogui.scroll(amount)
    elif direction == 'down':
        pyautogui.scroll(-amount)

def check_task():
    global gui_skip
    while not detect_color(gui_exit_backup, gui_exit_col, 15) and not detect_color(gui_exit_backup, gui_exit_col_backup, 15):
        if detect_color(gui_exit, (255, 255, 255), 20):
            move(*gui_exit)
        move(*competetive)
        if delay >= 0.1:
            time.sleep(delay)
    if not gui_skip:
        move(*tasks)
        time.sleep(0.2)
        gui_skip = True

    def find_best_match(template_path, area_coords):
        screenshot = ImageGrab.grab()
        left, top = area_coords[0]
        right, bottom = area_coords[1]
        cropped_img = screenshot.crop((left, top, right, bottom))
        img_rgb = np.array(cropped_img)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(template_path, 0)
        if template is None:
            return None, 0.0

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        return max_val

    def threaded_check(image_path, area_coords, results, index):
        confidence = find_best_match(image_path, area_coords)
        if confidence >= 0.85:
            results[index] = (image_path, confidence)
        else:
            results[index] = None

    while True:
        global no_reroll_orbs
        if not running_flag:
            time.sleep(0.2)
        else:
            left_results = [None] * len(images_list)
            left_threads = []
            for i, (number, image_path) in enumerate(images_list):
                t = threading.Thread(target=threaded_check, args=(image_path, left_area, left_results, i))
                t.start()
                left_threads.append(t)
            for t in left_threads:
                t.join()
            left_egg_matches = []
            for i, res in enumerate(left_results):
                if res is not None:
                    number = images_list[i][0]
                    confidence = res[1]
                    left_egg_matches.append((number, confidence, "left"))

            if not left_egg_matches:
                if not detect_color(left_orb_check, no_orbs_gui_col, 20):
                    if not detect_color(gui_exit_backup, gui_exit_col, 15) and not detect_color(gui_exit_backup, gui_exit_col_backup, 15):
                        if detect_color(gui_exit, (255, 255, 255), 20):
                            move(*gui_exit)
                        move(*competetive)
                        if delay >= 0.1:
                            time.sleep(delay)
                    move(*reroll_left)
                    time.sleep(delay)
                else:
                    no_orbs_left()
                right_results = [None] * len(images_list)
                right_threads = []
                for i, (number, image_path) in enumerate(images_list):
                    t = threading.Thread(target=threaded_check, args=(image_path, right_area, right_results, i))
                    t.start()
                    right_threads.append(t)
                for t in right_threads:
                    t.join()
                right_egg_matches = []
                for i, res in enumerate(right_results):
                    if res is not None:
                        number = images_list[i][0]
                        confidence = res[1]
                        right_egg_matches.append((number, confidence, "right"))

                if not right_egg_matches:
                    if not detect_color(left_orb_check, no_orbs_gui_col, 20):
                        if not detect_color(gui_exit_backup, gui_exit_col, 15) and not detect_color(gui_exit_backup, gui_exit_col_backup, 15):
                            if detect_color(gui_exit, (255, 255, 255), 20):
                                move(*gui_exit)
                            move(*competetive)
                            if delay >= 0.1:
                                time.sleep(delay)
                        move(*reroll_right)
                        if int(delay) > 0.1:
                            time.sleep(delay)
                    else:
                        no_orbs_left()
                else:
                    continue

            right_results = [None] * len(images_list)
            right_threads = []
            for i, (number, image_path) in enumerate(images_list):
                t = threading.Thread(target=threaded_check, args=(image_path, right_area, right_results, i))
                t.start()
                right_threads.append(t)
            for t in right_threads:
                t.join()
            right_egg_matches = []
            for i, res in enumerate(right_results):
                if res is not None:
                    number = images_list[i][0]
                    confidence = res[1]
                    right_egg_matches.append((number, confidence, "right"))

            while left_egg_matches and not right_egg_matches:
                if not detect_color(left_orb_check, no_orbs_gui_col, 0):
                    if not detect_color(gui_exit_backup, gui_exit_col, 15) and not detect_color(gui_exit_backup, gui_exit_col_backup, 15):
                        if detect_color(gui_exit, (255, 255, 255), 20):
                            move(*gui_exit)
                        move(*competetive)
                        if delay >= 0.1:
                            time.sleep(delay)
                    move(*reroll_right)
                    if int(delay) > 0.1:
                        time.sleep(delay)
                else:
                    no_orbs_left()

                right_results = [None] * len(images_list)
                right_threads = []
                for i, (number, image_path) in enumerate(images_list):
                    t = threading.Thread(target=threaded_check, args=(image_path, right_area, right_results, i))
                    t.start()
                    right_threads.append(t)
                for t in right_threads:
                    t.join()
                right_egg_matches = []
                for i, res in enumerate(right_results):
                    if res is not None:
                        number = images_list[i][0]
                        confidence = res[1]
                        right_egg_matches.append((number, confidence, "right"))
                else:
                    break

            if left_egg_matches and right_egg_matches:
                break

    best_left_egg = max(left_egg_matches, key=lambda x: x[1]) if left_egg_matches else (None, 0, None)
    best_right_egg = max(right_egg_matches, key=lambda x: x[1]) if right_egg_matches else (None, 0, None)

    return (best_left_egg[0], best_left_egg[2], best_right_egg[0], best_right_egg[2])

cls()
delay = input("Delay between checking images (lower = faster but you NEED low ping)\nType is in seconds example: 0.05\n\nYour delay: ")
delay = float(delay)
cls()

cls()
print("What do you want to do after your reroll orbs end? Choose an option:\n1 - Get more orbs (NOT recommended)\n2 - Blow bubbles\n3 - Hatch the current egg\nPlease note that you need the infinite backpack to blow bubbles")
no_reroll_orbs = input("Enter the number of your choice: ")
try:
    no_reroll_orbs = int(no_reroll_orbs)
    if no_reroll_orbs not in [1, 2, 3]:
        print("Invalid choice, defaulting to 1 (Get more orbs)")
        no_reroll_orbs = 1
except ValueError:
    print("Invalid input, defaulting to 1 (Get more orbs)")
    no_reroll_orbs = 1

cls()
# Ask user which images to target
print("Select which images to target by entering their numbers separated by commas:")
for num, img_name in images_list:
    print(f"{num} - {img_name}")
selected_images_input = input("Your selection (e.g., 1,2,4): ")
try:
    selected_nums = [int(x.strip()) for x in selected_images_input.split(",") if x.strip().isdigit()]
    filtered_images_list = [item for item in images_list if item[0] in selected_nums]
    if not filtered_images_list:
        print("No valid images selected, defaulting to all images.")
        filtered_images_list = images_list
except Exception:
    print("Invalid input, defaulting to all images.")
    filtered_images_list = images_list

images_list = filtered_images_list

def no_orbs_left():
    global running_flag, debug_counter
    print('You have run out of orbs')
    running_flag = False
    if no_reroll_orbs == 1:
        pydirectinput.press('f')
        time.sleep(0.4)
        move(*items)
        time.sleep(0.4)
        nomove(*center)
        time.sleep(0.3)
        scroll('down', 2000)
        time.sleep(0.5)
        find_box = pyautogui.locateOnScreen(mystery_box, confidence=0.9)
        if find_box is None:
            scroll('down', 2000)
            debug_counter += 1
            if debug_counter >= 5:
                print('You most likely have run out of mystery box, blowing bubles instead')
                pydirectinput.press('f')
                move(*center)
                while True:
                    pydirectinput.mouseDown()
                    pydirectinput.press('jump')
                    time.sleep(60)
        else:
            x, y, w, h = find_box
            center_x = x + w // 2
            center_y = y + h // 2
            move(center_x, center_y)
        move(*auto_open)
        for _ in range(900):
            pydirectinput.press('space')
            time.sleep(4)
            if not detect_color(box_auto_button, box_auto_button_col, 20):
                pydirectinput.press('f')
                move(*auto_open)
                if detect_color(box_auto_button, box_auto_button_col, 20):
                    print('You most likely have run out of mystery box while using them, blowing bubles instead')
                    pydirectinput.press('f')
                    move(*center)
                    while True:
                        pydirectinput.mouseDown()
                        pydirectinput.press('jump')
                        time.sleep(60)
        move(*box_auto_button)
        for _ in range(40):
            pydirectinput.click()
            time.sleep(0.1)
        move(*center)
        for _ in range(20):
            pydirectinput.click()
            time.sleep(0.3)
        time.sleep(3)
        running_flag = True
    elif no_reroll_orbs == 2:
        move(*gui_exit)
        time.sleep(0.4)
        move(*center)
        while True:
            pydirectinput.mouseDown()
            pydirectinput.press('jump')
            time.sleep(60)
    elif no_reroll_orbs == 3:
        move(*gui_exit)
        time.sleep(0.4)
        while True:
            pydirectinput.press('r')
            time.sleep(0.3)

cls()
for _ in range(20):
    print('PLEASE SET YOUR CAMERA FACING THE SKY AS IN THE MACRO CHANNEL')
print('AutoCompetetive by Lisek_guy2\n\nMacro running correctly\nTo start press F2, to stop press F3')
def action_loop():
    global running_flag, total_time, gui_skip, debug_counter
    while True:
        if not running_flag:
            time.sleep(0.2)
        else:
            check_task()
            move(*gui_exit)
            while not detect_color(mythic_pos, mythic_col, 90) and running_flag:
                pydirectinput.press('e')
                time.sleep(0.05)
            time.sleep(0.75)
            while not detect_color(hatch_info, hatch_color) and running_flag:
                time.sleep(0.1)

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