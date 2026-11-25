.PHONY: validate test targets doctor boot-plans

validate:
	python3 tools/validate_targets.py

test:
	python3 -m unittest discover -s tests -v

targets:
	python3 tools/snakey.py targets

doctor:
	python3 tools/snakey.py doctor

boot-plans:
	python3 tools/snakey.py boot-plan --target game-boy
	python3 tools/snakey.py boot-plan --target nintendo-ds
