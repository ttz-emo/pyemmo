from .domain import Domain
from .machineAllType import MachineAllType
from .rotorSPMSM import RotorSPMSM
from .statorSPMSM import StatorPMSM, datamodel
import math


###
# Eine Instanz der Klasse MachineSPMSM beschreibt eine Synchronmaschine mit Oberflächenmagneten im dreidimensionalen Raum.
# Dieser Maschinentype ist ein Bestandteil des Baukastens, welches vom Nutzer für die Simulation instanziiert werden kann.
# Durch die Vorauswahl des Maschinentypes, werden Eigenschaften aus dem Input-Dictionary den Bauteilen automatisch zugewiesen.
###
class MachineSPMSM(MachineAllType):
    """
    SPMSM machine class

        TODO: example
    """

    def __init__(self, simuParam):
        """create a SPMSM machine object

        Args:
            simuParam (dict): classical machine simulation parameter dict.

        DEFAULT simulation parameter dict:

        .. code:: python

            {
                "analysisParameter": {
                    "freq": 1000 / 60, # mech. frequency
                    "symmetryFactor": 4,
                    "nbrPolesTotal": 10,
                    "nbrSlotTotal": 12,
                    "timeMax": 1 / (1000/60), # stop time simulation
                    "timeStep": 1/ (180 * (1000/60) * 2),  # step time
                    "analysisType": "timedomain",  # options: 'timedomain' or 'static'
                    "startPosition": 0, # init rotation
                },
            }


        """
        # ###Name des Objektes.
        # self._name = "machine"
        ###Simulationsparameter gemäß der Eingabe.
        self._simuParam = simuParam
        # ###Symmetriefaktor z. B. 4 für ein Viertelmodell der Maschine.
        # self._symmetryFactor = self._simuParam["analysisParameter"]["symmetryFactor"]
        # ###Rotorobjekt der Klasse RotorSPMSM.
        # self._rotor = None
        # ###Statorobjekt der Klasse StatorSPMSM.
        # self._stator = None
        # Calculate Poles and Slots for Model
        super().__init__(
            name="machineSPMSM",
            nbrPolePairs=simuParam["analysisParameter"]["nbrPolesTotal"] / 2,
            symmetryFactor=simuParam["analysisParameter"]["symmetryFactor"],
            rotor=None,
            stator=None,
        )
        self._simuParam["analysisParameter"]["nbrPolesinModel"] = (
            self._simuParam["analysisParameter"]["nbrPolesTotal"] / self._symmetryFactor
        )
        self._simuParam["analysisParameter"]["nbrSlotinModel"] = (
            self._simuParam["analysisParameter"]["nbrSlotTotal"] / self._symmetryFactor
        )
        # self._nbrPolePairs = self._simuParam["analysisParameter"]["nbrPolesTotal"] / 2

    ###
    # Mit addRotorToMachine() wird ein Rotorobjekt der Klasse RotorSPMSM erzeugt und der Maschine zugewiesen.
    #
    #   Input:
    #
    #       laminationType : String
    #       magnetType : String
    #
    #   Output:
    #
    #       RotorSPMSM
    #
    #   Beispiel:
    #
    #       pmsm1 = pyd.MachineSPMSM(simuSPMSMDict)
    #       rotor1 = pmsm1.addRotorToMachine('sheet01_standard', 'magnet01_surface')
    #       rotor1.addLaminationParameter({'r_We' : 20e-3,
    #           'r_R' : 55e-3,
    #           'meshLength' : 3e-3,
    #           'material' : steel_1010,
    #           'machineCentrePoint' : PBohrung})
    #       rotor1.addMagnetParameter({'h_M' : 7e-3,
    #           'angularWidth_i' : math.pi/10,
    #           'angularWidth_a' : math.pi/12,
    #           'magnetisationDirection' : [1, -1, 1, -1, 1, -1, 1, -1],
    #           'magnetisationType' : 'radial',
    #           'material' : ndFe35,
    #           'meshLength' : 3e-3})
    #       rotor1.addAirGapParameter({'width' : 3e-3,
    #           'material' : air})
    #       rotor1.createRotor()
    #
    ###
    def addRotorToMachine(self, laminationType, magnetType):
        startPosition = (
            math.pi
            / self._symmetryFactor
            / self._simuParam["analysisParameter"]["nbrPolesinModel"]
            + self._simuParam["analysisParameter"]["startPosition"]
        )
        angleGeoParts = (
            math.pi
            / self._symmetryFactor
            / self._simuParam["analysisParameter"]["nbrPolesinModel"]
        )
        nbrGeoParts = self._simuParam["analysisParameter"]["nbrPolesinModel"] * 2
        rotorSPMSM1 = RotorSPMSM(
            laminationType,
            magnetType,
            angleGeoParts,
            nbrGeoParts,
            self._symmetryFactor,
            startPosition,
        )
        self._rotor = rotorSPMSM1
        return self._rotor

    ###
    # Mit addStatorToMachine() wird ein Statorobjekt der Klasse StatorSPMSM erzeugt und der Maschine zugewiesen.
    #
    #   Input:
    #
    #       laminationType : String
    #       slotType : String
    #
    #   Output:
    #
    #       StatorSPMSM
    #
    #   Beispiel:
    #
    #       pmsm1 = pyd.MachineSPMSM(simuSPMSMDict)
    #       stator1 = pmsm1.addStatorToMachine('sheet01_standard', 'slotForm_01')
    #       stator1.addLaminationParameter({'r_S_i' : 65e-3,
    #           'r_S_a' : 100e-3,
    #           'meshLength' : 3e-3,
    #           'material' : steel_1010,
    #           'machineCentrePoint' : PBohrung})
    #       stator1.addSlotParameter({'w_SlotOP' : 2e-3,
    #           'h_SlotOP' : 4e-3,
    #           'w_Wedge' : 9e-3,
    #           'h_Wedge' : 7e-3,
    #           'h_Slot' : 23e-3,
    #           'w_Slot' : 8e-3,
    #           'material' : copper,
    #           'meshLength' : 3e-3,
    #           'slot_OPAir' : False})
    #       stator1.addAirGapParameter({'width' : 3e-3, 'material' : air})
    #       stator1.createStator()
    #
    ###
    def addStatorToMachine(
        self, laminationType: str, slotType: str, winding: datamodel
    ):
        startPosition = (
            math.pi
            / self._symmetryFactor
            / self._simuParam["analysisParameter"]["nbrSlotinModel"]
            + self._simuParam["analysisParameter"]["startPosition"]
        )
        angleGeoParts = (
            math.pi
            / self._symmetryFactor
            / self._simuParam["analysisParameter"]["nbrSlotinModel"]
        )
        nbrGeoParts = self._simuParam["analysisParameter"]["nbrSlotinModel"] * 2
        nbrSlotsTotal = (
            nbrGeoParts * self._symmetryFactor / 2
        )  # divided by 2 because one slot is formed by 2 geoParts
        statorSPMSM1 = StatorPMSM(
            laminationType=laminationType,
            slotType=slotType,
            nbrSlots=nbrSlotsTotal,
            angleGeoParts=angleGeoParts,
            nbrGeoParts=nbrGeoParts,
            symmetryFactor=self._symmetryFactor,
            winding=winding,
            startPosition=startPosition,
        )
        self._stator = statorSPMSM1
        return self._stator

    ###createMachine() erzeugt alle nötigen Domaine automatisch und befüllt sie mit PhysicalElement-Objekten gemäß ihren Eigenschaften.
    ##
    ##  -> createMachineDomains() from MachineAllType
    # ä
    # def createMachine(self):
    #     rotor = self._rotor
    #     stator = self._stator
    #     if rotor and stator:
    #         rotor._createDomainForRotor()
    #         stator._createDomainForStator()
    #         ###DomainS beinhaltet alle Physical Elements, die bestromt werden.
    #         self._domainS = Domain(
    #             "DomainS",
    #             rotor._domainS.physicals
    #             + stator._domainS.physicals,
    #         )
    #         ###DomainM beinhaltet alle Physical Elements, die magnetisiert sind.
    #         self._domainM = Domain(
    #             "DomainM", rotor._domainM.physicals
    #         )
    #         ###DomainC beinhaltet alle Physical Elements, die leitend sind.
    #         self._domainC = Domain(
    #             "DomainC",
    #             rotor._domainC.physicals
    #             + stator._domainC.physicals,
    #         )
    #         ###mbRotor beinhaltet alle Physical Elements, die eine Moving Band auf der Rotorseite beschreiben.
    #         self._mbRotor = Domain("MB_Rotor", rotor._mb.physicals)
    #         ###mbStator beinhaltet alle Physical Elements, die eine Moving Band auf der Statorseite beschreiben.
    #         self._mbStator = Domain("MB_Stator", stator._mb.physicals)
    #         ###domain beinhaltet alle Physical Elements, die die elektrische Maschine beschreiben.
    #         self._domain = Domain(
    #             "Domain",
    #             rotor._domain.physicals
    #             + stator._domain.physicals,
    #         )
    #         ###domainL beinhaltet alle Physical Elements, die ein lineares Material besitzen.
    #         self._domainL = Domain(
    #             "DomainL",
    #             rotor._domainL.physicals
    #             + stator._domainL.physicals,
    #         )
    #         ###domainNL beinhaltet alle Physical Elements, die ein nicht lineares Material besitzen.
    #         self._domainNL = Domain(
    #             "DomainNL",
    #             rotor._domainNL.physicals
    #             + stator._domainNL.physicals,
    #         )

    #         ###rotorMoving beinhaltet alle Physical Elements, die während der Simulation rotiert werden müssen (Rotor).
    #         rotorMoving = Domain(
    #             "Rotor_Moving", rotor._rotorMoving.physicals
    #         )
    #         ###mbBaux beinhaltet alle Hilfslinien des MovingBands (Ergänzung zum Vollkreis), die wegen der Symmetrie ergänzt werden mussten. MovingBand auf der Rotorseite muss ein vollständiger Kreis beschreiben.
    #         self._mbBaux = Domain(
    #             "Rotor_Bnd_MBaux", rotor._mbBaux.physicals
    #         )
    #         ###DomainAirGapRotor beinhaltet alle Physical Elements, die einen Luftspalt auf der Rotorseite (Luftspalt bis zum Moving Band) beschreiben.
    #         self._domainAirGapRotor = Domain(
    #             "Rotor_Airgap", rotor._domainAirGap.physicals
    #         )
    #         ###DomainAirGapStator beinhaltet alle Physical Elements, die einen Luftspalt auf der Statorseite (Luftspalt ab dem Moving Band bis Statorinnenseite) beschreiben.
    #         self._domainAirGapStator = Domain(
    #             "Stator_Airgap", stator._domainAirGap.physicals
    #         )

    #         if (
    #             len(
    #                 rotor._domainprimary.physicals
    #                 + stator._domainprimary.physicals
    #             )
    #             > 0
    #         ):
    #             ###primarykante der elektrischen Maschine.
    #             self._domainprimary = Domain(
    #                 "primaryRegion_Rotor",
    #                 rotor._domainprimary.physicals
    #                 + stator._domainprimary.physicals,
    #             )
    #             ###Slavekante der elektrischen Maschine.
    #             self._domainSlave = Domain(
    #                 "SlaveRegion_Rotor",
    #                 rotor._domainSlave.physicals
    #                 + stator._domainSlave.physicals,
    #             )
    #         else:
    #             self._domainprimary = None
    #             self._domainSlave = None
    #         ###Innengrenze an der Welle.
    #         self._domainInnerLimit = Domain(
    #             "InnerLimitLine", rotor._domainInnerLimit.physicals
    #         )
    #         ###Maschinenaußengrenze.
    #         self._domainOuterLimit = Domain(
    #             "OuterLimitLine", stator._domainOuterLimit.physicals
    #         )
    #     else:
    #         print("No definition of stator or rotor!")

    ###Mit setName() kann der Name der Instanz geändert werden.
    def setName(self, name):
        self._name = name

    ###getName() gibt den Namen der Instanz als String zurück.
    def getName(self):
        return self._name

    ###
    # Mit addToScript wird die Maschine zum Skriptobjekt übergeben und in gmsh-Syntax übersetzt.
    # Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode von Script) verwendet werden.
    #
    #   Input:
    #
    #       script : Script
    #
    #   Output:
    #
    #       None
    #
    #   Beispiel:
    #
    #       Machine1 = MachineSPMSM(...)
    #       ...
    #       myScript = Script(...)
    #       Maschine1.addToScript(myScript)
    #
    ###
    def addToScript(self, script):
        # self._rotor.addToScript(script)
        # self._stator.addToScript(script)
        self.createMachineDomains()
        self._domainS.addToScript(script)
        self._domainM.addToScript(script)
        self._mbRotor.addToScript(script)
        self._mbStator.addToScript(script)
        self._domain.addToScript(script)
        self._domainL.addToScript(script)
        self._domainNL.addToScript(script)

        self._rotorMoving.addToScript(script)
        self._mbBaux.addToScript(script)
        self._domainAirGapRotor.addToScript(script)
        self._domainAirGapStator.addToScript(script)

        if self._domainPrimary != None:
            self._domainPrimary.addToScript(script)
            self._domainSlave.addToScript(script)

        self._domainInnerLimit.addToScript(script)
        self._domainOuterLimit.addToScript(script)
        # script._createMovingBand(
        #     self._mbStator,
        #     self._mbRotor,
        #     self._domain,
        #     self._mbRotor.physicals[0].getMaterial(),
        #     self._symmetryFactor,
        # )
        # script._printFormulationGetDP(self)
