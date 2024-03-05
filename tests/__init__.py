from sys import path
from os.path import join, dirname, abspath
from pyemmo.definitions import TEST_DIR

try:
    import hypothesis
except ImportError:
    pass
else:
    from hypothesis import configuration

    configuration.set_hypothesis_home_dir(join(TEST_DIR, ".hypothesis_venv"))

# add pyemmo to path
rootname = abspath(join(dirname(__file__), ".."))
print(rootname)
path.append(rootname)


save_path = join(TEST_DIR, "Results").replace("\\", "/")
