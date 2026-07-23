from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class DropdownPage(BasePage):
    DAY_SELECT = (By.ID, "select-demo")

    def select_day(self, day_name: str) -> str:
        dropdown = Select(self.wait_for_element(self.DAY_SELECT))
        dropdown.select_by_visible_text(day_name)
        return dropdown.first_selected_option.text
