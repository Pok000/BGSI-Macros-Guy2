from pynput import keyboard
from PIL import ImageGrab
import pydirectinput
import pyautogui
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
import requests
import tkinter as tk  # Added for overlay dots

version = "v28.1"
# DESCRIPTION: Enchants your whole team to a specific enchant (all enchanting masteries needed)
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
    base_w, base_h = 2560, 1440
    center = (1280, 720)
    start_enchanting = (1168, 834)
    enchanting = (1370, 788)
    change_pet = (895, 450)
    gems = (1056, 828)
    selected_enchants = ['enchant_select_ultra_roller.png', 'enchant_select_secret_hunter.png', 'enchant_select_determination.png', 'enchant_select_shiny_seeker.png', 'enchant_select_high_roller.png', 'enchant_select_bubbler.png', 'enchant_select_team.png']
    side_enchants = ['side_ultra_roller.png', 'side_secret.png', 'side_deter.png', 'side_shiny.png', 'side_high_roller.png', 'side_bubbler.png', 'side_team.png']
    top_left = (735, 670)
    bottom_right = (1052, 1124)
    center_pet = (1271, 575)
    PX_offset = 150
    # dual enchanting
    reroll_top = (990, 880)
    reroll_bottom = (990, 1020)
    top_area = ((750, 772), (1042, 870))
    reroll_area = ((936, 630), (1620, 950))
    GUI_reroll = (1163, 854)
    GUI_exit = (1390, 858)
    reroll_button_png = "reroll_button.PNG"
    reroll_check_coord = (777, 445)
    secret_text = 'secret_text.png'
    text_area = (805, 453, 1762, 917)
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    base_w, base_h = 1920, 1080
    center = (960, 540)
    start_enchanting = (863, 635)
    enchanting = (1037, 603)
    change_pet = (622, 300)
    gems = (765, 635)
    selected_enchants = ['enchant_select_ultra_roller2.png', 'enchant_select_secret_hunter2.png', 'enchant_select_determination2.png', 'enchant_select_shiny_seeker2.png', 'enchant_select_high_roller2.png', 'enchant_select_bubbler2.png', 'enchant_select_team2.png']
    side_enchants = ['side_ultra_roller2.png', 'side_secret2.png', 'side_deter2.png', 'side_shiny2.png', 'side_high_roller2.png', 'side_bubbler2.png', 'side_team2.png']
    top_left = (482, 571)
    bottom_right = (759, 889)
    center_pet = (955, 404)
    PX_offset = 130
    # dual enchanting
    reroll_top = (707, 683)
    reroll_bottom = (701, 800)
    top_area = ((499, 586), (752, 666))
    reroll_area = ((666, 456), (1254, 705))
    GUI_reroll = (862, 657)
    GUI_exit = (1062, 657)
    reroll_button_png = "reroll_button2.PNG"
    reroll_check_coord = (519, 303)
    secret_text = 'secret_text2.png'
    text_area = (543, 311, 1381, 737)
elif screen_width == 1366 and screen_height == 768:
    res_info = 1366
    base_w, base_h = 1366, 768
    center = (683, 384)
    start_enchanting = (607, 456)
    enchanting = (743, 430)
    change_pet = (420, 200)
    gems = (524, 459)
    selected_enchants = ['enchant_select_ultra_roller3.png', 'enchant_select_secret_hunter3.png', 'enchant_select_determination3.png', 'enchant_select_shiny_seeker3.png', 'enchant_select_high_roller3.png', 'enchant_select_bubbler3.png', 'enchant_select_team3.png']
    side_enchants = ['side_ultra_roller3.png', 'side_secret3.png', 'side_deter3.png', 'side_shiny3.png', 'side_high_roller3.png', 'side_bubbler3.png', 'side_team3.png']
    top_left = (312, 369)
    bottom_right = (529, 657)
    PX_offset = 100
    # dual enchanting
    reroll_top = (483, 492)
    reroll_bottom = (486, 585)
    top_area = ((324, 419), (520, 484))
    reroll_area = ((453, 330), (915, 491))
    GUI_reroll = (607, 473)
    GUI_exit = (761, 472)
    reroll_button_png = "reroll_button3.PNG"
    reroll_check_coord = (337, 196)
    secret_text = 'secret_text3.png'
    text_area = (360, 203, 1010, 535)
    center_pet = (680, 281)
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
pet_count = 0
afk = 0
click_count = 0
enchanting_col = (222, 40, 74)
reroll_check_color = (225, 243, 255)
total_pets = 0
text_match_threshold = 0.7
dual_enchant = False
first_enchant_idx = 0
second_enchant_idx = 0
target_alternative = False
alternative_enchant_idx = 0
pet_slots = []
overlay_start = False
overlay_req = threading.Event()
overlay_cap = threading.Event()
overlay_capd = threading.Event()
slot_coords = []

def calc_pos(bx, by, sx, sy, slots):
    positions = []
    rows = (slots + 4) // 5
    for row in range(rows):
        y_offset = by + row * sy
        dots_in_row = min(5, slots - row * 5)
        pos_r = []
        if dots_in_row == 1:
            pos_r.append((bx, y_offset))
        elif dots_in_row == 2:
            pos_r.append((bx - sx // 2, y_offset))
            pos_r.append((bx + sx // 2, y_offset))
        elif dots_in_row == 3:
            pos_r.append((bx - sx, y_offset))
            pos_r.append((bx, y_offset))
            pos_r.append((bx + sx, y_offset))
        elif dots_in_row == 4:
            pos_r.append((bx - sx - sx // 2, y_offset))
            pos_r.append((bx - sx // 2, y_offset))
            pos_r.append((bx + sx // 2, y_offset))
            pos_r.append((bx + sx + sx // 2, y_offset))
        elif dots_in_row == 5:
            pos_r.extend([(bx + i * sx - 2 * sx, y_offset) for i in range(dots_in_row)])
        positions.extend(pos_r)
    return positions

def dot_overlay(slots):
    global overlay_start
    if overlay_start:
        return
    overlay_start = True

    def overlay_thread_main():
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

        root = tk.Tk()
        root.title("slots overlay")
        root.attributes("-topmost", True)
        root.overrideredirect(True)

        TRANSPARENT_COLOR = "magenta"
        try:
            root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        except tk.TclError:
            pass

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        root.geometry(f"{screen_w}x{screen_h}+0+0")

        canvas = tk.Canvas(root, width=screen_w, height=screen_h, bg=TRANSPARENT_COLOR, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        dot_radius = 18
        dot_fill = "#ff3b30"
        dot_outline = "#ffffff"
        dot_outline_width = 3

        SPACING_X = PX_offset
        SPACING_Y = PX_offset
        start_x, start_y = (center_pet[0], center_pet[1])
        positions = calc_pos(start_x, start_y, SPACING_X, SPACING_Y, slots)

        dots_local = []

        def start_drag(event, dot):
            dot["drag"] = True
            dot["start_x"] = event.x
            dot["start_y"] = event.y

        def stop_drag(event, dot):
            dot["drag"] = False

        def drag(event, dot):
            if dot["drag"]:
                dx = event.x - dot["start_x"]
                dy = event.y - dot["start_y"]
                canvas.move(dot["id"], dx, dy)
                dot["start_x"] = event.x
                dot["start_y"] = event.y

        for x, y in positions:
            x0, y0 = x - dot_radius, y - dot_radius
            x1, y1 = x + dot_radius, y + dot_radius
            dot_id = canvas.create_oval(x0, y0, x1, y1, fill=dot_fill, outline=dot_outline, width=dot_outline_width)
            dot = {"id": dot_id, "drag": False, "start_x": 0, "start_y": 0}
            dots_local.append(dot)
            canvas.tag_bind(dot_id, "<ButtonPress-1>", lambda e, d=dot: start_drag(e, d))
            canvas.tag_bind(dot_id, "<ButtonRelease-1>", lambda e, d=dot: stop_drag(e, d))
            canvas.tag_bind(dot_id, "<B1-Motion>", lambda e, d=dot: drag(e, d))

        def poll_req():
            if overlay_cap.is_set():
                coords = []
                for d in dots_local:
                    x0, y0, x1, y1 = canvas.coords(d["id"])
                    cx = int((x0 + x1) // 2)
                    cy = int((y0 + y1) // 2)
                    coords.append((cx, cy))
                global slot_coords
                slot_coords = coords
                overlay_cap.clear()
                overlay_capd.set()

            if overlay_req.is_set():
                try:
                    root.withdraw()
                except Exception:
                    pass
                overlay_req.clear()

            root.after(50, poll_req)

        poll_req()
        root.mainloop()

    threading.Thread(target=overlay_thread_main, daemon=True).start()

def get_slots(timeout=3.0):
    global pet_slots
    overlay_capd.clear()
    overlay_cap.set()
    if not overlay_capd.wait(timeout=timeout):
        return []
    pet_slots = list(slot_coords)
    return pet_slots

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

log_queue = []
webhook_link = None
webhook_user_id = None
_lock = threading.Lock()
message_id = None
last_sent_pets = -1
webhook = False

def get_status_header():
    try:
        header_lines = [
            f"Processed pets: {pet_count}/{total_pets}",
            f"Time elapsed: {total_time}",
        ]
        return "\n".join(header_lines)
    except Exception:
        return (
            "Processed pets: 0/0\n"
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
    cls()
    print(f"Webhook found: {webhook_link}")
    try:
        DC_ID = input("Enter your Discord USER ID (numbers only). Enter 0 if you don't want to get pinged: ").strip()
        if DC_ID and DC_ID != '0' and DC_ID.isdigit():
            webhook_user_id = DC_ID
        else:
            webhook_user_id = None
    except Exception:
        webhook_user_id = None

def webhook_link_batch():
    global message_id, last_sent_pets

    if not webhook_link:
        return

    if message_id is None:
        try:
            initial = f"```text\n{get_status_header()}\n```"
            response = requests.post(webhook_link + "?wait=true", json={"content": initial})
            if response.status_code == 200:
                message_id = response.json().get("id")
                last_sent_pets = pet_count
            else:
                print(f"[Webhook] Failed to send initial message: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"[Webhook] Exception sending initial message: {e}")
            return

    while True:
        time.sleep(0.5)
        with _lock:
            filtered = [line for line in log_queue if not line.startswith("Processed ")]
            log_queue.clear()
        should_update = filtered or (pet_count != last_sent_pets)
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
                last_sent_pets = pet_count
        except Exception as e:
            print(f"[Webhook] Exception while editing message: {e}")

def save_msg(msg):
    with _lock:
        log_queue.append(msg)

threading.Thread(target=webhook_link_batch, daemon=True).start()

def mention():
    if not webhook_link:
        return
    try:
        mention = f"<@{webhook_user_id}> " if webhook_user_id else ""
        content = f"{mention}The Team Enchant {version} macro finished enchanting {pet_count}/{total_pets} pets in {total_time}."
        requests.post(webhook_link, json={"content": content}, timeout=5)
    except Exception as e:
        print(f"[Webhook] Failed to send final mention: {e}")

def detect_color(coords, target_color, tolerance=20):
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    bgr_color = img[coords[1], coords[0]]
    target_color_bgr = (target_color[2], target_color[1], target_color[0])
    diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
    return np.all(diff <= tolerance)

def find_item(image_path):
    screenshot = ImageGrab.grab()
    screen_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path)
    if template is None:
        print(f"WARNING: no image found: {image_path}")
        return None

    res = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    threshold = 0.8
    if max_val >= threshold:
        bottom_right_x = max_loc[0] + template.shape[1] - 1
        bottom_right_y = max_loc[1] + template.shape[0] - 1
        return (bottom_right_x, bottom_right_y)
    else:
        return None

def find_item_in_area(image_path, top_left, bottom_right):
    left, top = top_left
    right, bottom = bottom_right
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    screen_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path)
    if template is None:
        print(f"WARNING: no image found: {image_path}")
        return None

    res = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    threshold = 0.8
    if max_val >= threshold:
        found_x = left + max_loc[0] + template.shape[1] - 1
        found_y = top + max_loc[1] + template.shape[0] - 1
        return (found_x, found_y)
    else:
        return None

def scroll(direction, amount):
    if direction == 'up':
        pyautogui.scroll(amount)
    elif direction == 'down':
        pyautogui.scroll(-amount)

def got_ench(enchant_idx):
    enchant_image = side_enchants[enchant_idx - 1]
    found = find_item_in_area(enchant_image, top_left, bottom_right)
    return found is not None

def other_ench():
    if target_alternative and alternative_enchant_idx > 0:
        alt_enchant_image = side_enchants[alternative_enchant_idx - 1]
        found = find_item_in_area(alt_enchant_image, top_left, bottom_right)
        return found is not None
    return False

def time_sleep(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        while not running_flag:
            time.sleep(0.05)
        time.sleep(0.05)

def pause_wait():
    while not running_flag:
        time.sleep(0.05)

def enchant(enchant_btn):
    global pet_count, afk, ans, running_flag, click_count
    time_sleep(0.3)
    has_primary = got_ench(ans)
    has_alternative = other_ench() if dual_enchant else False
    
    if has_primary or has_alternative:
        enchant_name = selected_enchants[ans - 1].replace('enchant_select_', '').replace('_', ' ').replace('.png', '')
        if has_alternative:
            alt_enchant_names = ["Ultra Roller", "Secret Hunter", "Determination", "Shiny Seeker", "High Roller", "Bubbler", "Team"]
            alt_name = alt_enchant_names[alternative_enchant_idx - 1]
            enchant_name = alt_name
            
        if dual_enchant:
            print(f"Pet already has {enchant_name} enchant, starting reroll process...")
            start_dual_reroll()
        else:
            print(f"Pet already has {enchant_name} enchant, skipping this pet...")
        
    else:
        move(enchant_btn[0], enchant_btn[1])
        time_sleep(0.3)
        
        move(*start_enchanting)
        time_sleep(0.3)
        
        move(*gems)
        time_sleep(0.5)
        
        while detect_color(enchanting, enchanting_col):
            time_sleep(1)
            afk += 1
            if afk >= 600:
                pause_wait()
                pydirectinput.keyDown('i')
                time.sleep(0.1)
                pydirectinput.keyUp('i')
                time_sleep(0.5)
                pydirectinput.keyDown('o')
                time.sleep(0.3)
                pydirectinput.keyUp('o')
                afk = 0
        
        image_to_check = side_enchants[ans - 1]
        found = find_item_in_area(image_to_check, top_left, bottom_right)
        if found:
            enchant_name = selected_enchants[ans - 1].replace('enchant_select_', '').replace('_', ' ').replace('.png', '')
            print(f"Enchanted pet with {enchant_name} successfully!")
            
            if dual_enchant:
                start_dual_reroll()
                
        else:
            enchant_name = selected_enchants[ans - 1].replace('_', ' ').replace('.png', '')
            print(f"Failed to enchant pet with {enchant_name}. Retrying...")
            enchant(enchant_btn)
    
            pet_count += 1
            print(f'Processed pet {pet_count}/{total_pets}')
            if webhook:
                save_msg(f"Processed {pet_count}/{total_pets}")
    pause_wait()
    move(*change_pet)

def start_dual_reroll():
    if target_alternative:
        has_primary_in_top = find_item_in_area(side_enchants[first_enchant_idx - 1], top_area[0], top_area[1])
        has_alt_in_top = find_item_in_area(side_enchants[alternative_enchant_idx - 1], top_area[0], top_area[1])
        
        if has_primary_in_top or has_alt_in_top:
            reroll_image_name = selected_enchants[second_enchant_idx - 1].replace('enchant_select_', 'reroll_').replace('.png', '.PNG')
            target_enchant_name = selected_enchants[second_enchant_idx - 1].replace('enchant_select_', '').replace('_', ' ').replace('.png', '')
        else:
            reroll_image_name = selected_enchants[second_enchant_idx - 1].replace('enchant_select_', 'reroll_').replace('.png', '.PNG')
            target_enchant_name = selected_enchants[second_enchant_idx - 1].replace('enchant_select_', '').replace('_', ' ').replace('.png', '')
    else:
        reroll_image_name = selected_enchants[second_enchant_idx - 1].replace('enchant_select_', 'reroll_').replace('.png', '.PNG')
        target_enchant_name = selected_enchants[second_enchant_idx - 1].replace('enchant_select_', '').replace('_', ' ').replace('.png', '')
    
    found_in_top = find_item_in_area(side_enchants[first_enchant_idx - 1], top_area[0], top_area[1])
    
    if found_in_top:
        reroll_position = reroll_bottom
        print("First enchant found in top slot, rerolling bottom slot...")
    else:
        reroll_position = reroll_top
        print("First enchant found in bottom slot, rerolling top slot...")

    move(*reroll_position)
    
    while True:
        pause_wait()
        pydirectinput.click()
        time_sleep(0.04)

        found_primary = find_item_in_area(reroll_image_name, reroll_area[0], reroll_area[1])
        found_alternative = False
        if target_alternative and alternative_enchant_idx > 0:
            alt_reroll_image_name = selected_enchants[alternative_enchant_idx - 1].replace('enchant_select_', 'reroll_').replace('.png', '.PNG')
            found_alternative = find_item_in_area(alt_reroll_image_name, reroll_area[0], reroll_area[1])

        if detect_color(reroll_check_coord, reroll_check_color):
            if found_primary or found_alternative:
                final_enchant_name = target_enchant_name
                if found_alternative:
                    enchant_names = ["Ultra Roller", "Secret Hunter", "Determination", "Shiny Seeker", "High Roller", "Bubbler", "Team"]
                    final_enchant_name = enchant_names[alternative_enchant_idx - 1]
                print(f"Successfully got second enchant: {final_enchant_name}")
                pause_wait()
                move(*GUI_exit)
                break
        else:
            if find_item_in_area(reroll_button_png, reroll_area[0], reroll_area[1]):
                if found_primary or found_alternative:
                    final_enchant_name = target_enchant_name
                    if found_alternative:
                        enchant_names = ["Ultra Roller", "Secret Hunter", "Determination", "Shiny Seeker", "High Roller", "Bubbler", "Team"]
                        final_enchant_name = enchant_names[alternative_enchant_idx - 1]
                    print(f"Successfully got second enchant: {final_enchant_name}")
                    pause_wait()
                    move(*GUI_exit)
                    break
                else:
                    pause_wait()
                    move(*GUI_reroll)
                    move(*reroll_position)

def get_dual_enchant_option():
    while True:
        cls()
        option = input("Do you want to enchant both slots of each pet?\n\n1 - Yes (Dual enchanting)\n2 - No (Single enchanting)\n\nSelect option: ").strip()
        if option in ['1', '2']:
            return option == '1'
        else:
            print("Invalid input. Please enter 1 for Yes or 2 for No.")

def get_enchant_selection(slot_name=""):
    enchant_names = [
        "Ultra Roller",
        "Secret Hunter", 
        "Determination",
        "Shiny Seeker",
        "High Roller",
        "Bubbler",
        "Team"
    ]
    
    while True:
        cls()
        print(f"Select enchantment{' for ' + slot_name if slot_name else ''}:\n")
        for i, name in enumerate(enchant_names, 1):
            print(f"{i} - {name}")
        
        choice = input(f"\nSelect enchantment{' for ' + slot_name if slot_name else ''}: ").strip()
        if choice in [str(i) for i in range(1, 8)]:
            return int(choice)
        else:
            print("Invalid input. Please enter a number between 1 and 7.")

def get_alternative_enchant_option(selected_enchant, alternative_enchant):
    while True:
        cls()
        print(f"You have selected {selected_enchant} as your second enchant.")
        print(f"Since you're enchanting Secret pets, would you also like to target {alternative_enchant}?")
        print(f"\nThis means the script will accept either {selected_enchant} OR {alternative_enchant} in the second slot.")
        print(f"\n1 - Yes (Target both {selected_enchant} and {alternative_enchant})")
        print(f"2 - No (Only target {selected_enchant})")
        
        choice = input("\nSelect option: ").strip()
        if choice in ['1', '2']:
            return choice == '1'
        else:
            print("Invalid input. Please enter 1 for Yes or 2 for No.")

dual_enchant = get_dual_enchant_option()

if dual_enchant:
    first_enchant_idx = get_enchant_selection("first slot")
    second_enchant_idx = get_enchant_selection("second slot")
    ans = first_enchant_idx
    if second_enchant_idx in [1, 5]:
        enchant_names = ["Ultra Roller", "Secret Hunter", "Determination", "Shiny Seeker", "High Roller", "Bubbler", "Team"]
        selected_name = enchant_names[second_enchant_idx - 1]
        if second_enchant_idx == 1:
            alternative_name = "High Roller"
            alternative_enchant_idx = 5
        else:
            alternative_name = "Ultra Roller" 
            alternative_enchant_idx = 1
            
        target_alternative = get_alternative_enchant_option(selected_name, alternative_name)
else:
    ans = get_enchant_selection()

cls()
print(f'TeamEnchant {version} by Lisek_guy2\n')
while True:
    try:
        slots_input = int(input("Enter number of pet slots (1-14) to place as dots: ").strip())
        if 1 <= slots_input <= 14:
            break
        else:
            print("Please enter a value between 1 and 14.")
    except ValueError:
        print("Invalid number.")

dot_overlay(slots_input)
cls()

print(f'TeamEnchant {version} by Lisek_guy2\n\nMacro running correctly\nTo start press F2, to stop press F3\n')

def action_loop():
    global pet_count, afk
    while True:
        if running_flag:
            selected_enchant = selected_enchants[ans - 1]
            for idx, coord in enumerate(pet_slots, start=1):
                move(*coord)
                time_sleep(0.4)

                move(*center)
                time_sleep(0.3)

                has_primary = got_ench(ans)
                has_alternative = other_ench() if dual_enchant else False
                if has_primary or has_alternative:
                    enchant_name = selected_enchants[ans - 1].replace('enchant_select_', '').replace('_', ' ').replace('.png', '')
                    if has_alternative and dual_enchant and alternative_enchant_idx > 0:
                        alt_names = ["Ultra Roller", "Secret Hunter", "Determination", "Shiny Seeker", "High Roller", "Bubbler", "Team"]
                        enchant_name = alt_names[alternative_enchant_idx - 1]
                    if dual_enchant:
                        print(f"Pet already has the {enchant_name} enchant, starting dual enchanting")
                        start_dual_reroll()
                    else:
                        print(f"Pet already has the {enchant_name} enchant, skipping this pet")
                    pet_count += 1
                    print(f'Enchanted pet {pet_count}/{total_pets}\n')
                    pause_wait()
                    move(*change_pet)
                    continue
                
                enchant_btn = find_item(selected_enchant)
                if enchant_btn is None:
                    for _ in range(20):
                        scroll('down', 200)
                        time_sleep(0.2)
                        enchant_btn = find_item(selected_enchant)
                        if enchant_btn is not None:
                            break
                    if enchant_btn is not None:
                        enchant(enchant_btn)
                else:
                    enchant(enchant_btn)
                    
            print(f'Finished enchanting {pet_count} out of {total_pets} pets')
            if webhook:
                save_msg(f"Finished enchanting {pet_count}/{total_pets} pets in {total_time}")
                mention()
            break
        else:
            time_sleep(0.4)

# on/off switch with f2 and f3 keys
def toggle_switch(key):
    global running_flag, total_time, pet_slots, total_pets, pet_count
    if key == ON_switch:
        if not running_flag:
            if pet_slots and len(pet_slots) > 0:
                running_flag = True
                print(f"Script resumed...".ljust(60), end="\r")
            else:
                captured = get_slots()
                if not captured:
                    ctypes.windll.user32.MessageBoxW(0, "No dots captured. Make sure overlay is visible and dots are placed.", "Capture failed", 0x10)
                    return
                total_pets = len(captured)
                pet_count = 0
                print(f"Captured {total_pets} pet slot(s). Starting...".ljust(60), end="\r")
                overlay_req.set()
                auto_f11()
                running_flag = True
        else:
            running_flag = False
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