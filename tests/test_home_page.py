import pytest
from urllib.parse import urlparse
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.regression
def test_TC01_verify_zepto_website_launches(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    expect(page.locator("body")).to_be_visible()
    assert page.url.startswith("https://www.zepto.com/")


@pytest.mark.smoke
@pytest.mark.regression
def test_TC02_verify_home_page_title(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    home_page.verify_title()


@pytest.mark.smoke
@pytest.mark.regression
def test_TC03_verify_zepto_logo_is_displayed(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    home_page.verify_logo()


@pytest.mark.smoke
@pytest.mark.regression
def test_TC04_verify_location_selector_is_displayed(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    home_page.verify_location_selector()


@pytest.mark.smoke
@pytest.mark.regression
def test_TC05_verify_search_box_is_displayed(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    home_page.verify_search_box()


@pytest.mark.smoke
@pytest.mark.regression
def test_TC06_verify_login_option_is_displayed(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    home_page.verify_login()


@pytest.mark.smoke
@pytest.mark.regression
def test_TC07_verify_cart_option_is_displayed(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    home_page.verify_cart()


@pytest.mark.smoke
@pytest.mark.regression
def test_TC08_verify_shop_by_category_section_is_displayed(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    home_page.verify_categories()


@pytest.mark.regression
def test_TC09_verify_fruits_and_vegetables_category_is_displayed(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    expect(page.get_by_role("link", name="Fruits & Vegetables Fruits & Vegetables")).to_be_visible()


@pytest.mark.regression
def test_TC10_verify_grocery_category_is_displayed(page):
    # Arrange
    home_page = HomePage(page)

    # Act
    home_page.open()

    # Assert
    expect(page.get_by_role("link", name="Dairy, Bread & Eggs Dairy, Bread & Eggs")).to_be_visible()


@pytest.mark.regression
def test_TC39_verify_page_refresh_and_navigation_behavior(page):
    # Arrange
    home_page = HomePage(page)
    home_page.open()

    # Act
    page.get_by_role("link", name="Search for products").click()
    assert urlparse(page.url).path == "/search"
    page.go_back()
    page.reload(wait_until="domcontentloaded")

    # Assert
    home_page.verify_logo()
    home_page.verify_search_box()
