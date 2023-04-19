"""This module defines the functions to calculate
the iron losses from getdp b-field simulation results."""

from typing import List, Union, Dict, Tuple
import sys
import os
import gmsh
import numpy as np

# from matplotlib import pyplot as plt
from .importResults import importPos
from ..script.material import ElectricalSteel


def main(
    bFilePath: os.PathLike, lossFactor: dict, symFactor: int, axialLength: float = 1.0
) -> Tuple[Dict[str, np.ndarray], List[float]]:
    ironLoss = {}  # dict for loss results
    finGmsh = False  # determine if gmsh should be closed at the end
    if not gmsh.isInitialized():
        gmsh.initialize()
        finGmsh = True

    elementTags, time, bFieldData = importPos(bFilePath)
    nbrTimeSteps = len(time)

    # init derivative of B
    dBdt = np.zeros((nbrTimeSteps - 1, bFieldData.shape[1], bFieldData.shape[2]))

    # loop through time step and find element wise min/max
    bmin = bmax = bFieldData[0]  # init bmin and bmax array with first time step
    for step in range(1, nbrTimeSteps):
        bmax = np.maximum(bmax, bFieldData[step])
        bmin = np.minimum(bmin, bFieldData[step])
        dBdt[step - 1] = (bFieldData[step] - bFieldData[step - 1]) / (
            time[step] - time[step - 1]
        )

    ## calculate hysteresis losses
    hystLossFactor = lossFactor["hyst"]  # hysteresis loss factor
    # beta = 2  # hysteresis loss exponent

    magB = (bmax - bmin) / 2  # magnitude of B
    magH = 1 / np.pi * hystLossFactor * magB  # magnitude of H
    hystLossField = np.abs(magH[:, 0] * dBdt[:, :, 0]) + np.abs(
        magH[:, 1] * dBdt[:, :, 1]
    )
    # mean iron loss per element over all timesteps
    # meanHystLossField = np.mean(hystLossField, axis=0)
    time = time[0:-1]
    hystLoss = integrateField(np.array(hystLossField), time, elementTags)
    assert (
        hystLoss.size == nbrTimeSteps
    ), f"Integration should result in {nbrTimeSteps} values!"
    # skip first value, because its 0:
    hystLoss = hystLoss[1:] * symFactor * axialLength  # correct values
    ironLoss["hyst"] = hystLoss

    ## Calculate eddy current losses
    eddyLossFactor = lossFactor["eddy"]  # loss parameter
    # loss function for eddy current loss from paper:
    pi2 = np.square(np.pi)
    eddyLossField = (
        eddyLossFactor
        / (2 * pi2)
        * (np.square(dBdt[:, :, 0]) + np.square(dBdt[:, :, 1]))
    )
    # meanEddyLossField = np.mean(eddyLossField, axis=0)
    # eddyLoss = integrateField(np.array([meanEddyLossField]), [time[0]], elementTags)
    eddyLoss = integrateField(np.array(eddyLossField), time, elementTags)
    assert (
        eddyLoss.size == nbrTimeSteps
    ), f"Integration should result in {nbrTimeSteps} values!"
    # skip first value, because its 0:
    eddyLoss = eddyLoss[1:] * symFactor * axialLength  # correct values
    ironLoss["eddy"] = eddyLoss

    ## calculate excess loss
    excLossFactor = lossFactor["exc"]
    constExcFactor = 8.763363  # constant factor (from paper)
    excLossField = (
        excLossFactor
        / constExcFactor
        * np.power((np.square(dBdt[:, :, 0]) + np.square(dBdt[:, :, 1])), 0.75)
    )
    # meanExcLossField = np.mean(excLossField, axis=0)
    # excLoss = integrateField(np.array([meanExcLossField]), [time[0]], elementTags)
    excLoss = integrateField(np.array(excLossField), time, elementTags)
    assert (
        excLoss.size == nbrTimeSteps
    ), f"Integration should result in {nbrTimeSteps} values!"
    # skip first value, because its 0:
    excLoss = excLoss[1:] * symFactor * axialLength  # correct values
    ironLoss["exc"] = excLoss

    if finGmsh:
        gmsh.finalize()

    return ironLoss, time


def integrateField(
    fieldData: np.ndarray,
    time: List[float],
    elemTags: List[int],
    meshFile: os.PathLike = "",
):
    finGmsh = False
    if not gmsh.isInitialized():
        gmsh.initialize()
        finGmsh = True

    try:
        if meshFile:
            gmsh.open(meshFile)
        model = gmsh.model.getCurrent()
        viewTag = gmsh.view.add("FieldToIntegrate")
        for step, timeVal in enumerate(time):
            gmsh.view.addHomogeneousModelData(
                tag=viewTag,
                step=step + 1,  # steps must start a 1...
                modelName=model,
                dataType="ElementData",
                tags=elemTags,
                data=fieldData[step, :],
                time=timeVal,
            )
        # integrate:
        gmsh.plugin.setNumber("Integrate", "View", gmsh.view.getIndex(viewTag))
        integratedView = gmsh.plugin.run("Integrate")
        _, _, integratedData = gmsh.view.getListData(integratedView)
        # dataType is allways SP after integration
        # number of elements after integration should be 1
    except Exception as exce:
        gmsh.finalize()
        raise exce
    if finGmsh:
        gmsh.finalize()
    # only return data values (skip SP coordinates)
    return integratedData[0][3:]


def writeSimple(fName, time: List[float], data: Union[np.ndarray, List]) -> None:
    """_summary_

    Args:
        fName (_type_): _description_
        time (List[float]): _description_
        data (Union[np.ndarray, List]): _description_
    """
    nbrTimeSteps = len(time)
    if isinstance(data, np.ndarray):
        assert np.any(np.equal(data.shape, nbrTimeSteps))
    elif isinstance(data, list):
        assert len(data) == nbrTimeSteps
    else:
        raise TypeError(f"Data type was not numpy.ndarray or list, but {type(data)}.")
    with open(fName, "w", encoding="utf-8") as resFile:
        for varStep in range(nbrTimeSteps):
            resFile.write(f"{time[varStep]} {data[varStep]}\n")


def adaptIronLossParams(
    lossParams: List[float], steelMat: ElectricalSteel
) -> List[float]:
    assert len(lossParams) == 3, "Number of loss parameters should be 3!"
    assert isinstance(steelMat, ElectricalSteel), "Material should be steel"
    freq = steelMat.referenceFrequency  # frequency in Hz
    ind = steelMat.referenceFluxDensity  # induction in T
    dens = steelMat.getDensity()  # density in kg/m³
    lossParams[0] = lossParams[0] * dens / freq / (ind**2)
    lossParams[1] = lossParams[1] * dens / ((freq * ind) ** 2)
    lossParams[2] = lossParams[2] * dens / ((freq * ind) ** 1.5)
    # return lossParams
