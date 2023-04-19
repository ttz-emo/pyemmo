try:
    import setuptools
except ImportError:  # Install setuptools if needed
    from os import system
    from sys import executable

    # run 'pip install setuptools'
    system(f"{executable} -m pip install setuptools")

    import setuptools


# /!\ Increase the number before a release
# See https://www.python.org/dev/peps/pep-0440/
# Examples :
# First alpha of the release 0.1.0 : 0.1.0a1
# First beta of the release 1.0.0 : 1.0.0b1
# Second release candidate of the release 2.6.4 : 2.6.4rc2
# Release 1.1.0 : 1.1.0
# First post release of the release 1.1.0 : 1.1.0.post1

# get version from version.py file in package,
#  because we need to access the version number from pydraft.script
with open("pydraft/version.py", encoding="utf-8") as versionFile:
    exec(versionFile.read())
# from .pydraft.version import __version__
PYDRAFT_VERSION = __version__ # # pylint: disable=locally-disabled, undefined-variable

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PYTHON_REQUIRES = ">= 3.6"

# Pyleecan dependancies
install_requires = [
    "setuptools",
    "matplotlib>=3.4.3",
    "numpy>=1.23.1",
    "pandas>=1.2.4",
    "parse>=1.19.0",
    "gmsh>=4.8.4",
    "pygetdp>=1.0.0",
    "swat-em>=0.6.3",
    # "scipy>=1.6.3", # only used for mat file import
]

setuptools.setup(
    name="pydraft",
    version=PYDRAFT_VERSION,
    author="AG-EM TTZ-EMO",
    author_email="max.ganser@fhws.de",
    description="PyDraft is a interface for the open-source FEM software Onelab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude=[r"\tests*", r"\workingDirectory*", r"\.vscode*", r"\egg-info*"]
    ),
    # package data only works with binary packages!!!
    #   see -> https://stackoverflow.com/questions/7522250
    package_data={},
    include_package_data=True,
    # data_files=[
    #     ("", ["pydraft/script/default_color_dict.json"]),
    #     (
    #         "",
    #         [
    #             "pydraft/script/material/Material_new.db",
    #             "pydraft/script/material/Material_old.db",
    #         ],
    #     ),
    # ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ::Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=PYTHON_REQUIRES,
    install_requires=install_requires,
)