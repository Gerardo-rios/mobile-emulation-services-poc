# Mobile Emulation Services POC

This repository contains proof of concept implementations for BrowserStack and Appetize.io mobile application emulation services.

## Prerequisites

- Python 3.x
- Valid BrowserStack account and credentials
- Valid Appetize.io account and API token
- Android APK file for testing

## Setup

1. Clone the repository:
```bash
git clone [git@github.com:Gerardo-rios/mobile-emulation-services-poc.git]
cd mobile-emulation-services-poc
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install requests
```

## BrowserStack Implementation

The BrowserStack POC includes two main features:
- Espresso test execution
- Live app testing

### Configuration

1. Navigate to the browserstack directory:
```bash
cd browserstack
```

2. Copy the `.env.template` to `.env`:
```bash
cp .env.template .env
```

3. Update the `.env` file with your credentials:
```
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
APK_PATH_ANDROID=/path/to/your/app.apk
TEST_APK_PATH_ANDROID=/path/to/your/test_app-AndroidTest.apk
```

### Running Tests

#### Espresso Tests
Execute the following command to run Espresso tests:
```bash
python espresso.py
```
This will:
1. Upload your app
2. Create a test suite
3. Execute tests on a Google Pixel 3 device with Android 9.0
4. Provide a dashboard URL to monitor the test execution

#### Live App Testing
To start a live testing session:
```bash
python app_live.py
```
This will:
1. Upload your app
2. Open a browser session with your app running on a Google Pixel 5 device with Android 12.0
3. Provide an interactive session for manual testing

## Appetize Implementation

### Configuration

1. Navigate to the appetize directory:
```bash
cd appetize
```

2. Copy the `.env.template` to `.env`:
```bash
cp .env.template .env
```

3. Update the `.env` file with your credentials:
```
APTIZE_TOKEN=your_token
APP_FILE=/path/to/your/app.apk
```

### Upload App

To upload your app to Appetize.io:
```bash
python app_upload.py
```

This will:
1. Upload your Android APK to Appetize.io
2. Return the upload response with the public key and other details

## Notes

- Make sure your APK files are properly signed and built for release
- Keep your credentials secure and never commit the `.env` files
- Both services provide web-based dashboards to monitor your tests and sessions
- The implementations use basic configurations; refer to the respective service documentation for advanced options

## Links

- [BrowserStack Documentation](https://www.browserstack.com/docs/)
- [Appetize.io Documentation](https://docs.appetize.io/)

