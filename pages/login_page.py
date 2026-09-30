import re

from playwright.sync_api import Page, expect

from utils.logger import get_logger


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(__name__)

    def open_login(self) -> None:
        self.logger.info("Opening login UI")
        login_button = self.page.get_by_role("button", name=re.compile("login", re.IGNORECASE))
        if login_button.count():
            login_button.click()

    def verify_login_page(self) -> None:
        login_dialog = self.page.get_by_role("dialog", name=re.compile("login|welcome", re.IGNORECASE))
        if login_dialog.count() and login_dialog.first.is_visible():
            expect(login_dialog.first).to_be_visible()
            return
        expect(self.mobile_field.first).to_be_visible()

    @property
    def mobile_field(self):
        field = self.page.get_by_role("textbox", name=re.compile("mobile|phone|number", re.IGNORECASE))
        if field.count():
            return field
        field = self.page.get_by_placeholder(re.compile("mobile|phone|number", re.IGNORECASE))
        if field.count():
            return field
        return self.page.locator('input:not([type="hidden"])')

    def verify_mobile_field(self) -> None:
        expect(self.mobile_field.first).to_be_visible()

    def enter_mobile_number(self, mobile_number: str) -> None:
        self.logger.info("Entering synthetic invalid login input for validation")
        self.mobile_field.fill(mobile_number)

    def click_continue(self) -> bool:
        continue_button = self.page.get_by_role("button", name=re.compile("continue|next", re.IGNORECASE))
        expect(continue_button.first).to_be_visible()
        if not continue_button.first.is_enabled():
            return False
        continue_button.first.click()
        return True

    def verify_validation_message(self) -> None:
        continue_button = self.page.get_by_role("button", name=re.compile("continue|next", re.IGNORECASE))
        if continue_button.count() and not continue_button.first.is_enabled():
            expect(continue_button.first).to_be_disabled()
            return
        validation = self.page.get_by_text(
            re.compile("enter.*(valid|mobile|phone)|invalid|required|10 digit", re.IGNORECASE)
        )
        expect(validation.first).to_be_visible()
