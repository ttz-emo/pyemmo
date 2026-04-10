ONELAB Model Constants
''''''''''''''''''''''

.. list-table::
	:widths: 12 28
	:header-rows: 1

	*	- Constant Name
		- Value
	*	- Flag_EW
		- 0
	*	- Flag_3D
		- 0
	*	- Flag_Fault
		- 0
	*	- deg2rad
		- Pi / 180
	*	- rad2deg
		- 1 / deg2rad
	*	- nbrSlots
		- NBR_SLOTS
	*	- NbrPolesTot
		- NBR_POLE_PAIRS * 2
	*	- NbrPolePairs
		- NbrPolesTot / 2
	*	- Flag_MB
		- 1
	*	- r_AG
		- R_AIRGAP
	*	- nbrMagnets
		- NbrRegions[Rotor_Magnets]
	*	- nbrRotorBars
		- NbrRegions[Rotor_Bars]
	*	- Flag_Lam
		- 0
	*	- x_n
		- x_(n-1) + relaxation_factor*(x_clac-x_(n-1))
	*	- eccentircity_static_m
		- eccentricity_static * mm
	*	- eccentricity_dynamic_m
		- eccentricity_dynamic * mm
	*	- NbrMbSegments
		- GetNumber[StrCat[INPUT_MESH
	*	- GlobalMeshsizeFactor
		- GetNumber[StrCat[INPUT_MESH
	*	- pA
		- pA_deg * deg2rad
	*	- Flag_ConstantSource
		- 0
	*	- Va
		- VV
	*	- Vb
		- VV
	*	- Vc
		- VV
	*	- asm_finalrotor_pos
		- 360*(nbrStatorPeriods/freq_stator)*n
	*	- NbrPhases
		- 3
	*	- FillFactor_Winding
		- 1
	*	- Factor_R_3DEffects
		- 1
	*	- Flag_SrcType_StatorA
		- Flag_SrcType_Stator
	*	- Flag_SrcType_StatorB
		- Flag_SrcType_Stator
	*	- Flag_SrcType_StatorC
		- Flag_SrcType_Stator
	*	- Flag_ImposedSpeed
		- 1
	*	- ResDir
		- AbsolutePath[ StrCat[res

ONELAB Model Parameters
'''''''''''''''''''''''

.. list-table::
	:widths: 12 28
	:header-rows: 1

	*	- Parameter Name
		- Description
	*	- Flag_ExpertMode
		- 1, Name "01View/Expert Mode", Choices {0, 1}
	*	- Flag_Debug
		- 0, Name "01View/Debug", Choices {0,1}
	*	- MachineType
		- (nbrRotorBars > 0), Name StrCat[INPUT_ANA_SETTINGS, "00Machine Type"],Choices {SYNCHRONOUS = "Synchronous", ASYNCHRONOUS = "Asynchronous"},Visible Flag_Debug,ReadOnly 1,Highlight "LightGray"
	*	- Flag_AnalysisType
		- ANALYSIS_TYPE, Name StrCat[INPUT_ANA_SETTINGS, "01Analysis Type"],Choices{ STATIC = "Static", TRANSIENT = "Transient" }
	*	- Flag_SrcType_Stator
		- CURRENT_SOURCE,Name StrCat[INPUT_ANA_SETTINGS, "02Source Input Type"],Choices{CURRENT_SOURCE = "Current Source",VOLTAGE_SOURCE = "Voltage Source"},Visible Flag_ExpertMode
	*	- initrotor_pos
		- INIT_ROTOR_POS, Name StrCat[INPUT_ANA_SETTINGS, "04Initial rotor position"],Visible Flag_ExpertMode,Units "deg mech"
	*	- RPM
		- SPEED_RPM, Name StrCat[INPUT_ANA_SETTINGS, "09Rotational Speed"],Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,Units "min^-1"
	*	- d_theta
		- (RPM!=0) ? ANGLE_INCREMENT : 0. ,Name StrCat[INPUT_ANA_SETTINGS, "05Angle Increment"],Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,ReadOnly RPM==0,Units "deg mech"
	*	- nbrStatorPeriods
		- 10,Name StrCat[INPUT_ANA_SETTINGS, "07Number of Stator Periods"],Visible Flag_AnalysisType == TRANSIENT && (MachineType==ASYNCHRONOUS || RPM == 0),Help "Number of stator periods to determine simulation time"
	*	- nbrStepsPerPeriod
		- 90,Name StrCat[INPUT_ANA_SETTINGS, "08Time steps stator period"],Visible Flag_AnalysisType == TRANSIENT && RPM == 0,Help "Number of stator periods to determine simulation time"
	*	- finalrotor_pos
		- (RPM==0) ?initrotor_pos: (MachineType==SYNCHRONOUS) ?(FINAL_ROTOR_POS):(nbrStatorPeriods*360/NbrPolePairs+initrotor_pos),Name StrCat[INPUT_ANA_SETTINGS, "06Final rotor position"],Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,ReadOnly MachineType==ASYNCHRONOUS,Highlight StrChoice[MachineType==ASYNCHRONOUS, "LightGray", "White"],Help "Final rotor position",Units "deg mech"
	*	- NbSteps
		- (RPM != 0) ?Ceil[(finalrotor_pos - initrotor_pos) / (d_theta) + 1]: (nbrStatorPeriods*nbrStepsPerPeriod + 1),Name StrCat[INPUT_ANA_SETTINGS, "10Number of Time Steps"],Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,ReadOnly 1,Highlight "LightGray"
	*	- SymmetryFactor
		- SYMMETRY_FACTOR, Name StrCat[INPUT_ANA_SETTINGS, "Symmetry Factor"],ReadOnly 1,Highlight "LightGray",Visible Flag_Debug
	*	- Flag_SaveAllSteps
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "01Save all time steps"],Help "Save each field results (pos) in a separate file with time step index",Choices {0,1},Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT
	*	- res
		- Str[PATH_RES],Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "02Results folder path"],Help StrCat("Main results folder path where the results of the simulation ","will be stored. This folder will be created by GetDP if it does not ","exist yet. Use 'Results folder name' to create a result subfolder.")
	*	- ResId
		- "/", Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "03Results folder name"],Help StrCat("Name of the directory inside the results folder, where the result ","files of THIS simulation should be stored. This directory will be ","automatically created by GetDP.")
	*	- Flag_ClearResults
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "04Delete previous result files"],Choices {0,1}
	*	- Flag_ClearViews
		- 1,Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "05Delete all field plots"],Choices{0,1}
	*	- Flag_PrintFields
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "06Show Local Fields"],Choices{0, 1}
	*	- Flag_Calculate_ONELAB
		- 1, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "07Calculate torque: Arrkios method"],Choices {0,1},Help "ONELAB implementation of Arrkios method.",Visible Flag_ExpertMode
	*	- Flag_Calculate_VW
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "08Calculate torque: Virtual Work"],Choices {0,1},Visible Flag_ExpertMode
	*	- Flag_Inductance
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "09Compute inductances"],Choices{0, 1}
	*	- Flag_diffInductance
		- 1, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "10Inductance Computation Type"],Choices{0 = "Apparent", 1 = "Incremental"},Visible Flag_Inductance
	*	- Flag_SaveSolution
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "11Save Solution"],Choices{0, 1},Visible Flag_ExpertMode,Help StrCat["If Save Solution is active, the vector potential solution for each time ","step will be saved to a .res file. This is time consuming! For faster ","calculation, it is recommended to deactivate."]
	*	- Flag_EC_Magnets
		- CALC_MAGNET_LOSSES, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT_LOSS,"02Calculate Eddy Current in Magnets (2D)"],Choices{0, 1},Visible (Flag_ExpertMode && nbrMagnets > 0),Help "Consider Eddy-Current in the PMs"
	*	- Flag_SecondOrder
		- 0, Name StrCat[INPUT_SOLVER_SETTINGS, "01Second Order Basis Function"],Choices {0,1},Visible Flag_ExpertMode
	*	- Nb_max_iter
		- 30, Name "Nonlinear solver/Max. num. iterations", Visible 0
	*	- stop_criterion
		- 1e-4, Name "Nonlinear solver/Stopping criterion", Visible 0
	*	- relaxation_factor
		- 1, Name "Nonlinear solver/Relaxation factor", Visible 0
	*	- AxialLength_S
		- L_AX_S,Name StrCat[INPUT_GEO_STATOR, "Stator axial length"],Help "Axial length of the stator active material in m",Units "m"
	*	- AxialLength_R
		- L_AX_R,Name StrCat[INPUT_GEO_ROTOR, "Rotor axial length"],Help "Axial length of the rotor active material in m",Units "m"
	*	- Flag_NL
		- FLAG_NL, Name StrCat[INPUT_MAT_PROPERTIES, "Non-linear B-H curves"],Choices{0, 1},Visible Flag_ExpertMode,Help StrCat("If this parameter is checked (=1), then the non-linear B-H curves ","are used. Otherwise the non-linearity is replaced (extrapolated) by a ","constant mu_r.")
	*	- eccentricity_static
		- 0.0, Name StrCat[INPUT_GEO, "Static Eccentricity"],Unit "mm",ReadOnly SymmetryFactor != 1,Help StrCat("The stator will elements be translated by this in -x direction. ","Make sure that the sum of static and dynamic eccentricity are not greater ","than the movingband height! ","This can only be used in a full model (symmetry = 1).")
	*	- eccentricity_dynamic
		- 0.0, Name StrCat[INPUT_GEO, "Dynamic Eccentricity"],Unit "mm",ReadOnly SymmetryFactor != 1,Help StrCat("Dynamic eccentircity in mm. The rotor initial position will be ","translated by this in x-direction, while still rotating the rotor elements ","around the origin. ","Make sure that the sum of static and dynamic eccentricity are not greater ","than the movingband height! ","This can only be used in a full model (symmetry = 1).")
	*	- nbrTurns
		- NBR_TURNS_IN_FACE,Name StrCat[INPUT_ELEC_WINDINGS, "01Number of wires per slot surface"],Help StrCat("Number of wires in a single slot surface.","If the slot is divided in several surfaces, the value needs to match the ","number of wires in each surface.")
	*	- NbrParallelPaths
		- NBR_PARALLEL_PATHS, Name StrCat[INPUT_ELEC_WINDINGS, "02Number of parallel paths per phase"],ReadOnly !Flag_ExpertMode,Help "Number of parallel paths per phase."
	*	- R_S
		- 2 * L_AX_S * 0.4 * (nbrTurns*nbrSlots/3)^2 / (0.25/3*(1.6^2+1)*r_AG^2*Pi) / sigma_cu,Name StrCat[INPUT_ELEC_WINDINGS, "03Resistance"],Units "Ohm",Help StrCat("Stator winding phase resistance for voltage source simulation. ","Default value is calculated by a empirical formula based on the machine geometry and number of winding turns.","If possible, this should be defined by the user!"),Visible (Flag_SrcType_Stator==VOLTAGE_SOURCE)
	*	- FillFactor_Winding
		- 1, Name StrCat[INPUT_ELEC_WINDINGS, "03Fill factor"],Help "Winding fill factor from (0,1]. UNUSED FOR NOW!",Max 1,Visible ((Flag_SrcType_Stator == VOLTAGE_SOURCE) && 0)
	*	- Factor_R_3DEffects
		- 1, Name StrCat[INPUT_ELEC_WINDINGS, "04End winding factor"],Help "UNUSED FOR NOW! Factor from [0, inf) to scale stator winding resistance due to end winding region",Visible ((Flag_SrcType_Stator == VOLTAGE_SOURCE) && 0)
	*	- Flag_invertRotDir
		- FLAG_CHANGE_ROT_DIR, Name StrCat[INPUT_ELEC_EXCITATION, "05Invert rotation Direction"],Choices{0, 1},Visible Flag_ExpertMode,Help "Invert the stator field rotation direction by changing phase offset in source definition."
	*	- ID_RMS
		- Id_eff, Name StrCat[INPUT_ELEC_EXCITATION, "00ID_RMS"],Units "A",Visible Flag_SrcType_Stator == CURRENT_SOURCE && MachineType==SYNCHRONOUS
	*	- ID
		- ID_RMS * Sqrt[2], Name StrCat[INPUT_ELEC_EXCITATION, "02ID"],Units "A",Visible Flag_Debug && Flag_SrcType_Stator == CURRENT_SOURCE && MachineType==SYNCHRONOUS,ReadOnly 1,Highlight "LightGray"
	*	- IQ_RMS
		- Iq_eff,Name StrCat[INPUT_ELEC_EXCITATION, "01IQ_RMS"],Units "A",Visible Flag_SrcType_Stator == CURRENT_SOURCE && MachineType==SYNCHRONOUS
	*	- IQ
		- IQ_RMS * Sqrt[2],Name StrCat[INPUT_ELEC_EXCITATION, "03IQ"],Units "A",Visible Flag_Debug && Flag_SrcType_Stator == CURRENT_SOURCE && MachineType==SYNCHRONOUS,ReadOnly 1,Highlight "LightGray"
	*	- I0
		- 0, Name StrCat[INPUT_ELEC_EXCITATION, "04I0"],Units "A",Visible Flag_ExpertMode && Flag_SrcType_Stator==1 && MachineType==SYNCHRONOUS
	*	- ParkOffset
		- ParkAngOffset, Name StrCat[INPUT_ELEC_EXCITATION, "06Stator dq-System Offset [deg elec]"],Min -360, Max 360, Step 10,Visible Flag_ExpertMode && MachineType==SYNCHRONOUS,Help "Stator dq0 offset angle to align with rotor dq0 axis."
	*	- I_eff
		- Sqrt[ID_RMS^2 + IQ_RMS^2], Name StrCat[INPUT_ELEC_EXCITATION, "00Stator Phase Current (RMS)"],Units "A",Visible Flag_SrcType_Stator == CURRENT_SOURCE && MachineType==ASYNCHRONOUS,Help "Stator phase current (rms)"
	*	- freq_rotor
		- 5, Name StrCat[INPUT_ELEC_EXCITATION, "02Rotor Frequency"],Units "Hz",Visible MachineType==ASYNCHRONOUS,Help "Electrical rotor frequency for induction machine."
	*	- Flag_Cir
		- 0, Name StrCat[INPUT_ELEC_EXCITATION, "02Use Stator Circuit"],Choices {0,1},Visible Flag_SrcType_Stator == VOLTAGE_SOURCE
	*	- Flag_ParkTransformation
		- Flag_SrcType_Stator == CURRENT_SOURCE && MachineType==SYNCHRONOUS,Name StrCat[INPUT_ELEC_EXCITATION, "Use Clark-Park-Transformation"],Choices {0,1},ReadOnly 1,Highlight "LightGray"
	*	- VV
		- 12, Name StrCat[INPUT_ELEC_EXCITATION, "00Input Voltage Amplitude"],Units "V",Visible Flag_SrcType_Stator == VOLTAGE_SOURCE,Help "Amplitude of the input voltage (in case of voltage input)"
	*	- R_wire
		- 500e-3, Name StrCat[INPUT_ELEC_EXCITATION, "05Connection (Wire-)Resistance"],Units "Ohm",Visible Flag_Cir,Help StrCat("Connection resistance between voltage source and machine ","(cable and connection resistance).")
	*	- R_terminal
		- 1e12, Name StrCat[INPUT_ELEC_EXCITATION, "06Terminal Connection Resistance"],Units "Ohm",Help StrCat["Terminal connection resistance to account for in short circuit case. ","Only used when source is CEMF in circuit!"],Visible Flag_SrcType_Stator == CEMF_SOURCE
	*	- CircuitConnection
		- 0, Name StrCat[INPUT_ELEC_WINDINGS, "03Winding Type"],Choices{STAR_CONNECTION = "Star Connection", DELTA_CONNECTION = "Delta Connection" },Visible Flag_Cir,Help "Voltage source circuit connection type"
	*	- pA_deg
		- 0, Name StrCat[INPUT_ELEC_EXCITATION, "01Current System Offset"],Units "deg",Help "Offset angle for (sinusoidal) stator phase currents/voltages",Visible !Flag_ParkTransformation
	*	- Flag_Cir_RotorCage
		- (nbrRotorBars > 0) , Choices{0,1},Name StrCat(INPUT_ELEC_CIRCUIT_ROTOR,"Circuit/10Use circuit in rotor cage"),Visible (nbrRotorBars > 0),Help StrCat("Use circuit to connect rotor bars with endring resistance and inductance. ","Otherwise the bars will be ideally connected (without any reactance).")
	*	- R_endring_segment
		- 0.836e-6,Name StrCat[INPUT_ELEC_CIRCUIT_ROTOR,"Circuit/11Resistance of endring segment [Ohm]"],ReadOnly !Flag_Cir_RotorCage,Help StrCat("This must be given for a single endring segment! ","During processing the value is scaled to 1 meter because in ","the electromagnetic formulation the resulting voltage drop given to the ","circuit is in V/m!"),Visible (nbrRotorBars>0)
	*	- L_endring_segment
		- 4.8e-9,Name StrCat[INPUT_ELEC_CIRCUIT_ROTOR,"Circuit/12Inductance of endring segment [H]"],ReadOnly !Flag_Cir_RotorCage,Help StrCat("This must be given for a single endring segment! ","During processing the value is scaled to 1 meter because in ","the electromagnetic formulation the resulting voltage drop given to the ","circuit is in V/m!"),Visible (nbrRotorBars>0)
	*	- tempMag
		- TEMP_MAG,Name StrCat[INPUT_MAT_PROPERTIES_MAGNET, "Magnet temperature [degrees C]"],Visible Flag_ExpertMode && NbrRegions[Rotor_Magnets] > 0
	*	- freq_stator
		- (MachineType==SYNCHRONOUS)?(n * NbrPolePairs):freq_rotor + NbrPolePairs * n,Name StrCat[INPUT_ELEC_EXCITATION, "Stator Frequency"],Units "Hz",ReadOnly 1,Highlight "LightGray"
	*	- n_sync
		- freq_stator / NbrPolePairs,Name StrCat[INPUT_ELEC_EXCITATION, "Synchronous Speed"],Units "Hz",ReadOnly 1,Highlight "LightGray",Visible MachineType == ASYNCHRONOUS
	*	- slip
		- 1 - n/n_sync,Name StrCat[INPUT_ELEC_EXCITATION, "Slip"],ReadOnly 1,Highlight "LightGray",Visible MachineType == ASYNCHRONOUS
	*	- Flag_Relaxation
		- 1, Name StrCat[INPUT_ELEC_EXCITATION, "Use Voltage Relaxation"],Choices {0,1},Visible Flag_SrcType_Stator==VOLTAGE_SOURCE && Flag_ExpertMode,Help "Control relaxation of voltage. This is useful to decrease the transient times when simulating with voltages."
	*	- NbTrelax
		- 2, Name StrCat[INPUT_ELEC_EXCITATION, "Voltage Relaxation Periods"],Min 0, Step 1,Visible Flag_SrcType_Stator==VOLTAGE_SOURCE && Flag_ExpertMode,Help "Number of periods while relaxation is applied. This is useful to decrease the transient times when simulating with voltages."
	*	- R_
		- "Analysis", Name "GetDP/1ResolutionChoices", Visible Flag_Debug
	*	- C_
		- "-solve Analysis -v 3 -v2",Name "GetDP/9ComputeCommand",Visible Flag_Debug || Flag_ExpertMode
	*	- P_
		- "", Name "GetDP/2PostOperationChoices", Visible Flag_Debug
