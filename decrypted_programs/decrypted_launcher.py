# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: main.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global loading_root  # inserted
global loading_canvas  # inserted
global initialization_step  # inserted
global loading_animation_frame  # inserted
global main_app  # inserted
import urllib.parse
import time
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import requests
import re
import getpass
from tkinter import ttk
import keyboard
import pystray
import random
from decimal import Decimal, getcontext
from string import digits, ascii_uppercase
import platform
import shutil
from Crypto.Cipher import AES
import ctypes
from ctypes import wintypes
import hashlib
import winreg
from PIL import Image, ImageTk, ImageDraw
from Crypto.Util.Padding import pad, unpad
import traceback
import urllib.request
import pythoncom
import win32com.client
import webbrowser
import socket
import struct
import base64
import binascii
import psutil
import uuid
import glob
import math
import ipaddress
loading_animation_frame = 0
loading_canvas = None
loading_root = None

def set_window_icon(window):
    """Set the window icon for any tkinter window (Tk or Toplevel)"""  # inserted
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:  # inserted
            base_path = os.path.dirname(os.path.abspath(__file__))
        icon_png_path = os.path.join(base_path, 'script_icon.png')
        if os.path.exists(icon_png_path):
            img = Image.open(icon_png_path)
            photo = ImageTk.PhotoImage(img)
            window.iconphoto(False, photo)
            if not hasattr(window, '_icon_ref'):
                window._icon_ref = photo
        else:  # inserted
            icon_ico_path = os.path.join(base_path, 'script_icon.ico')
            if os.path.exists(icon_ico_path):
                window.iconbitmap(icon_ico_path)
    except Exception as e:
        print(f'Failed to set window icon: {e}')
        return

def get_user_ip():
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'text/plain, */*;q=0.1'}

    def valid_ip(text, family=None):
        try:
            ip_obj = ipaddress.ip_address(text.strip())
            if family is None:
                return True
            if family == 4 and isinstance(ip_obj, ipaddress.IPv4Address):
                return True
        except Exception:
            pass  # postinserted
        else:  # inserted
            if family == 6 and isinstance(ip_obj, ipaddress.IPv6Address):
                return True
        else:  # inserted
            return False
                return False
            else:  # inserted
                pass
    ipv4_services = ['https://ipv4.icanhazip.com', 'https://v4.ident.me', 'https://api.ipify.org?format=text', 'https://checkip.amazonaws.com']
    generic_services = ['https://ifconfig.me/ip', 'https://ifconfig.co/ip', 'https://ipinfo.io/ip', 'https://api.my-ip.io/ip', 'https://icanhazip.com']
    for svc in ipv4_services:
        try:
            resp = requests.get(svc, timeout=6, headers=headers)
            if resp.ok and valid_ip(resp.text, family=4):
                return resp.text.strip()
        except requests.exceptions.RequestException:
            pass  # postinserted
    else:  # inserted
        for svc in generic_services:
            try:
                resp = requests.get(svc, timeout=10, headers=headers)
                if resp.ok:
                    txt = resp.text.strip()
                    if valid_ip(txt, family=4):
                        return txt
    except requests.exceptions.RequestException:
                    if valid_ip(txt, family=6):
                        return txt
        else:  # inserted
            try:
                result = subprocess.run(['nslookup', 'myip.opendns.com', 'resolver1.opendns.com'], capture_output=True, text=True, timeout=6, shell=False)
                if result.returncode == 0:
                    candidates = []
                    for line in result.stdout.splitlines():
                        if 'Address:' in line and 'resolver1.opendns.com' not in line and ('::1' not in line):
                            pass  # postinserted
        except Exception:
                        else:  # inserted
                            ip = line.split('Address:')[(-1)].strip()
                            if valid_ip(ip, family=4):
                                candidates.append(ip)
                            else:  # inserted
                                if valid_ip(ip, family=6):
                                    pass  # postinserted
                                else:  # inserted
                                    candidates.append(ip)
                    else:  # inserted
                        if candidates:
                            for ip in candidates:
                                if valid_ip(ip, family=4):
                                    pass  # postinserted
                                else:  # inserted
                                    return ip
                            else:  # inserted
                                return candidates[(-1)]
            else:  # inserted
                return None
        pass
    else:  # inserted
        pass
        pass
    else:  # inserted
        pass
        return None
    else:  # inserted
        pass

def create_composite_loading_screen():
    """Create a single image with logo positioned on rounded background"""  # inserted
    width, height = (400, 360)
    composite = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(composite)
    box_width, box_height = (380, 280)
    box_x = (width - box_width) // 2
    box_y = height - box_height - 10
    draw.rounded_rectangle([(box_x, box_y), (box_x + box_width - 1, box_y + box_height - 1)], radius=20, fill=(68, 68, 68, 255))
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:  # inserted
            base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_path, 'script_icon.png')
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((120, 120), Image.LANCZOS)
            logo_x = (width - 120) // 2
            logo_y = 0
            if logo_img.mode == 'RGBA':
                composite.paste(logo_img, (logo_x, logo_y), logo_img)
            else:  # inserted
                composite.paste(logo_img, (logo_x, logo_y))
        else:  # inserted
            print('Logo file not found, creating placeholder')
            draw.ellipse([(140, 0), (260, 120)], fill=(255, 165, 0, 255))
    except Exception as e:
        pass  # postinserted
    else:  # inserted
        return ImageTk.PhotoImage(composite)
        print(f'Failed to load logo: {e}')
        draw.ellipse([(140, 0), (260, 120)], fill=(255, 165, 0, 255))

def create_loading_screen():
    """Create and show the loading screen - exact implementation from loading.py"""  # inserted
    global loading_canvas  # inserted
    global loading_animation_frame  # inserted
    global loading_root  # inserted
    loading_animation_frame = 0
    ANIMATION_SPEED = 1
    CIRCLE_RADIUS = 60
    NUM_DOTS = 12

    def animate_dna_circle():
        global loading_animation_frame  # inserted
        try:
            if not loading_root.winfo_exists():
                return
            loading_canvas.delete('all')
        except:
            return
        else:  # inserted
            pass  # postinserted
        canvas_width = 200
        canvas_height = 200
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        for i in range(NUM_DOTS):
            base_angle = i / NUM_DOTS * 2 * math.pi
            helix_angle1 = (loading_animation_frame * 0.15 + i * 30) * math.pi / 180
            helix_angle2 = helix_angle1 + math.pi
            x_base = center_x + math.cos(base_angle) * CIRCLE_RADIUS
            y_base = center_y + math.sin(base_angle) * CIRCLE_RADIUS
            spiral_radius = 8
            x1 = x_base + math.cos(helix_angle1) * spiral_radius
            y1 = y_base + math.sin(helix_angle1) * spiral_radius
            size1 = 3 + math.sin(helix_angle1 * 2) * 2
            x2 = x_base + math.cos(helix_angle2) * spiral_radius
            y2 = y_base + math.sin(helix_angle2) * spiral_radius
            size2 = 3 + math.sin(helix_angle2 * 2) * 2
            alpha1 = 0.3 + 0.7 * (1 + math.sin(helix_angle1)) / 2
            alpha2 = 0.3 + 0.7 * (1 + math.sin(helix_angle2)) / 2
            yellow_intensity = int(255 * alpha1)
            orange_r = int(255 * alpha2)
            orange_g = int(140 * alpha2)
            color1 = f'#{yellow_intensity:02x}{yellow_intensity:02x}{0:02x}'
            color2 = f'#{orange_r:02x}{orange_g:02x}{0:02x}'
            loading_canvas.create_oval(x1 - size1, y1 - size1, x1 + size1, y1 + size1, fill=color1, outline='')
            loading_canvas.create_oval(x2 - size2, y2 - size2, x2 + size2, y2 + size2, fill=color2, outline='')
        loading_animation_frame += 1
        try:
            if loading_root.winfo_exists():
                loading_root.after(ANIMATION_SPEED, animate_dna_circle)
        except:
            return None
    loading_root = tk.Tk()
    loading_root.title('Loading Screen')
    set_window_icon(loading_root)
    loading_root.update_idletasks()
    screen_width = loading_root.winfo_screenwidth()
    screen_height = loading_root.winfo_screenheight()
    window_width = 400
    window_height = 420
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    loading_root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    loading_root.overrideredirect(True)
    loading_root.wm_attributes('-topmost', True)
    transparent_color = '#123456'
    loading_root.config(bg=transparent_color)
    loading_root.wm_attributes('-transparentcolor', transparent_color)
    composite_image = create_composite_loading_screen()
    main_label = tk.Label(loading_root, image=composite_image, bg=transparent_color, bd=0, highlightthickness=0)
    main_label.place(relx=0.5, rely=0.5, anchor='center')
    main_label.image = composite_image
    loading_canvas = tk.Canvas(loading_root, width=200, height=200, bg='#444', highlightthickness=0)
    loading_canvas.place(relx=0.5, rely=0.6, anchor='center')
    text_label = tk.Label(loading_root, text='LOADING THE LAUNCHER', font=('Arial', 12, 'bold'), fg='white', bg='#444', justify='center')
    text_label.place(relx=0.5, rely=0.6, anchor='center')
    animate_dna_circle()
    return loading_root
BLACKLIST_KEY_RAW = b'aK3pQv9XmRzT1bHnW6LuF2YgDeCsJ4'
BLACKLIST_KEY = hashlib.sha256(BLACKLIST_KEY_RAW).digest()
REMOTE_BASE_URL = 'https://guy2-macros.com/launcher/'
home_dir = os.path.expanduser('~')
SCRIPTS_DIR = os.path.join(home_dir, 'GUY2 Macros', 'Macros')

def get_remote_version():
    """Get the remote version from the server"""  # inserted
    try:
        with urllib.request.urlopen(REMOTE_BASE_URL + 'version_main.txt') as response:
            pass  # postinserted
    except Exception as e:
            return response.read().decode().strip()
            print(f'Failed to fetch remote version: {e}')

def get_local_version():
    """Get the local version from file"""  # inserted
    local_version_path = os.path.join(SCRIPTS_DIR, 'version_main.txt')
    if os.path.exists(local_version_path):
        with open(local_version_path, 'r') as f:
            return f.read().strip()

def check_version_and_update():
    """Check if update is needed and launch launcher if required"""  # inserted
    if not os.path.exists(SCRIPTS_DIR):
        os.makedirs(SCRIPTS_DIR, exist_ok=True)
    remote_version = get_remote_version()
    local_version = get_local_version()
    if remote_version is None:
        print('Could not fetch remote version, continuing with application...')
        return False
    if remote_version!= local_version:
        print(f'Update needed: Local={local_version}, Remote={remote_version}')
        print('Launching GUY2 Launcher for update...')
        launcher_paths = [os.path.join(SCRIPTS_DIR, 'GUY2 Launcher.exe'), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GUY2 Launcher.exe'), os.path.join(os.path.expanduser('~'), 'Desktop', 'GUY2 Launcher.exe'), os.path.join(os.path.expanduser('~'), 'Downloads', 'GUY2 Launcher.exe')]
        launcher_found = False
        for launcher_path in launcher_paths:
            if os.path.exists(launcher_path):
                try:
                    subprocess.Popen([launcher_path], creationflags=subprocess.CREATE_NO_WINDOW)
                    launcher_found = True
                except Exception as e:
                    pass  # postinserted
                else:  # inserted
                    break
        if not launcher_found:
            print('GUY2 Launcher.exe not found, cannot perform update')
            return False
        sys.exit(0)
    print('Local files are up to date. Continuing with application.')
    return True
            print(f'Failed to launch {launcher_path}: {e}')
        else:  # inserted
            pass
if not check_version_and_update():
    print('Version check failed or update in progress, but continuing with application...')

def xor_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def decrypt_blacklist_file(filepath: str):
    if not os.path.exists(filepath):
        print(f'Blacklist file {filepath} does not exist.')
        return []
    decrypted_guids = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    for line in lines:
        try:
            encrypted_bytes = bytes.fromhex(line.strip())
            decrypted_bytes = xor_decrypt(encrypted_bytes, BLACKLIST_KEY)
            decrypted_guid = decrypted_bytes.decode('utf-8')
            decrypted_guids.append(decrypted_guid)
        except (binascii.Error, UnicodeDecodeError) as e:
            pass  # postinserted
    else:  # inserted
        return decrypted_guids
        print(f'Failed to decrypt line: {line} with error: {e}')

def get_machine_guid():
    try:
        if platform.system() == 'Windows':
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Cryptography') as key:
                pass  # postinserted
    except Exception as fallback_e:
                machine_guid, _ = winreg.QueryValueEx(key, 'MachineGuid')
                return machine_guid
        else:  # inserted
            return str(uuid.uuid1())
            print(f'Failed: {fallback_e}')
            return None
        else:  # inserted
            pass

def show_blacklist_error_and_exit():
    root = tk.Tk()
    root.withdraw()
    error_dialog = tk.Toplevel(root)
    error_dialog.title('Access Denied')
    error_dialog.geometry('400x150')
    error_dialog.configure(bg='#222222')
    error_dialog.resizable(False, False)
    error_dialog.attributes('-topmost', True)
    error_dialog.grab_set()
    set_window_icon(error_dialog)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 180
    x = screen_width // 2 - window_width // 2
    y = screen_height // 2 - window_height // 2
    error_dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')
    label = tk.Label(error_dialog, text='You have been blacklisted.\n\nIf you believe that this was a mistake,\nplease create a ticket.', bg='#222222', fg='white', font=('Arial', 12), justify='center')
    label.pack(expand=True, fill='both', padx=20, pady=20)

    def disable_event():
        return
    error_dialog.protocol('WM_DELETE_WINDOW', disable_event)

    def on_ok():
        error_dialog.destroy()
        root.destroy()
        sys.exit(1)
    ok_button = tk.Button(error_dialog, text='OK', command=on_ok, bg='#444444', fg='white', font=('Arial', 12, 'bold'))
    ok_button.pack(pady=(0, 20))
    root.bind_all('<Key>', lambda e: 'break')
    root.bind_all('<Button>', lambda e: 'break')
    root.mainloop()

def blacklist_check_loop(app):
    while True:
        if check_blacklist():
            app.terminate_all_script_processes()
            app.destroy()
            return
        time.sleep(120)
BLACKLIST_FILE_PATH = 'C:\\Users\\HARDPC\\Documents\\GUY2 MACROS\\blacklist\\blacklist.txt'
decrypted_blacklist = decrypt_blacklist_file(BLACKLIST_FILE_PATH)
machine_guid = get_machine_guid()
if machine_guid and decrypted_blacklist and (machine_guid in decrypted_blacklist):
    show_blacklist_error_and_exit()

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width=100, height=40, cornerradius=10, padding=2, bg='#444444', fg='white', text='', font=None, command=None, vertical_text_offset=0):
        tk.Canvas.__init__(self, parent, width=width, height=height, highlightthickness=0, bg=parent['bg'])
        self.command = command
        self.cornerradius = cornerradius
        self.padding = padding
        self.bg = bg
        self.fg = fg
        self.text = text
        self.font = font if font else ('Arial', 12, 'bold')
        self.width = width
        self.height = height
        self.vertical_text_offset = vertical_text_offset
        self.bind('<ButtonPress-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self._draw_button(bg)

    def _draw_button(self, color):
        self.delete('all')
        radius = self.cornerradius
        padding = self.padding
        w = self.width
        h = self.height
        radius = max(2, radius // 2)
        self.create_arc((padding, padding, padding + 2 * radius, padding + 2 * radius), start=90, extent=90, fill=color, outline=color)
        self.create_arc((w - padding - 2 * radius, padding, w - padding, padding + 2 * radius), start=0, extent=90, fill=color, outline=color)
        self.create_arc((padding, h - padding - 2 * radius, padding + 2 * radius, h - padding), start=180, extent=90, fill=color, outline=color)
        self.create_arc((w - padding - 2 * radius, h - padding - 2 * radius, w - padding, h - padding), start=270, extent=90, fill=color, outline=color)
        self.create_rectangle((padding + radius, padding, w - padding - radius, h - padding), fill=color, outline=color)
        self.create_rectangle((padding, padding + radius, w - padding, h - padding - radius), fill=color, outline=color)
        self.create_text(w // 2, h // 2 + self.vertical_text_offset, text=self.text, fill=self.fg, font=self.font)
        self.config(bg=self.master['bg'])
        if self.text in ['◀', '▶']:
            color = self._lighter_color(self.bg)
            self.delete('all')
            radius = self.cornerradius
            padding = self.padding
            w = self.width
            h = self.height
            radius = max(2, radius // 2)
            self.create_arc((padding, padding, padding + 2 * radius, padding + 2 * radius), start=90, extent=90, fill=color, outline=color)
            self.create_arc((w - padding - 2 * radius, padding, w - padding, padding + 2 * radius), start=0, extent=90, fill=color, outline=color)
            self.create_arc((padding, h - padding - 2 * radius, padding + 2 * radius, h - padding), start=180, extent=90, fill=color, outline=color)
            self.create_arc((w - padding - 2 * radius, h - padding - 2 * radius, w - padding, h - padding), start=270, extent=90, fill=color, outline=color)
            self.create_rectangle((padding + radius, padding, w - padding - radius, h - padding), fill=color, outline=color)
            self.create_rectangle((padding, padding + radius, w - padding, h - padding - radius), fill=color, outline=color)
            self.create_text(w // 2, h // 2, text=self.text, fill=self.fg, font=self.font)

    def _on_press(self, event):
        self._draw_button(self._darker_color(self.bg))

    def _on_release(self, event):
        self._draw_button(self.bg)
        if self.command:
            self.command()

    def _on_enter(self, event):
        if hasattr(self, 'bg'):
            self._draw_button(self._lighter_color(self.bg))
        else:  # inserted
            self._draw_button(self._lighter_color('#AA2222'))

    def _on_leave(self, event):
        if hasattr(self, 'bg'):
            self._draw_button(self.bg)
        else:  # inserted
            self._draw_button('#AA2222')

    def _darker_color(self, color):
        color = color.lstrip('#')
        color = len(color)
        rgb = tuple((int(color[i:i + lv // 3], 16) for i in range(0, color, color // 3)))
        darker = tuple((max(0, int(c * 0.8)) for c in rgb))
        return '#%02x%02x%02x' % darker

    def _lighter_color(self, color):
        color = color.lstrip('#')
        color = len(color)
        rgb = tuple((int(color[i:i + lv // 3], 16) for i in range(0, color, color // 3)))
        lighter = tuple((min(255, int(c * 1.2)) for c in rgb))
        return '#%02x%02x%02x' % lighter
if getattr(sys, 'frozen', False):
    os.environ['PYTHONPATH'] = os.path.dirname(sys.executable)
    sys.executable = sys.executable
USERNAME = getpass.getuser()
home_dir = os.path.expanduser('~')
SCRIPTS_DIR = os.path.join(home_dir, 'GUY2 Macros', 'Macros')
EXECUTOR_PATH = os.path.join(SCRIPTS_DIR, 'run.exe')
if not os.path.exists(SCRIPTS_DIR):
    os.makedirs(SCRIPTS_DIR)
MACROS_DIR = os.path.join(SCRIPTS_DIR, 'BGSI_macros')
os.makedirs(MACROS_DIR, exist_ok=True)

def migrate_macros_to_subdir():
    """Move all .py and .png files from SCRIPTS_DIR root into MACROS_DIR."""  # inserted
    try:
        for name in os.listdir(SCRIPTS_DIR):
            src_path = os.path.join(SCRIPTS_DIR, name)
            if not os.path.isfile(src_path):
                continue
            if not name.lower().endswith('.py') and (not name.lower().endswith('.png')):
                continue
            if os.path.abspath(os.path.dirname(src_path)) == os.path.abspath(MACROS_DIR):
                continue
            dst_path = os.path.join(MACROS_DIR, name)
    except Exception as e:
        else:  # inserted
            try:
                if os.path.exists(dst_path):
                    os.remove(dst_path)
                shutil.move(src_path, dst_path)
                print(f'[MIGRATE] Moved {name} -> BGSI_macros/')
            except Exception as e:
                pass  # postinserted
            print(f'[MIGRATE] Failed moving {name}: {e}')
            pass
            print(f'[MIGRATE] Migration error: {e}')
REMOTE_SCRIPTS_JSON_URL = 'https://guy2-macros.com/scripts/macros.json'
MACROS_IMAGES_JSON_URL = 'https://guy2-macros.com/images/images.json'
MACRO_USAGE_API_URL = 'https://discordbot-production-914b.up.railway.app/api/macro-usage'
MAIN_EXE_URL = 'https://github.com/LisekGuy2/Launcher/releases/download/launcher/main.exe'
RUN_EXE_URL = 'https://github.com/LisekGuy2/Launcher/releases/download/launcher/run.exe'
KEYBINDS_FILE = os.path.join(SCRIPTS_DIR, 'keybinds.json')
FREE_RUN_WHITELIST = {'fasthatch'}
OBFUSCATION_KEY_RAW = BLACKLIST_KEY_RAW

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind('<Enter>', self.show_tip)
        widget.bind('<Leave>', self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return None
        x, y, _cx, cy = self.widget.bbox('insert')
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f'+{x}+{y}')
        set_window_icon(tw)
        label = tk.Label(tw, text=self.text, justify='left', background='lightyellow', relief='solid', borderwidth=1, font=('Arial', 10))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class ScriptLauncher(tk.Tk):
    def close_other_instances(self):
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        EnumWindows = user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        self = user32.GetWindowTextLengthW
        GetWindowTextLengthW = user32.GetWindowTextW
        GetWindowTextW = user32.IsWindowVisible
        IsWindowVisible = user32.PostMessageW
        PostMessageW = 16

        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLengthW(hwnd)
                if length > 0:
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    GetWindowTextW(hwnd, buffer, length + 1)
                    window_title = buffer.value
                    if window_title == 'GUY2 MACROS' and hwnd!= self.winfo_id():
                        PostMessageW(hwnd, WM_CLOSE, 0, 0)
            return True
        EnumWindows(EnumWindowsProc(foreach_window), 0)

    def show_keybinds_menu(self):
        """Show the keybinds configuration menu"""  # inserted
        self.keybinds_dialog = tk.Toplevel(self)
        self.keybinds_dialog.title('Configure Keybinds')
        self.keybinds_dialog.geometry('400x300')
        self.keybinds_dialog.configure(bg='#222222')
        self.keybinds_dialog.resizable(False, False)
        self.keybinds_dialog.transient(self)
        self.keybinds_dialog.grab_set()
        set_window_icon(self.keybinds_dialog)
        self.keybinds_dialog.update_idletasks()
        screen_width = self.keybinds_dialog.winfo_screenwidth()
        screen_height = self.keybinds_dialog.winfo_screenheight()
        size = tuple((int(_) for _ in self.keybinds_dialog.geometry().split('+')[0].split('x')))
        x = screen_width // 2 - size[0] // 2
        y = screen_height // 2 - size[1] // 2
        self.keybinds_dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
        self.on_key = None
        self.off_key = None
        self.waiting_for_key = None
        on_frame = tk.Frame(self.keybinds_dialog, bg='#222222')
        on_frame.pack(pady=(20, 10), padx=20, fill='x')
        on_label = tk.Label(on_frame, text='ON KEYBIND:', bg='#222222', fg='white', font=('Arial', 12, 'bold'))
        on_label.pack(anchor='w')
        self.on_key_var = tk.StringVar()
        self.on_key_var.set('[Not set]')
        self.on_key_label = tk.Label(on_frame, textvariable=self.on_key_var, bg='#222222', fg='#AAAAAA', font=('Arial', 11))
        self.on_key_label.pack(pady=(5, 0), fill='x')
        on_set_btn = RoundedButton(on_frame, width=100, height=25, cornerradius=8, bg='#333333', fg='white', text='Set Key', font=('Arial', 10), command=lambda: self.start_key_listening('on'))
        on_set_btn.pack(pady=(5, 0))
        off_frame = tk.Frame(self.keybinds_dialog, bg='#222222')
        off_frame.pack(pady=(10, 10), padx=20, fill='x')
        off_label = tk.Label(off_frame, text='OFF KEYBIND:', bg='#222222', fg='white', font=('Arial', 12, 'bold'))
        off_label.pack(anchor='w')
        self.off_key_var = tk.StringVar()
        self.off_key_var.set('[Not set]')
        self.off_key_label = tk.Label(off_frame, textvariable=self.off_key_var, bg='#222222', fg='#AAAAAA', font=('Arial', 11))
        self.off_key_label.pack(pady=(5, 0), fill='x')
        off_set_btn = RoundedButton(off_frame, width=100, height=25, cornerradius=8, bg='#333333', fg='white', text='Set Key', font=('Arial', 10), command=lambda: self.start_key_listening('off'))
        off_set_btn.pack(pady=(5, 0))
        buttons_frame = tk.Frame(self.keybinds_dialog, bg='#222222')
        buttons_frame.pack(pady=(30, 20))

        def on_cancel():
            self.keybinds_dialog.destroy()

        def on_apply():
            if not self.on_key or not self.off_key:
                messagebox.showerror('Error', 'Please set both ON and OFF keybinds!')
                return
            if self.on_key == self.off_key:
                messagebox.showerror('Error', 'ON and OFF keybinds cannot be the same!')
                return
            try:
                import json
                data = {'on': self.on_key, 'off': self.off_key}
                with open(KEYBINDS_FILE, 'w', encoding='utf-8') as f:
                    pass  # postinserted
            except Exception as e:
                    json.dump(data, f)
                        self.saved_on_key = self.on_key
                        self.saved_off_key = self.off_key
                    else:  # inserted
                        total_modified = 0
                        folders = self.discover_macro_folders()
                        if not folders:
                            folders = [self.macros_dir]
                        for folder in folders:
                            try:
                                for fn in os.listdir(folder):
                                    if fn.lower().endswith('.py'):
                                        script_path = os.path.join(folder, fn)
                                        if self.modify_script_keybinds_at_path(script_path, self.on_key, self.off_key, silent=True):
                                            pass  # postinserted
                except Exception as e:
                                        else:  # inserted
                                            total_modified += 1
                        else:  # inserted
                            messagebox.showinfo('Success', f'Applied new keybinds to {total_modified} macros.\nFuture downloaded macros will also use them.')
                            self.keybinds_dialog.destroy()
                    print(f'[KEYBINDS] Failed to save keybinds: {e}')
                    print(f'[KEYBINDS] Skipped folder {folder}: {e}')
        cancel_btn = RoundedButton(buttons_frame, width=80, height=35, cornerradius=10, bg='#AA2222', fg='white', text='Cancel', font=('Arial', 12, 'bold'), command=on_cancel)
        cancel_btn.pack(side='left', padx=(0, 20))
        apply_btn = RoundedButton(buttons_frame, width=80, height=35, cornerradius=10, bg='#00AA00', fg='white', text='Apply', font=('Arial', 12, 'bold'), command=on_apply)
        apply_btn.pack(side='left')

    def start_key_listening(self, key_type):
        """Start listening for a key press for the specified key type (on/off)"""  # inserted
        self.waiting_for_key = key_type
        if key_type == 'on':
            self.on_key_var.set('[Press any key...]')
            self.on_key_label.config(fg='yellow')
        else:  # inserted
            self.off_key_var.set('[Press any key...]')
            self.off_key_label.config(fg='yellow')
        self.keybinds_dialog.bind('<KeyPress>', self.on_key_press)
        self.keybinds_dialog.focus_set()

    def on_key_press(self, event):
        """Handle key press events when waiting for a keybind"""  # inserted
        if not self.waiting_for_key:
            return
        key = event.keysym.upper()
        valid_keys = set()
        for i in range(1, 11):
            valid_keys.add(f'F{i}')
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            valid_keys.add(char)
        for digit in '0123456789':
            valid_keys.add(digit)
        if key not in valid_keys:
            messagebox.showerror('Invalid Key', f'\'{key}\' is not a valid key. Only F1-F10, A-Z, and 0-9 are allowed.')
            self.stop_key_listening()
            return
        if self.waiting_for_key == 'on' and self.off_key == key:
            messagebox.showerror('Key in Use', f'\'{key}\' is already used for the OFF keybind!')
            self.stop_key_listening()
            return
        if self.waiting_for_key == 'off' and self.on_key == key:
            messagebox.showerror('Key in Use', f'\'{key}\' is already used for the ON keybind!')
            self.stop_key_listening()
            return
        if self.waiting_for_key == 'on':
            self.on_key = key
            self.on_key_var.set(key)
            self.on_key_label.config(fg='white')
        else:  # inserted
            self.off_key = key
            self.off_key_var.set(key)
            self.off_key_label.config(fg='white')
        self.stop_key_listening()

    def stop_key_listening(self):
        """Stop listening for key presses"""  # inserted
        self.waiting_for_key = None
        self.keybinds_dialog.unbind('<KeyPress>')

    def select_script_for_keybind_modification(self, on_key, off_key, local_files):
        on_key = tk.Toplevel(self)
        on_key.title('Modify Keybinds for Macros')
        on_key.geometry('350x450')
        set_window_icon(on_key)
        on_key.configure(bg='#222222')
        on_key.resizable(False, False)
        on_key.transient(self)
        on_key.grab_set()
        on_key.withdraw()
        title_label = tk.Label(on_key, text='Select macro to modify keybinds:', bg='#222222', fg='white', font=('Arial', 12, 'bold'))
        title_label.pack(pady=(20, 10))
        frame = tk.Frame(on_key, bg='#222222')
        frame.pack(pady=10, padx=20, fill='both', expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        self = tk.Listbox(frame, yscrollcommand=scrollbar.set, bg='#333333', fg='white', selectbackground='#0078D4', font=('Arial', 10))
        self.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.yview)
        self.script_mapping = {}
        unique_base_names = set()
        for script in local_files:
            base_name = script.rsplit(' ', 1)[0] if ' ' in script else script.replace('.py', '')
            unique_base_names.add(base_name)
            self.script_mapping[base_name] = [s for s in local_files if s.startswith(base_name)]
        for base_name in sorted(unique_base_names):
            self.insert(tk.END, base_name)

        def on_script_select():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning('Warning', 'Please select a macro.')
                return
            selected_base_name = listbox.get(selection[0])
            matching_files = self.script_mapping[selected_base_name]
            modified_count = 0
            for filename in matching_files:
                if self.modify_script_keybinds(filename, on_key, off_key, silent=True):
                    modified_count += 1
            messagebox.showinfo('Success', f'Changed keybinds for {modified_count} macros')
            script_dialog.destroy()

        def on_apply_to_all():
            modified_count = 0
            for filename in local_files:
                if self.modify_script_keybinds(filename, on_key, off_key, silent=True):
                    modified_count += 1
            messagebox.showinfo('Success', f'Changed keybinds for {modified_count} macros')
            script_dialog.destroy()

        def on_cancel():
            script_dialog.destroy()
        button_frame = tk.Frame(on_key, bg='#222222')
        button_frame.pack(pady=10)
        apply_all_btn = RoundedButton(button_frame, width=180, height=35, cornerradius=10, bg='#5555FF', fg='white', text='Apply to All Macros', font=('Arial', 12, 'bold'), command=on_apply_to_all)
        apply_all_btn.pack(pady=(0, 10))
        bottom_buttons_frame = tk.Frame(on_key, bg='#222222')
        bottom_buttons_frame.pack(pady=10)
        cancel_btn = RoundedButton(bottom_buttons_frame, width=80, height=35, cornerradius=10, bg='#AA2222', fg='white', text='Cancel', font=('Arial', 12, 'bold'), command=on_cancel)
        cancel_btn.pack(side='left', padx=(0, 20))
        select_btn = RoundedButton(bottom_buttons_frame, width=80, height=35, cornerradius=10, bg='#00AA00', fg='white', text='Select', font=('Arial', 12, 'bold'), command=on_script_select)
        select_btn.pack(side='left')
        on_key.update_idletasks()
        screen_width = on_key.winfo_screenwidth()
        screen_height = on_key.winfo_screenheight()
        dialog_width = on_key.winfo_reqwidth()
        dialog_height = on_key.winfo_reqheight()
        x = screen_width // 2 - dialog_width // 2
        y = screen_height // 2 - dialog_height // 2
        on_key.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')
        on_key.deiconify()

    def modify_script_keybinds(self, script_filename, on_key, off_key, silent=False):
        script_path = os.path.join(self.macros_dir, script_filename)
        return self.modify_script_keybinds_at_path(script_path, on_key, off_key, silent=silent)

    def modify_script_keybinds_at_path(self, script_path, on_key, off_key, silent=False):
        if not os.path.exists(script_path):
            if not silent:
                messagebox.showerror('Error', f'Macro file not found: {os.path.basename(script_path)}')
            return False
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                pass  # postinserted
        except Exception as e:
                lines = f.readlines()

                    def key_to_code(key):
                        if key.startswith('F'):
                            return f'keyboard.Key.{key.lower()}'
                        if key.isalpha():
                            return f'keyboard.KeyCode.from_char(\'{key.lower()}\')'
                        if key.isdigit():
                            return f'keyboard.KeyCode.from_char(\'{key}\')'
                        return f'keyboard.KeyCode.from_char(\'{key.lower()}\')'

                    def key_to_display(key):
                        if key.startswith('F'):
                            return key
                        return f'\\\'{key}\\\''
                    on_code = key_to_code(on_key)
                    off_code = key_to_code(off_key)
                    on_display = key_to_display(on_key)
                    off_display = key_to_display(off_key)
                    modified_on = False
                    modified_off = False
                    modified_print = False
                    for i, line in enumerate(lines):
                        stripped_line = line.strip()
                        if stripped_line.startswith('ON_switch = keyboard.'):
                            lines[i] = f'ON_switch = {on_code}\n'
                            modified_on = True
                        else:  # inserted
                            if stripped_line.startswith('OFF_switch = keyboard.'):
                                lines[i] = f'OFF_switch = {off_code}\n'
                                modified_off = True
                            else:  # inserted
                                if 'To start press ' in line and ', to stop press ' in line:
                                    pass  # postinserted
                                else:  # inserted
                                    import re
                                    pattern = '(To start press )(F\\d+|\\\\\\\'[^\\\']+\\\\\\\'|\\\'[^\\\']+\\\'|[A-Za-z0-9]+)(, to stop press )(F\\d+|\\\\\\\'[^\\\']+\\\\\\\'|\\\'[^\\\']+\\\'|[A-Za-z0-9]+)'

                                    def replace_keys(match):
                                        return f'{match.group(1)}{on_display}{match.group(3)}{off_display}'
                                    new_line = re.sub(pattern, replace_keys, line)
                                    if new_line!= line:
                                        pass  # postinserted
                                    else:  # inserted
                                        lines[i] = new_line
                                        modified_print = True
                    else:  # inserted
                        with open(script_path, 'w', encoding='utf-8') as f:
                            f.writelines(lines)
                                return modified_on or modified_off or modified_print
                if not silent:
                    messagebox.showerror('Error', f'Failed to modify script:\n{e}')
                return False

    def is_special_free_run(self, filename: str) -> bool:
        """Return True if the base macro name is in the free-run whitelist."""  # inserted
        base_name, _ = self.parse_name_version(filename)
        return base_name.strip().lower() in FREE_RUN_WHITELIST

    def _key_to_code(self, key: str) -> str:
        """Map display key to code used in macros (same mapping as used for on-disk edits)."""  # inserted
        if key.startswith('F'):
            return f'keyboard.Key.{key.lower()}'
        if key.isalpha():
            return f'keyboard.KeyCode.from_char(\'{key.lower()}\')'
        if key.isdigit():
            return f'keyboard.KeyCode.from_char(\'{key}\')'
        return f'keyboard.KeyCode.from_char(\'{key.lower()}\')'

    def _key_to_display(self, key: str) -> str:
        if key.startswith('F'):
            return key
        return f'\'{key}\''

    def normalize_keybinds_text(self, text: str, on_key: str, off_key: str) -> str:
        """Return text with ON/OFF keybinds normalized to given keys (in-memory, no file write).\n\n        Mirrors modify_script_keybinds_at_path logic so obfuscation comparison is fair.\n        """  # inserted
        import re
        lines = text.splitlines(keepends=True)
        on_code = self._key_to_code(on_key)
        off_code = self._key_to_code(off_key)
        on_display = self._key_to_display(on_key)
        off_display = self._key_to_display(off_key)
        replaced_on = replaced_off = replaced_print = 0
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line.startswith('ON_switch = keyboard.'):
                lines[i] = f'ON_switch = {on_code}\n'
                replaced_on += 1
            else:  # inserted
                if stripped_line.startswith('OFF_switch = keyboard.'):
                    lines[i] = f'OFF_switch = {off_code}\n'
                    replaced_off += 1
                else:  # inserted
                    if 'To start press ' in line and ', to stop press ' in line:
                        pattern = '(To start press )(F\\d+|\\\\\\\'[^\\\']+\\\\\\\'|\'[^\\\']+\'|[A-Za-z0-9]+)(, to stop press )(F\\d+|\\\\\\\'[^\\\']+\\\\\\\'|\'[^\\\']+\'|[A-Za-z0-9]+)'

                        def replace_keys(match):
                            return f'{match.group(1)}{on_display}{match.group(3)}{off_display}'
                        new_line = re.sub(pattern, replace_keys, line)
                        if new_line!= line:
                            lines[i] = new_line
                            replaced_print += 1
        result = ''.join(lines)
        try:
            print(f'[FREE-RUN][normalize] replaced ON:{replaced_on} OFF:{replaced_off} PRINT:{replaced_print}')
        except Exception:
            pass  # postinserted
        else:  # inserted
            return result
            break
        else:  # inserted
            pass

    def _xor_bytes(self, data: bytes, key: bytes) -> bytes:
        return bytes((b ^ key[i % len(key)] for i, b in enumerate(data)))

    def obfuscate_for_site(self, data: bytes) -> bytes:
        """Return base64-encoded XOR-encrypted bytes, matching site\'s storage format."""  # inserted
        enc = self._xor_bytes(data, OBFUSCATION_KEY_RAW)
        return base64.b64encode(enc)

    def _ensure_raw_entries_map(self):
        """Ensure raw_entries_map is populated with the latest macros.json content."""  # inserted
        if hasattr(self, 'raw_entries_map') and (not self.raw_entries_map):
            try:
                response = requests.get(REMOTE_SCRIPTS_JSON_URL, timeout=10)
                response.raise_for_status()
                raw_filenames = response.json()
                self.raw_entries_map = {}
                for item in raw_filenames:
                    parts = item.split('|')
                    fname = parts[0].strip() if parts else item.strip()
                    self.raw_entries_map[fname] = item
            except Exception as e:
                pass  # postinserted
            print(f'[FREE-RUN] Failed to refresh macros.json: {e}')

    def verify_script_matches_site(self, script_path: str, clean_filename: str) -> bool:
        """Compare local script (after normalizing binds to F2/F3) with the site\'s stored version.\n\n        - If the site stores an obfuscated (XOR+base64) version, we obfuscate the local text\n          with the same key and compare base64 bytes.\n        - If the site stores plaintext, compare plaintext bytes directly.\n        """  # inserted
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                pass  # postinserted
        except Exception as e:
                local_text = f.read()
                    normalized = self.normalize_keybinds_text(local_text, 'F2', 'F3')
                    url = f'https://guy2-macros.com/scripts/{clean_filename}'
                    print(f'[FREE-RUN] Fetching site version for {clean_filename}')
                    resp = requests.get(url, timeout=10)
                    resp.raise_for_status()
                    site_bytes = resp.content.strip()
                    self._ensure_raw_entries_map()
                    raw_entry = getattr(self, 'raw_entries_map', {}).get(clean_filename, '')
                    is_encrypted = raw_entry.count('|') == 3
                    candidates = []
                    if not normalized.endswith('\n'):
                        normalized_nl = normalized + '\n'
                    else:  # inserted
                        normalized_nl = normalized
                    normalized_crlf = normalized_nl.replace('\n', '\r\n')
                    if is_encrypted:
                        cand_b64 = [self.obfuscate_for_site(normalized.encode('utf-8')).strip(), self.obfuscate_for_site(normalized_nl.encode('utf-8')).strip(), self.obfuscate_for_site(normalized_crlf.encode('utf-8')).strip()]
                        for idx, cand in enumerate(cand_b64):
                            if site_bytes == cand:
                                print(f'[FREE-RUN] Obfuscated compare for {clean_filename}: True (variant {idx})')
                                return True
                        else:  # inserted
                            print(f'[FREE-RUN] Obfuscated compare for {clean_filename}: False; site len={len(site_bytes)}, local variants lens={[len(c) for c in cand_b64]}')
                            else:  # inserted
                                try:
                                    print(f'[FREE-RUN] site head: {site_bytes[:60]!r}')
                                    return False
                                except Exception:
                                    pass  # postinserted
                    else:  # inserted
                        cand_plain = [normalized.encode('utf-8'), normalized_nl.encode('utf-8'), normalized_crlf.encode('utf-8')]
                        for idx, cand in enumerate(cand_plain):
                            if site_bytes == cand:
                                print(f'[FREE-RUN] Plain compare for {clean_filename}: True (variant {idx})')
                                return True
                        else:  # inserted
                            print(f'[FREE-RUN] Plain compare for {clean_filename}: False; site len={len(site_bytes)}, local variants lens={[len(c) for c in cand_plain]}')
                            else:  # inserted
                                try:
                                    print(f'[FREE-RUN] site head: {site_bytes[:60]!r}')
                                    return False
                                except Exception:
                                    pass  # postinserted
                return False
                return False
                print(f'[FREE-RUN] Verification error for {clean_filename}: {e}')
                return False

    def __init__(self):
        self.close_other_instances()
        super(ask_user_id, self).__init__()
        self.crypto_key = hashlib.sha256(b'aK3pQv9XmRzT1bHnW6LuF2YgDeCsJ4').digest()
        self.duration_file_path = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'duration')
        self.cmd_processes = []
        self.free_run_pids = set()
        self.script_buttons = {}
        self.visible = True
        self.images_map = {}
        self.macros_dir = MACROS_DIR
        self._game_selected = False
        self.title('GUY2 MACROS')
        self.protocol('WM_DELETE_WINDOW', self.exit)
        self._last_verify_time = 0
        self._verify_cooldown = 15
        self._last_ntp_time = None
        self._last_ntp_update = 0
        self._current_time = None
        set_window_icon(self)
        window_width = 610
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width // 2 - window_width // 2
        y = screen_height // 2 - window_height // 2
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.resizable(False, False)
        self.configure(bg='#222222')
        try:
            import json
            if os.path.exists(KEYBINDS_FILE):
                with open(KEYBINDS_FILE, 'r', encoding='utf-8') as f:
                    pass  # postinserted
        except Exception as e:
                    data = json.load(f)
                    self.saved_on_key = data.get('on')
                    self.saved_off_key = data.get('off')
        else:  # inserted
            keyboard.add_hotkey('f9', self.exit)
            self.protocol('WM_DELETE_WINDOW', self.exit)
            top_bar = tk.Frame(self, bg='#222222')
            top_bar.pack(fill='x', pady=(5, 0))
            top_bar.bind('<Button-1>', self.start_move)
            top_bar.bind('<B1-Motion>', self.do_move)
            btn_font = ('Arial', 12, 'bold')
            left_button_frame = tk.Frame(self, bg='#222222', width=120)
            left_button_frame.pack(side='left', fill='y', padx=(5, 0), pady=5)
            button_container = tk.Frame(left_button_frame, bg='#222222')
            button_container.pack(side='top', fill='x', pady=(0, 2))
            button_container2 = tk.Frame(left_button_frame, bg='#222222')
            button_container2.pack(side='top', fill='x', pady=(0, 0))

            def verify_button_clicked():
                current_time = time.time()
                time_since_last_verify = current_time - self._last_verify_time
                if time_since_last_verify < self._verify_cooldown:
                    remaining_time = int(self._verify_cooldown - time_since_last_verify) + 1
                    messagebox.showwarning('Cooldown Active', f'Please do not verify so often.\n\nPlease wait {remaining_time} more seconds before verifying again.')
                else:  # inserted
                    self._last_verify_time = current_time
                    ask_user_id()

            def ask_user_id():
                def get_verification_code_from_api(discord_id: int) -> str:
                    """Get verification code from Discord bot API instead of local generation"""  # inserted
                    try:
                        machine_guid = get_machine_guid()
                        user_ip = get_user_ip()
                        if not machine_guid:
                            raise Exception('Could not get identifier')
                        if not user_ip:
                            raise Exception('Could not determine your public IP from trusted providers.\n\nThis is usually caused by firewall/proxy blocks, SSL inspection, or IPv6-only networks.\n\nAllow outbound HTTPS to common IP services (api.ipify.org, ipv4.icanhazip.com, checkip.amazonaws.com, ipinfo.io) or configure your system proxy. If your network uses SSL inspection, ensure its root certificate is trusted by Python.')
                    except Exception as e:
                        pass  # postinserted
                    else:  # inserted
                        try:
                            timestamp = int(self.get_ntp_time())
                        except Exception:
                            pass  # postinserted
                        else:  # inserted
                            api_data = {'discordId': str(discord_id), 'machineGuid': machine_guid, 'userIP': user_ip, 'timestamp': timestamp}
                            print('[DEBUG] Requesting verification code from API...')
                            print(f'[DEBUG] Discord ID: {discord_id}')
                            print(f'[DEBUG] Machine GUID: {machine_guid}')
                            print(f'[DEBUG] User IP: {user_ip}')
                            print(f'[DEBUG] Timestamp: {timestamp}')
                            bot_url = 'https://discordbot-production-914b.up.railway.app/api/generate-code'
                        else:  # inserted
                            try:
                                response = requests.post(bot_url, json=api_data, timeout=10, headers={'Content-Type': 'application/json'})
                                if response.status_code == 200:
                                    result = response.json()
                                    if result.get('success'):
                                        verification_code = result.get('verificationCode')
                                        print('[DEBUG] Successfully received verification code from API')
                                        return verification_code
                                    print(f"[DEBUG] API returned error: {result.get('error')}")
                                    raise Exception(f"API error: {result.get('error')}")
                                print(f'[DEBUG] API request failed with status: {response.status_code}')
                                raise Exception(f'API request failed with status: {response.status_code}')
                        except requests.exceptions.RequestException as e:
                            timestamp = int(time.time())
                            print(f'[DEBUG] Failed to connect to {bot_url}: {e}')
                            raise Exception(f'Could not connect to verification server: {e}')
                            print(f'[ERROR] Failed to get verification code from API: {e}')
                            raise e
                user_id_file = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'UserID.dat')
                key_raw = b'aK3pQv9XmRzT1bHnW6LuF2YgDeCsJ4'
                key = hashlib.sha256(key_raw).digest()
                user_id = None
                if os.path.exists(user_id_file):
                    try:
                        with open(user_id_file, 'rb') as f:
                            pass  # postinserted
                    except Exception as e:
                            encrypted_id = f.read()
                                cipher = AES.new(key, AES.MODE_ECB)
                                decrypted_padded = cipher.decrypt(encrypted_id)
                                decrypted = unpad(decrypted_padded, AES.block_size)
                                user_id = decrypted.decode('utf-8')
                                print(f'[DEBUG] Loaded UserID from file: {user_id}')
                else:  # inserted
                    pass  # postinserted
                if user_id is None:
                    dialog = tk.Toplevel(self)
                    dialog.title('Enter Your Discord User ID')
                    dialog.geometry('300x150')
                    dialog.configure(bg='#222222')
                    dialog.resizable(False, False)
                    set_window_icon(dialog)
                    dialog.update_idletasks()
                    screen_width = dialog.winfo_screenwidth()
                    screen_height = dialog.winfo_screenheight()
                    size = tuple((int(_) for _ in dialog.geometry().split('+')[0].split('x')))
                    x = screen_width // 2 - size[0] // 2
                    y = screen_height // 2 - size[1] // 2
                    dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                    label = tk.Label(dialog, text='Please enter your Discord User ID:', bg='#222222', fg='white', font=('Arial', 12))
                    label.pack(pady=(20, 10))
                    user_id_var = tk.StringVar()
                    entry = tk.Entry(dialog, textvariable=user_id_var, font=('Arial', 12), bg='#444444', fg='white', insertbackground='white', relief='flat', bd=2)
                    entry.pack(pady=(0, 10), padx=20, fill='x')
                    entry.focus_set()

                    def on_submit(event=None):
                        nonlocal user_id  # inserted
                        entered_id = user_id_var.get()
                        if entered_id:
                            try:
                                int(entered_id)
                                user_id = entered_id
                                data = user_id.encode('utf-8')
                                padded_data = pad(data, AES.block_size)
                                cipher = AES.new(key, AES.MODE_ECB)
                                encrypted_data = cipher.encrypt(padded_data)
                                os.makedirs(os.path.dirname(user_id_file), exist_ok=True)
                                with open(user_id_file, 'wb') as f:
                                    pass  # postinserted
                            except ValueError:
                                    f.write(encrypted_data)
                                        print(f'[DEBUG] Saved UserID to file: {user_id}')
                                        dialog.destroy()
                            messagebox.showerror('Invalid Input', 'Please enter a valid integer Discord User ID.')
                    entry.bind('<Return>', on_submit)
                    button_frame = tk.Frame(dialog, bg='#222222')
                    button_frame.pack(pady=(0, 20))
                    how_btn = RoundedButton(button_frame, width=60, height=30, cornerradius=10, bg='#444444', fg='white', text='How?', font=('Arial', 12, 'bold'), command=lambda: webbrowser.open('https://www.youtube.com/watch?v=LiUBWdQ1rIg'))
                    how_btn.pack(side='left', padx=(0, 10))
                    submit_btn = RoundedButton(button_frame, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='Submit', font=('Arial', 12, 'bold'), command=on_submit)
                    submit_btn.pack(side='left')
                    dialog.transient(self)
                    dialog.grab_set()
                    self.wait_window(dialog)
                    if user_id is None:
                        return
                try:
                    original_id = int(user_id)
                    loading_dialog = tk.Toplevel(self)
                    loading_dialog.title('Generating Code')
                    loading_dialog.geometry('300x120')
                    loading_dialog.configure(bg='#222222')
                    loading_dialog.resizable(False, False)
                    set_window_icon(loading_dialog)
                    loading_dialog.update_idletasks()
                    sw = loading_dialog.winfo_screenwidth()
                    sh = loading_dialog.winfo_screenheight()
                    sz = tuple((int(_) for _ in loading_dialog.geometry().split('+')[0].split('x')))
                    rx = sw // 2 - sz[0] // 2
                    ry = sh // 2 - sz[1] // 2
                    loading_dialog.geometry(f'{sz[0]}x{sz[1]}+{rx}+{ry}')
                    loading_label = tk.Label(loading_dialog, text='Connecting to verification server...', bg='#222222', fg='white', font=('Arial', 12))
                    loading_label.pack(pady=(30, 10))
                    progress_label = tk.Label(loading_dialog, text='Please wait...', bg='#222222', fg='#AAAAAA', font=('Arial', 10))
                    progress_label.pack(pady=(5, 10))
                    loading_dialog.update()
                except ValueError:
                    pass  # postinserted
                else:  # inserted
                    try:
                        code = get_verification_code_from_api(original_id)
                        loading_dialog.destroy()
                    except Exception as api_error:
                        pass  # postinserted
                    else:  # inserted
                        result_dialog = tk.Toplevel(self)
                        result_dialog.title('Verification')
                        result_dialog.geometry('400x160')
                        result_dialog.configure(bg='#222222')
                        set_window_icon(result_dialog)
                        result_dialog.resizable(False, False)
                        result_dialog.update_idletasks()
                        sw = result_dialog.winfo_screenwidth()
                        sh = result_dialog.winfo_screenheight()
                        sz = tuple((int(_) for _ in result_dialog.geometry().split('+')[0].split('x')))
                        rx = sw // 2 - sz[0] // 2
                        ry = sh // 2 - sz[1] // 2
                        result_dialog.geometry(f'{sz[0]}x{sz[1]}+{rx}+{ry}')
                        label_result = tk.Label(result_dialog, text='Copy the following text:', bg='#222222', fg='white', font=('Arial', 12))
                        label_result.pack(pady=(10, 5))
                        obf_text = code
                        text_var = tk.StringVar(value=obf_text)
                        entry_result = tk.Entry(result_dialog, textvariable=text_var, font=('Arial', 12), bg='#444444', fg='white', relief='flat', bd=2, justify='center')
                        entry_result.pack(padx=20, pady=(0, 10), fill='x')

                        def copy_to_clipboard():
                            result_dialog.clipboard_clear()
                            result_dialog.clipboard_append(text_var.get())
                            result_dialog.destroy()

                            def input_bot_code():
                                bot_dialog = tk.Toplevel(self)
                                bot_dialog.title('Discord Verification')
                                bot_dialog.geometry('350x260')
                                bot_dialog.configure(bg='#222222')
                                bot_dialog.resizable(False, False)
                                set_window_icon(bot_dialog)
                                bot_dialog.update_idletasks()
                                screen_width = bot_dialog.winfo_screenwidth()
                                screen_height = bot_dialog.winfo_screenheight()
                                size = tuple((int(_) for _ in bot_dialog.geometry().split('+')[0].split('x')))
                                x = screen_width // 2 - size[0] // 2
                                y = screen_height // 2 - size[1] // 2
                                bot_dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                                auto_polling = True
                                status_label = None
                                status_label = tk.Label(bot_dialog, text='(2) attempt 1/60\nUse /verify in Discord and\nfollow the instructions', bg='#222222', fg='white', font=('Arial', 12, 'bold'), justify='center')
                                status_label.pack(expand=True, pady=50)
                                print(f'[DEBUG] Dialog created, auto_polling: {auto_polling}, status_label: {status_label is not None}')

                                def cancel_auto_verification():
                                    nonlocal auto_polling  # inserted
                                    auto_polling = False
                                    bot_dialog.destroy()
                                retry_attempt = 0
                                max_total_attempts = 60
                                start_time = time.time()
                                max_duration = 300
                                countdown_seconds = 0
                                countdown_active = False

                                def update_countdown():
                                    """Update the countdown display every second"""  # inserted
                                    nonlocal countdown_seconds  # inserted
                                    nonlocal countdown_active  # inserted
                                    if not countdown_active or not auto_polling:
                                        return None
                                    if countdown_seconds > 0:
                                        if status_label and bot_dialog.winfo_exists():
                                            status_label.config(text=f'({countdown_seconds}) attempt {retry_attempt + 1}/{max_total_attempts}\nUse /verify in Discord and\nfollow the instructions')
                                        countdown_seconds -= 1
                                        if bot_dialog.winfo_exists():
                                            bot_dialog.after(1000, update_countdown)
                                    else:  # inserted
                                        countdown_active = False

                                def poll_verification():
                                    nonlocal countdown_seconds  # inserted
                                    nonlocal countdown_active  # inserted
                                    nonlocal auto_polling  # inserted
                                    nonlocal retry_attempt  # inserted
                                    if not auto_polling:
                                        print('[DEBUG] Auto polling is disabled, stopping')
                                        return
                                    elapsed_time = time.time() - start_time
                                    if elapsed_time >= max_duration or retry_attempt >= max_total_attempts:
                                        print(f'[DEBUG] Verification timeout after {elapsed_time:.1f} seconds and {retry_attempt} attempts')
                                        if status_label and bot_dialog.winfo_exists():
                                            status_label.config(text='Took too long to verify (5 minutes timeout).\nPlease try the verification process again.', fg='#ffffff')
                                        auto_polling = False
                                        return
                                    retry_attempt += 1
                                    if status_label and bot_dialog.winfo_exists():
                                        status_label.config(text=f'Checking... attempt {retry_attempt}/{max_total_attempts}\nUse /verify in Discord and\nfollow the instructions', fg='white')
                                    try:
                                        machine_guid = get_machine_guid()
                                        if not machine_guid:
                                            print('[DEBUG] Could not get machine GUID')
                                            raise Exception('Could not get machine GUID')
                                        print(f'[DEBUG] Polling verification for GUID: {machine_guid} (attempt {retry_attempt})')
                                        response = requests.post('https://discordbot-production-914b.up.railway.app/api/check-verification', json={'machineGuid': machine_guid}, timeout=10)
                                        print(f'[DEBUG] API Response status: {response.status_code}')
                                        if response.status_code == 200:
                                            data = response.json()
                                            print(f'[DEBUG] API Response data: {data}')
                                            if data.get('success') and data.get('verified'):
                                                print('[DEBUG] Verification successful! Processing data...')
                                                verification_data = {'userId': data.get('userId'), 'startTimestamp': data.get('startTimestamp'), 'endTimestamp': data.get('endTimestamp'), 'machineGuid': data.get('machineGuid'), 'baseSeconds': data.get('baseSeconds'), 'accessSeconds': data.get('accessSeconds'), 'levelPercent': data.get('levelPercent'), 'levelRoleId': data.get('levelRoleId')}
                                                if verification_data['userId'] and verification_data['startTimestamp']:
                                                    auto_polling = False
                                                    process_verification_data(verification_data)
                                            else:  # inserted
                                                print('[DEBUG] Verification not ready yet')
                                        else:  # inserted
                                            print(f'[DEBUG] API request failed with status: {response.status_code}')
                                        next_delay = 5
                                        countdown_seconds = next_delay
                                        countdown_active = True

                                        def update_next_countdown():
                                            """Update the countdown display for next attempt"""  # inserted
                                            nonlocal countdown_seconds  # inserted
                                            nonlocal countdown_active  # inserted
                                            if not countdown_active or not auto_polling:
                                                return None
                                            if countdown_seconds > 0:
                                                if status_label and bot_dialog.winfo_exists():
                                                    next_attempt_num = retry_attempt + 1
                                                    status_label.config(text=f'({countdown_seconds}) attempt {next_attempt_num}/{max_total_attempts}\nUse /verify in Discord and\nfollow the instructions')
                                                countdown_seconds -= 1
                                                if bot_dialog.winfo_exists():
                                                    bot_dialog.after(1000, update_next_countdown)
                                            else:  # inserted
                                                countdown_active = False
                                        update_next_countdown()
                                        if bot_dialog.winfo_exists():
                                            bot_dialog.after(next_delay * 1000, poll_verification)
                                    except Exception as e:
                                                else:  # inserted
                                                    print('[DEBUG] Dialog no longer exists, stopping polling')
                                                    print(f'[DEBUG] Polling error: {str(e)}')
                                                    next_delay = 5
                                                    countdown_seconds = next_delay
                                                    countdown_active = True

                                                    def update_error_countdown():
                                                        """Update the error countdown display every second"""  # inserted
                                                        nonlocal countdown_seconds  # inserted
                                                        nonlocal countdown_active  # inserted
                                                        if not countdown_active or not auto_polling:
                                                            return None
                                                        if countdown_seconds > 0:
                                                            if status_label and bot_dialog.winfo_exists():
                                                                next_attempt_num = retry_attempt + 1
                                                                status_label.config(text=f'Connection error ({countdown_seconds}) attempt {next_attempt_num}/{max_total_attempts}\nUse /verify in Discord and\nfollow the instructions', fg='#ffaa00')
                                                            countdown_seconds -= 1
                                                            if bot_dialog.winfo_exists():
                                                                bot_dialog.after(1000, update_error_countdown)
                                                        else:  # inserted
                                                            countdown_active = False
                                                    update_error_countdown()
                                                    if bot_dialog.winfo_exists() and retry_attempt < max_total_attempts:
                                                        bot_dialog.after(next_delay * 1000, poll_verification)
                                                    else:  # inserted
                                                        print('[DEBUG] Dialog closed or max attempts reached, stopping polling due to error')
                                                        return

                                def process_verification_data(verification_data):
                                    try:
                                        user_id = verification_data.get('userId')
                                        start_timestamp = verification_data.get('startTimestamp')
                                        end_timestamp = verification_data.get('endTimestamp')
                                        machine_guid_decoded = verification_data.get('machineGuid')
                                        base_seconds = verification_data.get('baseSeconds')
                                        access_seconds = verification_data.get('accessSeconds')
                                        if str(user_id)!= str(original_id):
                                            messagebox.showerror('Verification Failed', 'User ID does not match')
                                            return
                                        current_machine_guid = get_machine_guid()
                                        if machine_guid_decoded!= current_machine_guid:
                                            messagebox.showerror('Verification Failed', 'Machine GUID does not match')
                                            return
                                    except Exception as e:
                                        pass  # postinserted
                                    else:  # inserted
                                        access_duration = access_seconds if isinstance(access_seconds, int) and access_seconds > 0 else end_timestamp - start_timestamp
                                        role_found = 'member'
                                        base_for_role = base_seconds if isinstance(base_seconds, int) and base_seconds > 0 else access_duration
                                        if base_for_role >= 2592000:
                                            role_found = 'supporter'
                                        else:  # inserted
                                            if base_for_role >= 604800:
                                                role_found = 'donator'
                                            else:  # inserted
                                                if base_for_role >= 259200:
                                                    role_found = 'booster'
                                                else:  # inserted
                                                    if base_for_role >= 172800:
                                                        role_found = 'giveaway_sponsor'
                                    else:  # inserted
                                        print('[DEBUG] Verification successful! Closing dialog and processing...')
                                        bot_dialog.destroy()
                                        current_time = start_timestamp
                                        expiration_timestamp = end_timestamp
                                        data_str = f'{current_time};{expiration_timestamp};{machine_guid_decoded};{role_found}'
                                        data = data_str.encode('utf-8')
                                        padded_data = pad(data, AES.block_size)
                                        cipher2 = AES.new(key, AES.MODE_ECB)
                                        encrypted_data = cipher2.encrypt(padded_data)
                                        file_path = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'duration.dat')
                                        try:
                                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                                            with open(file_path, 'wb') as f:
                                                pass  # postinserted
                                        except Exception as e:
                                                f.write(encrypted_data)
                                                else:  # inserted
                                                    def wait_for_file_and_update():
                                                        max_wait = 5
                                                        waited = 0
                                                        while (not os.path.exists(file_path) or os.path.getsize(file_path) == 0) and waited < max_wait:
                                                            time.sleep(0.1)
                                                            waited += 0.1
                                                        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                                                            current_time_stored, expiration_timestamp, guid, role = self.decrypt_duration()
                                                            if current_time_stored is not None:
                                                                self._current_time = current_time_stored
                                                            else:  # inserted
                                                                self._current_time = int(time.time())
                                                            self.update_timer_button()
                                                            if guid and role:
                                                                self.encrypt_duration(current_time_stored, expiration_timestamp, guid, role)
                                                    threading.Thread(target=wait_for_file_and_update, daemon=True).start()
                                                    code_confirm_dialog = tk.Toplevel(self)
                                                    code_confirm_dialog.title('Code Confirmation')
                                                    code_confirm_dialog.geometry('300x150')
                                                    code_confirm_dialog.configure(bg='#222222')
                                                    set_window_icon(code_confirm_dialog)
                                                    code_confirm_dialog.resizable(False, False)
                                                    code_confirm_dialog.update_idletasks()
                                                    sw = code_confirm_dialog.winfo_screenwidth()
                                                    sh = code_confirm_dialog.winfo_screenheight()
                                                    sz = tuple((int(_) for _ in code_confirm_dialog.geometry().split('+')[0].split('x')))
                                                    rx = sw // 2 - sz[0] // 2
                                                    ry = sh // 2 - sz[1] // 2
                                                    code_confirm_dialog.geometry(f'{sz[0]}x{sz[1]}+{rx}+{ry}')
                                                    code_validity = 'Verification Successful'
                                                    role_display = role_found.replace('_', ' ') if role_found else 'Unknown'
                                                    role_text = f'Role: {role_display}'
                                                    display_seconds = access_seconds if isinstance(access_seconds, int) and access_seconds > 0 else end_timestamp - start_timestamp

                                                    def format_duration_human(secs: int) -> str:
                                                        days = secs // 86400
                                                        rem = secs % 86400
                                                        hours = rem // 3600
                                                        minutes = rem % 3600 // 60
                                                        parts = []
                                                        parts.append(f'{days} day' + ('s' if days!= 1 else ''))
                                                        if hours > 0:
                                                            parts.append(f'{hours} hour' + ('s' if hours!= 1 else ''))
                                                        if days == 0 and minutes > 0:
                                                            parts.append(f'{minutes} minute' + ('s' if minutes!= 1 else ''))
                                                        if not parts:
                                                            parts.append('less than a minute')
                                                        return ' '.join(parts)
                                                    duration_text = f'Access duration: {format_duration_human(int(display_seconds))}'
                                                    label_validity = tk.Label(code_confirm_dialog, text=code_validity, bg='#222222', fg='white', font=('Arial', 14, 'bold'))
                                                    label_validity.pack(pady=(20, 5))
                                                    label_role = tk.Label(code_confirm_dialog, text=role_text, bg='#222222', fg='white', font=('Arial', 12))
                                                    label_role.pack(pady=5)
                                                    label_duration = tk.Label(code_confirm_dialog, text=duration_text, bg='#222222', fg='white', font=('Arial', 12))
                                                    label_duration.pack(pady=5)

                                                    def close_code_confirm():
                                                        code_confirm_dialog.destroy()
                                                    ok_button = RoundedButton(code_confirm_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_code_confirm)
                                                    ok_button.pack(pady=(20, 10))
                                                    self.update_timer_button()
                                            print(f'[DEBUG] Error processing verification data: {e}')
                                            messagebox.showerror('Verification Failed', f'Error processing verification data: {e}')
                                            messagebox.showerror('Error', f'Failed to create encrypted duration file:\n{e}')
                                cancel_button = tk.Button(bot_dialog, text='Cancel', command=lambda: cancel_auto_verification(), font=('Arial', 10), bg='#f44336', fg='white', relief='flat', pady=5)
                                cancel_button.pack(pady=(0, 20))
                                print('[DEBUG] Starting verification polling...')

                                def start_with_countdown():
                                    nonlocal countdown_seconds  # inserted
                                    nonlocal countdown_active  # inserted
                                    countdown_seconds = 2
                                    countdown_active = True

                                    def initial_countdown():
                                        nonlocal countdown_seconds  # inserted
                                        nonlocal countdown_active  # inserted
                                        if countdown_seconds > 0:
                                            if status_label and bot_dialog.winfo_exists():
                                                status_label.config(text=f'({countdown_seconds}) attempt 1/{max_total_attempts}\nUse /verify in Discord and\nfollow the instructions')
                                            countdown_seconds -= 1
                                            bot_dialog.after(1000, initial_countdown)
                                        else:  # inserted
                                            countdown_active = False
                                            poll_verification()
                                    initial_countdown()
                                start_with_countdown()
                                bot_dialog.transient(self)
                                bot_dialog.grab_set()
                                self.wait_window(bot_dialog)
                            input_bot_code()

                        def change_user_id():
                            user_id_file = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'UserID.dat')
                            try:
                                if os.path.exists(user_id_file):
                                    os.remove(user_id_file)
                                    print('[DEBUG] UserID.dat file deleted successfully')
                            except Exception as e:
                                pass  # postinserted
                            else:  # inserted
                                result_dialog.destroy()
                                ask_user_id()
                                print(f'[DEBUG] Failed to delete UserID.dat: {e}')
                                messagebox.showerror('Error', f'Failed to delete user ID file:\n{e}')
                                return None

                        def close_result():
                            result_dialog.destroy()
                        button_frame = tk.Frame(result_dialog, bg='#222222')
                        button_frame.pack(pady=(0, 10))
                        change_id_btn = RoundedButton(button_frame, width=80, height=30, cornerradius=10, bg='#FF6600', fg='white', text='Change ID', font=('Arial', 10, 'bold'), command=change_user_id)
                        change_id_btn.pack(side='left', padx=(0, 10))
                        copy_btn = RoundedButton(button_frame, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='Copy', font=('Arial', 12, 'bold'), command=copy_to_clipboard)
                        copy_btn.pack(side='left', padx=(0, 10))
                        result_dialog.transient(self)
                        result_dialog.grab_set()
                        self.wait_window(result_dialog)
                            print(f'[DEBUG] Failed to decrypt UserID.dat: {e}')
                            user_id = None
                            loading_dialog.destroy()
                            messagebox.showerror('Connection Error', f'Failed to connect to verification server:\n\n{str(api_error)}\n\nPlease check your internet connection and try again.')
                            messagebox.showerror('Invalid Input', 'Saved UserID is not a valid integer.')
            side_btn_w = 100
            side_btn_h = 54
            support_btn = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#FFAA00', fg='white', text='Support Me', font=btn_font, command=lambda: __import__('webbrowser').open('https://ko-fi.com/lisek_guy2/tip'))
            support_btn.pack(side='top', fill='x', pady=2)
            btn1 = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#0099FF', fg='white', text='Verify', font=btn_font, command=verify_button_clicked)
            btn1.pack(side='top', fill='x', pady=2)
            download_btn = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#444444', fg='white', text='Download', font=btn_font, command=self.show_downloads)
            download_btn.pack(side='top', fill='x', pady=2)

            def on_play_clicked():
                self._game_selected = False
                self.show_macro_folders()
            play_btn = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#444444', fg='white', text='Play', font=btn_font, command=on_play_clicked)
            play_btn.pack(side='top', fill='x', pady=2)
            macro_btn = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#444444', fg='white', text='Macros', font=btn_font, command=lambda: os.startfile(self.macros_dir))
            macro_btn.pack(side='top', fill='x', pady=2)
            webhook_btn = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#444444', fg='white', text='Webhook', font=btn_font, command=lambda: self.prompt_for_webhook_if_missing(force=True))
            webhook_btn.pack(side='top', fill='x', pady=2)
            keybinds_btn = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#444444', fg='white', text='Keybinds', font=btn_font, command=self.show_keybinds_menu)
            keybinds_btn.pack(side='top', fill='x', pady=2)
            resolution_btn = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#444444', fg='white', text='Resolution', font=btn_font, command=self.auto_detect_and_save_resolution)
            resolution_btn.pack(side='top', fill='x', pady=2)
            self.resolution_btn = resolution_btn
            btn2 = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#444444', fg='white', text='Timer', font=btn_font, command=None)
            btn2.pack(side='top', fill='x', pady=2)
            self.btn2 = btn2
            update_btn = RoundedButton(button_container, width=side_btn_w, height=side_btn_h, cornerradius=10, bg='#444445', fg='white', text='Update', font=btn_font, command=self.update_launcher_button_clicked)
            update_btn.pack(side='top', fill='x', pady=2)
            self.selected_resolution = tk.StringVar(value='Resolution')
            resolution_file_path = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'resolution.txt')
            if os.path.exists(resolution_file_path):
                try:
                    with open(resolution_file_path, 'r') as f:
                        saved_resolution = f.read().strip()
                            if saved_resolution:
                                self.selected_resolution.set(saved_resolution)
                                self.resolution_btn.text = saved_resolution
                                self.resolution_btn._draw_button(self.resolution_btn.bg)
            finally:  # inserted
                self.auto_detect_and_save_resolution()
                self.after(100, self.start_title_time_update)
                    print(f'[KEYBINDS] Failed to load persisted keybinds: {e}')

    def auto_detect_and_save_resolution(self):
        """Detect display scale first, then resolution.\n        - If Windows display Scale > 100%, show a warning dialog and stop.\n        - Else detect resolution and validate against the supported set.\n        Supported: 2560x1440, 1920x1080, 1366x768, 1364x768.\n        """  # inserted
        try:
            self._ensure_dpi_awareness()
            scale_percent = self._detect_display_scale_percent()
            if scale_percent is not None and scale_percent > 100:
                pass  # postinserted
        except Exception as e:
            else:  # inserted
                try:
                    self = tk.Toplevel(self)
                    self.title('Display Scale')
                    self.geometry('380x190')
                    self.configure(bg='#222222')
                    self.resizable(False, False)
                    set_window_icon(self)
                    self.update_idletasks()
                    sw = self.winfo_screenwidth()
                    sh = self.winfo_screenheight()
                    size = tuple((int(_) for _ in self.geometry().split('+')[0].split('x')))
                    x = sw // 2 - size[0] // 2
                    y = sh // 2 - size[1] // 2
                    self.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                    msg = f'Your Windows display scale is set to {scale_percent}%.\n\nPlease set Scale to 100% in Display Settings, then detect resolution again.'
                    tk.Label(self, text=msg, bg='#222222', fg='white', font=('Arial', 11), wraplength=340, justify='center').pack(pady=16, padx=16)

                    def _recheck_scale():
                        try:
                            warning_dialog.destroy()
                        except Exception:
                            pass  # postinserted
                        else:  # inserted
                            self.after(50, self.auto_detect_and_save_resolution)
                            pass
                        else:  # inserted
                            pass
                    RoundedButton(self, width=90, height=30, cornerradius=10, bg='#444444', fg='white', text='Recheck', font=('Arial', 10, 'bold'), command=_recheck_scale).pack(pady=(0, 14))
                    self.transient(self)
                    self.grab_set()
                except Exception as dialog_e:
                    pass  # postinserted
                else:  # inserted
                    try:
                        self.selected_resolution.set('Resolution')
                        if hasattr(self, 'resolution_btn') and self.resolution_btn.winfo_exists():
                            self.resolution_btn.text = 'Resolution'
                            self.resolution_btn._draw_button(self.resolution_btn.bg)
                        return
                except Exception:
                    pass  # postinserted
            else:  # inserted
                user32 = ctypes.windll.user32
                width = user32.GetSystemMetrics(0)
                height = user32.GetSystemMetrics(1)
                detected_resolution = f'{width}x{height}'
                allowed_resolutions = {'2560x1440', '1364x768', '1366x768', '1920x1080'}
                resolution_file_path = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'resolution.txt')
                if detected_resolution in allowed_resolutions:
                    resolution_to_save = detected_resolution
                else:  # inserted
                    warning_message = f'Your resolution {detected_resolution} is not supported.\nSupported resolutions are: 2560x1440, 1920x1080, 1366x768, 1364x768.\nPlease change your resolution.'
                    print(f'WARNING: {warning_message}')
                else:  # inserted
                    try:
                        self = tk.Toplevel(self)
                        self.title('Unsupported Resolution')
                        self.geometry('360x170')
                        self.configure(bg='#222222')
                        self.resizable(False, False)
                        set_window_icon(self)
                        self.update_idletasks()
                        sw = self.winfo_screenwidth()
                        sh = self.winfo_screenheight()
                        size = tuple((int(_) for _ in self.geometry().split('+')[0].split('x')))
                        x = sw // 2 - size[0] // 2
                        y = sh // 2 - size[1] // 2
                        self.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                        tk.Label(self, text=warning_message, bg='#222222', fg='white', font=('Arial', 10), wraplength=320, justify='center').pack(pady=16, padx=16)

                        def _recheck_res():
                            try:
                                warning_dialog.destroy()
                            except Exception:
                                pass  # postinserted
                            else:  # inserted
                                self.after(50, self.auto_detect_and_save_resolution)
                                pass
                            else:  # inserted
                                pass
                        RoundedButton(self, width=90, height=30, cornerradius=10, bg='#444444', fg='white', text='Recheck', font=('Arial', 10, 'bold'), command=_recheck_res).pack(pady=(0, 14))
                        self.transient(self)
                        self.grab_set()
                except Exception as dialog_e:
                    pass  # postinserted
                else:  # inserted
                    os.makedirs(os.path.dirname(resolution_file_path), exist_ok=True)
                    with open(resolution_file_path, 'w') as f:
                        f.write(resolution_to_save)
                            self.selected_resolution.set(resolution_to_save)
                            if hasattr(self, 'resolution_btn') and self.resolution_btn.winfo_exists():
                                self.resolution_btn.text = resolution_to_save
                                self.resolution_btn._draw_button(self.resolution_btn.bg)
                print(f'Failed to show scale warning dialog: {dialog_e}')
                return
                print(f'Failed to auto-detect and save resolution: {e}')

    def _detect_display_scale_percent(self):
        """Return Windows display scaling percentage for the PRIMARY monitor only.\n        Tries, in order (primary monitor handle):\n        - shcore.GetDpiForMonitor (Win8.1+, effective DPI)\n        - shcore.GetScaleFactorForMonitor (Win8.1+)\n        - gdi32.GetDeviceCaps(LOGPIXELSX) fallback (system DPI)\n        - Tk winfo_fpixels fallback\n        Returns an int percentage (e.g., 100, 125) or None if unknown.\n        """  # inserted
        try:
            user32 = ctypes.windll.user32
            MONITOR_DEFAULTTOPRIMARY = 1
            hprimary = user32.MonitorFromWindow(user32.GetDesktopWindow(), MONITOR_DEFAULTTOPRIMARY)
        except Exception as e:
            pass  # postinserted
        else:  # inserted
            try:
                shcore = ctypes.windll.shcore
                if hasattr(shcore, 'GetDpiForMonitor') and hprimary:
                    dpiX = ctypes.c_uint()
                    dpiY = ctypes.c_uint()
                    res = shcore.GetDpiForMonitor(hprimary, 0, ctypes.byref(dpiX), ctypes.byref(dpiY))
                    if res == 0 and dpiX.value:
                        return int(round(dpiX.value * 100 / 96))
                except Exception:
                    pass  # postinserted
        else:  # inserted
            try:
                shcore = ctypes.windll.shcore
                if hasattr(shcore, 'GetScaleFactorForMonitor') and hprimary:
                    scale = ctypes.c_int()
                    res = shcore.GetScaleFactorForMonitor(hprimary, ctypes.byref(scale))
                    if res == 0 and scale.value:
                        return int(scale.value)
                except Exception:
                    pass  # postinserted
        else:  # inserted
            try:
                LOGPIXELSX = 88
                hdc = user32.GetDC(0)
                dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, LOGPIXELSX)
                user32.ReleaseDC(0, hdc)
                if dpi:
                    return int(round(dpi * 100 / 96))
                except Exception:
                    else:  # inserted
                        try:
                            ppi = float(self.winfo_fpixels('1i'))
                            if ppi > 0:
                                return int(round(ppi * 100 / 96.0))
            except Exception:
                    else:  # inserted
                        return None
                    pass
                    pass
                    pass
                return
                print(f'[SCALE] Detection error: {e}')

    def _ensure_dpi_awareness(self):
        """Make the process DPI aware (Per-Monitor v2 preferred) so Windows APIs return real values.\n        Safe to call multiple times; failures are ignored.\n        """  # inserted
        pass
        try:
            SetProcessDpiAwarenessContext = ctypes.windll.user32.SetProcessDpiAwarenessContext
        except AttributeError:
            pass  # postinserted
        else:  # inserted
            if SetProcessDpiAwarenessContext:
                SetProcessDpiAwarenessContext(ctypes.c_void_p((-4)))
        except Exception:
            else:  # inserted
                try:
                    shcore = ctypes.windll.shcore
                    SetProcessDpiAwareness = shcore.SetProcessDpiAwareness
                    PROCESS_PER_MONITOR_DPI_AWARE = 2
                    SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
        except Exception:
            SetProcessDpiAwarenessContext = None
            pass
        else:  # inserted
            pass  # postinserted
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            return
            return

    def start_title_time_update(self):
        def tick():
            self.update_timer_button()
            self.after(1000, tick)
        self.after(200, self)
        search_frame = tk.Frame(self, bg='#222222')
        search_frame.pack(side='top', fill='x', padx=5, pady=(5, 8))
        search_label = tk.Label(search_frame, text='Search:', bg='#222222', fg='white', font=('Arial', 14, 'bold'))
        search_label.pack(side='left', padx=(0, 5), pady=2)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, bg='#333333', fg='white', font=('Arial', 12), insertbackground='white', relief='flat', bd=5)
        self.search_entry.pack(side='left', fill='x', expand=True, pady=2, padx=(0, 10))
        self.setup_search_placeholder()

        def on_main_click(event):
            if event.widget!= self.search_entry:
                self.focus_set()
        self.bind_all('<Button-1>', on_main_click)
        self.canvas = tk.Canvas(self, bg='#222222', highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scroll_frame = tk.Frame(self.canvas, bg='#222222')
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')
        self.scroll_frame.bind('<Configure>', self.on_frame_configure)
        migrate_macros_to_subdir()
        self.fetch_newest_remote_versions()
        self.fetch_images_map()
        self.show_macro_folders()

    def setup_search_placeholder(self):
        """Setup placeholder text for search entry"""  # inserted
        self.placeholder_text = 'Type to search for macros...'
        self.placeholder_active = True
        self.search_entry.insert(0, self.placeholder_text)
        self.search_entry.config(fg='#888888')

        def on_focus_in(event):
            if self.placeholder_active:
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg='white')
                self.placeholder_active = False

        def on_focus_out(event):
            current_text = self.search_entry.get()
            if not current_text or current_text == self.placeholder_text:
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, self.placeholder_text)
                self.search_entry.config(fg='#888888')
                self.placeholder_active = True

        def on_key_release(event):
            current_text = self.search_entry.get()
            if not current_text:
                self.placeholder_active = False
                self.search_entry.config(fg='white')
                return
            if current_text == self.placeholder_text:
                self.placeholder_active = True
                self.search_entry.config(fg='#888888')
            else:  # inserted
                self.placeholder_active = False
                self.search_entry.config(fg='white')

        def on_key_press(event):
            if event.keysym == 'Escape':
                self.clear_search()
            else:  # inserted
                if self.placeholder_active and event.keysym not in ['Tab', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
                    self.search_entry.delete(0, tk.END)
                    self.search_entry.config(fg='white')
                    self.placeholder_active = False
        self.search_entry.bind('<FocusIn>', on_focus_in)
        self.search_entry.bind('<FocusOut>', on_focus_out)
        self.search_entry.bind('<KeyPress>', on_key_press)
        self.search_entry.bind('<KeyRelease>', on_key_release)

    def clear_search(self):
        """Clear the search field"""  # inserted
        self.search_entry.delete(0, tk.END)
        self.search_entry.config(fg='white')
        self.placeholder_active = False
        self.search_entry.focus()

    def on_search_change(self, *args):
        """Handle search text changes"""  # inserted
        current_text = self.search_entry.get()
        if current_text == self.placeholder_text:
            self.placeholder_active = True
            return
        if current_text == '':
            self.placeholder_active = False
        else:  # inserted
            self.placeholder_active = False
        if hasattr(self, '_search_timer'):
            self.after_cancel(self._search_timer)
        self._search_timer = self.after(300, self.apply_search_filter)

    def apply_search_filter(self):
        """Apply search filter to currently displayed scripts"""  # inserted
        if self.placeholder_active:
            search_text = ''
        else:  # inserted
            search_text = self.search_var.get().lower()
        all_boxes = []
        for widget in self.scroll_frame.winfo_children():
            if hasattr(widget, '_script_name'):
                all_boxes.append(widget)
        for box in all_boxes:
            box.grid_remove()
        matching_boxes = []
        for box in all_boxes:
            if search_text == '' or self.matches_search(box._script_name.lower(), search_text):
                matching_boxes.append(box)
        row = 0
        col = 0
        for box in matching_boxes:
            box.grid(row=row, column=col, padx=10, pady=6)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        unique_count = len(matching_boxes)
        if unique_count <= 6:
            self.canvas.unbind_all('<MouseWheel>')
        else:  # inserted
            self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)
        self.canvas.yview_moveto(0)

    def matches_search(self, text, search):
        """Check if text matches search pattern (letters in sequence, case insensitive)"""  # inserted
        if not search:
            return True
        text_chars = [c.lower() for c in text if c.isalnum()]
        search_chars = [c.lower() for c in search if c.isalnum()]
        if not search_chars:
            return True
        text_idx = 0
        for search_char in search_chars:
            found = False
            while text_idx < len(text_chars):
                if text_chars[text_idx] == search_char:
                    found = True
                    text_idx += 1
                    break
                text_idx += 1
            if not found:
                return False
        else:  # inserted
            return True

    def show_resolution_dropdown(self):
        if hasattr(self, 'resolution_dropdown') and self.resolution_dropdown.winfo_exists():
            self.resolution_dropdown.destroy()
            return
        options = ['2560x1440', '1920x1080', '1366x768']
        self = tk.Toplevel(self)
        self.overrideredirect(True)
        self.configure(bg='#222222')
        set_window_icon(self)
        x = self.resolution_btn.winfo_rootx()
        y = self.resolution_btn.winfo_rooty() + self.resolution_btn.winfo_height()
        self.geometry(f'104x90+{x}+{y}')

        def on_click_outside(event):
            if dropdown.winfo_exists() and (not (dropdown == event.widget or dropdown.winfo_containing(event.x_root, event.y_root))):
                dropdown.destroy()
                self.unbind_all('<Button-1>')
        self.bind_all('<Button-1>', on_click_outside)
        self.resolution_dropdown = self

        def on_select(res):
            try:
                save_path = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'resolution.txt')
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'w') as f:
                    pass  # postinserted
            except Exception as e:
                    f.write(res)
                        self.selected_resolution.set(res)
                        self.resolution_btn.text = res
                        self.resolution_btn._draw_button(self.resolution_btn.bg)
                        self.show_local_scripts()
                    else:  # inserted
                        dropdown.destroy()
                        self.unbind_all('<Button-1>')
                    messagebox.showerror('Error', f'Failed to save resolution:\n{e}')
        for option in options:
            btn = RoundedButton(self, width=94, height=25, cornerradius=10, bg='#444444', fg='white', text=option, font=('Arial', 11, 'bold'), command=(option,), vertical_text_offset=lambda opt: on_select(opt), vertical_text_offset=2)
            btn.pack(pady=2, padx=5)

    def fetch_images_map(self):
        try:
            response = requests.get(MACROS_IMAGES_JSON_URL)
            response.raise_for_status()
            self.images_map = response.json()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load macros images map:\n{e}')
            self.images_map = {}
            return

    def load_local_scripts(self):
        local_files = self.get_local_scripts()
        if not local_files:
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            tk.Label(self.scroll_frame, text='No Macros found, download them.', fg='white', bg='#222222').pack(pady=10)
            self.after(100, self.update_mousewheel_binding)
            return
        else:  # inserted
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            grouped = self.sort_versions(local_files)
            downloaded_files = self.get_downloaded_scripts()
            downloaded_groups = self.sort_versions(downloaded_files)
            self.newest_local_versions = {}
            for base_name, versions in grouped.items():
                if versions:
                    _, newest_version = self.parse_name_version(versions[0])
                    self.newest_local_versions[base_name] = newest_version
                else:  # inserted
                    self.newest_local_versions[base_name] = 0
            row = 0
            col = 0
            for base_name, versions in grouped.items():
                self.create_versioned_script_box(base_name, versions, row, col, local=True, downloaded_versions=downloaded_groups.get(base_name, []), newest_remote_version=self.newest_remote_versions.get(base_name, 0) if hasattr(self, 'newest_remote_versions') else 0, newest_local_version=self.newest_local_versions.get(base_name, 0))
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
            self.after(100, self.update_mousewheel_binding)
            self.update_timer_button()

    def fetch_newest_remote_versions(self):
        try:
            response = requests.get(REMOTE_SCRIPTS_JSON_URL)
            response.raise_for_status()
            filenames = response.json()
        except Exception as e:
            pass  # postinserted
        else:  # inserted
            grouped_remote = self.sort_versions(filenames)
            self.newest_remote_versions = {}
            for base_name, versions in grouped_remote.items():
                if versions:
                    _, newest_version = self.parse_name_version(versions[0])
                    self.newest_remote_versions[base_name] = newest_version
                else:  # inserted
                    self.newest_remote_versions[base_name] = 0
            messagebox.showerror('Error', f'Failed to load macros:\n{e}')
            filenames = []
        else:  # inserted
            pass

    def exit(self, event=None):
        self.destroy()

    def decrypt_duration(self):
        file_path = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'duration.dat')
        if not os.path.exists(file_path):
            return (None, None, None, None)
        try:
            with open(file_path, 'rb') as f:
                pass  # postinserted
        except Exception:
                encrypted_data = f.read()
                    key_raw = b'aK3pQv9XmRzT1bHnW6LuF2YgDeCsJ4'
                    key = hashlib.sha256(key_raw).digest()
                    cipher = AES.new(key, AES.MODE_ECB)
                    decrypted_padded = cipher.decrypt(encrypted_data)
                    decrypted = unpad(decrypted_padded, AES.block_size)
                    decrypted_str = decrypted.decode('utf-8')
                    print(f'[DEBUG] Decrypted data: {decrypted_str}')
                    parts = decrypted_str.split(';')
                    if len(parts) == 4:
                        current_time_stored = int(parts[0])
                        expiration_timestamp = int(parts[1])
                        serial = parts[2]
                        role = parts[3]
                        return (current_time_stored, expiration_timestamp, serial, role)
                else:  # inserted
                    return (None, None, None, None)
                return (None, None, None, None)
            else:  # inserted
                pass

    def encrypt_duration(self, current_time, expiration_timestamp, serial, role):
        file_path = os.path.join(os.path.expanduser('~'), 'GUY2 Macros', 'duration.dat')
        try:
            data_str = f'{current_time};{expiration_timestamp};{serial};{role}'
            data = data_str.encode('utf-8')
            padded_data = pad(data, AES.block_size)
            key_raw = b'aK3pQv9XmRzT1bHnW6LuF2YgDeCsJ4'
            key = hashlib.sha256(key_raw).digest()
            cipher = AES.new(key, AES.MODE_ECB)
            encrypted_data = cipher.encrypt(padded_data)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                pass  # postinserted
        except Exception as e:
                f.write(encrypted_data)
                print(f'Failed to encrypt and save duration.dat: {e}')
                return False
            else:  # inserted
                pass

    def get_ntp_time(self):
        NTP_SERVER = 'pool.ntp.org'
        NTP_PORT = 123
        TIME1970 = 2208988800
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.settimeout(5)
            msg = b'\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            client.sendto(msg, (NTP_SERVER, NTP_PORT))
            msg, address = client.recvfrom(1024)
            if msg:
                unpacked = struct.unpack('!12I', msg[0:48])
                timestamp = unpacked[10] - TIME1970
                return int(timestamp)
        except Exception:
            return None
        else:  # inserted
            pass

    def update_timer_button(self):
        try:
            current_time_stored, expiration_timestamp, stored_serial, _ = self.decrypt_duration()
            now = time.time()
            current_serial = get_machine_guid()
            if self._last_ntp_time is None or now - self._last_ntp_update > 60:
                ntp_time = self.get_ntp_time()
                if ntp_time is not None:
                    self._last_ntp_time = ntp_time
                    self._last_ntp_update = now
                    self._current_time = ntp_time
                else:  # inserted
                    self._current_time = int(now)
            else:  # inserted
                if self._current_time is not None:
                    self._current_time += 1
                else:  # inserted
                    self._current_time = int(now)
            if stored_serial!= current_serial:
                timer_text = 'Time expired'
                self.terminate_all_script_processes()
            else:  # inserted
                if expiration_timestamp is None:
                    timer_text = '00:00:00'
                else:  # inserted
                    time_left = expiration_timestamp - self._current_time
                    if time_left <= 0:
                        timer_text = 'Time expired'
                        self.terminate_all_script_processes()
                    else:  # inserted
                        hours, remainder = divmod(time_left, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        timer_text = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            if hasattr(self, 'btn2') and self.btn2.winfo_exists() and (getattr(self, '_last_timer_text', None)!= timer_text):
                self._last_timer_text = timer_text
                self.btn2.text = timer_text
                self.btn2._draw_button(self.btn2.bg)
        except Exception as e:
            print(f'ERROR in update_timer_button: {e}')
            traceback.print_exc()

    def terminate_all_script_processes(self):
        """Close all run.exe windows except those whitelisted via free-run.\n\n        Uses window->PID mapping to preserve whitelisted macro processes.\n        """  # inserted
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        SCRIPTS_DIR = os.path.join(home_dir, 'GUY2 Macros', 'Macros')
        EXECUTOR_PATH = os.path.join(SCRIPTS_DIR, 'run.exe')
        WM_CLOSE = os.path.normpath(EXECUTOR_PATH)
        EnumWindows = user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        self = user32.GetWindowTextLengthW
        GetWindowTextLengthW = user32.GetWindowTextW
        GetWindowThreadProcessId = user32.PostMessageW
        GetWindowTextW = user32.GetWindowThreadProcessId
        PostMessageW = 16

        def foreach_window(hwnd, lParam):
            try:
                length = GetWindowTextLengthW(hwnd)
                if length > 0:
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    GetWindowTextW(hwnd, buffer, length + 1)
                    window_title = buffer.value
                    if window_title == target_title:
                        pid = wintypes.DWORD()
                        GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                        if hasattr(self, 'free_run_pids') and pid.value in self.free_run_pids:
                            return True
                        PostMessageW(hwnd, WM_CLOSE, 0, 0)
                return True
            except Exception:
                return True
            else:  # inserted
                pass
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        try:
            self.cmd_processes = [p for p in self.cmd_processes if p.pid in getattr(self, 'free_run_pids', set())]
        except Exception:
            self.cmd_processes = []
        else:  # inserted
            pass

    def remove_script(self, filename):
        script_path = os.path.join(self.macros_dir, filename)
        if messagebox.askyesno('Confirm', f'Delete {filename}?', parent=self):
            try:
                os.remove(script_path)
                base_name, _ = self.parse_name_version(filename)
                local_files = self.get_local_scripts()
                other_versions = [f for f in local_files if f!= filename and f.startswith(base_name)]
            except Exception as e:
                    if not other_versions:
                        images_dir = os.path.join(SCRIPTS_DIR, base_name + '_images')
                        if os.path.exists(images_dir) and os.path.isdir(images_dir):
                            pass  # postinserted
                        else:  # inserted
                            try:
                                shutil.rmtree(images_dir)
                            except Exception as e:
                                pass  # postinserted
                else:  # inserted
                    self.show_local_scripts()
            messagebox.showwarning('Warning', f'Failed to delete images folder:\n{e}')
            messagebox.showerror('Error', f'Couldn\'t delete:\n{e}')

    def hide_to_tray(self):
        self.withdraw()
        threading.Thread(target=self.create_tray_icon, daemon=True).start()

    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), 'white')
        menu = pystray.Menu(pystray.MenuItem('Exit', self.destroy))
        icon = pystray.Icon('GUY2 Macros', image, 'GUY2 Macros', menu)
        icon.run()

    def count_unique_macros(self, files):
        base_names = set()
        for f in files:
            base, _ = self.parse_name_version(f)
            base_names.add(base)
        return len(base_names)

    def parse_name_version(self, filename):
        base, ext = os.path.splitext(filename)
        match = re.search(' v(\\d+(?:\\.\\d+)*)$', base)
        if match:
            version_str = match.group(1)
            try:
                version = float(version_str)
            except ValueError:
                pass  # postinserted
            else:  # inserted
                base_name = base[:match.start()]
                return (base_name, version)
        else:  # inserted
            base_name = base
            version = 0
            return (base_name, version)
            version = 0
        else:  # inserted
            pass

    def sort_versions(self, files):
        groups = {}
        for f in files:
            base, ver = self.parse_name_version(f)
            groups.setdefault(base, []).append((ver, f))
        for base in groups:
            groups[base].sort(key=lambda x: x[0], reverse=True)
            groups[base] = [f for v, f in groups[base]]
        return groups

    def get_local_scripts(self):
        try:
            files = [f for f in os.listdir(self.macros_dir) if f.endswith('.py')]
        except Exception:
            return []
        else:  # inserted
            pass

    def get_downloaded_scripts(self):
        try:
            files = [f for f in os.listdir(self.macros_dir) if f.endswith('.py')]
        except Exception:
            return []
        else:  # inserted
            pass

    def discover_macro_folders(self):
        """Return list of absolute paths to subfolders under SCRIPTS_DIR ending with \'_macros\'."""  # inserted
        folders = []
        try:
            for name in os.listdir(SCRIPTS_DIR):
                abs_path = os.path.join(SCRIPTS_DIR, name)
                if os.path.isdir(abs_path) and name.lower().endswith('_macros'):
                    pass  # postinserted
        except Exception as e:
                else:  # inserted
                    folders.append(abs_path)
                return sorted(folders, key=lambda p: os.path.basename(p).lower())
                print(f'[FOLDERS] Failed to discover macro folders: {e}')

    def show_macro_folders(self):
        """Show a selection of all *_macros folders. If exactly one exists, open it automatically."""  # inserted
        if not hasattr(self, '_remote_available_counts') or not getattr(self, '_remote_available_counts'):
            try:
                resp = requests.get(REMOTE_SCRIPTS_JSON_URL, timeout=8)
                if resp.ok:
                    items = resp.json()
                    from collections import defaultdict
                    available_sets = defaultdict(set)
                    declared_folders = set()
                    for item in items:
                        parts = item.split('|') if isinstance(item, str) else []
                        filename = parts[0].strip() if parts else item.strip() if isinstance(item, str) else ''
                        if len(parts) >= 4 and parts[3].strip():
                            pass  # postinserted
            except Exception as e:
                        else:  # inserted
                            folder_name = parts[3].strip()
                            if not folder_name.lower().endswith('_macros'):
                                folder_name = folder_name + '_macros'
                            declared_folders.add(folder_name)
                            target = os.path.join(SCRIPTS_DIR, folder_name)
                            os.makedirs(target, exist_ok=True)
                        else:  # inserted
                            try:
                                base_name, _ = self.parse_name_version(filename)
                            except Exception:
                                pass  # postinserted
                            else:  # inserted
                                available_sets[folder_name].add(base_name)
                    else:  # inserted
                        self._remote_available_counts = {k: len(v) for k, v in available_sets.items()}
                            self._declared_folders_cache = declared_folders
        else:  # inserted
            pass  # postinserted
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, self.placeholder_text)
            self.search_entry.config(fg='#888888')
            self.placeholder_active = True
        folders = self.discover_macro_folders()
        folder_meta = getattr(self, '_folder_meta_cache', None)
        if folder_meta is None:
            folder_meta = {}
            try:
                names_url = 'https://guy2-macros.com/folders/names.json'
                meta_resp = requests.get(names_url, timeout=6)
                if meta_resp.ok:
                    data = meta_resp.json()
                    if isinstance(data, dict):
                        folder_meta = data
                        self._folder_meta_cache = folder_meta
            except Exception as e:
                pass  # postinserted
        else:  # inserted
            pass  # postinserted
        if not folders:
            os.makedirs(MACROS_DIR, exist_ok=True)
            folders = [MACROS_DIR]
        if len(folders) == 1:
            self.macros_dir = folders[0]
            self._game_selected = True
            self.show_local_scripts()
            return
        row = 0
        col = 0
        for folder in folders:
            name = os.path.basename(folder)
            display = name[:(-7)] if name.lower().endswith('_macros') else name
            folder_basename = os.path.basename(folder)
            macros_count = int(self._remote_available_counts.get(folder_basename, 0))
            meta = folder_meta.get(display, {}) if isinstance(folder_meta, dict) else {}
            friendly_name = meta.get('name', display) if isinstance(meta, dict) else display
            friendly_desc = meta.get('description', '') if isinstance(meta, dict) else ''
            slot = tk.Frame(self.scroll_frame, bg='#212121', width=150, height=210)
            slot.grid(row=row, column=col, padx=10, pady=6)
            slot.pack_propagate(False)
            box = tk.Frame(slot, bg='#2b2b2b', width=150, height=210, highlightbackground='#3a3a3a', highlightthickness=1)
            box.place(relx=0.5, rely=0.5, anchor='center')
            box.pack_propagate(False)
            box.grid_propagate(False)
            box._script_name = display
            for i in range(6):
                box.grid_rowconfigure(i, weight=0)
            box.grid_rowconfigure(4, weight=1)
            box.grid_columnconfigure(0, weight=1)
            name_label = tk.Label(box, text=friendly_name, fg='white', bg='#2b2b2b', font=('Arial', 13, 'bold'), wraplength=140, justify='center')
            name_label.grid(row=0, column=0, padx=8, pady=(12, 2), sticky='nwe')
            count_text = f'{macros_count} macro' + ('s' if macros_count!= 1 else '')
            count_lbl = tk.Label(box, text=count_text, fg='#bbbbbb', bg='#2b2b2b', font=('Arial', 9, 'bold'), wraplength=140, justify='center')
            count_lbl.grid(row=1, column=0, padx=8, pady=(0, 2), sticky='nwe')
            desc_text = friendly_desc.strip() if isinstance(friendly_desc, str) else ''
            desc_lbl = tk.Label(box, text=desc_text, fg='#bbbbbb', bg='#2b2b2b', font=('Arial', 9), wraplength=140, justify='center')
            desc_lbl.grid(row=2, column=0, padx=8, pady=(0, 0), sticky='nwe')

            def make_select_command(selected_folder=folder):
                def on_select():
                    self.macros_dir = selected_folder
                    self._game_selected = True
                    self.show_local_scripts()
                return on_select
            select_btn = RoundedButton(box, width=110, height=30, cornerradius=10, bg='#00AA00', fg='white', text='OPEN', font=('Arial', 12, 'bold'), command=make_select_command())
            select_btn.grid(row=5, column=0, pady=(8, 10))

            def on_card_enter(e, b=box, title=name_label, countl=count_lbl, descl=desc_lbl):
                b.config(highlightbackground='#6a6a6a', bg='#303030')
                title.config(bg='#303030')
                countl.config(bg='#303030')
                descl.config(bg='#303030')

            def on_card_leave(e, b=box, title=name_label, countl=count_lbl, descl=desc_lbl):
                b.config(highlightbackground='#3a3a3a', bg='#2b2b2b')
                title.config(bg='#2b2b2b')
                countl.config(bg='#2b2b2b')
                descl.config(bg='#2b2b2b')
            box.bind('<Enter>', on_card_enter)
            box.bind('<Leave>', on_card_leave)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        self.after(100, self.update_mousewheel_binding)
                        base_name = os.path.splitext(filename)[0]
                        print(f'[FOLDERS] Could not ensure remote-declared folders: {e}')
                        if not hasattr(self, '_remote_available_counts'):
                            self._remote_available_counts = {}
                        print(f'[FOLDERS] names.json not available or invalid: {e}')

    def show_local_scripts(self):
        self.script_buttons = {}
        self.remove_buttons = {}
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, self.placeholder_text)
            self.search_entry.config(fg='#888888')
            self.placeholder_active = True
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        local_files = self.get_local_scripts()
        unique_count = self.count_unique_macros(local_files)
        if unique_count <= 6:
            self.canvas.unbind_all('<MouseWheel>')
        else:  # inserted
            self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)
        self.load_local_scripts()
        self.canvas.yview_moveto(0)

    def show_downloads(self):
        self.script_buttons = {}
        self.remove_buttons = {}
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, self.placeholder_text)
            self.search_entry.config(fg='#888888')
            self.placeholder_active = True
        if not getattr(self, '_game_selected', False):
            warning_dialog = tk.Toplevel(self)
            warning_dialog.title('Select Game')
            warning_dialog.geometry('360x170')
            warning_dialog.configure(bg='#222222')
            warning_dialog.resizable(False, False)
            set_window_icon(warning_dialog)
            warning_dialog.update_idletasks()
            screen_width = warning_dialog.winfo_screenwidth()
            screen_height = warning_dialog.winfo_screenheight()
            size = tuple((int(_) for _ in warning_dialog.geometry().split('+')[0].split('x')))
            x = screen_width // 2 - size[0] // 2
            y = screen_height // 2 - size[1] // 2
            warning_dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
            label = tk.Label(warning_dialog, text='Please select a game before trying to download macros.', bg='#222222', fg='white', font=('Arial', 12), wraplength=320, justify='center')
            label.pack(pady=(40, 10), padx=10)

            def close_warning():
                warning_dialog.destroy()
            ok_button = RoundedButton(warning_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_warning)
            ok_button.pack(pady=(10, 20))
            warning_dialog.transient(self)
            warning_dialog.grab_set()
            self.wait_window(warning_dialog)
        else:  # inserted
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            self.fetch_images_map()
            threading.Thread(target=self.load_remote_scripts).start()

    def update_mousewheel_binding(self):
        bbox = self.canvas.bbox('all')
        if not bbox:
            self.canvas.unbind_all('<MouseWheel>')
            return
        canvas_height = self.canvas.winfo_height()
        frame_height = bbox[3] - bbox[1]
        if frame_height > canvas_height:
            self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)
        else:  # inserted
            self.canvas.unbind_all('<MouseWheel>')

    def load_remote_scripts(self):
        try:
            response = requests.get(REMOTE_SCRIPTS_JSON_URL)
            response.raise_for_status()
            raw_filenames = response.json()
            self.raw_entries_map = {}
            for item in raw_filenames:
                parts = item.split('|')
                filename = parts[0].strip() if parts else item.strip()
                self.raw_entries_map[filename] = item
            except Exception as e:
                pass  # postinserted
            current_folder = os.path.basename(self.macros_dir)
            downloaded_groups = []
            self = {}
            grouped = {}
            for item in raw_filenames:
                parts = item.split('|')
                filename = parts[0].strip() if parts else item.strip()
                description = 'No description.'
                min_role = 'member'
                folder_name = None
                if len(parts) >= 2:
                    description = parts[1].strip()
                if len(parts) >= 3:
                    min_role = parts[2].strip().lower() or 'member'
                if len(parts) >= 4:
                    folder_name = parts[3].strip()
                    if folder_name and (not folder_name.lower().endswith('_macros')):
                        folder_name = folder_name + '_macros'
                if not folder_name or folder_name!= current_folder:
                    continue
                downloaded_groups.append(filename)
                self[filename] = description
                grouped[filename] = min_role
            filenames = self.sort_versions(downloaded_groups)
            downloaded_files = self.get_downloaded_scripts()
            descriptions = self.sort_versions(downloaded_files)
            self.newest_remote_versions = {}
            for base_name, versions in filenames.items():
                if versions:
                    _, newest_version = self.parse_name_version(versions[0])
                    self.newest_remote_versions[base_name] = newest_version
                else:  # inserted
                    self.newest_remote_versions[base_name] = 0

            def verify_before_action():
                if self.selected_resolution.get() == 'Resolution':
                    messagebox.showerror('Error', 'Please select your resolution before downloading.')
                    return False
                decrypt_result = self.decrypt_duration()
                if decrypt_result is None:
                    expiration_timestamp = None
                    stored_serial = None
                    user_role = None
                else:  # inserted
                    _, expiration_timestamp, stored_serial, user_role = decrypt_result
                current_time = int(time.time())
                current_serial = get_machine_guid()
                if expiration_timestamp is None or current_time >= expiration_timestamp or stored_serial!= current_serial:
                    warning_dialog = tk.Toplevel(self)
                    warning_dialog.title('Time Expired')
                    warning_dialog.geometry('300x150')
                    warning_dialog.configure(bg='#222222')
                    warning_dialog.resizable(False, False)
                    set_window_icon(warning_dialog)
                    warning_dialog.update_idletasks()
                    screen_width = warning_dialog.winfo_screenwidth()
                    screen_height = warning_dialog.winfo_screenheight()
                    size = tuple((int(_) for _ in warning_dialog.geometry().split('+')[0].split('x')))
                    x = screen_width // 2 - size[0] // 2
                    y = screen_height // 2 - size[1] // 2
                    warning_dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                    label = tk.Label(warning_dialog, text='Please verify to download macros.', bg='#222222', fg='white', font=('Arial', 12), wraplength=280, justify='center')
                    label.pack(pady=(40, 10), padx=10)

                    def close_warning():
                        warning_dialog.destroy()
                    ok_button = RoundedButton(warning_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_warning)
                    ok_button.pack(pady=(10, 20))
                    warning_dialog.transient(self)
                    warning_dialog.grab_set()
                    self.wait_window(warning_dialog)
                else:  # inserted
                    return True

            def create_cards():
                for widget in self.scroll_frame.winfo_children():
                    widget.destroy()
                if not filenames:
                    tk.Label(self.scroll_frame, text='No macros found.', fg='white', bg='#222222').pack(pady=10)
                    self.after(100, self.update_mousewheel_binding)
                    return
                row = 0
                col = 0
                for base_name, versions in grouped.items():
                    def make_download_command(versions=versions, base_name=base_name):
                        def on_download_click():
                            if not getattr(self, '_game_selected', False):
                                warning_dialog = tk.Toplevel(self)
                                warning_dialog.title('Select Game')
                                warning_dialog.geometry('360x170')
                                warning_dialog.configure(bg='#222222')
                                warning_dialog.resizable(False, False)
                                set_window_icon(warning_dialog)
                                warning_dialog.update_idletasks()
                                sw = warning_dialog.winfo_screenwidth()
                                sh = warning_dialog.winfo_screenheight()
                                sz = tuple((int(_) for _ in warning_dialog.geometry().split('+')[0].split('x')))
                                rx = sw // 2 - sz[0] // 2
                                ry = sh // 2 - sz[1] // 2
                                warning_dialog.geometry(f'{sz[0]}x{sz[1]}+{rx}+{ry}')
                                label = tk.Label(warning_dialog, text='Please select a game before trying to download macros.', bg='#222222', fg='white', font=('Arial', 12), wraplength=320, justify='center')
                                label.pack(pady=(40, 10), padx=10)

                                def close_warning():
                                    warning_dialog.destroy()
                                ok_button = RoundedButton(warning_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_warning)
                                ok_button.pack(pady=(10, 20))
                                warning_dialog.transient(self)
                                warning_dialog.grab_set()
                                self.wait_window(warning_dialog)
                                return
                            decrypt_result = self.decrypt_duration()
                            if decrypt_result is None:
                                expiration_timestamp = None
                                stored_serial = None
                                user_role = None
                            else:  # inserted
                                _, expiration_timestamp, stored_serial, user_role = decrypt_result
                            current_time = int(time.time())
                            current_serial = get_machine_guid()
                            if expiration_timestamp is None or current_time >= expiration_timestamp or stored_serial!= current_serial:
                                warning_dialog = tk.Toplevel(self)
                                warning_dialog.title('Verification Required')
                                warning_dialog.geometry('300x150')
                                warning_dialog.configure(bg='#222222')
                                warning_dialog.resizable(False, False)
                                set_window_icon(warning_dialog)
                                warning_dialog.update_idletasks()
                                screen_width = warning_dialog.winfo_screenwidth()
                                screen_height = warning_dialog.winfo_screenheight()
                                size = tuple((int(_) for _ in warning_dialog.geometry().split('+')[0].split('x')))
                                x = screen_width // 2 - size[0] // 2
                                y = screen_height // 2 - size[1] // 2
                                warning_dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                                label = tk.Label(warning_dialog, text='Please verify to download macros.', bg='#222222', fg='white', font=('Arial', 12), wraplength=280, justify='center')
                                label.pack(pady=(40, 10), padx=10)

                                def close_warning():
                                    warning_dialog.destroy()
                                ok_button = RoundedButton(warning_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_warning)
                                ok_button.pack(pady=(10, 20))
                                warning_dialog.transient(self)
                                warning_dialog.grab_set()
                                self.wait_window(warning_dialog)
                            else:  # inserted
                                allowed_roles_map = {'member': ['member', 'giveaway_sponsor', 'booster', 'donator', 'supporter'], 'giveaway_sponsor': ['giveaway_sponsor', 'booster', 'donator', 'supporter'], 'booster': ['booster', 'donator', 'supporter'], 'donator': ['donator', 'supporter'], 'supporter': ['supporter']}
                                min_role = None
                                if min_roles and versions[0] in min_roles:
                                    min_role = min_roles[versions[0]]
                                else:  # inserted
                                    min_role = 'member'
                                if user_role is not None and user_role.lower() not in allowed_roles_map.get(min_role, []):
                                    allowed_roles = allowed_roles_map.get(min_role, [])
                                    allowed_roles_display = '\n'.join((role.capitalize() for role in allowed_roles))
                                    error_dialog = tk.Toplevel(self)
                                    error_dialog.title('Access Denied')
                                    error_dialog.geometry('350x250')
                                    error_dialog.configure(bg='#222222')
                                    error_dialog.resizable(False, False)
                                    set_window_icon(error_dialog)
                                    error_dialog.update_idletasks()
                                    sw = error_dialog.winfo_screenwidth()
                                    sh = error_dialog.winfo_screenheight()
                                    sz = tuple((int(_) for _ in error_dialog.geometry().split('+')[0].split('x')))
                                    rx = sw // 2 - sz[0] // 2
                                    ry = sh // 2 - sz[1] // 2
                                    error_dialog.geometry(f'{sz[0]}x{sz[1]}+{rx}+{ry}')
                                    label = tk.Label(error_dialog, text=f'This macro is reserved for users with\none of these roles:\n\n{allowed_roles_display}', bg='#222222', fg='white', font=('Arial', 12), justify='center')
                                    label.pack(pady=(20, 10), padx=10)

                                    def close_error():
                                        error_dialog.destroy()
                                    ok_button = RoundedButton(error_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_error)
                                    ok_button.pack(pady=(10, 20))
                                    error_dialog.transient(self)
                                    error_dialog.grab_set()
                                    self.wait_window(error_dialog)
                                else:  # inserted
                                    if verify_before_action():
                                        filename = versions[0]
                                        btn = self.script_buttons.get(filename)
                                        if btn:
                                            btn.text = 'Downloading...'
                                            btn.bg = '#1a1a1a'
                                            btn.fg = 'white'
                                            btn._draw_button(btn.bg)
                                            threading.Thread(target=self.download_script, args=(filename, btn)).start()
                        return on_download_click
                    self.create_versioned_script_box(base_name, versions, row, col, local=False, descriptions=descriptions, downloaded_versions=downloaded_groups.get(base_name, []), min_roles=min_roles)
                    filename = versions[0]
                    btn = self.script_buttons.get(filename)
                    if btn:
                        btn.command = make_download_command()
                    col += 1
                    if col >= 3:
                        col = 0
                        row += 1
                self.after(100, self.update_mousewheel_binding)
            self.after(0, create_cards)
                messagebox.showerror('Error', f'Failed to load macros:\n{e}')
                raw_filenames = []

    def create_versioned_script_box(self, base_name, versions, row, col, local=True, descriptions=None, downloaded_versions=None, newest_remote_version=0, newest_local_version=0, min_roles=None):
        local = 0
        self.versions = versions
        self.downloaded_versions = downloaded_versions if downloaded_versions else []
        downloaded_versions = None
        border_color = '#444444'
        resolution = self.selected_resolution.get()
        if resolution in ['1366x768', '1364x768']:
            script_path = os.path.join(self.macros_dir, versions[0]) if versions else None
            if script_path and os.path.exists(script_path):
                try:
                    with open(script_path, 'r', encoding='utf-8') as f:
                        pass  # postinserted
                except Exception as e:
                        for line in f:
                            line = line.strip()
                            if line.lower().startswith('# versions:'):
                                border_color = '#444444'
                                break
                        else:  # inserted
                            border_color = '#FF0000'
        else:  # inserted
            pass  # postinserted
        if local and newest_remote_version > newest_local_version:
            border_color = '#FFFF00'
        versions = tk.Frame(self.scroll_frame, bg='#333333', width=150, height=240, highlightbackground=border_color, highlightthickness=2)
        versions.grid(row=row, column=col, padx=10, pady=6)
        versions.pack_propagate(False)
        versions._script_name = base_name
        action_button = tk.Label(versions, fg='white', bg='#333333', font=('Arial', 12, 'bold'), wraplength=140, justify='center')
        action_button.pack(pady=(10, 2))
        descriptions = tk.Label(versions, fg='#AAAAAA', bg='#333333', font=('Arial', 9), wraplength=140, justify='center')
        descriptions.pack(pady=(0, 5))
        current_index = tk.Frame(versions, bg='#333333')
        current_index.pack(expand=True)
        edit_button = None
        if local and newest_remote_version > newest_local_version:
            edit_button = RoundedButton(versions, width=110, height=30, cornerradius=10, bg='#0077CC', fg='white', text='Update', font=('Arial', 10, 'bold'), command=None)
            edit_button.pack(side='top', pady=(0, 4))

        def on_update_click():
            if self.selected_resolution.get() == 'Resolution':
                messagebox.showerror('Error', 'Please select your resolution before updating.')
                return
            decrypt_result = self.decrypt_duration()
            if decrypt_result is None:
                expiration_timestamp = None
                stored_serial = None
                user_role = None
            else:  # inserted
                _, expiration_timestamp, stored_serial, user_role = decrypt_result
            current_time = int(time.time())
            current_serial = get_machine_guid()
            if expiration_timestamp is None or current_time >= expiration_timestamp or stored_serial!= current_serial:
                warning_dialog = tk.Toplevel(self)
                warning_dialog.title('Verification Required')
                warning_dialog.geometry('300x150')
                warning_dialog.configure(bg='#222222')
                warning_dialog.resizable(False, False)
                set_window_icon(warning_dialog)
                warning_dialog.update_idletasks()
                screen_width = warning_dialog.winfo_screenwidth()
                screen_height = warning_dialog.winfo_screenheight()
                size = tuple((int(_) for _ in warning_dialog.geometry().split('+')[0].split('x')))
                x = screen_width // 2 - size[0] // 2
                y = screen_height // 2 - size[1] // 2
                warning_dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                label = tk.Label(warning_dialog, text='Please verify to update macros.', bg='#222222', fg='white', font=('Arial', 12), wraplength=280, justify='center')
                label.pack(pady=(40, 10), padx=10)

                def close_warning():
                    warning_dialog.destroy()
                ok_button = RoundedButton(warning_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_warning)
                ok_button.pack(pady=(10, 20))
                warning_dialog.transient(self)
                warning_dialog.grab_set()
                self.wait_window(warning_dialog)
                return
            try:
                response = requests.get(REMOTE_SCRIPTS_JSON_URL)
                response.raise_for_status()
                raw_filenames = response.json()
                fresh_min_roles = {}
                for item in raw_filenames:
                    parts = item.split('|')
                    if len(parts) == 3:
                        filename = parts[0].strip()
                        min_role = parts[2].strip().lower()
                    else:  # inserted
                        if len(parts) == 2:
                            filename = parts[0].strip()
                            min_role = 'member'
                        else:  # inserted
                            filename = item.strip()
                            min_role = 'member'
                    fresh_min_roles[filename] = min_role
                except Exception as e:
                    pass  # postinserted
                newest_filename = f'{base_name} v{newest_remote_version}.py'
                print(f'Looking for newest version: {newest_filename}')
                print(f'Available in fresh_min_roles: {list(fresh_min_roles.keys())}')
                allowed_roles_map = {'member': ['member', 'booster', 'giveaway_sponsor', 'donator', 'supporter'], 'giveaway_sponsor': ['giveaway_sponsor', 'booster', 'donator', 'supporter'], 'booster': ['booster', 'donator', 'supporter'], 'donator': ['donator', 'supporter'], 'supporter': ['supporter']}
                min_role_required = fresh_min_roles.get(newest_filename, 'member')
                print(f'Min role required for {newest_filename}: {min_role_required}')
                print(f'User role: {user_role}')
                if user_role is not None and user_role.lower() not in allowed_roles_map.get(min_role_required, []):
                    allowed_roles = allowed_roles_map.get(min_role_required, [])
                    allowed_roles_display = '\n'.join((role.capitalize() for role in allowed_roles))
                    print(f'Access denied. Required roles: {allowed_roles}')
                    error_dialog = tk.Toplevel(self)
                    error_dialog.title('Access Denied')
                    error_dialog.geometry('350x250')
                    error_dialog.configure(bg='#222222')
                    error_dialog.resizable(False, False)
                    set_window_icon(error_dialog)
                    error_dialog.update_idletasks()
                    sw = error_dialog.winfo_screenwidth()
                    sh = error_dialog.winfo_screenheight()
                    sz = tuple((int(_) for _ in error_dialog.geometry().split('+')[0].split('x')))
                    rx = sw // 2 - sz[0] // 2
                    ry = sh // 2 - sz[1] // 2
                    error_dialog.geometry(f'{sz[0]}x{sz[1]}+{rx}+{ry}')
                    label = tk.Label(error_dialog, text=f'The latest version of this macro is reserved\nfor users with one of these roles:\n\n{allowed_roles_display}', bg='#222222', fg='white', font=('Arial', 12), justify='center')
                    label.pack(pady=(20, 10), padx=10)

                    def close_error():
                        error_dialog.destroy()
                    ok_button = RoundedButton(error_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_error)
                    ok_button.pack(pady=(10, 20))
                    error_dialog.transient(self)
                    error_dialog.grab_set()
                    self.wait_window(error_dialog)
                else:  # inserted
                    print('User has permission, proceeding with update')
                    update_button.text = 'Updating...'
                    update_button.bg = '#004477'
                    update_button._draw_button(update_button.bg)
                    threading.Thread(target=self.download_script, args=(newest_filename, update_button, True), daemon=True).start()
                    print(f'Failed to refresh remote scripts data: {e}')
                    fresh_min_roles = min_roles if min_roles else {}
        if edit_button:
            edit_button.command = on_update_click
        if len(versions) > 1:
            base_name = tk.Frame(versions, bg='#333333')
            if edit_button:
                if not local:
                    base_name.pack(side='top', pady=(0, 2))
                else:  # inserted
                    base_name.pack(side='top', pady=(0, 0))
            else:  # inserted
                if not local:
                    base_name.pack(side='top', pady=(0, 2))
                else:  # inserted
                    base_name.pack(side='top', pady=(0, 0))
            min_roles = RoundedButton(base_name, width=40, height=30, cornerradius=10, bg='#444444', fg='white', text='◀', font=('Arial', 12, 'bold'), command=None)
            min_roles._draw_button(min_roles._lighter_color(min_roles.bg))
            box = RoundedButton(base_name, width=40, height=30, cornerradius=10, bg='#444444', fg='white', text='▶', font=('Arial', 12, 'bold'), command=None)
            box._draw_button(box._lighter_color(box.bg))
            min_roles.grid(row=0, column=0, padx=(0, 11))
            box.grid(row=0, column=1, padx=(11, 0))

            def on_left_enter(e):
                left_btn._draw_button(left_btn._lighter_color(left_btn.bg))

            def on_left_leave(e):
                left_btn._draw_button(left_btn.bg)

            def on_right_enter(e):
                right_btn._draw_button(right_btn._lighter_color(right_btn.bg))

            def on_right_leave(e):
                right_btn._draw_button(right_btn.bg)
            min_roles.bind('<Enter>', on_left_enter)
            min_roles.bind('<Leave>', on_left_leave)
            box.bind('<Enter>', on_right_enter)
            box.bind('<Leave>', on_right_leave)
            min_roles.command = None
            box.command = None

            def on_left_click(event):
                if left_btn.command:
                    left_btn.command()

            def on_right_click(event):
                if right_btn.command:
                    right_btn.command()
            min_roles.bind('<ButtonRelease-1>', on_left_click)
            box.bind('<ButtonRelease-1>', on_right_click)
        else:  # inserted
            min_roles = box = None
        self = RoundedButton(versions, width=110, height=30, cornerradius=10, bg='#00AA00', fg='white', text='PLAY', font=('Arial', 12, 'bold'), command=None)
        self.pack(side='bottom', pady=3, padx=10)

        def get_description(filename):
            if local:
                return self.get_script_description_local(filename)
            if descriptions and filename in descriptions:
                return descriptions[filename]
            return 'No description.'

        def is_version_downloaded(filename):
            if not downloaded_versions:
                return False
            return filename in downloaded_versions

        def update_arrow_buttons(idx):
            if left_btn:
                if idx == len(versions) - 1:
                    left_btn.config(state='disabled')
                    left_btn.bg = '#363636'
                    left_btn._draw_button(left_btn._lighter_color(left_btn.bg))
                else:  # inserted
                    left_btn.config(state='normal')
                    left_btn.bg = '#252525'
                    left_btn._draw_button(left_btn._lighter_color(left_btn.bg))
            if right_btn:
                if idx == 0:
                    right_btn.config(state='disabled')
                    right_btn.bg = '#363636'
                    right_btn._draw_button(right_btn._lighter_color(right_btn.bg))
                else:  # inserted
                    right_btn.config(state='normal')
                    right_btn.bg = '#252525'
                    right_btn._draw_button(right_btn._lighter_color(right_btn.bg))
        if local:
            if not hasattr(self, 'remove_buttons'):
                self.remove_buttons = {}
            if versions[0] not in self.remove_buttons:
                button_frame = tk.Frame(versions, bg='#363636', width=130)
                button_frame.pack(side='bottom', pady=(4, 2))
                arrows_frame = RoundedButton(button_frame, width=60, height=30, cornerradius=10, bg='#AA2222', fg='white', text='DEL', font=('Arial', 10, 'bold'), command=None)

                def on_remove_enter(e):
                    if remove_button['state'] == 'normal':
                        remove_button._draw_button(remove_button._lighter_color(remove_button.bg))

                def on_remove_leave(e):
                    if remove_button['state'] == 'normal':
                        remove_button._draw_button(remove_button.bg)
                arrows_frame.bind('<Enter>', on_remove_enter)
                arrows_frame.bind('<Leave>', on_remove_leave)
                arrows_frame.pack(side='left', padx=(2, 6))
                downloaded_versions = RoundedButton(button_frame, width=60, height=30, cornerradius=10, bg='#10B7D4', fg='white', text='EDIT', font=('Arial', 10, 'bold'), command=None)
                downloaded_versions.pack(side='left', fill='x', expand=True, padx=(2, 1))
                self.remove_buttons[versions[0]] = arrows_frame
                self.remove_buttons[f'edit_{versions[0]}'] = downloaded_versions
            else:  # inserted
                arrows_frame = self.remove_buttons[versions[0]]
                downloaded_versions = self.remove_buttons.get(f'edit_{versions[0]}')
                if not isinstance(arrows_frame, RoundedButton):
                    parent = arrows_frame.master
                    arrows_frame.destroy()
                    arrows_frame = RoundedButton(parent, width=60, height=30, cornerradius=10, bg='#AA2222', fg='white', text='DEL', font=('Arial', 10, 'bold'), command=None)
                    arrows_frame.pack(side='left', padx=(2, 6))
                    self.remove_buttons[versions[0]] = arrows_frame
                if not isinstance(downloaded_versions, RoundedButton):
                    parent = downloaded_versions.master
                    downloaded_versions.destroy()
                    downloaded_versions = RoundedButton(parent, width=60, height=30, cornerradius=10, bg='#10B7D4', fg='white', text='EDIT', font=('Arial', 10, 'bold'), command=None)
                    downloaded_versions.pack(side='left', fill='x', expand=True, padx=(2, 1))
                    self.remove_buttons[f'edit_{versions[0]}'] = downloaded_versions

        def update_card(idx):
            filename = versions[idx]
            display_name = os.path.splitext(filename)[0]
            name_label.config(text=display_name)
            desc_label.config(text=get_description(filename))
            update_arrow_buttons(idx)
            border_color_local = '#444444'
            resolution = self.selected_resolution.get()
            if resolution in ['1366x768', '1364x768']:
                script_path = os.path.join(self.macros_dir, filename)
                if os.path.exists(script_path):
                    try:
                        with open(script_path, 'r', encoding='utf-8') as f:
                            pass  # postinserted
                    except Exception as e:
                            for line in f:
                                line = line.strip()
                                if line.lower().startswith('# versions:'):
                                    border_color_local = '#444444'
                                    break
                            else:  # inserted
                                border_color_local = '#FF0000'
            else:  # inserted
                pass  # postinserted
            if local and newest_remote_version > newest_local_version:
                border_color_local = '#FFFF00'
            box.config(highlightbackground=border_color_local)
            if not local:
                def darken_color(hex_color, factor=0.85):
                    try:
                        c = hex_color.lstrip('#')
                        r = int(c[0:2], 16)
                        g = int(c[2:4], 16)
                        b = int(c[4:6], 16)
                        r = max(0, min(255, int(r * factor)))
                        g = max(0, min(255, int(g * factor)))
                        b = max(0, min(255, int(b * factor)))
                        return f'#{r:02x}{g:02x}{b:02x}'
                    except Exception:
                        return hex_color
                    else:  # inserted
                        pass
                role_map = {'member': '#3e73ce', 'giveaway_sponsor': '#5ae2e0', 'booster': '#f79aff', 'donator': '#d1ae00', 'supporter': '#8543ff'}
                role = (min_roles.get(filename, 'member') if min_roles else 'member').lower()
                box_bg = role_map.get(role, '#333333')
                box_border = darken_color(box_bg, 0.8)
                box.config(bg=box_bg, highlightbackground=box_border)
                name_label.config(bg=box_bg)
                desc_label.config(bg=box_bg, fg='white')
                spacer.config(bg=box_bg)
                try:
                    if 'arrows_frame' in locals() and isinstance(arrows_frame, tk.Frame):
                        arrows_frame.config(bg=box_bg)
                        arrow_bg = darken_color(box_border, 0.9)
                        if 'left_btn' in locals() and left_btn is not None:
                            left_btn.bg = arrow_bg
                            left_btn._draw_button(left_btn.bg)
                        if 'right_btn' in locals() and right_btn is not None:
                            right_btn.bg = arrow_bg
                            right_btn._draw_button(right_btn.bg)
                except Exception:
                    pass  # postinserted
                else:  # inserted
                    try:
                        if 'action_button' in locals() and action_button is not None:
                            action_button._draw_button(action_button.bg)
                except Exception:
                    pass  # postinserted
            else:  # inserted
                pass  # postinserted
            if local:
                remove_button.text = 'DEL'
                remove_button.bg = '#AA2222'
                remove_button.fg = 'white'
                remove_button.command = lambda f=filename: self.remove_script(f)
                remove_button._draw_button(remove_button.bg)

                def on_remove_enter(e):
                    remove_button._draw_button(remove_button._lighter_color(remove_button.bg))

                def on_remove_leave(e):
                    remove_button._draw_button(remove_button.bg)
                remove_button.bind('<Enter>', on_remove_enter)
                remove_button.bind('<Leave>', on_remove_leave)
                edit_button.text = 'EDIT'
                edit_button.bg = '#10B7D4'
                edit_button.fg = 'white'
                edit_button.command = lambda f=filename: self.open_script_in_editor(f)
                edit_button._draw_button(edit_button.bg)

                def on_edit_enter(e):
                    edit_button._draw_button(edit_button._lighter_color(edit_button.bg))

                def on_edit_leave(e):
                    edit_button._draw_button(edit_button.bg)
                edit_button.bind('<Enter>', on_edit_enter)
                edit_button.bind('<Leave>', on_edit_leave)
            if local:
                def play_script_with_time_check():
                    try:
                        now_ts = time.time()
                        last_ts = getattr(self, '_last_play_click_ts', 0)
                        if now_ts - last_ts < 1.0:
                            return
                        self._last_play_click_ts = now_ts
                    except Exception:
                        pass  # postinserted
                    else:  # inserted
                        pass  # postinserted
                    if self.selected_resolution.get() == 'Resolution':
                        messagebox.showerror('Error', 'Please select your resolution')
                        return
                    decrypt_result = self.decrypt_duration()
                    if decrypt_result is None:
                        expiration_timestamp = None
                        stored_serial = None
                        user_role = None
                    else:  # inserted
                        _, expiration_timestamp, stored_serial, user_role = decrypt_result
                    current_time = int(time.time())
                    current_serial = get_machine_guid()
                    expired_or_invalid = expiration_timestamp is None or current_time >= expiration_timestamp or stored_serial!= current_serial
                    if expired_or_invalid:
                        allow_override = False
                        try:
                            if self.is_special_free_run(filename):
                                local_path = os.path.join(self.macros_dir, filename)
                                if os.path.exists(local_path) and self.verify_script_matches_site(local_path, filename):
                                    allow_override = True
                    except Exception as e:
                        else:  # inserted
                            if not allow_override:
                                warning_dialog = tk.Toplevel(self)
                                warning_dialog.title('Time Expired')
                                warning_dialog.geometry('300x150')
                                warning_dialog.configure(bg='#222222')
                                warning_dialog.resizable(False, False)
                                set_window_icon(warning_dialog)
                                warning_dialog.update_idletasks()
                                screen_width = warning_dialog.winfo_screenwidth()
                                screen_height = warning_dialog.winfo_screenheight()
                                size = tuple((int(_) for _ in warning_dialog.geometry().split('+')[0].split('x')))
                                x = screen_width // 2 - size[0] // 2
                                y = screen_height // 2 - size[1] // 2
                                warning_dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                                label = tk.Label(warning_dialog, text='Please verify to run macros.', bg='#222222', fg='white', font=('Arial', 12), wraplength=280, justify='center')
                                label.pack(pady=(40, 10), padx=10)

                                def close_warning():
                                    warning_dialog.destroy()
                                ok_button = RoundedButton(warning_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_warning)
                                ok_button.pack(pady=(10, 20))
                                warning_dialog.transient(self)
                                warning_dialog.grab_set()
                                self.wait_window(warning_dialog)
                            else:  # inserted
                                print(f'[FREE-RUN] Verified match for \'{filename}\'. Allowing run without time.')
                                launch_free_run = True
                    else:  # inserted
                        launch_free_run = False
                    if not self.is_special_free_run(filename):
                        allowed_roles_map = {'member': ['member', 'booster', 'giveaway_sponsor', 'donator', 'supporter'], 'giveaway_sponsor': ['giveaway_sponsor', 'booster', 'donator', 'supporter'], 'booster': ['booster', 'donator', 'supporter'], 'donator': ['donator', 'supporter'], 'supporter': ['supporter']}
                        min_role = None
                        if min_roles and filename in min_roles:
                            min_role = min_roles[filename]
                        else:  # inserted
                            min_role = 'member'
                        if user_role is None or user_role.lower() not in allowed_roles_map.get(min_role, []):
                            allowed_roles = allowed_roles_map.get(min_role, [])
                            allowed_roles_display = '\n'.join((role.capitalize() for role in allowed_roles))
                            messagebox.showerror('Access Denied', f'This macro is reserved for users with one of these roles:\n\n{allowed_roles_display}')
                            return
                    else:  # inserted
                        print(f'[FREE-RUN] Role gate bypassed for whitelisted macro \'{filename}\'.')
                    resolution = self.selected_resolution.get()
                    if resolution in ('1366x768', '1364x768') and border_color_local == '#FF0000':
                        messagebox.showerror('Error', 'This macro won\'t work on your resolution')
                        return
                    base_name, _ = self.parse_name_version(filename)
                    key_lower = filename.lower()
                    images = []
                    for k, v in self.images_map.items():
                        if k.lower() == key_lower:
                            images = v
                            break
                    if images:
                        suffix = ''
                        if resolution == '1920x1080':
                            suffix = '2'
                        else:  # inserted
                            if resolution in ['1366x768', '1364x768']:
                                suffix = '3'

                        def download_image(img_url, img_path):
                            try:
                                img_resp = requests.get(img_url, timeout=10)
                                img_resp.raise_for_status()
                                with open(img_path, 'wb') as img_file:
                                    pass  # postinserted
                            except Exception:
                                    img_file.write(img_resp.content)
                                        return True
                                    return False
                                else:  # inserted
                                    pass
                        base_url = 'https://guy2-macros.com/images/'
                        max_retries = 3
                        retry_delay = 2
                        failures = []
                        for src_url in images:
                            base_name = os.path.basename(src_url)
                            if not base_name.lower().endswith('.png'):
                                base_name += '.png'
                            name, ext = os.path.splitext(base_name)
                            target_name = f'{name}{suffix}{ext}' if suffix else base_name
                            img_path = os.path.join(self.macros_dir, target_name)
                            if os.path.exists(img_path):
                                continue
                            full_url = base_url + target_name
                            ok = False
                            for _ in range(max_retries):
                                if download_image(full_url, img_path) and os.path.exists(img_path):
                                    ok = True
                                    break
                                time.sleep(retry_delay)
                            if not ok:
                                failures.append(target_name)
                        if failures:
                            messagebox.showerror('Missing Images', 'You are missing these images for the current resolution:\n\n' + '\n'.join(failures) + '\n\nPlease delete and re-download the macro. If this persists, create a ticket.')
                            return
                    self.run_script_in_new_cmd(filename, free_run=launch_free_run)
                        pass
                        print(f'[FREE-RUN] Override check failed for {filename}: {e}')
                action_button.text = 'PLAY'
                action_button.bg = '#00AA00'
                action_button.fg = 'white'
                action_button.command = play_script_with_time_check
                action_button._draw_button(action_button.bg)

                def on_play_enter(e):
                    action_button._draw_button(action_button._lighter_color(action_button.bg))

                def on_play_leave(e):
                    action_button._draw_button(action_button.bg)
                action_button.bind('<Enter>', on_play_enter)
                action_button.bind('<Leave>', on_play_leave)
            if not local:
                downloaded = is_version_downloaded(filename)
                if downloaded:
                    action_button.text = 'Downloaded'
                    action_button.bg = '#008800'
                    action_button.fg = 'white'
                    action_button.command = None
                    action_button._draw_button(action_button.bg)
                    action_button.unbind('<Enter>')
                    action_button.unbind('<Leave>')
                else:  # inserted
                    action_button.text = 'Download'
                    action_button.bg = '#000000'
                    action_button.fg = 'white'
                    action_button._draw_button(action_button.bg)

                    def on_download_click():
                        if self.selected_resolution.get() == 'Resolution':
                            messagebox.showerror('Error', 'Please select your resolution before downloading.')
                            return
                        decrypt_result = self.decrypt_duration()
                        if decrypt_result is None:
                            expiration_timestamp = None
                            stored_serial = None
                            user_role = None
                        else:  # inserted
                            _, expiration_timestamp, stored_serial, user_role = decrypt_result
                        current_time = int(time.time())
                        current_serial = get_machine_guid()
                        if expiration_timestamp is None or current_time >= expiration_timestamp or stored_serial!= current_serial:
                            warning_dialog = tk.Toplevel(self)
                            warning_dialog.title('Verification Required')
                            warning_dialog.geometry('300x150')
                            warning_dialog.configure(bg='#222222')
                            warning_dialog.resizable(False, False)
                            set_window_icon(warning_dialog)
                            warning_dialog.update_idletasks()
                            screen_width = warning_dialog.winfo_screenwidth()
                            screen_height = warning_dialog.winfo_screenheight()
                            size = tuple((int(_) for _ in warning_dialog.geometry().split('+')[0].split('x')))
                            x = screen_width // 2 - size[0] // 2
                            y = screen_height // 2 - size[1] // 2
                            warning_dialog.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
                            label = tk.Label(warning_dialog, text='Please verify to download macros.', bg='#222222', fg='white', font=('Arial', 12), wraplength=280, justify='center')
                            label.pack(pady=(40, 10), padx=10)

                            def close_warning():
                                warning_dialog.destroy()
                            ok_button = RoundedButton(warning_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_warning)
                            ok_button.pack(pady=(10, 20))
                            warning_dialog.transient(self)
                            warning_dialog.grab_set()
                            self.wait_window(warning_dialog)
                        else:  # inserted
                            allowed_roles_map = {'member': ['member', 'booster', 'giveaway_sponsor', 'donator', 'supporter'], 'giveaway_sponsor': ['giveaway_sponsor', 'booster', 'donator', 'supporter'], 'booster': ['booster', 'donator', 'supporter'], 'donator': ['donator', 'supporter'], 'supporter': ['supporter']}
                            min_role = None
                            if min_roles and filename in min_roles:
                                min_role = min_roles[filename]
                            else:  # inserted
                                min_role = 'member'
                            if user_role is None or user_role.lower() not in allowed_roles_map.get(min_role, []):
                                allowed_roles = allowed_roles_map.get(min_role, [])
                                allowed_roles_display = '\n'.join((role.capitalize() for role in allowed_roles))
                                error_dialog = tk.Toplevel(self)
                                error_dialog.title('Access Denied')
                                error_dialog.geometry('350x250')
                                error_dialog.configure(bg='#222222')
                                error_dialog.resizable(False, False)
                                set_window_icon(error_dialog)
                                error_dialog.update_idletasks()
                                sw = error_dialog.winfo_screenwidth()
                                sh = error_dialog.winfo_screenheight()
                                sz = tuple((int(_) for _ in error_dialog.geometry().split('+')[0].split('x')))
                                rx = sw // 2 - sz[0] // 2
                                ry = sh // 2 - sz[1] // 2
                                error_dialog.geometry(f'{sz[0]}x{sz[1]}+{rx}+{ry}')
                                label = tk.Label(error_dialog, text=f'This macro is reserved for users with\none of these roles:\n\n{allowed_roles_display}', bg='#222222', fg='white', font=('Arial', 12), justify='center')
                                label.pack(pady=(20, 10), padx=10)

                                def close_error():
                                    error_dialog.destroy()
                                ok_button = RoundedButton(error_dialog, width=80, height=30, cornerradius=10, bg='#444444', fg='white', text='OK', font=('Arial', 12, 'bold'), command=close_error)
                                ok_button.pack(pady=(10, 20))
                                error_dialog.transient(self)
                                error_dialog.grab_set()
                                self.wait_window(error_dialog)
                            else:  # inserted
                                action_button.text = 'Downloading...'
                                action_button.bg = '#1a1a1a'
                                action_button.fg = 'white'
                                action_button._draw_button(action_button.bg)
                                threading.Thread(target=self.download_script, args=(filename, action_button)).start()
                    action_button.command = on_download_click

                def on_enter(e):
                    action_button._draw_button(action_button._lighter_color(action_button.bg))

                def on_leave(e):
                    action_button._draw_button(action_button.bg)
                action_button.bind('<Enter>', on_enter)
                action_button.bind('<Leave>', on_leave)
            self.script_buttons[filename] = action_button
                            print(f'Failed to read VERSIONS line in {script_path}: {e}')
                            pass
                            pass
                        else:  # inserted
                            pass

        def prev_version():
            nonlocal current_index  # inserted
            if current_index < len(versions) - 1:
                current_index += 1
                update_card(current_index)

        def next_version():
            nonlocal current_index  # inserted
            if current_index > 0:
                current_index -= 1
                update_card(current_index)
        if min_roles and box:
            min_roles.command = prev_version
            box.command = next_version
        get_description(local)
        if local and len(versions) == 1:
            filename = versions[0]
            if not hasattr(self, 'remove_buttons'):
                self.remove_buttons = {}
            if filename not in self.remove_buttons:
                arrows_frame = tk.Button(versions, text='REMOVE', font=('Arial', 10, 'bold'), bg='#AA2222', fg='white', activebackground='#881111', bd=0, width=11, command=lambda f=filename: self.remove_script(f))
                self.remove_buttons[filename] = arrows_frame
                arrows_frame.pack(side='bottom', pady=(0, 5))
                        print(f'Failed to read VERSIONS line in {script_path}: {e}')

    def get_script_description_local(self, filename):
        script_path = os.path.join(self.macros_dir, filename)
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                pass  # postinserted
        except:
            pass  # postinserted
        return 'No description.'
                for line in f:
                    line = line.strip()
                    if line.startswith('# DESCRIPTION:'):
                        return line.replace('# DESCRIPTION:', '').strip()
                    else:  # inserted
                        if line.startswith('DESCRIPTION'):
                            parts = line.split('=', 1)
                            if len(parts) == 2:
                                return parts[1].strip().strip('\'\"')
                    return 'No description.'

    def load_scripts_list(self):
        try:
            r = requests.get(REMOTE_SCRIPTS_JSON_URL)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print('Failed to load macros.json:', e)
            return []
        else:  # inserted
            pass

    def update_buttons_based_on_downloads(self):
        local_files = set(os.listdir(self.macros_dir))
        for script, btn in self.script_buttons.items():
            if script in local_files:
                btn.config(text='Downloaded', state='disabled', bg='#008800', fg='white')
            else:  # inserted
                btn.config(text='Download', state='normal', bg='#000000', fg='white')

    def download_script(self, filename, button, is_update=False):
        try:
            vm = os.path.join(SCRIPTS_DIR, 'version_main.txt')
            if os.path.exists(vm):
                run_path = os.path.join(SCRIPTS_DIR, 'run.exe')
                main_path = os.path.join(SCRIPTS_DIR, 'main.exe')
                if not os.path.exists(run_path) or not os.path.exists(main_path):
                    self.ensure_core_binaries()
            except Exception as _e:
                pass  # postinserted
        else:  # inserted
            if '|' in filename:
                filename = filename.split('|', 1)[0].strip()
        clean_filename = filename.strip()
        url = f'https://guy2-macros.com/scripts/{clean_filename}'
        target_dir = self.macros_dir
        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, clean_filename)
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            if not hasattr(self, 'raw_entries_map'):
                self.raw_entries_map = {}
            raw_entry = self.raw_entries_map.get(clean_filename, '')
            if is_update:
                pass  # postinserted
        except Exception as e:
            else:  # inserted
                try:
                    response = requests.get(REMOTE_SCRIPTS_JSON_URL)
                    response.raise_for_status()
                    raw_filenames = response.json()
                    self.raw_entries_map = {}
                    for item in raw_filenames:
                        parts = item.split('|')
                        fname = parts[0].strip() if parts else item.strip()
                        self.raw_entries_map[fname] = item
            except Exception as e:
                            raw_entry = self.raw_entries_map.get(clean_filename, '')
                if raw_entry.count('|') == 3:
                    def xor_decrypt(data: bytes, key: bytes) -> bytes:
                        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
                    key = b'aK3pQv9XmRzT1bHnW6LuF2YgDeCsJ4'
                    decoded_bytes = base64.b64decode(r.content)
                    decrypted_bytes = xor_decrypt(decoded_bytes, key)
                    with open(path, 'wb') as f:
                        f.write(decrypted_bytes)
                else:  # inserted
                    with open(path, 'wb') as f:
                        f.write(r.content)
            else:  # inserted
                try:
                    if not hasattr(self, 'saved_on_key') or not hasattr(self, 'saved_off_key'):
                        import json
                        if os.path.exists(KEYBINDS_FILE):
                            with open(KEYBINDS_FILE, 'r', encoding='utf-8') as jf:
                                pass  # postinserted
            except Exception as e:
                                data = json.load(jf)
                                self.saved_on_key = data.get('on')
                                self.saved_off_key = data.get('off')
                    if getattr(self, 'saved_on_key', None) and getattr(self, 'saved_off_key', None):
                        self.modify_script_keybinds_at_path(path, self.saved_on_key, self.saved_off_key, silent=True)
                else:  # inserted
                    key_lower = clean_filename.lower()
                    images = []
                    for k, v in self.images_map.items():
                        if k.lower() == key_lower:
                            images = v
                            break
                    if images:
                        resolution = self.selected_resolution.get()
                        suffix = ''
                        if resolution == '1920x1080':
                            suffix = '2'
                        else:  # inserted
                            if resolution in ['1366x768', '1364x768']:
                                suffix = '3'

                        def download_image(img_url, img_path):
                            try:
                                img_resp = requests.get(img_url, timeout=10)
                                img_resp.raise_for_status()
                                with open(img_path, 'wb') as img_file:
                                    pass  # postinserted
                            except Exception:
                                    img_file.write(img_resp.content)
                                        return True
                                    return False
                                else:  # inserted
                                    pass
                        max_retries = 3
                        retry_delay = 2
                        base_url = 'https://guy2-macros.com/images/'
                        img_base_dir = target_dir
                        failed_images = []
                        for src_url in images:
                            img_name = os.path.basename(src_url)
                            if not img_name.lower().endswith('.png'):
                                img_name += '.png'
                            name, ext = os.path.splitext(img_name)
                            if suffix:
                                img_name = f'{name}{suffix}{ext}'
                            img_path = os.path.join(img_base_dir, img_name)
                            new_img_url = base_url + img_name
                            success = False
                            for _ in range(max_retries):
                                if os.path.exists(img_path):
                                    success = True
                                    break
                                if download_image(new_img_url, img_path) and os.path.exists(img_path):
                                    success = True
                                    break
                                time.sleep(retry_delay)
                            if not success:
                                failed_images.append(img_name)
                        else:  # inserted
                            if failed_images:
                                messagebox.showerror('Image Download Error', 'The following images could not be downloaded after multiple attempts:\n\n' + '\n'.join(failed_images) + '\n\nPlease delete and download the macro again. If this persists, create a ticket.')

                    def update_button_ui():
                        if button.winfo_exists():
                            button.text = 'Downloaded'
                            button.bg = '#008800'
                            button.fg = 'white'
                            button._draw_button(button.bg)
                    self.after(0, update_button_ui)
                    self.after(0, self.show_local_scripts)
                print(f'[CORE DL] Skipping precheck during download: {_e}')
                print(f'Failed to refresh remote scripts list: {e}')
            print(f'[KEYBINDS] Failed to apply saved keybinds to {clean_filename}: {e}')
            messagebox.showerror('Download failed', f'Failed to download {clean_filename}:\n{e}')

            def reset_button_ui():
                if button.winfo_exists():
                    button.text = 'Download'
                    button.bg = '#000000'
                    button.fg = 'white'
                    button._draw_button(button.bg)
            self.after(0, reset_button_ui)

    def send_macro_usage(self, macro_name: str, seconds: int):
        """Send macro usage stats to external API.\n\n        Payload format: { \"macro\": <base_name>, \"seconds\": <int_seconds> }\n        """  # inserted
        try:
            payload = {'macro': macro_name, 'seconds': int(seconds)}
            resp = requests.post(MACRO_USAGE_API_URL, json=payload, timeout=10)
            print(f'[USAGE] Sent usage for \'{macro_name}\' = {seconds}s, status={resp.status_code}')
        except Exception as e:
            print(f'[USAGE] Failed to send usage for \'{macro_name}\': {e}')
            return None
        else:  # inserted
            pass

    def track_macro_usage(self, proc: subprocess.Popen, macro_name: str, pid: int):
        """Track a launched macro process and report usage when it exits.\n\n        Checks every 10 seconds whether the process is still running. When it\n        terminates, if runtime > 20 seconds, sends the usage to the API.\n        """  # inserted
        start_time = time.time()
        print(f'[USAGE] Tracking started for \'{macro_name}\' (pid={pid})')
        try:
            while True:
                if proc.poll() is not None:
                    break
                time.sleep(10)
            except Exception as e:
                finally:  # inserted
                    elapsed = int(time.time() - start_time)
                    print(f'[USAGE] Tracking finished for \'{macro_name}\' (pid={pid}), elapsed={elapsed}s')
                    if elapsed > 20:
                        self.send_macro_usage(macro_name, elapsed)
                    else:  # inserted
                        print(f'[USAGE] Elapsed <= 20s, not reporting for \'{macro_name}\'')
                    try:
                        if hasattr(self, 'free_run_pids') and pid in self.free_run_pids:
                            self.free_run_pids.discard(pid)
                            print(f'[FREE-RUN] Removed PID {pid} from exemption list.')
        except Exception:
                print(f'[USAGE] Monitoring error for \'{macro_name}\' (pid={pid}): {e}')
            return

    def run_script_in_new_cmd(self, filename, free_run=False):
        script_path = os.path.join(self.macros_dir, filename)
        if not self.ensure_core_binaries():
            return
        proc = subprocess.Popen([EXECUTOR_PATH, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=SCRIPTS_DIR)
        self.cmd_processes.append(proc)
        if free_run:
            try:
                self.free_run_pids.add(proc.pid)
                print(f'[FREE-RUN] Marked PID {proc.pid} as exempt from expiry termination.')
            except Exception:
                pass  # postinserted
        else:  # inserted
            pass  # postinserted
        base_name, _ = self.parse_name_version(filename)
        threading.Thread(target=self.track_macro_usage, args=(proc, base_name, proc.pid), daemon=True).start()
                pass
            else:  # inserted
                pass

    def ensure_core_binaries(self) -> bool:
        """Ensure main.exe and run.exe exist in SCRIPTS_DIR.\n\n        If missing but version_main.txt exists, auto-download the missing files\n        from trusted release URLs, then proceed. If downloads fail or the\n        version marker is absent, show an error and return False.\n        """  # inserted
        try:
            run_path = os.path.join(SCRIPTS_DIR, 'run.exe')
            main_path = os.path.join(SCRIPTS_DIR, 'main.exe')
            version_marker = os.path.join(SCRIPTS_DIR, 'version_main.txt')
            run_exists = os.path.exists(run_path)
            main_exists = os.path.exists(main_path)
            if run_exists and main_exists:
                return True
            if os.path.exists(version_marker):
                os.makedirs(SCRIPTS_DIR, exist_ok=True)

                def dl(url, dest):
                    try:
                        resp = requests.get(url, timeout=20)
                        resp.raise_for_status()
                        with open(dest, 'wb') as f:
                            pass  # postinserted
                    except Exception as e:
                            f.write(resp.content)
                                return True
                            print(f'[CORE DL] Failed to download {url}: {e}')
                            return False
                ok = True
                if not main_exists:
                    print('[CORE DL] main.exe missing; downloading...')
                    ok = dl(MAIN_EXE_URL, main_path) and ok
                if not run_exists:
                    print('[CORE DL] run.exe missing; downloading...')
                    ok = dl(RUN_EXE_URL, run_path) and ok
                if ok and os.path.exists(main_path) and os.path.exists(run_path):
                    print('[CORE DL] Core binaries restored.')
                    return True
        except Exception as e:
            else:  # inserted
                messagebox.showerror('Download Failed', 'Failed to download main.exe/run.exe\nPlease check your internet connection or click \'Update Launcher\'.')
                return False
            else:  # inserted
                missing = []
                if not main_exists:
                    missing.append('main.exe')
                if not run_exists:
                    missing.append('run.exe')
                messagebox.showerror('Missing Files', 'Required file(s) are missing: ' + ', '.join(missing) + '\nPlease click \'Update Launcher\' or reinstall the launcher.')
                return False
                print(f'[CORE DL] ensure_core_binaries error: {e}')
                messagebox.showerror('Error', f'Failed to verify core files:\n{e}')
                return False
            else:  # inserted
                pass

    def exit(self, event=None):
        """Close all script windows and exit"""  # inserted
        self.terminate_all_script_processes()
        self.destroy()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.winfo_x() + deltax
        new_y = self.winfo_y() + deltay
        self.geometry(f'+{new_x}+{new_y}')

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int((-1) * (event.delta / 120)), 'units')

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def open_script_in_editor(self, filename):
        script_path = os.path.join(self.macros_dir, filename)
        try:
            if platform.system() == 'Windows':
                vscode_path = shutil.which('Code.cmd') or shutil.which('Code.exe')
                if not vscode_path:
                    user_profile = os.environ.get('USERPROFILE', '')
                    possible_path = os.path.join(user_profile, 'AppData', 'Local', 'Programs', 'Microsoft VS Code', 'Code.exe')
                    if os.path.exists(possible_path):
                        vscode_path = possible_path
                if vscode_path:
                    subprocess.Popen([vscode_path, script_path], creationflags=subprocess.CREATE_NO_WINDOW)
                else:  # inserted
                    subprocess.Popen(['notepad.exe', script_path], creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            else:  # inserted
                os.startfile(script_path)
                messagebox.showerror('Error', f'Failed to open editor:\n{e}')

def check_and_update_launcher(self):
    launcher_url = 'https://github.com/LisekGuy2/Launcher/releases/download/launcher/GUY2.Launcher.exe'
    version_url = 'https://guy2-macros.com/launcher/version_launcher.txt'
    local_version_path = os.path.join(SCRIPTS_DIR, 'version_launcher.txt')
    local_launcher_path = os.path.join(SCRIPTS_DIR, 'GUY2 Launcher.exe')
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    desktop_shortcut_path = os.path.join(desktop_path, 'launcher.lnk')

    def get_remote_version():
        try:
            with urllib.request.urlopen(version_url) as response:
                pass  # postinserted
        except Exception as e:
                return response.read().decode().strip()
                print(f'Failed to fetch the launcher version: {e}')

    def get_local_version():
        if os.path.exists(local_version_path):
            with open(local_version_path, 'r') as f:
                return f.read().strip()

    def download_file(url, path):
        try:
            dest_path = path
            if url.lower().endswith('guy2.launcher.exe'):
                dest_path = os.path.join(os.path.dirname(path), 'GUY2 Launcher.exe')
            safe_url = urllib.parse.quote(url, safe=':/')
            with urllib.request.urlopen(safe_url) as response:
                pass  # postinserted
        except Exception as e:
                with open(dest_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                    print(f'Downloaded {os.path.basename(dest_path)} to {dest_path}')
                    return True
                print(f'Failed to download {url}: {e}')
                return False

    def delete_if_exists(path):
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f'Deleted old launcher at {path}')
        except Exception as e:
            print(f'Failed to delete {path}: {e}')

    def create_shortcut(target, shortcut_path, description='Launcher Shortcut'):
        try:
            pythoncom.CoInitialize()
            shell = win32com.client.Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.Description = description
            shortcut.save()
            print(f'Created shortcut at {shortcut_path}')
        except Exception as e:
            print(f'Failed to create shortcut: {e}')
            return
        else:  # inserted
            pass
    remote_version = get_remote_version()
    local_version = get_local_version()
    for fname in ['version.txt', 'launcher_version.txt']:
        fpath = os.path.join(SCRIPTS_DIR, fname)
        delete_if_exists(fpath)
    required_files = [{'filename': 'main.exe', 'url': 'https://github.com/LisekGuy2/Launcher/releases/download/launcher/main.exe'}, {'filename': 'run.exe', 'url': 'https://github.com/LisekGuy2/Launcher/releases/download/launcher/run.exe'}, {'filename': 'version_launcher.txt', 'url': version_url}]
    for fileinfo in required_files:
        fpath = os.path.join(SCRIPTS_DIR, fileinfo['filename'])
        if not os.path.exists(fpath):
            print(f"{fileinfo['filename']} not found, trying to download it.")
            success = download_file(fileinfo['url'], fpath)
            if not success:
                messagebox.showerror('Download Failed', f"Failed to download {fileinfo['filename']}.\nPlease try again")
    if local_version is None or remote_version!= local_version:
        print('Launcher version mismatch or missing, updating launcher...')
        if not os.path.exists(SCRIPTS_DIR):
            os.makedirs(SCRIPTS_DIR)
        success = download_file(launcher_url, local_launcher_path)
        if not success:
            messagebox.showerror('Launcher Update Failed', 'Failed to update the launcher. Please try again')
            webbrowser.open('https://github.com/LisekGuy2/Launcher/releases/download/launcher/GUY2.Launcher.exe')
            return
        unwanted_launcher = os.path.join(SCRIPTS_DIR, 'GUY2.Launcher.exe')
        delete_if_exists(unwanted_launcher)
        if remote_version is not None:
            success = download_file(version_url, local_version_path)
            if not success:
                print('Failed to download version_launcher.txt')

        def delete_matching_files(folder, pattern):
            files = glob.glob(os.path.join(folder, pattern))
            for f in files:
                try:
                    os.remove(f)
                    print(f'Deleted old launcher file: {f}')
                except Exception as e:
                    pass  # postinserted
                print(f'Failed to delete {f}: {e}')
        delete_matching_files(downloads_path, 'GUY2 Launcher*.exe')
        delete_matching_files(desktop_path, 'GUY2 Launcher*.exe')
        delete_matching_files(downloads_path, 'GUY2.Launcher*.exe')
        delete_matching_files(desktop_path, 'GUY2.Launcher*.exe')
        create_shortcut(local_launcher_path, desktop_shortcut_path)
    else:  # inserted
        print('Launcher is up to date.')
setattr(ScriptLauncher, 'check_and_update_launcher', check_and_update_launcher)
original_init = ScriptLauncher.__init__

def new_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    self.check_and_update_launcher()
    try:
        self.after(200, self.prompt_for_webhook_if_missing)
    except Exception as _e:
        print(f'[WEBHOOK] Skipping initial prompt: {_e}')
        return
    else:  # inserted
        pass
ScriptLauncher.__init__ = new_init

def prompt_for_webhook_if_missing(self, force: bool=False):
    try:
        webhook_path = os.path.join(SCRIPTS_DIR, 'webhook.txt')
        if os.path.exists(webhook_path) and (not force):
            return
        dialog = tk.Toplevel(self)
        dialog.title('Add Webhook (optional)')
        dialog.configure(bg='#222222')
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        set_window_icon(dialog)
        dialog.update_idletasks()
        width, height = (520, 210)
        sw, sh = (dialog.winfo_screenwidth(), dialog.winfo_screenheight())
        x = sw // 2 - width // 2
        y = sh // 2 - height // 2
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        title = tk.Label(dialog, text='Add a webhook for the macros!', bg='#222222', fg='white', font=('Arial', 13, 'bold'))
        title.pack(padx=16, pady=(16, 6), anchor='w')
        info = tk.Label(dialog, text='If you use macros that have a webhook function, enter the URL below\nfor it to automatically apply it to the macros.\nYou can skip this and add it later.', bg='#222222', fg='#CCCCCC', font=('Arial', 10), justify='left')
        info.pack(padx=16, pady=(0, 10), anchor='w')
        entry_var = tk.StringVar()
        entry = tk.Entry(dialog, textvariable=entry_var, font=('Arial', 11), bg='#444444', fg='white', insertbackground='white', relief='flat', bd=2)
        entry.pack(padx=16, pady=(0, 12), fill='x')
        entry.focus_set()
        btns = tk.Frame(dialog, bg='#222222')
        btns.pack(padx=16, pady=(0, 16))

        def save_and_close():
            url = entry_var.get().strip()
            if not url:
                messagebox.showwarning('Missing', 'Please paste a webhook URL or click Cancel.')
                return
            try:
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme not in ('https', 'http') or not parsed.netloc:
                    raise ValueError('Invalid URL')
            except Exception:
                pass  # postinserted
            else:  # inserted
                pass  # postinserted
            try:
                os.makedirs(SCRIPTS_DIR, exist_ok=True)
                with open(webhook_path, 'w', encoding='utf-8') as f:
                    pass  # postinserted
            except Exception as e:
                    f.write(url.strip() + '\n')
                        print(f'[WEBHOOK] Saved to {webhook_path}')
                        dialog.destroy()
                messagebox.showerror('Invalid URL', 'That doesn\'t look like a valid webhook URL.')
                return None
            else:  # inserted
                pass
                messagebox.showerror('Error', f'Failed to save webhook.txt:\n{e}')
                return None

        def skip_and_close():
            dialog.destroy()
    except Exception as e:
        pass  # postinserted
    else:  # inserted
        try:
            inner = tk.Frame(btns, bg='#222222')
            inner.pack()
            cancel_btn = RoundedButton(inner, width=110, height=34, cornerradius=10, bg='#AA2222', fg='white', text='Cancel', font=('Arial', 12, 'bold'), command=skip_and_close)
            cancel_btn.pack(side='left', padx=(0, 12))
            save_btn = RoundedButton(inner, width=110, height=34, cornerradius=10, bg='#00AA00', fg='white', text='Save', font=('Arial', 12, 'bold'), command=save_and_close)
            save_btn.pack(side='left')
        except Exception:
            pass  # postinserted
        else:  # inserted
            dialog.bind('<Return>', lambda _e: save_and_close())
            dialog.protocol('WM_DELETE_WINDOW', skip_and_close)
            dialog.wait_window()
            inner = tk.Frame(btns, bg='#222222')
            inner.pack()
            tk.Button(inner, text='Cancel', command=skip_and_close, bg='#AA2222', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=(0, 12))
            tk.Button(inner, text='Save', command=save_and_close, bg='#00AA00', fg='white', font=('Arial', 10, 'bold')).pack(side='left')
            print(f'[WEBHOOK] Prompt failed: {e}')
            return None
        else:  # inserted
            pass
setattr(ScriptLauncher, 'prompt_for_webhook_if_missing', prompt_for_webhook_if_missing)

def update_launcher_button_clicked(self):
    def delete_file_if_exists(path):
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f'Failed to delete {path}: {e}')

    def download_launcher(url, path):
        try:
            with urllib.request.urlopen(url) as response:
                pass  # postinserted
        except Exception as e:
                with open(path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                    return True
                print(f'Failed to download launcher: {e}')
                return False

    def run_launcher():
        launcher_path = os.path.join(SCRIPTS_DIR, 'GUY2 Launcher.exe')
        if os.path.exists(launcher_path):
            try:
                os.startfile(launcher_path)
                return
            except Exception as e:
                pass  # postinserted
        else:  # inserted
            url = 'https://github.com/LisekGuy2/Launcher/releases/download/launcher/GUY2.Launcher.exe'
            success = download_launcher(url, launcher_path)
            if success:
                try:
                    os.startfile(launcher_path)
        except Exception as e:
            else:  # inserted
                webbrowser.open(url)
            print(f'Failed to run launcher: {e}')
            return
        else:  # inserted
            pass
            print(f'Failed to run launcher after download: {e}')
            return None

    def task():
        version_main_path = os.path.join(SCRIPTS_DIR, 'version_main.txt')
        version_launcher_path = os.path.join(SCRIPTS_DIR, 'version_launcher.txt')
        delete_file_if_exists(version_main_path)
        delete_file_if_exists(version_launcher_path)
        time.sleep(0.5)
        if os.path.exists(version_main_path) or os.path.exists(version_launcher_path):
            print('Failed to delete version files.')
            return
        run_launcher()
        self.destroy()
    threading.Thread(target=task, daemon=True).start()
setattr(ScriptLauncher, 'update_launcher_button_clicked', update_launcher_button_clicked)

def xor_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def decrypt_guid(enc_guid_hex: str, key: bytes) -> str:
    try:
        encrypted_bytes = bytes.fromhex(enc_guid_hex.strip())
        decrypted_bytes = xor_decrypt(encrypted_bytes, key)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        print(f'Failed to decrypt GUID: {e}')
        return None
    else:  # inserted
        pass

def check_blacklist():
    key_raw = b'aK3pQv9XmRzT1bHnW6LuF2YgDeCsJ4'
    key = hashlib.sha256(key_raw).digest()
    try:
        response = requests.get('https://guy2-macros.com/blacklist/blacklist.txt', timeout=10)
        response.raise_for_status()
        encrypted_guids = [line.strip() for line in response.text.splitlines() if line.strip()]
    except Exception as e:
        else:  # inserted
            motherboard_serial = get_machine_guid()
            if not motherboard_serial:
                print('Could not get motherboard serial')
                return False
                print(f'Blacklisted GUID found: {dec_guid}')
                return True
        print(f'Failed to check blacklist: {e}')
        return False
if __name__ == '__main__':
    loading_screen = create_loading_screen()
    initialization_step = 0
    main_app = None

    def perform_initialization():
        """Perform initialization steps in the main thread"""  # inserted
        global main_app  # inserted
        global initialization_step  # inserted
        if initialization_step == 0:
            initialization_step = 1
            loading_screen.after(1500, perform_initialization)
        else:  # inserted
            if initialization_step == 1:
                try:
                    if check_blacklist():
                        loading_screen.destroy()
                        show_blacklist_error_and_exit()
                    else:  # inserted
                        initialization_step = 2
                        loading_screen.after(500, perform_initialization)
                except Exception as e:
                    pass  # postinserted
            else:  # inserted
                if initialization_step == 2:
                    try:
                        loading_screen.destroy()
                        main_app = ScriptLauncher()
                        threading.Thread(target=blacklist_check_loop, args=(main_app,), daemon=True).start()
                        main_app.mainloop()
            except Exception as e:
                print(f'Error during initialization: {e}')
                initialization_step = 2
                loading_screen.after(100, perform_initialization)
            else:  # inserted
                pass
                print(f'Error during app creation: {e}')
                traceback.print_exc()
                try:
                    loading_screen.destroy()
                except:
                    break
            else:  # inserted
                pass
    loading_screen.after(100, perform_initialization)
    loading_screen.mainloop()