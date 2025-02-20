from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

import shutil
import os


def get_available_driver():
    # Chrome
    if shutil.which("chromedriver"):
        print("ChromeDriver detected: Now using ChromeDriver")
        
        # Chrome options as provided
        service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        options.add_argument("--log-level=3")
        options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns,WebRTC-ICE")
        options.add_argument("--disable-usb-keyboard-detect")
        options.add_argument("--disable-usb-discovery")
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        driver = webdriver.Chrome(service=service, options=options)
    
    # Firefox
    elif shutil.which("geckodriver"):
        print("GeckoDriver detected: Now using FireFox.")
        
        # Firefox options as provided
        service = FirefoxService(GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        driver = webdriver.Firefox(service=service, options=options)
    
    # If neither is found, raise an error
    else:
        raise Exception("No compatible web driver found. Install ChromeDriver or GeckoDriver.")

    return driver


