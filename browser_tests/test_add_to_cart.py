"""Verify one Backpack reaches Your Cart; stop before checkout."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_add_backpack_to_cart(driver):
    # Arrange: use a fresh session and the public demo account.
    driver.get("https://www.saucedemo.com/")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Act: product-specific locator observed on the live Products page.
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="shopping-cart-link"]'))).click()

    # Assert: inspect actual cart contents, including row count and quantity.
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '[data-test="title"]'), "Your Cart"))
    assert driver.current_url == "https://www.saucedemo.com/cart.html"
    rows = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-test="inventory-item"]')))
    assert len(rows) == 1
    assert rows[0].find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]').text == "Sauce Labs Backpack"
    assert rows[0].find_element(By.CSS_SELECTOR, '[data-test="item-quantity"]').text == "1"
