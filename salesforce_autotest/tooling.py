"""Salesforce Tooling API helpers."""
from __future__ import annotations

import time
from typing import Dict, Iterable, List, Optional

import requests

from .auth import AuthResult


class ToolingClient:
    """Lightweight wrapper around the Salesforce Tooling API."""

    def __init__(self, auth: AuthResult, api_version: str) -> None:
        self.auth = auth
        self.api_version = api_version

    @property
    def base_url(self) -> str:
        return f"{self.auth.instance_url}/services/data/v{self.api_version}/tooling"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.auth.access_token}",
            "Content-Type": "application/json",
        }

    def _get(self, path: str) -> Dict:
        response = requests.get(f"{self.base_url}{path}", headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, json: Dict) -> Dict:
        response = requests.post(
            f"{self.base_url}{path}", headers=self._headers(), json=json, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def find_classes(self, names: Iterable[str]) -> Dict[str, str]:
        """Return a mapping of Apex class names to Ids."""
        quoted = ",".join([f"'{name}'" for name in names])
        query = (
            "SELECT Id, Name FROM ApexClass WHERE NamespacePrefix = NULL AND Name IN ("
            f"{quoted})"
        )
        data = self._get(f"/query/?q={query}")
        return {row["Name"]: row["Id"] for row in data.get("records", [])}

    def queue_tests(self, class_ids: Iterable[str]) -> List[str]:
        ids = list(class_ids)
        body = {
            "tests": [
                {
                    "classId": class_id,
                }
                for class_id in ids
            ]
        }
        data = self._post("/runTestsAsynchronous", json=body)
        job_id = data.get("id")
        if job_id:
            return [job_id]
        # Fallback path when API returns list of queue items
        return data.get("queueItems", [])

    def poll_queue(self, queue_ids: List[str], timeout_seconds: int = 300) -> Dict:
        start = time.time()
        while True:
            quoted = ",".join([f"'{queue_id}'" for queue_id in queue_ids])
            query = (
                "SELECT Id, Status, ApexClass.Name, ExtendedStatus FROM ApexTestQueueItem "
                f"WHERE Id IN ({quoted})"
            )
            data = self._get(f"/query/?q={query}")
            items = data.get("records", [])
            statuses = {item["Status"] for item in items}
            if statuses.issubset({"Completed", "Failed"}) and items:
                return {item["Id"]: item for item in items}
            if time.time() - start > timeout_seconds:
                raise TimeoutError("Timed out waiting for tests to complete")
            time.sleep(5)

    def get_test_results(self, queue_items: Dict[str, Dict]) -> List[Dict]:
        queue_ids = list(queue_items.keys())
        quoted = ",".join([f"'{queue_id}'" for queue_id in queue_ids])
        query = (
            "SELECT ApexClass.Name, MethodName, Outcome, Message, StackTrace "
            "FROM ApexTestResult WHERE QueueItemId IN (" + quoted + ")"
        )
        data = self._get(f"/query/?q={query}")
        return data.get("records", [])

    def run_synchronous(self, class_ids: Iterable[str]) -> Dict:
        body = {"classIds": list(class_ids)}
        return self._post("/runTestsSynchronous", json=body)
