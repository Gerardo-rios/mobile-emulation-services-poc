import requests
import os
import base64

API_URL = 'https://api.appetize.io/v1/apps'
API_KEY = os.getenv('APTIZE_TOKEN')
APP_PATH = os.getenv('APP_FILE')

def _authorization_header():
    auth_str = API_KEY + ':'
    encoded_bytes = base64.b64encode(auth_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return {
        'Authorization': f'Basic {encoded_str}'
    }

def upload_app():   
    files = {
        'file': (os.path.basename(APP_PATH), open(APP_PATH, 'rb'))
    }
    
    data = {
        'platform': 'android',
        'fileType': 'apk',
    }
    
    response = requests.post(API_URL, headers=_authorization_header(), data=data, files=files)
    return response.json()

def update_app(app_public_key):
    url = f'{API_URL}/{app_public_key}'

    files = {
        'file': (os.path.basename(APP_PATH), open(APP_PATH, 'rb'))
    }

    data = {
        'platform': 'android',
        'fileType': 'apk',
    }
    
    response = requests.post(url, headers=_authorization_header(), data=data, files=files)
    return response.json()



if __name__ == '__main__':
    print(upload_app())
