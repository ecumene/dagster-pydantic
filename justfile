install:
  poetry config virtualenvs.in-project true
  poetry install

shell:
  poetry shell

tests:
  pytest
