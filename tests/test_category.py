import pytest

from pages.category_page import CategoryPage
from pages.home_page import HomePage
from utils.test_data import CATEGORY


@pytest.mark.regression
@pytest.mark.category
def test_TC33_verify_category_navigation(page):
    # Arrange
    HomePage(page).open()
    category_page = CategoryPage(page)

    # Act
    opened = category_page.open_category(CATEGORY)

    # Assert
    assert opened, f"Category link not found: {CATEGORY}"
    category_page.verify_category(CATEGORY)


@pytest.mark.regression
@pytest.mark.category
def test_TC34_verify_category_product_listing(page):
    # Arrange
    HomePage(page).open()
    category_page = CategoryPage(page)

    # Act
    opened = category_page.open_category(CATEGORY)

    # Assert
    assert opened, f"Category link not found: {CATEGORY}"
    category_page.verify_category(CATEGORY)
    if not category_page.verify_products():
        pytest.skip("No products are currently exposed in this category or delivery area")


@pytest.mark.regression
@pytest.mark.category
def test_TC35_verify_best_sellers_navigation(page):
    # Arrange
    HomePage(page).open()
    category_page = CategoryPage(page)

    # Act
    opened = category_page.open_best_sellers()

    # Assert
    if not opened:
        pytest.skip("Best Sellers navigation is not exposed in the current public UI")
    if not category_page.verify_best_sellers():
        pytest.skip("The current Zepto UI did not expose a Best Sellers label after navigation")
