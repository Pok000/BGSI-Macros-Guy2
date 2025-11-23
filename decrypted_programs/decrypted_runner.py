# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: run.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import sys
import runpy
import ast
import importlib
import ctypes
import traceback
KNOWN_OPTIONAL_MODULES = ['tkinter', 'pywinauto', 'win32gui', 'win32con', 'win32api', 'pygetwindow', 'pydirectinput', 'pyautogui', 'pyperclip', 'pynput', 'pynput.keyboard', 'pynput.mouse', 'cv2', 'numpy', 'PIL', 'PIL.Image', 'PIL.ImageGrab', 'screeninfo', 'mss', 'ahk', 'requests', 'keyboard']

def _collect_for_freeze():
    if os.environ.get('FREEZE_COLLECT_IMPORTS') == '1':
        for name in KNOWN_OPTIONAL_MODULES:
            try:
                importlib.import_module(name)
            except Exception:
                pass  # postinserted
        pass
    else:  # inserted
        pass

def parse_required_modules(file_path):
    """Parse top-level imports from the target script and return a set of root module names.\n\n    This is informational and can be used to pre-import if you want to warm caches,\n    but it\'s not necessary for correctness.\n    """  # inserted
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            pass  # postinserted
    except Exception:
            src = f.read()
                tree = ast.parse(src, filename=file_path)
            else:  # inserted
                mods = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            root = (alias.name or '').split('.')[0]
                            if root:
                                mods.add(root)
                    else:  # inserted
                        if isinstance(node, ast.ImportFrom) and node.module:
                            root = node.module.split('.')[0]
                            if root:
                                mods.add(root)
                return mods
            return set()

def main():
    if len(sys.argv) < 2:
        print('Usage: run.exe <script_path>')
        sys.exit(1)
    script_path = sys.argv[1]
    _collect_for_freeze()
    try:
        sys.path.insert(0, os.path.dirname(sys.executable))
    except Exception:
        pass  # postinserted
    else:  # inserted
        try:
            os.chdir(os.path.dirname(script_path))
    except Exception:
        else:  # inserted
            needed = parse_required_modules(script_path)
            if os.environ.get('DEBUG_IMPORTS') == '1':
                print('[Launcher] Detected imports:', ', '.join(sorted(needed)) or '<none>')
        try:
            runpy.run_path(script_path, run_name='__main__')
        except SystemExit:
            pass  # postinserted
        pass
    else:  # inserted
        pass
        pass
    else:  # inserted
        pass
        return
    except Exception as e:
        tb = traceback.format_exc()
        print(f'ERROR: {e}\n{tb}')
        if os.environ.get('DEBUG_MODE'):
            input('\nPress Enter to exit...')
    else:  # inserted
        pass
if __name__ == '__main__':
    main()