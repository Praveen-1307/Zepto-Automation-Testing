import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.search_page import SearchPage
from utils.test_data import PRODUCT_NAME


def _open_product(page):
    HomePage(page).open()
    search_page = SearchPage(page)
    search_page.search_product(PRODUCT_NAME)
    if not search_page.product_cards.count():
        pytest.skip("No matching product is currently available in the public catalog")
    if not search_page.open_product():
        pytest.skip("The search result did not expose an openable product")
    return ProductPage(page)


@pytest.mark.regression
@pytest.mark.product
def test_TC23_verify_user_can_open_a_product(page):
    # Arrange
    HomePage(page).open()
    search_page = SearchPage(page)
    search_page.search_product(PRODUCT_NAME)
    if not search_page.product_cards.count():
        pytest.skip("No matching product is currently available")

    # Act
    opened = search_page.open_product()

    # Assert
    assert opened
    assert "/pn/" in page.url


@pytest.mark.regression
@pytest.mark.product
def test_TC24_verify_product_details_are_displayed(page):
    # Arrange
    product_page = _open_product(page)

    # Act
    product_page.verify_product_name()

    # Assert
    product_page.verify_product_price()


@pytest.mark.regression
@pytest.mark.product
def test_TC25_verify_add_button_is_displayed_for_available_product(page):
    # Arrange
    HomePage(page).open()
    search_page = SearchPage(page)
    search_page.search_product(PRODUCT_NAME)
    if not search_page.product_cards.count():
        pytest.skip("No matching product is currently available")

    # Act
    add_button = search_page.product_cards.first.get_by_role("button", name="ADD")

    # Assert
    expect(add_button).to_be_visible()
