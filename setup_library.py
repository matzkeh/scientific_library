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
Mark TVB-Simulator-Library as a Python import.
Mention dependencies for this package.
"""

import setuptools
import shutil


LIBRARY_VERSION = "1.0"

TVB_TEAM = "Stuart Knock, Marmaduke Woodman, Paula Sanz Leon"
CONTACT_EMAIL = "tvb.admin@thevirtualbrain.org"

TVB_INSTALL_REQUIREMENTS = ["networkx", "nibabel", "numpy", "numexpr", "scikit-learn", "scipy"]


setuptools.setup( name = 'tvb',
                  version = LIBRARY_VERSION,
                  packages = setuptools.find_packages(),
                  license = 'Not decided yet',
                  author = TVB_TEAM,
                  author_email = CONTACT_EMAIL,
                  include_package_data = True,
                  install_requires = TVB_INSTALL_REQUIREMENTS)
## Cleanup after EGG install.
shutil.rmtree('tvb.egg-info', True)


 