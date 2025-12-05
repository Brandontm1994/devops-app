# salesforce_autotest/locators/sf_dom_analyzer.py

from selenium.webdriver.common.by import By

class SalesforceDomAnalyzer:
    """
    Fallback analysis for Salesforce DOM:
    - Normalizes labels
    - Identifies repeated regions
    - Locates LWC input wrappers
    - Detects accessible names
    """

    def __init__(self, driver):
        self.driver = driver

    def fallback_locators(self, label=None):
        locs = []

        if label:
            # aria-label match
            locs.append((By.CSS_SELECTOR, f"[aria-label*='{label}']"))

            # text match
            locs.append((By.XPATH, f"//*[contains(normalize-space(), '{label}')]"))

            # LWC input wrapper
            locs.append((By.CSS_SELECTOR, f"lightning-input[label='{label}'] input"))

        return locs
