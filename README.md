<!--
Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.

This file is part of PyEMMO
(see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
-->

<!-- This is a comment -->
<!-- This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content. -->

<!-- ![PyEMMO project logo](./doc/images/PyEMMO_Logo.png) -->
<img src="./doc/images/PyEMMO_Logo.png" width="200">

# PyEMMO
_**Py**thon **E**lectrical **M**achine **M**odelling in **O**NELAB_

PyEMMO is a interface for modeling electrical machines in the open-source FEA software [Onelab](https://onelab.info/).
The goal of the project is to automate model creation and the simulation workflow for electrical machines with ONELAB.
<!-- That's why it name stands for **Py**thon **E**lectrical **M**achine **M**odelling in **O**NELAB -->


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyEMMO.

```bash
pip install pyemmo
```

You will need versions of [Gmsh](https://gmsh.info/) and [GetDP](https://getdp.info/) executables. While Gmsh can be directly installed from pip with the Gmsh Python-API, you will need to download GetDP individually.
> [!WARNING]
> Models created with PyEMMO fail with current GetDP version 3.6.0 due to mesh import error!
> You can check your GetDP version wirh  ``getdp --version``

## Usage

The easiest way to start is by using the [Pyleecan](https://github.com/Eomys/pyleecan) project to create a electrical machine instance and feeding it into the PyEMMO-Pyleecan interface.
- Have a look at the [Pyleecan tutorials](https://pyleecan.org/tutorials.html) on how to use Pyleecan. Especially the tutorial on ["How to define a machine"](https://pyleecan.org/01_tuto_Machine.html).
- See the [Pyleecan API tutorial](tutorials/tutorial_pyleecan_api.py) for detailed instructions on how to create a ONELAB model from a Pyleecan machine object.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Setup

After cloning the repository, run the following command to install Git hooks:

```sh
./workingDirectory/install-hooks.sh
```

Or if you are on Windows:

```sh
install-hooks.bat
```

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)

## Run Sphinx to create Documentation

To create or update the documentation you will need to do:

1. Install the doc requirments with: `pip install -r requirements-doc.txt`.
2. Make sure pyemmo is found by either creating a *pyemmo.pth* file in the *site-packages* folder or use `pip install -e .`.
3. To fully build the documentation including the pyleecan api subpackage you need to install pyleecan. Currently we have to use the Github version since the new release is not out yet: `pip install git+https://gitlab.com/Eomys/pyleecan/tree/update-python-version.git`
4. Run Sphinx to build the docs e.g. in html `doc\make.bat html`.
   
You can run `doc\make.bat` plane to see the build options.
Futher information on building the documentation can be found in the [Sphinx documentation](https://www.sphinx-doc.org/en/master/tutorial/index.html).
