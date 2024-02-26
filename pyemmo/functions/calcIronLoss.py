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
    bFilePath: os.PathLike,
    lossFactor: dict,
    symFactor: int,
    axialLength: float = 1.0,
) -> Tuple[Dict[str, np.ndarray], List[float]]:
    ironLoss, time = calcTimeDomainIronLosses(
        bFilePath, lossFactor, symFactor, axialLength
    )
    return ironLoss, time


def calcTimeDomainIronLosses(
    bFilePath: os.PathLike,
    lossFactor: dict,
    symFactor: int,
    axialLength: float = 1.0,
    saveFields: bool = True,
) -> Tuple[Dict[str, np.ndarray], List[float]]:
    """TODO: _summary_

    Args:
        bFilePath (os.PathLike): _description_
        lossFactor (dict): _description_
        symFactor (int): _description_
        axialLength (float, optional): _description_. Defaults to 1.0.
        saveFields (bool, optional): _description_. Defaults to True.

    Returns:
        Tuple[Dict[str, np.ndarray], List[float]]: Iron loss results-dict + time array
    """
    ironLoss = {}  # dict for loss results
    finGmsh = False  # determine if gmsh should be closed at the end
    if not gmsh.isInitialized():
        gmsh.initialize()
        finGmsh = True

    elementTags, time, bFieldData = importPos(bFilePath)
    nbrTimeSteps = len(time)
    if saveFields:
        # extract filename from path
        _, fileName = os.path.split(bFilePath)  # get filename with ext
        fileName, _ = os.path.splitext(fileName)  # get pure filename
    hystLossField = calcHystLossUCP(time, bFieldData, lossFactor["hyst"])
    if saveFields:
        # save the View to a pos file
        model = gmsh.model.getCurrent()  # or just get current model...
        actView = gmsh.view.add(
            f"Hystersis Loss [W/m³] ({fileName})"
        )  # get tag of new view
        for step in range(len(time) - 1):
            gmsh.view.addHomogeneousModelData(
                tag=actView,
                step=step + 1,
                modelName=model,
                dataType="ElementData",
                tags=elementTags,
                data=hystLossField[step, :],
                time=time[step],
            )
        # save p_hyst-field to file:
        pFilePath = os.path.join(
            os.path.dirname(bFilePath), f"p_hyst_from_{fileName}.pos"
        )
        gmsh.view.write(actView, pFilePath)
    # integrate field over area for each time step
    hystLoss = integrateField(hystLossField, time[1:], elementTags)
    # skip first value, because its 0:
    ironLoss["hyst"] = hystLoss[1:] * symFactor * axialLength  # correct values

    # ------------------------- Calculate eddy current losses ---------------------------
    eddyLossFactor = lossFactor["eddy"]  # loss parameter
    # loss function for eddy current loss from paper:
    tStep = time[1] - time[0]
    dBdt = np.diff(bFieldData, axis=0) / tStep  # calc dBdt
    eddyLossField = np.sum(eddyLossFactor / 2 / (np.pi**2) * (dBdt**2), axis=2)
    # meanEddyLossField = np.mean(eddyLossField, axis=0)
    # eddyLoss = integrateField(np.array([meanEddyLossField]), [time[0]], elementTags)
    if saveFields:
        # save the View to a pos file
        model = gmsh.model.getCurrent()  # or just get current model...
        actView = gmsh.view.add(f"Eddy current Loss [W/m³] ({fileName})")
        for step in range(len(time) - 1):
            gmsh.view.addHomogeneousModelData(
                tag=actView,
                step=step + 1,
                modelName=model,
                dataType="ElementData",
                tags=elementTags,
                data=eddyLossField[step, :],
                time=time[step],
            )
        # save p_hyst-field to file:
        pFilePath = os.path.join(
            os.path.dirname(bFilePath), f"p_eddy_from_{fileName}.pos"
        )
        gmsh.view.write(actView, pFilePath)
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
            lossFactor["exc"] / constExcFactor * np.power(dBdt**2, 0.75),
            axis=2,
        )
        if saveFields:
            # save the View to a pos file
            model = gmsh.model.getCurrent()  # or just get current model...
            actView = gmsh.view.add(f"Excess Loss [W/m³] ({fileName})")
            for step in range(len(time) - 1):
                gmsh.view.addHomogeneousModelData(
                    tag=actView,
                    step=step + 1,
                    modelName=model,
                    dataType="ElementData",
                    tags=elementTags,
                    data=excLossField[step, :],
                    time=time[step],
                )
            # save p_hyst-field to file:
            pFilePath = os.path.join(
                os.path.dirname(bFilePath), f"p_exc_from_{fileName}.pos"
            )
            gmsh.view.write(actView, pFilePath)
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
        excLossField = np.zeros(eddyLossField.shape)

    # Export total loss field
    if saveFields:
        # save the View to a pos file
        model = gmsh.model.getCurrent()
        actView = gmsh.view.add(f"Total Loss [W/m³] ({fileName})")
        totalLossField = hystLossField + eddyLossField + excLossField
        for step in range(len(time) - 1):
            gmsh.view.addHomogeneousModelData(
                tag=actView,
                step=step + 1,
                modelName=model,
                dataType="ElementData",
                tags=elementTags,
                data=totalLossField[step, :],
                time=time[step],
            )
        # save p_hyst-field to file:
        pFilePath = os.path.join(
            os.path.dirname(bFilePath), f"p_core_from_{fileName}.pos"
        )
        gmsh.view.write(actView, pFilePath)

    if finGmsh:
        gmsh.finalize()

    return ironLoss, time[0:-1]


def calcFreqDomainIronLosses(
    bFilePath: os.PathLike,
    lossFactor: dict,
    symFactor: int,
    axialLength: float = 1.0,
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
    amp = np.concatenate(
        ([amp[0] / nbrFreqs / 2], amp[1:] / (nbrFreqs)), axis=0
    )
    # norm of xyz comp. -> hystLossField has shape (nbrElements, nbrFreqs)
    hystLossField = np.linalg.norm(
        hystLossFactor * freqs * (amp.transpose() ** 2), axis=0
    )
    hystLoss = integrateField(hystLossField.transpose(), freqs, elementTags)[
        1:
    ]
    # skip first value, because its 0
    ironLoss["hyst"] = hystLoss * symFactor * axialLength  # correct values

    # ------------------------- Calculate eddy current losses -------------------------
    eddyLossFactor = lossFactor["eddy"]  # loss parameter
    # loss function for eddy current loss from paper:
    eddyLossField = np.linalg.norm(
        eddyLossFactor * (freqs**2) * (amp.transpose() ** 2), axis=0
    )
    eddyLoss = integrateField(eddyLossField.transpose(), freqs, elementTags)[
        1:
    ]
    assert (
        eddyLoss.size == nbrFreqs
    ), f"Integration should result in {nbrFreqs} values!"
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
        excLoss = integrateField(excLossField.transpose(), freqs, elementTags)[
            1:
        ]
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


def calcHystLossUCP(
    time: list[float], bFieldData: np.ndarray, hystLossFactor: float
) -> np.ndarray:
    """Calculate the hysteresis loss field according to ANSYS Maxwell User-
    Controll-Program"""
    nbrElements = bFieldData.shape[1]
    nbrTimeSteps = len(time)
    tStep = time[1] - time[0]
    dBdt = np.diff(bFieldData, axis=0) / tStep  # calc dBdt
    uex = np.zeros((nbrTimeSteps, nbrElements, 2))
    Hm = np.zeros((nbrTimeSteps, nbrElements, 2))
    H = np.zeros((nbrTimeSteps, nbrElements, 2))
    for it in range(1, nbrTimeSteps):
        # for each timestep
        for ie in range(nbrElements):
            # for each element
            for comp in (0, 1):
                # for x,y, and not z
                B_new = bFieldData[it, ie, comp]
                B_old = bFieldData[it - 1, ie, comp]
                find_ext(it, ie, comp, B_old, B_new, uex)
                # calc Hm
                Hm[it, ie, comp] = hystLossFactor / np.pi * uex[it, ie, comp]
                if uex[it, ie, comp] == 0:
                    H[it, ie, comp] = np.sqrt(Hm[it, ie, comp] ** 2)
                else:
                    H[it, ie, comp] = np.sqrt(
                        np.abs(
                            Hm[it, ie, comp] ** 2
                            - (
                                Hm[it, ie, comp]
                                * bFieldData[it, ie, comp]
                                / uex[it, ie, comp]
                            )
                            ** 2
                        )
                    )
    # sum of x and y; abs of value (x,y)
    hystLossField = np.sum(np.abs(H[1:, :, :] * dBdt[:, :, 0:1]), axis=2)
    return hystLossField


def find_ext(i_time, i_elem, i_comp, b_old, b_new, uex):
    if (b_new < b_old) and (b_old > uex[i_time - 1, i_elem, i_comp]):
        uex[i_time, i_elem, i_comp] = b_old
    elif (b_new > b_old) and (b_old < uex[i_time - 1, i_elem, i_comp]):
        uex[i_time, i_elem, i_comp] = b_old
    else:
        uex[i_time, i_elem, i_comp] = uex[i_time - 1, i_elem, i_comp]


def calc_Hm(bFieldData: np.ndarray, time: list[float], hystLossFactor):
    nbrElements = bFieldData.shape[1]
    nbrTimeSteps = len(time)
    uex = np.zeros((nbrTimeSteps, nbrElements, 2))
    Hm = np.zeros((nbrTimeSteps, nbrElements, 2))
    H = np.zeros((nbrTimeSteps, nbrElements, 2))
    for it in range(1, nbrTimeSteps):
        # for each timestep
        for ie in range(nbrElements):
            # for each element
            for comp in (0, 1):
                # for x,y, and not z
                B_new = bFieldData[it, ie, comp]
                B_old = bFieldData[it - 1, ie, comp]
                find_ext(it, ie, comp, B_old, B_new, uex)
                # calc Hm
                Hm[it, ie, comp] = hystLossFactor / np.pi * uex[it, ie, comp]
                if uex[it, ie, comp] == 0:
                    H[it, ie, comp] = np.sqrt(Hm[it, ie, comp] ** 2)
                else:
                    H[it, ie, comp] = np.sqrt(
                        np.abs(
                            Hm[it, ie, comp] ** 2
                            - (
                                Hm[it, ie, comp]
                                * bFieldData[it, ie, comp]
                                / uex[it, ie, comp]
                            )
                            ** 2
                        )
                    )


def calcHystLossSin(
    time: list[float], bFieldData: np.ndarray, hystLossFactor: float
) -> np.ndarray:
    """Calculate the hysteresis loss field by using the cosine of the
    fundamental B field wave"""
    nbrElements = bFieldData.shape[1]
    nbrTimeSteps = len(time)
    if np.all(
        np.linalg.norm((bFieldData[0] - bFieldData[-1]), axis=1)
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
    amp = np.concatenate(
        ([amp[0] / nbrFreqs / 2], amp[1:] / (nbrFreqs)), axis=0
    )
    phase = np.angle(bfft)
    for elem in range(nbrElements):
        # FIXME: Assume that freq. of max. amplitude is the same for x and y comp.
        #   -> norm                                         +1 because skipping DC
        fMaxInd = np.linalg.norm(amp[1:, elem, :], axis=1).argmax() + 1
        phi0 = phase[fMaxInd, :, :]

    # fMaxIndex equals order of that spectral part
    phi = np.linspace(
        phi0 + np.pi / 2,
        fMaxInd * (2 * np.pi) + phi0 + np.pi / 2,
        nbrTimeSteps - 1,
    )
    cosPhi = np.cos(phi)  # calc cos(phi)
    bmax = np.max(bFieldData, axis=0)
    bmin = np.min(bFieldData, axis=0)
    Bm = (bmax - bmin) / 2  # magnitude is (max-min)/2
    dBdt = np.diff(bFieldData, axis=0) / tStep  # calc dBdt
    Hm = hystLossFactor / np.pi * Bm  # magnitude of H according to paper
    Hirr = Hm * cosPhi
    hystLossField = np.sum(Hirr * dBdt, axis=2)
    return hystLossField


def calcHystLossdBdt(
    time: list[float], bFieldData: np.ndarray, hystLossFactor: float
) -> np.ndarray:
    """Calculate the hysteresis loss field by defining Hirr as the same trace
    as dBdt but with scaled amplitude"""
    tStep = time[1] - time[0]
    bmax = np.max(bFieldData, axis=0)
    bmin = np.min(bFieldData, axis=0)
    Bm = (bmax - bmin) / 2  # magnitude is (max-min)/2
    dBdt = np.diff(bFieldData, axis=0) / tStep  # calc dBdt
    Hdiff = np.nan_to_num(
        hystLossFactor / np.pi * Bm * dBdt / np.max(dBdt, axis=0)
    )
    Hdiff = [Hdiff, Hdiff[-1]]
    hystLossField = np.sum(Hdiff * dBdt, axis=2)
    return hystLossField


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


def writeSimple(
    fName, time: List[float], data: Union[np.ndarray, List]
) -> None:
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
        raise TypeError(
            f"Data type was not numpy.ndarray or list, but {type(data)}."
        )
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
    dens = steelMat.density  # density in kg/m³
    lossParams[0] = lossParams[0] * dens / freq / (ind**2)
    lossParams[1] = lossParams[1] * dens / ((freq * ind) ** 2)
    lossParams[2] = lossParams[2] * dens / ((freq * ind) ** 1.5)
    # return lossParams


def calcTimeDerivative(fieldFile: Union[str, os.PathLike]):
    """calculate time derivative and save to file

    Args:
        fieldFile (Union[str, os.PathLike]): pos results file
    """
    finGmsh = False  # determine if gmsh should be closed at the end
    if not gmsh.isInitialized():
        gmsh.initialize()
        finGmsh = True

    elementTags, time, fieldData = importPos(fieldFile)
    nbrTimeSteps = len(time)

    # init derivative of B
    dFdt = np.zeros((nbrTimeSteps - 1, fieldData.shape[1], fieldData.shape[2]))

    # loop through time step
    for step in range(1, nbrTimeSteps):
        dFdt[step - 1] = (fieldData[step] - fieldData[step - 1]) / (
            time[step] - time[step - 1]
        )

    # save as new
    model = gmsh.model.getCurrent()  # or just get current model...
    divView = gmsh.view.add("derivative")  # get tag of new view
    for step in range(len(time) - 1):
        gmsh.view.addModelData(
            tag=divView,
            step=step + 1,
            modelName=model,
            dataType="ElementData",
            tags=elementTags,
            data=dFdt[step, :],
            time=time[step],
        )

    # save p_hyst-field to file:
    dtFilepath = os.path.join(
        os.path.dirname(fieldFile), f"Dt_{os.path.basename(fieldFile)}"
    )
    gmsh.view.write(divView, dtFilepath)

    if finGmsh:
        gmsh.finalize()
