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
	*	- pA
		- pA_deg * deg2rad
	*	- Flag_ConstantSource
		- 0
	*	- pB
		- pA - 2 * Pi / 3
	*	- pC
		- pA + 2 * Pi / 3
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
		- | (nbrRotorBars > 0),
		  | Name StrCat[INPUT_ANA_SETTINGS, "00Machine Type"], 
		  | Choices {SYNCHRONOUS = "Synchronous", ASYNCHRONOUS = "Asynchronous"},
		  | Visible Flag_Debug, ReadOnly 1
	*	- Flag_AnalysisType
		- ANALYSIS_TYPE, Name StrCat[INPUT_ANA_SETTINGS, "01Analysis Type"],Choices{STATIC = "Static", TRANSIENT = "Transient"}
	*	- Flag_SrcType_Stator
		- 1, Name StrCat[INPUT_ANA_SETTINGS, "02Source Input Type"],Choices{1 = "Current Source"}, Visible Flag_ExpertMode
	*	- initrotor_pos
		- INIT_ROTOR_POS, Name StrCat[INPUT_ANA_SETTINGS, "04Initial rotor position"],Visible Flag_ExpertMode,Units "deg mech"
	*	- RPM
		- SPEED_RPM, Name StrCat[INPUT_ANA_SETTINGS, "09Rotational Speed"],Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,Units "min^-1"
	*	- d_theta
		- (RPM!=0) ? ANGLE_INCREMENT : 0. ,Name StrCat[INPUT_ANA_SETTINGS, "05Angle Increment [mech deg]"],Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,ReadOnly RPM==0
	*	- nbrStatorPeriods
		- 10,Name StrCat[INPUT_ANA_SETTINGS, "07Number of Stator Periods"],Visible Flag_AnalysisType == TRANSIENT && (MachineType==ASYNCHRONOUS || RPM == 0),Help "Number of stator periods to determine simulation time"
	*	- nbrStepsPerPeriod
		- 90,Name StrCat[INPUT_ANA_SETTINGS, "08Time steps stator period"],Visible Flag_AnalysisType == TRANSIENT && RPM == 0,Help "Number of stator periods to determine simulation time"
	*	- finalrotor_pos
		- (RPM==0) ?initrotor_pos: (MachineType==SYNCHRONOUS) ?(FINAL_ROTOR_POS):(nbrStatorPeriods*360/NbrPolePairs+initrotor_pos),Name StrCat[INPUT_ANA_SETTINGS, "06Final rotor position"],Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,ReadOnly MachineType==ASYNCHRONOUS,Help "Final rotor position",Units "deg mech"
	*	- NbSteps
		- (RPM != 0) ?Ceil[(finalrotor_pos - initrotor_pos) / (d_theta) + 1]: (nbrStatorPeriods*nbrStepsPerPeriod + 1),Name StrCat[INPUT_ANA_SETTINGS, "10Number of Time Steps"],Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,ReadOnly 1
	*	- SymmetryFactor
		- SYMMETRY_FACTOR, Name StrCat[INPUT_ANA_SETTINGS, "Symmetry Factor"],ReadOnly 1,Visible Flag_Debug
	*	- Flag_SaveAllSteps
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "01Save all time steps"],Help "Save each field results (pos) in a separate file with time step index",Choices {0,1},Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT
	*	- res
		- Str[PATH_RES],Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "02Results folder path"],Help "Main results folder path where the results of the simulationwill be stored. This folder will be created by GetDP if it does notexist yet. Use 'Results folder name' to create a result subfolder."
	*	- ResId
		- "/", Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "03Results folder name"],Help "Name of the directory inside the results folder, where the resultfiles of THIS simulation should be stored. This directory will beautomatically created by GetDP."
	*	- Flag_ClearResults
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "04Delete previous result files"],Choices {0,1}
	*	- Flag_PrintFields
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "05Show Local Fields"],Choices{0, 1}
	*	- Flag_Calculate_ONELAB
		- 1, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "06Calculate torque: Arrkios method"],Choices {0,1},Help "ONELAB implementation of Arrkios method.",Visible Flag_ExpertMode
	*	- Flag_Calculate_VW
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "07Calculate torque: Virtual Work"],Choices {0,1},Visible Flag_ExpertMode
	*	- Flag_Inductance
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "08Compute inductances"],Choices{0, 1}
	*	- Flag_diffInductance
		- 1, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "09Inductance Computation Type"],Choices{0 = "Apparent", 1 = "Incremental"},Visible Flag_Inductance
	*	- Flag_SaveSolution
		- 0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "10Save Solution"],Choices{0, 1},Visible Flag_ExpertMode,Help StrCat["If Save Solution is active, the vector potential solution for each time ","step will be saved to a .res file. This is time consuming! For faster ","calculation, it is recommended to deactivate."]
	*	- r_rotor_airgap
		- R_ROTOR_AIRGAP, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "/Airgap Field/Rotor Radius"],Min 0,Visible Flag_PrintFields,Help "Define the radius of the rotor airgap for the post-processing of B_rad and B_tan."
	*	- r_stator_airgap
		- R_STATOR_AIRGAP, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "/Airgap Field/Stator Radius"],Min 0,Visible Flag_PrintFields,Help "Define the radius of the stator airgap for the post-processing of B_rad and B_tan."
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
		- FLAG_NL, Name StrCat[INPUT_MAT_PROPERTIES, "Non-linear B-H curves"],Choices{0, 1},Visible Flag_ExpertMode,Help "If this parameter is checked (=1), then the non-linear B-H curvesare used. Otherwise the non-linearity is replaced (extrapolated) bya constant mu_r."
	*	- nbrTurns
		- NBR_TURNS_IN_FACE,Name StrCat[INPUT_ELEC_WINDINGS, "01Number of wires per slot surface"],Help "Number of wires in a single slot surface"
	*	- NbrParallelPaths
		- NBR_PARALLEL_PATHS, Name StrCat[INPUT_ELEC_WINDINGS, "02Number of parallel paths per phase"],ReadOnly !Flag_ExpertMode
	*	- Flag_invertRotDir
		- FLAG_CHANGE_ROT_DIR, Name StrCat[INPUT_ELEC_EXCITATION, "05Invert rotation Direction"],Choices{0, 1},Visible Flag_ExpertMode
	*	- ID_RMS
		- Id_eff, Name StrCat[INPUT_ELEC_EXCITATION, "00ID_RMS"],Units "A",Visible Flag_SrcType_Stator == 1 && MachineType==SYNCHRONOUS
	*	- ID
		- ID_RMS * Sqrt[2], Name StrCat[INPUT_ELEC_EXCITATION, "02ID"],Units "A",Visible Flag_Debug && Flag_SrcType_Stator == 1 && MachineType==SYNCHRONOUS,ReadOnly 1
	*	- IQ_RMS
		- Iq_eff,Name StrCat[INPUT_ELEC_EXCITATION, "01IQ_RMS"],Units "A",Visible Flag_SrcType_Stator == 1 && MachineType==SYNCHRONOUS
	*	- IQ
		- IQ_RMS * Sqrt[2],Name StrCat[INPUT_ELEC_EXCITATION, "03IQ"],Units "A",Visible Flag_Debug && Flag_SrcType_Stator == 1 && MachineType==SYNCHRONOUS,ReadOnly 1
	*	- I0
		- 0, Name StrCat[INPUT_ELEC_EXCITATION, "04I0"],Units "A",Visible Flag_ExpertMode && Flag_SrcType_Stator==1 && MachineType==SYNCHRONOUS
	*	- ParkOffset
		- ParkAngOffset, Name StrCat[INPUT_ELEC_EXCITATION, "06Stator dq-System Offset [deg elec]"],Min -360, Max 360, Step 10,Visible Flag_ExpertMode && MachineType==SYNCHRONOUS
	*	- I_eff
		- Sqrt[ID_RMS^2 + IQ_RMS^2], Name StrCat[INPUT_ELEC_EXCITATION, "00Stator Phase Current (RMS)"],Units "A",Visible Flag_SrcType_Stator == 1 && MachineType==ASYNCHRONOUS
	*	- freq_rotor
		- 5, Name StrCat[INPUT_ELEC_EXCITATION, "01Rotor Frquency"],Units "Hz",Visible Flag_SrcType_Stator == 1 && MachineType==ASYNCHRONOUS
	*	- Flag_ParkTransformation
		- Flag_SrcType_Stator == TRANSIENT && MachineType==SYNCHRONOUS,Name StrCat[INPUT_ELEC_EXCITATION, "Use Clark-Park-Transformation"],Choices {0,1},ReadOnly 1
	*	- VV
		- 12,Name StrCat[INPUT_ELEC, "V [V]"],Units "V",Visible Flag_SrcType_Stator == 2
	*	- R_wire
		- 0, Name StrCat[INPUT_ELEC, "Connection Resistance [Ohm]"],Visible Flag_Cir
	*	- CircuitConnection
		- 0, Name StrCat[INPUT_ELEC, "Winding Type"],Choices{0 = "Star Connection", 1 = "Delta Connection"},Visible Flag_Cir
	*	- pA_deg
		- 0, Name StrCat[INPUT_ELEC, "Current System Offset"],Units "deg",Help "Offset angle for (sinusoidal) stator phase currents",Visible !Flag_ParkTransformation
	*	- Flag_Cir_RotorCage
		- (nbrRotorBars > 0) , Choices{0,1},Name StrCat(INPUT_ELEC_CIRCUIT_ROTOR,"Circuit/10Use circuit in rotor cage"),Visible (nbrRotorBars > 0)
	*	- R_endring_segment
		- 0.836e-6,Name StrCat[INPUT_ELEC_CIRCUIT_ROTOR,"Circuit/11Resistance of endring segment [Ohm]"],ReadOnly !Flag_Cir_RotorCage,Help "This must be given for a single endring segment!During processing the value is scaled to 1 meter because inthe electromagnetic formulation the resulting voltage drop given to thecircuit is in V/m!",Visible (nbrRotorBars>0)
	*	- L_endring_segment
		- 4.8e-9,Name StrCat[INPUT_ELEC_CIRCUIT_ROTOR,"Circuit/12Inductance of endring segment [H]"],ReadOnly !Flag_Cir_RotorCage,Help "This must be given for a single endring segment!During processing the value is scaled to 1 meter because inthe electromagnetic formulation the resulting voltage drop given to thecircuit is in V/m!",Visible (nbrRotorBars>0)
	*	- tempMag
		- TEMP_MAG,Name StrCat[INPUT_MAT_PROPERTIES_MAGNET, "Magnet temperature [°C]"],Visible Flag_ExpertMode && NbrRegions[Rotor_Magnets] > 0
	*	- freq_stator
		- (MachineType==SYNCHRONOUS)?(n * NbrPolePairs):freq_rotor + NbrPolePairs * n,Name StrCat[INPUT_ELEC_EXCITATION, "Stator Frequency"],Units "Hz",ReadOnly 1
	*	- n_sync
		- freq_stator / NbrPolePairs,Name StrCat[INPUT_ELEC_EXCITATION, "Synchronous Speed"],Units "Hz",ReadOnly 1,Visible MachineType == ASYNCHRONOUS
	*	- slip
		- 1 - n/n_sync,Name StrCat[INPUT_ELEC_EXCITATION, "Slip"],ReadOnly 1,Visible MachineType == ASYNCHRONOUS
	*	- R_
		- "Analysis", Name "GetDP/1ResolutionChoices", Visible Flag_Debug
	*	- C_
		- "-solve Analysis -v 3 -v2",Name "GetDP/9ComputeCommand",Visible Flag_Debug || Flag_ExpertMode
	*	- P_
		- "", Name "GetDP/2PostOperationChoices", Visible Flag_Debug

