/*
  This template file contains a generic getdp/onelab template for 2D models of
  rotating electrical machines.  Fields are computed with a vector potential
  formulation. Motion is solved with the moving band technique.

  The template begins with a section devoted to the declaration of all potential
  interface variables, i.e. template variables that can be accessed/redefined
  from outside the template. Interface variables are either
  - groups (declared with DefineGroup[...])
  - functions (declared with DefineFunction[...])
  - constants (declared with DefineConstant[...])

  This declaration mechanism
  - allows the user to define the quantities of interest only, the others being
  assigned a default value (zero or "empty" if no value given in the declaration
  sentence)
  - avoids irrelevant error messages being produced when referencing to the
  unused variables in the template

  Redeclarations are ignored.
*/

//-------------------------------------------------------------------------------------
// Groups:
// The groups declared in this section can be defined by the user according to
// the characteristics of the modelled machine in a "model.pro" file including
// this template file.

// For an explanation of the differnet Objects defined in this file see
// https://stuff.mit.edu/afs/athena/software/gmsh_v3.0.1/getdp.pdf Chapter 1

Group {
  DefineGroup[
    Stator_Inds, StatorC, StatorCC, Stator_Air, Stator_Airgap, Stator_Magnets,
    Rotor_Inds, RotorC, RotorCC, Rotor_Air, Rotor_Airgap, Rotor_Magnets, Rotor_Bars,
    Stator_IndsP, Stator_IndsN, Rotor_IndsP, Rotor_IndsN,
    Stator_Al, Rotor_Al, Stator_Cu, Rotor_Cu, Stator_Fe, Rotor_Fe,
    Stator_Bnd_MB, Rotor_Bnd_MBaux, Rotor_Bnd_MB,
    Surf_bn0, Surf_Inf, Point_ref,
    PhaseA, PhaseB, PhaseC, PhaseA_pos, PhaseB_pos, PhaseC_pos,
    Resistance_Cir, Inductance_Cir, Capacitance_Cir, DomainZt_Cir, DomainSource_Cir
  ];
  // Exception: the group 'MovingBand_PhysicalNb' needs contain exactly one region
  // to pass a test done by the parser. It is declared with a dummy region "0".
  // MovingBand_PhysicalNb = Region[0] ;
}

//-------------------------------------------------------------------------------------
// Constants:
// Interface constants are declared in this section. Constants declared with
// a DefineConstant[...] AND with a `Name' attribute are automatically added to
// the ONELAB parameter database. Any previous declaration in another file of a
// ONELAB paramater with the same name will link to the corresponding template
// parameter.

// evaluate resID with right syntax
If (! StrFind(StrSub(ResId,0,1),"/"))
  ResId = StrCat("/",ResId);
EndIf
LenResId = StrLen(ResId);
If (!StrFind(StrSub(ResId,(LenResId-1),LenResId),"/"))
  ResId = StrCat(ResId,"/");
EndIf
Printf("ResId is %s", ResId());

DefineConstant[
  NbrMbSegments = GetNumber["Input/03Mesh/Number of Rotor Movingband Segments", 360],

  sigma_al = 3.72e7, // conductivity of aluminum [S/m]
  sigma_cu = 5.8e7  // conductivity of copper [S/m]
  sigma_fe = 1.0e7, // conductivity of iron [S/m]

  Nb_max_iter = {30, Name "Nonlinear solver/Max. num. iterations", Visible 0},
  relaxation_factor = {1, Name "Nonlinear solver/Relaxation factor", Visible 0},
  stop_criterion = {1e-4, Name "Nonlinear solver/Stopping criterion", Visible 0},
  // Coil system
  NbrPhases = 3,
  FillFactor_Winding = 1,
  Factor_R_3DEffects = 1,

  Flag_SrcType_StatorA = Flag_SrcType_Stator,
  Flag_SrcType_StatorB = Flag_SrcType_Stator,
  Flag_SrcType_StatorC = Flag_SrcType_Stator,

  Flag_ImposedSpeed=1,

  // Directory in which the results will be stored
  // TODO: Add code to check that path or use the model folder + ResId as
  //  default.
  ResDir = AbsolutePath[ StrCat[res, ResId] ],

  // Extension defintion for the results
  ExtGmsh = ".pos",   // fields are stored in pos files (they are then loaded automatically into onelab)
  ExtGnuplot = ".dat" // file type for table results sich as torque

  // some commandline options
  R_ = {"Analysis", Name "GetDP/1ResolutionChoices", Visible Flag_Debug},
  // Options:
  //  -v2         Creates mesh-based Gmsh output files when possible.
  //  -v (int)    Sets the verbosity level.
  //  -solve (res-id)   Same as -pre (res-id) -cal.
  //  -order(real)      Specifies the maximum interpolation order.
  //  -setnumber (name value)   Sets constant number name to value.
  //  -setstring (name value)   Sets constant string name to value.
    C_ = {
      "-solve Analysis -v 3 -v2",
      Name "GetDP/9ComputeCommand",
      Visible Flag_Debug || Flag_ExpertMode
    },
  P_ = {"", Name "GetDP/2PostOperationChoices", Visible Flag_Debug}
];

Printf("Results Directory is %s", ResDir());

//-------------------------------------------------------------------------------------
// Function declaration:
// Functions that can be defined explicitly outside the template in a calling .pro file
// are declared here so that their identifiers exist and can be referred to
// (but cannot be used) in other objects.

Function{
  DefineFunction[
    br, js,
    axialLength,
    Fac_Lam,
    Resistance, Inductance, Capacitance, NbWires, SurfCoil, NbrParallelPaths,
    Theta_Park, Theta_Park_deg,
    RotorPosition, RotorPosition_deg, Friction, Torque_mec
  ];
}

// End of declarations
//-------------------------------------------------------------------------------------


//-------------------------------------------------------------------------------------
// Definition of "template groups"
// Template groups represent the regions in terms of which the assembly or not
// of FE terms and the postprocessing calculations are controlled.  Template
// groups are defined in this section in terms of the above declared "user
// defined groups".

Group {
  //   DomainC    : with massive conductors
  //   DomainCC   : non-conducting domain
  //   DomainM    : with permanent magnets
  //   DomainB    : with inductors
  //   DomainS    : with imposed current density
  //   DomainL    : with linear permeability (no jacobian matrix)
  //   DomainNL   : with nonlinear permeability (jacobian matrix)
  //   DomainV    : with additional vxb term
  //   DomainKin  : region number for mechanical equation
  //   DomainDummy : region number for postpro with functions
  //   DomainPlotMovingGeo : region with boundary lines of geo for visualisation of moving rotor

  Inds = Region[ {Stator_Inds, Rotor_Inds} ] ;  // Group defining the inductors

  DomainM = Region[ {Rotor_Magnets} ] ;

  // DomainB is coupled to an external circuit, so if we impose the current density, it
  // is obvious that we cannot include them there
  If(!Flag_ImposedCurrentDensity)
    DomainB = Region[ {Inds} ] ;
    DomainS = Region[ {} ];
  Else
    DomainB = Region[ {} ] ;
    DomainS = Region[ {Inds} ];
  EndIf

  // Grouping of the conducting and non-conducting parts
  Stator  = Region[{ StatorC, StatorCC }] ;
  Rotor   = Region[{ RotorC,  RotorCC }] ;

  // Print out rotor regions for debugging
  // RegList() = GetRegions[Rotor];
  // For i In {0:#RegList()-1}
  //   Printf("Rotor Regions: %.0f", RegList(i));
  // EndFor

  // In the resolution, the nodes of the rotor are rotated, this defines the
  // regions which belong to the rotor and will consequently be rotated
  // similar to the definition of the moving object in Maxwell
  Rotor_Moving = Region[{ Rotor, Rotor_Air, Rotor_Airgap, Rotor_Bnd_MBaux} ] ;

  If (!Flag_MB)
    Rotor_Moving += Region[{Rotor_ClippingAux}];
  EndIf


  // If (Flag_MB)
    // Definition of the moving-band region (if used)
    // since the moving band is in the airgap, we assign it to the air region, such that the
    // permeability is correctly assigned to it
    MB  = MovingBand2D[ MovingBand_PhysicalNb, Stator_Bnd_MB, Rotor_Bnd_MB, SymmetryFactor] ;
    // Air = Region[{ Rotor_Air, Rotor_Airgap, Stator_Air, Stator_Airgap, MB } ] ;
  // Else
    // Air = Region[{ Rotor_Air, Rotor_Airgap, Stator_Air, Stator_Airgap} ] ;
  // EndIf

  // the non-conduting Domains are grouped (massive conductors)
  // even though the Inds are in DomainB, they are still included
  // in the non-conducting part.
  // If the individual coils are modelled seperately, it would be differently
  DomainCC = Region[{ MB, Inds, StatorCC, RotorCC }];
  // DomainCC = Region[{ Air, Inds, StatorCC, RotorCC }];

  // the conducting domains are grouped
  DomainC  = Region[{ StatorC, RotorC }];

  // the complete domain is defined
  Domain  = Region[{ DomainCC, DomainC }] ;

  // Dummy region number for postpro with functions
  // if we want to write a function (e.g. the d-axis flux-linkage) to
  // a file
  DomainDummy = Region[12345] ;
}



//-------------------------------------------------------------------------------------
// Defninition of functions and variables only used internally

// In GetDP, the material properties are defined as functions
// functions can be time or region dependent
// for example mu[{Air}] = 4e-7*pi; mu[{Iron}] = 3000*4e-7*pi
// Whenever the function is called (eg. when plotting fields), getdp will
// know to which domain the element belongs and use the correct value
Function {
  axialLength[Region[{Rotor}]] = AxialLength_R;
  axialLength[Region[{Stator}]] = AxialLength_S;
  axialLength[Region[{MovingBand_PhysicalNb}]] = AxialLength_R;

  // mu0 = 4.e-7 * Pi ;    // definition of the vaccum permeability as a constant // DEFINED IN MACHINE.PRO
  // nu0 = 1. / mu0 ;      // definition of the vaccum reluctivity as a constant // UNUSED
  // nu_m = 1/(mu0*muMag); // defintion of the relative reluctivity of the PMs

  // sigma[DomainM] = sigma_Mag;

  // since sigma is defined differntly for different regions so will rho[]
  rho[] = 1/sigma[] ;

  // defintion of the density function to be used in the calculation of the
  // moment of inertia
  // density[Motor_Region_1] = dens_Lam;
  // density[Motor_Region_3] = dens_Lam;
  // density[DomainM]  	    = dens_mag;

  // Calculation of the phase resistance (approximation)
  // Rb[] = Factor_R_3DEffects * axialLength[] * FillFactor_Winding * NbWires[]^2 / SurfCoil[] / sigma[] ;
  // Resistance[Region[{Stator_Inds}]] = Rb[] ;
  // Use pre-defined Resistance for stranded conductors in winding domains
  DefineConstant[
    R_S = {
      2 * L_AX_S * 0.4 * (nbrTurns*nbrSlots/3)^2 / (0.25/3*(1.6^2+1)*r_AG^2*Pi) / sigma_cu,
      Name StrCat[INPUT_ELEC_WINDINGS, "03Resistance"],
      Units "Ohm",
      Visible (Flag_SrcType_Stator==VOLTAGE_SOURCE)
    }
  ];
  Resistance[Region[{Stator_Inds}]] = R_S ;

  // definition of the current direction (1=positive z, -1=negative z)
  Idir[Region[{Stator_IndsP, Rotor_IndsP}]] =  1 ;
  Idir[Region[{Stator_IndsN, Rotor_IndsN}]] = -1 ;

  // define rotation direction of stator field. This is also depended on the winding layout!
  rotDirChange = (Flag_invertRotDir) ? -1 : 1;

  // defintion of the dq0-> vector
  Idq0[] = Vector[ $ID, $IQ, $I0 ] ;
  //Matrices can be seen as tensors, so here we define the inverse park matrix
  Pinv[] = Tensor[ Cos[Theta_Park[]],                       -Sin[Theta_Park[]],                       1,
                   Cos[Theta_Park[] - rotDirChange*2*Pi/3], -Sin[Theta_Park[] - rotDirChange*2*Pi/3], 1,
                   Cos[Theta_Park[] + rotDirChange*2*Pi/3], -Sin[Theta_Park[] + rotDirChange*2*Pi/3], 1 ];

  // as well as the park matrix
  P[] = 2/3 * Tensor[ Cos[Theta_Park[]],    Cos[Theta_Park[] - rotDirChange*2*Pi/3],    Cos[Theta_Park[] + rotDirChange*2*Pi/3],
                      -Sin[Theta_Park[]],   -Sin[Theta_Park[] - rotDirChange*2*Pi/3],   -Sin[Theta_Park[] + rotDirChange*2*Pi/3],
                      1/2,                  1/2,                                         1/2 ] ;

  // The abc flux is also defined as a vector
  Flux_abc[] = Vector[$Flux_a, $Flux_b, $Flux_c];

  // Here we see why the abs fluxes and the qq0 currents were defined as
  // vectors. Like this we can use the Tensor and Vector multiplication
  // to calculate the dq0 fluxes or abc currents
  Iabc[]     = Pinv[] * Idq0[] ;
  Flux_dq0[] = P[] *  Flux_abc[];

  // assign the current of each phase
  If(Flag_ParkTransformation)
    II = 1. ;
    IA[] = CompX[ Iabc[] ] ;
    IB[] = CompY[ Iabc[] ] ;
    IC[] = CompZ[ Iabc[] ] ;
  Else // Standard sinusoidal current definition
    II = I_eff * Sqrt[2];
    IA[] = ((Flag_Fault == 1) && ($Time>0.02)) ? 0*F_Sin_wt_p[]{2*Pi*freq_stator, rotDirChange*pA} : F_Sin_wt_p[]{2*Pi*freq_stator, rotDirChange*pA} ;
    IB[] = F_Sin_wt_p[]{2*Pi*freq_stator, rotDirChange*pB};
    IC[] = F_Sin_wt_p[]{2*Pi*freq_stator, rotDirChange*pC};
  EndIf
  Jz1A[] = NbWires[]/SurfCoil[] * Idir[] * Vector[0, 0, 1];
  // calculate the current density from the current and the surface of the coil
  js[PhaseA] = II * NbWires[]/SurfCoil[] * IA[] / NbrParallelPaths * Idir[] * Vector[0, 0, 1] ;
  js[PhaseB] = II * NbWires[]/SurfCoil[] * IB[] / NbrParallelPaths * Idir[] * Vector[0, 0, 1] ;
  js[PhaseC] = II * NbWires[]/SurfCoil[] * IC[] / NbrParallelPaths * Idir[] * Vector[0, 0, 1] ;

  // Maxwell stress tensor
  T_max[] = ( SquDyadicProduct[$1] - SquNorm[$1] * TensorDiag[0.5, 0.5, 0.5] ) / mu0 ;

  // This function returns the angle with respect to the x axis of the point that is being evaluated
  AngularPosition[] = (Atan2[$Y,$X]#7 >= 0.)? #7 : #7+2*Pi ;

  // Function to rotate the points around the z axis
  RotatePZ[] = Rotate[ Vector[$X,$Y,$Z], 0, 0, $1 ] ;

  // The inductance is calculated using the frozen permeability method.
  // Further details on this method can be found under
  // https://ieeexplore.ieee.org/abstract/document/732255
  // Since we need to energize the different axis one after the other
  // we define the new abc currents to apply, and consequently the new
  // current densitites
  // index one indicates the quantities when only d-axis current is present
  // index 2 when the q-axis current is present
  If (Flag_Inductance)
    Iabc_frozen_0[] = Pinv[]*Vector[1,0,0];
    Iabc_frozen_1[] = Pinv[]*Vector[0,1,0];
    For k In {0:1}
      IA_frozen~{k}[] = CompX[Iabc_frozen~{k}[]];
      IB_frozen~{k}[] = CompY[Iabc_frozen~{k}[]];
      IC_frozen~{k}[] = CompZ[Iabc_frozen~{k}[]];
      j_frozen~{k}[PhaseA] = II * NbWires[]/SurfCoil[] * IA_frozen~{k}[] * Idir[] * Vector[0, 0, 1] ;
      j_frozen~{k}[PhaseB] = II * NbWires[]/SurfCoil[] * IB_frozen~{k}[] * Idir[] * Vector[0, 0, 1] ;
      j_frozen~{k}[PhaseC] = II * NbWires[]/SurfCoil[] * IC_frozen~{k}[] * Idir[] * Vector[0, 0, 1] ;
    EndFor

    // During the PostOperation of the Frozen Permeability, we store the fluxes in the run-time
    // variables $Flux_x_PM for the case with only PM flux, $Flux_x_Id for the case with only
    // d-current , and $Flux_x_Iq in the other case
    Flux_dq0_PM[] = P[]*Vector[$Flux_a_PM,$Flux_b_PM,$Flux_c_PM];
    Flux_dq0_Id[] = P[]*Vector[$Flux_a_Id,$Flux_b_Id,$Flux_c_Id];
    Flux_dq0_Iq[] = P[]*Vector[$Flux_a_Iq,$Flux_b_Iq,$Flux_c_Iq];

    // since we used a current of 1A, the inductance is directly given by the flux
    Ld[] = CompX[Flux_dq0_Id[]];
    Lq[] = CompY[Flux_dq0_Iq[]];
    Ldq[]= CompY[Flux_dq0_Id[]];

  EndIf


  // Volumes for various regions
  // Volume_Magnet[]       = SurfaceArea[]{Region[Rotor_Magnets]}*axialLength[Region[Rotor_Magnets]]*SymmetryFactor;
  // Volume_Stator[]       = SurfaceArea[]{S_IRON}*axialLength[]*SymmetryFactor;
  // Volume_RotorCore[]    = SurfaceArea[]{R_IRON}*AxialLength_R*SymmetryFactor;
}


//-------------------------------------------------------------------------------------

// Since getdp transforms the elements into a reference elements having local coordinate systems
// during matrix assemply, calculations, ... we need to define the type of Jacobian
Jacobian {
  // In this case we name our Jacobian Vol, it is definied in all elements and is of type Vol
  // the type vol states that the dimension of the element during the transformation is not changed
  // in 2-D: triangle remains a triangle
  // When using a type Sur, the dimension is dectreased by 1, this means that f.eg. in 2-D the
  // element of type n=2 is mapped into a n=1
  { Name Vol; Case { { Region All ; Jacobian Vol; } } }
  { Name Sur; Case { { Region All ; Jacobian Sur; } } }
}

// Here we defined the integration method
Integration {
  // We call our integration I1, and the method used is a Gauss integration
  // (see: https://de.wikipedia.org/wiki/Gauß-Quadratur)
  // For each element we define the number of integration points
  { Name I1 ; Case {
      { Type Gauss ;
        Case {
          { GeoElement Line       ; NumberOfPoints  13 ; }
          { GeoElement Triangle   ; NumberOfPoints  6 ; }
          { GeoElement Quadrangle ; NumberOfPoints  4 ; }
        }
      }
    }
  }
}

//-------------------------------------------------------------------------------------

Constraint {
  // Here we define the constraints for the DoFs
  // The constraint is given a name for further identification
  { Name MVP_2D ;
    Case {
      // On the outer Boundary we define a value for the magnetic vector potential equal to 0
      // same as in Maxwell
      { Region Surf_Inf ; Type Assign; Value 0. ; }
      { Region Surf_bn0 ; Type Assign; Value 0. ; }

      If(Flag_Symmetry)
        // Here we link the DoFs from the primary surface (CutA0) to the slave surface (cutA1)
        // this is specified by the type Link.
        // the coefficient determines if we have positive or negative symmetry
        // The function specifies the transformation that has to be used to get from the primary
        // DoF to the slave DoF. Since we have rotational symmetry around Z, the rotation around Z function defined before has to be used.
        { Region Surf_cutA1; SubRegion Region[{Surf_Inf,Surf_bn0}]; Type Link;
          RegionRef Surf_cutA0; SubRegionRef Region[{Surf_Inf,Surf_bn0}];
          Coefficient ((NbrPolesInModel%2)?-1:1) ;
	        Function RotatePZ[-NbrPolesInModel*2*Pi/NbrPolesTot]; }
        { Region Surf_cutA1; Type Link; RegionRef Surf_cutA0;
          Coefficient (NbrPolesInModel%2)?-1:1 ;
	        Function RotatePZ[-NbrPolesInModel*2*Pi/NbrPolesTot]; }

        // In the Domain we only have 1/SymmetryFactor of the MovingBand, which is a full circle
        // This means that we also only have data for the DoFs on the part which we model, so we need
        // to use symmetry here as well to link the DoFs for which we have results to other parts
        // this has to be done since, these are also automaticcaly linked to the DoFs of the stator
        // and it can be that the Rotor_Moving_Band we have Dofs is diamterically oposite to the stator
        // (rememeber we have motion, possibly), and by copying it to the other parts, we can link them to the stator
        // DoFs
        For k In {1:SymmetryFactor-1}
          { Region Rotor_Bnd_MB~{k+1} ;
    	      SubRegion Rotor_Bnd_MB~{(k!=SymmetryFactor-1)?k+2:1}; Type Link;
            RegionRef Rotor_Bnd_MB_1; SubRegionRef Rotor_Bnd_MB_2;
            Coefficient ((NbrPolesInModel%2)?-1:1)^(k);
    	      Function RotatePZ[-k*NbrPolesInModel*2*Pi/NbrPolesTot]; }
        EndFor
      EndIf

    }
  }
  If (Flag_SecondOrder)
    // New similar Constraint for second order basis function
    { Name MVP_2D_2E ;
      Case {
        { Region Surf_Inf ; Type Assign; Value 0. ; } // Outer Boundary
        { Region Surf_bn0 ; Type Assign; Value 0. ; } // Inner Boundary
        If(Flag_Symmetry)
          // Primary and secondary link of symmetry lines:
          { Region Surf_cutA1; SubRegion Region[{Surf_Inf,Surf_bn0}]; Type Link; RegionRef Surf_cutA0; SubRegionRef Region[{Surf_Inf,Surf_bn0}]; Coefficient ((NbrPolesInModel%2)?-1:1); Function RotatePZ[-NbrPolesInModel*2*Pi/NbrPolesTot]; }
          { Region Surf_cutA1; Type Link; RegionRef Surf_cutA0; Coefficient (NbrPolesInModel%2)?-1:1; Function RotatePZ[-NbrPolesInModel*2*Pi/NbrPolesTot]; }
          // Link of the Dofs to the auxillary movingband lines:
          For k In {1:SymmetryFactor-1}
            { Region Rotor_Bnd_MB~{k+1} ; SubRegion Rotor_Bnd_MB~{(k!=SymmetryFactor-1)?k+2:1}; Type Link; RegionRef Rotor_Bnd_MB_1; SubRegionRef Rotor_Bnd_MB_2; Coefficient ((NbrPolesInModel%2)?-1:1)^(k); Function RotatePZ[-k*NbrPolesInModel*2*Pi/NbrPolesTot]; }
          EndFor
        EndIf
      }
    }
  EndIf
  // Constraint for the electrical sclar potential in which we fix the
  // current for certain regions.
  // The magnetic scalar potential is only defined in DomainC!
  { Name Current_2D ;
    Case {
      // if the magnets are conducting we need to have a net current of 0A
      // per magnet. This is defined here by setting the constraint to 0
      If (Flag_EC_Magnets)
        rotorMagList() = GetRegions[Rotor_Magnets];
        For i In {0:#rotorMagList()}
          { Region Region[{rotorMagList(i)}] ; Value 0;}
        EndFor
      EndIf
    }
  }

  // Here we could define constraints on the voltage.
  { Name Voltage_2D ;
    Case {
      If(!Flag_Cir_RotorCage)
        { Region RotorC  ; Value 0. ; }
      EndIf
    }
  }

  // When using the external circuit with voltages as input, we need to constraint the voltage drop across the input.
  // The IA[] function is just a since of amplitude 1!
  // The relaxiation function (Frelax) is used to continously increase the voltage at simulation start until max voltage. This improves the convergence of the model.
  { Name Voltage_Cir ;
    Case {
      If(Flag_Cir && Flag_SrcType_Stator == VOLTAGE_SOURCE) // == 2
        { Region Input1  ; Value Va  ; TimeFunction IA[]*Frelax[]; }
        { Region Input2  ; Value Vb  ; TimeFunction IB[]*Frelax[]; }
        { Region Input3  ; Value Vc  ; TimeFunction IC[]*Frelax[]; }
      EndIf
    }
  }

  { Name Current_Cir ;
    Case {
    }
  }

}

//-------------------------------------------------------------------------------------------

// Here we define the function spaces. Function Spaces are the entities which store the DoFs.
FunctionSpace {
  // Here we define the FunctionSpace for the magnetic vector potential. This is of Type Form1P.
  // Further definitions on differential forms can be found in literature.
  // A small summary is given here:
  // A FunctionSpace of Form:
  //    *0 : Sclar field with quantities are continous arcoss elements
  //    *1 : Vector Field having a continous tangential component on the interface between 2 domains (eg. magnetic field)
  //    *2 : Vector Field having a continous normal component on the interface between 2 domains (eg. magnetic flux density)
  //    *3 : Scalar Field with discontinous quantities acrcoss elements

  // Using the differential operators curl, div, grad we allow to get from one to the other
  // Form 0 <== grad ==> Form 1 <== curl ==> Form 2 <== Div ==> Form 3
  // Since the magnetic vector field is defined as b = Curl A ==> And the magnetic flux density is of form 2
  // it must follow that the magnetic vector potential is of form 1
  // In 2-D simulations, the magnetic vector poential has only a component on the z-axis, Form1b defines a support
  // which is perpendicular to the z-plane

  { Name Hcurl_a_2D ; Type Form1P ;
    BasisFunction {
      // The basis function determines how the vector space is approximated
      // The basis function is called se1 for further references,
      // the vector field se1 is then approximated using
      //      a = \sum_{i=1}^N ae1_n * se1_n
      // The function BF_PerpendicularEdge defines a vector having as support nodes and pointing in the z-direction
      { Name se1 ; NameOfCoef ae1 ; Function BF_PerpendicularEdge ;
        // The support of this function space are the all the nodes of Domain and the Rotor_Bnd_MBaux (the latter is needed since the unknowns are interpolated here as well; see: Constraint)
        Support Region[{ Domain, Rotor_Bnd_MBaux, Stator_Bnd_MB, Rotor_Bnd_MB_1}] ; Entity NodesOf [ All ] ; }
      If (Flag_SecondOrder)
        { Name se2 ; NameOfCoef ae2 ; Function BF_PerpendicularEdge_2E ; Support Region[{Domain, Rotor_Bnd_MBaux, Stator_Bnd_MB, Rotor_Bnd_MB_1}] ; Entity EdgesOf [ All ] ; }
      EndIf
   }
    // We constraint certain DoFs, with the previously defined constraint for the MVP
    Constraint {
      { NameOfCoef ae1 ; EntityType NodesOf ; NameOfConstraint MVP_2D ; }
      If (Flag_SecondOrder)
        { NameOfCoef ae2 ; EntityType EdgesOf ; NameOfConstraint MVP_2D_2E ; }
      EndIf
    }
  }

  // Magnetic Vector Potential for PM Flux only (Frozen permeability). Since each function space can only store one field we need to define fields for the solution of the calculations for the Frozen Permeability computations.
  // In the case with PMs only
  { Name Hcurl_a_2D_PM ; Type Form1P ;
    BasisFunction {
      { Name se1 ; NameOfCoef ae1 ; Function BF_PerpendicularEdge ;
        Support Region[{ Domain,Rotor_Bnd_MBaux}] ; Entity NodesOf [ All ] ; }
   }
    Constraint {
      { NameOfCoef ae1 ; EntityType NodesOf ; NameOfConstraint MVP_2D ; }
    }
  }

  // In the case with currents
  { Name Hcurl_a_2D_Currents ; Type Form1P ;
    BasisFunction {
      { Name se1 ; NameOfCoef ae1 ; Function BF_PerpendicularEdge ;
        Support Region[{ Domain,Rotor_Bnd_MBaux}] ; Entity NodesOf [ All ] ; }
   }
    Constraint {
      { NameOfCoef ae1 ; EntityType NodesOf ; NameOfConstraint MVP_2D ; }
    }
  }

  // Gradient of Electric scalar potential (2D)
  { Name Hregion_u_Mag_2D ; Type Form1P ;
    BasisFunction {
      // The BF_RegionZ defines one Function per Region!
      // So e.g. all nodes of one magnet (=Region) have the same potential 'ur'
      { Name sr ; NameOfCoef ur ; Function BF_RegionZ ;
        Support DomainC ; Entity DomainC ; }
    }
    GlobalQuantity {
      { Name U ; Type AliasOf        ; NameOfCoef ur ; }
      { Name I ; Type AssociatedWith ; NameOfCoef ur ; }
    }
    Constraint {
      { NameOfCoef U ; EntityType GroupsOfNodesOf ; NameOfConstraint Voltage_2D ; }
      { NameOfCoef I ; EntityType GroupsOfNodesOf ; NameOfConstraint Current_2D ; }
    }
  }

  { Name Hregion_i_Mag_2D ; Type Vector ;
    BasisFunction {
      // Single Value of ir over each slot surface, ir (local) = Ib (global)
      { Name sr ; NameOfCoef ir ; Function BF_RegionZ ;
        Support DomainB ; Entity DomainB ; }
    }
    GlobalQuantity {
      { Name Ib ; Type AliasOf        ; NameOfCoef ir ; }
      { Name Ub ; Type AssociatedWith ; NameOfCoef ir ; }
    }
    Constraint {
      { NameOfCoef Ub ; EntityType Region ; NameOfConstraint Voltage_2D ; }
      { NameOfCoef Ib ; EntityType Region ; NameOfConstraint Current_2D ; }
    }
  }

  // For circuit equations
  { Name Hregion_Z ; Type Scalar ;
    BasisFunction {
      { Name sr ; NameOfCoef ir ; Function BF_Region ;
        Support DomainZt_Cir ; Entity DomainZt_Cir ; }
    }
    GlobalQuantity {
      { Name Iz ; Type AliasOf        ; NameOfCoef ir ; }
      { Name Uz ; Type AssociatedWith ; NameOfCoef ir ; }
    }
    Constraint {
      { NameOfCoef Uz ; EntityType Region ; NameOfConstraint Voltage_Cir ; }
      { NameOfCoef Iz ; EntityType Region ; NameOfConstraint Current_Cir ; }
    }
  }
}

//-------------------------------------------------------------------------------------------
// The formaulation Object defines the equation of the problem to be solved. This has to be wrtiiten
// in weak form. How this is done see  pdf.
Formulation {

  If (Flag_Inductance)

  {
    Name MagSta_PM ; Type FemEquation ;
    Quantity {
      { Name a  ; Type Local  ; NameOfSpace Hcurl_a_2D ; }
      { Name a_PM;Type Local  ; NameOfSpace Hcurl_a_2D_PM;}
    }
    Equation {
      Galerkin { [ nu[{d a}] * Dof{d a_PM}  , {d a_PM} ] ;
        In Domain ; Jacobian Vol ; Integration I1 ; }

      If (Flag_diffInductance)
        Galerkin { [ dhdb_NL[{d a}] * Dof{d a_PM} ,  {d a_PM}] ;
          In DomainNL; Jacobian Vol; Integration I1 ; }
      EndIf

      // DO NOT REMOVE!!!
      // Keeping track of Dofs in auxiliar line of MB if Symmetry==1
      Galerkin {  [  0*Dof{d a_PM} , {d a_PM} ]  ;
        In Rotor_Bnd_MBaux; Jacobian Sur; Integration I1; }

      Galerkin { [ -nu[] * br[] , {d a_PM} ] ;
        In DomainM ; Jacobian Vol ; Integration I1 ; }
    }
  }

  For k In {0:1}
    { Name MagSta_Currents~{k} ; Type FemEquation ;
      Quantity {
        { Name a  ; Type Local  ; NameOfSpace Hcurl_a_2D ; }
        { Name a_I~{k};Type Local  ; NameOfSpace Hcurl_a_2D_Currents; }
      }
      Equation {
        Galerkin { [ nu[{d a}] * Dof{d a_I~{k}}  , {d a_I~{k}} ] ;
          In Domain ; Jacobian Vol ; Integration I1 ; }

        If (Flag_diffInductance)

          Galerkin { [ dhdb_NL[{d a}] * Dof{d a_I~{k}} ,  {d a_I~{k}}] ;
            In DomainNL; Jacobian Vol; Integration I1 ; }

        EndIf

        // DO NOT REMOVE!!!
        // Keeping track of Dofs in auxiliar line of MB if Symmetry==1
        Galerkin {  [  0*Dof{d a_I~{k}} , {d a_I~{k}} ]  ;
          In Rotor_Bnd_MBaux; Jacobian Sur; Integration I1; }

        /*Galerkin { [ -nu[] * br[]*0, {d a_I} ] ;
          In DomainM ; Jacobian Vol ; Integration I1 ; }*/

        Galerkin { [ -j_frozen~{k}[] , {a_I~{k}} ] ;
          In DomainS ; Jacobian Vol ; Integration I1 ; }
      }
    }
  EndFor
  // End If (Flag_Inductance)
  EndIf


  { Name MagStaDyn_a_2D ; Type FemEquation ;
    Quantity {
      { Name a  ; Type Local  ; NameOfSpace Hcurl_a_2D ; }
      { Name ur ; Type Local  ; NameOfSpace Hregion_u_Mag_2D ; }
      { Name I  ; Type Global ; NameOfSpace Hregion_u_Mag_2D [I] ; }
      { Name U  ; Type Global ; NameOfSpace Hregion_u_Mag_2D [U] ; }

      { Name ir ; Type Local  ; NameOfSpace Hregion_i_Mag_2D ; }
      { Name Ub ; Type Global ; NameOfSpace Hregion_i_Mag_2D [Ub] ; }
      { Name Ib ; Type Global ; NameOfSpace Hregion_i_Mag_2D [Ib] ; }

      { Name Uz ; Type Global ; NameOfSpace Hregion_Z [Uz] ; }
      { Name Iz ; Type Global ; NameOfSpace Hregion_Z [Iz] ; }
    }
    Equation {
      Galerkin { [ nu[{d a}] * Dof{d a}  , {d a} ] ;
        In Domain ; Jacobian Vol ; Integration I1 ; }
      If(Flag_NL)
      Galerkin { JacNL [ dhdb_NL[{d a}] * Dof{d a} , {d a} ] ;
        In DomainNL ; Jacobian Vol ; Integration I1 ; }
      EndIf

      // DO NOT REMOVE!!!
      // Keeping track of Dofs in auxiliar line of MB if Symmetry==1
      Galerkin {  [  0*Dof{d a} , {d a} ]  ;
        In Region[ {Rotor_Bnd_MBaux, Stator_Bnd_MB, Rotor_Bnd_MB_1} ] ; Jacobian Sur; Integration I1; }

      Galerkin { [ -nu[] * br[] , {d a} ] ;
        In DomainM ; Jacobian Vol ; Integration I1 ; }

      Galerkin { DtDof[ sigma[] * Dof{a} , {a} ] ;
        In DomainC ; Jacobian Vol ; Integration I1 ; }
      Galerkin { [ sigma[] * Dof{ur}, {a} ] ;
        In DomainC ; Jacobian Vol ; Integration I1 ; }

      Galerkin { [ -js[] , {a} ] ;
        In DomainS ; Jacobian Vol ; Integration I1 ; }

      Galerkin { DtDof[ sigma[] * Dof{a} , {ur} ] ;
        In DomainC ; Jacobian Vol ; Integration I1 ; }
      Galerkin { [ sigma[] * Dof{ur} , {ur} ] ;
        In DomainC ; Jacobian Vol ; Integration I1 ; }
      GlobalTerm { [ Dof{I} , {U} ] ; In DomainC ; }

      // Uncomment here if the eddy-current reaction field should be taken into account
      // If (Flag_Lam)
      //     Galerkin { DtDof [ Fac_Lam[] * Dof{d a} , {d a} ] ; In Domain_Lam ; Jacobian Vol ; Integration I1 ; }
      // EndIf

      Galerkin { [ -NbWires[]/SurfCoil[] * Dof{ir} , {a} ] ;
        In DomainB ; Jacobian Vol ; Integration I1 ; }
      Galerkin { DtDof [ axialLength[] * NbWires[]/SurfCoil[] * Dof{a} , {ir} ] ;
        In DomainB ; Jacobian Vol ; Integration I1 ; }
      GlobalTerm { [ Dof{Ub}/SymmetryFactor , {Ib} ] ; In DomainB ; }
      // Rb[] = Factor_R_3DEffects*axialLength[]*FillFactor_Winding*NbWires[]^2/SurfCoil[]/sigma[] ;
      // Rb = f_3D * l_ax * k_cu * N^2 / A_Coil / sigma_Cu
      // Galerkin { [ Rb[]/SurfCoil[]* Dof{ir} , {ir} ] ;
      //   In DomainB ; Jacobian Vol ; Integration I1 ; } // Resistance term

      GlobalTerm { [ Resistance[] / SymmetryFactor  * Dof{Ib} , {Ib} ] ; In DomainB ; }
      // The above term can replace the resistance term:
      // if we have an estimation of the resistance of DomainB, via e.g. measurements
      // which is better to account for the end windings...

      If(Flag_Cir || Flag_Cir_RotorCage)
	      GlobalTerm { NeverDt[ Dof{Uz}                , {Iz} ] ; In Resistance_Cir ; }
        GlobalTerm { NeverDt[ Resistance[] * Dof{Iz} , {Iz} ] ; In Resistance_Cir ; }

        GlobalTerm { [ Dof{Uz}                      , {Iz} ] ; In Inductance_Cir ; }
        GlobalTerm { DtDof [ Inductance[] * Dof{Iz} , {Iz} ] ; In Inductance_Cir ; }

        GlobalTerm { NeverDt[ Dof{Iz}        , {Iz} ] ; In Capacitance_Cir ; }
        GlobalTerm { DtDof [ Capacitance[] * Dof{Uz} , {Iz} ] ; In Capacitance_Cir ; }

        GlobalTerm { [ 0. * Dof{Iz} , {Iz} ] ; In DomainZt_Cir ; }
        GlobalTerm { [ 0. * Dof{Uz} , {Iz} ] ; In DomainZt_Cir ; }

        GlobalEquation {
          Type Network ; NameOfConstraint ElectricalCircuit ;
          { Node {I};  Loop {U};  Equation {I};  In DomainC ; }
          { Node {Ib}; Loop {Ub}; Equation {Ub}; In DomainB ; }
          { Node {Iz}; Loop {Uz}; Equation {Uz}; In DomainZt_Cir ; }
         }
      EndIf
    }
  }
}

//-----------------------------------------------------------------------------------------
// Resolution defines the steps which have to be made to solve the system
Resolution {
  { Name Analysis ;
    System {
        { Name A ; NameOfFormulation MagStaDyn_a_2D ; }
        If (Flag_Inductance)
          { Name A_PM ; NameOfFormulation MagSta_PM ; }
          For k In {0:1}
            { Name A_I~{k} ; NameOfFormulation MagSta_Currents~{k} ; }
          EndFor
        EndIf
    }
    Operation {
      // Bar resistance node-group IDs in circuit only in range 400-500
      If (nbrRotorBars>99)
        Error["Max. number of rotor bars is 99!"];
      ElseIf (!Exists[SurfCoil[]])
        Error["Missing value for single coil surface (Function SurfCoil). Make sure Domain_SurfCoil is set correctly."];
      EndIf
      Evaluate[$ID=ID]; // set the runtime variables
      Evaluate[$IQ=IQ];
      Evaluate[$I0=I0];
      Evaluate[$dtheta=0]; // the dtheta value is only needed when generating the ec lamination tables
      Printf("IQ:  %.0f", IQ);
      Printf("ID:  %.0f", ID);
      Printf("I0:  %.0f", I0);
      // Create the directory if necessary
      // SystemCommand[Sprintf["DEL /F /Q %s", ResDir()]]; // -> This does NOT work!
      If (Flag_ClearResults)
        // This works! But only removes the files in ResDir, not the directory itself.
        // Printf(Sprintf["del /F /Q %s", ResDir()]) > "delete.bat";
        Printf(Sprintf["del /F /Q %s\*.pos %s\*.dat", ResDir(), ResDir()]) > "delete.bat";
        SystemCommand["delete.bat"];
        DeleteFile["delete.bat"];
      EndIf
      // Create the directory if necessary
      CreateDir[ResDir];
      /*
      If(Flag_ClearResults)
        DeleteFile[StrCat[ResDir,"Flux_a",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Flux_b",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Flux_c",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Flux_d",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Flux_q",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Flux_0",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Ia",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Ib",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Ic",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"InducedVoltageA",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"InducedVoltageB",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"InducedVoltageC",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Ld",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Lq",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Ldq",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"LossesMagnets",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"ParkAngle_deg",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Pec_Lam",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"PMFlux_d",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"PMFlux_q",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"RotorPos_deg",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Surf_Phase_A_pos",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"temp",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Tr",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Ts",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Tmb",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Ua",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Ub",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Uc",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"JL",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"JL_Fe",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"P",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"V",ExtGnuplot]];;DeleteFile[StrCat[ResDir,"Irotor",ExtGnuplot]];
      EndIf
      */

      ChangeOfCoordinates[ NodesOf[Rotor_Moving], RotatePZ[initrotor_pos*Pi/180]]; // Rotation must occure before MovingBand meshing!
      InitMovingBand2D[MB] ;
      MeshMovingBand2D[MB] ;
      InitSolution[A];
      Evaluate[$RPos=RotorPosition_deg[]];
      Evaluate[$PAng=Theta_Park_deg[]];

      // PostOperation[GetInertia];   // declares the variable $Inertia

      // //Evaluate Some motor parameters and write them to a file
      // Print[{$Inertia}, Format "J=%e", File  StrCat[ResDir,'MotorParameters.txt']];
      // Evaluate[$Temp=NbrPolesTot];
      // Print[{$Temp}, Format "p=%.0f", File  StrCat[ResDir,'MotorParameters.txt']];
      // Evaluate[$Temp=Volume_Magnet[]];
      // Print[{$Temp}, Format "V_MAG=%e", File  StrCat[ResDir,'MotorParameters.txt']];
      // Evaluate[$Temp=Volume_Stator[]];
      // Print[{$Temp}, Format "V_STA=%e", File  StrCat[ResDir,'MotorParameters.txt']];
      // Evaluate[$Temp=Volume_RotorCore[]];
      // Print[{$Temp}, Format "V_ROT=%e", File  StrCat[ResDir,'MotorParameters.txt']];
      // Evaluate[$Temp=Volume_RotorHub[]];
      // Print[{$Temp}, Format "V_HUB=%e", File  StrCat[ResDir,'MotorParameters.txt']];
      // Evaluate[$Temp=Volume_RotorBridge[]];
      // Print[{$Temp}, Format "V_BRI=%e", File  StrCat[ResDir,'MotorParameters.txt']];

      If(Flag_ParkTransformation && Flag_SrcType_Stator == CURRENT_SOURCE)
        PostOperation[ThetaPark_IABC] ;
      EndIf

      If(!Flag_NL)
        Generate[A] ; Solve[A] ;
      EndIf
      If(Flag_NL)
        IterativeLoop[20, 1e-2, relaxation_factor/10]{
          GenerateJac[A] ; SolveJac[A] ;} // we allow this one to not converge
        IterativeLoop[Nb_max_iter, stop_criterion, relaxation_factor]{
          GenerateJac[A] ; SolveJac[A] ;}
      EndIf
      // PostOperations
      If (Flag_SaveSolution)
        SaveSolution[A] ;
      EndIf
      If(Flag_Debug)
        PostOperation[Debug] ;
      EndIf
      If(Flag_PrintFields)
        PostOperation[Get_LocalFields] ;
        PostOperation[GetBRadTanAirGap];
      EndIf
      PostOperation[Get_GlobalQuantities] ;
      If(Flag_Calculate_ONELAB)
        PostOperation[Get_Torque] ;
      EndIf
      If(Flag_Calculate_VW)
        PostOperation[Get_Torque_VW] ;
      EndIf

      If (Flag_Inductance)
        InitSolution[A_PM];
        Generate[A_PM]; Solve[A_PM];
        If (Flag_SaveSolution)
          SaveSolution[A_PM];
        EndIf
        PostOperation[GetPMFlux];
        For k In {0:1}
          InitSolution[A_I~{k}];
          Generate[A_I~{k}]; Solve[A_I~{k}];
          If (Flag_SaveSolution)
            SaveSolution[A_I~{k}];
          EndIf
          PostOperation[GetFluxWithoutPM~{k}];
        EndFor
      EndIf

      If (Flag_AnalysisType == 1)
        If (timemax>1)
          Printf[
            "Time loop from t_0 = %es to t_max = %fs with dt = %es",
            time0, timemax, delta_time
          ];
        ElseIf (timemax>1e-3)
          Printf[
            "Time loop from t_0 = %fms to t_max = %fms with dt = %fms",
            time0*1e3, timemax*1e3, delta_time*1e3
          ];
        Else
          Printf[
            "Time loop from t_0 = %fus to t_max = %fus with dt = %fus",
            time0*1e6, timemax*1e6, delta_time*1e6
          ];
        EndIf
        Printf["Executing %.1f steps", Ceil[(timemax-time0)/delta_time]];
        TimeLoopTheta[time0, timemax, delta_time, 1.]{
          // Euler implicit (1) -- Crank-Nicolson (0.5)
          // FIXME like this theta cannot be controlled by the user
          ChangeOfCoordinates[ NodesOf[Rotor_Moving], RotatePZ[delta_theta[]]];
          Print[
            {
              Floor[$Time/delta_time]+1,
              Ceil[(timemax-time0)/delta_time],
              ((Floor[$Time/delta_time]+1) / Ceil[(timemax-time0)/delta_time])*100
            },
            Format "Step %.0f / %.0f  -  %.1f percent"];
          // Print[{$Time}, Format "Time: %f"];
          MeshMovingBand2D[MB];
          Evaluate[$RPos=RotorPosition_deg[]];
          Evaluate[$PAng_mod=RotorPos_deg_mod[]];
          Evaluate[$PAng=Theta_Park_deg[]];

          If(!Flag_NL)
            Generate[A]; Solve[A];
          Else
            IterativeLoop[Nb_max_iter, stop_criterion, relaxation_factor] {
              GenerateJac[A] ; SolveJac[A] ; }
          EndIf
          // PostOperations:
          If(Flag_ParkTransformation && Flag_SrcType_Stator == CURRENT_SOURCE)
            // Had to shift PostOperation ThetaPark_IABC here, because if you
            // evaluate it before the solution process, you don't get the right
            // time step for the first iteration (= first rotational step).
            // Time for first rotational step would still be 0, but should be
            // "delta_time"
            PostOperation[ThetaPark_IABC] ;
          EndIf
          If (Flag_SaveSolution)
            SaveSolution[A];
          EndIf
          If(Flag_Debug)
            PostOperation[Debug];
          EndIf
          If(Flag_PrintFields)
            PostOperation[Get_LocalFields] ;
            PostOperation[GetBRadTanAirGap];
          EndIf
          PostOperation[Get_GlobalQuantities];
          If(Flag_Calculate_ONELAB)
            PostOperation[Get_Torque] ;
          EndIf
          If(Flag_Calculate_VW)
            PostOperation[Get_Torque_VW] ;
          EndIf
          PostOperation[GetInducedVoltages];
          If (Flag_EC_Magnets)
            PostOperation[Get_EC_LossesMagnets];
          EndIf
          If (Flag_Cir)
            If (R_terminal < 1 ) // Threshold for short circuit current evaluation
              PostOperation[GetShortCircuitCurrent];
            EndIf
          EndIf
          If (Flag_Inductance)
            InitSolution[A_PM];
            Generate[A_PM]; Solve[A_PM];
            If (Flag_SaveSolution)
              SaveSolution[A_PM];
            EndIf
            PostOperation[GetPMFlux];
            For k In {0:1}
              InitSolution[A_I~{k}];
              Generate[A_I~{k}]; Solve[A_I~{k}];
              If (Flag_SaveSolution)
                SaveSolution[A_I~{k}];
              EndIf
              PostOperation[GetFluxWithoutPM~{k}];
            EndFor
          EndIf
          // End of Time Loop
        }
        ChangeOfCoordinates[ NodesOf[Rotor_Moving], RotatePZ[-(finalrotor_pos)*Pi/180]];
      EndIf // End If (Flag_AnalysisType==1)
    }
  }
}
// Include "Tables_ECLossesLaminations.pro";  // For the computation of the EddyCurrent Tables for the simulink model

//-------------------------------------------------------------------------------------------
// In this object the Post processed quantities are defined and the expression of the different quantities are given. Multiple Postprocessings can be defined. Each one of them is given a name for identification and the name of the formulation on which it is applicable is also mentioned.
// There are different Types of PostProceessing Types
//    * integral : in this case, the quantity is integrated over the elements to get a single value per calculation (global quantity)
//    * Term     : in this case the quantitiy can calculated for each element given in the passed Region (see what follows after "In" below) (local quantity)

// Note: just because after the "In" statement the complete domain is listed, doesn't mean that in the end, it will be calculated for the complete domain it simply means that this quantity is defined for the complete domain, but we can only choose to apply it to a Subregion....
// This is defined in the PostOperation Object Below. For example, we can define the eqution for calculating torque on the complete domain, but only calculate it in the airgap. Inversely, if we only define the postprocessing eauqtion for a subregion of domain, but use the complete domain in the postOperation, is considered on the regions of the domain not defined in the mentioned subregion. For a small example see below.
PostProcessing {
  If (Flag_Inductance)
    // New PostProcessing: Frozen_PM
    { Name Frozen_PM ;
      NameOfFormulation MagSta_PM ;
      PostQuantity {
        // Here we define the equation to be used to calculate the flux linkage
        // For a explanation on this equation see : https://www.crcpress.com/Electrical-Machine-Analysis-Using-Finite-Elements/Bianchi/p/ book/9780849333996
        // in short the flux linkage of a given phase is defined by the surface integral
        // int_PhaseX (\vec{J1A}*\vec{a}) dV, in which J1A is a vector pointing in the direction of the current flow, and having the norm   nbrTurns/SurfaceCoil
        // since we are in the 2-D case both J1A and a are in the z-direction only ==> the integral is scalar!!
        // Since we have a 2-D model ==> we also need to multiply with the stack Length (dV = Lstk* dA)
        // Moreover, as we consider symmetry, we also need to multiply the result with the symmetryFactor
        // Since we have an integration we need to provide the integration method to be used
        {
          Name Flux ;
          Value {
            Integral { [ SymmetryFactor*axialLength[]*Idir[]*NbWires[]/SurfCoil[]/NbrParallelPaths * CompZ[{a_PM}] ] ;In Inds  ; Jacobian Vol ; Integration I1 ; }
          }
        }
        // As explained before, to output functions, we need to apply the post Processing to a Dummy domain....
        // For a Post Porcessing in which we plot something on a per element Basis, see further down.
        {
          Name Flux_d  ;
          Value {
            Term { Type Global; [ CompX[Flux_dq0_PM[]] ] ; In DomainDummy ; }
          }
        }
        {
          Name Flux_q  ;
          Value {
            Term { Type Global; [ CompY[Flux_dq0_PM[]] ] ; In DomainDummy ; }
          }
        }
        {
          Name Flux_0  ;
          Value {
            Term { Type Global; [ CompZ[Flux_dq0_PM[]] ] ; In DomainDummy ; }
          }
        }
      }
    }
    // New PostProcessing: Frozen_I_0
    { Name Frozen_I_0 ;
      NameOfFormulation MagSta_Currents_0;
      PostQuantity {
        {
          Name Flux ;
          Value {
            Integral { [ SymmetryFactor*axialLength[]*Idir[]*NbWires[]/SurfCoil[]/NbrParallelPaths* CompZ[{a_I_0}] ] ; In Inds  ; Jacobian Vol ; Integration I1 ; }
          }
        }

        {
          Name Flux_d  ;
          Value {
            Term { Type Global; [ CompX[Flux_dq0_Id[]] ] ; In DomainDummy ; }
          }
        }
        {
          Name Flux_q  ;
          Value {
            Term { Type Global; [ CompY[Flux_dq0_Id[]] ] ; In DomainDummy ; }
          }
        }
        {
          Name Flux_0  ;
          Value {
            Term { Type Global; [ CompZ[Flux_dq0_Id[]] ] ; In DomainDummy ; }
          }
        }
        {
          Name Ld  ;
          Value {
            Term { Type Global; [ Ld[] ] ; In DomainDummy ; }
          }
        }
        {
          Name Ldq  ;
          Value {
            Term { Type Global; [ Ldq[] ] ; In DomainDummy ; }
          }
        }
      }
    }
    // New PostProcessing: Frozen_I_1
    { Name Frozen_I_1 ;
      NameOfFormulation MagSta_Currents_1;
      PostQuantity {
        {
          Name Flux ;
          Value {
            Integral { [ SymmetryFactor*axialLength[]*Idir[]*NbWires[]/SurfCoil[]/NbrParallelPaths* CompZ[{a_I_1}] ] ; In Inds  ; Jacobian Vol ; Integration I1 ; }
          }
        }
        {
          Name Flux_d  ;
          Value {
            Term { Type Global; [ CompX[Flux_dq0_Iq[]] ] ; In DomainDummy ; }
          }
        }
        {
          Name Flux_q  ;
          Value {
            Term { Type Global; [ CompY[Flux_dq0_Iq[]] ] ; In DomainDummy ; }
          }
        }
        {
          Name Flux_0  ;
          Value {
            Term { Type Global; [ CompZ[Flux_dq0_Iq[]] ] ; In DomainDummy ; }
          }
        }
        {
          Name Lq  ;
          Value {
            Term { Type Global; [ Lq[] ] ; In DomainDummy ; }
          }
        }
      }
    }
  EndIf // (Flag_Inductance)

  // New PostProcessing: MagStaDyn_a_2D
  {
    Name MagStaDyn_a_2D;
    NameOfFormulation MagStaDyn_a_2D;
    NameOfSystem A;
    PostQuantity {
      { Name domain ; Value { Term { [ 1 ] ; In Domain ; Jacobian Vol ; } } }
      { Name boundary ; Value { Term { [ 1 ] ; In DomainPlotMovingGeo ; Jacobian Vol ; } } } // Dummy value - for visualization
      { Name surf; Value{ Integral { [ 1 ]; In Domain; Jacobian Vol; Integration I1; } } }

      { Name intAxLen; Value{ Integral { [ axialLength[]/SurfaceArea[] ]; In Domain; Jacobian Vol; Integration I1; } } }
      { Name axLen ; Value { Term { [ axialLength[] ] ; In Domain ; Jacobian Vol ; } } } // Dummy value - for visualization
      // { Name axLenValue; Value{ Term { Type Global; [ axialLength[] ]; In DomainDummy; Jacobian Vol; Integration I1; } } } // This does NOT work...

      { Name surfCoil; Value{ Term { Type Global; [ SurfCoil[] ]; In DomainDummy; Jacobian Vol; Integration I1; } } }
      // { Name surfCoil; Value{ Integral { [ SurfCoil[]/SurfaceArea[] ]; In Domain; Jacobian Vol; Integration I1; } } }

      { Name a  ; Value { Term { [ {a} ] ; In Domain ; Jacobian Vol ; } } }
      { Name az ; Value { Term { [ CompZ[{a}] ] ; In Domain ; Jacobian Vol ; } } }
      // Here we plot the b field on a per element basis (local quantity) since  b is defined as b=curl a. We state that the Term is {d a}. We could also have written {Curl a}. In GetDP the d operator takes the correct differential operator (div, curl, rot) depending on the differential form on which it is applied. (See function space above, or search for Tonti diagram):
      { Name b  ; Value { Term { [ {d a} ] ; In Domain ; Jacobian Vol ; } } }
      { Name bn  ; Value { Term { [ Norm[{d a}] ] ; In Domain ; Jacobian Vol ; } } }
      { Name hn  ; Value { Term { [ Norm[nu[{d a}]*{d a}] ] ; In Domain ; Jacobian Vol ; } } }
      {
        Name b_radial ;
        Value {
          Term { [ {d a}* Vector[  Cos[AngularPosition[]#4], Sin[#4], 0.] ] ;
            In Domain ; Jacobian Vol ; }
          Term { [ {d a}* Vector[  Cos[AngularPosition[]#4], Sin[#4], 0.] ] ;
            In Region[{Rotor_Bnd_MB,Stator_Bnd_MB}] ; Jacobian Sur ; }
        }
      }
      { Name b_tangent ;
        Value {
          Term { [ {d a}* Vector[ -Sin[AngularPosition[]#4], Cos[#4], 0.] ] ;
            In Domain ; Jacobian Vol ; }
          Term { [ {d a}* Vector[ -Sin[AngularPosition[]#4], Cos[#4], 0.] ] ;
            In Region[{Rotor_Bnd_MB, Stator_Bnd_MB}] ; Jacobian Sur ; }
        }
      }
      { Name br ; Value { Term { [ br[] ] ;      In DomainM ; Jacobian Vol ; } } }
      { Name mu ; Value { Term { [ 1/nu[{d a}]/(mu0) ] ; In Domain ; Jacobian Vol ; } } }
      { Name ur  ; Value { Term { [ {ur} ]; In DomainC ; Jacobian Vol ; } } }
      { Name urz  ; Value { Term { [ CompZ[{ur}] ]; In DomainC ; Jacobian Vol ; } } }
      { Name dta  ; Value { Term { [ Dt[{a}] ]; In DomainC ; Jacobian Vol ; } } }
      { Name dta_ur  ; Value { Term { [ Dt[{a}]+{ur} ]; In DomainC ; Jacobian Vol ; } } }
      { Name j  ; Value {
          Term { [ -sigma[]*(Dt[{a}]+{ur}) ];       In DomainC ; Jacobian Vol ; }
          Term { [ js[] ] ;                         In DomainS ; Jacobian Vol ; }
          Term { [ -NbWires[]/SurfCoil[] * {ir} ];  In DomainB ; Jacobian Vol ; }
        }
      }
      { Name js ; Value { Term { [ js[] ] ;      In DomainS ; Jacobian Vol ; } } }
      { Name jz ; Value { Term { [ CompZ[-sigma[]*(Dt[{a}]+{ur})] ]; In DomainC ; Jacobian Vol ; } } }
      // Integral over current density results in Ampere-Turns for wound areas (DomainS and DomainB)
      { Name intJz ; Value {
        Integral { [ CompZ[-sigma[]*(Dt[{a}]+{ur})] ];      In DomainC ; Jacobian Vol ; Integration I1; }
        Integral { [ CompZ[ js[] ] ];                       In DomainS ; Jacobian Vol ; Integration I1; }
        Integral { [ CompZ[-NbWires[]/SurfCoil[] * {ir}] ]; In DomainB ; Jacobian Vol ; Integration I1; }
        }
      }
      // { Name intSigma ; Value { Integral { [ sigma[] ]; In DomainC ; Jacobian Vol ; } } }
      { Name Vmag ; Value { Term { [ CompZ[js[]] * SurfaceArea[]  ]; In DomainS ; Jacobian Vol ; } } } // magnetic voltage (magentische Durchflutung /Theta der Wicklung) [A Turns]
      { Name I_n ; Value { Term { [ CompZ[js[]] * SurfaceArea[] / NbWires[]  ]; In DomainS ; Jacobian Vol ; } } } // Shows the actual current in the specified coil region [A]
      // { Name I_S ; Value {
      //   // Actual Phase current = int {Jz dA} / nbrOfSurfaces / nbrWires * nbrParallelPaths
      //   Integral { [ CompZ[ js[] ] * Idir[] / nbrSlotSurfsPerPhase / NbWires[] * NbrParallelPaths]; In DomainS ; Jacobian Vol ; Integration I1 ;}
      // } } //
      // PP for DomainB
      { Name ir ; Value { Term { [ {ir} ] ; In DomainB ; Jacobian Vol ; } } }
      // Voltage density over stator winding
      { Name u_R; Value{ Term{ [ Resistance[] * CompZ[{ir}]];                  In DomainB; Jacobian Vol;}}}
      // Actual voltage drop over winding resistance on stator Winding
      { Name U_R; Value{ Term {[  Resistance[] * {Ib}]; In DomainB; }}}
      // eddy currents in laminations:
      { Name p_Lam ; Value { Term { [ 1/density[]*Fac_Lam[]*SquNorm[Dt[{d a}]] ] ; In Domain_Lam ; Jacobian Vol ; } } }
      { Name P_Lam ; Value { Integral { [ SymmetryFactor*axialLength[]*Fac_Lam[]*SquNorm[Dt[{d a}]] ]; In Domain_Lam ; Jacobian Vol ; Integration I1 ; } } }
      // Inertia
	    { Name Inertia; Value { Integral { [ SymmetryFactor*SquNorm[XYZ[]]*density[]*axialLength[] ]; In Rotor; Jacobian Vol; Integration I1;}}}
      {
        Name JouleLosses ;
        Value {
          Integral { [ SymmetryFactor*axialLength[]*sigma[] * SquNorm[ Dt[{a}]+{ur} ] ] ; In DomainC ; Jacobian Vol ; Integration I1 ; }
          Integral { [ 1./sigma[]*SquNorm[ IA[]*{ir} ] ] ; In PhaseA ; Jacobian Vol ; Integration I1 ; }
          Integral { [ 1./sigma[]*SquNorm[ IB[]*{ir} ] ] ; In PhaseB  ; Jacobian Vol ; Integration I1 ; }
          Integral { [ 1./sigma[]*SquNorm[ IC[]*{ir} ] ] ; In PhaseC  ; Jacobian Vol ; Integration I1 ; }
        }
      }
      {
        Name p_Joule ;
        Value {
          Term { [ sigma[] * SquNorm[ Dt[{a}]+{ur} ] ] ; In Region[{DomainC}] ; Jacobian Vol ;}
        }
      }
      {
        Name Flux ;
        Value {
          Integral { [ SymmetryFactor*axialLength[]*Idir[]*NbWires[]/SurfCoil[]/NbrParallelPaths* CompZ[{a}] ] ; In Inds  ; Jacobian Vol ; Integration I1 ; }
          Integral { [ axialLength[] * CompZ[{a}] / SurfaceArea[]] ; In DomainC  ; Jacobian Vol ; Integration I1 ; }

        }
      }
      // Force computation by Virtual Works
      { Name Force_vw ; Value {
        Integral { Type Global ; [ 0.5 * nu[] * VirtualWork [{d a}] * axialLength[] ]; In ElementsOf[Rotor_Airgap, OnOneSideOf Rotor_Bnd_MB]; Jacobian Vol ; Integration I1 ; }
      } }

     { Name Torque_vw ; Value {
	      // Torque computation via Virtual Works
         Integral { Type Global ; [ - SymmetryFactor * CompZ[ 0.5 * nu[] * XYZ[] /\ VirtualWork[{d a}] ] * axialLength[] ];
         In ElementsOf[Rotor_Airgap, OnOneSideOf Rotor_Bnd_MB]; Jacobian Vol ; Integration I1 ; }
       }
     }
     { Name Torque_vw_s ; Value {
        // Torque computation via Virtual Works
        Integral { Type Global ; [ SymmetryFactor * CompZ[ 0.5 * nu[] * XYZ[] /\ VirtualWork[{d a}] ] * axialLength[] ];
        In ElementsOf[Stator_Airgap, OnOneSideOf Stator_Bnd_MB]; Jacobian Vol ; Integration I1 ; }
        }
      }


     { Name Torque_Maxwell_r ;
       // Torque computation via Maxwell stress tensor
       Value {
         Integral {
           // \int_S (\vec{r} \times (T_max \vec{n}) ) / ep
           // with ep = |S| / (2\pi r_avg)
           [ CompZ [ (XYZ[]-RotCenter_Current[]) /\ (T_max[{Curl a}] * (XYZ[]-RotCenter_Current[])) ] * 2*Pi*axialLength[]/SurfaceArea[] ] ;
           In Domain ; Jacobian Vol  ; Integration I1; }
       }
     }

     { Name Torque_Maxwell_s ;
       // Torque computation via Maxwell stress tensor
       Value {
         Integral {
           // \int_S (\vec{r} \times (T_max \vec{n}) ) / ep
           // with ep = |S| / (2\pi r_avg)
           [ CompZ [ XYZ[] /\ (T_max[{Curl a}] * XYZ[]) ] * 2*Pi*axialLength[]/SurfaceArea[] ] ;
          //  [ CompZ [ (XYZ[]-RotCenter_Current[]) /\ (T_max[{Curl a}] * (XYZ[]-RotCenter_Current[])) ] * 2*Pi*axialLength[]/SurfaceArea[] ] ;
           In Domain ; Jacobian Vol  ; Integration I1; }
        }
      }


	   { Name InducedVoltage  ;
        Value {
          Integral { [ SymmetryFactor * axialLength[] * Idir[] * NbWires[] / SurfCoil[] / NbrParallelPaths * Dt[CompZ[{a}]] ] ;
          In Inds  ; Jacobian Vol ; Integration I1 ; }
          Integral { [ axialLength[] * Dt[CompZ[{a}]] / SurfaceArea[]] ;
          In DomainC  ; Jacobian Vol ; Integration I1 ; }
        }
      }

     { Name ComplexPower ;
        // TODO: Check if implementation of power is valid for nonlinear definition
        // in DomainC!
       // S = P + i*Q
       Value {
         Integral { [ Complex[ sigma[]*SquNorm[Dt[{a}]+{ur}], nu[]*SquNorm[{d a}] ] ] ;
           In Region[{DomainC}] ; Jacobian Vol ; Integration I1 ; }
       }
     }

     { Name U ; Value {
         Term { [ {U} ]   ; In DomainC ; }
         Term { [ {Ub} * Idir[] ]  ; In DomainB ; }
         Term { [ {Uz} ]  ; In DomainZt_Cir ; }
     } }

     { Name I ; Value {
         Term { [ {I} ]   ; In DomainC ; }
         Term { [ {Ib} * Idir[] ]  ; In DomainB ; }
         Term { [ {Iz} ]  ; In DomainZt_Cir ; }
     } }

     { Name S ; Value {
         Term { [ {U}*Conj[{I}] ]    ; In DomainC ; }
         Term { [ {Ub}*Conj[{Ib}] ]  ; In DomainB ; }
         Term { [ {Uz}*Conj[{Iz}] ]  ; In DomainZt_Cir ; }
     } }

     { Name RotorPosition_deg ; Value { Term { Type Global; [ $RPos ] ; In DomainDummy ; } } }
     {
      Name R ; Value {
        Term { Type Global; [ Rb[] ] ; In DomainDummy; }
      }
    }
    {
      Name Resistance; Value{
        Integral {
          [ Resistance[]/SurfaceArea[] ]; In DomainB; Jacobian Vol; Integration I1;
        }
        If (MachineType==ASYNCHRONOUS)
          // Calculation of DC bar resistance in case ASM
          Integral { [ axialLength[] / sigma[] / SurfBar[]^2]; In Rotor_Bars; Jacobian Vol; Integration I1; }
        EndIf
      }
    }
    { Name R_Bar; Value{
        Integral { [
          // = P_el / I_bar^2
          axialLength[]*sigma[]*SquNorm[(Dt[{a}]+{ur})]
        ]; In Rotor_Bars; Jacobian Vol; Integration I1; }
        Term { [ 1 / SquNorm[{I}] ]   ; In Rotor_Bars ; }
      }
    }
    { Name Theta_Park_deg ; Value { Term { Type Global; [ $PAng ] ; In DomainDummy ; } } }
    { Name IA  ; Value { Term { Type Global; [ II*IA[] ] ; In DomainDummy ; } } }
    { Name IB  ; Value { Term { Type Global; [ II*IB[] ] ; In DomainDummy ; } } }
    { Name IC  ; Value { Term { Type Global; [ II*IC[] ] ; In DomainDummy ; } } }
    { Name Flux_d  ; Value { Term { Type Global; [ CompX[Flux_dq0[]] ] ; In DomainDummy ; } } }
    { Name Flux_q  ; Value { Term { Type Global; [ CompY[Flux_dq0[]] ] ; In DomainDummy ; } } }
    { Name Flux_0  ; Value { Term { Type Global; [ CompZ[Flux_dq0[]] ] ; In DomainDummy ; } } }
   }
 }

}

//-------------------------------------------------------------------------------------------

po      = StrCat["Output - Electromagnetics/", ResId];
poI     = StrCat[po,"0Current [A]/"];
poV     = StrCat[po,"1Voltage [V]/"];
poF     = StrCat[po,"2Flux linkage [Vs]/"];
poJL    = StrCat[po,"3Joule Losses [W]/"];
po_mec  = StrCat["Output - Mechanics/", ResId];
po_mecT = StrCat[po_mec,"0Torque [Nm]/"];
po_mecS = StrCat[po_mec,"1Surface [m²]/"];

//-------------------------------------------------------------------------------------------
// The post Operation block defines the Calculations to be actually calcuated (before we simply defined the formulas on how  to calculate it). Each PostOperation has a Name and is linked to a PostProcessing defined before, the name of this PostProcessing is given after the UsingPost statement below.
// Post Operations are defined with the Print statement.
PostOperation Debug UsingPost MagStaDyn_a_2D{
  // // Print all entities in domain
  // Print[ domain, OnElementsOf Domain, File StrCat[ResDir,"domain",ExtGmsh], LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps] ;
  // // Print the boundary lines -
  // Print[ boundary, OnElementsOf DomainPlotMovingGeo, File StrCat[ResDir,"bnd",ExtGmsh], LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps] ;
  // Echo[ Str["For i In {PostProcessing.NbViews-1:0:-1}",
  //   "  If(!StrCmp(View[i].Name, 'boundary'))",
  //   "    View[i].ShowElement=1;",
  //   "   EndIf",
  //   "EndFor"], File StrCat[ResDir, "tmp.geo"], LastTimeStepOnly] ;

  // #######################################################
  // Axial length with function definition works fine...
  // Integral over axial length function divided by SurfaceArea[] results in mean axial length of integration surface:
  Print[
    intAxLen[Stator_Airgap], OnGlobal, Format Table, LastTimeStepOnly,
    File StrCat[ResDir,"Integral_axLen_AirgapStator",ExtGnuplot],
    SendToServer StrCat[po_mec,"Axial Length Stator Airgap [m]"]{0}, Color "LightYellow"
  ];
  // Show surface area of stator airgap
  Print[
    surf[Stator_Airgap], OnGlobal, Format Table, LastTimeStepOnly,
    File StrCat[ResDir,"Surf_StLu2",ExtGnuplot],
    SendToServer StrCat[po_mecS,"Stator Airgap"]{0}, Color "LightYellow"
  ];
  // Print axial length on domain
  Print[
    axLen, OnElementsOf Domain, LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps,
    File StrCat[ResDir,"AxialeLaenge",ExtGmsh]
  ] ;
  // #######################################################

  // Print[ Vmag, OnElementsOf DomainS, File StrCat[ResDir,"magDurchflutung",ExtGmsh], LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps ] ;
  // Print[ I_n, OnElementsOf DomainS, File StrCat[ResDir,"Current",ExtGmsh], LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps ] ;
  Print [
    surfCoil , OnRegion DomainDummy, Format Table, LastTimeStepOnly,
    SendToServer StrCat[po_mecS,"Value of SurfCoil[] function"]{0}, Color "LightYellow"
  ];
  // Print[ surfCoil[PhaseA_pos], OnGlobal, Format Table, LastTimeStepOnly, File StrCat[ResDir,"SurfCoil_Debug",ExtGnuplot], SendToServer StrCat[po_mecS,"SurfCoil"]{0}, Color "LightYellow"];
  // Print[ surf[PhaseA_pos], OnGlobal, Format Table, LastTimeStepOnly, File StrCat[ResDir,"Surf_Phase_A_pos",ExtGnuplot], SendToServer StrCat[po_mecS,"Surf_Phase_A_pos"]{0}, Color "LightYellow"];
  // Print[ domain, OnElementsOf PhaseA_pos, File StrCat[ResDir,"PhaseA_pos",ExtGmsh],LastTimeStepOnly];
  // Print[ b_radial, OnGrid{(r_AG)*Sin[Pi/nbrSlots-$A*Pi/180],(r_AG)*Cos[Pi/nbrSlots-$A*Pi/180],0 }{0:360/SymmetryFactor,0,0},
  //   File StrCat[ResDir,"brad",ExtGmsh] ];
  // Print[ b_tangent, OnGrid{(r_AG)*Sin[Pi/nbrSlots-$A*Pi/180],(r_AG)*Cos[Pi/nbrSlots-$A*Pi/180],0 }{0:360/SymmetryFactor,0,0},
  //   File StrCat[ResDir,"btan",ExtGmsh] ];
  // Print[
  //   I_S[PhaseA], OnGlobal, Format TimeTable, LastTimeStepOnly,
  //   File>StrCat[ResDir,"Ia",ExtGnuplot],
  //   SendToServer StrCat[poI,"A"]{0}, Color "Pink"
  // ];

  If (nbrRotorBars>0)
    Print[
      j, OnElementsOf Rotor_Bars, File StrCat[ResDir, "j_bars", ExtGmsh],
      LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps
    ];

    If (Flag_Cir_RotorCage)
    //   For iBar In {1:nbrRotorBars}
        // Print[
        //   I, OnRegion Rotor_Bar~{iBar}, Format Table,
        //   File > StrCat[ResDir,"I_bar_", Sprintf["%.0f",iBar], ExtGnuplot], LastTimeStepOnly,
        //   SendToServer StrCat[poI,"I (Bar ",Sprintf["%.0f",iBar], ")"]{0}, Color "LightYellow",
        //   StoreInVariable $I_Bar~{iBar}
        // ];
        // Print[
        //   U, OnRegion Rotor_Bar~{iBar}, Format Table,
        //   File > StrCat[ResDir,"U_bar_", Sprintf["%.0f",iBar], ExtGnuplot], LastTimeStepOnly,
        //   SendToServer StrCat[poV,Sprintf["Rotor Bars/Bar %.0f",iBar]]{0}, Color "LightYellow"
        // ];
        // Print[
        //   ComplexPower[Rotor_Bar~{iBar}], OnGlobal, Format Table,
        //   File > StrCat[ResDir,"P_bar_", Sprintf["%.0f",iBar],ExtGnuplot], LastTimeStepOnly,
        //   SendToServer StrCat[poI,"P_complex (Bar ",Sprintf["%.0f",iBar], ")"]{0}, Color "LightRed"
        // ];
      // EndFor
      Print[
        intJz[Rotor_Bar_1], OnGlobal, Format Table,
        File > StrCat[ResDir,"intJz_bar_1",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poI,"I (Bar 1) = IntJz (Bar 1)"]{0}, Color "LightYellow"
      ];
    EndIf
  EndIf
  If (Flag_SrcType_Stator == VOLTAGE_SOURCE)
    Print[
      j, OnElementsOf DomainB, File StrCat[ResDir,"j_DomaiB",ExtGmsh], LastTimeStepOnly,
      AppendTimeStepToFileName Flag_SaveAllSteps, Name "j on DomainB"
    ];
    Print[
      Resistance[PhaseA], OnGlobal, Format Table, LastTimeStepOnly,
      File > StrCat[ResDir,"R_A",ExtGnuplot], SendToServer StrCat[po,"/Reistance/A"]{0}
    ];
    Print[
      Resistance[PhaseB], OnGlobal, Format Table, LastTimeStepOnly,
      File > StrCat[ResDir,"R_B",ExtGnuplot], SendToServer StrCat[po,"/Reistance/B"]{0}
    ];
    Print[
      Resistance[PhaseC], OnGlobal, Format Table, LastTimeStepOnly,
      File > StrCat[ResDir,"R_C",ExtGnuplot], SendToServer StrCat[po,"/Reistance/C"]{0}
    ];
    Print[
      ir, OnElementsOf DomainB, File StrCat[ResDir, "ir", ExtGmsh], LastTimeStepOnly,
      Name "ir on DomainB"
    ];
    Print[
      u_R, OnElementsOf DomainB, File StrCat[ResDir, "u_R", ExtGmsh], LastTimeStepOnly,
      Name "u_R on DomainB"
    ];
    Print[
      U_R, OnRegion PhaseA, Format Table, LastTimeStepOnly,
      File > StrCat[ResDir,"U_RA",ExtGnuplot], SendToServer StrCat[poV,"U_RA"]{0}
    ];

  EndIf
}

PostOperation Get_LocalFields UsingPost MagStaDyn_a_2D {
  // If we read the statement below, we would have:
  // Print the PostProcessing Quantity "jz" on the elements of the Region "DomainC" and save the Results (but only the results of the last time step) to the file "StrCat[ResDir,"jz",ExtGmsh]" (variables were defined before!) and append to the extension of the file the number of the timestep if Flag_SaveAllSteps > 0.
  // For an example in which we integrate a postquantiy see the example of the flux calcultation in the PostOperation "Get_GlobalQuantities".
  //------------------------------
  // Print[ jz, OnElementsOf DomainC, File StrCat[ResDir,"jz",ExtGmsh], LastTimeStepOnly,
	//  AppendTimeStepToFileName Flag_SaveAllSteps ] ;

  Print[
    j, OnElementsOf Region[{DomainS, DomainB}], File StrCat[ResDir,"js",ExtGmsh], LastTimeStepOnly,
    AppendTimeStepToFileName Flag_SaveAllSteps, Name "j (source)"
  ] ;

  Print[
    b,  OnElementsOf Domain, File StrCat[ResDir,"b",ExtGmsh], Format Gmsh,
    LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps
  ] ;

  Print[
    bn,  OnElementsOf Domain, File StrCat[ResDir,"bn",ExtGmsh], Format Gmsh,
    LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps
  ] ;

  Print[
    mu, OnElementsOf Domain, File StrCat[ResDir,"mu_r",ExtGmsh], LastTimeStepOnly,
    AppendTimeStepToFileName Flag_SaveAllSteps
  ] ;

  Print[
    az, OnElementsOf Domain, File StrCat[ResDir,"az",ExtGmsh], LastTimeStepOnly,
    AppendTimeStepToFileName Flag_SaveAllSteps
  ] ;
  Echo[ Str["l=PostProcessing.NbViews-1;", "View[l].IntervalsType = 1;", "View[l].NbIso = 30;", "View[l].Light = 0;", "View[l].LineWidth = 2;"],
    File StrCat[ResDir,"tmp.geo"], LastTimeStepOnly
  ] ;

  If (Flag_Lam)
    Print[
      p_Lam, OnElementsOf Domain_Lam, File StrCat[ResDir,"p_Lam.pos"],
      LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps
    ];
  EndIf
  If (Flag_EC_Magnets)
    Print[
      p_Joule, OnElementsOf Rotor_Magnets, File StrCat[ResDir,"p_EC_Mag.pos"],
      LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps
    ];
  EndIf
  If (Flag_Cir_RotorCage)
    Print[
      jz, OnElementsOf Rotor_Bars, File StrCat[ResDir, "jz_bars", ExtGmsh],
      LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps
    ];
  EndIf
}

PostOperation GetInertia UsingPost MagStaDyn_a_2D {
	Print[
    Inertia[Rotor], OnGlobal, Format Table, StoreInVariable $Inertia,
    LastTimeStepOnly, SendToServer StrCat[po_mec,"/000Inertia (kg*m^2)"]
	];
}

PostOperation PrintBFields UsingPost MagStaDyn_a_2D {
    Print[ b,  OnElementsOf Domain_Lam, File StrCat[ResDir,"b_Iron",ExtGmsh]] ;
}

PostOperation GetInducedCurrentDensity UsingPost MagStaDyn_a_2D {
    Print[ jz,  OnElementsOf Rotor_Magnets, File StrCat[ResDir,"jzMagnets",ExtGmsh]] ;
}

// PostOperation for getting the tangential and the radial components of the magnetic flux density:
PostOperation GetBRadTanAirGap UsingPost MagStaDyn_a_2D {
  // FIXME: The evaluation of results with 'OnGrid' leads to a individual post-processing
  // view in the Gmsh GUI for each time step. As a workaround we use the 'OnElementsOf'
  // option to get a single PP view for all time steps. Unfortunately the results cannot
  // be shown as a 2D space plot then.

  // Print the radial flux density on a curve in the stator airgap by steps of 0.5 deg
  // We did not manage to evaluate the results this way for the rotor airgap at runtime
  // since, due to the movement of the rotor, the grid must not be static and it seems
  // like the OnGrid option does not allow parametric attributes.
  //
  // Print[
  //   b_radial, OnGrid{r_stator_airgap*Cos[$A*Pi/180],r_stator_airgap*Sin[$A*Pi/180],0 }{0:360/SymmetryFactor:360/NbrMbSegments,0,0},
  //   Name "b radial (stator)", Format Gmsh, File StrCat[ResDir,"b_rad_stator",ExtGmsh],
  //   LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps];
  // Print[
  //   b_tangent, OnGrid{r_stator_airgap*Cos[$A*Pi/180],r_stator_airgap*Sin[$A*Pi/180],0 }{0:360/SymmetryFactor:360/NbrMbSegments,0,0},
  //   Name "b tangential (stator)", Format Gmsh, File StrCat[ResDir,"b_tan_stator",ExtGmsh],
  //   LastTimeStepOnly, AppendTimeStepToFileName Flag_SaveAllSteps];
  //
  // // The evaluation of results with 'OnGrid' interpolates results and leads to a
  // // individual post-processing view in the Gmsh GUI for each time step.
  // // The following code combines the views of each time step into one view, renames
  // // it back to "b radial (stator)" and sets the properties so that its a 2D space plot.
  // // But this only works once. If we run a second simulation in the same GUI session,
  // // the other views of the previous simulation (that have the same name like 'a' or
  // // 'b') are combined as well.
  // Echo[
  //   Str[
  //     "Combine TimeStepsByViewName ;",
  //     "nbViews=PostProcessing.NbViews; ",
  //     "For l In {nbViews-1:0:-1}",
  //     "   If (StrFind[View[l].Name, 'b radial (stator)_Combine'])",
  //     "       View[l].Name = StrReplace(View[l].Name,'_Combine','');",
  //     "       View[l].Visible = 1;",
  //     "       View[l].Type = 2;",
  //     "       View[l].IntervalsType = 3;",
  //     "       View[l].Axes = 3;",
  //     "       View[l].AutoPosition = 2;",
  //     "       View[l].LineWidth = 1;",
  //     "       // l = 0; // stop the loop",
  //     "   EndIf",
  //     "   If (StrFind[View[l].Name, 'b tangential (stator)_Combine'])",
  //     "       View[l].Name = StrReplace(View[l].Name,'_Combine','');",
  //     "       View[l].Visible = 1;",
  //     "       View[l].Type = 2;",
  //     "       View[l].IntervalsType = 3;",
  //     "       View[l].Axes = 3;",
  //     "       View[l].AutoPosition = 4;",
  //     "       View[l].LineWidth = 1;",
  //     "       // l = 0; // stop the loop",
  //     "   EndIf",
  //     "   Printf('l = %.1f', l);",
  //     "   Printf(StrCat['View name: ',View[l].Name]);",
  //     "EndFor"
  //   ],
  //   File StrCat[ResDir,"tmp_combine.geo"],
  //   LastTimeStepOnly
  // ];

  Print[
    b_radial, OnElementsOf Stator_Bnd_MB, Name "b radial (stator)",
    Format Gmsh, File StrCat[ResDir,"b_rad_stator",ExtGmsh], LastTimeStepOnly,
    AppendTimeStepToFileName Flag_SaveAllSteps];
  Print[
    b_tangent, OnElementsOf Stator_Bnd_MB, Name "b tangential (stator)",
    Format Gmsh, File StrCat[ResDir,"b_tan_stator",ExtGmsh], LastTimeStepOnly,
    AppendTimeStepToFileName Flag_SaveAllSteps];
}

PostOperation GetShortCircuitCurrent UsingPost MagStaDyn_a_2D {
  Print[ I, OnRegion PhaseA_pos, Format Table,
    File > StrCat[ResDir,"IshortA",ExtGnuplot], LastTimeStepOnly,
    SendToServer StrCat[poI,"Ashort"]{0}, Color "LightGreen" ];
  Print[ I, OnRegion PhaseB_pos, Format Table,
    File > StrCat[ResDir,"IshortB",ExtGnuplot], LastTimeStepOnly,
    SendToServer StrCat[poI,"Bshort"]{0}, Color "LightGreen" ];
  Print[ I, OnRegion PhaseC_pos, Format Table,
    File > StrCat[ResDir,"IshortC",ExtGnuplot], LastTimeStepOnly,
    SendToServer StrCat[poI,"Cshort"]{0}, Color "LightGreen" ];
}

PostOperation Get_GlobalQuantities UsingPost MagStaDyn_a_2D {
  Print[
    RotorPosition_deg, OnRegion DomainDummy, Format Table, LastTimeStepOnly,
    File>StrCat[ResDir, "RotorPos_deg",ExtGnuplot],
    SendToServer StrCat[po_mec,"9Rotor position [deg]"]{0}, Color "LightYellow"
  ];

  If (Flag_Lam)
    Print[
      P_Lam[Domain_Lam], OnGlobal, Format TimeTable, LastTimeStepOnly,
      File > StrCat[ResDir,Sprintf("Pec_Lam.dat")],
      SendToServer StrCat["Results/EDC/",  Sprintf("43stat lam. losses (W)")]
    ];
  EndIf

  // If(!Flag_Cir)
  //   If(!Flag_ParkTransformation)
  //     Print[ I, OnRegion PhaseA_pos, Format Table,
	//      File > StrCat[ResDir,"Ia",ExtGnuplot], LastTimeStepOnly,
  //      SendToServer StrCat[poI,"A"]{0}, Color "Pink" ];

  //     Print[ I, OnRegion PhaseB_pos, Format Table,
  //       File > StrCat[ResDir,"Ib",ExtGnuplot], LastTimeStepOnly,
  //       SendToServer StrCat[poI,"B"]{0}, Color "Yellow" ];

  //     Print[ I, OnRegion PhaseC_pos, Format Table,
  //       File > StrCat[ResDir,"Ic",ExtGnuplot], LastTimeStepOnly,
  //       SendToServer StrCat[poI,"C"]{0}, Color "LightGreen" ];
  //   EndIf
  // EndIf

  If(Flag_Cir)
    // plot the quantities for phase A in the case we have an external circuit
    // Phase A
    //  Input Values
    Print[ I, OnRegion Input1, Format Table,
     File > StrCat[ResDir,"Ia",ExtGnuplot], LastTimeStepOnly,
     SendToServer StrCat[poI,"Line/","A"]{0}, Color "Pink" ];
     Print[ U, OnRegion Input1, Format Table,
      File > StrCat[ResDir,"Ua",ExtGnuplot], LastTimeStepOnly,
      SendToServer StrCat[poV,"Line/","A"]{0}, Color "Pink" ];
    // Line Values
    If (NbrRegions[PhaseA_pos] > 0)
      Print[ I, OnRegion PhaseA_pos, Format Table,
        File > StrCat[ResDir,"Ia_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poI,"Winding/","A"]{0}, Color "Pink"
      ];
      Print[ U, OnRegion PhaseA_pos, Format Table,
        File > StrCat[ResDir,"Ua_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poV,"Winding/","A"]{0}, Color "Pink"
      ];
    Else
      Print[ I, OnRegion PhaseA, Format Table,
        File > StrCat[ResDir,"Ia_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poI,"Winding/","A"]{0}, Color "Pink"
      ];
      Print[ U, OnRegion PhaseA, Format Table,
        File > StrCat[ResDir,"Ua_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poV,"Winding/","A"]{0}, Color "Pink"
      ];
    EndIf

    // phase B
    //  Input Values
    Print[ I, OnRegion Input2, Format Table,
      File > StrCat[ResDir,"Ib",ExtGnuplot], LastTimeStepOnly,
      SendToServer StrCat[poI,"Line/","B"]{0}, Color "Yellow"
    ];
    Print[ U, OnRegion Input2, Format Table,
      File > StrCat[ResDir,"Ub",ExtGnuplot], LastTimeStepOnly,
      SendToServer StrCat[poV,"Line/","B"]{0}, Color "Yellow"
    ];
    // Line Values
    If (NbrRegions[PhaseB_pos] > 0)
      Print[ I, OnRegion PhaseB_pos, Format Table,
        File > StrCat[ResDir,"Ib_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poI,"Winding/","B"]{0}, Color "Yellow"
      ];
      Print[ U, OnRegion PhaseB_pos, Format Table,
        File > StrCat[ResDir,"Ub_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poV,"Winding/","B"]{0}, Color "Yellow"
      ];
    Else
      Print[ I, OnRegion PhaseB, Format Table,
        File > StrCat[ResDir,"Ib_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poI,"Winding/","B"]{0}, Color "Yellow"
      ];
      Print[ U, OnRegion PhaseB, Format Table,
        File > StrCat[ResDir,"Ub_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poV,"Winding/","B"]{0}, Color "Yellow"
      ];
    EndIf

    // phase C
    //  Input Values
    Print[ I, OnRegion Input3, Format Table,
     File > StrCat[ResDir,"Ic",ExtGnuplot], LastTimeStepOnly,
     SendToServer StrCat[poI,"Line/","C"]{0}, Color "LightGreen" ];
    Print[ U, OnRegion Input3, Format Table,
      File > StrCat[ResDir,"Uc",ExtGnuplot], LastTimeStepOnly,
      SendToServer StrCat[poV,"Line/","C"]{0}, Color "LightGreen" ];
    // Line Values
    If (NbrRegions[PhaseC_pos] > 0)
      Print[ I, OnRegion PhaseC_pos, Format Table,
        File > StrCat[ResDir,"Ic_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poI,"Winding/","C"]{0}, Color "LightGreen"
      ];
      Print[ U, OnRegion PhaseC_pos, Format Table,
        File > StrCat[ResDir,"Uc_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poV,"Winding/","C"]{0}, Color "LightGreen"
      ];
    Else
      Print[ I, OnRegion PhaseC, Format Table,
        File > StrCat[ResDir,"Ic_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poI,"Winding/","C"]{0}, Color "LightGreen"
      ];
      Print[ U, OnRegion PhaseC, Format Table,
        File > StrCat[ResDir,"Uc_w",ExtGnuplot], LastTimeStepOnly,
        SendToServer StrCat[poV,"Winding/","C"]{0}, Color "LightGreen"
      ];
    EndIf
  Else
    // If there is no circuit the current is given by IA[], IB[], IC[]
    Print[
      IA, OnRegion DomainDummy, Format Table,
      File>StrCat[ResDir,"Ia",ExtGnuplot], LastTimeStepOnly,
      SendToServer StrCat[poI,"A"]{0}, Color "Pink"
    ];
    Print[
      IB, OnRegion DomainDummy, Format Table,
      File>StrCat[ResDir,"Ib",ExtGnuplot], LastTimeStepOnly,
      SendToServer StrCat[poI,"B"]{0}, Color "Yellow"
    ];
    Print[
      IC, OnRegion DomainDummy, Format Table,
      File>StrCat[ResDir,"Ic",ExtGnuplot], LastTimeStepOnly,
      SendToServer StrCat[poI,"C"]{0}, Color "LightGreen"
    ];
  EndIf
  // Get global values for induction machine rotor circuit
  If (Flag_Cir_RotorCage)
    Print[
      I, OnRegion Rotor_Bars, Format Table, File > StrCat[ResDir,"I_bars",ExtGnuplot],
      LastTimeStepOnly
    ];
    Print[
      I, OnRegion Rotor_Bar_1, Format ValueOnly, LastTimeStepOnly,
      SendToServer StrCat[poI,"0Rotor Bar 1"]{0}, Color "LightYellow"
    ];
    Print[
      U, OnRegion Rotor_Bars, Format Table, File > StrCat[ResDir,"U_bars",ExtGnuplot],
      LastTimeStepOnly
    ];
    Print[
      U, OnRegion Rotor_Bar_1, Format ValueOnly, LastTimeStepOnly,
      SendToServer StrCat[poV,"0Rotor Bar 1"]{0}, Color "LightYellow"
    ];
  EndIf

  // Calculate the Flux linkage
  // In this case we have an integration quantity. The Region over which we should integrate is given between the brackets.
  // We would read: Print the Flux integrated over Phase A (rememeber that the flux was defined for Inds, for which PhaseX is a subregion) as a global quantity to the file StrCat[ResDir,"Flux_a",ExtGnuplot] (in this case since we have File > ... the quantity is appended, without the ">" it would be erased) for the last timestep only, store the result in the runtime variable $Flux_a (since we need it to calculate the dq0 fluxes) and send the value to the onelab server (GUI) in and include it under StrCat[poF,"A"]{0} with a color "Pink".
  Print[ Flux[PhaseA], OnGlobal, Format TimeTable,
    File > StrCat[ResDir,"Flux_a",ExtGnuplot], LastTimeStepOnly,
          StoreInVariable $Flux_a, SendToServer StrCat[poF,"0A"]{0},  Color "Pink" ];
  Print[ Flux[PhaseB], OnGlobal, Format TimeTable,
    File > StrCat[ResDir,"Flux_b",ExtGnuplot], LastTimeStepOnly,
          StoreInVariable $Flux_b, SendToServer StrCat[poF,"1B"]{0},  Color "Yellow" ];
  Print[ Flux[PhaseC], OnGlobal, Format TimeTable,
    File > StrCat[ResDir,"Flux_c",ExtGnuplot], LastTimeStepOnly,
          StoreInVariable $Flux_c, SendToServer StrCat[poF,"2C"]{0}, Color "LightGreen"];

  // d and q-axis flux linkage
  If (MachineType == SYNCHRONOUS)
    Print[
      Flux_d, OnRegion DomainDummy, Format Table,
      File > StrCat[ResDir,"Flux_d",ExtGnuplot], LastTimeStepOnly,StoreInVariable $Phi_d,
      SendToServer StrCat[poF,"4 d"]{0}, Color "LightYellow"
    ];
    Print[
      Flux_q, OnRegion DomainDummy, Format Table,
      File > StrCat[ResDir,"Flux_q",ExtGnuplot], LastTimeStepOnly,StoreInVariable $Phi_q,
      SendToServer StrCat[poF,"5 q"]{0}, Color "LightYellow"
    ];
    Print[
      Flux_0, OnRegion DomainDummy, Format Table,
      File > StrCat[ResDir,"Flux_0",ExtGnuplot], LastTimeStepOnly,StoreInVariable $Phi_0,
      SendToServer StrCat[poF,"3 0"]{0}, Color "LightYellow"
    ];
  EndIf
}

PostOperation Get_EC_LossesMagnets UsingPost MagStaDyn_a_2D {
  Print[ JouleLosses[Rotor_Magnets], OnGlobal, Format TimeTable,
	  File > StrCat[ResDir,"LossesMagnets",ExtGnuplot], LastTimeStepOnly,
	  SendToServer StrCat[poJL,"PMs"]{0}, Color "LightYellow" ];
}

PostOperation Get_Torque UsingPost MagStaDyn_a_2D {
  // In the case of a static eccentricity, the rotor center is at (0,0,0) => so we calculate the torque on the airgap layer of the rotor
  Print[ Torque_Maxwell_r[Rotor_Airgap], OnGlobal, Format TimeTable,
    File > StrCat[ResDir,"Tr",ExtGnuplot], LastTimeStepOnly, StoreInVariable $Tstator,
    SendToServer StrCat[po_mecT,"ArrkioONELAB_rotor"]{0}, Color "Ivory" ];
  // in the other cases we have either no eccentricity (it does not matter where we calculate the torque) or dynamic eccentricity => stator center at 0,0,0
  // in that case we calculate it on the stator airgap.
  Print[ Torque_Maxwell_s[Stator_Airgap], OnGlobal, Format TimeTable,
    File > StrCat[ResDir,"Ts",ExtGnuplot], LastTimeStepOnly, StoreInVariable $Tstator,
    SendToServer StrCat[po_mecT,"ArrkioONELAB_stator"]{0}, Color "Ivory" ];
}

PostOperation Get_Torque_VW UsingPost MagStaDyn_a_2D {
  // Via virtual work:
  Print[ Torque_vw_s, OnRegion NodesOf[Stator_Bnd_MB], LastTimeStepOnly, Format RegionValue,
    File >  StrCat[ResDir,"Ts_vw", ExtGnuplot], StoreInVariable $Tstator_vw,
    SendToServer StrCat[po_mecT, "VW_stator"]{0}, Color "Ivory"];
  Print[ Torque_vw, OnRegion NodesOf[Rotor_Bnd_MB], LastTimeStepOnly, Format RegionValue,
    File >  StrCat[ResDir,"Tr_vw", ExtGnuplot], StoreInVariable $Trotor_vw,
    SendToServer StrCat[po_mecT, "VW_rotor"]{0}, Color "Ivory"] ;
  }

// PostOperation for getting the inducedVoltaged
PostOperation GetInducedVoltages UsingPost MagStaDyn_a_2D {
  If (Flag_SrcType_Stator != CEMF_SOURCE)
    Print[ InducedVoltage[PhaseA], OnGlobal, Format Table,
      LastTimeStepOnly, SendToServer StrCat[poV,"Induced Voltage","A"]{0},
      File>StrCat[ResDir,"InducedVoltageA",ExtGnuplot], Color "Pink"];
    Print[ InducedVoltage[PhaseB], OnGlobal, Format Table,
      LastTimeStepOnly, SendToServer StrCat[poV,"Induced Voltage","B"]{0},
      File>StrCat[ResDir,"InducedVoltageB",ExtGnuplot], Color "Yellow"];
    Print[ InducedVoltage[PhaseC], OnGlobal, Format Table,
      LastTimeStepOnly, SendToServer StrCat[poV,"Induced Voltage","C"]{0},
      File>StrCat[ResDir,"InducedVoltageC",ExtGnuplot], Color "LightGreen"];
  Else
    Print[ U, OnRegion Rp1, Format Table,
      LastTimeStepOnly, SendToServer StrCat[poV,"Winding/Induced Voltage","A"]{0},
      File>StrCat[ResDir,"InducedVoltageA",ExtGnuplot], Color "Pink"];
    Print[ U, OnRegion Rp2, Format Table,
      LastTimeStepOnly, SendToServer StrCat[poV,"Winding/Induced Voltage","B"]{0},
      File>StrCat[ResDir,"InducedVoltageB",ExtGnuplot], Color "Yellow"];
    Print[ U, OnRegion Rp3, Format Table,
      LastTimeStepOnly, SendToServer StrCat[poV,"Winding/Induced Voltage","C"]{0},
      File>StrCat[ResDir,"InducedVoltageC",ExtGnuplot], Color "LightGreen"];
  EndIf
}

If (Flag_ParkTransformation)
  PostOperation ThetaPark_IABC UsingPost MagStaDyn_a_2D {
    Print[ Theta_Park_deg, OnRegion DomainDummy, Format Table, LastTimeStepOnly,
    File>StrCat[ResDir, "ParkAngle_deg",ExtGnuplot],
    SendToServer StrCat[po,"11Theta park"]{0}, Color "LightYellow" ];

    // ** Moved this to "GetGlobalQuantities" **
    // Print[ IA, OnRegion DomainDummy, Format Table, LastTimeStepOnly,
    // File>StrCat[ResDir,"Ia",ExtGnuplot],
    // SendToServer StrCat[poI,"A"]{0}, Color "Pink" ];
    // Print[ IB, OnRegion DomainDummy, Format Table, LastTimeStepOnly,
    // File>StrCat[ResDir,"Ib",ExtGnuplot],
    // SendToServer StrCat[poI,"B"]{0}, Color "Yellow" ];
    // Print[ IC, OnRegion DomainDummy, Format Table, LastTimeStepOnly,
    // File>StrCat[ResDir,"Ic",ExtGnuplot],
    // SendToServer StrCat[poI,"C"]{0}, Color "LightGreen"  ];
  }
EndIf


// These post operations are used in order to calculate the inductances usingthe frozen permeabilty method see Papers:
//  - https://ieeexplore.ieee.org/document/5316039/
//  - https://ieeexplore.ieee.org/document/732255/

If (Flag_Inductance)
  PostOperation GetPMFlux UsingPost Frozen_PM {
    Print[ Flux[PhaseA], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_a_PM ];
    If(NbrPhases==3)
      Print[ Flux[PhaseB], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_b_PM ];
      Print[ Flux[PhaseC], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_c_PM];
    EndIf

    Print[ Flux_d, OnRegion DomainDummy, Format Table,
  	     File > StrCat[ResDir,"PMFlux_d",ExtGnuplot], LastTimeStepOnly,
  	     SendToServer StrCat[poF,"PM Flux-d"]{0}, Color "LightYellow",
         StoreInVariable $PMFlux_d];
    Print[ Flux_q, OnRegion DomainDummy, Format Table,
  	     File > StrCat[ResDir,"PMFlux_q",ExtGnuplot], LastTimeStepOnly,
  	     SendToServer StrCat[poF,"PM Flux-q"]{0}, Color "LightYellow",
         StoreInVariable $PMFlux_q];
  }

  PostOperation GetFluxWithoutPM_0 UsingPost Frozen_I_0 {
    Print[ Flux[PhaseA], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_a_Id ];
    If(NbrPhases==3)
      Print[ Flux[PhaseB], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_b_Id ];
      Print[ Flux[PhaseC], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_c_Id];
    EndIf

    Print[ Flux_d, OnRegion DomainDummy, Format Table, LastTimeStepOnly];
    Print[ Flux_q, OnRegion DomainDummy, Format Table, LastTimeStepOnly];

    Print [ Ld , OnRegion DomainDummy, Format Table, LastTimeStepOnly,
      File> StrCat[ResDir,"Ld",ExtGnuplot],
      SendToServer StrCat[poF,"Ld [H]"]{0}, Color "LightYellow"];

      Print [ Ldq , OnRegion DomainDummy, Format Table, LastTimeStepOnly,
        File> StrCat[ResDir,"Ldq",ExtGnuplot],
        SendToServer StrCat[poF,"Ldq [H]"]{0}, Color "LightYellow"];
  }

  PostOperation GetFluxWithoutPM_1 UsingPost Frozen_I_1 {
    Print[ Flux[PhaseA], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_a_Iq ];
    If(NbrPhases==3)
      Print[ Flux[PhaseB], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_b_Iq ];
      Print[ Flux[PhaseC], OnGlobal, Format Table, LastTimeStepOnly,
             StoreInVariable $Flux_c_Iq];
    EndIf

    Print[ Flux_d, OnRegion DomainDummy, Format Table, LastTimeStepOnly];
    Print[ Flux_q, OnRegion DomainDummy, Format Table, LastTimeStepOnly];

    Print [ Lq , OnRegion DomainDummy, Format Table, LastTimeStepOnly,
      File> StrCat[ResDir,"Lq",ExtGnuplot],
      SendToServer StrCat[poF,"Lq [H]"]{0}, Color "LightYellow"];
  }
EndIf
