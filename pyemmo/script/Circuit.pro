// CIRCUIT EQUATION
Group {
	// Dummy numbers for circuit definition
	//	Voltage source for stator circuit
	Input1 = #10001;
	Input2 = #10002;
	Input3 = #10003;
	// 	Stator winding resistances
	R1	   = #20001;
	R2     = #20002;
	R3 	   = #20003;
	// 	Terminal connection resistances
	Rp1	   = #20004;
	Rp2    = #20005;
	Rp3    = #20006;

	// Rotor squirrel cage circuit elements
	//	For each rotor bar in the cage create a separate upper and lower end ring
	// 	segement (resistance + inductance) and bar (axial) resistance
	All_EndRingResistancesRotor += Region[ { } ] ;
	All_EndRingInductancesRotor += Region[ { } ] ;
	All_BarResistancesRotor += Region[ { } ] ;
	For k In {1:nbrRotorBars}
		Ruers~{k} = Region[{(60000+k)}]; // resistance per endring segment
		Rlers~{k} = Region[{(70000+k)}]; // resistance per endring segment
		All_EndRingResistancesRotor += Region[ Ruers~{k} ] ;
		All_EndRingResistancesRotor += Region[ Rlers~{k} ] ;
		Luers~{k} = Region[{(80000+k)}]; // inductance per end ring segment
		Llers~{k} = Region[{(90000+k)}]; // inductance per end ring segment
		All_EndRingInductancesRotor += Region[ Luers~{k} ] ;
		All_EndRingInductancesRotor += Region[ Llers~{k} ] ;
		Rbar~{k} = Region[{(95000+k)}];
		All_BarResistancesRotor += Region[ Rbar~{k} ] ;
	EndFor

	// Group all the circuit elements in the respective circuit domains
	Resistance_Cir  = Region[{ }]; // All resistances in the circuit
	Inductance_Cir  = Region[{ }]; // All inductances in the circuit

	Resistance_Cir  += Region[{ All_EndRingResistancesRotor, All_BarResistancesRotor }];
	Inductance_Cir  += Region[{ All_EndRingInductancesRotor }];

	// Why do we need to define Source_Cir and Z_Cir separately?
	DomainSource_Cir = Region[ { } ] ;
	If (Flag_SrcType_Stator != 0)
		Resistance_Cir += #{R1,R2,R3,Rp1,Rp2,Rp3};
		DomainSource_Cir += #{Input1,Input2,Input3};
	Else
		Resistance_Cir += #{Rp1,Rp2,Rp3};
	EndIf
	// Why do we need to define Source_Cir and Z_Cir separately?
	DomainZ_Cir = Region[ {Resistance_Cir, Inductance_Cir} ];
	// Main circuit domain
	DomainZt_Cir    = Region[ {DomainZ_Cir, DomainSource_Cir} ];
}

// =====================================================================================
// =======================STATOR WINDING CIRCUIT========================================
// =====================================================================================

Function {
	If (Flag_SrcType_Stator != CEMF_SOURCE)
		// If source type is not back-emf in circuit
		// Set resistance of phase resistance domain to R_wire parameter
		Resistance[#{R1,R2,R3}] = R_wire;
	EndIf
	// Set terminal resistance to R_terminal parameter
	Resistance[#{Rp1,Rp2,Rp3}] = R_terminal;
}

// =====================================================================================
// ==================SQUIRREL-CAGE INDUCTION MASCHINE ROTOR CIRCUIT=====================
// =====================================================================================

Function {
	// Create node numbers for cage circuit:
	For k In {1:nbrRotorBars} //existing numbers of rotor Bars in the model
		NB1~{k} =  400+k; // first node number for each rotor bar
		NB2~{k} =  500+k; // second node number for extra rotor bar resistance
		NB3~{k} =  600+k; // third node number for each rotor bar
		NIM1~{k} = 700+k; // upper intermediate node number for each rotor bar connection
		NIM2~{k} = 800+k; // lower intermediate node number for each rotor bar connection
	EndFor

	// If only one pole is simulated in the model, the end rings of the A and B
	// sides must be crossed. If one or more pole pairs are simulated, they do not.
	If (NbrPolesInModel%2 == 1)
		For k In {1:nbrRotorBars}
			// Upper Branch
			NRu1~{k} = NB1~{k}; // first node number for upper endring resistance
			// second node number for each endring resistance:
			NRu2~{k} = NIM1~{k}; // = intermediate node

			NLu1~{k} = NRu2~{k}; // first node number for each endring inductance (= output of resistance)
			// second node number for each endring inductance:
			k2 = (k<nbrRotorBars) ? k+1 : 1.; // We need this since in the next inline
			// if statement, the first and second option will both be evaluated at
			// runtime, even if only one of the option is used (like in a real if-case).
			NLu2~{k} = (k<nbrRotorBars) ? NB1~{k2} : NB3~{1} ;

			// Lower Branch
			NRl1~{k} = NB3~{k}; // first node number for lower endring resistance
			// second node number for lower endring resistance:
			NRl2~{k} = NIM2~{k}; // = lower intermediate node

			NLl1~{k} = NRl2~{k}; // first node number for lower endring inductance (= output of lower resistance)
			// second node number for lower endring inductance:
			NLl2~{k} = (k<nbrRotorBars) ? NB3~{k2} : NB1~{1} ;
		EndFor
	ElseIf (NbrPolesInModel>1 && !(NbrPolesInModel%2))
		For k In {1:nbrRotorBars}
			// NR1~{k} = NB1~{k}; // first node number for each endring resistance
			// k2 = (k<nbrRotorBars) ? k+1 : 1.;
			// // second node number for each endring resistance:
			// NR2~{k} = (k<nbrRotorBars) ? NB1~{k2} : NB1~{1} ;
			// NL1~{k} = NB3~{k}; // first node number for each endring inductance
			// // second node number for each endring inductance:
			// NL2~{k} = (k<nbrRotorBars) ? NB3~{k2} : NB3~{1} ;

			// Upper Branch
			NRu1~{k} = NB1~{k}; // first node number for upper endring resistance
			// second node number for each endring resistance:
			NRu2~{k} = NIM1~{k}; // = intermediate node

			NLu1~{k} = NRu2~{k}; // first node number for each endring inductance (=
			// output of resistance)
			// second node number for each endring inductance:
			k2 = (k<nbrRotorBars) ? k+1 : 1.; // We need this since in the next
			// inline if statement, the first and second option will both be
			// evaluated at runtime, even if only one of the option is used (like in
			// a real if-case).
			NLu2~{k} = (k<nbrRotorBars) ? NB1~{k2} : NB1~{1} ;

			// Lower Branch
			NRl1~{k} = NB3~{k}; // first node number for lower endring resistance
			// second node number for lower endring resistance:
			NRl2~{k} = NIM2~{k}; // = lower intermediate node

			NLl1~{k} = NRl2~{k}; // first node number for lower endring inductance (=
			// output of lower resistance)
			// second node number for lower endring inductance:
			NLl2~{k} = (k<nbrRotorBars) ? NB3~{k2} : NB3~{1} ;
	  	EndFor
	Else
		Printf[
			"Unbalanced number of poles (%.0f) for ASM Cage Circuit",
			NbrPolesInModel
		];
	EndIf
	// The values must be twice as large as the real ring section replacement
	// values, as the resistors are only installed on the A side and the
	// inductors only on the B side.
	Resistance[All_EndRingResistancesRotor] = R_endring_segment;
	Inductance[All_EndRingInductancesRotor] = L_endring_segment;
	For k In {1:nbrRotorBars}
	  	Resistance[Rbar~{k}] = $R_Bar~{k};
	EndFor
}

Constraint {
	/*{	Name ElectricalCircuit;
			Type Network;
			Case Circuit1 {
          { Region Input1        ; Branch {100,101} ; }
          { Region Stator_Ind_Ap ; Branch {101,102} ; }
          { Region Stator_Ind_Am ; Branch {103,102} ; }
          { Region R1            ; Branch {103,100} ; }
        }
        Case Circuit2 {
          { Region Input2        ; Branch {200,201} ; }
          { Region Stator_Ind_Bp ; Branch {201,202} ; }
          { Region Stator_Ind_Bm ; Branch {203,202} ; }
          { Region R2            ; Branch {203,200} ; }
        }
        Case Circuit3 {
          { Region Input3       ; Branch {300,301} ; }
          { Region Stator_Ind_Cp ; Branch {301,302} ; }
          { Region Stator_Ind_Cm ; Branch {303,302} ; }
          { Region R3            ; Branch {303,300} ; }
        }
      }*/
{
	Name ElectricalCircuit;
	Type Network;
	If(CircuitConnection == STAR_CONNECTION)
		Case Circuit1 {
			If (Flag_SrcType_Stator != CEMF_SOURCE) // not back-emf
				// for phase A
				{Region Input1; 		Branch {1,3};}
				{Region Rp1;			Branch {1,3};}
				{Region R1; 			Branch {3,31};}

				If (NbrRegions[Stator_Ind_Ap] == 1 && NbrRegions[Stator_Ind_Am] == 1)
					// There are positive and negative stator winding regions
					{Region Stator_Ind_Ap;	Branch {31,32};}
					{Region Stator_Ind_Am;	Branch {5,32};}
				ElseIf (NbrRegions[Stator_Ind_Am] == 1)
					// Only negative wound stator winding region
					{Region Stator_Ind_Am;	Branch {5,31};}
				ElseIf (NbrRegions[Stator_Ind_Ap] == 1)
					// Only positive stator winding region
					{Region Stator_Ind_Ap;	Branch {31,5};}
				Else
					Error[
						Sprintf[
							StrCat[
								"Stator winding domains (Stator_Ind_{A,B,C}{p,m}) need to ",
								"contain exactly one Physical object to use circuit! ",
								"Stator_Ind_Ap: %.0f, Stator_Ind_Am: %.0f"
							],
							NbrRegions[Stator_Ind_Ap],
							NbrRegions[Stator_Ind_Am]
						]
					];
				EndIf

				// for phase B
				{Region Input2; 		Branch {1,4};}
				{Region Rp2;			Branch {1,4};}
				{Region R2; 			Branch {4,41};}

				If (NbrRegions[Stator_Ind_Bp] == 1 && NbrRegions[Stator_Ind_Bm] == 1)
					// There are positive and negative stator winding regions
					{Region Stator_Ind_Bp;	Branch {41,42};}
					{Region Stator_Ind_Bm;	Branch {5,42};}

				ElseIf (NbrRegions[Stator_Ind_Bm] == 1)
					// Only negative wound stator winding region
					{Region Stator_Ind_Bm;	Branch {5,41};}
				ElseIf (NbrRegions[Stator_Ind_Bp] == 1)
					// Only positive stator winding region
					{Region Stator_Ind_Bp;	Branch {41,5};}
				Else
					Error[
						Sprintf[
							StrCat[
								"Stator winding domains (Stator_Ind_{A,B,C}{p,m}) need to ",
								"contain exactly one Physical object to use circuit! ",
								"Stator_Ind_Bp: %.0f, Stator_Ind_Bm: %.0f"
							],
							NbrRegions[Stator_Ind_Bp],
							NbrRegions[Stator_Ind_Bm]
						]
					];
				EndIf


				// for phase C
				{Region Input3; 		Branch {1,2};}
				{Region Rp3;			Branch {1,2};}
				{Region R3; 			Branch {2,21};}
				If (NbrRegions[Stator_Ind_Cp] == 1 && NbrRegions[Stator_Ind_Cm] == 1)
					// There are positive and negative stator winding regions
					{Region Stator_Ind_Cp;	Branch {21,22};}
					{Region Stator_Ind_Cm;	Branch {5,22};}
				ElseIf (NbrRegions[Stator_Ind_Cm] == 1)
					// Only negative wound stator winding region
					{Region Stator_Ind_Cm;	Branch {5,21};}
				ElseIf (NbrRegions[Stator_Ind_Cp] == 1)
					// Only positive stator winding region
					{Region Stator_Ind_Cp;	Branch {21,5};}
				Else
					Error[
						Sprintf[
							StrCat[
								"Stator winding domains (Stator_Ind_{A,B,C}{p,m}) need to ",
								"contain exactly one Physical object to use circuit! ",
								"Stator_Ind_Cp: %.0f, Stator_Ind_Cm: %.0f"
							],
							NbrRegions[Stator_Ind_Cp],
							NbrRegions[Stator_Ind_Cm]
						]
					];
				EndIf

			Else
				// If source type is back-emf, skip soure and phase resistances
				{Region Stator_Ind_Ap;	Branch {1,2};}
				{Region Stator_Ind_Am;	Branch {3,2};}
				{Region Rp1;	Branch {3,1}; }

				{Region Stator_Ind_Bp;	Branch {1,4};}
				{Region Stator_Ind_Bm;	Branch {5,4};}
				{Region Rp2;	Branch {5,1}; }

				{Region Stator_Ind_Cp;	Branch {1,6};}
				{Region Stator_Ind_Cm;	Branch {7,6};}
				{Region Rp3;	Branch {7,1}; }
			EndIf
		}
	// } // End Star connection
	ElseIf (CircuitConnection == DELTA_CONNECTION)
		// {
		// Name ElectricalCircuit;
		// Type Network;
		Case Circuit1 {
			If (Flag_SrcType_Stator != CEMF_SOURCE) // not back-emf
				{Region Input1; 		Branch {1,3};}
				{Region Rp1;			Branch {1,3};}
				{Region R1; 			Branch {3,7};}
				{Region Stator_Ind_Ap;	Branch {7,8};}
				{Region Stator_Ind_Am;	Branch {9,8};}
				{Region Input2; 		Branch {1,4};}
				{Region Rp2;			Branch {1,4};}
				{Region R2; 			Branch {4,5};}
				{Region Stator_Ind_Bp;	Branch {5,6};}
				{Region Stator_Ind_Bm;	Branch {7,6};}
				{Region Input3; 		Branch {1,2};}
				{Region Rp3;			Branch {1,2};}
				{Region R3; 			Branch {2,9};}
				{Region Stator_Ind_Cp;	Branch {9,10};}
				{Region Stator_Ind_Cm;	Branch {5,10};}
			Else // back EMF in circuit
				{Region Stator_Ind_Ap;	Branch {7,8};}
				{Region Stator_Ind_Am;	Branch {9,8};}
				{Region Rp1;	Branch {9,7}; }

				{Region Stator_Ind_Bp;	Branch {5,6};}
				{Region Stator_Ind_Bm;	Branch {7,6};}
				{Region Rp2;	Branch {7,5}; }

				{Region Stator_Ind_Cp;	Branch {9,10};}
				{Region Stator_Ind_Cm;	Branch {5,10};}
				{Region Rp3;	Branch {5,9}; }
			EndIf
		}
	// } // End Delta connection
	Else
		// Pass since there just is no stator circuit!
		If Flag_SrcType_Stator != CURRENT_SOURCE
			// Make sure source type does not include circuit (=Current source),
			// otherwise raise an error!
			Error[
				Sprintf[
					"Invalid circuit connection type: %d. Use %d for star or %d for delta.",
					CircuitConnection, STAR_CONNECTION, DELTA_CONNECTION
				]
			];
		EndIf
	EndIf
	If (Flag_Cir_RotorCage)
		Case Circuit4 {
			For k In {1:nbrRotorBars}
			{ Region Rotor_Bar~{k} ; Branch {NB1~{k}, NB2~{k}} ; }
			{ Region Rbar~{k} ;     Branch {NB2~{k}, NB3~{k}} ; }
			{ Region Ruers~{k} ;     Branch {NRu1~{k}, NRu2~{k}} ; }
			{ Region Rlers~{k} ;     Branch {NRl1~{k}, NRl2~{k}} ; }
			{ Region Luers~{k} ;      Branch {NLu1~{k}, NLu2~{k}} ; }
			{ Region Llers~{k} ;      Branch {NLl1~{k}, NLl2~{k}} ; }
			EndFor
		}
	EndIf
}
}
