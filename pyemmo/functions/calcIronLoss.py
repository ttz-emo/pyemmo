"""This module defines the functions to calculate
the iron losses from getdp b-field simulation results."""

from typing import List, Union, Dict, Tuple
import os
import gmsh
import numpy as np

# from matplotlib import pyplot as plt
from .importResults import importPos
from ..script.material import ElectricalSteel


def main(
    bFilePath: os.PathLike, lossFactor: dict, symFactor: int, axialLength: float = 1.0
) -> Tuple[Dict[str, np.ndarray], List[float]]:
    ironLoss, time = calcTimeDomainIronLosses(
        bFilePath, lossFactor, symFactor, axialLength
    )
    return ironLoss, time


def calcTimeDomainIronLosses(
    bFilePath: os.PathLike, lossFactor: dict, symFactor: int, axialLength: float = 1.0
) -> Tuple[Dict[str, np.ndarray], List[float]]:
    ironLoss = {}  # dict for loss results
    finGmsh = False  # determine if gmsh should be closed at the end
    if not gmsh.isInitialized():
        gmsh.initialize()
        finGmsh = True

    elementTags, time, bFieldData = importPos(bFilePath)
    nbrTimeSteps = len(time)
    nbrElements = len(elementTags)

    # --------------------------- calc hysteresis loss ---------------------------
    if np.all(
        np.linalg.norm((bFieldData[0] - bFieldData[-1]), axis=(1))
        < np.linalg.norm(bFieldData, axis=(2, 0)) * 1e-3
    ):
        # value of last time step is nearly equal to first time step
        # -> skip last time step!
        bFieldDataFFT = bFieldData[:-1, :, :]
    else:
        bFieldDataFFT = bFieldData
    # calculate element wise fft of b-field:
    bfft = np.fft.rfft(bFieldDataFFT, axis=0)
    amp = np.abs(bfft)
    # to get correct amplitude regarding the specific frequencies, the amplitudes
    # must be corrected by 1/nbrFreqs and DC-part by 1/(2*nbrFreqs) because its value
    # is doubled since its part of the positive and negative side of the spectrum.
    # Since I defined the number of frequencies to be only for the one sided spectrum,
    # we have to double the value for amp[0] and use only nbrFreqs for amp[1:]
    tStep = time[1] - time[0]
    freqs = np.fft.rfftfreq(np.shape(bFieldDataFFT)[0], tStep)
    nbrFreqs = len(freqs)
    amp = np.concatenate(([amp[0] / nbrFreqs / 2], amp[1:] / (nbrFreqs)), axis=0)
    phase = np.angle(bfft)
    for elem in range(nbrElements):
        # FIXME: Assume that freq. of max. amplitude is the same for x and y comp.
        #   -> norm                                         +1 because skipping DC
        fMaxInd = np.linalg.norm(amp[1:, elem, :], axis=1).argmax() + 1
        phi0 = phase[fMaxInd, :, :]

    # fMaxIndex equals order of that spectral part
    phi = np.linspace(
        phi0 + np.pi / 2, fMaxInd * (2 * np.pi) + phi0 + np.pi / 2, nbrTimeSteps - 1
    )
    cosPhi = np.cos(phi)  # calc cos(phi)
    bmax = np.max(bFieldData, axis=0)
    bmin = np.min(bFieldData, axis=0)
    Bm = (bmax - bmin) / 2  # magnitude is (max-min)/2

    Hm = lossFactor["hyst"] / np.pi * Bm  # magnitude of H according to paper
    Hirr = Hm * cosPhi
    dBdt = np.diff(bFieldData, axis=0) / tStep
    hystLossField = np.sum(Hirr * dBdt, axis=2)

    # model = gmsh.model.getCurrent()  # or just get current model...
    # pHFreqView = gmsh.view.add("Hystersis Loss (FFT) [W/m³]")  # get tag of new view
    # gmsh.view.addHomogeneousModelData(
    #     tag=pHFreqView,
    #     step=0,
    #     modelName=model,
    #     dataType="ElementData",
    #     tags=elementTags,
    #     data=np.sum(phFreq, axis=1),
    #     time=0,
    # )

    hystLoss = integrateField(hystLossField, time[1:], elementTags)
    # skip first value, because its 0:
    ironLoss["hyst"] = hystLoss[1:] * symFactor * axialLength  # correct values

    # ------------------------- Calculate eddy current losses ---------------------------
    eddyLossFactor = lossFactor["eddy"]  # loss parameter
    # loss function for eddy current loss from paper:
    eddyLossField = np.sum(eddyLossFactor / 2 / (np.pi**2) * (dBdt**2), axis=2)
    # meanEddyLossField = np.mean(eddyLossField, axis=0)
    # eddyLoss = integrateField(np.array([meanEddyLossField]), [time[0]], elementTags)

    eddyLoss = integrateField(np.array(eddyLossField), time[1:], elementTags)
    assert (
        eddyLoss.size == nbrTimeSteps
    ), f"Integration should result in {nbrTimeSteps} values!"
    # skip first value, because its 0:
    eddyLoss = eddyLoss[1:] * symFactor * axialLength  # correct values
    ironLoss["eddy"] = eddyLoss

    # --------------------------- calculate excess loss ---------------------------
    if lossFactor["exc"] > 0:
        constExcFactor = 8.763363  # constant factor (from paper)
        excLossField = np.sum(
            lossFactor["exc"] / constExcFactor * np.power(dBdt**2, 0.75), axis=2
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
    else:
        # set iron loss to 0
        ironLoss["exc"] = np.zeros(eddyLoss.shape)

    if finGmsh:
        gmsh.finalize()

    return ironLoss, time[0:-1]


def calcFreqDomainIronLosses(
    bFilePath: os.PathLike, lossFactor: dict, symFactor: int, axialLength: float = 1.0
) -> Tuple[Dict[str, np.ndarray], List[float]]:
    ironLoss = {}  # dict for loss results
    finGmsh = False  # determine if gmsh should be closed at the end
    if not gmsh.isInitialized():
        gmsh.initialize()
        finGmsh = True

    elementTags, time, bFieldData = importPos(bFilePath)
    ## calculate hysteresis losses
    hystLossFactor = lossFactor["hyst"]  # hysteresis loss factor
    # beta = 2  # hysteresis loss exponent
    # calculate element wise fft of b-field
    if np.all(
        np.linalg.norm((bFieldData[0] - bFieldData[-1]), axis=(1))
        < np.linalg.norm(bFieldData, axis=(2, 0)) * 1e-3
    ):
        # value of last time step is nearly equal to first time step
        # -> skip last time step!
        bFieldData = bFieldData[:-1, :, :]
        time = time[:-1]
    tStep = time[1] - time[0]
    nbrTimeSteps = len(time)
    amp = np.abs(np.fft.rfft(bFieldData[:, :, :], axis=0))
    # to get correct amplitude regarding the specific frequencies, the amplitudes
    # must be corrected by 1/nbrFreqs and DC-part by 1/(2*nbrFreqs) because its value
    # is doubled since its part of the positive and negative side of the spectrum.
    # Since I defined the number of frequencies to be only for the one sided spectrum,
    # we have to double the value for amp[0] and use only nbrFreqs for amp[1:]
    freqs = np.fft.rfftfreq(nbrTimeSteps, tStep)
    nbrFreqs = len(freqs)
    amp = np.concatenate(([amp[0] / nbrFreqs / 2], amp[1:] / (nbrFreqs)), axis=0)
    # norm of xyz comp. -> hystLossField has shape (nbrElements, nbrFreqs)
    hystLossField = np.linalg.norm(
        hystLossFactor * freqs * (amp.transpose() ** 2), axis=0
    )
    hystLoss = integrateField(hystLossField.transpose(), freqs, elementTags)[1:]
    # skip first value, because its 0
    ironLoss["hyst"] = hystLoss * symFactor * axialLength  # correct values

    # ------------------------- Calculate eddy current losses -------------------------
    eddyLossFactor = lossFactor["eddy"]  # loss parameter
    # loss function for eddy current loss from paper:
    eddyLossField = np.linalg.norm(
        eddyLossFactor * (freqs**2) * (amp.transpose() ** 2), axis=0
    )
    eddyLoss = integrateField(eddyLossField.transpose(), freqs, elementTags)[1:]
    assert eddyLoss.size == nbrFreqs, f"Integration should result in {nbrFreqs} values!"
    # skip first value, because its 0
    eddyLoss = eddyLoss * symFactor * axialLength  # correct values
    ironLoss["eddy"] = eddyLoss

    ## calculate excess loss
    excLossFactor = lossFactor["exc"]
    if excLossFactor:
        constExcFactor = 8.763363  # constant factor (from paper)
        excLossField = np.linalg.norm(
            excLossFactor * (freqs**1.5) * (amp.transpose() ** 1.5)
        )
        excLoss = integrateField(excLossField.transpose(), freqs, elementTags)[1:]
        assert (
            excLoss.size == nbrFreqs
        ), f"Integration should result in {nbrFreqs} values!"
        # skip first value, because its 0:
        excLoss = excLoss * symFactor * axialLength  # correct values
        ironLoss["exc"] = excLoss
    else:
        ironLoss["exc"] = np.zeros(eddyLoss.shape)

    if finGmsh:
        gmsh.finalize()

    return ironLoss, freqs


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
    originVerbose = gmsh.option.getNumber("General.Verbosity")
    gmsh.option.setNumber("General.Verbosity", 1)

    try:
        if meshFile:
            gmsh.open(meshFile)
        model = gmsh.model.getCurrent()
        viewTag = gmsh.view.add("FieldToIntegrate")
        for step, timeVal in enumerate(time):
            gmsh.view.addHomogeneousModelData(
                tag=viewTag,
                step=step + 1,  # steps must start at 1...
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
        # set original verbosity after integration
        gmsh.option.setNumber("General.Verbosity", originVerbose)
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
