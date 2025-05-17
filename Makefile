run:
	PYTHONPATH=src python -m main

root:
	PYTHONPATH=src python -m main --parallel root --workers 4

profile:
	PYTHONPATH=src python -m main --profile
