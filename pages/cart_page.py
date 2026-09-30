import re

from playwright.sync_api import Page, expect

from utils.logger import get_logger


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(__name__)

    def open_cart(self) -> None:
        self.logger.info("Opening cart")
        self.page.get_by_role("button", name=re.compile("Cart", re.IGNORECASE)).click()

    def verify_cart(self) -> None:
        cart_heading = self.page.get_by_role("heading", name=re.compile("cart|your bag", re.IGNORECASE))
        empty_state = self.page.get_by_text(re.compile("cart is empty|your cart is empty|empty cart", re.IGNORECASE))
        if cart_heading.count() and cart_heading.first.is_visible():
            expect(cart_heading.first).to_be_visible()
            return
        expect(empty_state.first).to_be_visible()

    def verify_product(self, product_name: str | None = None) -> bool:
        if product_name:
            product = self.page.get_by_text(re.compile(re.escape(product_name), re.IGNORECASE))
            return product.count() > 0 and product.first.is_visible()
        product_link = self.page.locator('a[href*="/pn/"]')
        return product_link.count() > 0 and product_link.first.is_visible()

    def increase_quantity(self) -> bool:
        button = self.page.get_by_role("button", name=re.compile(r"increase|increment|plus|\+", re.IGNORECASE))
        if not button.count():
            return False
        button.first.click()
        return True

    def decrease_quantity(self) -> bool:
        button = self.page.get_by_role("button", name=re.compile(r"decrease|decrement|minus|remove one|−|-", re.IGNORECASE))
        if not button.count():
            return False
        button.first.click()
        return True

    def remove_product(self) -> bool:
        remove = self.page.get_by_role("button", name=re.compile("remove|delete", re.IGNORECASE))
        if remove.count():
            remove.first.click()
            return True
        return self.decrease_quantity()

    def verify_empty_cart(self) -> None:
        empty_state = self.page.get_by_text(re.compile("cart is empty|your cart is empty|empty cart", re.IGNORECASE))
        expect(empty_state.first).to_be_visible()

    def get_cart_count(self) -> int:
        cart_button = self.page.get_by_test_id("cart-btn")
        if not cart_button.count():
            cart_button = self.page.get_by_role("button", name="Cart", exact=True)
        label = cart_button.get_attribute("aria-label") if cart_button.count() else ""
        text = cart_button.inner_text() if cart_button.count() else ""
        match = re.search(r"\d+", f"{label or ''} {text}")
        return int(match.group()) if match else 0

    def verify_checkout_button(self) -> bool:
        checkout = self.page.get_by_role("button", name=re.compile("checkout|proceed", re.IGNORECASE))
        return checkout.count() > 0 and checkout.first.is_visible()
