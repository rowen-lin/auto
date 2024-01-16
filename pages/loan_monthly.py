from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

from pages.base_page import Page


class LoanMonthly(Page):
    AMOUNT_INPUT = (By.ID, "TxtloanAmount")
    PERIOD_INPUT = (By.ID, "TxtloanPeriod")
    # Rate 1 是單一利率
    RATE_ONE_INPUT = (By.ID, "TxtRate1")
    FEE_INPUT = (By.ID, "TxtFee")
    RATE_INFO_BTN = (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div/div[7]/div[1]")
    RATE_INFO_POPUP = (By.ID, "popup")
    FEE_INFO_BTN = (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div/div[8]/div[1]")
    FEE_INFO_POPUP = (By.ID, "popup2")
    CALCULATE_BTN = (By.ID, "LbtnCalculate")
    # 試算結果：貸款期間
    RESULT_PERIOD = (By.CLASS_NAME, "resultWording")
    # 試算結果：每月還款金額
    RESULT_PAYMENT = (
        By.XPATH,
        "/html/body/div[2]/div[3]/div[3]/div[2]/div/div[1]/div/div[1]/p[2]/span[1]",
    )
    # 試算結果：APR
    RESULT_APR = (By.ID, "yearRate")
    # 試算結果：本金
    RESULT_AMOUNT = (By.CLASS_NAME, "totalPayPrincipal")
    # 試算結果：利息
    RESULT_INTEREST = (By.CLASS_NAME, "totalPayInterest")
    # 試算結果：本息
    RESULT_TOTAL_AMOUNT = (By.CLASS_NAME, "totalPayPrincipalAndInterest")

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

    def fill_in_all_input(self, data, rate_data_set):
        # 輸入 貸款金額，必須先預設值清掉
        self.get_element_by(self.AMOUNT_INPUT).clear()
        self.get_element_by(self.AMOUNT_INPUT).send_keys(data["amount"])
        # 輸入 貸款期間，必須先預設值清掉
        self.get_element_by(self.PERIOD_INPUT).clear()
        self.get_element_by(self.PERIOD_INPUT).send_keys(data["period"])
        # 輸入 利率，必須先預設值清掉
        self.get_element_by(self.RATE_ONE_INPUT).clear()
        self.get_element_by(self.RATE_ONE_INPUT).send_keys(rate_data_set)
        # 輸入 相關費用，必須先預設值清掉
        self.get_element_by(self.FEE_INPUT).clear()
        self.get_element_by(self.FEE_INPUT).send_keys(data["fee"])

    def click_calculate_btn(self):
        calculate_button = self.scroll_into_view(self.CALCULATE_BTN)
        time.sleep(1)
        calculate_button.click()

    def get_result_value(self):
        value = []
        value.append(self.get_element_by(self.RESULT_PERIOD).text)
        value.append(self.get_element_by(self.RESULT_PAYMENT).text)
        value.append(self.get_element_by(self.RESULT_APR).text)
        value.append(self.get_element_by(self.RESULT_AMOUNT).text)
        value.append(self.get_element_by(self.RESULT_INTEREST).text)
        value.append(self.get_element_by(self.RESULT_TOTAL_AMOUNT).text)
        return value
