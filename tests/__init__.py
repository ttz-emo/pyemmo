from sys import path
from os.path import join, dirname, abspath

# add pyemmo to path
rootname = abspath(join(dirname(__file__), ".."))
print(rootname)
path.append(rootname)

from pyemmo.definitions import TEST_DIR

save_path = join(TEST_DIR, "Results").replace("\\", "/")