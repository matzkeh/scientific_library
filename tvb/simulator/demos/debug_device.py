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
This demos how to go about debugging some device code. 
Rather, It is actually used for that, but could be helpful to others
eventually.

good
----

So far I've verified (on cpu) Euler & Euler stochastic w/ Gen 2D osc, 
WilsonCowan. JansenRit seems good with deterministic Euler, but diverges
numerically more quickyl with noise. Kuramoto seems fine as well.
ReducedFHN and ReducedHMR have more error, needs checking to see what the
source is.

The Heun integrators now appear to work as well as the Euler integrators.

Linear coupling is good, sigmoidal appears ok, difference & Kuramoto
are ok as well.

bad
---

The otherwise slow error creep is due to one or more of

- 64-bit vs 32-bit precision
- effects of order of operations on 
- history indexing off by one
- connectivity orientation/convention


ugly
----

HeunStoch doesn't like ReducedHMR, makes lots of NaaN.


.. moduleauthor:: marmaduke woodman <mw@eml.cc>

"""

import time
import itertools

from numpy import *

from tvb.simulator import lab
from tvb.simulator.backend import driver_conf
driver_conf.using_gpu = 0
from tvb.simulator.backend import driver
reload(driver)

sim = lab.simulator.Simulator(
    model = lab.models.Generic2dOscillator(),
    connectivity = lab.connectivity.Connectivity(speed=4.0),
    coupling = lab.coupling.Linear(a=1e-2),                                         # shape must match model..
    integrator = lab.integrators.HeunStochastic(dt=2**-5, noise=lab.noise.Additive(nsig=ones((2, 1, 1))*1e-2)),
    monitors = lab.monitors.Raw()
)

sim.configure()

# then build device handler and pack it iwht simulation
dh = driver.device_handler.init_like(sim)
dh.n_thr = 1
dh.fill_with(0, sim)


# run both with raw monitoring, compare output
simgen = sim(simulation_length=100)
cont = True

ys1,ys2 = [], []
while cont:

    # simulator output
    try:
        # history & indicies
        histidx = ((sim.current_step - 1 - sim.connectivity.idelays)%sim.horizon)[:4, :4].flat[:]*74 + r_[:4, :4, :4, :4]
        histval = [sim.history[(sim.current_step - 1 - sim.connectivity.idelays[10,j])%sim.horizon, 0, j, 0] for j in range(dh.n_node)]
        #print 'histidx', histidx
        #print 'hist[idx]', histval

        t1, y1 = next(simgen)[0]
        ys1.append(y1)
    except StopIteration:
        break


    #print 'state sim', sim.integrator.X[:, -1, 0]
    #print 'state dh ', dh.x.value.transpose((1, 0, 2))[:, -1, 0]


    # dh output
    driver.gen_noise_into(dh.ns, dh.inpr.value[0])
    dh()

    #print 'I sim', sim.coupling.ret[0, 10:15, 0]

    # compare dx
    #print 'dx1 sim', sim.integrator.dX[:, -1, 0]
    #print 'dx1 dh ', dh.dx1.value.flat[:]
    
    t2 = dh.i_step*dh.inpr.value[0]
    y2 = dh.x.value.reshape((dh.n_node, -1, dh.n_mode)).transpose((1, 0, 2))
    ys2.append(y2)

    if dh.i_step % 100 == 0:
        stmt = "%4.2f\t%4.2f\t%.3f"
        print stmt % (t1, t2, ((y1 - y2)**2).sum()/y1.ptp())

ys1 = array(ys1)
ys2 = array(ys2)

print ys1.flat[::450]
print ys2.flat[::450]

savez('debug.npz', ys1=ys1, ys2=ys2)

from matplotlib import pyplot as pl

pl.figure(2)
pl.clf()
pl.subplot(311), pl.imshow(ys1[:, 0, :, 0].T, aspect='auto', interpolation='nearest'), pl.colorbar()
pl.subplot(312), pl.imshow(ys2[:, 0, :, 0].T, aspect='auto', interpolation='nearest'), pl.colorbar()
pl.subplot(313), pl.imshow(((ys1 - ys2)/ys1.ptp())[:, 0, :, 0].T, aspect='auto', interpolation='nearest'), pl.colorbar()

pl.show()
