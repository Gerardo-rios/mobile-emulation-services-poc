import os
import requests
from requests.auth import HTTPBasicAuth

BROWSERSTACK_USERNAME = os.getenv('BROWSERSTACK_USERNAME')
BROWSERSTACK_ACCESS_KEY = os.getenv('BROWSERSTACK_ACCESS_KEY')

app_path = os.getenv('APK_PATH_ANDROID')
test_path = os.getenv('TEST_APK_PATH_ANDROID')

def upload_app():
    upload_url = 'https://api-cloud.browserstack.com/app-automate/espresso/v2/app'

    if not os.path.exists(app_path):
        print(f"APK does not exists: {app_path}")
        return
    
    with open(app_path, 'rb') as app_file:
        files = {
            'file': (os.path.basename(app_path), app_file, 'application/octet-stream')
        }
        
        data = {
            'custom_id': 'SampleAppAndroid'
        }
        
        response = requests.post(
            upload_url,
            auth=(BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY),
            files=files,
            data=data
        )
    
    if response.status_code == 200:
        app_url = response.json().get('app_url')
        print(f'App uploaded here: {app_url}')
        return app_url
    else:
        print(f'Error uploading app: {response.status_code}')
        print(f'Response: {response.text}')
        return None

def create_test_suite():
    create_test_suite_url = 'https://api-cloud.browserstack.com/app-automate/espresso/v2/test-suite'
    
    with open(test_path, 'rb') as app_file:
        files = {
            'file': (os.path.basename(test_path), app_file, 'application/octet-stream')
        }
        
        response = requests.post(
            create_test_suite_url,
            auth=(BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY),
            files=files,
        )

    if response.status_code == 200:
        test_suite_url = response.json().get('test_suite_url')
        print(f'Test suite created successfully. Test Suite URL: {test_suite_url}')
        return test_suite_url
    else:
        print(f'Error creating test suite: {response.status_code}')
        print(f'Response: {response.text}')
        return None


def create_build(app_url, test_suite_url, device, os_version):
    build_endpoint_url = 'https://api-cloud.browserstack.com/app-automate/espresso/v2/build'
    
    payload = {
        'app': app_url,
        'testSuite': test_suite_url,
        'deviceLogs': 'true',
        'devices': [f'{device}-{os_version}']
    }
    
    response = requests.post(
        build_endpoint_url,
        auth=(BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY),
        json=payload
    )
    
    if response.status_code == 200:
        build_id = response.json().get('build_id')
        print(f'Session successfully created. Build ID: {build_id}')
        return build_id
    else:
        print(f'Error while creating session: {response.status_code}')
        print(f'Response: {response.text}')
        return None

if __name__ == '__main__':
    app_url = upload_app()
    test_suite_url = create_test_suite()
    if app_url and test_suite_url:
        build_id = create_build(app_url, test_suite_url, 'Google Pixel 3', '9.0')
        
        if build_id:
            print(f'Dashboard URL: https://app-automate.browserstack.com/dashboard/v2/builds/{build_id}')