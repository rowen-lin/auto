import pytest

from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Constants

DUCKDUCKGO_HOME = "https://duckduckgo.com/"

# Scenarios

scenarios("./web.feature")

# Fixtures


@pytest.fixture
def browser():
    b = webdriver.Chrome()
    b.implicitly_wait(10)
    yield b
    b.quit()


# Given Steps


@given("the DuckDuckGo home page is displayed")
def ddg_home(browser):
    browser.get(DUCKDUCKGO_HOME)


# When Steps


@when(parsers.parse('the user searches for "{phrase}"'))
def search_phrase(browser, phrase):
    search_input = browser.find_element(By.ID, "search_form_input_homepage")
    search_input.send_keys(phrase + Keys.RETURN)


# Then Steps


@then(parsers.parse('results are shown for "{phrase}"'))
def search_results(browser, phrase):
    # Check search result list
    # (A more comprehensive test would check results for matching phrases)
    # (Check the list before the search phrase for correct implicit waiting)
    links_div = browser.find_element(By.ID, "links")
    assert len(links_div.find_elements(By.XPATH, "//div")) > 0
    # Check search phrase
    search_input = browser.find_element(By.ID, "search_form_input")
    assert search_input.get_attribute("value") == phrase
