import platform
import os
import ctypes

def display_message():
    os_type = platform.system()
    if os_type == "Windows":
        ctypes.windll.user32.MessageBoxW(0, "You've been infected by HydraInfect!", "Malware Alert", 1)
    elif os_type == "Darwin":  # macOS
        os.system('osascript -e \'display dialog "You\'ve been infected by HydraInfect!"\'')
    elif os_type == "Linux":
        os.system('zenity --info --text="You\'ve been infected by HydraInfect!"')
    else:
        print("You've been infected by HydraInfect!")  # Fallback for other OSes