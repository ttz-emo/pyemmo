#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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
"""
pytest test-subpackage configuration to skip all pyleecan test cases if not installed
"""
from __future__ import annotations

import importlib.util
import logging
import pathlib

import pytest  # pylint: disable=unused-import

from . import TEST_DIR


def pytest_ignore_collect(collection_path: pathlib.Path, config):
    """Using the pytest_ignore_collect hook to skip all tests in "tests/api/pyleecan"
    and "tests/integrationTest" folders if pyleecan is missing.

    This was taken from:
    https://community.lambdatest.com/t/how-can-i-skip-all-pytest-tests-in-a-directory-if-a-certain-condition-is-met/47397
    """
    logger = logging.getLogger(__name__)
    if not importlib.util.find_spec("pyleecan"):
        # logging.info("Current path is: %s", str(collection_path))
        # Skip tests under a specific folder
        pylcn_test_path = pathlib.PurePath(TEST_DIR) / "api" / "pyleecan"
        if pylcn_test_path in pathlib.PurePath(collection_path).parents:
            logger.debug(
                "Ignoring test path '%s' because pyleecan is missing",
                str(collection_path),
            )
            return True

        # skip integration tests because they are using pyleecan aswell
        integration_test_path = pathlib.PurePath(TEST_DIR) / "integrationTest"
        if integration_test_path in pathlib.PurePath(collection_path).parents:
            logger.debug(
                "Ignoring test path '%s' because pyleecan is missing",
                str(collection_path),
            )
            return True
    return False
