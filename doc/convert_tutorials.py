# call jupyter nbconvert on tutorials
from __future__ import annotations

import logging
import os
from os.path import abspath

from pyemmo.definitions import ROOT_DIR

logging.basicConfig()

try:
    from nbconvert import RSTExporter

    logger = logging.getLogger(__name__)
    tutorial_folder = abspath(os.path.join(ROOT_DIR, "tutorials"))
    for infile in os.listdir(tutorial_folder):
        if infile.endswith(".ipynb"):
            logger.info("Creating rst file from tutorial: %s", infile)
            filename = infile.removesuffix(".ipynb")
            tutorial_file = abspath(os.path.join(tutorial_folder, filename + ".ipynb"))
            # jake_notebook = nbformat.reads(tutorial_file, as_version=4)
            rst_exporter = RSTExporter()
            # Convert the notebook to RST format
            (body, resources) = rst_exporter.from_file(tutorial_file)
            out_file = abspath(
                os.path.join("doc", "source", "tutorials", filename + ".rst")
            )
            logger.info("Writing converted tutorial to %s", out_file)
            with open(out_file, "w", encoding="utf-8") as rstFile:
                rstFile.write(body)
except Exception as e:
    raise e
