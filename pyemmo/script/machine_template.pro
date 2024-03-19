// This script has initally be written by Diogo Pinto and is adapted for the use with pyemmo by Max Ganser

Include PARAMETER_FILE

// Strings defining the Parameter tree =========================================
// Options for the Analysis Setting
INPUT_ANA_SETTINGS = "Input/01Analysis Parameters/";
INPUT_ANA_SETTINGS_OUTPUT =StrCat[INPUT_ANA_SETTINGS, "99Results/"];

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

// Some script constants which are currently unused:
DefineConstant[
    Flag_EW = 0,
    Flag_3D = 0,
    Flag_Cir = 0,
    deg2rad = Pi / 180,
    rad2deg = 1 / deg2rad
];

//=============================================================================
// ====================== ANALYSIS AND SOLVER PARAMETERS ======================
//=============================================================================
DefineConstant[
    Flag_ExpertMode = {
        1,
        Name '01View/Expert Mode',
        Choices {0, 1}
    },

    Flag_Debug = {1, Name "01View/Debug", Choices {0,1}},

    Flag_AnalysisType = {
        ANALYSIS_TYPE, Name StrCat[INPUT_ANA_SETTINGS, "01Analysis Type"],
        Choices{0 = "Static", 1 = "Transient"}
    },

    Flag_SrcType_Stator = {
        1, Name StrCat[INPUT_ANA_SETTINGS, "02Source Input Type"],
        Choices{1 = "Current Source"}, // Only current source for now
        // Choices{1 = "Current Source", 2 = "Voltage Source", 0 = "back EMF in Circuit"},
        Visible Flag_ExpertMode
    },

    initrotor_pos = {
        INIT_ROTOR_POS, Name StrCat[INPUT_ANA_SETTINGS, "04Initial rotor position"],
        Visible Flag_ExpertMode,
        Units "deg mech"
    },

    d_theta = {
        ANGLE_INCREMENT, Name StrCat[INPUT_ANA_SETTINGS, "05Angle Increment [mech deg]"],
        Visible Flag_ExpertMode && Flag_AnalysisType==1
    },

    finalrotor_pos = {
        FINAL_ROTOR_POS, Name StrCat[INPUT_ANA_SETTINGS, "06Final rotor position"],
        Visible Flag_ExpertMode && Flag_AnalysisType==1,
        Help "Final rotor position",
        Units "deg mech"
    },

    NbSteps = {
        Ceil[(finalrotor_pos - initrotor_pos) / (d_theta) + 1],
        Name StrCat[INPUT_ANA_SETTINGS, "07Number of Time Steps"],
        Visible Flag_ExpertMode &&Flag_AnalysisType,
        ReadOnly 1
    },

    RPM = {
        SPEED_RPM, Name StrCat[INPUT_ANA_SETTINGS, "08Rotational Speed [RPM]"],
        Visible Flag_ExpertMode &&Flag_AnalysisType
    },

    SymmetryFactor = SYMMETRY_FACTOR,
    Flag_Symmetry = SymmetryFactor > 1,

    // Flag_Symmetry = {SymmetryFactor > 1,
    //             Choices{0, 1},
    //             Name StrCat[INPUT_ANA_SETTINGS, "91Use symmetry"],
    //             ReadOnly 1,
    //             Visible Flag_ExpertMode},

    // -------------------------------------------------------------------------
    // -------------------- ANALYSIS - OUTPUT SETTINGS -------------------------
    // -------------------------------------------------------------------------

    Flag_SaveAllSteps = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "01Save all time steps"],
        Help "Save each field results (pos) in a separate file with time step index",
        Choices {0,1},
        Visible Flag_ExpertMode && Flag_AnalysisType==1
    },

    Flag_ClearResults = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "02Delete previous result files"],
        Choices {0,1},
        Visible Flag_ExpertMode
    },

    Flag_Calculate_ONELAB = {
        1, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "03Calculate torque: Arrkios method"],
        Choices {0,1},
        Help "ONELAB implementation of Arrkios method.",
        Visible Flag_ExpertMode
    },

    Flag_Calculate_VW = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "03Calculate torque: Virtual Work"],
        Choices {0,1},
        Visible Flag_ExpertMode
    },

    ResId = {
        "/", Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "Results folder name"],
        Help "Name of the folder inside the results folder, where the result files of THIS simulation should be stored."
    },

    Flag_PrintFields = {
        1, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "Show Local Fields"],
        Choices{0, 1}
    },

    Flag_Lam = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "Calc Eddy Current losses in laminations"],
        Choices{0, 1},
        Visible Flag_ExpertMode && Flag_AnalysisType
    },

    Flag_EC_Magnets = {
        CALC_MAGNET_LOSSES, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "Eddy Current in Magnets (2D)"],
        Visible Flag_ExpertMode,
        Choices{0, 1},
        Help "Consider Eddy-Current in the PMs"
    },

    Flag_Inductance = {
        0, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "Compute inductances"],
        Choices{0, 1}
    },

    Flag_diffInductance = {
        1, Name StrCat[INPUT_ANA_SETTINGS_OUTPUT, "Inductance Computation Type"],
        Choices{0 = "Apparent", 1 = "Incremental"},
        Visible Flag_Inductance
    }

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
    //     // Constant to model short-circuit in winding => only when we impose the voltage
    //     DefineConstant[
    //         Flag_Fault = {0,
    //             Name StrCat[INPUT_ANA_SETTINGS, "Fault Condition to model",
    //             Choices{0 = "none", 1 = "Short Circuit A-B"}}
    //     ];
    // EndIf
//=============================================================================
// ==================== END ANALYSIS AND SOLVER PARAMETERS ====================
//=============================================================================


// In order to be able to use the machine_magstadyn_a.pro file which is included
// in onelab, we will have to define some additional constants number of
// NbrPolesTot in the model
DefineConstant[
    nbSlots = NBR_SLOTS,
    NbrPolesTot = NBR_POLE_PAIRS * 2,
    NbrPolesInModel = (Flag_Symmetry) ? NbrPolesTot / SymmetryFactor : NbrPolesTot,
    NbrPolesPairs = NbrPolesTot / 2,
    Flag_MB = 1, // Allways use Movingband!
    r_AG = R_AIRGAP
    //Flag_Link = 0 			// Use Link Constraint - is not used in magstatdyn...
];
Printf("Number of poles total (NbrPolesTot) = %.0f", NbrPolesTot);
Printf("Number of poles in Model = %.0f", NbrPolesInModel);
Printf("Symmetry Faktor = %.0f", SymmetryFactor);
Printf("Flag Symmetry = %.0f", Flag_Symmetry);
Printf("Airgap radius = %.5f", r_AG);

//=============================================================================
// ==================== MACHINE PARAMETERS ====================
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

    // d_Lam_i = {0.5,
    //            Name StrCat[INPUT_MAT_PROPERTIES, "Lamination thickness [mm]"],
    //            Units "mm",
    //            Visible Flag_Lam &&Flag_ExpertMode,
    //            Help "Lamination Thickness"},
    // d_Lam = d_Lam_i * mm, // conversion to SI

    // determine if we want to calculate using a linear or non-linear material
    Flag_NL = {
        FLAG_NL, Name StrCat[INPUT_MAT_PROPERTIES, "Non-linear B-H curves"],
        Choices{0, 1},
        Visible Flag_ExpertMode,
        Help "If this parameter is checked (=1), then the non-linear B-H curves
             are used. Otherwise the non-linearity is replaced (extrapolated) by
             a constant mu_r."
        }

    // dens_Lam = {
    //     VALUE_DENSITY_LAM,
    //     Name StrCat[INPUT_MAT_PROPERTIES, "Lamination density [kg/m³]"],
    //     Units "kg m^-3",
    //     Visible Flag_Lam &&Flag_ExpertMode,
    //     Help "density of the lammination part where eddy current losses should be calculated"}

];

// Printf("%g d_lam", d_Lam);

//=============================================================================
// ==================== END MACHINE PARAMETERS ====================
//=============================================================================

//=============================================================================
// ==================== EXCITATION PARAMETERS ====================
//=============================================================================

DefineConstant[
    ID_RMS = {Id_eff,
              Name StrCat[INPUT_ELEC_EXCITATION, "00ID_RMS"],
              Units "A",
              Visible Flag_SrcType_Stator == 1},

    ID = {ID_RMS * Sqrt[2],
          Name StrCat[INPUT_ELEC_EXCITATION, "02ID"],
          Units "A",
          Visible Flag_Debug && Flag_SrcType_Stator == 1,
          ReadOnly 1},

    IQ_RMS = {Iq_eff,
              Name StrCat[INPUT_ELEC_EXCITATION, "01IQ_RMS"],
              Units "A",
              Visible Flag_SrcType_Stator == 1},

    IQ = {IQ_RMS * Sqrt[2],
          Name StrCat[INPUT_ELEC_EXCITATION, "03IQ"],
          Units "A",
          Visible Flag_Debug && Flag_SrcType_Stator == 1,
          ReadOnly 1},

    I0 = {0,
          Name StrCat[INPUT_ELEC_EXCITATION, "04I0"],
          Units "A",
          Visible Flag_ExpertMode && Flag_SrcType_Stator == 1},

    Flag_invertRotDir = {FLAG_CHANGE_ROT_DIR,
          Name StrCat[INPUT_ELEC_EXCITATION, "05Invert rotation Direction"],
          Choices{0, 1},
          Visible Flag_ExpertMode},

    ParkOffset = {ParkAngOffset,
          Name StrCat[INPUT_ELEC_EXCITATION, "06Stator dq-System Offset [deg elec]"],
          Min -360, Max 360, Step 10,
          Visible Flag_ExpertMode},


    nbTurns = {NBR_TURNS_IN_FACE,
               Name StrCat[INPUT_ELEC_WINDINGS, "nbTurns in one slot side"]},

    NbrParallelPaths = {NBR_PARALLEL_PATHS,
            Name StrCat[INPUT_ELEC_WINDINGS, "number of parallel paths per phase"],
            ReadOnly 1},

    R_wire = {0,
              Name StrCat[INPUT_ELEC, "Connection Resistance [Ohm]"],
              Visible Flag_Cir},

    CircuitConnection = {0,
                         Name StrCat[INPUT_ELEC, "Winding Type"],
                         Choices{0 = "Star Connection", 1 = "Delta Connection"},
                         Visible Flag_Cir}
];

//=============================================================================
// ==================== END EXCITATION PARAMETERS ====================
//=============================================================================

//=============================================================================
// ==================== MATERIAL PARAMETERS ====================
//=============================================================================

DefineConstant[ //Material definitions
    tempMag = {TEMP_MAG,
        Name StrCat[INPUT_MAT_PROPERTIES_MAGNET, "Magnet temperature [°C]"],
        Visible Flag_ExpertMode}
];

//=============================================================================
// ==================== END MATERIAL PARAMETERS ====================
//=============================================================================

DefineConstant[ // Some circiut definitions
    // Variable controlling if the current density in the windings is imposed (via current)
    // or calculated (volatge imposed, or back-emf calculation in circuit)
    Flag_ImposedCurrentDensity = (Flag_SrcType_Stator == 1),

    // are the windings connected via an external circuit
    Flag_Cir = Flag_ImposedCurrentDensity != 1,

    // Use the Park transformation
    Flag_ParkTransformation = Flag_SrcType_Stator == 1,

    // Amplitude of the input voltage (in case of voltage input)
    VV = {12,
          Name StrCat[INPUT_ELEC, "V [V]"],
          Units "V",
          Visible Flag_SrcType_Stator == 2},

    // Phase angle of the voltage
    pA_deg = {0,
              Name StrCat[INPUT_ELEC, "Theta A [deg]"],
              Visible !Flag_ParkTransformation},

    // conversion of the angles from deg to rad
    pA = pA_deg * Pi / 180,
    Flag_ConstantSource = 0,
    pB = pA - 2 * Pi / 3,
    pC = pA + 2 * Pi / 3,
    Va = VV,
    Vb = VV,
    Vc = VV

];

// Printing some messages for information
Printf("Flag_Cir = %g", Flag_Cir);
Printf("Flag_SrcType_Stator = %g", Flag_SrcType_Stator);
Printf("Flag_ImposedCurrentDensity = %g", Flag_ImposedCurrentDensity);

Group
{
    DefineGroup[
        Domain_Lam, // part of the domain which is laminated
        Rotor_Magnets,
        Stator_Ind_Am, Stator_Ind_Bm, Stator_Ind_Cm,
        Stator_Ind_Ap, Stator_Ind_Bp, Stator_Ind_Cp,
        Rotor_Bars
    ];
}

GROUP_CODE

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
    //     For coil In{1 : nbSlots}
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
        For i In{0 : nbSlots - 1}
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

    /*
	// If we use an external circuit we populate these regions in the Circuit.pro
	// file => otherwise we still need to define them in order to avoid an error
	// message by machine_magstadyn_a.pro
	Resistance_Cir 		= Region[{}];
	Capacitance_Cir 	= Region[{}];
	Inductance_Cir 		= Region[{}];
	DomainZt 			= Region[{}];
	DomainSource_Cir	= Region[{}];
	*/

    // Control eddy current calculation in magentic material
    If(!Flag_EC_Magnets)
        RotorCC += Region[{Rotor_Magnets}];
    Else
        RotorC += Region[{Rotor_Magnets}];
    EndIf

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
// Set number of rotor bars after group definition
DefineConstant[
    nbRotorBars = NbrRegions[Rotor_Bars],
    Flag_Cir_RotorCage = {(nbRotorBars > 0) , Choices{0,1},
        Name StrCat(
            INPUT_ELEC_CIRCUIT_ROTOR,"Circuit/10Use circuit in rotor cage"
            ),
        Visible (nbRotorBars > 0)
        // ReadOnly (Flag_SrcType_Stator==1)
    }
    R_endring_segment = {0.836e-6,
        Name StrCat[
            INPUT_ELEC_CIRCUIT_ROTOR,
            "Circuit/11Resistance of endring segment [Ohm]"
        ],
        ReadOnly !Flag_Cir_RotorCage,
        Visible (nbRotorBars>0)
    },
    L_endring_segment = {4.8e-9,
        Name StrCat[
            INPUT_ELEC_CIRCUIT_ROTOR,
            "Circuit/12Inductance of endring segment [H]"
        ],
        ReadOnly !Flag_Cir_RotorCage,
        Visible (nbRotorBars>0)
    },
    slip = {0.9,
        Name StrCat[
            INPUT_ELEC_CIRCUIT_ROTOR,
            "Circuit/09Rotor slip"
        ],
        Range {0, 1, 0.05},
        ReadOnly !Flag_Cir_RotorCage,
        Visible (nbRotorBars>0)
    }
];
If (nbRotorBars > 0)
    Printf["Rotor_Bars detected! Number of rotor bars: %.0f", nbRotorBars];
EndIf

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

Function
{
    magn = Flag_Symmetry ? NbrPolesTot / SymmetryFactor : NbrPolesTot; // number of magnets
    NbWires[] = nbTurns;                                          // number of turns
    If(Flag_3D)
        // // unused for now!
        // SurfCoil[] = SurfaceArea[]{SURF_COND_STATOR} / (nbSlots / SymmetryFactor * 2);
        // Surf_Airgap_r[] = SurfaceArea[]{MBR_AIR_SURF};
        // Surf_Airgap_s[] = SurfaceArea[]{MBS_AIR_SURF};
    Else
        RegionListAp() = GetRegions[Stator_Ind_Ap]; // found new function GetRegions[] which retruns the group-list
        //                         RegionListAp(0): accesses the first element of the list which is a region number
        SurfCoil[] = SurfaceArea[]{RegionListAp(0)}; // save the area of on coil(side) in SurfCoil for current density calculation
        // Surf_Airgap_r[] = SurfaceArea[]{Region[Rotor_Airgap]}; // seems to be unused
    EndIf

    // rotational speed in mec rad/s
    wr = RPM * 2 * Pi / 60;
    // supply frequency
    Freq = wr * NbrPolesPairs / (2 * Pi);
    // electrical period
    T = 1 / Freq;
    // electrical pulsation
    Omega = 2 * Pi * Freq;
    // inital position in rad
    theta0 = initrotor_pos * deg2rad;
    // change in position between 2 time steps in rad
    delta_theta[] = d_theta * deg2rad;
    // stop time of the simulation
    timemax = (finalrotor_pos - initrotor_pos) * deg2rad / wr;
    // final rotor position in rad
    thetaMax = finalrotor_pos * deg2rad;
    // change in time between to time steps
    delta_time = d_theta * deg2rad / wr;
    // start time
    time0 = 0;
    // Number of steps
    NbSteps = Ceil[(thetaMax - theta0) / (d_theta * deg2rad) + 1];

    // variable containing the current rotor position => required to calculate the
    // magnetization direction of the magnets in rad. $Time is an internal variable
    // containing the current time
    RotorPosition[] = initrotor_pos * deg2rad + $Time * wr + $dtheta * deg2rad;
    // current position in deg
    RotorPosition_deg[] = RotorPosition[] * rad2deg;
    // stuff for testing => possible extension to include block communtation
    RotorPos_deg_mod[] = NbrPolesPairs * (RotorPosition_deg[] - 52.5) % 360;
    RotorPos_deg_mod_2[] = NbrPolesPairs * (RotorPosition_deg[] - 52.5 + 120) % 360;
    RotorPos_deg_mod_3[] = NbrPolesPairs * (RotorPosition_deg[] - 52.5 + 240) % 360;

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

    // if the nbSlots or NbrPolesTot are changed we have to change the offset
    // Theta_Park[]	= (RotorPosition[]-OFFSET*deg2rad)*NbrPolesPairs;
    // Offset moved outside the brackets -> Offset in electrical degrees and in rotation direction.
    // (Rotation direction is defined by Park matrix in magstadyn file.)
    Theta_Park[] = RotorPosition[] * NbrPolesPairs + (ParkOffset)*deg2rad;

    Theta_Park_deg[] = Theta_Park[] * rad2deg;

    // electrical period in (s)
    Period = 1 / Freq;

    NbTrelax = 2; // Number of periods while relaxation is applied, this is useful to decrease the transient times when simulating with voltages

    Trelax = NbTrelax * Period;

    // To apply relaxation such that when we use a voltage supply, we do not apply max voltage at t=0
    Frelax[] = (!Flag_NL || Flag_AnalysisType == 0 || $Time > Trelax) ? 1. : 0.5 * (1. - Cos[Pi * $Time / Trelax]);
}

FUNCTION_CODE

If(Flag_Cir_RotorCage)
    // include circuit
    Include "Circuit_SC_ASM.pro";
EndIf

// load 2D or 3D problem
// Include DEFAULT_PRO_FILE
