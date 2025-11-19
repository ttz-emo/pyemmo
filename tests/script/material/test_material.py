#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import annotations

import numpy as np
import pytest

from pyemmo.script.material.material import Material


def test_material_init_defaults():
    m = Material(name="")
    assert m.name == ""
    assert m.conductivity == 0.0
    assert m.relPermeability == 1.0
    assert m.remanence == 0.0
    assert m.tempCoefRem == 0.0
    assert m.density == 0.0
    assert isinstance(m.BH, np.ndarray)
    assert m.BH.size == 0
    assert m.linear is True
    assert m.thermalConductivity == 0.0
    assert m.thermalCapacity == 0.0


def test_material_name_setter_and_getter():
    m = Material(name="Steel")
    m.name = "Steel"
    assert m.name == "Steel"
    with pytest.raises(ValueError):
        m.name = 123


def test_conductivity_setter():
    m = Material(name="Steel")
    m.conductivity = 5.0
    assert m.conductivity == 5.0
    m.conductivity = 0
    assert m.conductivity == 0
    with pytest.raises(TypeError):
        m.conductivity = "bad"
    with pytest.raises(TypeError):
        m.conductivity = None


def test_relPermeability_setter():
    m = Material(name="Steel")
    m.relPermeability = 1000
    assert m.relPermeability == 1000
    with pytest.raises(ValueError):
        m.relPermeability = "bad"


def test_remanence_setter():
    m = Material(name="Steel")
    m.remanence = 1.2
    assert m.remanence == 1.2
    with pytest.raises(ValueError):
        m.remanence = "bad"


def test_tempCoefRem_setter():
    m = Material(name="Steel")
    m.tempCoefRem = 0.01
    assert m.tempCoefRem == 0.01
    with pytest.raises(ValueError):
        m.tempCoefRem = "bad"


def test_density_setter():
    m = Material(name="Steel")
    m.density = 7800
    assert m.density == 7800
    with pytest.raises(TypeError):
        m.density = "bad"
    with pytest.raises(Exception):
        m.density = -1


def test_thermalConductivity_setter():
    m = Material(name="Steel")
    m.thermalConductivity = 50
    assert m.thermalConductivity == 50
    with pytest.raises(TypeError):
        m.thermalConductivity = "bad"
    with pytest.raises(Exception):
        m.thermalConductivity = -1


def test_thermalCapacity_setter():
    m = Material(name="Steel")
    m.thermalCapacity = 500
    assert m.thermalCapacity == 500
    with pytest.raises(TypeError):
        m.thermalCapacity = "bad"
    with pytest.raises(Exception):
        m.thermalCapacity = -1


def test_linear_property():
    m = Material(name="Steel")
    m.linear = True
    assert m.linear is True
    m.linear = False
    assert m.linear is False
    with pytest.raises(ValueError):
        m.linear = "bad"


def test_BH_setter_and_getter():
    m = Material(name="Steel")
    arr = np.array([[0, 0.0], [1.0, 1]])
    m.BH = arr
    np.testing.assert_array_equal(m.BH, arr)
    # Should set linear to False
    assert m.linear is False


def test_set_BH_with_list():
    m = Material(name="Steel")
    bh_list = [[0, 0], [1, 1]]
    m.set_BH(bh_list)
    np.testing.assert_array_equal(m.BH, np.array(bh_list))


def test_set_BH_without_origin():
    m = Material(name="Steel")
    arr = np.array([[1.0, 1], [2, 2], [2.2, 300]])
    m.BH = arr
    exp_arr = np.array([[0, 0], [1.0, 1], [2, 2], [2.2, 300]])
    np.testing.assert_array_equal(m.BH, exp_arr)
    # Should set linear to False
    assert m.linear is False


def test_str_and_print(capsys):
    m = Material(
        name="Test",
        conductivity=1.0,
        relPermeability=2.0,
        remanence=0.5,
        density=1000,
        thermalConductivity=10,
        thermalCapacity=100,
    )
    s = str(m)
    assert "Remanence Flux Density[T]: 0.5" in s
    m.print()
    captured = capsys.readouterr()
    assert "Remanence Flux Density[T]: 0.5" in captured.out
    m.remanence = 1.5
    print(m)
    captured = capsys.readouterr()
    assert "Remanence Flux Density[T]: 1.5" in captured.out
