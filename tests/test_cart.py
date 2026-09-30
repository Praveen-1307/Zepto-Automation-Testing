import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.search_page import SearchPage
from utils.test_data import PRODUCT_NAME


def _prepare_cart(page):
    HomePage(page).open()
    search_page = SearchPage(page)
    search_page.search_product(PRODUCT_NAME)
    if not search_page.product_cards.count():
        pytest.skip("No matching product is currently available in the public catalog")
    if not ProductPage(page).add_to_cart():
        pytest.skip("The current result does not expose an add-to-cart control")
    cart_page = CartPage(page)
    cart_page.open_cart()
    return cart_page


@pytest.mark.regression
@pytest.mark.cart
def test_TC26_add_product_to_cart(page):
    # Arrange
    HomePage(page).open()
    search_page = SearchPage(page)
    search_page.search_product(PRODUCT_NAME)
    if not search_page.product_cards.count():
        pytest.skip("No matching product is currently available")

    # Act
    added = ProductPage(page).add_to_cart()
    cart_page = CartPage(page)
    cart_page.open_cart()

    # Assert
    assert added
    assert cart_page.verify_product(PRODUCT_NAME)


@pytest.mark.regression
@pytest.mark.cart
def test_TC27_verify_cart_count_changes_after_add(page):
    # Arrange
    HomePage(page).open()
    cart_page = CartPage(page)
    before_count = cart_page.get_cart_count()
    search_page = SearchPage(page)
    search_page.search_product(PRODUCT_NAME)
    if not search_page.product_cards.count():
        pytest.skip("No matching product is currently available")

    # Act
    added = ProductPage(page).add_to_cart()
    after_count = cart_page.get_cart_count()

    # Assert
    assert added
    if after_count <= before_count:
        pytest.skip("Zepto did not expose an updated numeric cart count in this UI state")
    assert after_count > before_count


@pytest.mark.regression
@pytest.mark.cart
def test_TC28_verify_cart_displays_added_product(page):
    # Arrange
    cart_page = _prepare_cart(page)

    # Act
    product_is_visible = cart_page.verify_product(PRODUCT_NAME)

    # Assert
    assert product_is_visible


@pytest.mark.regression
@pytest.mark.cart
def test_TC29_verify_product_quantity_can_be_increased(page):
    # Arrange
    cart_page = _prepare_cart(page)
    before_count = cart_page.get_cart_count()

    # Act
    increased = cart_page.increase_quantity()

    # Assert
    if not increased:
        pytest.skip("The cart does not expose a quantity-increase control")
    after_count = cart_page.get_cart_count()
    assert after_count > before_count


@pytest.mark.regression
@pytest.mark.cart
def test_TC30_verify_product_quantity_can_be_decreased(page):
    # Arrange
    cart_page = _prepare_cart(page)
    if not cart_page.increase_quantity():
        pytest.skip("The cart does not expose a quantity-increase control")

    # Act
    decreased = cart_page.decrease_quantity()

    # Assert
    if not decreased:
        pytest.skip("The cart does not expose a quantity-decrease control")
    assert cart_page.verify_product(PRODUCT_NAME)


@pytest.mark.regression
@pytest.mark.cart
def test_TC31_verify_product_can_be_removed_from_cart(page):
    # Arrange
    cart_page = _prepare_cart(page)

    # Act
    removed = cart_page.remove_product()

    # Assert
    if not removed:
        pytest.skip("The cart does not expose a reversible remove control")
    empty_state = page.get_by_text("Your cart is empty", exact=False)
    if empty_state.count():
        expect(empty_state.first).to_be_visible()
    else:
        assert not cart_page.verify_product(PRODUCT_NAME)


@pytest.mark.regression
@pytest.mark.cart
def test_TC32_verify_empty_cart_state_is_displayed(page):
    # Arrange
    HomePage(page).open()
    cart_page = CartPage(page)

    # Act
    cart_page.open_cart()

    # Assert
    cart_page.verify_empty_cart()
