"""Module to export data to Ansys Maxwell"""
from os import path
from ..script.material.material import Material
from . import cleanName
from ..definitions import RESULT_DIR


def exportBH2Maxwell(material: Material, filepath: str = None) -> None:
    """function to export the BH-Curve in ANSYS Maxwell readable format.

    Args:
        data (list): List of data vectors.
        identifier (list[str]): List of data identifier for Maxwell like "H (A_per_meter)" or "B (tesla)".
        filepath (str, optional): File path to write the results to. File extension must be ".tab"!
            Defaults to PYEMMO_RESULTS_FOLDER/MATERIAL_NAME.tab .
    """
    assert not material.linear
    bh = material.getBH()
    b = bh[:, 0]
    h = bh[:, 1]
    header = ["H (A_per_meter)", "B (tesla)"]
    if not filepath:
        filepath = path.join(
            RESULT_DIR, cleanName.cleanName(material.getName()) + "_BH.tab"
        )
    exportTabMaxwell([h, b], header, filepath)


def exportTabMaxwell(data: list, identifier: list[str], filepath: str) -> None:
    """function to export any data in ANSYS Maxwell tab delimited format.

    Args:
        data (list): List of data vectors.
        identifier (list[str]): List of data identifier for Maxwell like "H (A_per_meter)" or "B (tesla)".
        filepath (str, optional): File path to write the results to. File extension must be ".tab"!

    Raises:
        ValueError: If extension is not .tab
    """
    assert len(data) == len(identifier), "data and identifier length are not matching!"
    assert not path.isfile(filepath), f"Given .tab file allready exists: {filepath}"
    assert path.isdir(
        path.dirname(filepath)
    ), f"Folder of given file path does not exist: {filepath}"

    # check file path format
    _, ext = path.splitext(filepath)
    if ext != ".tab":
        raise ValueError("Wrong extension for bh curve export: " + ext)

    fileContent = ""
    for id in identifier:
        fileContent += '"' + id + '"\t'
    fileContent += "\n"
    for i in range(len(data[0])):
        for dataVector in data:
            fileContent += f"{dataVector[i]}\t"
        fileContent += "\n"

    with open(filepath, encoding="utf-8", mode="w") as tabFile:
        tabFile.write(fileContent)
