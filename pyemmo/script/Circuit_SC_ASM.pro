// Circuit for induction motor

Group{
  // Dummy numbers for circuit definition

  For k In {1:nbrRotorBars}
    Ruers~{k} = Region[{(60000+k)}]; // resistance per endring segment
    Rlers~{k} = Region[{(70000+k)}]; // resistance per endring segment
    All_EndRingResistancesRotor += Region[ Ruers~{k} ] ;
    All_EndRingResistancesRotor += Region[ Rlers~{k} ] ;
    Luers~{k} = Region[{(80000+k)}]; // inductance per end ring segment
    Llers~{k} = Region[{(90000+k)}]; // inductance per end ring segment
    All_EndRingInductancesRotor += Region[ Luers~{k} ] ;
    All_EndRingInductancesRotor += Region[ Llers~{k} ] ;
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
  For k In {1:nbrRotorBars} //existing numbers of rotor Bars in the model
	NB1~{k} =  400+k; // first node number for each rotor bar
	NB2~{k} =  500+k; // second node number for extra rotor bar resistance
  // Each rotor bar has Node NB1 -> NB2 for the coupling with the bar voltage
	NIM1~{k} = 700+k; // upper intermediate node number for each rotor bar connection
	NIM2~{k} = 800+k; // lower intermediate node number for each rotor bar connection
  EndFor

  // If only one pole is simulated in the model, the end rings of the A and B
  // sides must be crossed. If one or more pole pairs are simulated, they do not.
  If (NbrPolesInModel == 1)
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
      NLu2~{k} = (k<nbrRotorBars) ? NB1~{k2} : NB2~{1} ;

      // Lower Branch
      NRl1~{k} = NB2~{k}; // first node number for lower endring resistance
      // second node number for lower endring resistance:
      NRl2~{k} = NIM2~{k}; // = lower intermediate node

      NLl1~{k} = NRl2~{k}; // first node number for lower endring inductance (= output of lower resistance)
      // second node number for lower endring inductance:
      NLl2~{k} = (k<nbrRotorBars) ? NB2~{k2} : NB1~{1} ;
    EndFor

    ElseIf (NbrPolesInModel>1 && !(NbrPolesInModel%2))
      For k In {1:nbrRotorBars}
        // NR1~{k} = NB1~{k}; // first node number for each endring resistance
        // k2 = (k<nbrRotorBars) ? k+1 : 1.;
        // // second node number for each endring resistance:
        // NR2~{k} = (k<nbrRotorBars) ? NB1~{k2} : NB1~{1} ;
        // NL1~{k} = NB2~{k}; // first node number for each endring inductance
        // // second node number for each endring inductance:
        // NL2~{k} = (k<nbrRotorBars) ? NB2~{k2} : NB2~{1} ;

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
        NRl1~{k} = NB2~{k}; // first node number for lower endring resistance
        // second node number for lower endring resistance:
        NRl2~{k} = NIM2~{k}; // = lower intermediate node

        NLl1~{k} = NRl2~{k}; // first node number for lower endring inductance (=
        // output of lower resistance)
        // second node number for lower endring inductance:
        NLl2~{k} = (k<nbrRotorBars) ? NB2~{k2} : NB2~{1} ;
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


// --------------------------------------------------------------------------

Constraint {
  //If(SymmetryFactor==4 && Flag_Cir_RotorCage) // Only one physical region in
  //geo allow per branch
  { Name ElectricalCircuit ; Type Network ;
    Case Circuit4 {
      For k In {1:nbrRotorBars}
        { Region Rotor_Bar~{k} ;  Branch {NB1~{k},  NB2~{k}} ; }  // Bar voltage drop
          { Region Ruers~{k} ;      Branch {NRu1~{k}, NRu2~{k}} ; }
          { Region Rlers~{k} ;      Branch {NRl1~{k}, NRl2~{k}} ; }
          { Region Luers~{k} ;      Branch {NLu1~{k}, NLu2~{k}} ; }
          { Region Llers~{k} ;      Branch {NLl1~{k}, NLl2~{k}} ; }
        EndFor
      }
    }
 // EndIf

}
