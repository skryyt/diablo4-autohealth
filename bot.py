import time
import keyboard
import pyautogui
import tkinter as tk
from win32gui import FindWindow, SetForegroundWindow
from win32api import keybd_event

# Constants for virtual key codes
VK_Q = 0x51

# ANSI escape codes for colored text
ANSI_GREEN_BOLD = "\033[1;32m"  # Bold green text
ANSI_RESET = "\033[0m"          # Reset to default text color

class OverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-topmost', True)  # Keep the window on top
        self.root.attributes('-alpha', 0.5)      # Set transparency
        self.root.geometry("300x100")            # Set the window size
        self.label = tk.Label(root, text="Script is running...", bg="black", fg="white")
        self.label.pack(expand=True, fill='both')
        
        self.check_health_and_use_potion()  # Start monitoring health

    def bring_game_to_foreground(self, window_title):
        """Bring the game window to the foreground by its title."""
        hwnd = FindWindow(None, window_title)
        
        if hwnd:
            SetForegroundWindow(hwnd)
        else:
            print(f"Nie znaleziono okna gry o tytule '{window_title}'!")  # Game window not found

    def press_key(self, key_code):
        """Simulate a key press event."""
        keybd_event(key_code, 0, 0, 0)      # Key down event
        time.sleep(0.05)                    # Short delay
        keybd_event(key_code, 0, 0x0002, 0) # Key up event

    def check_health_and_use_potion(self):
        """Continuously monitor health and use potion when necessary."""
        while True:
            if keyboard.is_pressed('q'):
                print("Zamknięcie skryptu...")  # Quitting script
                self.root.destroy()  # Close the overlay
                return

            coords_and_colors = [
                ((629, 909), (18, 20, 23)),  # Coordinates and RGB color to check
            ]

            for (x, y), expected_color in coords_and_colors:
                pixel_color = pyautogui.pixel(x, y)
                
                if pixel_color == expected_color:
                    self.bring_game_to_foreground("Diablo IV")
                    self.press_key(VK_Q)
                    print(f"{ANSI_GREEN_BOLD}Zdrowie uzupełnione! Użyto mikstury w współrzędnych ({x}, {y}) z kolorem {expected_color}!{ANSI_RESET}")
                    break
                else:
                    print(f"Kolor w ({x}, {y}) to {pixel_color}. Oczekiwanie na właściwy kolor...")

            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = OverlayApp(root)
    root.mainloop()
