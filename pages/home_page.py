import re

from playwright.sync_api import Page, expect

from utils.config import BASE_URL
from utils.logger import get_logger


class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(__name__)

    def open(self) -> None:
        self.logger.info("Opening Zepto website")
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        expect(self.page.locator("body")).to_be_visible()

    def verify_title(self) -> None:
        expect(self.page).to_have_title(re.compile("Zepto", re.IGNORECASE))

    def verify_logo(self) -> None:
        expect(self.page.get_by_role("link", name=re.compile("Zepto Home", re.IGNORECASE))).to_be_visible()

    def verify_location_selector(self) -> None:
        expect(self.page.get_by_role("button", name=re.compile("Select Location", re.IGNORECASE))).to_be_visible()

    def verify_search_box(self) -> None:
        search_link = self.page.get_by_role("link", name=re.compile("Search for products", re.IGNORECASE))
        search_input = self.page.get_by_role("combobox", name=re.compile("Search", re.IGNORECASE))
        expect(search_link if search_link.count() else search_input).to_be_visible()

    def verify_login(self) -> None:
        expect(self.page.get_by_role("button", name=re.compile("login", re.IGNORECASE))).to_be_visible()

    def verify_cart(self) -> None:
        expect(self.page.get_by_role("button", name=re.compile("Cart", re.IGNORECASE))).to_be_visible()

    def verify_categories(self) -> None:
        expect(self.page.get_by_role("heading", name=re.compile("Shop by Category", re.IGNORECASE))).to_be_visible()

    def open_login(self) -> None:
        self.logger.info("Opening login UI")
        self.page.get_by_role("button", name=re.compile("login", re.IGNORECASE)).click()

    def open_cart(self) -> None:
        self.logger.info("Opening cart")
        self.page.get_by_role("button", name=re.compile("Cart", re.IGNORECASE)).click()

    def open_location(self) -> None:
        dialog = self.page.get_by_role("dialog", name=re.compile("Your Location", re.IGNORECASE))
        if not dialog.count() or not dialog.is_visible():
            self.page.get_by_role("button", name=re.compile("Select Location", re.IGNORECASE)).click()

    def search_product(self, product_name: str) -> None:
        self.logger.info("Searching for product: %s", product_name)
        search_box = self.page.get_by_role("combobox", name=re.compile("Search", re.IGNORECASE))
        if not search_box.count():
            trigger = self.page.get_by_role("link", name=re.compile("Search for products", re.IGNORECASE))
            if trigger.count():
                trigger.click()
            else:
                self.page.goto(f"{BASE_URL.rstrip('/')}/search", wait_until="domcontentloaded")
            search_box = self.page.get_by_role("combobox", name=re.compile("Search", re.IGNORECASE))
        expect(search_box).to_be_visible()
        search_box.fill(product_name)
        search_box.press("Enter")
