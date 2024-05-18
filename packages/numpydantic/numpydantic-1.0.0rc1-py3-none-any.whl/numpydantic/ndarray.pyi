from dask.array.core import Array as DaskArrayCoreArray
from numpydantic.interface.hdf5 import H5ArrayPath
from typing import typing.Tuple[typing.Union[pathlib.Path, str], str]
from pathlib import Path as PathlibPath
from zarr.core import Array as ZarrCoreArray
from numpydantic.interface.zarr import ZarrArrayPath
from numpy import ndarray as Numpyndarray
import typing
import pathlib
NDArray = DaskArrayCoreArray | H5ArrayPath | typing.Tuple[typing.Union[pathlib.Path, str], str] | PathlibPath | ZarrCoreArray | ZarrArrayPath | Numpyndarray