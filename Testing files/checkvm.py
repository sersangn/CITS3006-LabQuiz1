import os
import platform

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

    return False

print(is_virtual_environment())