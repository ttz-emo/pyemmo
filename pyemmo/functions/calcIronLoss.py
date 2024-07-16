#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""This module defines the functions to calculate
the iron losses from getdp b-field simulation results."""

from __future__ import annotations

import os

import gmsh
import numpy as np
import numpy.typing as npt

# from matplotlib import pyplot as plt
from .import_results import importPos


def main(
    b_filepath: str | os.PathLike,
    loss_factor: dict[str, float],
    sym_factor: int,
    axial_length: float = 1.0,
) -> tuple[dict[str, np.ndarray], list[float]]:
    """The main of core loss calculation. This calls the time domain core loss
    calculation. For more info see :meth TODO

    Args: TODO...
        b_filepath (Union[str, os.PathLike]): _description_
        loss_factor (dict[str, float]): _description_
        sym_factor (int): _description_
        axial_length (float, optional): _description_. Defaults to 1.0.

    Returns:
        Tuple[Dict[str, np.ndarray], List[float]]: _description_
    """
    core_loss, time = calc_time_domain_core_loss(b_filepath, loss_factor, sym_factor, axial_length)
    return core_loss, time


def calc_time_domain_core_loss(
    b_filepath: str | os.PathLike,
    loss_factor: dict,
    sym_factor: int,
    axial_length: float = 1.0,
    save_fields: bool = True,
) -> tuple[dict[str, np.ndarray], list[float]]:
    """This function implements a time domain method for calculating the steel
    sheet core loss. For more information about the calculation method see
    `Lin u. a., „A Dynamic Core Loss Model for Soft Ferromagnetic and Power
    Ferrite Materials in Transient Finite Element Analysis“
    <https://ieeexplore.ieee.org/document/1284663>`_.

    The implementation is based on a magnetic flux density fea result of at
    least one electrical period. The result file (`b_filepath`) must be in
    `Gmsh readable (.pos) format
    <https://gmsh.info/doc/texinfo/#MSH-file-format>`_ and only contain the
    element values of the object (core surface) of intrest.

    Args:
        bFilePath (os.PathLike): _description_ TODO
        lossFactor (dict): _description_
        symFactor (int): _description_
        axialLength (float, optional): _description_. Defaults to 1.0.
        saveFields (bool, optional): _description_. Defaults to True.

    Returns:
        Tuple[Dict[str, np.ndarray], List[float]]: Iron loss results-dict +
            time array
    """
    core_loss = {}  # dict for loss results
    close_gmsh = False  # determine if gmsh should be closed at the end
    if not gmsh.isInitialized():
        gmsh.initialize()
        close_gmsh = True

    element_tags, time, b_field_data = importPos(b_filepath)
    nbr_timesteps = len(time)
    if save_fields:
        # extract filename from path
        _, filename = os.path.split(b_filepath)  # get filename with ext
        filename, _ = os.path.splitext(filename)  # get pure filename
    hyst_loss_field = calc_hyst_loss_ucp(time, b_field_data, loss_factor["hyst"])
    if save_fields:
        # save the View to a pos file
        model = gmsh.model.getCurrent()  # or just get current model...
        actual_view = gmsh.view.add(f"Hystersis Loss [W/m³] ({filename})")  # get tag of new view
        for step in range(len(time) - 1):
            gmsh.view.addHomogeneousModelData(
                tag=actual_view,
                step=step + 1,
                modelName=model,
                dataType="ElementData",
                tags=element_tags,
                data=hyst_loss_field[step, :],
                time=time[step],
            )
        # save loss density "p_hyst"-field to file:
        p_filepath = os.path.join(os.path.dirname(b_filepath), f"p_hyst_from_{filename}.pos")
        gmsh.view.write(actual_view, p_filepath)
    # integrate field over area for each time step
    hysteresis_loss: npt.NDArray[np.float64] = integrate_field(hyst_loss_field, time[1:], element_tags)
    # skip first value, because its 0:
    core_loss["hyst"] = hysteresis_loss[1:] * sym_factor * axial_length  # correct values

    # ------------------------- Calculate eddy current losses ---------------------------
    eddy_factor = loss_factor["eddy"]  # loss parameter
    # loss function for eddy current loss from paper:
    step_time = time[1] - time[0]
    diff_b = np.diff(b_field_data, axis=0) / step_time  # calc dBdt
    eddy_loss_field = np.sum(eddy_factor / 2 / (np.pi**2) * (diff_b**2), axis=2)
    # meanEddyLossField = np.mean(eddyLossField, axis=0)
    # eddyLoss = integrateField(np.array([meanEddyLossField]), [time[0]], elementTags)
    if save_fields:
        # save the View to a pos file
        model = gmsh.model.getCurrent()  # or just get current model...
        actual_view = gmsh.view.add(f"Eddy current Loss [W/m³] ({filename})")
        for step in range(len(time) - 1):
            gmsh.view.addHomogeneousModelData(
                tag=actual_view,
                step=step + 1,
                modelName=model,
                dataType="ElementData",
                tags=element_tags,
                data=eddy_loss_field[step, :],
                time=time[step],
            )
        # save p_hyst-field to file:
        p_filepath = os.path.join(os.path.dirname(b_filepath), f"p_eddy_from_{filename}.pos")
        gmsh.view.write(actual_view, p_filepath)
    eddy_loss = integrate_field(np.array(eddy_loss_field), time[1:], element_tags)
    if eddy_loss.size != nbr_timesteps:
        raise RuntimeError(f"Integration should result in {nbr_timesteps} values!")
    # skip first value, because its 0:
    eddy_loss = eddy_loss[1:] * sym_factor * axial_length  # correct values
    core_loss["eddy"] = eddy_loss

    # --------------------------- calculate excess loss ---------------------------
    if loss_factor["exc"] > 0:
        excess_loss_constant = 8.763363  # constant factor (from paper)
        exc_loss_field = np.sum(
            loss_factor["exc"] / excess_loss_constant * np.power(diff_b**2, 0.75),
            axis=2,
        )
        if save_fields:
            # save the View to a pos file
            model = gmsh.model.getCurrent()  # or just get current model...
            actual_view = gmsh.view.add(f"Excess Loss [W/m³] ({filename})")
            for step in range(len(time) - 1):
                gmsh.view.addHomogeneousModelData(
                    tag=actual_view,
                    step=step + 1,
                    modelName=model,
                    dataType="ElementData",
                    tags=element_tags,
                    data=exc_loss_field[step, :],
                    time=time[step],
                )
            # save p_hyst-field to file:
            p_filepath = os.path.join(os.path.dirname(b_filepath), f"p_exc_from_{filename}.pos")
            gmsh.view.write(actual_view, p_filepath)
        # meanExcLossField = np.mean(excLossField, axis=0)
        # excLoss = integrateField(np.array([meanExcLossField]), [time[0]], elementTags)
        exc_loss = integrate_field(np.array(exc_loss_field), time, element_tags)
        if exc_loss.size != nbr_timesteps:
            raise RuntimeError(f"Integration should result in {nbr_timesteps} values!")
        # skip first value, because its 0:
        exc_loss = exc_loss[1:] * sym_factor * axial_length  # correct values
        core_loss["exc"] = exc_loss
    else:
        # set iron loss to 0
        core_loss["exc"] = np.zeros(eddy_loss.shape)
        exc_loss_field = np.zeros(eddy_loss_field.shape)

    # Export total loss field
    if save_fields:
        # save the View to a pos file
        model = gmsh.model.getCurrent()
        actual_view = gmsh.view.add(f"Total Loss [W/m³] ({filename})")
        sum_loss_field = hyst_loss_field + eddy_loss_field + exc_loss_field
        for step in range(len(time) - 1):
            gmsh.view.addHomogeneousModelData(
                tag=actual_view,
                step=step + 1,
                modelName=model,
                dataType="ElementData",
                tags=element_tags,
                data=sum_loss_field[step, :],
                time=time[step],
            )
        # save p_hyst-field to file:
        p_filepath = os.path.join(os.path.dirname(b_filepath), f"p_core_from_{filename}.pos")
        gmsh.view.write(actual_view, p_filepath)

    if close_gmsh:
        gmsh.finalize()

    return core_loss, time[0:-1]


def calc_freq_domain_core_loss(
    b_filepath: str | os.PathLike,
    loss_factor: dict,
    sym_factor: int,
    axial_length: float = 1.0,
) -> tuple[dict[str, np.ndarray], npt.NDArray[np.float64]]:
    core_loss = {}  # dict for loss results
    close_gmsh = False  # determine if gmsh should be closed at the end
    if not gmsh.isInitialized():
        gmsh.initialize()
        close_gmsh = True

    elem_tags, time, b_field_data = importPos(b_filepath)
    ## calculate hysteresis losses
    hyst_loss_factor = loss_factor["hyst"]  # hysteresis loss factor
    # beta = 2  # hysteresis loss exponent
    # calculate element wise fft of b-field
    if np.all(
        np.linalg.norm((b_field_data[0] - b_field_data[-1]), axis=(1)) < np.linalg.norm(b_field_data, axis=(2, 0)) * 1e-3
    ):
        # value of last time step is nearly equal to first time step
        # -> skip last time step!
        b_field_data = b_field_data[:-1, :, :]
        time = time[:-1]
    timestep = time[1] - time[0]
    nbr_timesteps = len(time)
    amp = np.abs(np.fft.rfft(b_field_data[:, :, :], axis=0))
    # to get correct amplitude regarding the specific frequencies, the amplitudes
    # must be corrected by 1/nbrFreqs and DC-part by 1/(2*nbrFreqs) because its value
    # is doubled since its part of the positive and negative side of the spectrum.
    # Since I defined the number of frequencies to be only for the one sided spectrum,
    # we have to double the value for amp[0] and use only nbrFreqs for amp[1:]
    freqs = np.fft.rfftfreq(nbr_timesteps, timestep)
    nbr_freqs = len(freqs)
    amp = np.concatenate(([amp[0] / nbr_freqs / 2], amp[1:] / (nbr_freqs)), axis=0)
    amp = np.concatenate(([amp[0] / nbr_freqs / 2], amp[1:] / (nbr_freqs)), axis=0)
    # norm of xyz comp. -> hystLossField has shape (nbrElements, nbrFreqs)
    hyst_loss_field = np.linalg.norm(hyst_loss_factor * freqs * (amp.transpose() ** 2), axis=0)
    hyst_loss = integrate_field(hyst_loss_field.transpose(), freqs, elem_tags)[1:]
    hyst_loss = integrate_field(hyst_loss_field.transpose(), freqs, elem_tags)[1:]
    # skip first value, because its 0
    core_loss["hyst"] = hyst_loss * sym_factor * axial_length  # correct values

    # ------------------------- Calculate eddy current losses -------------------------
    eddy_loss_factor = loss_factor["eddy"]  # loss parameter
    # loss function for eddy current loss from paper:
    eddy_loss_field: np.ndarray = np.linalg.norm(eddy_loss_factor * (freqs**2) * (amp.transpose() ** 2), axis=0)
    eddy_loss = integrate_field(eddy_loss_field.transpose(), freqs, elem_tags)[1:]
    if eddy_loss.size != nbr_freqs:
        raise RuntimeError(f"Integration should result in {nbr_freqs} values!")
    # skip first value, because its 0
    eddy_loss = eddy_loss * sym_factor * axial_length  # correct values
    core_loss["eddy"] = eddy_loss

    ## calculate excess loss
    exc_loss_factor = loss_factor["exc"]
    if exc_loss_factor:
        exc_loss_field = np.linalg.norm(exc_loss_factor * (freqs**1.5) * (amp.transpose() ** 1.5))
        exc_loss = integrate_field(exc_loss_field.transpose(), freqs, elem_tags)[1:]
        if exc_loss.size != nbr_freqs:
            raise RuntimeError(f"Integration should result in {nbr_freqs} values!")
        # skip first value, because its 0:
        exc_loss = exc_loss * sym_factor * axial_length  # correct values
        core_loss["exc"] = exc_loss
    else:
        core_loss["exc"] = np.zeros(eddy_loss.shape)

    if close_gmsh:
        gmsh.finalize()

    return core_loss, freqs


def calc_hyst_loss_ucp(time: list[float], b_field_data: np.ndarray, hyst_loss_factor: float) -> np.ndarray:
    """Calculate the hysteresis loss field according to ANSYS Maxwell User-
    Controll-Program"""
    nbr_elements = b_field_data.shape[1]
    nbr_steps = len(time)
    timestep = time[1] - time[0]
    diff_b = np.diff(b_field_data, axis=0) / timestep  # calc dBdt
    uex = np.zeros((nbr_steps, nbr_elements, 2))
    h_m = np.zeros((nbr_steps, nbr_elements, 2))
    H = np.zeros((nbr_steps, nbr_elements, 2))
    for it in range(1, nbr_steps):
        # for each timestep
        for ie in range(nbr_elements):
            # for each element
            for comp in (0, 1):
                # for x,y, and not z
                b_new = b_field_data[it, ie, comp]
                b_old = b_field_data[it - 1, ie, comp]
                find_ext(it, ie, comp, b_old, b_new, uex)
                # calc Hm
                h_m[it, ie, comp] = hyst_loss_factor / np.pi * uex[it, ie, comp]
                if uex[it, ie, comp] == 0:
                    H[it, ie, comp] = np.sqrt(h_m[it, ie, comp] ** 2)
                else:
                    H[it, ie, comp] = np.sqrt(
                        np.abs(
                            h_m[it, ie, comp] ** 2 - (h_m[it, ie, comp] * b_field_data[it, ie, comp] / uex[it, ie, comp]) ** 2
                        )
                    )
    # sum of x and y; abs of value (x,y)
    hyst_loss_field = np.sum(np.abs(H[1:, :, :] * diff_b[:, :, 0:1]), axis=2)
    return hyst_loss_field


def find_ext(i_time, i_elem, i_comp, b_old, b_new, uex):
    if (b_new < b_old) and (b_old > uex[i_time - 1, i_elem, i_comp]):
        uex[i_time, i_elem, i_comp] = b_old
    elif (b_new > b_old) and (b_old < uex[i_time - 1, i_elem, i_comp]):
        uex[i_time, i_elem, i_comp] = b_old
    else:
        uex[i_time, i_elem, i_comp] = uex[i_time - 1, i_elem, i_comp]


def calc_Hm(bFieldData: np.ndarray, time: list[float], hystLossFactor):
    nbr_elements = bFieldData.shape[1]
    nbr_timesteps = len(time)
    uex = np.zeros((nbr_timesteps, nbr_elements, 2))
    h_m = np.zeros((nbr_timesteps, nbr_elements, 2))
    H = np.zeros((nbr_timesteps, nbr_elements, 2))
    for it in range(1, nbr_timesteps):
        # for each timestep
        for ie in range(nbr_elements):
            # for each element
            for comp in (0, 1):
                # for x,y, and not z
                b_new = bFieldData[it, ie, comp]
                b_old = bFieldData[it - 1, ie, comp]
                find_ext(it, ie, comp, b_old, b_new, uex)
                # calc Hm
                h_m[it, ie, comp] = hystLossFactor / np.pi * uex[it, ie, comp]
                if uex[it, ie, comp] == 0:
                    H[it, ie, comp] = np.sqrt(h_m[it, ie, comp] ** 2)
                else:
                    H[it, ie, comp] = np.sqrt(
                        np.abs(h_m[it, ie, comp] ** 2 - (h_m[it, ie, comp] * bFieldData[it, ie, comp] / uex[it, ie, comp]) ** 2)
                    )


def calc_hyst_loss_sin(time: list[float], b_field_data: np.ndarray, hystLossFactor: float) -> np.ndarray:
    """Calculate the hysteresis loss field by using the cosine of the
    fundamental B field wave"""
    nbr_elements = b_field_data.shape[1]
    nbr_timesteps = len(time)
    if np.all(np.linalg.norm((b_field_data[0] - b_field_data[-1]), axis=1) < np.linalg.norm(b_field_data, axis=(2, 0)) * 1e-3):
        # value of last time step is nearly equal to first time step
        # -> skip last time step!
        b_field_data_fft = b_field_data[:-1, :, :]
    else:
        b_field_data_fft = b_field_data
    # calculate element wise fft of b-field:
    b_fft = np.fft.rfft(b_field_data_fft, axis=0)
    amp = np.abs(b_fft)
    # to get correct amplitude regarding the specific frequencies, the amplitudes
    # must be corrected by 1/nbrFreqs and DC-part by 1/(2*nbrFreqs) because its value
    # is doubled since its part of the positive and negative side of the spectrum.
    # Since I defined the number of frequencies to be only for the one sided spectrum,
    # we have to double the value for amp[0] and use only nbrFreqs for amp[1:]
    timestep = time[1] - time[0]
    freqs = np.fft.rfftfreq(np.shape(b_field_data_fft)[0], timestep)
    nbr_freqs = len(freqs)
    amp = np.concatenate(([amp[0] / nbr_freqs / 2], amp[1:] / (nbr_freqs)), axis=0)
    phase = np.angle(b_fft)
    for elem in range(nbr_elements):
        # FIXME: Assume that freq. of max. amplitude is the same for x and y comp.
        #   -> norm                                         +1 because skipping DC
        index_f_max = np.linalg.norm(amp[1:, elem, :], axis=1).argmax() + 1
        phi0 = phase[index_f_max, :, :]

    # fMaxIndex equals order of that spectral part
    phi = np.linspace(
        phi0 + np.pi / 2,
        index_f_max * (2 * np.pi) + phi0 + np.pi / 2,
        nbr_timesteps - 1,
    )
    cos_phi = np.cos(phi)  # calc cos(phi)
    bmax = np.max(b_field_data, axis=0)
    bmin = np.min(b_field_data, axis=0)
    b_m = (bmax - bmin) / 2  # magnitude is (max-min)/2
    diff_b = np.diff(b_field_data, axis=0) / timestep  # calc dBdt
    h_m = hystLossFactor / np.pi * b_m  # magnitude of H according to paper
    h_irr = h_m * cos_phi
    hyst_loss_field = np.sum(h_irr * diff_b, axis=2)
    return hyst_loss_field


def calc_hyst_loss_diff_b(time: list[float], b_field_data: np.ndarray, hyst_loss_factor: float) -> np.ndarray:
    """Calculate the hysteresis loss field by defining Hirr as the same trace
    as dBdt but with scaled amplitude"""
    timestep = time[1] - time[0]
    bmax = np.max(b_field_data, axis=0)
    bmin = np.min(b_field_data, axis=0)
    b_m = (bmax - bmin) / 2  # magnitude is (max-min)/2
    diff_b = np.diff(b_field_data, axis=0) / timestep  # calc dBdt
    h_diff = np.nan_to_num(hyst_loss_factor / np.pi * b_m * diff_b / np.max(diff_b, axis=0))
    h_diff = [h_diff, h_diff[-1]]
    hyst_loss_filed = np.sum(h_diff * diff_b, axis=2)
    return hyst_loss_filed


def integrate_field(
    field_data: npt.NDArray,
    time: list[float],
    elem_tags: npt.NDArray,
    mesh_file: str | os.PathLike = "",
) -> npt.NDArray[np.float64]:
    close_gmsh = False
    if not gmsh.isInitialized():
        gmsh.initialize()
        close_gmsh = True
    origin_verbosity = gmsh.option.getNumber("General.Verbosity")
    gmsh.option.setNumber("General.Verbosity", 1)

    try:
        if mesh_file:
            gmsh.open(mesh_file)
        model = gmsh.model.getCurrent()
        view_tag = gmsh.view.add("FieldToIntegrate")
        for step, time_val in enumerate(time):
            gmsh.view.addHomogeneousModelData(
                tag=view_tag,
                step=step + 1,  # steps must start at 1...
                modelName=model,
                dataType="ElementData",
                tags=elem_tags,
                data=field_data[step, :],
                time=time_val,
            )
        # integrate:
        gmsh.plugin.setNumber("Integrate", "View", gmsh.view.getIndex(view_tag))
        integrate_view = gmsh.plugin.run("Integrate")
        _, _, integrated_data = gmsh.view.getListData(integrate_view)
        # dataType is allways SP after integration
        # number of elements after integration should be 1
        # set original verbosity after integration
        gmsh.option.setNumber("General.Verbosity", origin_verbosity)
    except Exception as exce:
        gmsh.finalize()
        raise exce
    if close_gmsh:
        gmsh.finalize()
    # only return data values (skip SP coordinates)
    data: npt.NDArray[np.float64] = integrated_data[0][3:]
    return data


def write_simple(
    filename: str | os.PathLike,
    time: list[float],
    data: np.ndarray | list,
) -> None:
    """_summary_
    TODO
    Args:
        fName (os.PathLike): File name to existing folder.
        time (List[float]): Time vector.
        data (Union[np.ndarray, List]): Data vector or matrix.
    """
    nbr_timesteps = len(time)
    if isinstance(data, np.ndarray):
        if not np.any(np.equal(data.shape, nbr_timesteps)):
            raise ValueError("No axis of the given data array does match the length of the time vector.")
    elif isinstance(data, list):
        if len(data) != nbr_timesteps:
            raise ValueError(
                "Length of the data vector does not match length of time vector " f"{len(data)} != {nbr_timesteps}"
            )
    else:
        raise TypeError(f"Data type was not numpy.ndarray or list, but {type(data)}.")
    with open(filename, "w", encoding="utf-8") as resFile:
        for varStep in range(nbr_timesteps):
            resFile.write(f"{time[varStep]} {data[varStep]}\n")


def calcTimeDerivative(fieldFile: str | os.PathLike):
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
        dFdt[step - 1] = (fieldData[step] - fieldData[step - 1]) / (time[step] - time[step - 1])

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
    dtFilepath = os.path.join(os.path.dirname(fieldFile), f"Dt_{os.path.basename(fieldFile)}")
    gmsh.view.write(divView, dtFilepath)

    if finGmsh:
        gmsh.finalize()
