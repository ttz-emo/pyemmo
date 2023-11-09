from os import remove
from pyemmo.functions.exportMaxwell import exportTabMaxwell

data = [[1, 2, 3], [4, 5, 6]]
ids = ["H (A_per_meter)", "otherVal (W)"]

file = (
    r"C:\Users\ganser\AppData\Local\Programs\pyemmo\Results\testExportMaxwellData.tab"
)
try:
    exportTabMaxwell(data, ids, file)
except AssertionError as assErr:
    assert "Given .tab file allready exists: " in assErr.args[0]
    print("File allready existed. Removing file and trying again...")
    remove(file)
    exportTabMaxwell(data, ids, file)
    print("Worked.\nDone.")
except Exception as exce:
    raise exce
