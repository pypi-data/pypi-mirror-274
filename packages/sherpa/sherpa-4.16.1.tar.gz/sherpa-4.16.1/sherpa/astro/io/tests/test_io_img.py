#
#  Copyright (C) 2021, 2023, 2024
#  Smithsonian Astrophysical Observatory
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import numpy as np

import pytest

from sherpa.astro.data import DataIMG, Data2D
from sherpa.astro import io
from sherpa.astro.io.wcs import WCS
from sherpa.utils.testing import requires_data, requires_fits, \
    requires_region, requires_wcs


def backend_is(name):
    """Are we using the given backend?"""
    return io.backend.__name__ == f"sherpa.astro.io.{name}_backend"


@requires_fits
@requires_data
def test_image_write_basic(make_data_path, tmp_path):
    """Check we can write out an image file as a FITS file
    and keep useful data.
    """

    def check_header(obj):
        # check header for a selected set of keywords
        hdr = obj.header

        assert "HDUNAME" not in hdr

        assert hdr["HDUCLASS"] == "OGIP"
        assert hdr["HDUCLAS1"] == "EVENTS"
        assert hdr["HDUCLAS2"] == "ACCEPTED"
        assert "HDUCLAS3" not in hdr
        assert hdr["HDUVERS"] == "1.0.0"

        # a few header keywords to check they are handled,
        # including data types (string, float, integer,
        # logical).
        #
        assert hdr["OBJECT"] == "CSC"
        assert hdr["INSTRUME"] == "ACIS"
        assert hdr["GRATING"] == "NONE"
        assert hdr["DETNAM"] == "ACIS-0"
        assert hdr["RAND_SKY"] == pytest.approx(0.5)
        assert hdr["RAND_PI"] == pytest.approx(1.0)
        assert hdr["DATE-OBS"] == "2006-11-25T09:25:17"
        assert isinstance(hdr["CLOCKAPP"], (bool, np.bool_))
        assert hdr["CLOCKAPP"]
        assert hdr["TIMEZERO"] == 0

        assert "EQUINOX" not in hdr

    def check_data(obj):
        """Basic checks of the data"""

        assert obj.shape == (377, 169)
        assert obj.staterror is None
        assert obj.syserror is None

        assert isinstance(obj.sky, io.wcs.WCS)
        assert isinstance(obj.eqpos, io.wcs.WCS)

        assert obj.sky.name == "physical"
        assert obj.sky.type == "LINEAR"
        assert obj.sky.crval == pytest.approx([3061.8101, 4332.6299])
        assert obj.sky.crpix == pytest.approx([0.5, 0.5])
        assert obj.sky.cdelt == pytest.approx([1.0, 1.0])

        assert obj.eqpos.name == "world"
        assert obj.eqpos.type == "WCS"
        assert obj.eqpos.crval == pytest.approx([149.8853, 2.60795])
        assert obj.eqpos.crpix == pytest.approx([4096.5, 4096.5])
        cd = 0.492 / 3600
        assert obj.eqpos.cdelt == pytest.approx([-cd, cd])
        assert obj.eqpos.crota == pytest.approx(0)
        assert obj.eqpos.epoch == pytest.approx(2000.0)
        assert obj.eqpos.equinox == pytest.approx(2000.0)

        assert obj.coord == "logical"

        assert obj.x0.shape == (63713, )
        assert obj.x1.shape == (63713, )
        assert obj.y.shape == (63713, )

        yexp, xexp = np.mgrid[1:378, 1:170]
        xexp = xexp.flatten()
        yexp = yexp.flatten()

        assert obj.x0 == pytest.approx(xexp)
        assert obj.x1 == pytest.approx(yexp)

        vals = obj.y.reshape((377, 169))
        expected = np.asarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 2])
        assert vals[184:194, 83] == pytest.approx(expected)

        # What do we expect for the data types? It is backend-specific
        #
        assert obj.x0.dtype == np.dtype("float64")
        assert obj.x1.dtype == np.dtype("float64")
        if backend_is("crates"):
            assert obj.y.dtype == np.dtype("float64")

        elif backend_is("pyfits"):
            assert obj.y.dtype == np.dtype(">i2")

        else:
            pytest.fail("Unrecognized IO backend")

    infile = make_data_path("acisf07999_000N001_r0035_regevt3_srcimg.fits")
    indata = io.read_image(infile)
    assert isinstance(indata, DataIMG)
    assert indata.name.endswith("/acisf07999_000N001_r0035_regevt3_srcimg.fits")
    check_header(indata)
    check_data(indata)

    # check we can write it out - be explicit with all options
    #
    outfile = tmp_path / "test.img"
    outfile = str(outfile)  # our IO routines don't recognize paths
    io.write_image(outfile, indata, ascii=False, clobber=False)

    outdata = io.read_image(outfile)
    assert isinstance(outdata, DataIMG)
    assert outdata.name.endswith("/test.img")
    check_header(outdata)
    check_data(outdata)


@requires_fits
@requires_data
@requires_wcs  # only needed for physical and world
@pytest.mark.parametrize("incoord,outcoord,x0,x1",
                         [("logical", None, 1, 1),
                          ("image", "logical", 1, 1),
                          ("physical", None, 2987.3400878906, 4363.16015625),
                          ("world", None, 150.03707837630427, 2.644383154504334),
                          ("wcs", "world", 150.03707837630427, 2.644383154504334)])
def test_1762(incoord, outcoord, x0, x1, make_data_path):
    """What does setting a non-logical coord system do?

    This is a regression test so depends on whether #1762 is
    fixed or not.
    """

    infile = make_data_path("acisf08478_000N001_r0043_regevt3_srcimg.fits")
    d = io.read_image(infile, coord=incoord)

    if outcoord is None:
        assert d.coord == incoord
    else:
        assert d.coord == outcoord

    # Just check the first element
    i0, i1 = d.get_indep()
    assert i0[0] == pytest.approx(x0)
    assert i1[0] == pytest.approx(x1)


@requires_fits
@requires_data
def test_can_read_image_as_data2d(make_data_path):
    """We should be able to read in an image as a Data2D object"""

    infile = make_data_path("acisf08478_000N001_r0043_regevt3_srcimg.fits")
    dimg = io.read_image(infile, dstype=DataIMG)
    d2d = io.read_image(infile, dstype=Data2D)

    assert d2d.x0 == pytest.approx(dimg.x0)
    assert d2d.x1 == pytest.approx(dimg.x1)
    assert d2d.y == pytest.approx(dimg.y)


@requires_fits
@requires_region
@requires_wcs
def test_axs_ordering(tmp_path):
    """Check out the #1789 #1880 behavior.

    See sherpa/astro/tests/test_astro_data2.py::test_dataimg_axis_ordering
    """

    # nx=3, ny=2
    #
    x1, x0 = np.mgrid[1:3, 1:4]
    x0 = x0.flatten()
    x1 = x1.flatten()
    y = np.arange(6) * 10 + 10

    sky = WCS("physical", "LINEAR", [100, 200], [1, 1], [10, 10])
    eqpos = WCS("world", "WCS", [30, 50], [100, 200], [-0.1, 0.1])
    orig = DataIMG("faked", x0, x1, y, shape=(2, 3), sky=sky,
                   eqpos=eqpos)

    outfile = tmp_path / "test.img"
    outfile = str(outfile)
    io.write_image(outfile, orig, ascii=False, clobber=False)

    new = io.read_image(outfile)
    new.set_coord("physical")
    new.notice2d("circle(110, 210, 6)", True)

    assert new.get_dep(filter=True) == pytest.approx([10, 20, 30, 40, 60])
    a0, a1 = new.get_indep()
    assert a0 == pytest.approx([100, 110, 120] * 2)
    assert a1 == pytest.approx([200, 200, 200, 210, 210, 210])


@requires_fits
@requires_region
@requires_wcs
def test_axs_ordering_1880(tmp_path):
    """Check out the #1880 behavior.

    See sherpa/astro/tests/test_astro_data2.py::test_dataimg_axis_ordering_1880
    """

    # nx=2, ny=3
    #
    x1, x0 = np.mgrid[1:4, 1:3]
    x0 = x0.flatten()
    x1 = x1.flatten()
    y = np.arange(6) * 10 + 10

    sky = WCS("physical", "LINEAR", [100, 200], [1, 1], [10, 10])
    eqpos = WCS("world", "WCS", [30, 50], [100, 200], [-0.1, 0.1])
    orig = DataIMG("faked", x0, x1, y, shape=(2, 3), sky=sky,
                   eqpos=eqpos)

    outfile = tmp_path / "test.img"
    outfile = str(outfile)
    io.write_image(outfile, orig, ascii=False, clobber=False)

    new = io.read_image(outfile)
    new.set_coord("physical")
    new.notice2d("circle(110, 210, 6)", True)

    # Unlike test_dataimg_axis_ordering, this filter does remove the
    # bin=50 pixel, but the independent axes do not match x0, x1
    # above.
    #
    assert new.get_dep(filter=True) == pytest.approx([10, 20, 30, 40, 60])
    a0, a1 = new.get_indep()
    assert a0 == pytest.approx([100, 110, 120] * 2)
    assert a1 == pytest.approx([200, 200, 200, 210, 210, 210])
