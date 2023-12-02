## overview
Learning project for setting up fastapi (and then testing it)

### installation
```dos
pip install fastapi uvicorn pytest pytest-cov pytest-bdd
```

### running
Just as per the docs
```dos
uvicorn main:app --reload --log-config logging.ini --log-level debug
```


http://localhost:8000/docs

### db setup
tbc

### testing
#### unit
Using pytest for unit testing. Fairly minimal mainly for the purpose of
showing how to mock/patch out the database
```dos
pytest -v --cov=main --cov-report=html --junitxml=test-results/junit.xml ./tests/unit
```

#### integration
Generating the skeleton step defs is easy enough to then fill in the blanks and
avoid a bit of typing
```dos
pytest-bdd generate tests/integration/shape.feature
```

```running the tests
pytest -v --junitxml=test-results/junit_int.xml ./tests/integration
pytest -v --junitxml=test-results/junit_int.xml --cucumberjson=test-results/cuke.json ./tests/integration --gherkin-terminal-reporter
```