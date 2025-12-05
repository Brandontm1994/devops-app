import json
from salesforce_autotest.locators.locator_engine import SalesforceLocatorEngine

class SalesforceEventListener:
    """
    Captures Salesforce UI events (clicks, inputs, dropdowns, lookups)
    and converts them to YAML-ready test steps.
    """

    def __init__(self, driver):
        self.driver = driver
        self.locator_engine = SalesforceLocatorEngine(driver)
        self.records = []

    def record_click(self, element):
        locator = self.locator_engine.build_locator(element)
        self.records.append({
            "action": "click",
            "locator": locator
        })
        print(f"[RECORDER] Captured click → {locator}")

    def record_input(self, element, value):
        locator = self.locator_engine.build_locator(element)
        self.records.append({
            "action": "input",
            "locator": locator,
            "value": value
        })
        print(f"[RECORDER] Captured input → {locator} = {value}")

    def record_combobox_select(self, element, value):
        locator = self.locator_engine.build_locator(element)
        self.records.append({
            "action": "select",
            "locator": locator,
            "value": value
        })
        print(f"[RECORDER] Combobox select → {locator}: {value}")

    def record_lookup_pick(self, element, value):
        locator = self.locator_engine.build_locator(element)
        self.records.append({
            "action": "lookup_select",
            "locator": locator,
            "value": value
        })
        print(f"[RECORDER] Lookup pick → {value}")

    def export_yaml_steps(self):
        return {"steps": self.records}