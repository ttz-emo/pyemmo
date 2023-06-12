"""This module defines a function to clean strings for variable names in Onelab (C-programming style)"""
import re

def cleanName(instanceName: str) -> str:
    """
    cleanName removes characters that cannot be interpreted by Onelab.
    Like in C programming language there can only be letters, digits and underscores.
    The first letter cannot be a digit.
    
    Args:
        instanceName (str): Variable or entity name to be fixed for Onelab.
    
    Returns:
        str: New string with cleaned name.
    
    Raises:
        ValueError: instanceName must be string
    """
    if not isinstance(instanceName, str):
        raise ValueError(f"Object name was not a string!: {type(instanceName)}")
    pattern = "^([a-zA-Z_][a-zA-Z0-9_]+)$"
    # if there were wrong characters in the name, try to remove them
    if re.match(pattern=pattern, string=instanceName):
        return instanceName
    else:
        newName = instanceName
        if instanceName[0].isdigit():  # check if first char is a number
            newName = "_" + newName  # add underscore to fix that
        # remove possible wrong characters
        # removeChars = ""
        # for char in removeChars:
        #     newName = newName.replace(char, "")
        underscoreChars = r"\/*- .:+<>,;#'`?%&$§"
        for char in underscoreChars:
            newName = newName.replace(char, "_")
        # if there are still wrong chars, raise error
        if not re.match(pattern=pattern, string=newName):
            raise (
                ValueError(
                    f"Variable name '{instanceName}' is invalid for GetDP/Gmsh script. Name could not be resolved. Variable names must have valid C or C# syntax."
                )
            )
    return newName

def isValidFilename(fileName: str) -> bool:
    """check if filename is a valid Windows filename to use.

    Args:
        fileName (str): Given filename.

    Returns:
        bool: True if filename is valid, otherwise False.
    """
    if re.search(r'[^A-Za-z0-9_\-\\]',fileName):
        return False
    return True
