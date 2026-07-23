"""Hands-On 5, Task 1: locator examples for the Simple Form and Checkbox demos."""
from selenium.webdriver.common.by import By


def verify_locator_strategies(driver, base_url: str) -> None:
    driver.get(base_url + "simple-form-demo")
    # Preference order: ID, NAME, CSS, relative XPath, class, tag, absolute XPath.
    # IDs are unique/readable; absolute XPath breaks whenever markup changes.
    by_id = driver.find_element(By.ID, "user-message")
    by_name = driver.find_element(By.NAME, "message")
    by_class = driver.find_element(By.CLASS_NAME, "form-control")
    by_tag = driver.find_element(By.TAG_NAME, "input")
    by_absolute_xpath = driver.find_element(By.XPATH, "/html/body//input[@id='user-message']")
    by_relative_xpath = driver.find_element(By.XPATH, "//input[@id='user-message']")
    css_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
    css_attribute = driver.find_element(By.CSS_SELECTOR, "input[name='message']")
    css_parent_child = driver.find_element(By.CSS_SELECTOR, "div > input#user-message")
    assert all((by_id, by_name, by_class, by_tag, by_absolute_xpath, by_relative_xpath,
                css_id, css_attribute, css_parent_child))

    driver.get(base_url + "checkbox-demo")
    option_one = driver.find_element(By.XPATH, "//label[text()='Option 1']")
    option_labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
    assert option_one.is_displayed() and option_labels
