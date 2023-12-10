import pytest

from utils.driver_factory import DriverFactory


def pytest_addoption(parser):
    # TODO: add options: test env -> dev / staging / prod
    parser.addoption("--browser", default="chrome", help="set your web driver")
    parser.addoption("--device", default="destop", help="set your screen size")


@pytest.fixture(scope="function")
def driver_class(request):
    parm = request.config.getoption("--browser")
    screen_size = request.config.getoption("--device")
    web_driver = DriverFactory(parm).create_web_driver()
    url = "https://roo.cash/calculator/loan-monthly-payment"
    if screen_size == "desktop":
        web_driver.maximize_window()
    elif screen_size == "phone":
        web_driver.set_window_size(470, 830)
    web_driver.get(url)
    yield web_driver
    web_driver.quit()
