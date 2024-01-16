import time
import pytest

from pages.loan_monthly import LoanMonthly
from utils import csv_tool


class TestLoanMonthly:
    # 確認 信貸月付金試算 URL Title
    def test_url(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        meta_title = loan_monthly.get_meta_title()
        assert meta_title == "3 秒掌握最新銀行信用貸款利率試算分析 - 袋鼠金融 Roo.Cash"

    # 確認 試算輸入欄位預設值
    def test_default_value(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        # 預設值：貸款金額：30, 貸款期間：60, 單一利率：2.92
        expected = ["30", "60", "2.92"]
        default_value = loan_monthly.get_default_value()
        assert default_value == expected

    # 確認 貸款金額輸入最大值
    def test_amount_max(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        loan_monthly.clear_amount_field()
        loan_monthly.set_value(501)
        value = loan_monthly.get_value()
        assert value == "500"

    # 確認 單一利率 popup
    def test_click_rate_info_popup(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        loan_monthly.click_rate_info_button()
        assert loan_monthly.is_rate_popup_exist()

    # 確認 會有哪些相關費用 popup
    def test_click_fee_info_popup(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        loan_monthly.click_fee_info_button()
        assert loan_monthly.is_fee_popup_exist()

    # 測資：貸款金額、貸款期間、單一利率、相關費用、預期結果 預期結果：[貸款區間、每月還款金額、APR、本金、利息、本息]
    # TODO: 轉換成 csv 檔
    data_set = (
        {
            "amount": "100",
            "period": "60",
            "rate": "6",
            "fee": "0",
            "expected": ["第1~60月", "19,333", "6%", "1,000,000", "159,968", "1,159,968"],
        },
        {
            "amount": "50",
            "period": "60",
            "rate": "6",
            "fee": "0",
            "expected": ["第1~60月", "9,666", "6%", "500,000", "79,989", "579,989"],
        },
    )

    # 確認 貸款利率試算結果
    @pytest.mark.parametrize(
        "rate_data_set", csv_tool.read_data_from_csv("rate_data_set")
    )
    def test_calculate_monthly_repayment_amount(self, driver_class, rate_data_set):
        data = {
            "amount": "100",
            "period": "60",
            "fee": "0",
            "expected": ["第1~60月", "19,333", "6%", "1,000,000", "159,968", "1,159,968"],
        }
        loan_monthly = LoanMonthly(driver_class)

        loan_monthly.fill_in_all_input(data, rate_data_set)
        time.sleep(1)
        loan_monthly.click_calculate_btn()
        time.sleep(1)
        result = loan_monthly.get_result_value()
        time.sleep(1)
        assert result == data["expected"]

    # 確認 寄送 email
    def test_send_full_calculation_results_via_email(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
