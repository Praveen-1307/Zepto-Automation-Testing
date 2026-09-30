import re

from playwright.sync_api import Page, expect

from utils.config import BASE_URL
from utils.logger import get_logger


class CategoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(__name__)

    def open_category(self, category: str) -> bool:
        self.logger.info("Opening category: %s", category)
        link = self.page.get_by_role("link", name=re.compile(re.escape(category), re.IGNORECASE))
        if not link.count():
            self.page.goto(BASE_URL, wait_until="domcontentloaded")
            link = self.page.get_by_role("link", name=re.compile(re.escape(category), re.IGNORECASE))
        if not link.count():
            return False
        link.first.click()
        return True

    def verify_category(self, category: str) -> None:
        expect(self.page.get_by_text(re.compile(re.escape(category), re.IGNORECASE)).first).to_be_visible()

    def verify_products(self) -> bool:
        products = self.page.locator('a[href*="/pn/"]')
        return products.count() > 0 and products.first.is_visible()

    def open_best_sellers(self) -> bool:
        self.logger.info("Opening Best Sellers navigation when available")
        item = self.page.get_by_role("link", name=re.compile("best.?sellers?", re.IGNORECASE))
        if not item.count():
            item = self.page.get_by_role("button", name=re.compile("best.?sellers?", re.IGNORECASE))
        if not item.count():
            return False
        item.first.click()
        return True

    def verify_best_sellers(self) -> bool:
        label = self.page.get_by_text(re.compile("best.?sellers?", re.IGNORECASE))
        return label.count() > 0 and label.first.is_visible()
