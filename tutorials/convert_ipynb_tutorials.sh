#!/bin/sh

## To use this you need to install ``nbconvert`` and ``pandoc``!
python -m nbconvert --RegexRemovePreprocessor.patterns="['^%']" --to python ./tutorials/pyleecan_api.ipynb

python -m isort ./tutorials/pyleecan_api.py
python -m black ./tutorials/pyleecan_api.py
python -m pyupgrade ./tutorials/pyleecan_api.py
