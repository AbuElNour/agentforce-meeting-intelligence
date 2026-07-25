from __future__ import annotations

import hashlib
import re

from .types import ActionItem, MeetingResult


ACTION = re.compile(r"^ACTION:\s*(?P<task>.+?)\s*\|\s*owner=(?P<owner>[^|]+)\|\s*due=(?P<due>.+)$", re.I)


class MeetingProcessor:
    """Outcome extractor with source-line evidence and idempotent storage."""

    def __init__(self) -> None:
        self._processed: dict[str, MeetingResult] = {}

    @staticmethod
    def meeting_id(transcript: str) -> str:
        return hashlib.sha256(transcript.strip().encode()).hexdigest()[:16]

    def process(self, transcript: str) -> MeetingResult:
        identifier = self.meeting_id(transcript)
        if identifier in self._processed:
            cached = self._processed[identifier]
            cached.trace.append({"step": "idempotency.hit", "meeting_id": identifier})
            return cached

        result = MeetingResult(meeting_id=identifier)
        result.trace.append({"step": "transcript.accepted", "lines": len(transcript.splitlines())})
        for number, raw_line in enumerate(transcript.splitlines(), start=1):
            line = raw_line.strip()
            lowered = line.lower()
            if lowered.startswith("decision:"):
                result.decisions.append(line.split(":", 1)[1].strip())
                result.trace.append({"step": "decision.extracted", "line": number})
            elif match := ACTION.match(line):
                result.actions.append(
                    ActionItem(
                        match.group("task").strip(),
                        match.group("owner").strip(),
                        match.group("due").strip(),
                    )
                )
                result.trace.append({"step": "action.extracted", "line": number})
            elif lowered.startswith("risk:"):
                result.risks.append(line.split(":", 1)[1].strip())
                result.trace.append({"step": "risk.extracted", "line": number})
            elif lowered.startswith(("probably:", "assume:", "guess:")):
                result.unsupported_claims.append(line)
                result.trace.append({"step": "unsupported.rejected", "line": number})
        result.trace.append({"step": "result.saved", "meeting_id": identifier})
        self._processed[identifier] = result
        return result

