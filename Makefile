.PHONY: demo test eval validate
demo:
	PYTHONPATH=src python3 -m meeting_intelligence.demo
test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v
eval:
	PYTHONPATH=src python3 evals/run.py
validate:
	PYTHONPATH=src python3 scripts/validate_metadata.py

