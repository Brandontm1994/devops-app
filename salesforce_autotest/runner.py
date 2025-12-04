"""High-level test runner for Salesforce Apex tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .auth import SalesforceAuthenticator
from .config import Settings
from .tooling import ToolingClient


@dataclass
class TestOutcome:
    queue_items: Dict
    results: List[Dict]

    def has_failures(self) -> bool:
        return any(result.get("Outcome") != "Pass" for result in self.results)


class TestRunner:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def run(self) -> TestOutcome:
        auth_result = SalesforceAuthenticator(self.settings.auth.resolve()).authenticate()
        tooling = ToolingClient(auth_result, self.settings.test_plan.api_version)

        class_ids = tooling.find_classes(self.settings.test_plan.classes)
        missing = set(self.settings.test_plan.classes) - set(class_ids.keys())
        if missing:
            raise ValueError(f"Unable to locate Apex classes in org: {', '.join(sorted(missing))}")

        if self.settings.test_plan.synchronous:
            data = tooling.run_synchronous(class_ids.values())
            queue_items = {"synchronous": data}
            results = data.get("records", []) if isinstance(data, dict) else []
            return TestOutcome(queue_items=queue_items, results=results)

        queue_ids = tooling.queue_tests(class_ids.values())
        if not queue_ids:
            raise ValueError("No test queue items were created; check API permissions")
        queue_items = tooling.poll_queue(queue_ids, timeout_seconds=self.settings.test_plan.timeout_seconds)
        results = tooling.get_test_results(queue_items)
        return TestOutcome(queue_items=queue_items, results=results)
