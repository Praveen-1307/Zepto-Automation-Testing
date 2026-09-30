import argparse
import re
from datetime import datetime

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from utils.config import (
    DEFAULT_TIMEOUT_MS,
    SCREENSHOTS_DIR,
    TRACES_DIR,
    VIDEOS_DIR,
)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def pytest_addoption(parser):
    try:
        parser.addoption("--headed", action="store_true", help="Run the selected browser with a visible window")
    except argparse.ArgumentError:
        pass
    try:
        parser.addoption(
        "--browser",
        choices=("chromium", "firefox", "webkit"),
        default="chromium",
        help="Browser engine to use (default: chromium)",
        )
    except argparse.ArgumentError:
        pass
    try:
        parser.addoption("--record-video", action="store_true", help="Record videos under videos/ for each test")
    except argparse.ArgumentError:
        pass


@pytest.fixture(scope="session")
def browser(request) -> Browser:
    browser_name = request.config.getoption("--browser")
    if isinstance(browser_name, list):
        browser_name = browser_name[0] if browser_name else "chromium"
    headless = not request.config.getoption("--headed")
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, browser_name)
        instance = browser_type.launch(headless=headless)
        yield instance
        instance.close()


@pytest.fixture
def browser_context(browser: Browser, request) -> BrowserContext:
    record_video = request.config.getoption("--record-video")
    context_options = {"viewport": {"width": 1440, "height": 1000}}
    if record_video:
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        context_options["record_video_dir"] = str(VIDEOS_DIR)
    context = browser.new_context(**context_options)
    context.set_default_timeout(DEFAULT_TIMEOUT_MS)
    yield context
    context.close()


@pytest.fixture
def page(browser_context: BrowserContext, request) -> Page:
    current_page = browser_context.new_page()
    browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield current_page

    report = getattr(request.node, "rep_call", None)
    failed = report is not None and report.failed
    case_id = re.search(r"TC\d{2}", request.node.name)
    name = re.sub(r"[^A-Za-z0-9_-]+", "_", request.node.name.removeprefix("test_"))
    if case_id and not name.startswith(case_id.group()):
        name = f"{case_id.group()}_{name}"

    if failed:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        TRACES_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = SCREENSHOTS_DIR / f"{name}.png"
        trace_path = TRACES_DIR / f"{name}.zip"
        if screenshot_path.exists() or trace_path.exists():
            suffix = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            screenshot_path = SCREENSHOTS_DIR / f"{name}_{suffix}.png"
            trace_path = TRACES_DIR / f"{name}_{suffix}.zip"
        current_page.screenshot(path=str(screenshot_path), full_page=True)
        browser_context.tracing.stop(path=str(trace_path))
    else:
        browser_context.tracing.stop()
