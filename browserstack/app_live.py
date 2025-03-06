import os
import requests
from requests.auth import HTTPBasicAuth
import time
import webbrowser
import urllib.parse

BROWSERSTACK_USERNAME = os.getenv('BROWSERSTACK_USERNAME')
BROWSERSTACK_ACCESS_KEY = os.getenv('BROWSERSTACK_ACCESS_KEY')

app_path = os.getenv('APK_PATH_ANDROID')

def upload_app_for_live_testing():
    upload_url = 'https://api-cloud.browserstack.com/app-live/upload'

    if not os.path.exists(app_path):
        print(f"APK does not exists: {app_path}")
        return
    
    with open(app_path, 'rb') as app_file:
        files = {
            'file': (os.path.basename(app_path), app_file, 'application/octet-stream')
        }
        
        response = requests.post(
            upload_url,
            auth=(BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY),
            files=files
        )
    
    if response.status_code == 200:
        app_url = response.json().get('app_url')
        print(f'App uploaded for live testing: {app_url}')
        app_id = app_url.removeprefix('bs://')
        return app_id
    else:
        print(f'Error uploading app: {response.status_code}')
        print(f'Response: {response.text}')
        return None

def start_live_session(app_id, device, os_version):
    # Determine OS type based on the app or other logic
    # For now assuming Android since your original code was for Android
    os_type = "android"
    
    # URL encode device name 
    device_encoded = urllib.parse.quote_plus(device)
    
    # Construct the dynamic session URL
    session_url = (
        f"https://app-live.browserstack.com/dashboard"
        f"#os={os_type}"
        f"&os_version={os_version}"
        f"&device={device_encoded}"
        f"&app_hashed_id={app_id}"
        f"&scale_to_fit=true"
        f"&speed=1"
        f"&start=true"
    )
    
    print(f'Starting live session: {session_url}')
    webbrowser.open(session_url)
    
    print("\nLive session should now be open in your browser.")
    print("Note: You may need to log in to your BrowserStack account if not already logged in.")
    print("When you're done testing, close the browser tab to end the session.")

def get_available_devices():
    """Fetch available devices from BrowserStack API for reference"""
    devices_url = 'https://api-cloud.browserstack.com/app-live/devices.json'
    
    response = requests.get(
        devices_url,
        auth=(BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY)
    )
    
    if response.status_code == 200:
        devices = response.json()
        print("\nAvailable devices:")
        
        # Group by OS type
        for device in devices:
            if device.get('device') and device.get('os_version'):
                print(f"- {device.get('device')} ({device.get('os')} {device.get('os_version')})")
        
        return devices
    else:
        print(f'Error fetching devices: {response.status_code}')
        print(f'Response: {response.text}')
        return None

if __name__ == '__main__':
    # Upload app for live testing
    app_id = upload_app_for_live_testing()
    
    if app_id:
        # Optionally show available devices (uncomment to use)
        # get_available_devices()
        
        # Specify device and OS version 
        device = 'Google Pixel 5'
        os_version = '12.0'
        
        # Start a live session
        start_live_session(app_id, device, os_version)