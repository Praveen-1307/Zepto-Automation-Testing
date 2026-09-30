import re

from playwright.sync_api import Page, expect

from utils.logger import get_logger


class LocationPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(__name__)

    @property
    def dialog(self):
        return self.page.get_by_role("dialog", name=re.compile("Your Location", re.IGNORECASE))

    @property
    def location_input(self):
        field = self.page.get_by_role("textbox", name=re.compile("Search a new address", re.IGNORECASE))
        if field.count():
            return field
        return self.page.get_by_placeholder(re.compile("Search a new address|location|address", re.IGNORECASE))

    def open_location_selector(self) -> None:
        self.logger.info("Opening location selector")
        if not self.dialog.count() or not self.dialog.is_visible():
            self.page.get_by_role("button", name=re.compile("Select Location", re.IGNORECASE)).click()
        expect(self.dialog).to_be_visible()

    def verify_location_input(self) -> None:
        expect(self.location_input).to_be_visible()

    def enter_location(self, location: str) -> None:
        self.logger.info("Entering a non-personal location query")
        expect(self.location_input).to_be_visible()
        self.location_input.fill(location)

    def select_location(self, location: str) -> bool:
        """Select a visible public suggestion only when the caller explicitly requests it."""
        suggestion = self.page.get_by_text(location, exact=True)
        if suggestion.count() and suggestion.first.is_visible():
            suggestion.first.click()
            return True
        return False

    def verify_location(self) -> bool:
        selected = self.page.get_by_role("button", name=re.compile("Select Location", re.IGNORECASE))
        return selected.count() > 0 and selected.is_visible()

    def handle_location_validation(self) -> bool:
        """Confirm the selector remains open for a synthetic, unsupported query."""
        return self.dialog.count() > 0 and self.dialog.is_visible()
