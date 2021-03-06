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
Framework methods for the Connectivity datatype.

.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
.. moduleauthor:: Stuart A. Knock <Stuart@tvb.invalid>
"""

import numpy
import tvb.datatypes.connectivity_data as connectivity_data

class ConnectivityFramework(connectivity_data.ConnectivityData):
    """ 
    This class exists to add framework methods and attributes to Connectivity.
    """
    
    __tablename__ = None
    

    def generate_new_connectivity(self, new_weights, interest_areas, storage_path):
        """
        Generate new Connectivity object based on current one, by changing
        weights (e.g. simulate leasion).
        """
        if isinstance(new_weights, str) or isinstance(new_weights, unicode):
            new_weights = eval(new_weights)
            interest_areas = eval(interest_areas)
        
        for i in range(len(new_weights)):
            for j in range(len(new_weights)):
                new_weights[i][j] = numpy.float(new_weights[i][j])
        for i in range(len(interest_areas)):
            interest_areas[i] = int(interest_areas[i]) 
                     
        final_weights = []
        for i in range(len(self.weights)):
            weight_line = []
            for j in range(len(self.weights)):
                if (interest_areas and i in interest_areas and j in interest_areas):
                    weight_line.append(new_weights[i][j])
                else:
                    weight_line.append(0)
            final_weights.append(weight_line)
        final_conn = (self.__class__)()
        final_conn.parent_connectivity = self.gid
        final_conn.storage_path = storage_path
        final_conn.nose_correction = self.nose_correction
        final_conn.weights = final_weights
        final_conn.centres = self.centres
        final_conn.region_labels = self.region_labels
        final_conn.orientations = self.orientations
        final_conn.cortical = self.cortical
        final_conn.hemispheres = self.hemispheres
        final_conn.areas = self.areas
        final_conn.tract_lengths = self.tract_lengths
        final_conn.saved_selection = interest_areas
        final_conn.subject = self.subject
        return final_conn


    @property
    def saved_selection_labels(self):
        """
        Taking the entity field saved_selection, convert indexes in that array
        into labels.
        """
        if self.saved_selection:
            idxs = [int(i) for i in self.saved_selection]
            result = ''
            for i in idxs:
                result += self.region_labels[i] + ','
            return result[:-1]
        else:
            return ''


    @staticmethod  
    def accepted_filters():
        filters = connectivity_data.ConnectivityData.accepted_filters()
        filters.update({'datatype_class._number_of_regions': {'type': 'int', 'display':'No of Regions',
                                                              'operations': ['==', '<', '>']}})
        return filters


