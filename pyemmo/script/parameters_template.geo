// Values that have to be set programmatically
// MACHINE SPECIFIC VALUES
L_AX_R = 1; // axial length of the stator
L_AX_S = 1; // axial length of the rotor
NBR_POLE_PAIRS = 4;
SYMMETRY_FACTOR = 4;
NBR_TURNS_IN_FACE = 20;
nbSlots = 12; 
R_AIRGAP = 0.02823; 
// SIMULATION SPECIFIC VALUES
INIT_ROTOR_POS = 0.0;
FINAL_ROTOR_POS = 45.0;
ANGLE_INCREMENT = 0.5;
SPEED_RPM = 1000;
FLAG_NL = 1;
READONLY_FLAG_NL = 1;
IQ_0 = 10;
ID_0 = 0;
ParkAngOffset = 0; // in deg
L_ECCENT_STATIC = 0.0;

PATH_RES = "res2D/";
// MATERIAL VALUES
dens_Lam = 7800;

DUMM = 9000000; // high domain id for dummy printing

// Group{
//     // Groups from magstatdyn file
//     DefineGroup[
//     // === STATOR ===
//     Stator_Inds, // grouping all stator inductor surfaces = Stator_IndsP + Stator_IndsN
//     StatorC, // electrically conducting surfaces (with sigma[] defined)
//     StatorCC, // non-conducting surfaces
//     Stator_Air, // stator air - only material definition 
//     Stator_Airgap, // for maxwell stress tensor torque
//     // used for current direction definition (+ or -):
//     Stator_IndsP, Stator_IndsN, Rotor_IndsP, Rotor_IndsN, 
//     Stator_Fe, Rotor_Fe, // used for material definition... maybe do this somewhere else
//     Stator_Bnd_MB, // inner Movingband line stator
//     PhaseA, PhaseB, PhaseC, // all inductor surfaces belonging to phase A,B or C
//     PhaseA_pos, PhaseB_pos, PhaseC_pos, // all positiv inductor surfaces belonging to phase A,B or C

//     // === ROTOR ===
//     RotorC, // conducting on rotor
//     RotorCC, // non-conduction on rotor
//     // Rotor_Air, // only material
//     Rotor_Airgap, // for maxwell stress tensor torque
//     Rotor_Magnets, // surfaces with Br[] defined 
//     // Rotor movingband must consist of:
//     // - Rotor_Bnd_MB_1 == inner rotor movingband line
//     // - Rotor_Bnd_MB_2...SymFactor == outer rotor movingband lines
//     Rotor_Bnd_MBaux,//  outer rotor movingband line(s) rotor
//     Rotor_Bnd_MB, // all rotor movingband lines

//     // === MISCELLANEOUS ===
//     Surf_bn0, // inner boundary line
//     Surf_Inf, // external boundary line
//     // primary and slave lines for the 2D case => bad naming
// 	  Surf_cutA0, // primary line
// 	  Surf_cutA1, // Slave line
//     Point_ref, // center point of machine
//     // Maybe using these later on...: Resistance_Cir, Inductance_Cir, Capacitance_Cir, DomainZt_Cir,
//     Dummy // -> DomainPlotMovingGeo : region with boundary lines of geo for visualisation of moving rotor

//     // === ADDITIONAL GROUPS FOR DIOGOS MAGSTATDYN FILE===
// 	  Domain_Lam // part of the domain which is laminated
//   ];
// }

//-------------------------------------------------------------------------------------
// Function declaration:
// Functions that can be defined explicitly outside the template in a calling .pro file
// are declared here so that their identifiers exist and can be referred to
// (but cannot be used) in other objects.

// Function{
//   DefineFunction[
//     br, // obvious
//     js, // can be defined outside! I think its just redefined later to make sure...
//     sigma,
//     muMag, // permeability of the rotor magnets
//     density,
//     Resistance, // If the resistance is known by measurement, it should be prefered, because its better to account for the end windings!
//     Inductance, Capacitance, // used in circuit
//     NbWires, // NbWires must be defined! -> Parameter
//     nbSlots, // Number of slots (two slot sides are one slot!)
//     SurfCoil, // Previous defined slot area of one coil (side)
//     RotorPosition, // = initrotor_pos*deg2rad + $Time * wr + $dtheta*deg2rad; // $dtheta = runtime variable!
//     RotorPosition_deg, // RotorPosition*rad2deg;
//     Theta_Park, // mostly defined as:   = ((RotorPosition[] + Pi/8) - Pi/6) * NbrPolePairs; 
//                 //                      = ( (RotorPosition[] + Pi/NbrPolesTot) + Pi/3) * NbrPolePairs;
//                 // Definition Diogo:
//                     // defintion of the park Angle
// 	                // if the nbSlots or nbPoles are changed we have to change the offset
// 	                // Theta_Park[]	= (RotorPosition[]-OFFSET*deg2rad)*NbrPolesPairs;
// 	                // Theta_Park[]	= (RotorPosition[]-(ParkAngOffset)*deg2rad)*NbrPolesPairs;
//     Theta_Park_deg // defined as: = Theta_Park[]*rad2deg;
//     // Unused: 
//     //Friction, Torque_mec

//     // === ADDITIONAL FUNCTIONS FOR DIOGOS MAGSTATDYN FILE===
//   ];
// }

// End of declarations
//-------------------------------------------------------------------------------------
