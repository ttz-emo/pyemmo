# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [unreleased] - 2026-xx-xx
### Added
-

### Changed
-

### Fixed
-

### Removed
-

## [1.6.0] - 2026-03-19
### Added
- New option to supply user defined symmetry to PYLEECAN api `api.pyleecan.main()` via new attribute `symmetry`. Otherwise symmetry will be calculated from geometry and winding in `api.pyleecan.create_param_dict()`.
- New function `functions.import_results.freq_from_signal` to extract fundamental frequency from signal.
- Added GetDP parameter `GlobalMeshsizeFactor = GetNumber[StrCat[INPUT_MESH, "00Mesh size factor"], 1.0]` to adjust evaluation of airgap field (OnGrid).
- Script `convert_ipynb_tutorials.sh` to convert tutorials to .py files using `nbconvert` package.
- Updated and release current version of the documentation. See *README.md* for details.

### Changed
- Min. Python version is 3.9 now.
- Updated requirement files.
- Moved methods `get_radial_position` and `get_circumferential_position` from `Slot` to `PhysicalElement`.
- Renamed/moved modules (python files):
  - `functions.calcIronLoss` -> `functions.core_loss`.
  - `functions.runOnelab` -> `functions.run_onelab`.
  - `geometry.slaveLine` -> `physicals.secondary_line`.
  - `geometry.airGap` -> `physicals.airgap`.
  - `geometry.physicalElement` -> `physicals.physical_element`.
  - `script.geometry.domain` -> `script.domain`.
  - `script.geometry.machineAllType` -> `script.machine`.
  - `script.geometry.rotor` -> `script.rotor`.
  - `script.geometry.stator` -> `script.stator`.
- United modules `functions.exportMaxwell` and `functions.import_maxwell` -> `functions.maxwell` for ANSYS Maxwell IO.
- Renamed functions:
  - In `pyemmo.api.json.boundaryJSON`:
    - `createMB` -> `create_MB`.
    - `getRotFreq` -> `get_mech_speed`.
    - `getMagTemperature` -> `get_magnet_temperature`.
  - In `functions.core_loss`: `calcTimeDerivative` -> `calc_time_derivative`.
  - In `functions.import_results`:
    - `importSP` -> `import_sp`.
    - `importPos` -> `import_pos`.
    - `import_pos_parsedFormat` -> `import_pos_legacy`.
  - In `functions.run_onelab` (previous `runOnelab`):
    - `findGmsh` -> `find_gmsh`.
    - `findGetDP` -> `find_getdp`.
    - `findExe` -> `find_exe`.
    - `createCmdCommand` -> `create_command`.
    - `createGMSHCommand` -> `create_gmsh_command`.
    - `runCalcforCurrent` -> `run_simulation`.
- Moved `PhysicalElement` class implementations from `pyemmo.script.geometry` to separate subpackage `pyemmo.script.physicals`. This includes class modules: `airArea`,`airgap`,`bar`,`limitLine`,`magnet`,`movingband`,`physical_element`,`primaryLine`,`rotorLamination`,`secondary_line`,`slaveLine`,`slot`,`statorLamination`.
- Renamed `PhysicalElement` boundary line class `Slaveline` to `SecondaryLine` in module `pyemmo.script.physicals.secondary_line`.
- Renamed `PhysicalElement` attribute `PhysicalElement.geoElementType` to `PhysicalElement.geo_type`.
- Renamed machine container class `MachineAllType` to `Machine`.
  - Renamed machine methods:
    - `createMachineDomains` -> `create_domains`.
    - `domainsCreated` -> `domains_created`.
    - `symmetryFactor` -> `symmetry_factor`.
    - `primaryLines` -> `primary_lines`.
    - `getSecondaryLines` -> `get_secondary_lines`.
    - `physicalElements` -> `physicals`.
    - `setFunctionMesh` -> `set_function_mesh`.
- Moved GetDP Parameter *NbrMbSegments* from *machine_magstadyn_a.pro* to *machine_template.pro*.
- Renamed properties/methods in `Script` class:
  - `scriptPath` -> `script_path`.
  - `resultsPath` -> `results_path`.
  - `colorCode` -> `color_code`.
  - `functionMaterial` -> `function_material`.
  - `functionMagnetisation` -> `function_magnetization`.
  - `proFilePath` -> `pro_file_path`.
  - `geoFilePath` -> `geo_file_path`.
  - `simParams` -> `sim_params`.
  - `materialDict` -> `material_dict`.
  - `postOperation` -> `post_operation`.
  - `postOperationNames` -> `get_post_operation_names()` (function now).
  - `addPostOperation()` -> `add_post_operation()`.
  - `writeGeo()` -> `write_geo()`.
  - `writePro()` -> `write_pro()`.
  - `generateScript()` -> `generate()`.

### Fixed

- Sort induction machine rotor bar physicals in json api ``modelJSON.createSlot()`` in circumferential direction to make sure they are connected correctly in the rotor squirrel cage circuit.
- `api.pyleecan.build_pyemmo_material()` sets default values for Material properties instead of None.
- Extraction of winding direction in `pyemmo.api.json.modelJSON.getSlotPhase()` dependent on single or double layer.
- Fix bug in Git hash extraction if GitPython installed, but repository not found.

### Removed
- Removed unused functions:
  - In `pyemmo.api.json.boundaryJSON`: `findLine`, `findLines`, `getBoundaryLines`, `createMBLines`, `getLimitLines`, `geoElemList`
  - In `pyemmo.api.json.importJSON`: `InvalidSheetThicknessError`, `getCurrentAmpl`, `getElecFreq`, `isAir`
- Removed unused toolkit `PhysicalElement` subclasses: `MachineASM`, `MachineIPMSM`, `MachineSPMSM`, `MagnetSlot01`, `MagnetSurface01`, `MagnetSurface02`, `MagnetSurface03`, ...
- Unused properties in `Script` class: `pointCode`, `pointArray`, `curveCode`, `curveList`, `areaCode`, `areaArray`, `physicalElementCode`, `physicalElementArray`, `factory`.
-

## [1.5.0dev2] - 2026-02-03
### Added
- Added option to generate a SWAT-EM winding from model information when value "winding" is set to "auto" instead of winding config. This tries to evaluate the number of winding layers from the given geometry input.

## [1.5.0dev1] - 2026-01-21
**Reworked Pyleecan API to run for new Gmsh api workflow in PyEMMO**
### Added
- Raise error in api if number of stator winding phases != 3, because GetDP template assumes 3 phases for now.
- Completely reworked pyleecan api with new general workflow:
  - Core is the `create_geo_dict` function that created minimal segments of the pyleecan model surfaces from the geometry symmetry and handles all surfaces depended on type and pyleecan surface labels. Rotor and stator holes (vents) are handles separately after the other surfaces, as well as shaft and frame.
  - New function `create_gmsh_surface` to translate pyleecan surfaces to `MachineSegmentSurface` via `create_gmsh_lines` for curve loop.
  - New function `label2part_id` handles relevant `part_id`s for json api.
  - Added tutorial script for pyleecan api usage.
  - Reworked magnetization transformation in `create_param_dict`.
- Refactored function `load_view`  in module `import_results` from function `importPos` and added `import_pos_parsedFormat` to improve import OnGrid formatted GetDP results.
- New module `functions.transform_coords` for coordinate system transformations:
  - `cart2pol`
  - `pol2cart`
  - `cart2sph`
  - `cart2sphA`
- Added `tag` support for curve plots in `PhysicalElement`
- Added PostOperation `DeleteViews` and ONELAB parameter `Flag_ClearViews` to remove all PostProcessing views from current gmsh GUI session when running a (new) simulation.
- Added airgap Maxwell Stress Tensor (MST) force PostProcessing:
  - `Force_MST`: MST in cartesian coords.
  - `Force_MST_Cyl`: MST in cylindrical coords
  - `Force_MST_Rad`: MST radial component.
  - `Force_MST_Tan`: MST tangential component.

### Changed
- Extended logging. Log messages are more verbose now and contain module and function information.
- Setting default airgap mesh size to band height in `create_airgaps`.
- Material creation in json api with `create_material` is now based on `Material.from_dict`.
- Suppress gmsh terminal output by setting `General.Terminal = 0` in gmsh options, because gmsh always raises an error if the model of occ and internal is not synchronized.

### Fixed
- Check start and endpoints of airgap interface curve for homogeneity in `create_airgaps` to also account for bore shape.

### Removed
- Removed some now unused pyleecan api modules.
- Removed line support for GetDP PostOperations `b_radial` and `b_tangent`, because can't evaluate curl on line correctly (returns only normal component to line).

## [1.4.1a2] - 2026-11-24
### Added
- Static and dynamic eccentricities in GetDP model template using initial `ChangeOfCoordinates` to change initial mesh coordinates of stator/rotor. The eccentricity is controlled by new parameters `eccentricity_static` and `eccentricity_dynamic` in mm.
- Added rotor bar flux linkage PostOperation in GetDP template.

### Fixed
- Update of `GmshSegmentSurface` tool segment number on `rotateDuplicate` of parent surface.

## [1.4.1a1] - 2025-11-27
### Added
- Improved logging by adding logging setup (file and console) and extended logging calls and messages.
- Extended debugging with log level `< logging.DEBUG`. This also triggers Gmsh GUI in API modeling process to show progress.
- New module `create_airgaps` in json api to create airgap(s) if not in given geometry. See doc for details.
- Added voltage source simulation results to `import_results.main()` result.
- Added module `functions.onelab_parameters` with function `extract_onelab_parameters` to parse onelab parameter definitions from .pro files
- Added file logging of simulation output in `runOnelab.runCalcForCurrent()`.
- Added `Line.angle_to_middle()` method.
- New module `create_gmsh_curve` with function `create_curve` to handle TrimmedCurve objects created from occ boolean operations.
- New functions in `gmsh.utils`:
  - `get_global_center()`
  - `create_disk()`

### Changed
- Renamed functions in `importJSON`
  - `importExtInfo` -> `load_info_dict`
  - `getMagDir` -> `get_mag_type`
  - `getWindingList` -> `get_winding_layout`
  - `getNbrOfTurns` -> `get_nbr_of_turns`
  - `getSymFactor`-> `get_sym_factor`
  - `getNbrPolePairs` -> `get_nbr_of_pole_pairs`
  - `getNbrSlots` -> `get_nbr_of_slots`
  - `getAxialLength` -> `get_axial_length`
  - `getSimuParams` -> `get_simulation_params`
  - `getModelName` -> `get_model_name`
  - `getFlagOpenGui` -> `get_flag_open_gui`
  - `getMovingbandRadius` -> `get_MB_radius`
  - `getNbrParalellPaths` -> `get_nbr_of_parallel_paths`
  - `getFlagCalcIronLoss` -> `get_flag_core_loss_calc`
  - `getMagAngle` -> `get_mag_angle`
  - `createMaterial` -> `create_material`
- Update SWAT-EM config dict on package init to improve MMF accuracy.

### Fixed
- Added separate implementation of `rotate_duplicate` method for `MachineSegmentSurface`, because did return `GmshSegmentSurface`.
- Sort rotor bars in circumferential direction to create bar domains in correct order for circuit coupling.
- Fixed newline character placement in `Script._printAllMaterial()` BH data export to .pro file

### Removed
- Setter of `Movingband.radius`, because MB radius is determined by `geo_list` arc instances and moved logic to check for consistent MB radius to getter.

## [1.4.0rc2] - 2025-07-29
### Added
- Added Class `GmshSpline`.
- Support for `GmshSpline` in json api (`modelJSON.createLine`), where `"MP"` attribute of Curve structure is control point.
- ONELAB parameters:
  -  `Flag_SaveSolution` to control the GetDP export of solution data to .res file. Because this slows down the calculation quite a lot and is not really used.
  -  `NbrMbSegments` for number of movingband mesh segments. Used in PostOperation to get best resolution for airgap field.
  - `r_rotor_airgap` and `r_stator_airgap` for control of where to evaluate airgap field. And set their default values to mean airgap radius (center of airgap band surface).
- Setting of Gmsh internal mesh size parameter `Mesh.MeshSizeFactor` to PyEMMO parameter `gmsf` (global mesh size factor).

### Changed
- Python minimal version increased to 3.8 due to issues with setuptools package.

### Fixed
- Gmsh points potentially loosing their mesh sizes due to boolean options in json api. Fixed that by `gmsh.utils.fix_missing_mesh_sizes()` function. It loops through all points and tries to find the next closest points mesh size if one is missing.
- Adapted `filter_lines_at_angle` function to also account for center point, because angle to x-axis is allways 0 for center point.

### Removed
- Unused template `parameters_template.geo` since param file is created directly from `Script`.

## [1.4.0rc1] - 2025-07-08
Integration of new API workflow using gmsh Python package.
The new subpackage `pyemmo.script.gmsh` implements the utility to create PyEMMO machine models live through the [Gmsh Python api](https://gmsh.info/doc/texinfo/gmsh.html#Gmsh-application-programming-interface).
This enables faster model creation, because the very time consuming filter process in the `Script` class for duplicated Points and Lines can be replace by the `gmsh.model.remove_duplicates()` algorithm.
But this change involves massive changes in the overall model creation workflow, especially for the JSON and Pyleecan APIs, since the geometries are now created at runtime.
Before they were only created when `Script.generate()` was invoked.
Additionally this extends modelling capabilities by using the boolean operations available in the [OpenCASCADE](https://dev.opencascade.org/project/gmsh) kernel of Gmsh.
**Pyleecan api was not reworked yet and doesn't work in the current version.**

### Added
- New Gmsh geometry classes in subpackage `pyemmo.script.gmsh` to handle objects between gmsh python api and PyEMMO: `GmshGeometry`(AbstractClass), `GmshPoint`, `GmshLine`, `GmshArc`, `GmshSurface`, `GmshSegmentSurface`
  - These classes keep the consistency between the `pyemmo.script.geometry`classes and the gmsh internal occ kernel instances by keeping track of the surface IDs, even if they change through boolean operations.
  - So for example `GmshSurface` is a child class of PyEMMO `Surface` and abstract class `GmshGeometry`.
  - The property `id` was moved from the PyEMMO geometry classes to the gmsh geometry classes, so the PyEMMO geometry classes only implement structures (like abstract classes) for geometries.
  - `PhysicalElement` creates `PhyiscalGroup` in gmsh api with `gmsh.model.addPhysicalGroup()`.
- `gmsh.utils` module for various utility functions:
  - `get_dim_tags` to get list of dimTags (list of tuple of (dimension index, Gmsh ID)) from a list of PyEMMO gmsh geometries.
  - `get_point_tags`: get a list of gmsh point IDs.
  - `get_max_radius`
  - `get_min_radius`
  - `filter_curves_on_radius`: to filter curves in boundary recognition.
  - `filter_lines_at_angle`: to filter curves in boundary recognition.
  - `is_straight`: to check if a arbitrary gmsh curve is a straight line.
- New `colors` module which defines a `Colors` dict with all available Gmsh colors and their rgba code.
- New Classes `SegmentSurface`, `GmshSegmentSurface` for segmented surfaces as base for api `MachineSegmentSurface` class:
  - These classes represent circumferentially segmented geometries with properties:
    - `nbr_segments`
    - `segment_number` which is set when `rotate_duplicate()` method is called.
- `MachineSegmentSurface` class as new core for api algorithm:
  - This class combines the segmented geometry properties with:
    - `part_id` that describes what part of the machine the geometry represents. The important identifiers with special properties, like stator slots or airgap, are defined by constants in `pyemmo.api.json` package init.
    - `material` information (like PhysicalElement).
- Added property `Point.x`,`.y`,`.z` for coordinates.
- `Line.length` property to all Line classes.
- `Line.vector` property to get vector from start to end point.
- `Line.complex` complex reprensentation of a 2D line.

### Changed
- Replaced manual geometry creation in `Script` and replaced it by `gmsh.write()`. But still added the manual model settings around the created geometry code.
- Reworked the complete JSON api workflow to use `MachineSegmentSurface` and general PyEMMO gmsh objects, but idea of segmented input is the same.
  - Boundary identification is now done by extracting all boundary lines of rotor and stator and filtering them into primary/secondary, movinband and outer/inner boundaries.
  - Updated string identifiers in surface names to `MachineSegmentSurface.part_id`
- `PhyiscalElement.geometricalElement` was renamed to `PhyiscalElement.geo_list`.
- `Line.startPoint`/`Line.endPoint` was renamed to `Line.start_point`/`Line.end_point`.
- `Line.middlePoint` was renamed to `Line.middle_point`.
- `Line.getPoints()` method was replaced by `Line.points` property.
- `Spline.controlPoints` was renamed to `Spline.control_points`.
- `Spline.splineType` was renamed to `Spline.spline_type`.
- Replaced `sys.exec` call in `definitions` module by `import` statements.

### Fixed
- Fixed bug in `Line.combine()` by checking for line directions.

### Removed
- Old, manual geometry creation algorithm in `Script`.
- Class `api.json.SurfaceJSON` because is replaced by `api.MachineSegmentSurface` class.
- `id` property from `Tranformable`s.
- `meshSize` property from `geometry.Point`.
- `force` property of geometry instances because replaced by new workflow.
- `addToScript()` methods of `Tranformable`s.


## [1.3.3] - 2025-07-07
### NOTE
This version was not really a release but was added for better organization of changes.
### Added
- Export of simulation parameter setup as json file in `runOnelab.runCalcForCurrent()` and new function `import_results.load_param_file()` to load it.
- Separate function `import_results.main()` to correctly import default results as dict according to `runOnelab` parameters.
- Added module `functions.import_maxwell` to import ANSYS Maxwell result files.
- New function `phase.angle2phase()`.
- `plot` method for `PhysicalElement`s.
- Added splines package to requirements

### Changed
- Moved functions `phase2angle` and `phase2color` from `modelJSON` module to new module `functions.phase`.
- `Surface.plot()` method returns matplotlib `Figure` and `Axes` objects.
- Only save GetDP solution in a .res file on if `Flag_Debug` is set by user.

### Fixed
- Induction machine circuit by scaling equivalent circuit components of squirrel cage circuit by axial length, because internal voltage quantity is in V/m.
- Reset axes limits in `MachineAllType.plot()` for symmetry > 1 and no Movingband
- Induction machine circuit for uneven number of poles greater than 1.

### Removed
- Additional wrong DC bar resistance from induction machine circuit.
- Dynamic bar resistance evaluation in GetDP template Resolution.
- Bar resistance PostProcessing and PostOperation definition.
- Removed pyleecan package from requirements due to issue with Python compatibility (only \<3.10 possible)

## [1.3.2] - 2024-10-15
### Added
- Model supports induction machine calculation with rotor bar circuit now:
  - Class `Bar(PhysicalElement)` for induction machine rotor bars.
  - New identifier (IdExt) "RoCu" for rotor bars in json api.
  - New template file *Circuit_SC_ASM.pro* for rotor bar circuit.
- Constants for GetDP template domain names in `Script.__init__` like `DOMAIN_MAGNET`.
- GPLv3 License according to `gmsh` python package.
- Adapted simulation parameter setup and added ONELAB Parameter to *machine_template.pro*:
  - **MachineType** to check for SM or ASM.
  - **nbrStatorPeriods** for ASM simulation.
  - **nbrStepsPerPeriod** for ASM short circuit simulation (N=0 rpm).
  - **freq_rotor** for ASM simulation.
  - **I_eff** for ASM simulation.
  - **Flag_Cir_RotorCage** to control ASM circuit usage.
  - **R_endring_segment** for ASM circuit ring elements.
  - **L_endring_segment** for ASM circuit ring elements.
  - **freq_stator** for ASM simulation.
  - **n_sync** for ASM simulation.
  - **slip** for ASM simulation.
- Added GetDP PostOperation `Get_I_Bar` for rotor bar currents.
- Added mag. `Flux` and `InducedVoltage` PostProcessing for *DomainC* (induced currents).
- Added bar resistance PostProcessing `Resistance` for DC resistance and `R_Bar_{index}` for time depended AC resistance.
- Added function `json.get_min_coilspan.get_min_coilspan()`to calculate the minimal coil span from a SWAT-EM winding layout and the total number of slots. Used in `modelJSON.create_winding()`
- Several changes to `runOnelab` module:
  - Added function `log_subprocess_output()` to log the Gmsh/GetDP command-line outputs.
  - Added option to use existing .msh mesh file for calculations with `"msh"` parameter keyword. Otherwise trigger mesh creation.
  - Added option to control subprocess output verbosity by parameter keyword `"verbosity level"`.
  - Added option to delete previous result files by parameter keyword `"Flag_ClearResults"`.
  - Added option to execute additional post operations by parameter keyword `"PostOp"` with list of GetDP  PostOperation names.
  - Split gmsh and getdp commands in `createCmdCommand()`.
  - Added default import of results from *I_bars.dat* file (rotor bar currents).
  - Added import of rotor and stator Maxwell Stress Tensor torque + mean of both.
- `PhysicalElement` property `type`.
- New method `Slot.get_circumferential_position()` to sort slots.
- Added plot method for Spline: `Spline.plot()`.
- Added `Stator` method `Stator.outer_radius()` to find greatest radius from geometry.
- Added property `Material.tempCoefRem` for remanence induction temperature coefficient.

### Changed
- Calculate property `symmetryFactor` of Machine classes by geometry and winding symmetries. Option in `MachineAllType` to force set `symmetryFactor` stays.
- Type annotations of standard containers (Dict, List, Tuple, Union) changes from `typing.Dict` to `dict`. Added `from __future__ import annotations` to all files to allow for compability with Python 3.7+ versions.
- JSON api creates standard `Material` for ElectricalSteel material `sheetThickness` value greater 5 mm.
- Refactored function `json._open_onelab()` and `json._run_core_loss_calculation()` from `json.main()`.
- Moved adaption of core loss parameters from `json` package to `ElectricalSteel` class `lossParams` getter.
- Remove ArgumentParser from `runOnelab.main()` and moved it to `if __name__ == "__main__"` section
- Automatic mesh size algorithm:
  - Implementation moved from `MachineAllType` to `Rotor` and `Stator` to set mesh size individually.
  - Parameters `functionType` and `meshGainFactor` of `MachineAllType.setFunctionMesh()` are optional now.
- Renamed `Slot.getRadialPosition()` -> `Slot.get_radial_position()`.
- Automatically sort slots in circumferential and radial position in getter `Stator.slots`.

### Fixed
- No need to provide of have Gmsh instance installed to use JSON api, since gmsh Python package comes with a small version of the executable.
- Some bug fixed and optimizations in PyleecanAPI, but still limited interface capabilities.
- Bug fix when adding materials with equal name but different properties in `Script`
- Bug in pro file by adding newlines in BH curve data export, because for highly resolved BH curves getdp fails to read all data from a single line.

## [1.3.1.b1] - 2024-03-05
### Added
- First version of API to [Pyleecan project](https://pyleecan.org/)
- New hysteresis loss calculation algorithm. 3 options for hysteresis loss calculation:
  - sin-wave H field
  - H field trace as scales differentiation of B field
  - UCP method (default)
- `runOnelab.runCalcForCurrent` function to start subprocess calculation of ONELAB model based on input parameter dict and import default results.
- New option *useFunctionMesh* in json api parameter dict to trigger usage of `MachineAllType.setFunctionMesh()` method.
- Property `Line.middlePoint`

### Changed
- `Material.isLinear()` method to property `Material.linear`
- Renamed modules, functions and methods from CamelCase to snake_case
  - `functions.importResults` -> `functions.import_results`
  - `import_results.getResFileList()` -> `import_results.get_result_files()`
  - `import_results.plotAllDat()` -> `import_results.plot_all_dat()`
  - `import_results.plotTimeTableDat()` -> `import_results.plot_timetable_dat()`
  - `pyleecan.createGeoDict` -> `pyleecan.create_geo_dict`

### Fixed
- Some small bug fixes and adaptions to json api


## [1.3.1.a2] - 2024-01-31
### Added
- `GetResFileList` function to get list of .dat and .pos result files
- Warning log in `modelJSON.createWinding` if number of parallel connections given exceeds max. number of parallel connections calculated by SWAT-EM.

### Fixed
- Addes missing parameter *NBR_PARALLEL_PATHS* to *simuParams* dict in `importJSON.getSimuParams()`

### Removed
- Center point detection in jsonAPI, because it leads to in case of multiple api runs.

## [1.3.1.a1] - 2023-12-13
### Added
- "MB_CurveRotor", "OuterLimit", "InnerLimit" Identifier for jsonAPI coupling with Pyleecan.
- Import of magnetization angle as dict with magnet idExt as key and magnetization vector (allways outwards) as value.
- Function getSlotPhase to return phase and winding direction of a segment.
- Added options to save field data files in iron loss calculation.
- Redefined function to set slot color dependet on phase.
- Functions and tests to export data in ANSYS Maxwell tab format.

### Changed
- Changes nearly all getter and setter functions to python properties.
- jsonAPI keyword for magnetization type (e.g. parallel) -> "magType".
- jsonAPI winding import directly by SWAT-EM layout.
- Datatype of Script class attribute simulation parameter from SimpleNamespace -> dict, because parameters can be merge easier.
- Simulation parameter names directly named like the GetDP template variables.
- Handling of geo and extInfo import in jsonAPI to directly take dict aswell.
- Updated requirement versions.

### Fixed
- jsonAPI boundary inner limit line check.
- Logging of system call stderr.
- Function to create winding layout for SWAT-EM.
- Paths in test.

### Removed
- Center point detection in jsonAPI, because it leads to in case of multiple api runs.

## [1.3.0.post2] - 2023-09-18
### Added
- Logging to file and command line handler.
- Logging for json api in separate model folder file.
- Json-api command line option for log level.
- Flow chart file.
- Function to calculate time derivative of Gmsh field result file.
- Flag for global eddy current calculation.
- Magnet loss post operation in json api.

### Changed
- Log sterr of subprocess call in api if GUI is off.
- Updated requirements file and moved to top level folder.

### Fixed
- Center point detection in json api.
- BH-curve type error in api.
- Bug in material BH-curve comparison due to new numpy version.

### Removed
- Warnings and warning package from json api.

## [1.3.0.post1] - 2023-06-12
### Changed
- Check if Script-obj. name is valid file name at init time.

### Fixed
- Bug in global center point generation (using float instead of int!).

## [1.3.0] - 2023-05-31
### Added
- Optional plot of tags in surface, line and point plot.
- Additional test cases for different slot and magent types in SPMSM test.
- Function 'getPoints()' in Spline class.
- Functions 'calcTimeDomainIronLosses()' and 'calcFreqDomainIronLosses()' to calculate iron losses based on time domain and fft of b-field.

### Changed
- RENAMING PROJECT PYDRAFT -> PYEMMO
- Project structure reorganized.
- Renamed API modules to 'json', 'importJSON', 'modelJSON', ...
- Replaced api package center point with global center point.
- Renamed lamination domain from 'Domain_Lam' to 'DomainLam'.

### Fixed
- Remove commented lines in .dat-file import.
- Bug in case of light mesh coloring.
- Validation of script file name.
- Mesh setting by function for Spline case.
- Bug in PostOperation code generation.


## [1.2.10] - 2023-02-20
### Added
- First version of documentation with sphinx in html format.
- Function to export results in simple getdp dat-format ('TimeTable').
- Iron loss calculation by module 'calcIronLoss' under 'functions' to calculate iron loss from b field result file.
- Function integrateField to build the surface integral of field results in gmsh.
- Function importPos to import results in onelab pos format with gmsh api.
- Git commit hash export to generated model files.
- Iron loss calculation in json api.
- ElecticalSteel Material class.
- Optional Git hash export additional to PyDraft version number in simlation files.

### Changed
- Selection of dq matrix depended on winding system rotation direction.
- torque calculation method defaults to Arkkio; VW is optional.

### Fixed
- Dq-offset angle calculation adapted to new dq matrices.
- Test for tool box IPMSM class.
- Missing domain 'statorLam' in stator class.
- Check for equality of movingband radius by tolerance.
- Phase magnetic flux calculation by adding number of parallel paths

### Removed
- Linearity flag from Material init


## [1.2.9] - 2022-11-14
### Added
- Readded surface ids for identification of 3-segment airgap definition.
- Code (commented out) to plot boundary for debugging.

### Changed
- Workaround for including of Onelab parameter ResDir in user defined post operation for B field on line export.
- Sign of rotor virtual work post processing. Post operation returned oposite torque result compared to the other 3 calculation methods.
- Setting of center point to single, global center point defined before geometry import.

### Fixed
- Bug in center point mesh due to global center point.


## [1.2.8.post3] - 2022-11-04
### Added
- Number of parallel paths to json api
- global center point in json api (0,0,0)

### Changed
- Code appearance according to pylint (snakeCase naming style).
- Position of swat-em method overriding to pydraft init.
- Some classes privat attributes to class properties.

### Fixed
- Inner limit line setting in case of shaft without inner radius in json api.


## [1.2.8.post2]  - 2022-10-28
### Added
- Function to calculate dq-offset angle (experimental).
- Function to recombine curves of surface line loop.
- General plot function to plot list of Transformables.
- Number of parallel winding paths to simulation parameters.
- Distinction between Airgap and AirArea in api airgap.
- Function to automatically generate a uml diagram.

### Changed
- Project structure to meet recomendation from https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application.
- Split up code of json api into several files.

### Fixed
- Moving band mesh visibility in post processing.
- Toolkit test scripts.
- Version error in init_config_dict function.
- Torque calculation via virtual work principle due to missing symmetry factor.
- findGmsh function call on runOnelab import.
- brad, btan post processing evaluation OnGrid.


## [1.2.8.post1]
### Added
- SWAT-EM module for winding definition.
- function override in swat-em for correct phase order calculation (calc_phaseangle_starvoltage()).
- park offset angle as onelab parameter.

### Changed
- import of version in init_environment.

### Fixed
- bug in lineloop sorting due to line-list modification.
- Movingband line names detection due to new definition of airgap surfaces (5 segments).

### Removed
- Watchman class due to error with missing Tkinter package.


## [1.2.8] - 2022-08-03
### Added
- copying of mesh from primary to secondary boundary line in case of symmetry.
- parametric mesh size setting of movingband lines by 'number of mesh segments in movingband'.
- PhysicalElement parent class init in child classes.
- Change of stator field rotation direction to allways rotate CCW.
- Periodic mesh constraint for boundary lines (Primeary, Secondary and Movingband lines).
- Radius attribute to Movingband class.
- Functions to combine lines and surfaces.

### Changed
- Setting of winding layout via swat-em winding object in stator class.
- Slot class structure. Removed winding dict.
- some getter and setter functions to more python syntax using '@property' and '@property.setter'.
- Equal operator for line and surface. Lines and Surfaces are equal, if all points/lines are matching.
- Geometry generation via dict instead of list, because surfaces can be identified more easily. Less physical elements because constructor gets surface list from dict.
- mesh coloring of physicals.

### Fixed
- Order of machine domain generation due to protection of boundary line IDs.


## [1.2.7.post2] - 2022-07-12
### Added
- import of POS files in SP (scalar point) format.
- Script function to return pro file path.
- Plot for Machine class.
- Spline curves.

### Changed
- Key name for surface mesh size setting in api from "MeshSize" to "Meshsize"
- Formatting of Gmsh/GetDP instance (point, line, surface,...) names to C-like variable names in Script

### Fixed
- Bug in Material linearity flag setting
- Name setting in API PostOperation
- Imports in Script class by new type_checking method from typing module.


## [1.2.7] - 2022-06-24
### Added
- some mesh settings in GEO file.
- user defined post operation generation througth script class.
- call of user defined post operation to cmd command generation.
- import for result DAT files with "RegionValue" formatted content (VW Torque).
- function to reset the machine geometry in a Script object.
- setting of Onelab parameters in cmd command generation.
- option to set mesh size of surface in API.
- plot of moving geometry in gmsh GUI while simulation is runing.
- generation of compound mesh code for iron and airgap segmented surfaces.

### Changed
- not using placeholder for import of calculation file in PRO script anymore.
- init of Script, so no machine object is needed to instantiate a script object.

### Fixed
- error on initial rotation (must occure before moving band is meshed).
- error in material print for value 'None'.


## [1.2.6] - 2022-03-07
### Added
- class SurfaceAPI inherit from surface to store and evaluate the additional surface data.
- temperature scaling of remanence flux density Br of PM material.
- new parameter to control analysis type via API.
- optional operation in magstadyn file to remove previous result files.
- function getAngle in CircleArc to get the angle between start and end point.
- temperature coefficient for Br in Material class.
- function isTool in Surface to check is a surface is subtracted.
- overloaded isequal operation in Material.

### Changed
- API data exchange via JSON file instead of csv files. Geometry and simulation parameters are exchanged via two separate JSON files now.
- Simulation information by dict for easier parameter handling.
- function plotAllTimeTableDat to opionally not show the generated figures (just saving).
- defintion of BH-curve via ndarray in Material.
- material code generation. Some general improvements (getter and setter,...).

### Fixed
- evaluation of rotor position and current (I_A,B,C) with correct time step.
- getAllPoints also accounts for center points now.

### Removed
- unnecessary code for csv files in API

## [1.2.5] - 2022-02-21
### Added
- material database ("new") as json file
- new attibutes in material class
- lamination domain to calculate eddy current losses
- error if csv folder in api call is not a folder.
- optional second order basis function in template files (number of integration points in Integration section must be >1!)
- setter for (point) mesh length in line and surface class

### Changed
- evaluation of radial airgap flux density to only on first timestep.
- IPMSM-tool kit files to new script workflow

### Fixed
- bug when generating lines with similar start and end point
- bug when generating circle arc with points of different radius (start and endpoint dont have the same distance to the given center point)

### Removed
- unused variables and attributes in Script class.

## [1.2.4.post2] - 2022-02-01
### Added
- compute command option description
- test for import of pos files

### Fixed
- attachment of data to brad btan pos files

## [1.2.4.post1] - 2022-01-31

### Fixed
- attachment of data to brad btan pos files

### Removed
- .vscode folder from build

## [1.2.4] - 2022-01-31
### Added
- flag to decide if gmsh GUI should be opened.
- flag "debug" for additional debugging post operations in getdp.
- print of pydraft version number in created simulation files.
- global mesh size factor for points.

### Changed
- location of magstadyn file now in model folder so this folder is independed from the local location of the magstadyn file.
- removed working directory and tests from build

## [1.2.3] - 2022-01-17
### Added
- new plot function for simulation results in dat file format.

### Changed
- name of function findGmsh to findExe with exe name as variable.

### Fixed
- current density calculation in getdp template.

## [1.2.2] - 2022-01-11
### Added
- some more simulation parameters to the script.
- new onelab parameter resID to generate subfolders in the results dir.
- external mesh setting options through api

### Changed
- updated several parts of api due to script changes.

## [1.2.1] - 2021-12-16
### Added
- generation of parameter file to script.
- default parameter dict to script init module.

### Changed
- is* function of children of physicalElement to overwritten function getType.
- Moved some slot parameters to simulation parameters (like current and frequency).

## [1.2.0] - 2021-12-08
### Added
- new script generation process. Script now consists of template pro file, parameter geo file and magstadyn file. Script calls addMachine which creates the machine domains and adds the physical elements to the script instance. Groups are defined so the match the magstadyn file groups.

### Changed
- domain generation in rotor and stator due to new script method.
- attributes of slot to winding dict.
- command-line interface with argparse module


## [1.1.6] - 2021-11-09
### Added
- improvements to the script function by only grouping the used domains.
- some debugging outputs to check why so many geo instances are duplicated.
The reason is due to rotation and duplication interface points and lines are duplicated (basically all lines inside the geometry are interface lines). Tried to fix the duplication, but its not that easy. The whole geometry process would be needed to be redone.


## [1.1.5] - 2021-10-19
### Added
- findGmsh function.
- new layout of repository for valid python project.

### Changed
- subtracting algorithm from OpenCascade to build-in geometry kernel (gmsh).
- definition of the symmetry factor in motor kit.

### Fixed
- pythonic imports.


## [1.1.4] - 2021-10-05
### Added
- surface name in geo file generation.
- function in material module to print material infomation to command line.
- more functionality to api (physicals generation like slot and magnet).
- plot function to geo objects.

### Changed
- mue_r of material failing to export set to 1.

### Fixed
- duplicate of geo-object instead of rotated geo-object in rotateDuplicate.
- import error because of too imprecise number export (maximal export precision; 17 digits).
- domain creation order so boundary lines are not overwritten.
- material "air" import.


## [1.1.3] - 2021-09-27
### Added
- name cleaning for invalid ONELAB formated names.
- functions for boundary identification and generation.
- module runOnelab in function sub-package to open and run geo files.
- init module to api package.

### Changed
- rotate and duplicate function to account for any geo instance.
- split up API test in single and multi motor test.


## [1.1.2] - 2021-09-21
### Added
- identification of primary-(/master-)line in api.
- function in point class to calculate the distance to another point.
- function to identify movingband radius (to differ between rotor and stator surfaces).
- secondary-(slave-)line creation in api.
- center point as default rotation center.

### Changed
- repository client; moved from svn to git via git-svn.


## [1.1.1] - 2021-09-08
### Added
- functions for material import in pydraft

### Removed
- function for start and endpoint in CircleArc because its allready defined in line (unnecessary redefinition)


## [1.1.0] - 2021-09-06
### Added
- own export function for lineloops to be able to export different line lengths.
- new python sub-package "api" in pydraft.
- importResults module

### Changed
- export csv function to additionally export material name, angle and quantity of surface.

### Fixed
- magnet export; added ID and name for magnets to differentiate them


## [1.0.5] - 2021-08-05
### Added
- internal workshop files.

### Changed
- absolute picture paths to relativ paths in documentation.


## [1.0.4] - 2021-06-24
### Added
- new slot form "Form03" (might be spoke type magnet slot).

### Fixed
- Movingband definition in IPMSM class.


## [1.0.3] - 2021-05-03
### Added
- API for pydraft via csv files.
- more documentation.
- fist version of API to FreeCAD.
- cut method for surfaces in script class.


## [1.0.2] - 2021-02-09
### Added
- IPMSM class and some tests.
- new magnetization directions "parallel" and "tangential".
- some more documentation.

### Changed
- code format with black.
- path setting for python so path to pydraft is set automatically.


## [1.0.1] - 2020-12-09
### Added
- Template magstadyn.pro file with comments.
- Software_V2 folder.
- Doku-folder with docu as html.
- requirements file.
- test for step import.

### Changed
- material allocation; moved it from surface to group class.
- database import from xls to sql


## [1.0.0] - 2020-06-09
### Added
- All the code and documentation from PyDraft "Version 1 (V1)".
