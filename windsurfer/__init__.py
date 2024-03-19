from importlib_metadata import PackageNotFoundError
from importlib_metadata import version as metadata_version

try:
    __version__ = metadata_version("windsurfer")
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass
