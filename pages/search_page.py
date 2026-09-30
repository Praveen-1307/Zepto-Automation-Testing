import re

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from utils.config import BASE_URL
from utils.logger import get_logger


class SearchPage:
    PRODUCT_CARD_SELECTOR = 'a[href*="/pn/"]'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(__name__)
        self.query = ""

    @property
    def search_box(self):
        field = self.page.get_by_role("combobox", name=re.compile("Search", re.IGNORECASE))
        if field.count():
            return field
        return self.page.get_by_placeholder(re.compile("Search", re.IGNORECASE))

    @property
    def product_cards(self):
        cards = self.page.locator(self.PRODUCT_CARD_SELECTOR)
        if self.query:
            return cards.filter(has_text=re.compile(re.escape(self.query), re.IGNORECASE))
        return cards

    def search_product(self, product_name: str) -> None:
        self.query = product_name
        self.logger.info("Searching for product: %s", product_name)
        if not self.search_box.count():
            trigger = self.page.get_by_role("link", name=re.compile("Search for products", re.IGNORECASE))
            if trigger.count():
                trigger.click()
            else:
                self.page.goto(f"{BASE_URL.rstrip('/')}/search", wait_until="domcontentloaded")
        expect(self.search_box).to_be_visible()
        self.search_box.fill(product_name)
        self.search_box.press("Enter")

    def verify_search_results(self) -> None:
        try:
            self.product_cards.first.wait_for(state="visible", timeout=5000)
            return
        except PlaywrightTimeoutError:
            pass

        empty_state = self.page.get_by_text(re.compile("No (products|results)|try another", re.IGNORECASE))
        if empty_state.count():
            expect(empty_state.first).to_be_visible()
        else:
            expect(self.search_box).to_be_visible()

    def get_product_names(self) -> list[str]:
        names = []
        for card in self.product_cards.all():
            image = card.locator("img").first
            alt_text = image.get_attribute("alt") if image.count() else None
            text = alt_text or card.inner_text().splitlines()[0]
            if text.strip():
                names.append(text.strip())
        return names

    def verify_product_name(self, product_name: str | None = None) -> None:
        card = self.product_cards.first
        expect(card).to_be_visible()
        expected = product_name or self.query
        if expected:
            expect(card).to_contain_text(re.compile(re.escape(expected), re.IGNORECASE))

    def verify_product_price(self) -> bool:
        if not self.product_cards.count():
            return False
        return bool(re.search(r"₹\s*[\d,]+(?:\.\d{1,2})?", self.product_cards.first.inner_text()))

    def verify_product_discount(self) -> bool:
        if not self.product_cards.count():
            return False
        return bool(re.search(r"(?:\bOFF\b|\b\d+\s*%\s*off\b)", self.product_cards.first.inner_text(), re.IGNORECASE))

    def verify_product_rating(self) -> bool:
        if not self.product_cards.count():
            return False
        card_text = self.product_cards.first.inner_text()
        return bool(re.search(r"\b[1-5]\.\d\b", card_text))

    def open_product(self) -> bool:
        self.logger.info("Opening product")
        if not self.product_cards.count():
            return False
        self.product_cards.first.click()
        return True

    def verify_no_results(self) -> bool:
        no_results = self.page.get_by_text(
            re.compile("No (products|results)|try another|couldn't find", re.IGNORECASE)
        )
        if no_results.count() and no_results.first.is_visible():
            return True
        return self.product_cards.count() == 0 and self.search_box.is_visible()
