import time
import pytest

from pytest_bdd import scenario, given, when, then
from pages.loan_monthly import LoanMonthly


class TestLoanMonthly:
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
            "period": "36",
            "rate": "6",
            "fee": "0",
            "expected": ["第1~60月", "19,333", "6%", "1,000,000", "159,968", "1,159,968"],
        },
    )

    @scenario("./calculate_monthly.feature", "Calculate the mpnthly payment amount")
    def test_calculate_monthly_repayment_amount(self):
        pass

    @given("I want to apply for a loan (50w / 3year)")
    @pytest.mark.parametrize("data_set", data_set)
    def load_test_data(self, data_set):
        return data_set[1]

    @when("I go to the loan monthly calculate page")
    def loan_monthly_page(self, driver_class):
        loan_monthly = LoanMonthly(driver_class)
        return loan_monthly

    @when("I fill in all the info")
    def fill_in_info(self):
        self.loan_monthly.fill_in_all_input(data_set)

    # def test_calculate_monthly_repayment_amount(self, driver_class, data_set):
    #     loan_monthly.fill_in_all_input(data_set)
    #     time.sleep(1)
    #     loan_monthly.click_calculate_btn()
    #     time.sleep(1)
    #     result = loan_monthly.get_result_value()
    #     time.sleep(1)
    #     assert result == data_set["expected"]
