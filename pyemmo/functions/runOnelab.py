import sys
from os import listdir, walk
from os.path import abspath, expanduser, isdir, isfile, join, normpath, splitext
from typing import Dict, Union, List
import logging
from shutil import which
import subprocess
from argparse import ArgumentParser


def findGmsh(verbosity: bool = True) -> str:
    """Find gmsh executable on maschine"""
    gmshExe = findExe("gmsh", verbosity=verbosity)
    return gmshExe


def findGetDP(verbosity: bool = True) -> str:
    """Find getdp executable on maschine"""
    getdpExe = findExe("getdp", verbosity=verbosity)
    return getdpExe


def findExe(exeName: str, verbosity: bool = True) -> str:
    """Search the local machine for the executalble given in exeName.
    There are several searching stages and the function returns the exe path if one stage gives a result:
        1. search with "which" command
        2. search the python path
        3. search the "User/appdate/local/programs" path

    TODO:
        Search "C:/Program Files" path

    Args:
        exeName (str): name of the executable. E.g. "myExe.exe" or just "myExe"
        verbosity (bool): Print additional information to the command line if True. Defaults to True.

    Raises:
        SystemError: If not run on Windows
        FileNotFoundError: If the exe is not found.

    Returns:
        str: filepath to the executable
    """
    executableName, _ = splitext(exeName)
    # first opion: try to find gmsh with "which"
    exePath = which(executableName)
    if not exePath:
        if verbosity:
            logging.debug(
                "Could not find %s from command line. Trying to find it in python-path...",
                executableName,
            )
        # second option: try to find gmsh in python path. (Should work since gmsh module is installed!)
        for path in sys.path:
            if isdir(path):
                for fileList in listdir(path):
                    if fileList == f"{executableName}.exe":
                        exePath = join(path, fileList)
                        if verbosity:
                            logging.debug("Found %s in '%s'!", executableName, exePath)
                        return exePath
        if not exePath:
            if verbosity:
                logging.debug(
                    "%s was not found in 'path' Variable. Trying to find it in user home directory. This can take some time!",
                    executableName,
                )
            # third option: try to find {executableName} in user/local/programs and subfolders. Takes time to iterate through all files
            if sys.platform.startswith("win32"):
                # is system windows; user-program-path:
                userProgDir = normpath(
                    join(expanduser("~"), "appdata", "local", "programs")
                )
                # try to find {executableName} in user programm path
                if isdir(userProgDir):
                    for root, _, files in walk(userProgDir):
                        if files == f"{executableName}.exe":
                            if verbosity:
                                logging.debug(
                                    "Found %s in '%s'! :)", executableName, root
                                )
                            return join(root, f"{executableName}.exe")
                    # if exe was not found in home dir
                    if verbosity:
                        logging.debug(
                            "%s could not be found in home program folder '%s'",
                            executableName,
                            userProgDir,
                        )
                else:
                    if verbosity:
                        logging.debug("Can't find home directory.")
            else:
                raise SystemError(
                    f"sys.platform is {sys.platform}, not 'win32'.  Could not find home directory"
                )
            if not exePath:
                raise FileNotFoundError(
                    f"Can not find {executableName} on your system! Please install {executableName} or set PATH Variable."
                )
    else:
        if verbosity:
            logging.debug("Found %s in '%s'!", executableName, exePath)
        return exePath


def mergeAllGeoFiles(folderPath, gmshExe):
    # get all files in path:
    allFiles = listdir(folderPath)
    allCommands = list()
    allCommands.append(gmshExe)  # add gmsh exe as first command part
    for filename in allFiles:
        if ".geo" in filename:  # if its a geo file
            geoFilePath = join(folderPath, filename)
            allCommands.append(geoFilePath)  # append the total filename to allCommands
    subprocess.run(allCommands, shell=True)
    return None


def createCmdCommand(
    onelabFile: str,
    useGUI: bool,
    gmshPath: str = "",
    getdpPath: str = "",
    logFileName: str = "",
    paramDict: Dict[str, Union[str, int, float]] = None,
    postOperations: List[str] = None,
) -> str:
    """Create a cmd command to open a .geo or .pro file with the gmsh gui or
    run gmsh and getdp from the command line.

    Args:
        onelabFile (str): Path to the .geo or .pro file.
        useGUI (bool): If True command will open the file in the gmsh gui (independed if its a geo or pro file).
        gmshPath (str): Path to the gmsh executable. By defaults the gmsh exe is searched.
        getdpPath (str, optional): path to a getdp executable. Path will only be used if gui is not used. Defaults to "".
        paramDict (Dict[str, Union[str, int, float]], optional): Dict with parameters to set in the simulation. Defaults to None.

            E.g. to set the onelab parameter "IQ_RMS" for the quadrature rms current to 10A the dict would look like:

            .. code:: python

                {
                    "IQ_RMS": 10,
                }

        postOperations (List[str], optional): List containing the PostOperation names that should be performed after the solving stage.
            ! PostOperations will only be executed if a getdp executable is given !

    Returns:
        str: string of the executable command-line command

    Raises:
        ValueError: If the file extension of onelabFile is not .geo or .pro.
        TypeError: If paramDict is not type dict.
        TypeError: If the parameter value is not str, float or int.
        FileNotFoundError: If onelabFile does not exist or is not a file.
    """
    if not gmshPath:
        gmshPath = findGmsh()
    # check if the onelab file is valid:
    if isfile(onelabFile):
        (filePath, ext) = splitext(onelabFile)
        # first part of the cmd command: open the geo or pro-file
        command = f'{gmshPath} "{onelabFile}"'  # the command is: 'gmsh "FILE.xxx"'
        if ext.lower() == ".geo":
            # if its a geo file
            if not useGUI:
                # run onelab server in command line if gui is False
                #   this does the meshing and database generation
                command += " -run"  # the command is: "gmsh FILE.geo -run"
                if logFileName:
                    command += f" -log {logFileName} "
            # else:
            #   just leave the command as it is: "gmsh FILE.geo" to open gmsh GUI
        elif ext.lower() == ".pro":
            if not useGUI:
                if getdpPath:
                    # if command line and getdp specified
                    
                    # # TODO: Check if mesh file exists -> if not, create command to generate .msh file
                    # if not isfile(filePath+'.msh')

                    command = f"{gmshPath} {filePath}.geo -run "  # set the gmsh file extension to mesh and && for new command
                    if logFileName:
                        command += f" -log {logFileName} "
                    command += "&& "
                    command += f"{getdpPath} {onelabFile} -solve Analysis"  # run the simulation with specific getdp exe
                    # the command is: "gmsh FILE.geo -run && getdp FILE.pro -solve Analysis"
                    # add post operations
                    if postOperations:
                        command += " -pos "
                        for postOp in postOperations:
                            if isinstance(postOp, str):
                                command += postOp + " "
                            else:
                                raise (
                                    ValueError(
                                        f"Given Post Operation name was not a string: {type(postOp)}, {postOp}"
                                    )
                                )
                else:
                    # only command line specified
                    command += " -run"  # just run "gmsh FILE.pro -run", which auto-selects a getdp installation
            # else:
            # if gui was specified, just leave the command as it is: "gmsh FILE.pro" to open gui
        else:
            raise (
                ValueError(
                    f"File '{onelabFile}' has wrong file extension (not '.geo' or '.pro') or is missing file extension: {ext}"
                )
            )
        if paramDict:
            # if the paramDict is not empty or None
            if not isinstance(paramDict, dict):
                raise TypeError(
                    f"Parameter dict was not a dict, but type '{type(paramDict)}.'"
                )
            else:
                for paramName, paramValue in paramDict.items():
                    if isinstance(paramValue, str):
                        command += f" -setstring {paramName} {paramValue}"
                    elif isinstance(paramValue, (float, int)):
                        command += f" -setnumber {paramName} {paramValue}"
                    else:
                        raise (
                            TypeError(
                                f"Parameter value was not string, float or int! -> {type(paramValue)}"
                            )
                        )
    else:
        raise FileNotFoundError(f"Provided Onelab file was not found: {onelabFile}")
    return command

def createGMSHCommand(
    gmshFile: str,
    useGUI: bool,
    gmshPath: str = "",
    logFileName: str = "",
) -> str:
    """Create a cmd command to open a GMSH .geo file with the GUI or
    generate the mesh by running gmsh from the command line.

    Args:
        onelabFile (str): Path to the .geo or .pro file.
        useGUI (bool): If True command will open the file in the gmsh gui (independed if its a geo or pro file).
        gmshPath (str): Path to the gmsh executable. By defaults the gmsh exe is searched.

            E.g. to set the onelab parameter "IQ_RMS" for the quadrature rms current to 10A the dict would look like:

            .. code:: python

                {
                    "IQ_RMS": 10,
                }

        postOperations (List[str], optional): List containing the PostOperation names that should be performed after the solving stage.
            ! PostOperations will only be executed if a getdp executable is given !

    Returns:
        str: string of the executable command-line command

    Raises:
        ValueError: If the file extension of onelabFile is not .geo or .pro.
        TypeError: If paramDict is not type dict.
        TypeError: If the parameter value is not str, float or int.
        FileNotFoundError: If onelabFile does not exist or is not a file.
    """
    if not gmshPath:
        gmshPath = findGmsh()
    # check if the onelab file is valid:
    if isfile(gmshFile):
        (filePath, ext) = splitext(gmshFile)
        # first part of the cmd command: open the geo or pro-file
        command = f'{gmshPath} "{gmshFile}"'  # the command is: 'gmsh "FILE.xxx"'
        if ext.lower() == ".geo":
            # if its a geo file
            if not useGUI:
                # run onelab server in command line if gui is False
                #   this does the meshing and database generation
                command += " -run"  # the command is: "gmsh FILE.geo -run"
                if logFileName:
                    command += f" -log {logFileName} "
            # else:
            #   just leave the command as it is: "gmsh FILE.geo" to open gmsh GUI
        elif ext.lower() == ".pro":
            if not useGUI:
                if getdpPath:
                    # if command line and getdp specified
                    
                    # # TODO: Check if mesh file exists -> if not, create command to generate .msh file
                    # if not isfile(filePath+'.msh')

                    command = f"{gmshPath} {filePath}.geo -run "  # set the gmsh file extension to mesh and && for new command
                    if logFileName:
                        command += f" -log {logFileName} "
                    command += "&& "
                    command += f"{getdpPath} {gmshFile} -solve Analysis"  # run the simulation with specific getdp exe
                    # the command is: "gmsh FILE.geo -run && getdp FILE.pro -solve Analysis"
                    # add post operations
                    if postOperations:
                        command += " -pos "
                        for postOp in postOperations:
                            if isinstance(postOp, str):
                                command += postOp + " "
                            else:
                                raise (
                                    ValueError(
                                        f"Given Post Operation name was not a string: {type(postOp)}, {postOp}"
                                    )
                                )
                else:
                    # only command line specified
                    command += " -run"  # just run "gmsh FILE.pro -run", which auto-selects a getdp installation
            # else:
            # if gui was specified, just leave the command as it is: "gmsh FILE.pro" to open gui
        else:
            raise (
                ValueError(
                    f"File '{gmshFile}' has wrong file extension (not '.geo' or '.pro') or is missing file extension: {ext}"
                )
            )
        if paramDict:
            # if the paramDict is not empty or None
            if not isinstance(paramDict, dict):
                raise TypeError(
                    f"Parameter dict was not a dict, but type '{type(paramDict)}.'"
                )
            else:
                for paramName, paramValue in paramDict.items():
                    if isinstance(paramValue, str):
                        command += f" -setstring {paramName} {paramValue}"
                    elif isinstance(paramValue, (float, int)):
                        command += f" -setnumber {paramName} {paramValue}"
                    else:
                        raise (
                            TypeError(
                                f"Parameter value was not string, float or int! -> {type(paramValue)}"
                            )
                        )
    else:
        raise FileNotFoundError(f"Provided Onelab file was not found: {gmshFile}")
    return command

def main() -> None:
    # print("running main() of runOnelab.")
    # 1. Check that all argvs are valid!
    parser = ArgumentParser(description="Open the given Onelab file with gmsh.")

    parser.add_argument(
        "onelabFile", help="path to the file that should be processed", type=str
    )
    parser.add_argument(
        "--gmsh",
        help="path to the Gmsh executable",
        type=str,
        default="",
    )
    parser.add_argument(
        "--getdp", help="path to the GetDP executable", type=str, default=""
    )
    parser.add_argument(
        "--gui",
        help="flag to decide if the file should be opened in the gui or command line. Defaults to False if flag is not mentioned",
        default=False,
        action="store_true",
    )

    args = parser.parse_args()
    # check if gmsh was provided
    if not args.gmsh:
        # if not provided find gmsh
        args.gmsh = findGmsh()
    else:
        # if provided check if its a correct file
        if not isfile(args.gmsh):
            raise (
                FileNotFoundError(
                    f"Provided gmsh executable was not found: {args.gmsh}"
                )
            )

    command = createCmdCommand(
        args.onelabFile, useGUI=args.gui, gmshPath=args.gmsh, getdpPath=args.getdp
    )
    subprocess.run(command, check=False)


if __name__ == "__main__":
    main()
