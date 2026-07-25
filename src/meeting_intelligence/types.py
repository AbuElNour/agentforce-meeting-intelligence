from dataclasses import dataclass, field


@dataclass(frozen=True)
class ActionItem:
    task: str
    owner: str
    due: str


@dataclass
class MeetingResult:
    meeting_id: str
    decisions: list[str] = field(default_factory=list)
    actions: list[ActionItem] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    unsupported_claims: list[str] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)

