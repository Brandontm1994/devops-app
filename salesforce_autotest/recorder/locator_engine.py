class SalesforceLocatorEngine:

    def __init__(self, driver):
        self.driver = driver

    def build_locator(self, element):
        """
        Salesforce-specific locator rules:
        - aria-label
        - data-target
        - LWC/Aura fallback attributes
        """

        # Highest priority: aria-label
        aria = element.get_attribute("aria-label")
        if aria:
            return {"type": "aria_label", "value": aria}

        # Next priority: data-target
        target = element.get_attribute("data-target")
        if target:
            return {"type": "data_target", "value": target}

        # LWC / Aura generated IDs (input-17, combobox-button-42)
        element_id = element.get_attribute("id")
        if element_id and ("input" in element_id or "button" in element_id):
            return {"type": "id", "value": element_id}

        # Visible text fallback
        text = element.text.strip()
        if text:
            return {"type": "text", "value": text}

        # Tag/class fallback
        tag = element.tag_name
        class_name = element.get_attribute("class")
        return {"type": "tag_class", "tag": tag, "class": class_name}

    def find_shadow(self, locator):
        """
        Handles LWC Shadow DOM traversal.
        """
        script = """
            const root = arguments[0].shadowRoot;
            if (!root) return null;
            return root.querySelector(arguments[1]);
        """
        root_elem = self.find(locator)
        selector = self.selector_from_locator(locator)

        try:
            return self.driver.execute_script(script, root_elem, selector)
        except Exception:
            return None
