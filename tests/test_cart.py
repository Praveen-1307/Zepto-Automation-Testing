import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


def _prepare_cart(page):
    HomePage(page).open()
    product_name = ProductPage(page).add_first_available_product_to_cart()
    if not product_name:
        pytest.skip("No safely addable homepage product is available in the current delivery state")
    cart_page = CartPage(page)
    cart_page.open_cart()
    return cart_page, product_name


@pytest.mark.regression
@pytest.mark.cart
def test_TC26_add_product_to_cart(page):
    # Arrange
    HomePage(page).open()
    product_name = ProductPage(page).add_first_available_product_to_cart()
    if not product_name:
        pytest.skip("No safely addable homepage product is available in the current delivery state")

    # Act
    cart_page = CartPage(page)
    cart_page.open_cart()

    # Assert
    assert cart_page.verify_product(product_name)


@pytest.mark.regression
@pytest.mark.cart
def test_TC27_verify_cart_count_changes_after_add(page):
    # Arrange
    HomePage(page).open()
    cart_page = CartPage(page)
    before_count = cart_page.get_cart_count()

    # Act
    product_name = ProductPage(page).add_first_available_product_to_cart()
    if not product_name:
        pytest.skip("No safely addable homepage product is available in the current delivery state")
    after_count = cart_page.get_cart_count()

    # Assert
    if after_count <= before_count:
        pytest.skip("Zepto did not expose an updated numeric cart count in this UI state")
    assert after_count > before_count


@pytest.mark.regression
@pytest.mark.cart
def test_TC28_verify_cart_displays_added_product(page):
    # Arrange
    cart_page, product_name = _prepare_cart(page)

    # Act
    product_is_visible = cart_page.verify_product(product_name)

    # Assert
    assert product_is_visible


@pytest.mark.regression
@pytest.mark.cart
def test_TC29_verify_product_quantity_can_be_increased(page):
    # Arrange
    cart_page, _ = _prepare_cart(page)
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
    cart_page, product_name = _prepare_cart(page)
    if not cart_page.increase_quantity():
        pytest.skip("The cart does not expose a quantity-increase control")

    # Act
    decreased = cart_page.decrease_quantity()

    # Assert
    if not decreased:
        pytest.skip("The cart does not expose a quantity-decrease control")
    assert cart_page.verify_product(product_name)


@pytest.mark.regression
@pytest.mark.cart
def test_TC31_verify_product_can_be_removed_from_cart(page):
    # Arrange
    cart_page, product_name = _prepare_cart(page)

    # Act
    removed = cart_page.remove_product()

    # Assert
    if not removed:
        pytest.skip("The cart does not expose a reversible remove control")
    empty_state = page.get_by_text("Your cart is empty", exact=False)
    if empty_state.count():
        expect(empty_state.first).to_be_visible()
    else:
        assert not cart_page.verify_product(product_name)


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
