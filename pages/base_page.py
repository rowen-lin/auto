from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Page(object):
    def __init__(self, driver):
        self.driver = driver

    def get_element_by(self, by, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(by)
            )
        except (NoSuchElementException, TimeoutException):
            raise
        return element

    def get_elements_by(self, by, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(by)
            )
        except (NoSuchElementException, TimeoutException):
            raise
        return elements

    def wait_for_element_present(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except (NoSuchElementException, TimeoutException):
            return False
        return True

    def wait_for_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except (NoSuchElementException, TimeoutException):
            return False
        return True

    def scroll_into_view(self, locator):
        try:
            element = self.get_element_by(locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except (NoSuchElementException, TimeoutException):
            raise
        return element

    def get_current_url(self, timeout=10):
        try:
            current_url = self.driver.current_url
        except TimeoutException:
            raise
        return current_url

    def get_meta_title(self):
        try:
            meta_title = self.driver.title
        except TimeoutException:
            raise
        return meta_title
