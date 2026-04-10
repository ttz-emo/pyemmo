#!/bin/sh

## To use this you need to install ``nbconvert`` and ``pandoc``!
python -m nbconvert --RegexRemovePreprocessor.patterns="['^%']" --to python ./tutorials/pyleecan_api.ipynb

python -m isort ./tutorials/pyleecan_api.py
python -m black ./tutorials/pyleecan_api.py
python -m pyupgrade ./tutorials/pyleecan_api.py


python -m nbconvert --RegexRemovePreprocessor.patterns="['^%']" --to python ./tutorials/voltage_source_simulation.ipynb

python -m isort ./tutorials/voltage_source_simulation.py
python -m black ./tutorials/voltage_source_simulation.py
python -m pyupgrade ./tutorials/voltage_source_simulation.py
