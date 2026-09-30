import re

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from utils.logger import get_logger


class ProductPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(__name__)

    def open_product(self) -> bool:
        if "/pn/" in self.page.url:
            return True
        product_link = self.page.locator('a[href*="/pn/"]').first
        if not product_link.count():
            return False
        self.logger.info("Opening product")
        product_link.click()
        return True

    def verify_product_image(self) -> None:
        image = self.page.locator("img[alt]").filter(has_not=self.page.locator("[aria-hidden='true']")).first
        expect(image).to_be_visible()

    def verify_product_name(self) -> None:
        heading = self.page.get_by_role("heading", level=1).first
        if heading.count():
            expect(heading).to_be_visible()
        else:
            image = self.page.locator("img[alt]").first
            expect(image).to_be_visible()
            assert image.get_attribute("alt"), "Product image should provide a product name"

    def verify_product_price(self) -> None:
        price = self.page.get_by_text(re.compile(r"₹\s*[\d,]+(?:\.\d{1,2})?"))
        expect(price.first).to_be_visible()

    def verify_product_rating(self) -> bool:
        rating = self.page.get_by_text(re.compile(r"\b[1-5]\.\d\b"))
        return rating.count() > 0 and rating.first.is_visible()

    @property
    def add_button(self):
        return self.page.get_by_role(
            "button",
            name=re.compile(r"^(ADD|Add|Add to cart|Increase quantity by one)$", re.IGNORECASE),
        )

    def verify_add_button(self) -> None:
        expect(self.add_button.first).to_be_visible()

    def add_to_cart(self) -> bool:
        self.logger.info("Adding product to cart")
        if not self.add_button.count():
            return False
        self.add_button.first.click()
        return True

    def add_first_available_product_to_cart(self) -> str | None:
        cards = self.page.locator('a[href*="/pn/"]')
        for index in range(cards.count()):
            card = cards.nth(index)
            image = card.locator("img[alt]").first
            product_name = image.get_attribute("alt") if image.count() else None
            if not product_name:
                continue
            if not self.open_product():
                return None
            self.logger.info("Adding available product to cart: %s", product_name)
            try:
                return product_name if self.add_to_cart() else None
            except PlaywrightTimeoutError:
                self.logger.warning("Zepto did not expose a safely clickable Add control for this product")
                return None
        return None

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
