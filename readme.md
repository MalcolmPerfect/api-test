## overview
Learning project for setting up fastapi (and then testing it)

### installation
```dos
pip install fastapi uvicorn pytest pytest-cov
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
pytest -v --cov=main --cov-report=html
```

#### integration
