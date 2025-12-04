"""Authentication helpers for Salesforce tooling API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import requests

from .config import ResolvedAuthConfig


@dataclass
class AuthResult:
    access_token: str
    instance_url: str


class SalesforceAuthenticator:
    """Perform OAuth username-password flow against Salesforce."""

    def __init__(self, config: ResolvedAuthConfig) -> None:
        self.config = config

    def authenticate(self) -> AuthResult:
        payload = {
            "grant_type": "password",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "username": self.config.username,
            "password": f"{self.config.password}{self.config.security_token}",
        }
        response = requests.post(self.config.login_url, data=payload, timeout=30)
        response.raise_for_status()
        data: Dict[str, str] = response.json()
        return AuthResult(access_token=data["access_token"], instance_url=data["instance_url"])
