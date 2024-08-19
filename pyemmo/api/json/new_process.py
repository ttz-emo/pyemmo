import os
import subprocess
from os import mkdir
from os.path import isdir, isfile, join
from typing import Dict, List, Tuple, Union
import logging
import json
import datetime
from ... import logFmt
from ...functions import runOnelab, calcIronLoss, import_results
from ...script.geometry.machineAllType import MachineAllType
from ...script.geometry.rotor import Rotor
from ...script.geometry.stator import Stator
from ...script.script import Script
from ...script.material import ElectricalSteel
from .. import logger
from . import boundaryJSON, importJSON, modelJSON, apiNameDict
from .SurfaceJSON import SurfaceAPI
from .modelJSON import importMachineGeometry

def main(
    geo: Union[str, dict],
    extInfo: Union[str, dict],
    model: Union[str, os.PathLike],
    gmsh: Union[str, os.PathLike] = "",
    getdp: Union[str, os.PathLike] = "",
    results: Union[str, os.PathLike] = "",
):
    # get geometry
    if isinstance(geo, str):
        if isfile(geo):
            # import the segment surface list from the json file
            try:
                with open(geo, encoding="utf-8") as jsonFile:
                    machineGeoList = json.load(jsonFile)
                    # create dict with surface api (segment) objects from the surface list
                    segmentSurfDict = modelJSON.importMachineGeometry(
                        machineGeoList
                    )
            except FileNotFoundError as fnfe:
                raise fnfe
            except Exception as exept:
                raise exept
        else:
            raise (FileNotFoundError(f"Given file path {geo} was not a file."))
    elif isinstance(geo, dict):
        segmentSurfDict = geo
    else:
        raise TypeError(
            f"Geometry file has to be type 'File' or 'dict', not {type(geo)}"
        )
     # addition information
    if isinstance(extInfo, str):
        if isfile(extInfo):
            # import the extended information
            extendedInfo = importJSON.importExtInfo(extInfo)
        else:
            raise (
                FileNotFoundError(f"Given file path {extInfo} was not a file.")
            )
    elif isinstance(extInfo, dict):
        extendedInfo = extInfo
    else:
        raise TypeError(
            f"Model information file has to be type 'File' or 'dict', not {type(extInfo)}"
        )
    
    symFactor = importJSON.getSymFactor(extendedInfo)
    # create the remaining machine surfaces
    maschineSurfDict = modelJSON.createMachineGeometryFromSegment(
        segmentSurfDict, symFactor
    )
    

    
if __name__ == "__main__":
    # importMachineGeometry()
    # main()
    import gmsh
    import sys

    gmsh.initialize()

    gmsh.model.add("TestModel")