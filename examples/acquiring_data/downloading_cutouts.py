"""
==============================================
Requesting cutouts of AIA images from the JSOC
==============================================

This example shows how to request a cutout of a series of
AIA images from the JSOC.
"""
import os

import matplotlib.pyplot as plt

import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.visualization import ImageNormalize, SqrtStretch

import sunpy.map
from sunpy.net import Fido
from sunpy.net import attrs as a

#####################################################
# First, query a full frame AIA image.

start_time = Time('2022-01-01T00:00:00', scale='utc', format='isot')
query = Fido.search(
    a.Instrument.aia,
    a.Physobs.intensity,
    a.Wavelength(171*u.angstrom),
    a.Time(start_time, start_time + 13*u.s),
)
file = Fido.fetch(query)
amap = sunpy.map.Map(file)

#####################################################
# Next, we will use the coordinate frame from this map to define the top right and bottom
# left coordinates we want for the cutout request.

bottom_left = SkyCoord(-100*u.arcsec, -400*u.arcsec, frame=amap.coordinate_frame)
top_right = SkyCoord(400*u.arcsec, 100*u.arcsec, frame=amap.coordinate_frame)

#####################################################
# Now construct the cutout from the coordinates above
# above using the `~sunpy.net.jsoc.attrs.Cutout` attribute.

cutout = a.jsoc.Cutout(bottom_left, top_right=top_right, tracking=True)

#####################################################
# Exporting data from the JSOC requires registering your
# email first. Please replace this with your email
# address once you have registered.
# See `this page <http://jsoc.stanford.edu/ajax/register_email.html>`_
# for more details.

jsoc_email = os.environ["JSOC_EMAIL"]

#####################################################
# Now we are ready to construct the query. Note that all of this is
# the same for a full-frame image except for the
# cutout component. We will download images from a 12 hour interval
# centered on the time of the above cutout.
# We request one image every 2 hours.

query = Fido.search(
    a.Time(amap.date - 6*u.h, amap.date + 6*u.h),
    a.Wavelength(amap.wavelength),
    a.Sample(2*u.h),
    a.jsoc.Series.aia_lev1_euv_12s,
    a.jsoc.Notify(jsoc_email),
    a.jsoc.Segment.image,
    cutout,
)
print(query)

#####################################################
# Submit the export request and download the data.

files = Fido.fetch(query)
files.sort()

#####################################################
# Now that we've downloaded the files, we can create
# a `~sunpy.map.MapSequence` from them and animate
# them.

sequence = sunpy.map.Map(files, sequence=True)

plt.figure()
ani = sequence.plot(norm=ImageNormalize(vmin=0, vmax=5e3, stretch=SqrtStretch()))

plt.show()
