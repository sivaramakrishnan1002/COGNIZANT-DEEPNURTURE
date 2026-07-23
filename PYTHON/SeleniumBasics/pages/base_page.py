from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url: str) -> None:
        self.driver.get(url)

    def get_title(self) -> str:
        return self.driver.title

    def wait_for_element(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
