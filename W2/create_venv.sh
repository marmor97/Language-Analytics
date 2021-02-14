#!/usr/bin/env bash

VENVNAME = marmor_lang

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate
pip install --upgrade pip

pip3 install ipython
pip3 install jupyter

python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip3 install -r requirements.txt

deactivate
echo "build $VENVNAME"
