run:
	PYTHONPATH=src python -m main

help:
	PYTHONPATH=src python -m main --help
	
root:
	PYTHONPATH=src python -m main --parallel root

tree:
	PYTHONPATH=src python -m main --parallel tree

profile:
	PYTHONPATH=src python -m main --profile
