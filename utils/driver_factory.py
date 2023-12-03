from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class DriverFactory:
    def __init__(self, browser):
        self.browser = browser

    def create_web_driver(self):
        if self.browser == "chrome":
            driver = webdriver.Chrome()
        elif self.browser == "safari":
            driver = webdriver.Safari()
        else:
            raise WebDriverException(f"we do not support {self.browser}...")
        return driver
