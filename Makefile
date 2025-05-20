run:
	PYTHONPATH=src python -m main

root:
	PYTHONPATH=src python -m main --parallel root

tree:
	PYTHONPATH=src python -m main --parallel tree

profile:
	PYTHONPATH=src python -m main --profile
