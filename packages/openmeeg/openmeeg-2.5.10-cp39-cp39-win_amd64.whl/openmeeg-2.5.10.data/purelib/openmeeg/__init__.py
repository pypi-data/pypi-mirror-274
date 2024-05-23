"""""" # start delvewheel patch
def _delvewheel_patch_1_6_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'openmeeg.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-openmeeg-2.5.10')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-openmeeg-2.5.10')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_6_0()
del _delvewheel_patch_1_6_0
# end delvewheel patch

from importlib.metadata import version as _version

from . import _distributor_init

# Here we import as few things as possible to keep our API as limited as
# possible
from ._openmeeg_wrapper import (
    HeadMat,
    Sensors,
    Integrator,
    Head2EEGMat,
    Head2MEGMat,
    DipSourceMat,
    DipSource2MEGMat,
    GainEEG,
    GainMEG,
    GainEEGadjoint,
    GainMEGadjoint,
    GainEEGMEGadjoint,
    Forward,
    SurfSourceMat,
    SurfSource2MEGMat,
    Matrix,
    SymMatrix,
)
from ._make_geometry import make_geometry, make_nested_geometry, read_geometry
from ._utils import get_log_level, set_log_level, use_log_level

try:
    __version__ = _version("openmeeg")
except Exception:
    __version__ = "0.0.0"
del _version

set_log_level("warning")
