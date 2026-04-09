// This script has initally be written by Diogo Pinto and is adapted for the use with pyemmo by Max Ganser

Include PARAMETER_FILE

// Strings defining the Parameter tree =========================================
// Options for the Analysis Setting
INPUT_ANA_SETTINGS = "Input/01Analysis Parameters/";
INPUT_ANA_SETTINGS_OUTPUT =StrCat[INPUT_ANA_SETTINGS, "99Results/"];
INPUT_ANA_SETTINGS_OUTPUT_LOSS =StrCat[INPUT_ANA_SETTINGS_OUTPUT, "Losses/"];

INPUT_SOLVER_SETTINGS = "Input/02Solver Parameters/";
INPUT_SOLVER_SETTINGS_NL = StrCat[INPUT_SOLVER_SETTINGS, "99Nonlinear solver/"];

// For Geometrical Parameters
INPUT_GEO = "Input/03Geometry/";
INPUT_GEO_ROTOR = StrCat[INPUT_GEO, "01Rotor/"];
INPUT_GEO_ROTOR_POLESHAPING = StrCat[INPUT_GEO_ROTOR, "01Pole Shaping/"];
INPUT_GEO_ROTOR_SLOT = StrCat[INPUT_GEO_ROTOR, "02Slot/"];
INPUT_GEO_STATOR = StrCat[INPUT_GEO, "02Stator/"];
INPUT_GEO_MAGNET = StrCat[INPUT_GEO, "03Magnet/"];

INPUT_MESH = "Input/04Mesh/";

INPUT_ELEC = "Input/05Electrical Parameters/";
INPUT_ELEC_WINDINGS = StrCat[INPUT_ELEC, "01Windings/"];
INPUT_ELEC_EXCITATION = StrCat[INPUT_ELEC, "02Excitation/"];
INPUT_ELEC_CIRCUIT_ROTOR = StrCat[INPUT_ELEC, "03Rotor Cage Circuit/"];

// For Material Properties
INPUT_MAT_PROPERTIES = "Input/06Material Properties/";
INPUT_MAT_PROPERTIES_MAGNET = StrCat[INPUT_MAT_PROPERTIES, "Magnets/"];
INPUT_MAT_PROPERTIES_CORE = StrCat[INPUT_MAT_PROPERTIES, "Rotor Core/"];
INPUT_MAT_PROPERTIES_STATOR = StrCat[INPUT_MAT_PROPERTIES, "Stator/"];

mm = 1e-3;

// PARAMETER: MachineType
SYNCHRONOUS = 0;
ASYNCHRONOUS = 1;

// PARAMETER: Flag_AnalysisType
TRANSIENT = 1;
STATIC = 0;

// PARAMETER: CircuitConnection
STAR_CONNECTION = 0;
DELTA_CONNECTION = 1;

// PARAMETER: Flag_SrcType_Stator
CURRENT_SOURCE = 1; // standard current source (no circuit)
VOLTAGE_SOURCE = 2; // voltage source (with circuit)
CEMF_SOURCE = 0; // back EMF in circuit

// If the model is moved to a different folder and the default res folder does not exist
// anymore, update the result folder to be the current folder:
If (! FileExists[Str[PATH_RES]])
    PATH_RES = AbsolutePath[StrCat[CurrentDir, "res"]];
EndIf

// Some script constants which are currently unused:
DefineConstant[
    sigma_al = 3.72e7, // conductivity of aluminum [S/m]
    sigma_cu = 5.8e7  // conductivity of copper [S/m]
    sigma_fe = 1.0e7, // conductivity of iron [S/m]

    Flag_EW = 0,
    Flag_3D = 0,
    Flag_Fault = 0, // Calculate short circuit in phase A

    deg2rad = Pi / 180,
    rad2deg = 1 / deg2rad,

    // In order to be able to use the machine_magstadyn_a.pro file which is included
    // in onelab, we will have to define some additional constants number of
    // NbrPolesTot in the model
    nbrSlots = NBR_SLOTS,
    NbrPolesTot = NBR_POLE_PAIRS * 2,
    NbrPolePairs = NbrPolesTot / 2,
    Flag_MB = 1, // Allways use Movingband!
    r_AG = R_AIRGAP // Rotor airgap radius at the interface of the moving band
    //Flag_Link = 0 			// Use Link Constraint - is not used in magstatdyn...
];
//=============================================================================
//============================= DOMAIN DEFINITION =============================
//=============================================================================
Group
{
    DefineGroup[
        Domain_Lam, // part of the domain which is laminated
        Rotor_Magnets,
        Stator_Ind_Am, Stator_Ind_Bm, Stator_Ind_Cm,
        Stator_Ind_Ap, Stator_Ind_Bp, Stator_Ind_Cp,
        Rotor_Bars,
        Domain_SurfCoil // Domain for single slot surface area calculation
    ];
}

GROUP_CODE
//=============================================================================
//=========================== END DOMAIN DEFINITION ===========================
//=============================================================================

//=============================================================================
// ====================== ANALYSIS AND SOLVER PARAMETERS ======================
//=============================================================================
DefineConstant[
    nbrMagnets = NbrRegions[Rotor_Magnets],  // number of rotor magnet domains
    nbrRotorBars = NbrRegions[Rotor_Bars],   // number of rotor bar domains

    Flag_ExpertMode = {1, Name "01View/Expert Mode", Choices {0, 1}},

    Flag_Debug = {0, Name "01View/Debug", Choices {0,1}},

    MachineType = {
        (nbrRotorBars > 0), Name StrCat[INPUT_ANA_SETTINGS, "00Machine Type"],
        Choices {SYNCHRONOUS = "Synchronous", ASYNCHRONOUS = "Asynchronous"},
        Visible Flag_Debug,
        ReadOnly 1,
        Highlight "LightGray"
    },

    Flag_AnalysisType = {
        ANALYSIS_TYPE, Name StrCat[INPUT_ANA_SETTINGS, "01Analysis Type"],
        Choices{ STATIC = "Static", TRANSIENT = "Transient" }
    },

    Flag_SrcType_Stator = {
        CURRENT_SOURCE,
        Name StrCat[INPUT_ANA_SETTINGS, "02Source Input Type"],
        Choices{
            CURRENT_SOURCE = "Current Source",
            VOLTAGE_SOURCE = "Voltage Source"
            // CEMF_SOURCE = "Back EMF in Circuit"
        },
        Visible Flag_ExpertMode
    },


    initrotor_pos = {
        INIT_ROTOR_POS, Name StrCat[INPUT_ANA_SETTINGS, "04Initial rotor position"],
        Visible Flag_ExpertMode,
        Units "deg mech"
    },

    RPM = {
        SPEED_RPM, Name StrCat[INPUT_ANA_SETTINGS, "09Rotational Speed"],
        Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,
        Units "min^-1"
    },

    d_theta = {
        (RPM!=0) ? ANGLE_INCREMENT : 0. ,
        Name StrCat[INPUT_ANA_SETTINGS, "05Angle Increment"],
        Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,
        ReadOnly RPM==0,
        Units "deg mech"
    },


    // ASYNCHRONOUS
    nbrStatorPeriods = {
        10,
        Name StrCat[INPUT_ANA_SETTINGS, "07Number of Stator Periods"],
        Visible Flag_AnalysisType == TRANSIENT && (MachineType==ASYNCHRONOUS || RPM == 0),
        Help "Number of stator periods to determine simulation time"
    },
    nbrStepsPerPeriod = {
        90,
        Name StrCat[INPUT_ANA_SETTINGS, "08Time steps stator period"],
        Visible Flag_AnalysisType == TRANSIENT && RPM == 0,
        Help "Number of stator periods to determine simulation time"
    },
    // END ASYNCHRONOUS

    // SYNCHRONOUS
    finalrotor_pos = {
        (RPM==0) ?
            initrotor_pos
            : (MachineType==SYNCHRONOUS) ?
                (FINAL_ROTOR_POS)
                :(nbrStatorPeriods*360/NbrPolePairs+initrotor_pos),
        Name StrCat[INPUT_ANA_SETTINGS, "06Final rotor position"],
        Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,
        ReadOnly MachineType==ASYNCHRONOUS,
        Highlight StrChoice[MachineType==ASYNCHRONOUS, "LightGray", "White"],
        Help "Final rotor position",
        Units "deg mech"
    },
    // END SYNCHRONOUS

    NbSteps = {
        (RPM != 0) ?
            Ceil[(finalrotor_pos - initrotor_pos) / (d_theta) + 1]
            : (nbrStatorPeriods*nbrStepsPerPeriod + 1),
        Name StrCat[INPUT_ANA_SETTINGS, "10Number of Time Steps"],
        Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT,
        ReadOnly 1,
        Highlight "LightGray"
    },

    SymmetryFactor = {
        SYMMETRY_FACTOR, Name StrCat[INPUT_ANA_SETTINGS, "Symmetry Factor"],
        ReadOnly 1,
        Highlight "LightGray",
        Visible Flag_Debug
    },

    Flag_Symmetry = SymmetryFactor > 1,
    NbrPolesInModel = (Flag_Symmetry) ? NbrPolesTot / SymmetryFactor : NbrPolesTot,

    // -------------------------------------------------------------------------
    // -------------------- ANALYSIS - OUTPUT SETTINGS -------------------------
    // -------------------------------------------------------------------------

    Flag_SaveAllSteps = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "01Save all time steps"],
        Help "Save each field results (pos) in a separate file with time step index",
        Choices {0,1},
        Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT
    },

    res = {
        Str[PATH_RES],
        Name StrCat[
            INPUT_ANA_SETTINGS_OUTPUT, "02Results folder path"
        ],
        Help StrCat("Main results folder path where the results of the simulation ",
            "will be stored. This folder will be created by GetDP if it does not ",
            "exist yet. Use 'Results folder name' to create a result subfolder.")
    }

    ResId = {
        "/", Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "03Results folder name"],
        Help StrCat("Name of the directory inside the results folder, where the result ",
            "files of THIS simulation should be stored. This directory will be ",
            "automatically created by GetDP.")
    },

    Flag_ClearResults = {
        0, Name StrCat[
            INPUT_ANA_SETTINGS_OUTPUT, "04Delete previous result files"
        ],
        Choices {0,1}
    },

    Flag_ClearViews = {
        1,
        Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "05Delete all field plots"],
        Choices{0,1}
    },


    Flag_PrintFields = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "06Show Local Fields"],
        Choices{0, 1}
    },

    Flag_Calculate_ONELAB = {
        1, Name StrCat[
            INPUT_ANA_SETTINGS_OUTPUT, "07Calculate torque: Arrkios method"
        ],
        Choices {0,1},
        Help "ONELAB implementation of Arrkios method.",
        Visible Flag_ExpertMode
    },

    Flag_Calculate_VW = {
        0, Name StrCat[
            INPUT_ANA_SETTINGS_OUTPUT, "08Calculate torque: Virtual Work"
        ],
        Choices {0,1},
        Visible Flag_ExpertMode
    },

    Flag_Inductance = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "09Compute inductances"],
        Choices{0, 1}
    },

    Flag_diffInductance = {
        1, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "10Inductance Computation Type"],
        Choices{0 = "Apparent", 1 = "Incremental"},
        Visible Flag_Inductance
    },

    Flag_SaveSolution = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "11Save Solution"],
        Choices{0, 1},
        Visible Flag_ExpertMode,
        Help StrCat[
            "If Save Solution is active, the vector potential solution for each time ",
            "step will be saved to a .res file. This is time consuming! For faster ",
            "calculation, it is recommended to deactivate."
        ]
    },

    // r_rotor_airgap = {
    //     R_ROTOR_AIRGAP, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "/Airgap Field/Rotor Radius"],
    //     Min 0,
    //     Visible Flag_PrintFields,
    //     Help "Define the radius of the rotor airgap for the post-processing of B_rad and B_tan."
    // },

    // r_stator_airgap = {
    //     R_STATOR_AIRGAP, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "/Airgap Field/Stator Radius"],
    //     Min 0,
    //     Visible Flag_PrintFields,
    //     Help "Define the radius of the stator airgap for the post-processing of B_rad and B_tan."
    // },

    Flag_Lam = 0, // FIXME: Not using lamination eddy current calculation yet!
    // Flag_Lam = {
    // 0, Name StrCat[
    //     INPUT_ANA_SETTINGS_OUTPUT_LOSS, "01Calculate Eddy Current in Laminations"
    // ],
    // Choices{0, 1},
    // Visible Flag_ExpertMode && Flag_AnalysisType == TRANSIENT
    // },

    Flag_EC_Magnets = {
        CALC_MAGNET_LOSSES, Name StrCat[
            INPUT_ANA_SETTINGS_OUTPUT_LOSS,
            "02Calculate Eddy Current in Magnets (2D)"
        ],
        Choices{0, 1},
        Visible (Flag_ExpertMode && nbrMagnets > 0),
        Help "Consider Eddy-Current in the PMs"
    },

    // -------------------------------------------------------------------------
    // -------------------- ANALYSIS - SOLVER SETTINGS -------------------------
    // -------------------------------------------------------------------------

    // Flag to set second order basis function:
    Flag_SecondOrder = {
        0, Name StrCat[INPUT_SOLVER_SETTINGS, "01Second Order Basis Function"],
        Choices {0,1},
        Visible Flag_ExpertMode
    },
    Nb_max_iter = {
        60,
        Name StrCat[INPUT_SOLVER_SETTINGS_NL, "Max. num. iterations"],
        // Visible Flag_NL,
        Help "Maximum number of iterations in the Newton-Raphson method."
        },

    // solver will stop when Norm((Ax-b)/x) < stop_criterion
    stop_criterion = {
        1e-7, Name StrCat[INPUT_SOLVER_SETTINGS_NL, "Stopping criterion"],
        //   Visible Flag_NL,
        Help "Stop criterion for Newton-Raphson method. Solver will stop when Norm((Ax-b)/x) < stop_criterion."
    },

    // In the newton raphson method, the relaxation factor determines the new x
    // to be in the next iteration if x_(n-1) is the solution of the previous
    // iteration, x_calc the new calculated solution, then
    //      x_n = x_(n-1) + relaxation_factor*(x_clac-x_(n-1))
    relaxation_factor = {
        1, Name StrCat[INPUT_SOLVER_SETTINGS_NL, "Relaxation factor"],
        //  Visible Flag_NL,
        Help "Relaxation Factor for Newton-Raphson method."
    }
];

// If(Flag_SrcType_Stator == 2)
//     // Constant to model short-circuit in winding
//     // => only when we impose the voltage
//     DefineConstant[
//         Flag_Fault = {0,
//             Name StrCat[INPUT_ANA_SETTINGS, "Fault Condition to model",
//             Choices{0 = "none", 1 = "Short Circuit A-B"}}
//     ];
// EndIf
//=============================================================================
// ==================== END ANALYSIS AND SOLVER PARAMETERS ====================
//=============================================================================

Printf("Number of poles total (NbrPolesTot) = %.0f", NbrPolesTot);
Printf("Number of poles in Model = %.0f", NbrPolesInModel);
Printf("Symmetry Faktor = %.0f", SymmetryFactor);
Printf("Flag Symmetry = %.0f", Flag_Symmetry);
Printf("Airgap radius = %.5f", r_AG);

//=============================================================================
//============================ MACHINE PARAMETERS =============================
//=============================================================================
DefineConstant[
    AxialLength_S = {L_AX_S,
                     Name StrCat[INPUT_GEO_STATOR, "Stator axial length"],
                     Help "Axial length of the stator active material in m",
                     Units "m"},
    AxialLength_R = {L_AX_R,
                     Name StrCat[INPUT_GEO_ROTOR, "Rotor axial length"],
                     Help "Axial length of the rotor active material in m",
                     Units "m"},

    // determine if we want to calculate using a linear or non-linear material
    Flag_NL = {
        FLAG_NL, Name StrCat[INPUT_MAT_PROPERTIES, "Non-linear B-H curves"],
        Choices{0, 1},
        Visible Flag_ExpertMode,
        Help StrCat("If this parameter is checked (=1), then the non-linear B-H curves ",
            "are used. Otherwise the non-linearity is replaced (extrapolated) by a ",
            "constant mu_r.")
        },
    eccentricity_static = {
        0.0, Name StrCat[INPUT_GEO, "Static Eccentricity"],
        Unit "mm",
        ReadOnly SymmetryFactor != 1,
        Help StrCat("The stator will elements be translated by this in -x direction. ",
            "Make sure that the sum of static and dynamic eccentricity are not greater ",
            "than the movingband height! ",
            "This can only be used in a full model (symmetry = 1).")
        },
    eccentircity_static_m = eccentricity_static * mm,
    eccentricity_dynamic = {
        0.0, Name StrCat[INPUT_GEO, "Dynamic Eccentricity"],
        Unit "mm",
        ReadOnly SymmetryFactor != 1,
        Help StrCat("Dynamic eccentircity in mm. The rotor initial position will be ",
            "translated by this in x-direction, while still rotating the rotor elements ",
            "around the origin. ",
            "Make sure that the sum of static and dynamic eccentricity are not greater ",
            "than the movingband height! ",
            "This can only be used in a full model (symmetry = 1).")
        },
    // tranlate to meter
    eccentricity_dynamic_m = eccentricity_dynamic * mm,
    // Get number of movingband segments from .geo file to use in PostOperations
    NbrMbSegments = GetNumber[StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"], 360],
    GlobalMeshsizeFactor = GetNumber[StrCat[INPUT_MESH, "00Mesh size factor"], 1.0]
];
Printf("eccentricity_dynamic = %.6e mm", eccentricity_dynamic);
Printf("eccentricity_static =  %.6e mm", eccentricity_static);
Printf("Number of Movingband Segments (for PostProcessing) = %.0f", NbrMbSegments);
Printf("Global mesh size factor (for PostProcessing) = %.0f", GlobalMeshsizeFactor);

//=============================================================================
//========================== END MACHINE PARAMETERS ===========================
//=============================================================================

//=============================================================================
//========================== EXCITATION PARAMETERS ============================
//=============================================================================

DefineConstant[
    //========================== WINDING PARAMETERS ==========================

    nbrTurns = {
        NBR_TURNS_IN_FACE,Name StrCat[
            INPUT_ELEC_WINDINGS, "01Number of wires per slot surface"
        ],
        Help StrCat(
            "Number of wires in a single slot surface.",
            "If the slot is divided in several surfaces, the value needs to match the ",
            "number of wires in each surface."
            )
    },

    NbrParallelPaths = {
        NBR_PARALLEL_PATHS, Name StrCat[
            INPUT_ELEC_WINDINGS, "02Number of parallel paths per phase"
        ],
        ReadOnly !Flag_ExpertMode,
        Help "Number of parallel paths per phase."
    },

    R_S = {
        2 * L_AX_S * 0.4 * (nbrTurns*nbrSlots/3)^2 / (0.25/3*(1.6^2+1)*r_AG^2*Pi) / sigma_cu,
        Name StrCat[INPUT_ELEC_WINDINGS, "03Resistance"],
        Units "Ohm",
        Help StrCat(
            "Stator winding phase resistance for voltage source simulation. ",
            "Default value is calculated by a empirical formula based on the machine geometry and number of winding turns.",
            "If possible, this should be defined by the user!"
        ),
        Visible (Flag_SrcType_Stator==VOLTAGE_SOURCE)
    }

    FillFactor_Winding = {
        1, Name StrCat[
            INPUT_ELEC_WINDINGS, "03Fill factor"
        ],
        Help "Winding fill factor from (0,1]",
        Max 1,
        Visible Flag_SrcType_Stator == VOLTAGE_SOURCE
    },
    Factor_R_3DEffects = {
        1, Name StrCat[
            INPUT_ELEC_WINDINGS, "04End winding factor"
        ],
        Help "Factor from [0, inf) to scale stator winding resistance due to end winding region",
        Visible Flag_SrcType_Stator == VOLTAGE_SOURCE
    },

    //======================== EXCITATION PARAMETERS =========================

    Flag_invertRotDir = {
        FLAG_CHANGE_ROT_DIR, Name StrCat[
            INPUT_ELEC_EXCITATION, "05Invert rotation Direction"
        ],
        Choices{0, 1},
        Visible Flag_ExpertMode,
        Help "Invert the stator field rotation direction by changing phase offset in source definition."
    },
    // IF SYNCHRONOUS
    ID_RMS = {
        Id_eff, Name StrCat[INPUT_ELEC_EXCITATION, "00ID_RMS"],
        Units "A",
        Visible Flag_SrcType_Stator == 1 && MachineType==SYNCHRONOUS
    },

    ID = {
        ID_RMS * Sqrt[2], Name StrCat[INPUT_ELEC_EXCITATION, "02ID"],
        Units "A",
        Visible Flag_Debug && Flag_SrcType_Stator == 1 && MachineType==SYNCHRONOUS,
        ReadOnly 1,
        Highlight "LightGray"
    },

    IQ_RMS = {
        Iq_eff,Name StrCat[INPUT_ELEC_EXCITATION, "01IQ_RMS"],
        Units "A",
        Visible Flag_SrcType_Stator == 1 && MachineType==SYNCHRONOUS
    },

    IQ = {
        IQ_RMS * Sqrt[2],Name StrCat[INPUT_ELEC_EXCITATION, "03IQ"],
        Units "A",
        Visible Flag_Debug && Flag_SrcType_Stator == 1 && MachineType==SYNCHRONOUS,
        ReadOnly 1,
        Highlight "LightGray"
    },

    I0 = {
        0, Name StrCat[INPUT_ELEC_EXCITATION, "04I0"],
        Units "A",
        Visible Flag_ExpertMode && Flag_SrcType_Stator==1 && MachineType==SYNCHRONOUS
    },

    ParkOffset = {
        ParkAngOffset, Name StrCat[
            INPUT_ELEC_EXCITATION, "06Stator dq-System Offset [deg elec]"
        ],
        Min -360, Max 360, Step 10,
        Visible Flag_ExpertMode && MachineType==SYNCHRONOUS,
        Help "Stator dq0 offset angle to align with rotor dq0 axis."
    },
    // Else if MachineType is ASYNCHRONOUS
    // For async we define rotor frequency and rms phase current
    I_eff = {
        Sqrt[ID_RMS^2 + IQ_RMS^2], Name StrCat[
            INPUT_ELEC_EXCITATION, "00Stator Phase Current (RMS)"
        ],
        Units "A",
        Visible Flag_SrcType_Stator == 1 && MachineType==ASYNCHRONOUS,
        Help "Stator phase current (rms)"
    },

    freq_rotor = {
        5, Name StrCat[
            INPUT_ELEC_EXCITATION, "01Rotor Frquency"
        ],
        Units "Hz",
        Visible MachineType==ASYNCHRONOUS,
        Help "Electrical rotor frequency for induction machine."
    },


    //======================== CIRCUIT PARAMETERS =========================
    // STATOR CIRCUIT

    // Variable controlling if the current density in the windings is imposed
    // (via current) or calculated (volatge imposed, or back-emf calculation in
    // circuit)
    Flag_ImposedCurrentDensity = (Flag_SrcType_Stator == CURRENT_SOURCE),
    // are the windings connected via an external circuit
    // Flag_Cir = (!Flag_ImposedCurrentDensity),
    Flag_Cir = {
        0, Name StrCat[INPUT_ELEC_EXCITATION, "02Use Stator Circuit"],
        Choices {0,1},
        Visible Flag_SrcType_Stator == VOLTAGE_SOURCE
    },


    // Use the Park transformation
    Flag_ParkTransformation = {
        // current source and synchronous machine
        Flag_SrcType_Stator == TRANSIENT && MachineType==SYNCHRONOUS,
        Name StrCat[INPUT_ELEC_EXCITATION, "Use Clark-Park-Transformation"],
        Choices {0,1},
        ReadOnly 1,
        Highlight "LightGray"
    },

    VV = {
        12, Name StrCat[INPUT_ELEC_EXCITATION, "Input Voltage Amplitude"],
        Units "V",
        Visible Flag_SrcType_Stator == VOLTAGE_SOURCE,
        Help "Amplitude of the input voltage (in case of voltage input)"
    },

    R_wire = {
        500e-3, Name StrCat[INPUT_ELEC_EXCITATION, "Connection (Wire-)Resistance"],
        Units "Ohm",
        Visible Flag_Cir,
        Help StrCat("Connection resistance between voltage source and machine ",
            "(cable and connection resistance).")
    },

    R_terminal = {
        1e12, // Default value is very high so its like open circuit if not set
        Name StrCat[INPUT_ELEC_EXCITATION, "Terminal Connection Resistance"],
        Units "Ohm",
        Help StrCat[
            "Terminal connection resistance to account for in short circuit case. ",
            "Only used when source is CEMF in circuit!"
        ],
        Visible Flag_SrcType_Stator == CEMF_SOURCE // Only if source type is back-emf
    }

    CircuitConnection = {
        0, Name StrCat[INPUT_ELEC_WINDINGS, "Winding Type"],
        Choices{
            STAR_CONNECTION = "Star Connection", // 0
            DELTA_CONNECTION = "Delta Connection" // 1
        },
        Visible Flag_Cir,
        Help "Voltage source circuit connection type"
    },

    // Phase angle of the voltage
    pA_deg = {
        0, Name StrCat[INPUT_ELEC_EXCITATION, "Current System Offset"],
        Units "deg",
        Help "Offset angle for (sinusoidal) stator phase currents/voltages",
        Visible !Flag_ParkTransformation
    },

    // conversion of the angles from deg to rad
    pA = pA_deg * deg2rad,
    Flag_ConstantSource = 0,
    pB = (Flag_invertRotDir) ? pA + 2 * Pi / 3 : pA - 2 * Pi / 3,
    pC = (Flag_invertRotDir) ? pA - 2 * Pi / 3 : pA + 2 * Pi / 3,
    Va = VV,
    Vb = VV,
    Vc = VV,

    // ROTOR CIRCUIT
    Flag_Cir_RotorCage = {(nbrRotorBars > 0) , Choices{0,1},
        Name StrCat(INPUT_ELEC_CIRCUIT_ROTOR,"Circuit/10Use circuit in rotor cage"),
        Visible (nbrRotorBars > 0),
        Help StrCat(
            "Use circuit to connect rotor bars with endring resistance and inductance. ",
            "Otherwise the bars will be ideally connected (without any reactance)."
            )
        // ReadOnly (Flag_SrcType_Stator==1)
    },

    R_endring_segment = {0.836e-6,
        Name StrCat[
            INPUT_ELEC_CIRCUIT_ROTOR,
            "Circuit/11Resistance of endring segment [Ohm]"
        ],
        ReadOnly !Flag_Cir_RotorCage,
        Help StrCat("This must be given for a single endring segment! ",
            "During processing the value is scaled to 1 meter because in ",
            "the electromagnetic formulation the resulting voltage drop given to the ",
            "circuit is in V/m!"),
        Visible (nbrRotorBars>0)
    },
    L_endring_segment = {4.8e-9,
        Name StrCat[
            INPUT_ELEC_CIRCUIT_ROTOR,
            "Circuit/12Inductance of endring segment [H]"
        ],
        ReadOnly !Flag_Cir_RotorCage,
        Help StrCat("This must be given for a single endring segment! ",
            "During processing the value is scaled to 1 meter because in ",
            "the electromagnetic formulation the resulting voltage drop given to the ",
            "circuit is in V/m!"),
        Visible (nbrRotorBars>0)
    }
];
//=============================================================================
//========================= END EXCITATION PARAMETERS =========================
//=============================================================================

//=============================================================================
//============================ MATERIAL PARAMETERS ============================
//=============================================================================

DefineConstant[ //Material definitions
    tempMag = {
        TEMP_MAG,
        Name StrCat[INPUT_MAT_PROPERTIES_MAGNET, "Magnet temperature [degrees C]"],
        Visible Flag_ExpertMode && NbrRegions[Rotor_Magnets] > 0
    }
];

//=============================================================================
//========================== END MATERIAL PARAMETERS ==========================
//=============================================================================

// Printing some messages for information
Printf("Flag_Cir = %g", Flag_Cir);
Printf("Flag_SrcType_Stator = %g", Flag_SrcType_Stator);
Printf("Flag_ImposedCurrentDensity = %g", Flag_ImposedCurrentDensity);

Group
{
    // If we have endwindings in the 3D simulation then we need to include the
    // outer air and the region between the windings and the stack to the Stator_Air
    // Group. In that case, the coils need to be specified in a different manner
    // Each coil is split in 6 regions (because the current density vector has a different
    // expression in each region), and then there is one region to regroup the 6 regions
    // of each coil
    // If(Flag_EW)
    //     Stator_Air += Region[{OUTERAIR_S, EW_AIR}];
    //     For coil In{1 : nbrSlots}
    //         For reg In{1 : EndWindingReg + 2} Coil ~ { coil }
    //             ~{reg} = Region[{COILS_3D ~{coil} ~{reg}}];
    //             Coil ~{coil} += Region[{COILS_3D ~{coil} ~{reg}}];
    //         EndFor
    //         Coil_3D += Region[{Coil ~{coil}}];
    //     EndFor
    // EndIf

    // If(Flag_3D)
    //     // To surfaces of the motor when using 3D (Top => positive z)
    //     // Bottom z=0 (or negative z if we model the EW)
    //     Surf_Top = Region[{SURF_TOP}];
    //     Surf_Bottom = Region[{SURF_BOTTOM}];
    // EndIf

    // Assign the windings to the corresponding regions:
    If(!Flag_EW)
        // positive and negative conductors
        Stator_IndsN = Region[{Stator_Ind_Am, Stator_Ind_Bm, Stator_Ind_Cm}];
        Stator_IndsP = Region[{Stator_Ind_Ap, Stator_Ind_Bp, Stator_Ind_Cp}];
    Else
        // unused for now!
        For i In{0 : nbrSlots - 1}
            If(Phases(i) == 1)
                If(CoilDir(i) == 1)
                    Stator_Ind_Ap += Region[{Coil ~{i + 1}}];
                Else
                    Stator_Ind_Am += Region[{Coil ~{i + 1}}];
                EndIf
            EndIf
            If(Phases(i) == 2)
                If(CoilDir(i) == 1)
                    Stator_Ind_Bp += Region[{Coil ~{i + 1}}];
                Else
                    Stator_Ind_Bm += Region[{Coil ~{i + 1}}];
                EndIf
            EndIf
            If(Phases(i) == 3)
                If(CoilDir(i) == 1)
                    Stator_Ind_Cp += Region[{Coil ~{i + 1}}];
                Else
                    Stator_Ind_Cm += Region[{Coil ~{i + 1}}];
                EndIf
            EndIf
        EndFor
        Stator_IndsN = Region[{Stator_Ind_Am, Stator_Ind_Bm, Stator_Ind_Cm}];
        Stator_IndsP = Region[{Stator_Ind_Ap, Stator_Ind_Bp, Stator_Ind_Cp}];
    EndIf

    // regrouping all the conductors in 1 region
    Stator_Inds = Region[{Stator_IndsN, Stator_IndsP}];

    // regrouping the different phases into 1 group
    PhaseA = Region[{Stator_Ind_Am, Stator_Ind_Ap}];
    PhaseB = Region[{Stator_Ind_Bm, Stator_Ind_Bp}];
    PhaseC = Region[{Stator_Ind_Cm, Stator_Ind_Cp}];

    // for post processing reasons
    PhaseA_pos = Region[{Stator_Ind_Ap}];
    PhaseB_pos = Region[{Stator_Ind_Bp}];
    PhaseC_pos = Region[{Stator_Ind_Cp}];

	// If we use an external circuit we populate these regions in the Circuit.pro
	// file => otherwise we still need to define them in order to avoid an error
	// message by machine_magstadyn_a.pro
	Resistance_Cir 		= Region[{}];
	Capacitance_Cir 	= Region[{}];
	Inductance_Cir 		= Region[{}];
	DomainZt 			= Region[{}];
	DomainSource_Cir	= Region[{}];

    // Control eddy current calculation in magentic material
    If(!Flag_EC_Magnets)
        RotorCC += Region[{Rotor_Magnets}];
    Else
        RotorC += Region[{Rotor_Magnets}];
    EndIf

    // FIXME: Don't sort RotorBars into non-conducting or conducting domain!
    RotorC += Region[{Rotor_Bars}];
    RotorCC -= Region[{Rotor_Bars}];

    MovingBand_PhysicalNb = #0;

    // SOME 3D STUFF -  NOT USED YET
    // // In 3-D this corresponds to the surfaces making the 3-D colume of the conducting parts
    // Skin_DomainC = #{};
    // // Surfaces belonging to the volume in which eddy-currents can arise but for which the normal component of the b field to the surface is 0
    // // we need to define this surface since in 3-D this condition (Bn=0) can not be strongly verified. So it needs to be verified in a week for
    // Surf_EC_bn0 = #{};

    // // Surface if we would want to define a constant potential at one surface
    // Surf_elec = #{};

    // If(Flag_EC_Magnets)
    // // If we want to calculate eddy currents in the magnets, the skin of the magnets has to be included
    // Skin_DomainC += Region[{SKIN_DOMAINC}];

    // If(!Flag_EW)
    //     Surf_EC_bn0 += Region[{SURF_MAGNETS_EC0_BOTTOM}];
    // Else
    //     Skin_DomainC += Region[{SURF_MAGNETS_EC0_BOTTOM}];
    // EndIf

    // For the top Part we need to distingish if we exploit axial
    // symmetry or not.
    // If it is the case, then we add the top surface of the magnets to surface top
    // since we have that there is a bounday condition, else we need to add it to
    // Surf_EC_bn0.
    // If(!Flag_SymmetryLstk)
    //     If(!Flag_EW)
    //         Surf_EC_bn0 += Region[{SURF_MAGNETS_EC0_TOP}];
    //     Else
    //         Skin_DomainC += Region[{SURF_MAGNETS_EC0_TOP}];
    //     EndIf
    // Else
    //     //Surf_EC_bn0 += Region[{SURF_MAGNETS_EC0_TOP}];
    //     Surf_Top += Region[{SURF_MAGNETS_EC0_TOP}];
    // EndIf
    // Else
    //     If(!Flag_EW)
    //         // In the case in which there are no eddy currents in the magnets
    //         // we need to add this region which we left out of the boundary
    //         // condition because otherwise it would have been a too strong
    //         // constraint and the solver would have difficulties to converge in the case of EC
    //         // In the case without EC, the solution will be wrong! Some magnetic field leaving that surface
    //         // which makes no physical sense
    //         Surf_Bottom += Region[{SURF_MAGNETS_EC0_BOTTOM}];
    //         Surf_Top += Region[{SURF_MAGNETS_EC0_TOP}];
    //         // we only need to do that in the case without
    //         // endwindings as in that case there is normally a boundary condition
    //         // on that surface (SURF_MAGNETS_EC0), whereas this is not the case with EW (no BC on i that case on    that region)
    //     Else
    //         // In this case we have end windings, and if we only model half of the machine, we need to add  the magnet surface to the
    //         // Surf_Top group
    //         If(Flag_SymmetryLstk)
    //             Surf_Top += Region[{SURF_MAGNETS_EC0_TOP}];
    //         EndIf
    //     EndIf
    // EndIf
}

// FUNCTIONS TO BE DEFINED
Function
{
    DefineFunction[
        density, sigma
        Resistance, // If the resistance is known by measurement, it should be prefered, because its better to account for the end windings!
        // used in circuit:
        Inductance,
        Capacitance
    ];
}

Function{
    NbWires[] = nbrTurns;                                          // number of turns
    If(Flag_3D)
        // // unused for now!
        // SurfCoil[] = SurfaceArea[]{SURF_COND_STATOR} / (nbrSlots / SymmetryFactor * 2);
        // Surf_Airgap_r[] = SurfaceArea[]{MBR_AIR_SURF};
        // Surf_Airgap_s[] = SurfaceArea[]{MBS_AIR_SURF};
    Else
        RegionListAp() = GetRegions[Domain_SurfCoil]; // found new function GetRegions[] which retruns the group-list
        //                         RegionListAp(0): accesses the first element of the list which is a region number
        If (#RegionListAp()==0)
            // If Domain_SurfCoil is empty
            Printf(
                StrCat(
                    "WARNING: The Group 'Domain_SurfCoil' was empty! ",
                    "We need at least one single slot surface physical in Domain_SurfCoil ",
                    "to determine the slot surface for current density calculation!"
                )
            );
        Else
            SurfCoil[] = SurfaceArea[]{RegionListAp(0)}; // save the area of on coil(side) in SurfCoil for current density calculation
            // Surf_Airgap_r[] = SurfaceArea[]{Region[Rotor_Airgap]}; // seems to be unused
        EndIf
        If (MachineType==ASYNCHRONOUS) // && nbrRotorBars > 0
            RegionListBars() = GetRegions[Rotor_Bars];
            SurfBar[] = SurfaceArea[]{RegionListBars(0)};
        EndIf
    EndIf

    n = RPM / 60; // rotational frequency in Hz
    wr = n * 2 * Pi; // rotational speed in mec rad/s
    // supply frequency
    DefineConstant[
        freq_stator = {
            (MachineType==SYNCHRONOUS)?(n * NbrPolePairs):freq_rotor + NbrPolePairs * n,
            Name StrCat[INPUT_ELEC_EXCITATION, "Stator Frequency"],
            Units "Hz",
            ReadOnly 1,
            Highlight "LightGray"
        },
        n_sync = {
            freq_stator / NbrPolePairs,
            Name StrCat[INPUT_ELEC_EXCITATION, "Synchronous Speed"],
            Units "Hz",
            ReadOnly 1,
            Highlight "LightGray",
            Visible MachineType == ASYNCHRONOUS
        },
        slip = {
            1 - n/n_sync,
            Name StrCat[INPUT_ELEC_EXCITATION, "Slip"],
            ReadOnly 1,
            Highlight "LightGray",
            Visible MachineType == ASYNCHRONOUS
        }
        asm_finalrotor_pos = 360*(nbrStatorPeriods/freq_stator)*n
    ];
    If (MachineType==ASYNCHRONOUS && (n != 0))
        // Reset ONELAB parameters after calculating stator frequency
        // Reset final rotor position (we did not know fs before)
        Printf("finalrotor_pos -> asm_finalrotor_pos: %.5f -> %.5f", finalrotor_pos , asm_finalrotor_pos);
        SetNumber[
            StrCat[INPUT_ANA_SETTINGS, "06Final rotor position"],
            asm_finalrotor_pos
        ];
        SetNumber[
            StrCat[INPUT_ANA_SETTINGS, "10Number of Time Steps"],
            Ceil[(asm_finalrotor_pos - initrotor_pos) / (d_theta) + 1]
        ];
        // Update value to calculate correct parameters when loading script!
        // NOTE: GetNumber somehow does not give 0 when running GetDP from the
        // commandline, but workds in GUI... Resetting finalrotor_pos with asm variable.
        // finalrotor_pos = GetNumber[StrCat[INPUT_ANA_SETTINGS, "06Final rotor position"]];
        finalrotor_pos = asm_finalrotor_pos;
    EndIf
    Printf("Final rotor position is %.1f deg", finalrotor_pos);
    // electrical period
    T = 1 / freq_stator;
    // electrical pulsation
    Omega = 2 * Pi * freq_stator;
    // inital position in rad
    theta0 = initrotor_pos * deg2rad;
    // change in position between 2 time steps in rad
    delta_theta[] = d_theta * deg2rad;
    If (n != 0)
        // stop time of the simulation
        timemax = (finalrotor_pos - initrotor_pos) * deg2rad / wr;
        // final rotor position in rad
        thetaMax = finalrotor_pos * deg2rad;
        // time step
        delta_time = d_theta * deg2rad / wr;
    Else
        // Case: Speed n = 0 rpm
        timemax = nbrStatorPeriods * T;
        // final rotor position in rad
        thetaMax = theta0;
        // time step
        delta_time = T / nbrStepsPerPeriod;
    EndIf
    // start time
    time0 = 0;

    // variable containing the current rotor position => required to calculate the
    // magnetization direction of the magnets in rad. $Time is an internal variable
    // containing the current time
    // the $dtheta value is only used when generating the ec lamination tables!
    RotorPosition[] = initrotor_pos * deg2rad + $Time * wr + $dtheta * deg2rad;
    // current position in deg
    RotorPosition_deg[] = RotorPosition[] * rad2deg;
    // stuff for testing => possible extension to include block communtation
    RotorPos_deg_mod[] = NbrPolePairs * (RotorPosition_deg[] - 52.5) % 360;
    RotorPos_deg_mod_2[] = NbrPolePairs * (RotorPosition_deg[] - 52.5 + 120) % 360;
    RotorPos_deg_mod_3[] = NbrPolePairs * (RotorPosition_deg[] - 52.5 + 240) % 360;

    // For eddy-current loss calculation
    // FIXME: fix Fac_Lam calculation!
    // Fac_Lam[] = 0.043255350884945; // = sigma_Lam*d_Lam^2/12/density_Lam ;
    // Fac_Lam[] = sigma[]*d_Lam[]^2/12/density[] ;

    // In the case of a static eccentricity the initial rotor center is offset in the y axis
    // RotCenter_i[] = Vector[0, EccentSta, 0];
    RotCenter_i[] = Vector[0, 0, 0];
    // From there we can calculate the current position of the rotor center using the rotation matrix along Z, Rz
    Rz[] = Tensor[Cos[$1], -Sin[$1], 0,
                  Sin[$1], Cos[$1], 0,
                  0, 0, 1];
    RotCenter_Current[] = Rz[$Time * wr] * RotCenter_i[];

    // if the nbrSlots or NbrPolesTot are changed we have to change the offset
    // Theta_Park[]	= (RotorPosition[]-OFFSET*deg2rad)*NbrPolePairs;
    // Offset moved outside the brackets -> Offset in electrical degrees and in rotation direction.
    // (Rotation direction is defined by Park matrix in magstadyn file.)
    Theta_Park[] = RotorPosition[] * NbrPolePairs + (ParkOffset)*deg2rad;

    Theta_Park_deg[] = Theta_Park[] * rad2deg;

    // electrical period in (s)
    Period = 1 / freq_stator;

    DefineConstant[
        Flag_Relaxation = {
            1, Name StrCat[INPUT_ELEC_EXCITATION, "Use Voltage Relaxation"],
            Choices {0,1},
            Visible Flag_SrcType_Stator==VOLTAGE_SOURCE && Flag_ExpertMode,
            Help "Control relaxation of voltage. This is useful to decrease the transient times when simulating with voltages."
        },
        NbTrelax = {
            2, Name StrCat[INPUT_ELEC_EXCITATION, "Voltage Relaxation Periods"],
            Min 0, Step 1,
            Visible Flag_SrcType_Stator==VOLTAGE_SOURCE && Flag_ExpertMode,
            Help "Number of periods while relaxation is applied. This is useful to decrease the transient times when simulating with voltages."
        }
    ];

    Trelax = NbTrelax * Period;

    // To apply relaxation such that when we use a voltage supply, we do not apply max voltage at t=0
    Frelax[] = (!Flag_Relaxation || !Flag_NL || Flag_AnalysisType == STATIC || $Time > Trelax) ?
        1.
        : 0.5 * (1. - Cos[Pi * $Time / Trelax]);
}

FUNCTION_CODE

If(Flag_Cir || Flag_Cir_RotorCage)
    // include circuit constraints for the stator and rotor circuit
    Include "Circuit.pro";
EndIf

// load 2D or 3D problem
// Include DEFAULT_PRO_FILE
