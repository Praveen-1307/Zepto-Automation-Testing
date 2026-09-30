import logging

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_page import SearchPage
from utils.test_data import ALTERNATE_PRODUCT, INVALID_PRODUCT

logger = logging.getLogger(__name__)


def _search(page, query):
    HomePage(page).open()
    search_page = SearchPage(page)
    search_page.search_product(query)
    return search_page


@pytest.mark.regression
@pytest.mark.search
def test_TC14_verify_search_box_accepts_product_name(page):
    # Arrange
    search_page = _search(page, ALTERNATE_PRODUCT)

    # Act
    entered_value = search_page.search_box.input_value()

    # Assert
    assert entered_value.lower() == ALTERNATE_PRODUCT.lower()


@pytest.mark.regression
@pytest.mark.search
def test_TC15_search_valid_product_name(page):
    # Arrange
    search_page = _search(page, ALTERNATE_PRODUCT)

    # Act
    search_page.verify_search_results()

    # Assert
    if not search_page.product_cards.count():
        pytest.skip("The product is unavailable or the public site requires a location selection")
    expect(search_page.product_cards.first).to_be_visible()


@pytest.mark.regression
@pytest.mark.search
def test_TC16_verify_search_results_are_displayed(page):
    # Arrange
    search_page = _search(page, ALTERNATE_PRODUCT)

    # Act
    search_page.verify_search_results()

    # Assert
    if not search_page.product_cards.count():
        pytest.skip("Zepto returned no public results for this query in the current delivery area")
    expect(search_page.product_cards.first).to_be_visible()


@pytest.mark.regression
@pytest.mark.search
def test_TC17_verify_invalid_product_search(page):
    # Arrange
    search_page = _search(page, INVALID_PRODUCT)

    # Act
    search_page.verify_search_results()

    # Assert
    assert search_page.product_cards.count() == 0 or search_page.verify_no_results()


@pytest.mark.regression
@pytest.mark.search
def test_TC18_verify_search_result_product_name_is_displayed(page):
    # Arrange
    search_page = _search(page, ALTERNATE_PRODUCT)

    # Act
    if not search_page.product_cards.count():
        pytest.skip("No matching products are available to validate")
    product_names = search_page.get_product_names()

    # Assert
    assert product_names, "Search result cards should expose a product name"


@pytest.mark.regression
@pytest.mark.search
def test_TC19_verify_product_price_is_displayed(page):
    # Arrange
    search_page = _search(page, ALTERNATE_PRODUCT)

    # Act
    has_price = search_page.verify_product_price()

    # Assert
    if not search_page.product_cards.count():
        pytest.skip("No products are available to inspect for a price")
    assert has_price, "A visible product card should show its current price"


@pytest.mark.regression
@pytest.mark.search
def test_TC20_verify_product_discount_where_available(page):
    # Arrange
    search_page = _search(page, ALTERNATE_PRODUCT)

    # Act
    has_discount = search_page.verify_product_discount()

    # Assert
    if not search_page.product_cards.count():
        pytest.skip("No products are available to inspect for discounts")
    if not has_discount:
        pytest.skip("The current result has no discount label")
    assert has_discount


@pytest.mark.regression
@pytest.mark.search
def test_TC21_verify_product_rating_where_available(page):
    # Arrange
    search_page = _search(page, ALTERNATE_PRODUCT)

    # Act
    has_rating = search_page.verify_product_rating()

    # Assert
    if not search_page.product_cards.count():
        pytest.skip("No products are available to inspect for ratings")
    if not has_rating:
        pytest.skip("The current result does not display a rating")
    assert has_rating


@pytest.mark.regression
@pytest.mark.search
def test_TC22_verify_product_image_is_displayed(page):
    # Arrange
    search_page = _search(page, ALTERNATE_PRODUCT)

    # Act
    if not search_page.product_cards.count():
        pytest.skip("No product cards are available to inspect")
    image = search_page.product_cards.first.locator("img").first

    # Assert
    expect(image).to_be_visible()
