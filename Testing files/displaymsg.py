#This works for mac now

import platform
import os
import ctypes
import subprocess

def display_message():
    os_type = platform.system()
    if os_type == "Windows":
        ctypes.windll.user32.MessageBoxW(0, "You've been infected by HydraInfect!", "Malware Alert", 1)
    elif os_type == "Darwin":  # macOS
        try:
            subprocess.run(['osascript', '-e', 'display dialog "You\'ve been infected by HydraInfect!"'])
        except Exception as e:
            print(f"Failed to display message on macOS: {e}")
    elif os_type == "Linux":
        try:
            subprocess.run(['zenity', '--info', '--text=You\'ve been infected by HydraInfect!'])
        except Exception as e:
            print(f"Failed to display message on Linux: {e}")
    else:
        print("You've been infected by HydraInfect!")  # Fallback for other OSes
