import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.test_data import INVALID_MOBILE_INPUT


@pytest.mark.regression
@pytest.mark.login
def test_TC36_verify_login_page_or_modal_opens(page):
    # Arrange
    HomePage(page).open()
    login_page = LoginPage(page)

    # Act
    login_page.open_login()

    # Assert
    login_page.verify_login_page()


@pytest.mark.regression
@pytest.mark.login
def test_TC37_verify_login_mobile_number_field_is_displayed(page):
    # Arrange
    HomePage(page).open()
    login_page = LoginPage(page)
    login_page.open_login()

    # Act
    login_page.verify_login_page()

    # Assert
    login_page.verify_mobile_field()


@pytest.mark.regression
@pytest.mark.login
def test_TC38_verify_login_validation_for_invalid_input(page):
    # Arrange
    HomePage(page).open()
    login_page = LoginPage(page)
    login_page.open_login()
    login_page.verify_mobile_field()

    # Act
    login_page.enter_mobile_number(INVALID_MOBILE_INPUT)
    login_page.click_continue()

    # Assert
    login_page.verify_validation_message()
