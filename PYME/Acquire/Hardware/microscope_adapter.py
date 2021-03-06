#!/usr/bin/python

##################
# Copyright David Miguel Susano Pinto, 2020
# david.pinto@bioch.ox.ac.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################

"""Adapters to the Python microscope package devices.

This module provides adapter classes to devices controlled with the
Python microscope package <https://pypi.org/project/microscope/>.
"""

import PYME.Acquire.Hardware.lasers


class MicroscopeLaser(PYME.Acquire.Hardware.lasers.Laser):
    """
    Adapter for Python microscope laser classes.

    Parameters
    ----------
        laser: an object, already initialized, implementing the
            `microscope.devices.LaserDevice` interface.
    """
    def __init__(self, laser, *args, **kwargs):
        # We can't call super() at the start because the parent class
        # may try to call self.TurnOn().
        self._laser = laser
        self.powerControlable = True
        self.MIN_POWER = self._laser.get_min_power_mw()
        self.MAX_POWER = self._laser.get_max_power_mw()
        super().__init__(*args, **kwargs)

    def IsOn(self):
        return self._laser.get_is_on()

    def TurnOn(self):
        self._laser.enable()

    def TurnOff(self):
        self._laser.disable()

    def SetPower(self, power):
        self._laser.set_power_mw(power)

    def GetPower(self):
        return self._laser.get_power_mw()
