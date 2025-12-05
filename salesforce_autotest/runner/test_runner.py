import yaml
import os
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from salesforce_autotest.locators.locator_engine import SalesforceLocatorEngine
from salesforce_autotest.runner.html_reporter import HTMLReporter
from salesforce_autotest.runner.logger import create_logger

class TestRunner:

    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        self.logger = create_logger()
        self.results = []
        self.html_reporter = HTMLReporter()

    def load_yaml(self):
        with open(self.yaml_file, "r") as f:
            return yaml.safe_load(f)

    def resolve_env(self, value):
        if isinstance(value, str):
            matches = re.findall(r"\$\{([^}]+)\}", value)
            for m in matches:
                env_val = os.environ.get(m, "")
                value = value.replace(f"$\{{{m}}}", env_val)
        return value

    def start_driver(self):
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        # CI Headless mode
        if os.environ.get("CI", "false").lower() == "true":
            options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    def execute_step(self, driver, step):
        action = step.get("action")
        self.logger.info(f"Running action: {action}")

        try:
            if action == "navigate":
                driver.get(step["url"])
                self.results.append({"action": action, "status": "PASS"})
                return

            locator = step.get("locator", {})

            # Resolve environment variables
            if "value" in step:
                step["value"] = self.resolve_env(step["value"])

            sf = SalesforceLocatorEngine(driver)

            if action == "click":
                el = sf.find(locator)
                el.click()
                self.results.append({"action": action, "status": "PASS"})
                return

            if action == "input":
                el = sf.find(locator)
                el.clear()
                el.send_keys(step["value"])
                self.results.append({"action": action, "status": "PASS"})
                return

            if action == "wait_for":
                timeout = step.get("timeout", 15)
                sf.wait_for(locator, timeout)
                self.results.append({"action": action, "status": "PASS"})
                return

            if action == "assert_visible":
                sf.wait_for(locator, timeout=10)
                self.results.append({"action": action, "status": "PASS"})
                return

            raise Exception(f"Unknown action {action}")

        except Exception as e:
            screenshot = f"screenshot_{int(time.time())}.png"
            driver.save_screenshot(screenshot)
            self.results.append({
                "action": action,
                "status": "FAIL",
                "details": str(e),
                "screenshot": screenshot
            })
            self.logger.error(f"Step failed: {e}")
            return "FAIL"

    def run(self):
        test = self.load_yaml()
        steps = test.get("steps", [])

        driver = self.start_driver()

        for step in steps:
            result = self.execute_step(driver, step)
            if result == "FAIL":
                break

        driver.quit()

        report_file = self.html_reporter.generate(self.results)
        self.logger.info(f"HTML report generated: {report_file}")

        # Return exit code for CI pipelines
        if any(r["status"] == "FAIL" for r in self.results):
            return 1

        return 0


def cli_main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", help="Path to YAML test file")
    args = parser.parse_args()

    runner = TestRunner(args.yaml_file)
    exit(runner.run())
