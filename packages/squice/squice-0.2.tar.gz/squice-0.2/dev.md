# Create dev environments for both the app and the lib seperately

**Use the appropriate one for the dev work. Keep a seperation in your mind between the scientific library (lib) and the demonstration of it (app).**

# Virtual environments

## STREAMLIT APP
```
python -m venv .env-sq-app
## Load dev environment
source .env-sq-app/bin/activate
(deactivate to exit venv)
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### run app
streamlit run app/home.py

## distribute to streamlit
This will be automatically distributed to streamlit on push to main
https://share.streamlit.io/

## Pypi library
```
python -m venv .env-sq-lib
## Load dev environment
source .env-sq-lib/bin/activate
(deactivate to exit venv)
pip install --upgrade pip
pip install -r requirements_lib.txt --upgrade
```

---

# Debugging

## A python file

## The streamlit app
