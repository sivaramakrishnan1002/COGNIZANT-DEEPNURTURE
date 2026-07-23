from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckboxPage(BasePage):
    OPTION_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")

    def _option(self, index: int):
        return self.driver.find_elements(*self.OPTION_CHECKBOXES)[index]

    def check_option(self, index: int) -> None:
        option = self._option(index)
        if not option.is_selected():
            self.driver.execute_script("arguments[0].click();", option)

    def uncheck_option(self, index: int) -> None:
        option = self._option(index)
        if option.is_selected():
            self.driver.execute_script("arguments[0].click();", option)

    def is_option_checked(self, index: int) -> bool:
        return self._option(index).is_selected()
