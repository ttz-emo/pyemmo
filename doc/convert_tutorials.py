# call jupyter nbconvert on tutorials
from os.path import abspath
try:
    from nbconvert import RSTExporter

    # import nbformat

    tutorial_file = abspath(r"tutorials/pyleecan_api.ipynb")
    # jake_notebook = nbformat.reads(tutorial_file, as_version=4)
    rst_exporter = RSTExporter()
    # Convert the notebook to RST format
    (body, resources) = rst_exporter.from_file(tutorial_file)
    out_file = abspath(r"doc/source/tutorials/pyleecan_api.rst")
    with open(out_file, "w", encoding="utf-8") as rstFile:
        rstFile.write(body)
except ImportError:
    pass
