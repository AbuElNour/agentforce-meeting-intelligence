from __future__ import annotations

import json
import time
from pathlib import Path

from meeting_intelligence import MeetingProcessor


def cases() -> list[dict]:
    return [
        *[
            {
                "id": f"decision-{index}",
                "transcript": f"Decision: Choose synthetic option {index}.",
                "expected": ("decisions", 1),
            }
            for index in range(1, 6)
        ],
        *[
            {
                "id": f"action-{index}",
                "transcript": f"ACTION: Prepare fixture {index} | owner=Owner {index} | due=2026-09-{index:02d}",
                "expected": ("actions", 1),
            }
            for index in range(1, 6)
        ],
        *[
            {
                "id": f"risk-{index}",
                "transcript": f"Risk: Synthetic risk {index}.",
                "expected": ("risks", 1),
            }
            for index in range(1, 4)
        ],
        *[
            {
                "id": f"unsupported-{index}",
                "transcript": f"Assume: Unverified claim {index}.",
                "expected": ("unsupported_claims", 1),
            }
            for index in range(1, 4)
        ],
        {"id": "malformed-1", "transcript": "ACTION: no owner", "expected": ("actions", 0)},
        {"id": "malformed-2", "transcript": "", "expected": ("decisions", 0)},
        {
            "id": "mixed-1",
            "transcript": "Decision: Proceed.\nACTION: Verify | owner=Lee | due=Tomorrow\nRisk: Delay.",
            "expected": ("actions", 1),
        },
        {
            "id": "idempotent-1",
            "transcript": "Decision: Record once.",
            "expected": ("decisions", 1),
            "idempotent": True,
        },
    ]


def main() -> None:
    records = []
    latencies = []
    for case in cases():
        for trial in range(1, 4):
            processor = MeetingProcessor()
            start = time.perf_counter()
            result = processor.process(case["transcript"])
            if case.get("idempotent"):
                processor.process(case["transcript"])
            latency = (time.perf_counter() - start) * 1000
            latencies.append(latency)
            field, expected = case["expected"]
            records.append(
                {
                    "case_id": case["id"],
                    "trial": trial,
                    "passed": len(getattr(result, field)) == expected,
                    "latency_ms": round(latency, 3),
                }
            )
    passed = sum(item["passed"] for item in records)
    report = {
        "schema_version": 1,
        "mode": "deterministic-offline",
        "cases": len(cases()),
        "trials": len(records),
        "passed": passed,
        "success_rate": passed / len(records),
        "p50_latency_ms": round(sorted(latencies)[len(latencies) // 2], 3),
        "estimated_cost_usd": 0,
        "results": records,
    }
    Path(__file__).with_name("results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "results"}, indent=2))
    raise SystemExit(0 if passed == len(records) else 1)


if __name__ == "__main__":
    main()

