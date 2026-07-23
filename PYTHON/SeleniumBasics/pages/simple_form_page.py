from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Get Checked Value')]")
    DISPLAYED_MESSAGE = (By.CSS_SELECTOR, "#message")

    def enter_message(self, text: str) -> None:
        field = self.wait_for_element(self.MESSAGE_INPUT)
        field.clear()
        field.send_keys(text)

    def click_submit(self) -> None:
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_displayed_message(self) -> str:
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text
