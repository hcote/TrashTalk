PYTHON = python3
PYLINT = ./venv/bin/pylint --rcfile=./.pylintrc
TRASHTALK = ./trashtalk/**/*.py
TT_PATH = ./trashtalk/

runserver:
    ${PYTHON} manage.py runserver

lint:
    ${PYLINT} ${TRASHTALK}
