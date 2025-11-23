from pynput import keyboard
from PIL import ImageGrab
import mss
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
import random

# DESCRIPTION: Fast competetive macro (130 or less ping required)
# VERSIONS: all
version = "v24.3"

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
        0x101
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
    daily = (69, 693)
    box_max = (1279, 812)
    box_max_col = (241, 58, 72)
    competetive = (2483, 1105)
    box_use = (800, 965)
    box12 = (1238, 836)
    box25 = (1535, 839)
    exit_comp = (1655, 441)
    reroll_left = (920, 864)
    reroll_right = (1331, 866)
    no_orbs = (1197, 832)
    no_orbs_col = (217, 36, 74)
    color_coords = (center[0], 18)
    inf_backpack = (1322, 736)
    inf_backpack_col = (122, 242, 19)
    # new
    comp_gui = (1654, 409)
    comp_gui_col = (247, 63, 71)
    mystery_box = (715, 563)
    mystery_box_col = (255, 122, 255)
    inventory = ((939, 451), (1841, 1075))
    items = (606, 718)
    box_image = "box.png"
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    center = (960, 540)
    daily = (59, 513)
    box_max = (960, 618) 
    box_max_col = (244, 60, 71)
    competetive = (1847, 779)
    box_use = (540, 751)
    box12 = (925, 638)
    box25 = (1186, 643)
    exit_comp = (1288, 294)
    reroll_left = (644, 668)
    reroll_right = (1002, 666)
    no_orbs = (890, 639)
    no_orbs_col = (216, 35, 74)
    color_coords = (center[0], 15)
    inf_backpack = (994, 554)
    inf_backpack_col = (121, 242, 19)
    # new
    comp_gui = (1288, 268) #
    comp_gui_col = (246, 62, 71) #
    mystery_box = (464, 402) #
    mystery_box_col = (255, 123, 255) #
    inventory = ((664, 302), (1452, 857)) #
    items = (366, 540) #
    box_image = "box2.png"
elif screen_width in [1366, 1364] and screen_height == 768:
    res_info = 1366
    center = (683, 384)
    daily = (47, 362)
    box_max = (682, 445)
    box_max_col = (244, 60, 71)
    competetive = (1308, 538)
    box_use = (359, 546)
    box12 = (655, 463)
    box25 = (857, 464)
    exit_comp = (937, 193)
    reroll_left = (436, 483)
    reroll_right = (719, 484)
    no_orbs = (629, 459)
    no_orbs_col = (219, 38, 74)
    color_coords = (center[0], 12)
    inf_backpack = (710, 394) 
    inf_backpack_col = (124, 243, 19)
    # new
    comp_gui = (938, 172) #
    comp_gui_col = (247, 63, 71) #
    mystery_box = (298, 277) #
    mystery_box_col = (255, 123, 255) #
    inventory = ((453, 196), (1060, 633)) #
    items = (224, 380) #
    box_image = "box3.png"
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

def find_box_in_inventory():
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), box_image)
    if not os.path.exists(template_path):
        return False
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print("ERROR: No image present")
        return False
    (x1, y1), (x2, y2) = inventory
    width, height = x2 - x1, y2 - y1
    with mss.mss() as sct:
        monitor = {"left": x1, "top": y1, "width": width, "height": height}
        shot = sct.grab(monitor)
        img = np.array(shot)
        img_bgr = img[:, :, :3]
    res = cv2.matchTemplate(img_bgr, template[:, :, :3], cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    threshold = 0.85
    if max_val >= threshold:
        th, tw = template.shape[:2]
        center_x = x1 + max_loc[0] + tw // 2
        center_y = y1 + max_loc[1] + th // 2
        pydirectinput.click(center_x, center_y)
        return True
    return False

quests = {
    1: {
        'name': 'mythic',
        2560: [((1047, 840), (255, 30, 255)), ((1460, 841), (254, 38, 255))],
        1920: [((753, 641), (245, 26, 255)), ((1115, 640), (248, 34, 255))],
        1366: [((522, 464), (253, 24, 255)), ((804, 463), (254, 29, 255))],
    },
    2: {
        'name': 'shiny',
        2560: [((1077, 804), (255, 249, 125)), ((1490, 804), (255, 249, 125))],
        1920: [((782, 614), (255, 249, 113)), ((1143, 615), (255, 251, 120))],
        1366: [((544, 442), (255, 251, 109)), ((825, 442), (255, 251, 109))],
    },
    3: {
        'name': 'legendary',
        2560: [((1115, 871), (0, 37, 255)), ((1529, 872), (0, 26, 255))],
        1920: [((815, 669), (0, 37, 255)), ((1177, 670), (0, 34, 255))],
        1366: [((570, 484), (0, 38, 255)), ((852, 484), (0, 25, 241))],
    },
    4: {
        'name': 'spike',
        2560: [((1005, 848), (194, 200, 210)), ((1417, 849), (195, 201, 211))],
        1920: [((719, 653), (194, 199, 209)), ((1080, 653), (194, 199, 209))],
        1366: [((496, 471), (191, 196, 207)), ((777, 471), (191, 196, 207))],
    },
    5: {
        'name': 'common',
        2560: [((1139, 862), (255, 255, 255)), ((1551, 862), (255, 255, 255))],
        1920: [((834, 664), (255, 255, 255)), ((1197, 664), (255, 255, 255))],
        1366: [((585, 481), (255, 255, 255)), ((866, 481), (255, 255, 255))],
    },
}

def select_quest():
    print("Select quest types to target (comma separated numbers):")
    for i in range(1, 6):
        print(f"{i}: {quests[i]['name']}")
    while True:
        try:
            sel = input("Enter quest numbers (e.g. 1,3,4,5): ")
            nums = [int(x.strip()) for x in sel.split(',') if x.strip() and int(x.strip()) in quests]
            if nums:
                return nums
        except Exception:
            pass
        print("Invalid input. Try again.")

def egg_table(selected, res_info):
    left, right = [], []
    for num in selected:
        quest = quests[num]
        pairs = quest.get(res_info, [])
        for i in range(0, len(pairs), 2):
            if i+1 < len(pairs):
                l, r = pairs[i], pairs[i+1]
                if l[0][0] is not None:
                    left.append({'coords': l[0], 'color': l[1], 'name': f"{quest['name']}_left_{i//2+1}"})
                if r[0][0] is not None:
                    right.append({'coords': r[0], 'color': r[1], 'name': f"{quest['name']}_right_{i//2+1}"})
    return left, right

# global names
TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3

# others
running_flag = False
total_time = ""
hatching_click_flag = False
quests_done = 0
orbs_total = 0
daily_col = (238, 49, 94)
rerolled_left = False
rerolled_right = False
hatching_phase = False
mythic_detect_count = 0
left_quest_type = None
right_quest_type = None
tolerance = 50
start_time_orbs = time.time()

def hatching_clicker():
    global hatching_click_flag
    while True:
        if hatching_click_flag:
            pydirectinput.click()
            time.sleep(0.08)
        else:
            time.sleep(0.1)

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
    pydirectinput.moveTo(target_x + 4, target_y + 4)
    ahk.mouse_move(target_x, target_y)
    pydirectinput.click(target_x, target_y)

def click(target_x, target_y):
    pydirectinput.click(target_x, target_y)

def nomove(x, y):
    ahk.mouse_move(x, y)

def min_box(coords_list):
    xs = [x for x, y in coords_list]
    ys = [y for x, y in coords_list]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return min_x, min_y, max_x, max_y

def grab_mss(coords_colors, tolerance=20):
    coords = [c for c, _ in coords_colors]
    min_x, min_y, max_x, max_y = min_box(coords)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    with mss.mss() as sct:
        monitor = {"left": min_x, "top": min_y, "width": width, "height": height}
        shot = sct.grab(monitor)
        img = np.array(shot) 
        img_bgr = img[:, :, :3]
    results = []
    for (x, y), target_color in coords_colors:
        rel_x, rel_y = x - min_x, y - min_y
        bgr_color = img_bgr[rel_y, rel_x]
        target_color_bgr = (target_color[2], target_color[1], target_color[0])
        diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
        results.append(np.all(diff <= tolerance))
    return results

def detect_color(coords, target_color, tolerance=20, frame=None, bbox_origin=None):
    if frame is not None and bbox_origin is not None:
        x, y = coords
        rel_x, rel_y = x - bbox_origin[0], y - bbox_origin[1]
        bgr_color = frame[rel_y, rel_x]
        target_color_bgr = (target_color[2], target_color[1], target_color[0])
        diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
        return np.all(diff <= tolerance)
    else:
        return grab_mss([(coords, target_color)], tolerance)[0]

def scroll(direction, amount):
    if direction == 'up':
        pyautogui.scroll(amount)
    elif direction == 'down':
        pyautogui.scroll(-amount)

cls()
selected_quests = select_quest()
left_table, right_table = egg_table(selected_quests, res_info)
require_ten_mythic = all(q in (2, 4, 5) for q in selected_quests) and len(selected_quests) >= 2

def select_box():
    print("How many boxes do you want to open?\n\n1: Open 25 boxes\n2: Open 49 boxes\n3: Don't open boxes")
    while True:
        val = input("Enter 1, 2, or 3: ").strip()
        if val == "1":
            return 25
        elif val == "2":
            return 49
        elif val == "3":
            return 0
        print("Invalid input. Please enter 1, 2, or 3.")

boxes_to_open = select_box()
open_25_flag = (boxes_to_open == 25)
open_49_flag = (boxes_to_open == 49)
open_none_flag = (boxes_to_open == 0)

def ask_no_orbs_func():
    print("What should you do after you run out of reroll orbs:\n1 - hatch the eggs\n2 - blow bubbles")
    while True:
        val = input("Enter 1 or 2: ").strip()
        if val in ("1", "2"):
            return int(val)
        print("Invalid input. Please enter 1 or 2.")

no_orbs_func = ask_no_orbs_func()

def gui_open():
    return detect_color(comp_gui, comp_gui_col, 10)

def open_comp_def():
    move(*competetive)
    time.sleep(0.15)
    if detect_color(daily, (119, 25, 47), 10):
        time.sleep(0.2)
        if gui_open():
            return
        else:
            open_comp_def()
    else:
        move(*box_use)
        move(*box12)
        time.sleep(0.15)
        if detect_color(box_max, box_max_col, 10):
            move(*box_max)
            time.sleep(0.2)
            pydirectinput.press('f')
            time.sleep(0.2)
        open_comp_def()

    def detect_box_image():
        if not hasattr(detect_box_image, "template"):
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), box_image)
            if not os.path.exists(template_path):
                print("[WARN] image not found for mystery_box detection!")
                return False
            detect_box_image.template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
            if detect_box_image.template is None:
                print("[WARN] image could not be loaded!")
                return False
        template = detect_box_image.template
        x, y = mystery_box
        w, h = template.shape[1], template.shape[0]
        with mss.mss() as sct:
            monitor = {"left": x, "top": y, "width": w, "height": h}
            shot = sct.grab(monitor)
            img = np.array(shot)
            img_bgr = img[:, :, :3]
        res = cv2.matchTemplate(img_bgr, template[:, :, :3], cv2.TM_CCOEFF_NORMED)
        threshold = 0.85
        loc = np.where(res >= threshold)
        return len(loc[0]) > 0

def pixel_c(table, tolerance=20):
    if not table:
        return None
    coords_colors = [(info["coords"], info["color"]) for info in table]
    try:
        results = grab_mss(coords_colors, tolerance)
    except RuntimeError:
        for info in table:
            if detect_color(info["coords"], info["color"], tolerance):
                return info["name"]
        return None
    for idx, match in enumerate(results):
        if match:
            return table[idx]["name"]
    return None

def no_orbs_left():
    move(*no_orbs)
    if not gui_open():
        open_comp_def()
    else:
        print("no orbs left")
        move(*exit_comp)
        time.sleep(0.4)
        move(center[0], center[1] + 350)
        if no_orbs_func == 2:
            while True:
                pydirectinput.click()
                time.sleep(0.2)
                if detect_color(inf_backpack, inf_backpack_col, 10):
                    pydirectinput.mouseUp()
                    move(*inf_backpack)
                    time.sleep(3)
                    move(*inf_backpack)
                    for _ in range(3):
                        pydirectinput.click()
                        time.sleep(0.3)
                    while True:
                        pydirectinput.mouseDown()
                        time.sleep(120)
                        pydirectinput.mouseUp()
                        time.sleep(0.4)
        else:
            while True:
                pydirectinput.press('e')
                time.sleep(0.3)
        
cls()
def get_col(coords):
    color_bgr = None
    with mss.mss() as sct:
        monitor = {"left": coords[0], "top": coords[1], "width": 1, "height": 1}
        shot = sct.grab(monitor)
        img = np.array(shot)
        color_bgr = img[0, 0, :3]
    return (int(color_bgr[2]), int(color_bgr[1]), int(color_bgr[0]))

def color_diff(c1, c2):
    return np.linalg.norm(np.array(c1, dtype=int) - np.array(c2, dtype=int))

def get_match(table, reroll_coords, tolerance=20):
    if not table:
        return False
    info = table[0]
    last_color = get_col(info["coords"])
    first = True
    global quests_done, orbs_total, start_time_orbs
    consecutive_no_color = 0
    for attempt in range(2):
        match = pixel_c(table, tolerance)
        if match:
            elapsed = time.time() - start_time_orbs
            orbs_per_hour = (orbs_total / elapsed * 3600) if elapsed > 0 else 0
            if attempt == 0:
                print(f"{match} quest found (total orbs: {orbs_total}, orbs/h: {orbs_per_hour:.2f}, quests done: {quests_done})")
            return match
        time.sleep(0.15)

    stuck_pixel_count = 0
    while True:
        if first:
            move(*reroll_coords)
            orbs_total += 5
            first = False
        else:
            click(*reroll_coords)
            orbs_total += 5
        start = time.time()
        changed = False
        while time.time() - start < 0.3:
            time.sleep(0.08)
            new_color = get_col(info["coords"])
            if color_diff(new_color, last_color) > tolerance:
                changed = True
                stuck_pixel_count = 0
                break
        if not changed:
            stuck_pixel_count += 1
            if stuck_pixel_count >= 10:
                print("possible lag, attempting to fix")
                move(*box12)
                time.sleep(0.2)
                if not gui_open():
                    move(*competetive)
                    time.sleep(0.2)
                    if not gui_open():
                        print("welll uhhhh... there's a small issue mate")
                stuck_pixel_count = 0
            match = pixel_c(table, tolerance)
            if match:
                quests_done += 1
                elapsed = time.time() - start_time_orbs
                orbs_per_hour = (orbs_total / elapsed * 3600) if elapsed > 0 else 0
                print(f"{match} quest found post-click (total orbs: {orbs_total}, orbs/h: {orbs_per_hour:.2f}, quests done: {quests_done})")
                return match
            else:
                consecutive_no_color += 1
                if consecutive_no_color >= 20 and no_orbs is not None:
                    try:
                        if detect_color(no_orbs, no_orbs_col, 10):
                            no_orbs_left()
                    finally:
                        consecutive_no_color = 0
        if changed:
            match = pixel_c(table, tolerance)
            if match:
                quests_done += 1
                elapsed = time.time() - start_time_orbs
                orbs_per_hour = (orbs_total / elapsed * 3600) if elapsed > 0 else 0
                print(f"{match} quest found (total orbs: {orbs_total}, orbs/h: {orbs_per_hour:.2f}, quests done: {quests_done})")
                return match
            else:
                last_color = new_color
                consecutive_no_color += 1
                if consecutive_no_color >= 20 and no_orbs is not None:
                    try:
                        if detect_color(no_orbs, no_orbs_col, 10):
                            no_orbs_left()
                    finally:
                        consecutive_no_color = 0
                continue
        else:
            continue

cls()
print(f'FastComp {version} by Lisek_guy2\n\nMacro running correctly\nTo start press F2, to stop press F3')
def action_loop():
    global orbs_total, initial_color, hatching_click_flag, rerolled_left, rerolled_right, hatching_phase, mythic_detect_count, left_quest_type, right_quest_type, tolerance
    while True:
        if running_flag:
            if 'initial_color' not in globals():
                initial_color = get_col(color_coords)
                open_comp_def()
            gui_was_open = False
            if not rerolled_left:
                if gui_open():
                    match = get_match(left_table, reroll_left)
                    if match:
                        rerolled_left = True
                        left_quest_type = match.split('_')[0]
                    gui_was_open = True
                else:
                    if gui_was_open:
                        time.sleep(0.3)
                        gui_was_open = False
                        mythic_detect_count = 0
            elif not rerolled_right:
                if gui_open():
                    match = get_match(right_table, reroll_right)
                    if match:
                        rerolled_right = True
                        right_quest_type = match.split('_')[0]
                    gui_was_open = True
                else:
                    if gui_was_open:
                        time.sleep(0.3)
                        gui_was_open = False
                        mythic_detect_count = 0
            elif not hatching_phase:
                move(*exit_comp)
                time.sleep(0.05)
                if not detect_color(daily, daily_col, 10):
                    while not detect_color(daily, daily_col, 10):
                        move(*exit_comp)
                        time.sleep(0.3)
                hatching_phase = True
                hatching_click_flag = True
                orbs_total += 5
            else:
                if not gui_open():
                    current_color = get_col(color_coords)
                    if color_diff(current_color, initial_color) > tolerance:
                        time.sleep(0.3)
                        current_color2 = get_col(color_coords)
                        if color_diff(current_color2, initial_color) > tolerance:
                            mythic_detect_count += 1
                            require_ten = (left_quest_type in ("shiny", "spike", "common")) and (right_quest_type in ("shiny", "spike", "common"))
                            if require_ten and mythic_detect_count < 5:
                                pydirectinput.press('e')
                                pydirectinput.click()
                            else:
                                print("Mythic hatched")
                                for _ in range(30):
                                    if detect_color(daily, daily_col, 10):
                                        if open_none_flag:
                                            break
                                        pydirectinput.keyDown('f')
                                        pydirectinput.keyUp('f')
                                        if not detect_color(mystery_box, mystery_box_col, 10):
                                                move(*items)
                                                find_box_in_inventory()
                                        if open_25_flag:
                                            move(*box_use)
                                            move(*box25)
                                        if open_49_flag:
                                            for _ in range(2):
                                                if not detect_color(mystery_box, mystery_box_col, 10):
                                                        move(*items)
                                                        find_box_in_inventory()
                                                move(*box_use)
                                                move(*box12)
                                                pydirectinput.keyDown('f')
                                                pydirectinput.keyUp('f')
                                                    
                                            move(*box_use)
                                            move(*box25)
                                        if detect_color(box_max, box_max_col, 10):
                                            move(*box_max)
                                            time.sleep(0.2)
                                            pydirectinput.press('f')
                                            time.sleep(0.1)
                                            break
                                        break
                                    pydirectinput.click()
                                    time.sleep(0.1)
                                hatching_click_flag = False
                                open_comp_def()
                                rerolled_left = False
                                rerolled_right = False
                                hatching_phase = False
                                mythic_detect_count = 0
                                left_quest_type = None
                                right_quest_type = None
                    else:
                        pydirectinput.press('e')
                        pydirectinput.click()
                time.sleep(0.08)
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


# Start the hatching clicker thread
click_thread = threading.Thread(target=hatching_clicker, daemon=True)
click_thread.start()

with keyboard.Listener(on_press=toggle_switch) as listener:
    action_thread = threading.Thread(target=action_loop)
    action_thread.daemon = True
    action_thread.start()
    listener.join()