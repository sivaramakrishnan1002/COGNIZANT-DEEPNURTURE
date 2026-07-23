"""Shared pytest configuration for Hands-On 6 and 7."""
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_OUTPUT = Path(__file__).resolve().parents[1] / "outputs"


@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver(request):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.implicitly_wait(0)
    request.node.driver = browser
    yield browser
    screenshot_dir = BASE_OUTPUT / "HANDSON 6"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    safe_name = request.node.name.replace("[", "_").replace("]", "").replace(" ", "_")
    browser.save_screenshot(str(screenshot_dir / f"{safe_name}.png"))
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a failure screenshot before the browser fixture tears down."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = getattr(item, "driver", None)
        if browser:
            screenshot_dir = BASE_OUTPUT / "HANDSON 6"
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            safe_name = item.name.replace("[", "_").replace("]", "").replace(" ", "_")
            browser.save_screenshot(str(screenshot_dir / f"{safe_name}_failure.png"))
