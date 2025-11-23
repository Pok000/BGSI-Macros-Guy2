import ctypes
import win32gui
import win32con
import sys
import os
import win32api

# DESCRIPTION: QoL window alignment and resizing
# VERSIONS: all

# yes this was made with AI and yes it was made in march of 2025
def get_windows_by_title(title):
    hwnds = []

    def enum_callback(hwnd, _):
        window_title = win32gui.GetWindowText(hwnd).lower()
        if win32gui.IsWindowVisible(hwnd):
            if title.startswith("*") and title.endswith("*"):
                if title[1:-1].lower() in window_title:
                    hwnds.append(hwnd)
            elif title.startswith("*"):
                if window_title.endswith(title[1:].lower()):
                    hwnds.append(hwnd)
            elif title.endswith("*"):
                if window_title.startswith(title[:-1].lower()):
                    hwnds.append(hwnd)
            elif title.lower() == window_title:
                hwnds.append(hwnd)

    win32gui.EnumWindows(enum_callback, None)
    return hwnds

def force_minimum_size(hwnd, width, height, x, y):
    try:
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE))
        win32gui.SetWindowPos(hwnd, None, x, y, width, height, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
        ctypes.windll.user32.SetWindowPos(hwnd, None, x, y, width, height, win32con.SWP_NOZORDER | win32con.SWP_NOSENDCHANGING)
    except Exception as e:
        print(f"Error resizing window {hwnd}: {str(e)}")

def main():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
        sys.exit()

    os.system('cls')
    title = input("Enter window title: ")
    size_input = input("\nPlease note that if you want to resize RDP's then they can't be in full screen\nEnter dimensions or grid (e.g., '300 200' for width and height, or '3x4' for a grid layout): ")

    if "x" in size_input:
        grid_size = size_input.split("x")
        
        if len(grid_size) != 2:
            print("Invalid grid input format!")
            return
        
        try:
            rows = int(grid_size[0])
            cols = int(grid_size[1])
        except ValueError:
            print("Invalid grid format! Please enter numbers.")
            return
        
        if rows > 7 or cols > 7:
            print("Too big! Maximum grid size is 7x7.")
            return

        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        
        hwnds = get_windows_by_title(title)
        if not hwnds:
            print("No windows found with that title!")
            return

        window_width = screen_width // cols
        window_height = screen_height // rows

        print(f"Screen resolution: {screen_width}x{screen_height}")
        print(f"Placing {len(hwnds)} windows in a {rows}x{cols} grid.")

        for i, hwnd in enumerate(hwnds):
            row = i // cols
            col = i % cols

            x = col * window_width
            y = row * window_height

            force_minimum_size(hwnd, window_width, window_height, x, y)

        print("\nDone!")
        input("\nPress Enter to exit...")
        return
    size_values = size_input.split()

    if len(size_values) == 1:
        width = int(size_values[0])
        height = int(width * 9 / 16)

    elif len(size_values) == 2:
        width = int(size_values[0])
        height = int(size_values[1])

    else:
        print("Invalid input format!")
        return

    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    
    hwnds = get_windows_by_title(title)
    if not hwnds:
        print("No windows found with that title!")
        return

    print(f"Screen resolution: {screen_width}x{screen_height}")
    print(f"Resizing {len(hwnds)} windows to {width}x{height}...")

    for i, hwnd in enumerate(hwnds):

        row = i // (screen_width // width)
        col = i % (screen_width // width)
        
        x = col * width
        y = row * height

        force_minimum_size(hwnd, width, height, x, y)

    print("\nDone!")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()