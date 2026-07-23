"""Hands-On 4: Selenium architecture, setup, navigation, tabs, and screenshots.

WebDriver is Selenium's browser-control API. It sends W3C WebDriver commands to a
browser driver, which controls the browser. Selenium Grid distributes those commands
to browser/machine combinations for parallel cross-browser execution. Selenium IDE is
a browser extension for recording/playback and generating starter automation code.
"""
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"
OUTPUT = Path(__file__).resolve().parents[2] / "outputs" / "HANDSON 4"


def create_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    driver = create_driver()
    try:
        # An implicit wait applies to every element lookup and can mask slow locators;
        # prefer explicit waits that state exactly what this particular action needs.
        driver.implicitly_wait(10)
        driver.get(BASE_URL)
        print(f"Playground title: {driver.title}")
        print(f"Original window size: {driver.get_window_size()}")
        # A fixed viewport makes responsive layouts and screenshots deterministic.
        driver.set_window_size(1280, 800)
        driver.get(BASE_URL + "simple-form-demo")
        assert "simple-form-demo" in driver.current_url
        driver.back()
        driver.execute_script('window.open("https://www.google.com");')
        print(f"Open handles: {driver.window_handles}")
        driver.switch_to.window(driver.window_handles[1])
        print(f"Second-tab title: {driver.title}")
        driver.switch_to.window(driver.window_handles[0])
        screenshot = OUTPUT / "playground_screenshot.png"
        assert driver.save_screenshot(str(screenshot))
        print(f"Screenshot created: {screenshot}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
