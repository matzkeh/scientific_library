# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and 
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2013, Baycrest Centre for Geriatric Care ("Baycrest")
#
# This program is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License version 2 as published by the Free
# Software Foundation. This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details. You should have received a copy of the GNU General 
# Public License along with this program; if not, you can download it here
# http://www.gnu.org/licenses/old-licenses/gpl-2.0
#
#

"""
The Data component of Connectivity datatype.

.. moduleauthor:: Stuart A. Knock <Stuart@tvb.invalid>
.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>

"""

import numpy
import tvb.basic.traits.types_basic as basic
import tvb.basic.traits.core as core
import tvb.basic.traits.data_readers as readers
import tvb.datatypes.volumes as volumes
import tvb.datatypes.arrays as arrays
from tvb.basic.traits.types_mapped import MappedType


class ConnectivityData(MappedType):
    """
    This class primarily exists to bundle the long range structural connectivity
    data into a single object. 
    """

    default = readers.File(folder_path = "connectivity/o52r00_irp2008")

    parcellation_mask = volumes.ParcellationMask(
        label="Parcellation mask (volume)", 
        required = False,
        doc="""A 3D volume mask defining the parcellation of the brain into
        distinct regions.""")#'B'

    region_labels = arrays.StringArray(
        label = "Region labels",
        console_default = default.read_data(file_name = "centres.txt.bz2", usecols = (0,), 
                                            dtype = "string", field = "region_labels"),
        doc = """Short strings, 'labels', for the regions represented by the
            connectivity matrix.""") #  'B' -- sort of 'C', index as string.

    weights = arrays.FloatArray(
        label = "Connection strengths",
        console_default = default.read_data(file_name = "weights.txt.bz2", field = "weights"),
        doc = """Matrix of values representing the strength of connections
                 between regions, arbitrary units.""") #  'B'

    unidirectional = basic.Integer(default=0, 
        required = False,
        doc="1, when the weights matrix is square and symmetric over the main diagonal, 0 when bi-directional matrix.")

    tract_lengths = arrays.FloatArray(
        label = "Tract lengths",
        console_default = default.read_data(file_name = "tract_lengths.txt.bz2", field = "tract_lengths"),
        doc = """The length of myelinated fibre tracts between regions. If
                 not provided Euclidean distance between region centres is used.""") #'SC'

    speed = arrays.FloatArray(
        label = "Conduction speed", 
        default = numpy.array([3.0]), file_storage = core.FILE_STORAGE_NONE,
        doc = """A single number or matrix of conduction speeds for the 
            myelinated fibre tracts between regions.""") 
        #  'B' -- FUTURE: calc/estimate from myelination.

    centres = arrays.PositionArray(
        label = "Region centres",
        console_default = default.read_data(file_name = "centres.txt.bz2", usecols = (1, 2, 3), field = "centres"),
        doc = "An array specifying the location of the centre of each region.")
        #  'C' -- calc is from parcellation_mask.

    cortical = arrays.BoolArray(
        label = "Cortical",
        console_default = default.read_data(file_name = "cortical.txt.bz2", dtype = numpy.bool, field = "cortical"),
        required = False,
        doc = """A boolean vector specifying whether or not a region is part of the cortex.""") # 'B'

    hemispheres = arrays.BoolArray(
        label = "Hemispheres (True for Right and False for Left Hemisphere",
        required = False,
        doc = """A boolean vector specifying whether or not a region is part of the right hemisphere""")

    orientations = arrays.OrientationArray(
        label = "Average region orientation",
        console_default = default.read_data(file_name = "average_orientations.txt.bz2", field = "orientations"),
        required = False,
        doc = """Unit vectors of the average orientation of the regions 
            represented in the connectivity matrix. NOTE: Unknown data should
            be zeros.""") #  'CS' -- 'C' assumes linked Cortex.

    areas = arrays.FloatArray(
        label = "Area of regions",
        console_default = default.read_data(file_name = "areas.txt.bz2", field = "areas"),
        required = False,
        doc = """Estimated area represented by the regions in the connectivity 
            matrix. NOTE: Unknown data should be zeros.""") 
        #  'CS' -- 'C' assumes linked Cortex.

    idelays = arrays.IndexArray(
        label="Conduction delay indices",
        required = False, file_storage = core.FILE_STORAGE_NONE,
        doc = "An array of time delays between regions in integration steps.") # 'C'

    delays = arrays.FloatArray(
        label = "Conduction delay",
        file_storage = core.FILE_STORAGE_NONE, required = False,
        doc = """Matrix of time delays between regions in physical units,
            setting conduction speed automatically combines with tract lengths
            to update this matrix, i.e. don't try and change it manually.""") #'C'

    number_of_regions = basic.Integer(
        label = "Number of regions",
        doc = """The number of regions represented in this Connectivity """)

    # ------------- FRAMEWORK ATTRIBUTES -----------------------------

    # Rotation if positions are not normalized.
    nose_correction = basic.JSONType(required = False)

    # Original Connectivity, from which current connectivity was edited.
    parent_connectivity = basic.String(required = False)

    # In case of edited Connectivity, this are the nodes left in interest area,
    # the rest were part of a lesion, so they were removed.
    saved_selection = basic.JSONType(required = False)


