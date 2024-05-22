#
#  Copyright (C) 2007, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023
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
"""Provide Astronomy-specific I/O routines for Sherpa.

This module contains read and write routines for handling `FITS
<https://en.wikipedia.org/wiki/FITS>`_ and ASCII format data. The
actual support is provided by the selected I/O backend package
(currently Crates, provided by CIAO, or the FITS support in the
AstroPy package, if installed).

Which backend is used?
----------------------

When this module is first imported, Sherpa tries to import the
backends installed with Sherpa in the order listed in the
``.sherpa.rc`` or ``.sherpa-standalone.rc`` file. The first module that imports
successfully is set as the active backend. The following command prints the
name and the location on disk of that module:

   >>> from sherpa.astro import io
   >>> print(io.backend)

Change the backend
------------------

After the initial import, the backend can be changed by loading one of the
I/O backends shipped with sherpa (or any other module that provides the same
interface):

  >>> import sherpa.astro.io.pyfits_backend
  >>> io.backend = sherpa.astro.io.pyfits_backend

"""

from configparser import ConfigParser
import importlib
import logging
import os
import re
from typing import Any, Optional

import numpy

from sherpa import get_config
from sherpa.astro.data import DataIMG, DataIMGInt, DataARF, DataRMF, \
    DataPHA, DataRosatRMF
# leads to circular imports
# from sherpa.astro.instrument import ARF1D, RMF1D
from sherpa.astro.utils import reshape_2d_arrays
from sherpa.data import Data2D, Data1D, BaseData, Data2DInt
import sherpa.io
from sherpa.utils.err import ArgumentErr, DataErr, IOErr
from sherpa.utils.numeric_types import SherpaFloat

config = ConfigParser()
config.read(get_config())

# What should we use for the default package?
io_opt = [o.strip().lower() + '_backend' for o in
          config.get('options', 'io_pkg', fallback='dummy').split()]

ogip_emin_str = config.get('ogip', 'minimum_energy', fallback='1.0e-10')

ogip_emin : Optional[float]
if ogip_emin_str.upper() == 'NONE':
    ogip_emin = None
else:
    emsg = "Invalid value for [ogip] minimum_energy config value; " + \
           "it must be None or a float > 0"
    try:
        ogip_emin = float(ogip_emin_str)
    except ValueError as ve:
        raise ValueError(emsg) from ve

    if ogip_emin <= 0.0:
        raise ValueError(emsg)

backend = None
'''Currently active backend module for astronomy specific I/O.'''

for iotry in io_opt:
    try:
        backend = importlib.import_module('.' + iotry,
                                          package='sherpa.astro.io')
        break
    except ImportError:
        pass
else:
    # None of the options in the rc file work, e.g. because it's an old file
    # that does not have dummy listed
    import sherpa.astro.io.dummy_backend as backend

warning = logging.getLogger(__name__).warning
info = logging.getLogger(__name__).info


__all__ = ('backend',
           'read_table', 'read_image', 'read_arf', 'read_rmf', 'read_arrays',
           'read_pha', 'write_image', 'write_pha', 'write_table',
           'write_arf', 'write_rmf',
           'pack_table', 'pack_image', 'pack_pha', 'read_table_blocks')


# Note: write_arrays is not included in __all__, so don't add to the
#       See Also section.
#
def read_arrays(*args):
    """Create a dataset from multiple arrays.

    The return value defaults to a `sherpa.data.Data1D` instance,
    but this can be changed by supplying the required class
    as the last argument (anything that is derived from
    `sherpa.data.BaseData`).

    Parameters
    ----------
    *args
        There must be at least one argument. The number of
        arguments depends on the data type being read in.
        The supported argument types depends on the I/O backend
        in use (as supported by the ``get_column_data`` routine
        provided by the backend).

    Returns
    -------
    data : a sherpa.data.BaseData derived object

    Examples
    --------
    The following examples do not contain argument types specific to
    a particular I/O backend.

    Create a `sherpa.data.Data1D` instance from the data in the
    arrays ``x`` and ``y`` (taken to be the independent and
    dependent axes respectively):

    >>> d = read_arrays(x, y)

    As in the previous example, but explicitly declaring the data type:

    >>> d = read_arrays(x, y, sherpa.data.Data1D)

    Create a `sherpa.data.Data2D` instance with the independent
    axes ``x0`` and ``x1``, and dependent axis ``y``:

    >>> d = read_arrays(x0, x1, y, sherpa.data.Data2D)

    """
    args = list(args)
    if len(args) == 0:
        raise IOErr('noarrays')

    dstype = Data1D
    if sherpa.io._is_subclass(args[-1], BaseData):
        dstype = args.pop()

    args = backend.get_column_data(*args)

    # Determine max number of args for dataset constructor
    sherpa.io._check_args(len(args), dstype)

    return dstype('', *args)


def read_table(arg, ncols=2, colkeys=None, dstype=Data1D):
    """Create a dataset from a tabular file.

    The supported file types (e.g. ASCII or FITS) depends on the
    selected I/O backend.

    Parameters
    ----------
    arg
        The name of the file or a representation of the file
        (the type depends on the I/O backend).
    ncols : int, optional
        The first ncols columns are read from the file.
    colkeys : None or list of strings, optional
        If given, select these columns from the file.
    dstype : optional
        The data type to create (it is expected to follow the
        `sherpa.data.BaseData` interface).

    Returns
    -------
    data : a sherpa.data.BaseData derived object

    See Also
    --------
    write_table

    Examples
    --------
    The following examples do not contain argument types specific to
    a particular I/O backend.

    Create a `sherpa.data.Data1D` object from the first two
    columns in the file ``src.fits``:

    >>> d = read_table('src.fits')

    Create a `sherpa.data.Data1DInt` object from the first three
    columns in the file ``src.fits``:

    >>> d = read_table('src.fits', ncols=3, dstype=Data1DInt)

    Create a `sherpa.data.Data1D` data set from the specified
    columns in ``tbl.fits``, where ``WLEN`` is used for the
    independent axis, ``FLUX`` the dependent axis, and
    ``FLUXERR`` for the statistical error on the dependent axis:

    >>> d = read_table('tbl.fits', colkeys=['WLEN', 'FLUX', 'FLUXERR'])

    """
    args = backend.get_table_data(arg, ncols, colkeys)
    cols = args[1]
    name = args[2]

    # Determine max number of args for dataset constructor
    sherpa.io._check_args(len(cols), dstype)

    return dstype(name, *cols)


# TODO: should this be exported?
def read_ascii(filename, ncols=2, colkeys=None, dstype=Data1D, **kwargs):
    """Create a dataset from an ASCII tabular file.

    Parameters
    ----------
    filename : str
        The name of the file or a representation of the file
        (the type depends on the I/O backend).
    ncols : int, optional
        The first ncols columns are read from the file.
    colkeys : None or list of strings, optional
        If given, select these columns from the file.
    dstype : optional
        The data type to create (it is expected to follow the
        `sherpa.data.BaseData` interface).
    **kwargs
        The remaining arguments are passed through to the
        ``get_ascii_data`` routine of the I/O backend. It is
        expected that these include ``sep`` and ``comment``,
        which describe the column separators and indicator of
        a comment line, respectively.

    Returns
    -------
    data : a sherpa.data.BaseData derived object

    Examples
    --------
    The following examples do not contain argument types specific to
    a particular I/O backend.

    Create a `sherpa.data.Data1D` object from the first two
    columns in the file ``src.dat``:

    >>> d = read_ascii('src.dat')

    Create A `sherpa.data.Data1DInt` object from the first three
    columns in the file ``src.dat``:

    >>> d = read_ascii('src.dat', ncols=3, dstype=Data1DInt)

    Create a `sherpa.data.Data1D` data set from the specified
    columns in ``tbl.fits``, where ``WLEN`` is used for the
    independent axis, ``FLUX`` the dependent axis, and
    ``FLUXERR`` for the statistical error on the dependent axis:

    >>> d = read_ascii('tbl.fits', colkeys=['WLEN', 'FLUX', 'FLUXERR'])

    """
    args = backend.get_ascii_data(filename, ncols=ncols, colkeys=colkeys,
                                  dstype=dstype, **kwargs)
    cols = args[1]
    name = args[2]

    # Determine max number of args for dataset constructor
    sherpa.io._check_args(len(cols), dstype)

    return dstype(name, *cols)


def read_image(arg, coord='logical', dstype=DataIMG):
    """Create an image dataset from a file.

    .. versionchanged:: 4.16.0
       Setting coord to a value other than 'logical' will now
       correctly change the coordinate setting for `DataIMG` datasets.

    Parameters
    ----------
    arg
        The name of the file or a representation of the file
        (the type depends on the I/O backend).
    coord : {'logical', 'physical', 'world'}, optional
        The type of axis coordinates to use. An error is raised if the
        file does not contain the necessary metadata for the selected
        coordinate system.
    dstype : optional
        The data type to create (it is expected to follow the
        `sherpa.data.BaseData` interface).

    Returns
    -------
    data : a sherpa.data.BaseData derived object

    See Also
    --------
    write_image

    Examples
    --------
    The following examples do not contain argument types specific to
    a particular I/O backend.

    Create a `sherpa.astro.data.DataIMG` object from the FITS file
    ``img.fits``:

    >>> d = read_image('img.fits')

    Select the physical coordinate system from the file:

    >>> d = read_image('img.fits', coord='physical')

    """
    data, filename = backend.get_image_data(arg)
    data['header'] = _remove_structural_keywords(data['header'])
    axlens = data['y'].shape

    x0 = numpy.arange(axlens[1], dtype=SherpaFloat) + 1.
    x1 = numpy.arange(axlens[0], dtype=SherpaFloat) + 1.
    x0, x1 = reshape_2d_arrays(x0, x1)

    data['y'] = data['y'].ravel()
    data['shape'] = axlens

    # We have to be careful with issubclass checks because
    #
    #   base class |   sub class
    #    Data2D        Data2DInt
    #    Data2D        DataIMG
    #    DataIMG       DataIMGInt
    #
    # Drop the transform fields if the object doesn't support them.
    #
    if not issubclass(dstype, DataIMG):
        for name in ['eqpos', 'sky', 'header']:
            data.pop(name, None)

    # What are the independent axes?
    #
    if issubclass(dstype, (Data2DInt, DataIMGInt)):
        indep = [x0 - 0.5, x1 - 0.5, x0 + 0.5, x1 + 0.5]
    else:
        indep = [x0, x1]

    # Note that we only set the coordinates after creating the
    # dataset, which assumes that data['x'] and data['y'] are always
    # in logical units. They may not be, but in this case we need to
    # drop the logical/physical/world conversion system (or improve it
    # to be more flexible). This is an attempt to resolve issue #1762,
    # where sherpa.astro.ui.load_image(infile, coord="physical") did
    # not behave sensibly (likely due to #1414 which was to address
    # issue #1380).
    #
    dataset = dstype(filename, *indep, **data)

    if issubclass(dstype, DataIMG):
        dataset.set_coord(coord)

    return dataset


def read_arf(arg):
    """Create a DataARF object.

    Parameters
    ----------
    arg
        The name of the file or a representation of the file
        (the type depends on the I/O backend) containing the
        ARF data.

    Returns
    -------
    data : sherpa.astro.data.DataARF

    """
    data, filename = backend.get_arf_data(arg)
    data['header'] = _remove_structural_keywords(data['header'])

    # It is unlikely that the backend will set this, but allow
    # it to override the config setting.
    #
    if 'emin' not in data:
        data['ethresh'] = ogip_emin

    return DataARF(filename, **data)


def read_rmf(arg):
    """Create a DataRMF object.

    Parameters
    ----------
    arg
        The name of the file or a representation of the file
        (the type depends on the I/O backend) containing the
        RMF data.

    Returns
    -------
    data : sherpa.astro.data.DataRMF

    """
    data, filename = backend.get_rmf_data(arg)
    data['header'] = _remove_structural_keywords(data['header'])

    # It is unlikely that the backend will set this, but allow
    # it to override the config setting.
    #
    if 'emin' not in data:
        data['ethresh'] = ogip_emin

    return _rmf_factory(filename, data)


def _rmf_factory(filename, data):
    response_map = {
        'ROSAT': DataRosatRMF,
        'DEFAULT': DataRMF,
    }

    rmf_telescop = data['header'].get('TELESCOP', 'DEFAULT')
    rmf_class = response_map.get(rmf_telescop, DataRMF)

    return rmf_class(filename, **data)


def _read_ancillary(data, key, label, dname,
                    read_func, output_once=True):
    """Read in a file if the keyword is set.

    Parameters
    ----------
    data
        The header information, which behaves like a dictionary.
    key
        The key to look for in data. If not set, or its value compares
        case insensitively to "none" then nothing is read in.
    label : str
        This is used to identify the file being read in. It is only
        used if output_once is set.
    dname : str
        The location of the file containing the metadata. This is prepended
        to  the value read from the data argument if it is not an
        absolute path.
    read_func
        The function used to read in the file: it expects one argument,
        the file to read in, and returns the data object.
    output_once : bool, optional
        If set then the routine uses the Sherpa logger to display
        informational or warning information.

    Returns
    -------
    data : None or a sherpa.data.BaseData derived object

    """

    if not(data[key]) or data[key].lower() == 'none':
        return None

    out = None
    try:
        if os.path.dirname(data[key]) == '':
            data[key] = os.path.join(dname, data[key])

        out = read_func(data[key])
        if output_once:
            info(f'read {label} file {data[key]}')

    except Exception as exc:
        if output_once:
            warning(str(exc))

    return out


def read_pha(arg, use_errors=False, use_background=False):
    """Create a DataPHA object.

    Parameters
    ----------
    arg
        The name of the file or a representation of the file
        (the type depends on the I/O backend) containing the
        PHA data.
    use_errors : bool, optional
        If the PHA file contains statistical error values for the
        count (or count rate) column, should it be read in. This
        defaults to ``False``.
    use_background : bool, optional
        Should the background PHA data (and optional responses) also
        be read in and associated with the data set?

    Returns
    -------
    data : sherpa.astro.data.DataPHA

    """
    datasets, filename = backend.get_pha_data(arg,
                                              use_background=use_background)
    phasets = []
    output_once = True
    for data in datasets:
        data['header'] = _remove_structural_keywords(data['header'])

        if not use_errors:
            if data['staterror'] is not None or data['syserror'] is not None:
                if data['staterror'] is None:
                    msg = 'systematic'
                elif data['syserror'] is None:
                    msg = 'statistical'
                    if output_once:
                        warning("systematic errors were not found in "
                                "file '%s'", filename)

                else:
                    msg = 'statistical and systematic'

                if output_once:
                    info("%s errors were found in file '%s'\n"
                         "but not used; to use them, re-read "
                         "with use_errors=True", msg, filename)

                data['staterror'] = None
                data['syserror'] = None

        dname = os.path.dirname(filename)
        albl = 'ARF'
        rlbl = 'RMF'
        if use_background:
            albl = albl + ' (background)'
            rlbl = rlbl + ' (background)'

        arf = _read_ancillary(data, 'arffile', albl, dname, read_arf,
                              output_once)
        rmf = _read_ancillary(data, 'rmffile', rlbl, dname, read_rmf,
                              output_once)

        backgrounds = []

        if data['backfile'] and data['backfile'].lower() != 'none':
            try:
                if os.path.dirname(data['backfile']) == '':
                    data['backfile'] = os.path.join(os.path.dirname(filename),
                                                    data['backfile'])

                bkg_datasets = []
                # Do not read backgrounds of backgrounds
                if not use_background:
                    bkg_datasets = read_pha(data['backfile'], use_errors, True)
                    if output_once:
                        info(f"read background file {data['backfile']}")

                if numpy.iterable(bkg_datasets):
                    for bkg_dataset in bkg_datasets:
                        if bkg_dataset.get_response() == (None, None) and \
                           rmf is not None:
                            bkg_dataset.set_response(arf, rmf)
                        backgrounds.append(bkg_dataset)
                else:
                    if bkg_datasets.get_response() == (None, None) and \
                       rmf is not None:
                        bkg_datasets.set_response(arf, rmf)
                    backgrounds.append(bkg_datasets)

            except Exception as exc:
                if output_once:
                    warning(str(exc))

        for bkg_type, bscal_type in zip(('background_up', 'background_down'),
                                        ('backscup', 'backscdn')):
            if data[bkg_type] is not None:
                bkg = DataPHA(filename,
                              channel=data['channel'],
                              counts=data[bkg_type],
                              bin_lo=data['bin_lo'],
                              bin_hi=data['bin_hi'],
                              grouping=data['grouping'],
                              quality=data['quality'],
                              exposure=data['exposure'],
                              backscal=data[bscal_type],
                              header=data['header'])
                bkg.set_response(arf, rmf)
                if output_once:
                    info(f"read {bkg_type} into a dataset from file {filename}")
                backgrounds.append(bkg)

        for k in ['backfile', 'arffile', 'rmffile', 'backscup', 'backscdn',
                  'background_up', 'background_down']:
            data.pop(k, None)

        pha = DataPHA(filename, **data)
        pha.set_response(arf, rmf)
        for i, bkg in enumerate(backgrounds):
            if bkg.grouping is None:
                bkg.grouping = pha.grouping
                bkg.grouped = bkg.grouping is not None
            if bkg.quality is None:
                bkg.quality = pha.quality
            pha.set_background(bkg, i + 1)

        # set units *after* bkgs have been set
        pha._set_initial_quantity()
        phasets.append(pha)
        output_once = False

    if len(phasets) == 1:
        phasets = phasets[0]

    return phasets


def _pack_table(dataset):
    """Identify the columns in the data.

    This relies on the _fields attribute containing the data columns,
    and _extra_fields the extra information (other than the name
    column). We only return values from _fields that contain data.

    Parameters
    ----------
    dataset : sherpa.data.Data instance

    Returns
    -------
    data : dict
        The dictionary containing the columns to write out, with
        the column names being converted to upper case.

    """
    data = {}
    for name in dataset._fields:
        if name == 'name':
            continue

        val = getattr(dataset, name)
        if val is None:
            continue

        # Convert to upper-case names
        data[name.upper()] = val

    return data


def _pack_image(dataset):
    if not isinstance(dataset, (Data2D, DataIMG)):
        raise IOErr('notimage', dataset.name)

    data = {}

    # Data2D does not have a header
    header = getattr(dataset, "header", {})

    data['pixels'] = numpy.asarray(dataset.get_img())
    data['sky'] = getattr(dataset, 'sky', None)
    data['eqpos'] = getattr(dataset, 'eqpos', None)

    return data, header


# This is to match NAXIS1 and the like, but we do not make it
# very prescriptive (ie enforce the FITS keyword standards).
#
NUMBERED_KEYWORD_PAT = re.compile(r"^([^\d]+)(\d+)$")


def _is_structural_keyword(key: str) -> bool:
    """Do we think this is a "structural" keyword?

    Parameters
    ----------
    key : str
       The keyword (need not be upper case).

    Returns
    -------
    flag : bool
       Is this considered a structural keyword.

    Notes
    -----
    The decision of what is a structural header and what isn't is
    rather ad-hoc and may need to be updated over time. The current
    code is based in part on the `HEASARC keyword list
    <https://heasarc.gsfc.nasa.gov/docs/fcg/standard_dict>`_.

    This does not strip out the OGIP keywords like HDUCLAS1 or
    HDUVERS.

    It does not remove secondary WCS keywords, like CTYPE1P.

    """

    ukey = key.upper()
    if ukey in ["BITPIX", "BLANK", "BLOCKED", "BSCALE", "BUNIT",
                "BZERO", "DATAMAX", "DATAMIN", "END", "EXTEND",
                "EXTLEVEL", "EXTNAME", "EXTVER", "GCOUNT", "GROUPS",
                "NAXIS", "PCOUNT", "SIMPLE", "TFIELDS", "THEAP",
                "XTENSION",
                # other common ones
                "CHECKSUM", "DATASUM", "CHECKVER",
                # HEASARC
                "TSORTKEY",
                # CIAO uses this as well as EXTNAME
                "HDUNAME"
                ]:
        return True

    # Keywords which end in 1, 2, ..
    match = NUMBERED_KEYWORD_PAT.match(ukey)
    if match is None:
        return False

    # The pattern is not completely robust so catch a case when
    # it does not restrict to an integer > 0.
    #
    if match[2].startswith("0"):
        return False

    return match[1] in ["CDELT", "CROTA", "CRPIX", "CRVAL", "CTYPE", "CUNIT",
                        "NAXIS", "PSCAL", "PTYPE", "PZERO", "TBCOL",
                        "TDIM", "TDISP", "TFORM", "TNULL", "TSCAL",
                        "TTYPE", "TUNIT", "TZERO",
                        "TCTYP", "TCUNI", "TCRPX", "TCRVL", "TCDLT",
                        # HEASARC
                        "TDMAX", "TDMIN", "TLMAX", "TLMIN",
                        # CIAO Data-Model keywords
                        "DSTYP", "DSVAL", "DSFORM", "DSUNIT", "TDBIN",
                        "MTYPE", "MFORM",
                        ]


def _remove_structural_keywords(header: dict[str, Any]) -> dict[str, Any]:
    """Remove FITS keywords relating to file structure.

    The aim is to allow writing out a header that was taken from a
    file and not copy along "unwanted" values, since the data may
    no-longer be relevant. Not all FITS header keys may be passed
    along by a particular backend (e.g. crates).

    Parameters
    ----------
    header : dict[str, Any]
       The input header

    Returns
    -------
    nheader : dict[str, Any]
       Header with unwanted keywords returned (including those
       set to None).

    Notes
    -----
    The tricky part is knowing what is unwanted, since copying
    along a WCS transform for a column may be useful, or may
    break things.

    """

    out = {}
    for key, value in header.items():
        if value is None or _is_structural_keyword(key):
            continue

        out[key] = value

    return out


def _pack_pha(dataset):
    """Extract FITS column and header information.

    Notes
    -----
    The `PHA Data Extension header page
    <https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/docs/spectra/ogip_92_007/node6.html>`_
    lists the following keywords as either required or
    we-really-want-them:

        EXTNAME = "SPECTRUM"
        TELESCOP - the "telescope" (i.e. mission/satellite name).
        INSTRUME - the instrument/detector.
        FILTER - the instrument filter in use (if any)
        EXPOSURE - the integration time (in seconds) for the PHA data (assumed to be corrected for deadtime, data drop-outs etc. )
        BACKFILE - the name of the corresponding background file (if any)
        CORRFILE - the name of the corresponding correction file (if any)
        CORRSCAL - the correction scaling factor.
        RESPFILE - the name of the corresponding (default) redistribution matrix file (RMF; see George et al. 1992a).
        ANCRFILE - the name of the corresponding (default) ancillary response file (ARF; see George et al. 1992a).
        HDUCLASS = "OGIP"
        HDUCLAS1 = "SPECTRUM"
        HDUVERS = "1.2.1"
        POISSERR - whether Poissonian errors are appropriate to the data (see below).
        CHANTYPE - whether the channels used in the file have been corrected in any way (see below).
        DETCHANS - the total number of detector channels available.

    We also add in the following, defaulting to the first value - we
    should do better to support HDUCLAS3=RATE data!

        HDUCLAS2 - indicating the type of data stored.
          Allowed values are:
            'TOTAL' for a gross PHA Spectrum (source + bkgd)
            'NET' for a bkgd-subtracted PHA Spectrum
            'BKG' for a bkgd PHA Spectrum
        HDUCLAS3 - indicating further details of the type of data stored.
          Allowed values are:
            'COUNT' for PHA data stored as counts (rather than count/s)
            'RATE' for PHA data stored in count/s
        HDUCLAS4 - indicating whether this is a type I or II extension.
          Allowed values are:
            'TYPE:I' for type I (single spectrum) data
            'TYPE:II' for type II (multiple spectra) data

    The POISSERR keyword is not required if a STAT_ERR column is
    present however it is recommended in this case for clarity. If
    STAT_ERR is to be used for the errors then POISSERR is set to
    false.

    If the CHANNEL array doesn't start at 1 then TLMIN1 and TLMAX1 are
    required (here we assume the CHANNEL column is first) and they are
    strongly recommended otherwise.

    """

    # The logic here repeats some of the checks that probably should
    # be done by the DataPHA class itself. However, it is likely
    # that we don't want to make the DataPHA class always reject
    # inconsistent state, as this could preclude certain workflows,
    # so we need some validation here.
    #
    if not isinstance(dataset, DataPHA):
        raise IOErr("notpha", dataset.name)

    arf, rmf = dataset.get_response()
    bkg = dataset.get_background()

    # The default keywords; these will be over-ridden by
    # anything set by the input.
    #
    default_header = {
        "EXTNAME": "SPECTRUM",
        "HDUCLASS": "OGIP",
        "HDUCLAS1": "SPECTRUM",
        "HDUCLAS2": "TOTAL",
        "HDUCLAS3": "COUNT",
        "HDUCLAS4": "TYPE:I",
        "HDUVERS": "1.2.1",
        "HDUDOC": "Arnaud et al. 1992a Legacy 2  p 65",

        # Rely on the DataPHA class to have set up TELESCOP/INSTRUME/FILTER
        # based on any associated background or response. If the user has
        # changed them then so be it.
        #
        "TELESCOP": "none",
        "INSTRUME": "none",
        "FILTER": "none",
        "CORRFILE": "none",
        "CORRSCAL": 0,
        "CHANTYPE": "PI",
        "RESPFILE": "none",
        "ANCRFILE": "none",
        "BACKFILE": "none"
    }

    # Header Keys
    header = dataset.header

    # Merge the keywords
    #
    header = default_header | header

    # Over-write the header value (if set). This value should really
    # exist (OGIP standards) but may not, particularly for testing.
    #
    if dataset.exposure is not None:
        header["EXPOSURE"] = dataset.exposure

    def _set_keyword(label: str, value: Optional[Data1D]) -> None:
        """Do we set the *FILE keyword?"""

        if value is None or value.name is None:
            return

        # Split on / and then take the last element. Should this
        # instead make the path relative to the file name for the PHA
        # dataset (but the problem is that this information is not
        # known here)?
        #
        toks = value.name.split("/")
        header[label] = toks[-1]

    _set_keyword("RESPFILE", rmf)
    _set_keyword("ANCRFILE", arf)
    _set_keyword("BACKFILE", bkg)

    # The column ordering for the output file is determined by the
    # order the keys are added to the data dict.
    #
    # TODO: perhaps we should error out if channel or counts is not set?
    #
    data = {}
    data["channel"] = getattr(dataset, "channel", None)
    data["counts"] = getattr(dataset, "counts", None)
    data["stat_err"] = getattr(dataset, "staterror", None)
    data["sys_err"] = getattr(dataset, "syserror", None)
    data["bin_lo"] = getattr(dataset, "bin_lo", None)
    data["bin_hi"] = getattr(dataset, "bin_hi", None)
    data["grouping"] = getattr(dataset, "grouping", None)
    data["quality"] = getattr(dataset, "quality", None)

    def convert_scale_value(colname):
        val = getattr(dataset, colname, None)
        uname = colname.upper()
        if val is None:
            header[uname] = 1.0
            return

        if numpy.isscalar(val):
            header[uname] = val
        else:
            data[colname] = val
            try:
                del header[uname]
            except KeyError:
                pass

    # This over-writes (or deletes) the header
    convert_scale_value("backscal")
    convert_scale_value("areascal")

    # Replace columns where appropriate.
    #
    if data["sys_err"] is None or (data["sys_err"] == 0).all():
        header["SYS_ERR"] = 0.0
        del data["sys_err"]

    if data["quality"] is None or (data["quality"] == 0).all():
        header["QUALITY"] = 0
        del data["quality"]

    if data["grouping"] is None or (data["grouping"] == 1).all():
        header["GROUPING"] = 0
        del data["grouping"]

    # Default to using the STAT_ERR column if set. This is only
    # changed if the user has not set the POISSERR keyword: this
    # keyword is likely to be set for data that has been read in from
    # a file.
    #
    if "POISSERR" not in header:
        header["POISSERR"] = data["stat_err"] is None

    # We are not going to match OGIP standard if there's no data...
    #
    # It's also not clear how to handle the case when the channel
    # range is larger than the channel column. At present we rely in
    # the header being set, which is not ideal. There is also the
    # question of whether we should change all header values if
    # any are missing, or do it on a keyword-by-keyword basis.
    #
    # The assumption here is that "channel" is the first keyword
    # added to the data dictionary.
    #
    if data["channel"] is not None:
        tlmin = data["channel"][0]
        tlmax = data["channel"][-1]

        if "TLMIN1" not in header:
            header["TLMIN1"] = tlmin

        if "TLMAX1" not in header:
            header["TLMAX1"] = tlmax

        if "DETCHANS" not in header:
            header["DETCHANS"] = tlmax - tlmin + 1

    data = {k.upper(): v for (k, v) in data.items() if v is not None}

    # Enforce the column types:
    #   CHANNEL:  Int2 or Int4
    #   COUNTS:   Int2, Int4, or Real4
    #   GROUPING: Int2
    #   QUALITY:  Int2
    #
    # Rather than try to work out whether to use Int2 or Int4
    # just use Int4.
    #
    def convert(column, dtype):
        try:
            vals = data[column]
        except KeyError:
            return

        # assume vals is a numpy array
        if vals.dtype == dtype:
            return

        # Do we warn if we are doing unit conversion? For now
        # we don't.
        #
        data[column] = vals.astype(dtype)

    convert("CHANNEL", numpy.int32)
    convert("GROUPING", numpy.int16)
    convert("QUALITY", numpy.int16)

    # COUNTS has to deal with integer or floating-point.
    #
    try:
        vals = data["COUNTS"]
        if numpy.issubdtype(vals.dtype, numpy.integer):
            vals = vals.astype(numpy.int32)
        elif numpy.issubdtype(vals.dtype, numpy.floating):
            vals = vals.astype(numpy.float32)
        else:
            raise DataErr("ogip-error", "PHA dataset",
                          dataset.name,
                          "contains an unsupported COUNTS column")

        data["COUNTS"] = vals

    except KeyError:
        pass

    return data, header


def _pack_arf(dataset):
    """Extract FITS column and header information.

    There is currently no support for Type II ARF files.

    Notes
    -----
    The `ARF Data Extension header page
    <https://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/docs/memos/cal_gen_92_002/cal_gen_92_002.html>`_
    lists the following keywords as either required or
    we-really-want-them:

        EXTNAME = 'SPECRESP'
        TELESCOP - the "telescope" (ie mission/satellite name).
        INSTRUME - the instrument/detector.
        FILTER - the instrument filter in use (if any)
        HDUCLASS = 'OGIP' - file format is OGIP standard.
        HDUCLAS1 = 'RESPONSE' - extension contains response data.
        HDUCLAS2 = 'SPECRESP' - extension contains an ARF.
        HDUVERS = '1.1.0' - version of the file format.

    We do not add the ARFVERSN, HDUVERS1, or HDUVERS2 keywords which
    are marked as obsolete.

    """

    # The UI layer wraps up a DataARF into ARF1D quite often, so
    # support both types as input.
    #
    from sherpa.astro.instrument import ARF1D
    if not isinstance(dataset, (DataARF, ARF1D)):
        raise IOErr("data set is not an ARF")

    # Check we have data. Should we allow missing columns?
    #
    for col in ["energ_lo", "energ_hi", "specresp"]:
        if getattr(dataset, col) is None:
            raise ArgumentErr("bad", "ARF",
                              f"{col.upper()} column is missing")

    # The default keywords; these will be over-ridden by
    # anything set by the input.
    #
    default_header = {
        "EXTNAME": "SPECRESP",
        "HDUCLASS": "OGIP",
        "HDUCLAS1": "RESPONSE",
        "HDUCLAS2": "SPECRESP",
        "HDUVERS": "1.1.0",
        "TELESCOP": "none",
        "INSTRUME": "none",
        "FILTER": "none",
    }

    # Header Keys
    header = dataset.header

    # Merge the keywords
    #
    header = default_header | header

    # The exposure time is not an OGIP-mandated value but
    # is used by CIAO, so copy it across if set.
    #
    if dataset.exposure is not None:
        header["EXPOSURE"] = dataset.exposure

    # The column ordering for the output file is determined by the
    # order the keys are added to the data dict. Ensure the
    # data type meets the FITS standard (Real4).
    #
    data = {}
    data["ENERG_LO"] = dataset.energ_lo.astype(numpy.float32)
    data["ENERG_HI"] = dataset.energ_hi.astype(numpy.float32)
    data["SPECRESP"] = dataset.specresp.astype(numpy.float32)

    # Chandra files can have BIN_LO/HI values, so copy
    # across if both set.
    #
    blo = dataset.bin_lo
    bhi = dataset.bin_hi
    if blo is not None and bhi is not None:
        data["BIN_LO"] = blo
        data["BIN_HI"] = bhi

    return data, header


def _make_int_array(rows, ncols):
    """Convert a list of rows into a 2D array of "width" ncols.

    The conversion is to a type determined by the maximum value in
    rows (it selects between 2-byte and 4-byte integers).

    Parameters
    ----------
    rows : list of 1D arrays
        The values to convert. Expected to be integers (>= 0).
    ncols : int
        The size of each row in the output. There must be no row
        with more elements.

    Returns
    -------
    out : ndarray of size (nrows, ncols)

    """

    nrows = len(rows)
    maxval = 0
    for row in rows:
        if len(row) == 0:
            continue

        maxval = max(maxval, row.max())

    dtype = numpy.int32 if maxval > 32767 else numpy.int16
    out = numpy.zeros((nrows, ncols), dtype=dtype)
    for idx, row in enumerate(rows):
        if len(row) == 0:
            continue

        out[idx, 0:len(row)] = row

    return out


def _make_float32_array(rows, ncols):
    """Convert a list of rows into a 2D array of "width" ncols.

    The output has type numpy.float32.

    Parameters
    ----------
    rows : list of 1D arrays
        The values to convert. Expected to have type float32.
    ncols : int
        The size of each row in the output. There must be no row
        with more elements.

    Returns
    -------
    out : ndarray of size (nrows, ncols)

    """

    nrows = len(rows)
    out = numpy.zeros((nrows, ncols), dtype=numpy.float32)
    for idx, row in enumerate(rows):
        out[idx, 0:len(row)] = row

    return out


def _make_int_vlf(rows):
    """Convert a list of rows into a VLF.

    The conversion is to a type determined by the maximum value in
    rows (it selects between 2-byte and 4-byte integers).

    Parameters
    ----------
    rows : list of 1D arrays
        The values to convert. Expected to be integers (>= 0).

    Returns
    -------
    out : ndarray of dtype object

    """

    nrows = len(rows)
    maxval = 0
    for row in rows:
        if len(row) == 0:
            continue

        maxval = max(maxval, row.max())

    dtype = numpy.int32 if maxval > 32767 else numpy.int16
    out = []
    for row in rows:
        out.append(numpy.asarray(row, dtype=dtype))

    return numpy.asarray(out, dtype=object)


def _reconstruct_rmf(rmf):
    """Recreate the structure needed to write out as a FITS file.

    This does not guarantee to create byte-identical data in a round
    trip, but it should create equivalent data (e.g. the choice of
    whether a column should be a Variable Length Field may differ, as
    can the data types).

    Parameters
    ----------
    rmf : DataRMF or RMF1D instance

    Returns
    -------
    out : dict
        The re-constructed data and header values.

    Notes
    -----
    The F_CHAN, N_CHAN, and MATRIX columns are stored as either
      - 1D arrays (unlikely for MATRIX); N_GRP = 1 for all rows
      - 2D arrays when N_GRP is a constant for all rows
      - 2D arrays when N_GRP <= 4 (so some rows will have 0's in
        when N_GRP for that row is less than the max N_GRP)
      - 2D array with dtype=object indicates a VLF (each row
        should be the correct type though)

    """

    n_grp = []
    f_chan = []
    n_chan = []
    matrix= []

    # Used to reconstruct the original data
    idx = 0
    start = 0

    # Header keyword
    numelt = 0

    # How big is the matrix?
    matrix_size = set()

    for ng in rmf.n_grp:
        n_grp.append(ng)

        f_chan.append([])
        n_chan.append([])
        matrix.append([])

        # Short-cut when no data
        if ng == 0:
            matrix_size.add(0)

            # Convert from [] to numpy empty list
            f_chan[-1] = numpy.asarray([], dtype=numpy.int32)
            n_chan[-1] = numpy.asarray([], dtype=numpy.int32)
            matrix[-1] = numpy.asarray([], dtype=numpy.float32)
            continue

        # Grab the next ng elements from rmf.f_chan/n_chan
        # and the corresponding rmf.matrix elements. Fortunately
        # we can ignore F_CHAN when extracting data from matrix.
        #
        for _ in range(ng):
            # ensure this is an integer and not a floating-point number
            # which can happen when rmf.n_chan is stored as Unt64.
            #
            end = start + rmf.n_chan[idx].astype(numpy.int32)
            mdata = rmf.matrix[start:end]

            f_chan[-1].append(rmf.f_chan[idx])
            n_chan[-1].append(rmf.n_chan[idx])
            matrix[-1].extend(mdata)

            idx += 1
            start = end

        # Ensure F_CHAN/N_CHAN is either 2- or 4-byte integer by
        # converting to 4-byte integer here, which can later be
        # downcast.
        #
        f_chan[-1] = numpy.asarray(f_chan[-1], dtype=numpy.int32)
        n_chan[-1] = numpy.asarray(n_chan[-1], dtype=numpy.int32)

        # Ensure the matrix is Real-4
        matrix[-1] = numpy.asarray(matrix[-1], dtype=numpy.float32)
        matrix_size.add(matrix[-1].size)

        numelt += sum(n_chan[-1])

    # N_GRP should be 2-byte integer.
    #
    n_grp = numpy.asarray(n_grp, dtype=numpy.int16)
    numgrp = n_grp.sum()

    # Can we convert F_CHAN/N_CHAN to fixed-length if either:
    #  - N_GRP is the same for all rows
    #  - max(N_GRP) < 4
    #
    if len(set(n_grp)) == 1 or n_grp.max() < 4:
        ny = n_grp.max()
        f_chan = _make_int_array(f_chan, ny)
        n_chan = _make_int_array(n_chan, ny)
    else:
        f_chan = _make_int_vlf(f_chan)
        n_chan = _make_int_vlf(n_chan)

    # We can convert the matrix to fixed size if each row in matrix
    # has the same size.
    #
    if len(matrix_size) == 1:
        ny = matrix_size.pop()
        matrix = _make_float32_array(matrix, ny)
    else:
        matrix = numpy.asarray(matrix, dtype=object)

    return {"N_GRP": n_grp,
            "F_CHAN": f_chan,
            "N_CHAN": n_chan,
            "MATRIX": matrix,
            "NUMGRP": numgrp,
            "NUMELT": numelt}


def _pack_rmf(dataset):
    """Extract FITS column and header information.

    Unlike the other pack routines this returns data for
    multiple blocks. At present this ignores the ORDER column
    in the MATRIX block.

    Notes
    -----
    The `RMF Data Extension header page
    <https://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/docs/memos/cal_gen_92_002/cal_gen_92_002.html>`_
    lists the following keywords as either required or
    we-really-want-them. First for the MATRIX block:

        EXTNAME = 'MATRIX' or 'SPECRESP MATRIX'
        TELESCOP - the "telescope" (ie mission/satellite name).
        INSTRUME - the instrument/detector.
        FILTER - the instrument filter in use (if any)
        CHANTYPE - PI or PHA
        DETCHANS - the total number of raw detector PHA channels
        HDUCLASS = 'OGIP' - file format is OGIP standard.
        HDUCLAS1 = 'RESPONSE' - extension contains response data.
        HDUCLAS2 = 'RSP_MATRIX' - extension contains a response matrix.
        HDUVERS = '1.3.0' - version of the file format.
        TLMIN# - the first channel in the response.

    These are optional but mechanical so can be added:

        NUMGRP - sum(N_GRP)
        NUMELT - sum(N_CHAN)

    These are optional:

        LO_THRES - minimum probability threshold
        HDUCLAS3 - 'REDIST', 'DETECTOR', 'FULL'

    For the EBOUNDS extension we have:

        EXTNAME  = 'EBOUNDS'
        TELESCOP
        INSTRUME
        FILTER
        CHANTYPE
        DETCHANS
        HDUCLASS = 'OGIP'
        HDUCLAS1 = 'RESPONSE'
        HDUCLAS2 = 'EBOUNDS'
        HDUVERS = '1.2.0'

    We do not add the RMFVERSN, HDUVERS1, or HDUVERS2 keywords which
    are marked as obsolete.

    """

    # The UI layer wraps up a DataRMF into RMF1D quite often, so
    # support both types as input.
    #
    from sherpa.astro.instrument import RMF1D
    if not isinstance(dataset, (DataRMF, RMF1D)):
        raise IOErr("data set is not a RMF")

    rmfdata = _reconstruct_rmf(dataset)

    # The default keywords; these will be over-ridden by
    # anything set by the input.
    #
    default_matrix_header = {
        "EXTNAME": "MATRIX",
        "HDUCLASS": "OGIP",
        "HDUCLAS1": "RESPONSE",
        "HDUCLAS2": "RSP_MATRIX",
        "HDUVERS": "1.3.0",
        "TELESCOP": "none",
        "INSTRUME": "none",
        "FILTER": "none",
        "CHANTYPE": "PI",
        "DETCHANS": "none",
        "NUMGRP": 0,
        "NUMELT": 0
    }

    ebounds_header = {
        "EXTNAME": "EBOUNDS",
        "HDUCLASS": "OGIP",
        "HDUCLAS1": "RESPONSE",
        "HDUCLAS2": "EBOUNDS",
        "HDUVERS": "1.2.0",
        "TELESCOP": "none",
        "INSTRUME": "none",
        "FILTER": "none",
        "CHANTYPE": "PI",
        "DETCHANS": "none"
    }

    # Header Keys
    header = dataset.header

    # Merge the keywords (at least for the MATRIX block).
    #
    matrix_header = default_matrix_header | header

    matrix_header["NUMGRP"] = rmfdata["NUMGRP"]
    matrix_header["NUMELT"] = rmfdata["NUMELT"]
    matrix_header["DETCHANS"] = dataset.detchans

    # Copy values over.
    #
    for copykey in ["TELESCOP", "INSTRUME", "FILTER", "CHANTYPE",
                    "DETCHANS"]:
        ebounds_header[copykey] = matrix_header[copykey]

    # The column ordering for the output file is determined by the
    # order the keys are added to the data dict.
    #
    # To allow the backend convert to Variable-Length fields, we
    # have F_CHAN/N_CHAN/MATRIX either be a 2D ndarray (so fixed
    # output) OR a list of rows (use VLF). It's not ideal: we could
    # wrap up in a local VLF type just to indicate this to the
    # backend.
    #
    matrix_data = {
        "ENERG_LO": dataset.energ_lo,
        "ENERG_HI": dataset.energ_hi,
        "N_GRP": rmfdata["N_GRP"],
        "F_CHAN": rmfdata["F_CHAN"],
        "N_CHAN": rmfdata["N_CHAN"],
        "MATRIX": rmfdata["MATRIX"],
        "OFFSET": dataset.offset  # copy over this value
    }

    # TODO: is this correct?
    nchan = dataset.offset + dataset.detchans - 1
    dchan = numpy.int32 if nchan > 32767 else numpy.int16
    ebounds_data = {
        "CHANNEL": numpy.arange(dataset.offset, nchan + 1, dtype=dchan),
        "E_MIN": dataset.e_min.astype(numpy.float32),
        "E_MAX": dataset.e_max.astype(numpy.float32)
        }

    return [(matrix_data, matrix_header),
            (ebounds_data, ebounds_header)]


def write_arrays(filename, args, fields=None, ascii=True, clobber=False):
    """Write out a collection of arrays.

    Parameters
    ----------
    filename : str
       The name of the file.
    args
       The data to write out.
    fields : None or list of str, optional
       The names to use for each column. If ``None`` then the names
       default to `col1` ... `colN`.
    ascii : bool, optional
       If `True` use an ASCII format, otherwise a binary format.
    clobber : bool, optional
       If `True` then the output file will be over-written if it
       already exists, otherwise an error is raised.

    See Also
    --------
    read_arrays

    """
    backend.set_arrays(filename, args, fields, ascii=ascii, clobber=clobber)


def write_table(filename, dataset, ascii=True, clobber=False):
    """Write out a table.

    Parameters
    ----------
    filename : str
       The name of the file.
    dataset
       The data to write out.
    ascii : bool, optional
       If `True` use an ASCII format, otherwise a binary format.
    clobber : bool, optional
       If `True` then the output file will be over-written if it
       already exists, otherwise an error is raised.

    See Also
    --------
    read_table

    """
    data = _pack_table(dataset)
    names = list(data.keys())
    backend.set_table_data(filename, data, names, ascii=ascii, clobber=clobber)


def write_image(filename, dataset, ascii=True, clobber=False):
    """Write out an image.

    Parameters
    ----------
    filename : str
       The name of the file.
    dataset
       The data to write out.
    ascii : bool, optional
       If `True` use an ASCII format, otherwise a binary format.
    clobber : bool, optional
       If `True` then the output file will be over-written if it
       already exists, otherwise an error is raised.

    See Also
    --------
    read_image

    """
    data, hdr = _pack_image(dataset)
    backend.set_image_data(filename, data, hdr, ascii=ascii, clobber=clobber)


def write_pha(filename, dataset, ascii=True, clobber=False):
    """Write out a PHA dataset.

    Parameters
    ----------
    filename : str
       The name of the file.
    dataset
       The data to write out.
    ascii : bool, optional
       If `True` use an ASCII format, otherwise a binary format.
    clobber : bool, optional
       If `True` then the output file will be over-written if it
       already exists, otherwise an error is raised.

    See Also
    --------
    read_pha

    """
    data, hdr = _pack_pha(dataset)
    col_names = list(data.keys())
    backend.set_pha_data(filename, data, col_names, header=hdr,
                         ascii=ascii, clobber=clobber)


def write_arf(filename, dataset, ascii=True, clobber=False):
    """Write out an ARF.

    This does not handle Type II files.

    .. versionadded:: 4.16.0

    Parameters
    ----------
    filename : str
       The name of the file.
    dataset
       The data to write out.
    ascii : bool, optional
       If `True` use an ASCII format, otherwise a binary format.
    clobber : bool, optional
       If `True` then the output file will be over-written if it
       already exists, otherwise an error is raised.

    See Also
    --------
    read_arf

    """
    data, hdr = _pack_arf(dataset)
    names = list(data.keys())
    backend.set_arf_data(filename, data, names, header=hdr,
                         ascii=ascii, clobber=clobber)


def write_rmf(filename, dataset, clobber=False):
    """Write out a RMF.

    .. versionadded:: 4.16.0

    Parameters
    ----------
    filename : str
       The name of the file.
    dataset
       The data to write out.
    clobber : bool, optional
       If `True` then the output file will be over-written if it
       already exists, otherwise an error is raised.

    See Also
    --------
    read_rmf

    """

    blocks = _pack_rmf(dataset)
    backend.set_rmf_data(filename, blocks, clobber=clobber)


def pack_table(dataset):
    """Convert a Sherpa data object into an I/O item (tabular).

    Parameters
    ----------
    dataset : a sherpa.data.Data1D derived object

    Returns
    -------
    obj
       An object representing the data, the format of which depends
       on the I/O backend.

    See Also
    --------
    pack_image, pack_pha

    Examples
    --------

    >>> d = sherpa.data.Data1D('tmp', [1, 2, 3], [4, 10, 2])
    >>> tbl = pack_table(d)

    """
    data = _pack_table(dataset)
    names = list(data.keys())
    return backend.set_table_data('', data, names, packup=True)


def pack_image(dataset):
    """Convert a Sherpa data object into an I/O item (image).

    Parameters
    ----------
    dataset : a sherpa.data.Data2D derived object

    Returns
    -------
    obj
       An object representing the data, the format of which depends
       on the I/O backend.

    See Also
    --------
    pack_image, pack_pha

    Examples
    --------

    >>> y, x = np.mgrid[:10, :5]
    >>> z = (x-2)**2 + (y-2)**3
    >>> d = sherpa.data.Data2D('img', x.flatten(), y.flatten(),
                               z.flatten(), shape=z.shape)
    >>> img = pack_image(d)

    """
    data, hdr = _pack_image(dataset)
    return backend.set_image_data('', data, hdr, packup=True)


def pack_pha(dataset):
    """Convert a Sherpa PHA data object into an I/O item (tabular).

    Parameters
    ----------
    dataset : a sherpa.astro.data.DataPHA derived object

    Returns
    -------
    obj
       An object representing the data, the format of which depends
       on the I/O backend.

    See Also
    --------
    pack_image, pack_table

    """
    data, hdr = _pack_pha(dataset)
    col_names = list(data.keys())
    return backend.set_pha_data('', data, col_names, header=hdr,
                                packup=True)


def read_table_blocks(arg, make_copy=False):
    """Return the HDU elements (columns and header) from a FITS table.

    Parameters
    ----------
    arg
       The data file, which can be the name of the file or an object
       representing the opened file (the type of this depends on the I/O
       backend in use).
    make_copy : bool, optional
       This argument is currently unused.

    Returns
    -------
    filename, cols, hdr : str, dict, dict
       The name of the file, the column data, and the header data
       from the HDUs in the file. The keys of the dictionaries are the
       block name and the values are dictionaries, with the keys
       being the column or header name.

    """

    return backend.read_table_blocks(arg, make_copy=make_copy)
