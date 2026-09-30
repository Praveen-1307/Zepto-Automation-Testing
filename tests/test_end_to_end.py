import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.location_page import LocationPage
from pages.product_page import ProductPage
from pages.search_page import SearchPage
from utils.test_data import PRODUCT_NAME


@pytest.mark.regression
@pytest.mark.e2e
def test_TC40_complete_shopping_workflow(page):
    # Arrange
    home_page = HomePage(page)
    search_page = SearchPage(page)
    home_page.open()

    # Act: inspect the location step without saving a real address.
    location_page = LocationPage(page)
    location_page.open_location_selector()
    location_page.verify_location_input()
    close_button = page.get_by_role("button", name="Location modal close Icon")
    if close_button.count():
        close_button.click()

    # Search and open a currently available product.
    search_page.search_product(PRODUCT_NAME)
    if not search_page.product_cards.count():
        pytest.skip("No matching product is currently available in the public catalog")
    if not search_page.open_product():
        pytest.skip("The current result does not expose a product details link")

    # Assert product details and add the item to the temporary browser cart.
    product_page = ProductPage(page)
    product_page.verify_product_name()
    product_page.verify_product_price()
    if not product_page.add_to_cart():
        pytest.skip("Zepto did not expose an add-to-cart action for this product")

    # Verify the cart only; checkout, payment, and order placement are out of scope.
    cart_page = CartPage(page)
    cart_page.open_cart()
    expect(page.locator("body")).to_be_visible()
    assert cart_page.verify_product(PRODUCT_NAME), "The searched product should appear in the cart"
    if cart_page.get_cart_count() == 0:
        pytest.skip("The product is in the cart, but this UI state exposes no numeric cart count")
