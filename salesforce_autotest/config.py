"""Configuration helpers for the Salesforce auto testing tool."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml


def _get_env_value(env_var: str, required: bool = True) -> Optional[str]:
    """Read an environment variable, optionally requiring a value."""
    value = os.getenv(env_var)
    if required and not value:
        raise ValueError(f"Environment variable {env_var} is required but not set")
    return value


@dataclass
class AuthConfig:
    """Environment-driven auth settings."""

    client_id_env: str
    client_secret_env: str
    username_env: str
    password_env: str
    security_token_env: str
    domain: str = "login"

    def resolve(self) -> "ResolvedAuthConfig":
        """Resolve environment variables to real values."""
        return ResolvedAuthConfig(
            client_id=_get_env_value(self.client_id_env),
            client_secret=_get_env_value(self.client_secret_env),
            username=_get_env_value(self.username_env),
            password=_get_env_value(self.password_env),
            security_token=_get_env_value(self.security_token_env),
            domain=self.domain,
        )


@dataclass
class TestPlan:
    """Collection of Apex test classes to execute."""

    classes: List[str] = field(default_factory=list)
    synchronous: bool = False
    api_version: str = "58.0"
    timeout_seconds: int = 300

    def validate(self) -> None:
        if self.timeout_seconds < 1:
            raise ValueError("timeout_seconds must be >= 1")
        if not self.classes:
            raise ValueError("At least one Apex test class must be provided")


@dataclass
class Settings:
    auth: AuthConfig
    test_plan: TestPlan

    @classmethod
    def from_file(cls, path: str) -> "Settings":
        try:
            with open(path, "r", encoding="utf-8") as handle:
                raw: Dict[str, Any] = yaml.safe_load(handle) or {}
        except FileNotFoundError as exc:  # pragma: no cover - IO defensive
            raise ValueError(f"Configuration file not found: {path}") from exc

        if not isinstance(raw, dict):
            raise ValueError("Configuration must be a mapping of settings")

        if "auth" not in raw or "test_plan" not in raw:
            raise ValueError("Configuration requires 'auth' and 'test_plan' sections")

        auth = AuthConfig(**raw["auth"])
        test_plan = TestPlan(**raw["test_plan"])
        test_plan.validate()
        return cls(auth=auth, test_plan=test_plan)


@dataclass
class ResolvedAuthConfig:
    """Resolved authentication values for Salesforce."""

    client_id: str
    client_secret: str
    username: str
    password: str
    security_token: str
    domain: str

    @property
    def login_url(self) -> str:
        return f"https://{self.domain}.salesforce.com/services/oauth2/token"
