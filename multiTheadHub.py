import time
import os
import requests
import threading
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

API_KEY = os.environ["API_KEY"]
token = API_KEY

#use ocr python enviornment
class SimpleTests(threading.Thread):
    def __init__(self, argument, argument2):
        super(SimpleTests, self).__init__()
        self.argument = argument
        self.argument2 = argument2

    def run(self):
        device_id = self.argument
        host = self.argument2    
        driver_url = f"https://appium-dev.headspin.io:443/v0/{token}/wd/hub"
        options = AppiumOptions()
        options.load_capabilities({
        "automationName": "xcuitest",
        "platformName": "ios",
        "deviceName": "iPhone",
        "bundleId": "com.air-watch.agent",
        "udid": device_id
    })
        driver = webdriver.Remote(driver_url, options.to_capabilities())

        driver.implicitly_wait(20)

        session_id = driver.session_id

        try:
            acc_btn = driver.find_element(by=AppiumBy.IOS_CLASS_CHAIN, value="**/XCUIElementTypeButton[`name == \"navigation_account\"`]")
            acc_btn.click()
            print ("Clicked on Account Button " + device_id)
        except:
            print ("Account Button not found " + device_id)
            pass

        try:
            logout_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="device_remove-logout")
            logout_btn.click()
            print ("Logged out successfully " + device_id)
        except:
            driver.quit()
            print ("Failed to logout or user not logged in " + device_id)
        
        driver.terminate_app("com.air-watch.agent")

        print ("Done")

        driver.quit()


json_url = "https://api-dev.headspin.io/v0/devices/device_type:ios/information"

headers = {"Authorization": "Bearer " + token}
json_data = requests.get(json_url, headers=headers).json()

holder = json_data['devices'].copy()
for device_obj in holder:
    if device_obj["owner_email"] is not None:
        json_data['devices'].remove(device_obj)
        print("removing " + device_obj['device_id'])

if 'devices' in json_data:
    for device_obj in json_data['devices']:
        if 'hostname' in device_obj:
            hostname = device_obj['hostname']
        else:
            hostname = None

        if 'device_id' in device_obj:
            device_id = device_obj['device_id']
        else:
            device_id = None

        if 'safari' not in device_id and 'chrome' not in device_id and 'opera' not in device_id and 'firefox' not in device_id and 'edge' not in device_id:
            appiumThread = SimpleTests(device_id, hostname)
            appiumThread.start()
        
else:
    print("'devices' key not found in the JSON data.")


    