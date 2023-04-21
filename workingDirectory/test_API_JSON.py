# %% Imports
from sys import path
from os.path import abspath, dirname, isdir, isfile, join, normpath, realpath

# Add Software_V2 to Path so pyemmo can be found
# This must be done since this is a script (not really a module) and we cannot guarante where it will run from
#   If it will be run as a module (from command line) __file__ will be the actual file path
#   But if its run cellwise, like in an interactive pyhton (IPython) shell, __file__ variable will not exist and we have to add the path manually
try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
#%%
from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script.script import Script
from pyemmo.script.geometry.primaryLine import PrimaryLine
from pyemmo.script.geometry.slaveLine import SlaveLine
from pyemmo.script.geometry.limitLine import LimitLine
from pyemmo.script.geometry.rotor import Rotor
from pyemmo.script.geometry.stator import Stator
from pyemmo.script.geometry.machineAllType import MachineAllType
from pyemmo.api.json import *
from pyemmo.functions.runOnelab import findGmsh, mergeAllGeoFiles
import subprocess
from matplotlib import pyplot as plt
import gmsh

#%%
# try to find gmsh in system path
gmshExe = findGmsh()
if not gmshExe:  # if gmsh was not found set manually
    gmshExe = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-210904\gmsh.exe"
    print(f"Did not find gmsh executable. Setting it manually to '{gmshExe}'")
else:
    print(f'gmsh exe is "{gmshExe}"')

workingDir = abspath(join(rootname, "Results", "Test_API_JSON"))
modelFileDir = join(workingDir, "model files")
geoJsonFile = join(workingDir, "test_API_geometry.json")
infoJsonFile = join(workingDir, "test_API_simuInfo.json")
#%% NEW API ALGO
# check if csv path is a directory
if isfile(geoJsonFile) and isfile(infoJsonFile):
    # import the segment machine geometry
    segmentSurfList = importMachineGeometry(geoJsonFile)
    # import the extended information
    extendedInfo = importExtInfo(infoJsonFile)
    # generate the machine geometry
    machine = createMachine(segmentSurfList, extendedInfo)
    # create dir for model files if it doesnt exist
    if not isdir(modelFileDir):
        mkdir(modelFileDir)
    # get the simulation pareameters
    simulationParameters = getSimuParams(extendedInfo=extendedInfo)
    # generate the script
    apiScript = Script(
        name="TestAPI_JSON",
        scriptPath=modelFileDir,
        simuParams=simulationParameters,
        machine=machine,
        resultsPath="",
        # factory="OpenCascade",
    )
    addPostOperations(apiScript, extendedInfo)
    apiScript.generateScript()
    #%%
    command = runOnelab.createCmdCommand(
        onelabFile=abspath(
            join(apiScript.getScriptPath(), apiScript.getName() + ".pro")
        ),
        gmshPath=findGmsh(),
        getdpPath="",
        useGUI=True,
    )
    subprocess.run(command)
    ###########################################################################################
    ################ Plot Results for Debugging ##################
    # resPath = apiScript.getResultsPath()
    # if isdir(resPath):
    #     # if the folder for results exists
    #     for file in listdir(resPath):
    #         filename, fileExt = splitext(file)
    #         if fileExt == ".dat":
    #             importResults.plotTimeTableDat(
    #                 abspath(join(resPath, file)),
    #                 filename,
    #                 title=filename,
    #                 savefig=True,F
    #                 showfig=False,
    #                 savePath=None,
    #             )
    ###########################################################################################
else:
    print()
    raise (
        FileNotFoundError(
            f"Given json file(s) did not exist! Check '{geoJsonFile}' or '{infoJsonFile}'."
        )
    )


# # %% OLD DEVELOPMENT VERSION
# # get maschine geo infos
# SurfaceAPIList = importMachineGeometry(join(workingDir, "test_API_geometry.json"))
# # fig, ax = plt.subplots()
# # ax.set_aspect("equal", adjustable="box")
# # for surf in MaschineSegmentSurfList:
# #     surf.plot(fig=fig)
# extendedInfoPath = join(workingDir, "test_API_extendedInfo.json")
# with open(extendedInfoPath, encoding="utf-8") as exInfoJson:
#     extendedInfo = json.load(exInfoJson)[0]

# symFactor = getSymFactor(extendedInfo)

# # %% GENERATE WHOLE MACHINE!
# # create boundarys
# r_RotorMB = getMovingbandRadius(extendedInfo)
# StatorPhysicals: List[PhysicalElement] = list()
# RotorPhysicals: List[PhysicalElement] = list()
# StatorPhysicals, RotorPhysicals = createBoundaries(
#     machineSurfList=segmentSurfList, symFactor=symFactor, rotorMBRadius=r_RotorMB
# )
# # fig, ax = plt.subplots()
# # ax.set_aspect("equal", adjustable="box")
# # for phys in StatorPhysicals+RotorPhysicals:
# #     geoList = phys.geometricalElement
# #     for geo in geoList:
# #         geo.plot(fig=fig)
# #%% create machine surfaces WITH CUTTING!
# segmentSurfDict = createSurfaceDict(surfList=segmentSurfList)
# # # get key dict to identify which and how surfs shoud be cut:
# # ParentKeyDict = identifySubtractSurfaces(segmentSurfDict)
# # SurfList = duplicateCutSurfs(
# #     segmentSurfDict, ParentKeyDict, symFactor
# # )  # first rotate and duplicate cut surfs

# # # fig, ax = plt.subplots()
# # # fig.set_dpi(300)
# # # ax.set_aspect("equal", adjustable="box")
# # # for surf in SurfList:
# # #     surf.plot(fig=fig)

# # NotDupSurfDict = removeCutSurfs(
# #     segmentSurfDict, ParentKeyDict
# # )  # then get new surface dict without allready duplicated surfs
# #%% create ALL machine surfaces
# MaschineSurfList = createMachineGeometryFromSegment(segmentSurfList, symFactor)

# #%% create physical surfaces from all the surfaces
# StatorSiemens = createMachine()
# nbrPolePair = getNbrPolePairs(extendedInfo)
# machineSiemens = MachineAllType(
#     rotor=RotorSiemens,
#     stator=StatorSiemens,
#     name=f"Machine from json interface ({modelName})",
#     nbrPolePairs=nbrPolePair,
#     symmetryFactor=symFactor,
# )
# #%% create dir for model files if it doesnt exist
# if not isdir(modelFileDir):
#     mkdir(modelFileDir)
# simulationParameters = getSimuParams(extendedInfo=extendedInfo)
# testScript = Script(
#     name=modelName,
#     scriptPath=modelFileDir,
#     simuParams=simulationParameters,
#     machine=machineSiemens,
#     resultsPath=args.res,
#     factory="OpenCascade",
# )
# testScript.generateScript()
# # run(
# #     [args.gmsh, abspath(join(modelFileDir, testScript.getName() + ".geo")), "-2"],
# #     shell=True,
# # )
# # run(
# #     args.getdp
# #     + " "
# #     + abspath(join(modelFileDir, testScript.getName() + ".pro"))
# #     + " -solve Analysis -v1",
# #     shell=True,
# # )
# command = runOnelab.createCmdCommand(
#     onelabFile=abspath(join(testScript.getScriptPath(), testScript.getName() + ".pro")),
#     gmshPath=args.gmsh,
#     getdpPath=args.getdp,
#     useGUI=getFlagOpenGui(extendedInfo),
# )
# subprocess.run(command)
# ###########################################################################################
# ################ Plot Results for Debugging ##################
# resPath = testScript.getResultsPath()
# if isdir(resPath):
#     # if the folder for results exists
#     for file in listdir(resPath):
#         filename, fileExt = splitext(file)
#         if fileExt == ".dat":
#             importResults.plotTimeTableDat(
#                 abspath(join(resPath, file)),
#                 filename,
#                 title=filename,
#                 savefig=True,
#                 showfig=False,
#                 savePath=None,
#             )
###########################################################################################

# #%% EVEN OLDER DEVELOPMENT VERSION
# dataFrameDict = getMachineDFDict(csvFilePath=Path2CSV)  # get maschine dataframe
# extendedInfo = getDataFrameFromCSV(join(Path2CSV, "duplicationInformation.csv"))
# symFaktor = getSymFactor(extendedInfo)
# ##%%
# ###############################################################################
# # # Set air gap color
# # for key in SurfaceDict.keys():
# #     if "Lu" in key:
# #         SurfaceDict[key].setMeshColor(pyd.LightSkyBlue1)
# #%% Test Segment export and cutting code
# SurfaceDict: Dict[str, Surface] = createSurfaceDict(dataFrameDict)

# # PLOT MACHINE IN PYTHON
# fig, ax = plt.subplots()
# fig.set_dpi(300)
# for key in SurfaceDict.keys():
#     SurfaceDict[key].plot(fig=fig, linewidth=0.5, color="b")
# fig.axes[0].set(xlim=(-0.01, 0.06), ylim=(-0.01, 0.06))
# # ax.autoscale()
# ax.set_aspect("equal", adjustable="box")

# # testScript = Script("TestSiemensOneSeg", RESULT_DIR)
# # for key in SurfaceDict.keys():
# #     SurfaceDict[key].addToScript(testScript)
# # testScript.generateScript()
# # subprocess.run([gmshExe, join(RESULT_DIR, testScript.getName()+".geo")], shell = True)

# #%% ######## Material #############
# MatDataframe = getDataFrameFromCSV(join(Path2CSV, "Materials.csv"))
# MatList = createMatList(MatDataframe)
# MatDict = createMatDict(MatList)
# # for mat in MatList:
# #     mat.print()

# #%% Find the shortest line
# # MaschineSurfList = createMachineSurfs(dataFrameDict, extendedInfo.symFactor[0])
# # shortLineLen = 1.0
# # for surf in MaschineSurfList:
# #     for line in surf.getCurve():
# #         lineLen = line.getPointDist()
# #         if lineLen < shortLineLen:
# #             shortestLine = line
# #             shortLineLen = shortestLine.getPointDist()
# #         elif lineLen == shortLineLen:
# #             print(line.getName(), " and ", shortestLine.getName(), "are equal in length: ", lineLen, shortLineLen)
# # print(shortestLine.getName(),": ",shortestLine.getPointDist())

# #%% ####### Physical Line #######
# r_RotorMB = getMovingbandRadius(extendedInfo)

# RotorPhys = list()
# StatorPhys = list()

# MaschineSurfaceDict = createSurfaceDict(dataFrameDict)

# if symFaktor > 1:
#     [MasterLinesStator, MasterlinesRotor] = getMasterLines(
#         MaschineSurfaceDict, r_RotorMB, symFaktor
#     )
#     [SlaveLinesStator, SlavelinesRotor] = createSlaveLines(
#         MasterLinesStator, MasterlinesRotor, symFaktor
#     )

#     RotorPhys.append(MasterLine("masterLineR", MasterlinesRotor))
#     StatorPhys.append(MasterLine("masterLineS", MasterLinesStator))
#     RotorPhys.append(SlaveLine("slaveLineR", SlavelinesRotor))
#     StatorPhys.append(SlaveLine("slaveLineS", SlaveLinesStator))
#     # # TESTING
#     # scriptName = "TestMasterSlaveLines"
#     # TestMasterSlaveScript = Script(scriptName, RESULT_DIR)
#     # for line in RotorPhys + StatorPhys:
#     #     line.addToScript(TestMasterSlaveScript)
#     # TestMasterSlaveScript.generateScript()  # generate test script with aux lines
#     # subprocess.run(
#     #     [gmshExe, join(rootname, r"resultDirectory\\" + scriptName + ".geo"),],
#     #     shell=True,
#     # )
# #%% Create the moving band lines and object
# MB_Stator, MB_Rotor_inner, MB_Rotor_Aux = createMB(
#     dataFrameDict, MaschineSurfaceDict, symFaktor
# )
# # # TESTING
# # scriptName = "TestMBLines"
# # TestMBScript = Script(scriptName, RESULT_DIR)
# # if MB_Rotor_Aux is not None:
# #     for MBAux in MB_Rotor_Aux:
# #         MBAux.addToScript(TestMBScript)
# # MB_Rotor_inner.addToScript(TestMBScript)
# # MB_Stator.addToScript(TestMBScript)
# # TestMBScript.generateScript()  # generate test script with aux lines
# # subprocess.run(
# #     [gmshExe, join(rootname, r"resultDirectory\\" + scriptName + ".geo"),], shell=True,
# # )

# #%% Outer limit line for A=0
# OuterLimitLineDict = {
#     "Geh": [  # first case: no inner shaft radius; second case: with radius
#         ["G1", "G3"],  # first case: zylindrical housing
#         [
#             ["G1", "G2a"],  # second case: quadratic or "kreuzprofil" with rounding
#             ["G2a", "G2e"],
#             ["G2e", "G3"],
#             ["G2", "G1"],  # without rounding
#             ["G2", "G3"],
#         ],
#     ],
#     "StNut": ["SZ", "SN"],  # if there is no housing, use stator iron outer line
# }
# limitLineList = getLimitLines(
#     OuterLimitLineDict, dataFrameDict, MaschineSurfaceDict, symFaktor
# )
# OuterLimit = LimitLine("outerLimit", limitLineList)
# StatorPhys.append(OuterLimit)

# # # TESTING
# # scriptName = "TestOuterLimitLines"
# # TestLimLineScript = Script(scriptName, RESULT_DIR)
# # for line in limitLineList:
# #     line.addToScript(TestLimLineScript)
# # OuterLimit.addToScript(TestLimLineScript)
# # TestLimLineScript.generateScript()  # generate test script with aux lines
# # subprocess.run(
# #     [gmshExe, join(rootname, r"resultDirectory\\" + scriptName + ".geo"),], shell=True,
# # )

# #%% Inner limit line for A=0
# # Vorgehen, wenn Welle -> Dann Welle
# # Wenn nicht Welle, aber Hülse -> Dann Hülse
# # Sonst -> Rotorblech
# InnerLimitLineDict = {
#     "Wel": [
#         ["W2", "MP"],
#         ["W4", "W3"],
#     ],  # first case: no inner shaft radius; second case: with radius
#     "Hul": ["H3", "H4"],
#     "Pol": [["RMi", "RI"], ["RndI", "RndM"]],  # first case:IPM; second case:APM
#     "RoNut": ["SZ", "SN"],
# }
# InnerLimitLines = getLimitLines(
#     InnerLimitLineDict, dataFrameDict, MaschineSurfaceDict, symFaktor
# )
# InnerLimit = LimitLine("innerLimit", InnerLimitLines)
# # print(len(InnerLimitLines))

# # # TESTING
# # scriptName = "TestInnerLimitLines"
# # TestLimLineScript = Script(scriptName, RESULT_DIR)
# # for line in InnerLimitLines:
# #     line.addToScript(TestLimLineScript)
# # InnerLimit.addToScript(TestLimLineScript)
# # TestLimLineScript.generateScript()  # generate test script with aux lines
# # subprocess.run(
# #     [gmshExe, join(rootname, r"resultDirectory\\" + scriptName + ".geo"),], shell=True,
# # )
# #%% PRINT ALL BOUNDARYS IN ONE SESSION
# # from pyemmo.functions.runOnelab import mergeAllGeoFiles
# # mergeAllGeoFiles(RESULT_DIR, gmshExe)

# #%% Test createBoundary function:
# StatorPhysicals, RotorPhysicals = createBoundarys(
#     dataFrameDict=dataFrameDict,
#     MaschineSurfaceDict=MaschineSurfaceDict,
#     SymFactor=symFaktor,
#     RotorMBRadius=r_RotorMB,
#     MatDict=MatDict,
# )

# # # TESTING
# # scriptName = "TestBoundaryFunction"
# # TestBoundaryScript = Script(scriptName, RESULT_DIR)
# # for PhysicalElem in StatorPhysicals + RotorPhysicals:
# #     if type(PhysicalElem) is list:
# #         for Element in PhysicalElem:
# #             Element.addToScript(TestBoundaryScript)
# #     else:
# #         PhysicalElem.addToScript(TestBoundaryScript)
# # TestBoundaryScript.generateScript()  # generate test script with aux lines
# # subprocess.run(
# #     [gmshExe, join(rootname, r"resultDirectory\\" + scriptName + ".geo"),], shell=True,
# # )
# #%% Physical Surfaces for Onelab Domains
# MaschineSurfList = createMachineSurfs(dataFrameDict, symFaktor)
# # IDs:
# #   LuR/RoLu    Airgap Rotor;
# #   Mag         Magnet;
# #   StCu1/2     Stator-Slot side;
# #   RoCu        Rotor-Slot;
# #   StLu        Airgap Stator
# fig, ax = plt.subplots()
# fig.set_dpi(300)
# for surf in MaschineSurfList:
#     surf.plot(fig=fig, linewidth=0.5, color="b")
# #%% GENERATE WHOLE MACHINE!
# # create clean machine material dict (=dict for connection between machineSurfaceID and SurfaceMaterial)
# MachineMatDict = dict()
# for key in dataFrameDict.keys():
#     name = cleanName(dataFrameDict[key].Material[0])
#     if not isAir(name):
#         MachineMatDict[key] = name
#     else:
#         MachineMatDict[key] = "Air"

# # create boundarys
# StatorPhysicals.clear()
# RotorPhysicals.clear()

# # [MB_Stator, MB_Rotor_i, MB_Rotor_a] = createMB(
# #     dataFrameDict, MaschineSurfaceDict, symFaktor
# # )
# # StatorPhysicals.append(MB_Stator)
# # RotorPhysicals.append(MB_Rotor_i)
# # for mb_aux in MB_Rotor_a:
# #     RotorPhysicals.append(mb_aux)

# StatorPhysicals, RotorPhysicals = createBoundarys(
#     dataFrameDict=dataFrameDict,
#     MaschineSurfaceDict=MaschineSurfaceDict,
#     SymFactor=symFaktor,
#     RotorMBRadius=r_RotorMB,
#     MatDict=MatDict,
# )

# # # get number of identical points
# # pointdupCounter = 0
# # nbrPointsTotal = 0
# # surfListB = MaschineSurfList.copy()
# # for surfa in MaschineSurfList:
# #     #!!! getPoints only returns the start and end points, NOT center points etc.!!!
# #     points_a = surfa.getPoints()
# #     nbrPointsTotal += len(points_a)
# #     surfListB.pop(surfListB.index(surfa))
# #     for surfb in surfListB:
# #         points_b = surfb.getPoints()
# #         for point_a in points_a:
# #             for point_b in points_b:
# #                 if point_b.isEqual(point_a):
# #                     pointdupCounter +=1

# # # try to replace duplicated lines
# # for surf in MaschineSurfList:
# #     for compSurf in MaschineSurfList:
# #         if surf != compSurf:
# #             replaceIdenticalLines(compSurf, surf)


# # create physical surfaces
# for surf in MaschineSurfList:
#     surfName = surf.getName()
#     if (
#         "GehIn_0" in surfName and symFaktor == 1
#     ):  # if the inner surface is air, overlapping the rotor:
#         surf.delete()  # set the delete-flag to not create the surface
#     else:
#         physicalSurf, machineSide = createPhysicalSurface(
#             surf=surf,
#             MatDict=MatDict,
#             MachineMatDict=MachineMatDict,
#             RotorMBRadius=r_RotorMB,
#             extendedInfo=extendedInfo,
#         )
#         if machineSide == "Stator":
#             StatorPhysicals.append(physicalSurf)
#         elif machineSide == "Rotor":
#             RotorPhysicals.append(physicalSurf)
#         else:
#             ValueError(
#                 f"MachineSide was whether rotor or stator: {machineSide}", machineSide
#             )
# # # Test
# # testScript = pyd.Script("TestDuplication", RESULT_DIR, "OpenCASCADE")
# # for element in StatorPhysicals+RotorPhysicals:
# #     element.addToScript(testScript)
# # testScript.generateScript()
# # subprocess.run([gmshExe, join(RESULT_DIR, testScript.getName() + ".geo")], shell=True)

# #%%
# RotorSiemens = Rotor(
#     name="RotorSiemens",
#     # physicalElement=[phyLMaster_Rotor, phyLSlave_Rotor, phyInner, Blech_Rotor, Bohrung, LuftRotor] + phyMBRotor + Magnete
#     physicalElementList=RotorPhysicals,
# )
# StatorSiemens = Stator(
#     name="StatorSiemens",
#     physicalElement=StatorPhysicals,
# )
# nbrSlotTotal = dataFrameDict["StNut"].Quantity[0]
# symFaktor = getSymFactor(extendedInfo)
# nbrPolePair = getNbrPolePairs(extendedInfo)
# speed = getRotFreq(extendedInfo)
# startAngle = -2 * pi / nbrPolePair / 4
# machineSiemens = MachineAllType(
#     simuParam={
#         "analysisParameter": {
#             "freq": speed,  # Drehfrequenz
#             "symmetryFactor": symFaktor,
#             "nbrPolesTotal": int(nbrPolePair * 2),
#             "nbrSlotTotal": int(nbrSlotTotal),
#             # Winkel/wr 2*math.pi / (2 * math.pi * freq) = 1/freq für ganzen mech. Winkel:
#             "timeMax": 1 / speed / symFaktor,
#             # Ein Grad pro Step -> math.pi/180/(2*math.pi*freq) = 1/(180*2*freq):
#             "timeStep": 1 / (180 * 2 * speed),
#             "analysisType": "timedomain",  #'timedomain', #'static'
#             "startPosition": startAngle,
#         },
#         "output": {"b": True, "az": True, "js": True},
#     },
#     rotor=RotorSiemens,
#     stator=StatorSiemens,
# )

# # Test
# testScript = Script("TestFinalMachine", RESULT_DIR)
# machineSiemens.addToScript(testScript)
# idedentPoints, idedentLines = testScript.generateScript()
# #%% debugging identical points

# # for point in idedentPoints:
# #     point.plot(fig=fig, color="r", markersize=0.5, marker=".")
# # ax.set_aspect("equal", adjustable="box")
# # fig.axes[0].set(xlim=(-0.06, 0.06), ylim=(-0.06, 0.06))
# # ax.autoscale()
# # ax.set_aspect("equal", adjustable="box")
# # plt.show()
# #%%
# # # If you just want to show the geo file you can use:
# # gmsh.initialize()
# # gmsh.open(abspath(join(RESULT_DIR, testScript.getName() + ".geo")))
# # gmsh.fltk.run()
# # # if you want to run the simulation without user interaction (GUI), you can do:
# # # gmsh.onelab.run()
# # #...
# # gmsh.finalize()
# # If you want to show the geo and merged pro file you have to start a subprocess and run somthing like "gmsh PATH/TO/profile.pro", because gmsh.merge(...) seems only to work well with geo files:

# subprocess.run(
#     [gmshExe, abspath(join(RESULT_DIR, testScript.getName() + ".pro"))], shell=True
# )
# # %%
