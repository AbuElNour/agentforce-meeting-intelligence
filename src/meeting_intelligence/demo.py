from __future__ import annotations

import json
from dataclasses import asdict

from .processor import MeetingProcessor


TRANSCRIPT = """
Decision: Launch the synthetic pilot in the North region.
ACTION: Prepare the evaluation dataset | owner=Sam | due=2026-08-15
Risk: The mock connector may exceed its latency budget.
Assume: The customer approved production deployment.
"""


def main() -> None:
    print(json.dumps(asdict(MeetingProcessor().process(TRANSCRIPT)), indent=2))


if __name__ == "__main__":
    main()

