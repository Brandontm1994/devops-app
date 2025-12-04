# salesforce_autotest/locators/locator_builder_salesforce.py

from selenium.webdriver.common.by import By
from .shadow_dom import expand_shadow_root
from .sf_dom_analyzer import SalesforceDomAnalyzer

class SalesforceLocatorBuilder:
    """
    Generates resilient locators for Salesforce Lightning based on:
    - aria-label
    - data-* attributes
    - lightning-base-component classes
    - LWC shadow structure
    - text content normalization
    """

    def __init__(self, driver):
        self.driver = driver
        self.dom = SalesforceDomAnalyzer(driver)

    def by_label(self, label_text):
        """
        Returns a locator using aria-label, fallback text, or LWC wrappers.
        """
        candidates = [
            (By.CSS_SELECTOR, f"[aria-label='{label_text}']"),
            (By.CSS_SELECTOR, f"button[title='{label_text}']"),
            (By.XPATH, f"//*[normalize-space()='{label_text}']"),
        ]
        return candidates

    def by_data_key(self, key):
        return [(By.CSS_SELECTOR, f"[data-key='{key}']")]

    def by_record_id(self, record_id):
        return [(By.CSS_SELECTOR, f"[data-recordid='{record_id}']")]

    def by_lwc_component(self, tag_name):
        """
        Locates custom LWC components like lightning-input, lightning-button.
        """
        return [(By.CSS_SELECTOR, tag_name)]

    def resolve_shadow_locator(self, element, css_selector):
        """
        Traverses shadow roots until the element is found.
        """
        return expand_shadow_root(self.driver, element, css_selector)

    def smart_locator(self, label=None, key=None, record_id=None, tag=None):
        """
        Combines heuristics into a single lookup strategy.
        """
        locators = []

        if label:
            locators.extend(self.by_label(label))

        if key:
            locators.extend(self.by_data_key(key))

        if record_id:
            locators.extend(self.by_record_id(record_id))

        if tag:
            locators.extend(self.by_lwc_component(tag))

        # Add DOM analyzer fallback normalization
        locators.extend(self.dom.fallback_locators(label=label))

        return locators
