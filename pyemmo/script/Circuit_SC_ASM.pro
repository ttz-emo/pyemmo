// Circuit for induction motor

Group{
  // Dummy numbers for circuit definition

  For k In {1:nbRotorBars}
    Rers~{k} = Region[{(60000+k)}]; // resistance per endring segment
    All_EndRingResistancesRotor += Region[ Rers~{k} ] ;
    Lers~{k} = Region[{(70000+k)}]; // inductance per end ring segment
    All_EndRingInductancesRotor += Region[ Lers~{k} ] ;
  EndFor

  Resistance_Cir  = Region[{ }];
  Inductance_Cir  = Region[{ }];

  Resistance_Cir  += Region[{ All_EndRingResistancesRotor }];
  Inductance_Cir  += Region[{ All_EndRingInductancesRotor }];

  DomainZ_Cir = Region[ {Resistance_Cir, Inductance_Cir} ];
  DomainSource_Cir = Region[ { } ] ;
  DomainZt_Cir    = Region[ {DomainZ_Cir, DomainSource_Cir} ];
}

// --------------------------------------------------------------------------
// --------------------------------------------------------------------------

Function {
  For k In {1:nbRotorBars} //existing numbers of rotor Bars in the model
	NB1~{k} =  400+k; // first node number for each rotor bar
	NB2~{k} =  500+k; // second node number for each rotor bar
  EndFor

  // If only one pole is simulated in the model, the end rings of the A and B
  // sides must be crossed. If one or more pole pairs are simulated, they do not.
  If (NbrPolesInModel == 1)
    For k In {1:nbRotorBars}
      NR1~{k} = NB1~{k}; // first node number for each endring resistance
      k2 = (k<nbRotorBars) ? k+1 : 1.;
      // second node number for each endring resistance:
      NR2~{k} = (k<nbRotorBars) ? NB1~{k2} : NB2~{1} ;
      NL1~{k} = NB2~{k}; // first node number for each endring inductance
      // second node number for each endring inductance:
      NL2~{k} = (k<nbRotorBars) ? NB2~{k2} : NB1~{1} ;
    EndFor

  ElseIf (NbrPolesInModel>1 && (NbrPolesInModel%2 == 0))
    For k In {1:nbRotorBars}
      NR1~{k} = NB1~{k}; // first node number for each endring resistance
      k2 = (k<nbRotorBars) ? k+1 : 1.;
      // second node number for each endring resistance:
      NR2~{k} = (k<nbRotorBars) ? NB1~{k2} : NB1~{1} ;
      NL1~{k} = NB2~{k}; // first node number for each endring inductance
      // second node number for each endring inductance:
      NL2~{k} = (k<nbRotorBars) ? NB2~{k2} : NB2~{1} ;
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
}


// --------------------------------------------------------------------------

Constraint {
  //If(SymmetryFactor==4 && Flag_Cir_RotorCage) // Only one physical region in
  //geo allow per branch
    { Name ElectricalCircuit ; Type Network ;
      Case Circuit4 {
        For k In {1:nbRotorBars}
          { Region Rotor_Bar~{k} ; Branch {NB1~{k}, NB2~{k}} ; }
          { Region Rers~{k} ;      Branch {NR1~{k}, NR2~{k}} ; }
          { Region Lers~{k} ;      Branch {NL1~{k}, NL2~{k}} ; }
        EndFor
      }
    }
 // EndIf

}
