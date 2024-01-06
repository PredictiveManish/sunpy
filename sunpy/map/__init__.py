"""
SunPy Map

isort:skip_file
"""
# check if user has installed the map extras
from sunpy.util.sysinfo import warn_missing_deps
warn_missing_deps('map')

from ._units import maxwell
from sunpy.map.mapbase import *

from sunpy.map import sources
from sunpy.map.header_helper import *
from sunpy.map.map_factory import Map
from sunpy.map.maputils import *
from .compositemap import CompositeMap
from .mapsequence import MapSequence
