#!/usr/bin/env bash

VENVNAME=marmor_langw6

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate
pip install --upgrade pip

pip install matplotlib
pip install ipython
pip install jupyter
pip install -U pip setuptools wheel
pip install -U spacy
pip install scipy
python -m spacy download en_core_web_sm

python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip install -r requirements.txt
# python -m spacy download en_core_web_sm
# pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz


deactivate
echo "build $VENVNAME"
