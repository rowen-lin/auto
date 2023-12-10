from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
from pages.loan_monthly import LoanMonthly


class TestLoanMonthly:
    def test_url(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        meta_title = loan_monthly.get_meta_title()
        assert meta_title == "3 秒掌握最新銀行信用貸款利率試算分析 - 袋鼠金融 Roo.Cash"

    def test_default_value(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        # 貸款金額：30, 貸款期間：60, 單一利率：2.92
        expected = ["30", "60", "2.92"]
        default_value = loan_monthly.get_default_value()
        assert default_value == expected

    def test_amount_max(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        loan_monthly.clear_amount_field()
        loan_monthly.set_value(501)
        time.sleep(1)
        value = loan_monthly.get_value()
        assert value == "500"

    def test_click_rate_info_popup(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        loan_monthly.click_rate_info_button()
        time.sleep(1)
        assert loan_monthly.is_rate_popup_exist()

    def test_click_fee_info_popup(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        loan_monthly.click_fee_info_button()
        time.sleep(1)
        assert loan_monthly.is_fee_popup_exist()

    def test_set_range(self, driver_class):
        # 在這裡進行測試
        # 假設網頁上有一個滑塊元素的 ID 為 "slider"
        slider = driver_class.get_element_by(By.ID, "TxtloanAmountSlidebar")

        # 獲取初始值
        # initial_value = float(slider.get_attribute("value"))

        # 設定滑塊的目標值，比如從 30 調整到 100
        target_value = 500

        # 計算值的差異，然後調整滑塊
        self.set_range(driver_class, slider, target_value)

        time.sleep(3)

        # 驗證滑塊的值是否正確
        assert int(slider.get_attribute("value")) == target_value

    def set_range(self, driver_class, el, val):
        # The adjustment helper to drag the slider thumb
        def adjust(deltax):
            if deltax < 0:
                deltax = int(math.floor(min(-1, deltax)))
            else:
                deltax = int(math.ceil(max(1, deltax)))
            ac = ActionChains(driver_class)
            ac.click_and_hold(None)
            ac.move_by_offset(deltax, 0)
            ac.release(None)
            ac.perform()

        minval = float(el.get_attribute("min") or 0)
        maxval = float(el.get_attribute("max") or 100)
        v = max(0, min(1, (float(val) - minval) / (maxval - minval)))
        width = el.size["width"]
        target = float(width) * v

        ac = ActionChains(driver_class)

        # drag from min to max value, to ensure oninput event
        ac.move_to_element_with_offset(el, 0, 1)
        ac.click_and_hold()
        ac.move_by_offset(width, 0)

        # drag to the calculated position
        target = min(max(target, 0), width - 1)
        ac.move_to_element_with_offset(el, target, 1)

        ac.release()
        ac.perform()

        minguess = 0  # Initialize minguess
        maxguess = width  # Initialize maxguess
        # perform a binary search and adjust the slider thumb until the value matches
        while True:
            curval = el.get_attribute("value")
            if float(curval) == float(val):
                return True
            prev_guess = target

            if float(curval) < float(val):
                minguess = target
                target += (maxguess - target) / 2

            else:
                maxguess = target
                target = minguess + (target - minguess) / 2
            deltax = target - prev_guess
            if abs(deltax) < 0.5:
                break  # cannot find a way, fallback to javascript.

            time.sleep(0.1)  # Don't consume CPU too much

            adjust(deltax)

        # Finally, if the binary search algoritm fails to achieve the final value
        # we'll revert to the javascript method so at least the value will be changed
        # even though the browser events wont' be triggered.

        # Fallback
        driver_class.execute_script("arguments[0].value=arguments[1];", el, val)
        curval = el.get_attribute("value")
        if float(curval) == float(val):
            return True
        else:
            raise Exception("Can't set value %f for the element." % val)
