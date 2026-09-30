import pytest

from pages.home_page import HomePage
from pages.location_page import LocationPage
from utils.test_data import INVALID_LOCATION_QUERY


@pytest.mark.regression
@pytest.mark.smoke
def test_TC11_verify_user_can_open_location_selector(page):
    # Arrange
    home_page = HomePage(page)
    location_page = LocationPage(page)
    home_page.open()

    # Act
    location_page.open_location_selector()

    # Assert
    assert location_page.dialog.is_visible()


@pytest.mark.regression
def test_TC12_verify_location_search_field_is_displayed(page):
    # Arrange
    home_page = HomePage(page)
    location_page = LocationPage(page)
    home_page.open()

    # Act
    location_page.open_location_selector()

    # Assert
    location_page.verify_location_input()


@pytest.mark.regression
def test_TC13_verify_location_selection_validation(page):
    # Arrange
    home_page = HomePage(page)
    location_page = LocationPage(page)
    home_page.open()
    location_page.open_location_selector()

    # Act
    location_page.enter_location(INVALID_LOCATION_QUERY)

    # Assert
    assert location_page.handle_location_validation()
    assert not location_page.select_location(INVALID_LOCATION_QUERY)
