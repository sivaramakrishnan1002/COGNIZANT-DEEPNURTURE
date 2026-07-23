from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InputFormPage(BasePage):
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "inputEmail4")
    PHONE_INPUT = (By.ID, "inputPassword4")
    ADDRESS_INPUT = (By.ID, "inputAddress1")
    COMPANY_INPUT = (By.ID, "company")
    WEBSITE_INPUT = (By.ID, "websitename")
    COUNTRY_SELECT = (By.NAME, "country")
    CITY_INPUT = (By.ID, "inputCity")
    ADDRESS_2_INPUT = (By.ID, "inputAddress2")
    STATE_INPUT = (By.ID, "inputState")
    ZIP_INPUT = (By.ID, "inputZip")
    SUBMIT_BUTTON = (By.XPATH, "//main//button[@type='submit' and normalize-space()='Submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#success-msg, .success-msg, .alert-success")

    def fill_form(self, name: str, email: str, phone: str, address: str) -> None:
        for locator, value in ((self.NAME_INPUT, name), (self.EMAIL_INPUT, email),
                               (self.PHONE_INPUT, phone), (self.ADDRESS_INPUT, address)):
            element = self.wait_for_element(locator)
            element.clear()
            element.send_keys(value)
        # The live demo marks additional contact/address controls as required.
        for locator, value in ((self.COMPANY_INPUT, "Deep Nurture"),
                               (self.WEBSITE_INPUT, "https://example.com"),
                               (self.CITY_INPUT, "Bengaluru"),
                               (self.ADDRESS_2_INPUT, "Learning Block"),
                               (self.STATE_INPUT, "Karnataka"),
                               (self.ZIP_INPUT, "560001")):
            element = self.wait_for_element(locator)
            element.clear()
            element.send_keys(value)
        Select(self.wait_for_element(self.COUNTRY_SELECT)).select_by_visible_text("India")

    def submit_form(self) -> None:
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_success_message(self) -> str:
        return self.wait_for_element(self.SUCCESS_MESSAGE).text
