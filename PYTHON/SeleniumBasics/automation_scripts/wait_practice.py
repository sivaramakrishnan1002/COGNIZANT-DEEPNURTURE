"""Hands-On 5, Task 2: explicit waits, clickability, and FluentWait-style polling."""
from time import perf_counter, sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def explicit_alert_wait(driver, base_url: str) -> float:
    driver.get(base_url + "bootstrap-alerts-demo")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Success Message')]"))
    )
    started = perf_counter()
    button.click()
    alert = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "successfully" in alert.text.lower()
    return perf_counter() - started


def sleep_alert_wait(driver, base_url: str) -> float:
    driver.get(base_url + "bootstrap-alerts-demo")
    started = perf_counter()
    driver.find_element(By.XPATH, "//button[contains(., 'Success Message')]").click()
    sleep(3)  # Deliberately poor example: always waits the full duration.
    assert "successfully" in driver.find_element(By.CSS_SELECTOR, ".alert-success").text.lower()
    return perf_counter() - started


def fluent_table_row_wait(driver) -> None:
    """Poll every 500 ms for a visible table row, ignoring temporarily absent elements."""
    wait = WebDriverWait(driver, 10, poll_frequency=0.5, ignored_exceptions=(NoSuchElementException,))
    row = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
    assert row.is_displayed()


# visibility_of_element_located means the element is displayed; element_to_be_clickable
# additionally requires it to be enabled and ready to receive a click.
