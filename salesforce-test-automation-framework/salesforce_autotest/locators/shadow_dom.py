# salesforce_autotest/locators/shadow_dom.py

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def expand_shadow_root(driver, element, final_selector):
    """
    Recursively navigates through LWC shadow roots to locate elements inside Lightning components.
    """

    try:
        shadow = driver.execute_script("return arguments[0].shadowRoot", element)
        if shadow:
            try:
                return shadow.find_element(By.CSS_SELECTOR, final_selector)
            except NoSuchElementException:
                pass
    except Exception:
        pass

    # If no shadow root resolution works, standard CSS lookup
    try:
        return element.find_element(By.CSS_SELECTOR, final_selector)
    except NoSuchElementException:
        return None
