#!/usr/bin/python

###############
# sCMOSCamera.py
#
# Created: 16 September 2017
# Author : Z Marin
#
# Based on: AndorZyla.py
#
# Copyright David Baddeley, 2012
# d.baddeley@auckland.ac.nz
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
################

import time

from threading import Thread
from fftw3f import create_aligned_array

from PYME.Acquire.Hardware.Camera import Camera


class sCMOSCamera(Camera):

    def __init__(self, camNum):
        # Default Camera object initializations
        Camera.__init__(self, camNum)

        self.doPoll = False
        self.pollLoopActive = False
        self.pollThread = Thread(target=self._pollLoop)
        self.pollThread.start()

    def InitBuffers(self):
        """
        Initialize camera buffers. A couple of the variables are too
        camera-specific for this to be in the general class.

        Returns
        -------
        None.
        """
        pass

    def _flush(self):
        """
        Flush all buffers (queuedBuffers, buffersToQueue, fullBuffers). Also
        need to flush camera buffers, which means this function must be
        overridden for each camera, with buffer flushing added.

        Usage
        -----
        class ASpecificCam(sCMOSCamera):
            ...
            def _flush(self):
                # Turn off camera polling
                self.doPoll = False

                # flush camera buffers
                [Code here]

                # flush local buffers
                sCMOSCamera._flush(self)

                # flush camera buffers again
                [Code here]

        Returns
        -------
        None
        """
        # purge our local queues
        while not self.queuedBuffers.empty():
            self.queuedBuffers.get()

        while not self.buffersToQueue.empty():
            self.buffersToQueue.get()

        self.nQueued = 0

        while not self.fullBuffers.empty():
            self.fullBuffers.get()

        self.nFull = 0

    def _queueBuffer(self, buf):
        """
        Put buffer into buffersToQueue.

        Parameters
        ----------
        buf : `~numpy.ndarray`
            Numpy array that is n-byte-aligned (usually 8-bit integer)

        Returns
        -------
        None
        """
        self.buffersToQueue.put(buf)

    def _queueBuffers(self):
        """
        Grab camera buffers and stash them in queuedBuffers, moving the data
        first through buffersToQueue. This function is too camera-specific
        for any general code in the class.
        nQueued += 1
        """
        pass

    def _pollBuffer(self):
        """
        Grabbed the queuedBuffers off the camera and stash them in fullBuffers.
        This function is too camera-specific for any general code in the class.
        nFull += 1
        """
        pass

    def _pollLoop(self):
        while self.pollLoopActive:
            self._queueBuffers()
            if self.doPoll: #only poll if an acquisition is running
                self._pollBuffer()
            else:
                time.sleep(.05)
            time.sleep(.0005)

    def ExtractColor(self, chSlice, mode):
        """
        Pulls the oldest frame from the camera buffer and copies it into
        memory we provide. Note that the function signature and parameters are
        a legacy of very old code written for a colour camera with a bayer mask.
        This function is too camera-specific for any general code in the class.

        Parameters
        ----------
        chSlice : `~numpy.ndarray`
            The array we want to put the data into
        mode : int
            Previously specified how to deal with the Bayer mask.

        Returns
        -------
        None
        """

        pass

    def SetBurst(self, burstSize):
        """
        Some support for burst mode on the Neo and Zyla. Is not called from
        the GUI, and can be considered experimental and non-essential.

        Parameters
        ----------
        burtSize : int
            Number of frames to acquire in burst mode.

        Returns
        -------
        None
        """
        pass

    def SetROIIndex(self, index):
        """
        Set the ROI via an index (as opposed to via coordinates). Legacy code
        for old Andor NEO cameras which only supported certain fixed ROIs.
        Should not be essential / can remove.

        Parameters
        ----------
        index : int
            Index of top left coordinate in image. Width/height automatically
            determined prior to function use by chopping image into ROIs of
            desired size.

        Returns
        -------
        None

        See Also
        --------
        SetROI
        """
        pass