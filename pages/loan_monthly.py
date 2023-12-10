from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

from pages.base_page import Page


class LoanMonthly(Page):
    AMOUNT_INPUT = (By.ID, "TxtloanAmount")
    PERIOD_INPUT = (By.ID, "TxtloanPeriod")
    # Rate 1 是單一利率
    RATE_ONE_INPUT = (By.ID, "TxtRate1")
    RATE_INFO_BTN = (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div/div[7]/div[1]")
    RATE_INFO_POPUP = (By.ID, "popup")
    FEE_INFO_BTN = (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div/div[8]/div[1]")
    FEE_INFO_POPUP = (By.ID, "popup2")

    def __init__(self, driver):
        super(LoanMonthly, self).__init__(driver)

    def get_url(self):
        return self.get_meta_title()

    def get_default_value(self):
        value = []
        amount = self.get_element_by(self.AMOUNT_INPUT).get_attribute("value")
        period = self.get_element_by(self.PERIOD_INPUT).get_attribute("value")
        rate = self.get_element_by(self.RATE_ONE_INPUT).get_attribute("value")
        value.append(amount)
        value.append(period)
        value.append(rate)
        return value

    def clear_amount_field(self):
        self.get_element_by(self.AMOUNT_INPUT).send_keys(Keys.DELETE)

    def set_value(self, value):
        self.get_element_by(self.AMOUNT_INPUT).send_keys(value)

    def get_value(self):
        amount = self.get_element_by(self.AMOUNT_INPUT).get_attribute("value")
        return amount

    def click_rate_info_button(self):
        rate_info_button = self.get_element_by(self.RATE_INFO_BTN)
        rate_info_button.click()

    def is_rate_popup_exist(self):
        return self.wait_for_visible(self.RATE_INFO_POPUP)

    def click_fee_info_button(self):
        fee_info_button = self.scroll_into_view(self.FEE_INFO_BTN)
        time.sleep(1)
        fee_info_button.click()

    def is_fee_popup_exist(self):
        return self.wait_for_visible(self.FEE_INFO_POPUP)
