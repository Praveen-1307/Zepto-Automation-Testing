# Zepto Automation Testing

## Project Overview

A GitHub-ready Python automation framework for the publicly accessible Zepto website. It uses Playwright's synchronous API, Pytest, and Page Object Model classes. The tests exercise observable browsing and validation behavior; catalog data and delivery availability remain dynamic.

The suite does not use real credentials, OTPs, addresses, or payment information. It does not bypass CAPTCHA, confirm an order, or proceed through checkout/payment. Cart tests use an isolated browser context and stop at cart verification.

## Technologies

- Python 3.10+
- Playwright (sync API)
- Pytest
- pytest-html
- pytest-xdist
- Page Object Model
- Python logging

## Features

- Seven reusable page objects and shared browser fixtures
- 40 individually mapped test cases
- Chromium by default, with Firefox and WebKit options
- Headless by default; optional headed execution
- Screenshots and Playwright traces on test failures
- Optional per-test video recording
- HTML reports and Python logging
- Smoke, regression, search, product, cart, login, category, and end-to-end markers
- Dynamic product details are checked only when present

## Project Structure

```text
zepto-automation-testing/
├── pages/
│   ├── __init__.py
│   ├── home_page.py
│   ├── location_page.py
│   ├── search_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   ├── category_page.py
│   └── login_page.py
├── tests/
│   ├── __init__.py
│   ├── test_home_page.py
│   ├── test_location.py
│   ├── test_search.py
│   ├── test_product.py
│   ├── test_cart.py
│   ├── test_category.py
│   ├── test_login.py
│   └── test_end_to_end.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   └── test_data.py
├── screenshots/
├── reports/
├── videos/
├── traces/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── run_tests.py
├── .gitignore
└── README.md
```

## Installation

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install
```

To use another supported browser engine, install its browser with `python -m playwright install firefox` or `python -m playwright install webkit`.

## Run Tests

Run all tests:

```powershell
pytest
```

Run headed:

```powershell
pytest --headed
```

Select a browser:

```powershell
pytest --browser firefox
pytest --browser webkit
```

Run smoke, search, product, or cart tests:

```powershell
pytest -m smoke
pytest -m search
pytest -m product
pytest -m cart
```

The convenience runner supports the same groups:

```powershell
python run_tests.py
python run_tests.py smoke
python run_tests.py search
python run_tests.py product
python run_tests.py cart
```

Generate the self-contained HTML report:

```powershell
pytest --html=reports/report.html --self-contained-html
```

Run one test:

```powershell
pytest tests/test_search.py::test_TC15_search_valid_product_name
```

Run tests in parallel:

```powershell
pytest -n auto
```

Record videos in addition to failure screenshots and traces:

```powershell
pytest --record-video
```

Override the base URL or default timeout using environment variables `ZEPTO_BASE_URL` and `ZEPTO_TIMEOUT_MS`.

## Test Cases

| ID | Test Case | Module |
|----|-----------|--------|
| TC01 | Verify website launches | Home |
| TC02 | Verify home page title | Home |
| TC03 | Verify Zepto logo is displayed | Home |
| TC04 | Verify location selector is displayed | Home |
| TC05 | Verify search box is displayed | Home |
| TC06 | Verify login option is displayed | Home |
| TC07 | Verify cart option is displayed | Home |
| TC08 | Verify Shop by Category section is displayed | Home |
| TC09 | Verify Fruits & Vegetables category is displayed | Home |
| TC10 | Verify grocery category is displayed | Home |
| TC11 | Verify user can open the location selector | Location |
| TC12 | Verify location search field is displayed | Location |
| TC13 | Verify location selection validation | Location |
| TC14 | Verify search box accepts a product name | Search |
| TC15 | Verify search using a valid product name | Search |
| TC16 | Verify search results are displayed | Search |
| TC17 | Verify invalid/non-existing product search | Search |
| TC18 | Verify search result product name is displayed | Search |
| TC19 | Verify product price is displayed | Search |
| TC20 | Verify product discount where available | Search |
| TC21 | Verify product rating where available | Search |
| TC22 | Verify product image is displayed | Search |
| TC23 | Verify user can open a product | Product |
| TC24 | Verify product details are displayed | Product |
| TC25 | Verify Add button is displayed for an available product | Product |
| TC26 | Verify user can add a product to cart | Cart |
| TC27 | Verify cart count changes after adding a product | Cart |
| TC28 | Verify cart displays the added product | Cart |
| TC29 | Verify product quantity can be increased | Cart |
| TC30 | Verify product quantity can be decreased | Cart |
| TC31 | Verify product can be removed from cart | Cart |
| TC32 | Verify empty cart state is displayed | Cart |
| TC33 | Verify category navigation | Category |
| TC34 | Verify category product listing | Category |
| TC35 | Verify Best Sellers navigation | Category |
| TC36 | Verify login page/modal opens | Login |
| TC37 | Verify login/mobile number field is displayed | Login |
| TC38 | Verify login validation for invalid input | Login |
| TC39 | Verify page refresh/navigation behavior | Home |
| TC40 | Verify complete shopping workflow, stopping at cart | E2E |

## Limitations

- OTP is not automated and no real credentials are used.
- CAPTCHA is not bypassed or solved.
- Real payments, checkout confirmation, and order placement are not performed.
- The end-to-end flow adds an item only to the isolated browser cart and stops before checkout.
- Product names, availability, prices, discounts, and ratings can change; optional data is not hard-coded.
- Location availability and the public website UI can change. The location tests use a synthetic invalid query; the end-to-end test inspects the location selector but does not save a personal address.
- Automated-browser protection may return an HTTP 202 response with an empty document in some environments. The suite does not bypass CAPTCHA or other access controls; site-dependent checks require the public interface to be accessible.
- A test may be skipped with a reason if an item, optional UI element, or public delivery area is unavailable.

## Reports and Artifacts

`reports/report.html` is a self-contained pytest-html summary with test outcomes and captured log output. The `screenshots/` and `traces/` directories receive artifacts for failed tests; trace archives can be opened with `python -m playwright show-trace traces/<trace-file>.zip`. Video capture is off by default and enabled with `--record-video`. Generated artifacts are ignored by Git, while the directories remain tracked.

## Upload to GitHub

Create an empty GitHub repository, then run these commands from the project directory:

```powershell
git init
git add .
git commit -m "Add Zepto Playwright automation framework"
git branch -M main
git remote add origin https://github.com/<your-user>/zepto-automation-testing.git
git push -u origin main
```
