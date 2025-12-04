"""Module entrypoint for running the CLI with `python -m salesforce_autotest`."""
from .cli import main


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
