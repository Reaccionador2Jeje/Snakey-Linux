.PHONY: validate test targets doctor

validate:
	python3 tools/validate_targets.py

test:
	python3 -m unittest discover -s tests -v

targets:
	python3 tools/snakey.py targets

doctor:
	python3 tools/snakey.py doctor
