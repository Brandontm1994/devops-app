"""Command line interface for running Salesforce Apex tests."""
from __future__ import annotations

import argparse
import json
import sys

from .config import Settings
from .runner import TestRunner


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Salesforce Apex tests from the CLI")
    parser.add_argument(
        "config",
        help="Path to YAML configuration file containing auth settings and test plan.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write JSON results; defaults to stdout.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        settings = Settings.from_file(args.config)
        runner = TestRunner(settings)
        outcome = runner.run()
    except Exception as exc:  # pragma: no cover - CLI convenience
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    payload = {
        "queue_items": outcome.queue_items,
        "results": outcome.results,
        "failed": outcome.has_failures(),
    }

    serialized = json.dumps(payload, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(serialized)
    else:
        print(serialized)

    return 0 if not outcome.has_failures() else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
