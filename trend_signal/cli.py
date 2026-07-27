from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from .pipeline import run_pipeline


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Run the fictional public trend signal pipeline")
    command.add_argument("--input", type=Path, required=True)
    command.add_argument("--output-dir", type=Path, required=True)
    command.add_argument(
        "--as-of",
        default="2026-07-27T00:00:00Z",
        help="ISO-8601 scoring time. Defaults to the proof date.",
    )
    return command


def main() -> None:
    args = parser().parse_args()
    as_of = datetime.fromisoformat(args.as_of.replace("Z", "+00:00")).astimezone(UTC)
    receipt = run_pipeline(args.input, args.output_dir, as_of=as_of)
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
