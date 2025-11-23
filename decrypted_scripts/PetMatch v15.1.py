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
version = "13.1"
# DESCRIPTION: Match pets in the Pet Match minigame
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
    top_left = (0, 300)
    bottom_right = (2188, 1000)
    absolute_bottom_right = (2560, 1440)
    insane_btn = (1264, 994)
    game_run = (2305, 146)
    leave = (1165, 874)
    center = (1280, 720)
    insane_get_ss = (615, 1068)
    claim = ['claim.png']
    skip = ['skip.png', 'skip_hover.png']
    insane = ['insane.png']
    easy_get_ss = (1446, 346)
    insane_tl = [
    (600, 360), (770, 360), (940, 360), (1110, 360), (1290, 360), (1460, 360), (1640, 360), (1810, 360), (598, 608), (770, 608), (942, 608), (1117, 608),
    (1289, 608), (1464, 608), (1639, 608), (1811, 608), (596, 858), (768, 858), (940, 858), (1118, 858), (1291, 858), (1465, 858), (1638, 858), (1812, 858)
    ]
    insane_br = [
        (740, 580), (910, 580), (1090, 580), (1260, 580), (1440, 580), (1610, 580), (1790, 580), (1960, 580), (744, 833), (920, 833), (1094, 823), (1268, 833),
        (1443, 833), (1615, 833), (1790, 833), (1963, 833), (745, 1084), (920, 1084), (1095, 1084), (1268, 1084), (1442, 1084), (1617, 1084), (1790, 1084), (1966, 1084)
    ]
    easy = (1019, 936)
    easy_tl = [(897, 340), (1167, 340), (1438, 340), (893, 740), (1165, 740), (1436, 740)]
    easy_br = [(1122, 690), (1393, 690), (1667, 690), (1122, 1100), (1397, 1100), (1671, 1100)]
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    top_left = (0, 300)
    bottom_right = (1660, 759)
    absolute_bottom_right = (1920, 1080)
    insane_btn = (948, 778)
    game_run = (1728, 106)
    leave = (862, 674)
    center = (960, 540)
    insane_get_ss = (419, 841)
    claim = ['claim2.png']
    skip = ['skip2.png', 'skip_hover2.png']
    insane = ['insane2.png']
    easy_get_ss = (1104, 212)
    insane_tl = [
        (365, 220), (514, 220), (664, 220), (816, 220), (970, 220), (1123, 220), (1272, 220), (1425, 220), (363, 440), (515, 440), (666, 440), (816, 440),
        (973, 440), (1124, 440), (1275, 440), (1427, 440), (362, 660), (516, 660), (666, 660), (818, 660), (972, 660), (1124, 660), (1273, 660), (1425, 660)
    ]
    insane_br = [
        (491, 420), (642, 420), (796, 420), (949, 420), (1101, 420), (1253, 420), (1405, 420), (1558, 420), (490, 638), (643, 638), (793, 638), (948, 638),
        (1101, 638), (1253, 638), (1405, 638), (1557, 638), (491, 858), (645, 858), (796, 858), (947, 858), (1100, 858), (1253, 858), (1405, 858), (1559, 858)
    ]
    easy = (733, 717)
    easy_tl = [(621, 209), (861, 209), (1099, 208), (621, 556), (862, 557), (1098, 559)]
    easy_br = [(822, 517), (1059, 518), (1299, 517), (821, 867), (1060, 869), (1300, 870)]
elif screen_width == 1366 and screen_height == 768:
    res_info = 1366
    top_left = (0, 200) #
    bottom_right = (1366, 768) #
    absolute_bottom_right = (1366, 768) #
    insane_btn = (679, 569) #
    game_run = (1231, 75) #
    leave = (607, 492) #
    center = (683, 384) #
    insane_get_ss = (742, 148) #
    claim = ['claim3.png'] #
    skip = ['skip3.png', 'skip_hover3.png'] #
    insane = ['insane3.png'] #
    easy_get_ss = (934, 138) #
    insane_tl = [
        (221, 141), (339, 141), (460, 141), (578, 141), (696, 141), (815, 141), (934, 141), (1054, 141),
        (221, 311), (340, 311), (458, 311), (576, 311), (697, 311), (815, 311), (934, 311), (1054, 311),
        (221, 481), (340, 481), (457, 481), (577, 481), (696, 481), (816, 481), (935, 481), (1053, 481)
    ] #
    insane_br = [
        (313, 284), (432, 284), (553, 284), (670, 284), (791, 284), (909, 284), (1027, 284), (1147, 284),
        (313, 455), (431, 455), (551, 455), (669, 455), (789, 455), (908, 455), (1029, 455), (1146, 455),
        (313, 625), (434, 625), (551, 625), (671, 625), (790, 625), (908, 625), (1027, 625), (1146, 625)
    ] #
    easy = (505, 517) #
    easy_tl = [(416, 125), (603, 123), (789, 123), (417, 394), (602, 393), (788, 392)] #
    easy_br = [(580, 322), (766, 322), (950, 322), (580, 591), (765, 593), (951, 593)] #
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

TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3

running_flag = False
total_time = ""
minigame = 0
minigame_fail = 0
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

def claim_function(found):
    global minigame
    minigame += 1
    pydirectinput.press('space')
    move(*found)
    for _ in range(3):
        pydirectinput.click()
        time.sleep(0.15)
    pydirectinput.mouseUp()
    time.sleep(0.5)

def skip_function(found):
    move(found[0] + 6, found[1])
    time.sleep(0.5)

def insane_function(found):
    if ans == 1:
        move(*easy)
    else:
        move(*found)
    time.sleep(1)
    if ans == 1:
        move(*easy)
    else:
        move(*insane_btn)
    cls()
    print(f'PetMatch {version} by Lisek_guy2')
    print('')
    print(f'Total Playtime: {total_time}')
    print(f'Games won: {minigame} Games lost: {minigame_fail}')

cls()
difficulty = input("1 - EASY MODE\n2 - INSANE MODE\n\nChoose difficulty: ")
if difficulty not in ['1', '2']:
    ans = 1
else:
    ans = int(difficulty)
cls()
print(f'PetMatch {version} by Lisek_guy2')
print('')
print("Macro running correctly")
print("To start press F2, to stop press F3")
def action_loop():
    global minigame, center, minigame_fail, ans, running_flag, total_time
    while True:
        if running_flag:
            move(center[0], center[1] - 300)
            timeout = time.time() + 15
            while time.time() < timeout:
                found_claim = image(top_left, absolute_bottom_right, claim[0])
                if found_claim:
                    claim_function(found_claim)
                found_skip = image(top_left, absolute_bottom_right, skip[0]) or image(top_left, absolute_bottom_right, skip[1])
                if found_skip:
                    skip_function(found_skip)
                    time.sleep(0.2)
                found_insane = image(top_left, absolute_bottom_right, insane[0])
                if found_insane:
                    insane_function(found_insane)
                    time.sleep(1.3)
                    break
                else:
                    pydirectinput.press('space')
                    time.sleep(1.5)
            else:
                print('I have no idea what happened, for some reason u weren\'t in the minigame and no claim/skip/insane button was present')
            timeout = time.time() + 5
            get_ss = easy_get_ss if ans == 1 else insane_get_ss
            while time.time() < timeout:
                if detect_color(get_ss, (255, 255, 255), 5):
                    time.sleep(0.2)
                    break
                else:
                    time.sleep(0.1)
                    
            while detect_color(game_run, (255, 255, 255), 5):
                print("Checking for pets")
                full_screenshot = ImageGrab.grab()
                full_screenshot_cv = cv2.cvtColor(np.array(full_screenshot), cv2.COLOR_RGB2BGR)

                cropped_images = []
                cropped_positions = []
                full_images = []
                full_positions = []
                top_left_coords = easy_tl if ans == 1 else insane_tl
                bottom_right_coords = easy_br if ans == 1 else insane_br
                for (tl, br) in zip(top_left_coords, bottom_right_coords):
                    full_img_cv = full_screenshot_cv[tl[1]:br[1], tl[0]:br[0]]
                    full_images.append(full_img_cv)
                    full_positions.append((tl[0], tl[1], br[0], br[1]))

                    left = tl[0] + 10
                    top = tl[1] + 10
                    right = br[0] - 10
                    bottom = br[1] - 10
                    cropped_img_cv = full_screenshot_cv[top:bottom, left:right]
                    cropped_images.append(cropped_img_cv)
                    cropped_positions.append((left, top, right, bottom))

                matched_pairs = []
                threshold = 0.9
                for i in range(len(cropped_images)):
                    for j in range(len(full_images)):
                        if i == j:
                            continue
                        img1 = cropped_images[i]
                        img2 = full_images[j]
                        if img1.shape[0] < img2.shape[0] or img1.shape[1] < img2.shape[1]:
                            img1, img2 = img2, img1
                        res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                        if max_val >= threshold:
                            matched_pairs.append((i, j))

                clicked_pairs = set()

                time.sleep(0.5)
                for idx1, idx2 in matched_pairs:
                    pair_key = tuple(sorted((idx1, idx2)))
                    if pair_key in clicked_pairs:
                        continue
                    clicked_pairs.add(pair_key)

                    left1, top1, right1, bottom1 = cropped_positions[idx1]
                    left2, top2, right2, bottom2 = full_positions[idx2]

                    pair1_x = left1 + (right1 - left1) // 2
                    pair1_y = top1 + (bottom1 - top1) // 2
                    pair2_x = left2 + (right2 - left2) // 2
                    pair2_y = top2 + (bottom2 - top2) // 2

                    print(f"Found pair at ({pair1_x}, {pair1_y}) and ({pair2_x}, {pair2_y})")

                    move(pair1_x, pair1_y)
                    move(pair2_x, pair2_y)
                    time.sleep(0.5)

                time.sleep(4)
                if detect_color(game_run, (255, 255, 255), 5):
                    minigame_fail += 1
                    print("Match clearing failed, exiting game")
                    move(*game_run)
                    time.sleep(0.5)
                    move(*leave)
                    time.sleep(3)
                    break

                print("Game Finished")
                time.sleep(1)
        else:
            time.sleep(0.4)

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
        pydirectinput.mouseUp()
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
