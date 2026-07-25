import unittest

from meeting_intelligence import MeetingProcessor


class ProcessorTests(unittest.TestCase):
    def test_extracts_decisions_actions_and_risks(self):
        result = MeetingProcessor().process(
            "Decision: Ship the mock.\nACTION: Test it | owner=Alex | due=Friday\nRisk: Delay."
        )
        self.assertEqual(result.decisions, ["Ship the mock."])
        self.assertEqual(result.actions[0].owner, "Alex")
        self.assertEqual(result.risks, ["Delay."])

    def test_rejects_unsupported_claims(self):
        result = MeetingProcessor().process("Guess: The buyer approved.")
        self.assertEqual(len(result.unsupported_claims), 1)
        self.assertEqual(result.decisions, [])

    def test_is_idempotent(self):
        processor = MeetingProcessor()
        first = processor.process("Decision: Keep the synthetic fixture.")
        second = processor.process("Decision: Keep the synthetic fixture.")
        self.assertEqual(first.meeting_id, second.meeting_id)
        self.assertIn("idempotency.hit", [item["step"] for item in second.trace])

    def test_malformed_action_is_not_invented(self):
        result = MeetingProcessor().process("ACTION: Missing structured fields")
        self.assertEqual(result.actions, [])

    def test_trace_points_to_source_lines(self):
        result = MeetingProcessor().process("\nDecision: Use code-based graders.")
        event = next(item for item in result.trace if item["step"] == "decision.extracted")
        self.assertEqual(event["line"], 2)


if __name__ == "__main__":
    unittest.main()

