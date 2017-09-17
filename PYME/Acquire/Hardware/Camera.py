#!/usr/bin/python

###############
# Camera.py
#
# Created: 12 September 2017
#
# Based on: AndorZyla.py, AndorIXon.py
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

import ctypes

try:
    import Queue
except ImportError:
    import queue as Queue

from threading import Lock

from PYME.IO import MetaDataHandler


class Camera(object):

    # Acquisition modes
    MODE_SINGLE_SHOT = 0
    MODE_CONTINUOUS = 1

    def __init__(self, camNum, *args, **kwargs):
        """
        Create a camera object. This gets called from the PYMEAcquire init
        script, which is custom for any given microscope and can take
        whatever arguments are needed for a given camera.

        .. note:: The one stipulation is that the Camera should register itself
                  as providing metadata.

        Parameters
        ----------
        camNum:
            Camera object number to initialize.
        args :
            Optional arguments, usually instantiated in inherited camera.
        kwargs :
            Optional dictionary of arguments, usually instantiated in
            inherited camera.

        Returns
        -------
        Camera
            A camera object.
        """
        self.camNum = camNum  # Must associate Camera object with a UID

        # Default into continuous acquisition mode
        self.CycleMode = self.MODE_CONTINUOUS

        self._temp = 0  # Default camera temperature (Celsius)
        self._frameRate = 0

        # Camera lock
        self.camLock = Lock()

        # Camera info
        self.SerialNumber = ""
        self.CameraModel = ""

        self.buffersToQueue = Queue.Queue()
        self.queuedBuffers = Queue.Queue()
        self.fullBuffers = Queue.Queue()

        self.nQueued = 0
        self.nFull = 0

        self.nBuffers = 100
        self.defBuffers = 100

        self.active = True  # Should the camera write its metadata?

        # Register as a provider of metadata (record camera settings)
        # this is important so that the camera settings get recorded
        MetaDataHandler.provideStartMetadata.append(
            self.GenStartMetadata
            )

    def Init(self):
        """
        Optional intialization function. Also called from the init script.
        Not really part of 'specification'

        Returns
        -------
        None
        """
        pass

    def StartExposure(self):
        """
        Starts an acquisition.

        Returns
        -------
        int
            Success (0) or failure (-1) of initialization.
        """

        return 0

    def StopAq(self):
        """
        Stops acquiring.

        Returns
        -------
        None
        """
        pass

    def GenStartMetadata(self, mdh):
        """
        Create Camera metadata. This ensures the Camera's settings get
        recorded.

        Parameters
        ----------
        mdh : MetaDataHandler
            MetaDataHandler object for Camera.

        Returns
        -------
        None
        """

        if self.active:
            # Set Camera object metadata here with calls to mdh.setEntry

            # Personal identification
            mdh.setEntry('Camera.Name', 'Andor Neo')
            mdh.setEntry('Camera.Model', self.GetModel())
            mdh.setEntry('Camera.SerialNumber', self.GetSerialNumber())

            # Time
            mdh.setEntry('Camera.IntegrationTime', self.GetIntegTime())
            mdh.setEntry('Camera.CycleTime', self.GetCycleTime())

            # Gain
            mdh.setEntry('Camera.EMGain', self.GetEMGain())
            mdh.setEntry('Camera.TrueEMGain', self.GetTrueEMGain())

            # Noise
            mdh.setEntry('Camera.ReadNoise', self.GetReadNoise())
            mdh.setEntry('Camera.NoiseFactor', self.GetNoiseFactor())

            # QE
            mdh.setEntry('Camera.ElectronsPerCount', self.GetElectrPerCount())

            # Temp
            mdh.setEntry('Camera.StartCCDTemp', self.GetCCDTemp())

            # Chip size
            mdh.setEntry('Camera.SensorWidth', self.GetCCDWidth())
            mdh.setEntry('Camera.SensorHeight', self.GetCCDHeight())

            # FOV
            mdh.setEntry('Camera.ROIPosX', self.GetROIX1())
            mdh.setEntry('Camera.ROIPosY', self.GetROIY1())
            mdh.setEntry('Camera.ROIWidth',
                         self.GetROIX2() - self.GetROIX1())
            mdh.setEntry('Camera.ROIHeight',
                         self.GetROIY2() - self.GetROIY1())

    @property
    def contMode(self):
        """ Return whether the camera is running in continuous mode or not.
        This property (was previously a class member
        variable) is required to allow the calling code to determine whether it
        needs to restart exposures after processing
        the previous one."""
        return self.GetAcquisitionMode() == self.MODE_CONTINUOUS

    def ExpReady(self):
        """
        Checks whether there are any frames waiting in the camera buffers

        Returns
        -------
        bool
            True if there are frames waiting

        """

        return not self.fullBuffers.empty()

    def CamReady(*args):
        """
        Returns true if the camera is ready (initialized) not really used for
        anything, but might still be checked.

        Returns
        -------
        bool
            Is the camera ready?
        """

        return True

    def ExtractColor(self, chSlice, mode):
        """
        Pulls the oldest frame from the camera buffer and copies it into
        memory we provide. Note that the function signature and parameters are
        a legacy of very old code written for a colour camera with a bayer mask.

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

    def GetModel(self):
        """
        Get the model name of the hardware represented by Camera object.

        Returns
        -------
        str
            Hardware model name of Camera object
        """
        if isinstance(self.CameraModel, str):
            return self.CameraModel
        raise TypeError("Camera model must be stored as a string.")

    def GetSerialNumber(self):
        """
        Get the serial number of the hardware represented by Camera object.

        Returns
        -------
        str
            Hardware serial number of Camera object
        """
        if isinstance(self.SerialNumber, str):
            return self.SerialNumber
        raise TypeError("Serial number must be stored as a string.")

    def GetIntegTime(self):
        """
        Get Camera object integration time.

        Returns
        -------
        float
            The exposure time in s

        See Also
        --------
        SetIntegTime
        """
        pass

    def GetCycleTime(self):
        """
        Get camera cycle time (1/fps) in seconds (float)

        Returns
        -------
        float
            Camera cycle time (seconds)
        """
        if self._frameRate > 0:
            return 1.0/self._frameRate

        return 0.0

    def GetReadNoise(self):
        pass

    def GetNoiseFactor(self):
        pass

    def GetElectrPerCount(self):
        pass

    def GetCCDTemp(self):
        """
        Gets the Camera object's sensor temperature.

        Returns
        -------
        float
            The sensor's temperature in degrees Celsius
        """

        return self._temp

    def GetCCDWidth(self):
        """
        Gets the Camera object's sensor width.

        Returns
        -------
        int
            The sensor width in pixels

        """
        pass

    def GetCCDHeight(self):
        """
        Gets the Camera object's sensor height.

        Returns
        -------
        int
            The sensor height in pixels

        """
        pass

    def GetPicWidth(self):
        """
        Returns the width (in pixels) of the currently selected ROI.

        Returns
        -------
        int
            Width of ROI (pixels)
        """
        pass

    def GetPicHeight(self):
        """
        Returns the height (in pixels) of the currently selected ROI.

        Returns
        -------
        int
            Height of ROI (pixels)
        """
        pass

    def SetROI(self, x1, y1, x2, y2):
        """
        Set the ROI via coordinates (as opposed to via an index).

        FIXME: this is somewhat inconsistent over cameras, with some
        cameras using 1-based and some cameras using 0-based indexing.
        Ideally we would convert them all to using zero based indexing and be
        consistent with numpy.

        Most use 1 based (as it's a thin wrapper around the camera API), but we
        should really do something saner here.

        Parameters
        ----------
        x1 : int
            Left x-coordinate
        y1 : int
            Top y-coordinate
        x2 : int
            Right x-coordinate
        y2 : int
            Bottom y-coordinate

        Returns
        -------
        None

        See Also
        --------
        SetROIIndex
        """

    def GetROIX1(self):
        """
        Gets the position of the leftmost pixel of the ROI.

        Returns
        -------
        int
            Left x-coordinate of ROI.
        """
        pass

    def GetROIX2(self):
        """
        Gets the position of the rightmost pixel of the ROI.

        Returns
        -------
        int
            Right x-coordinate of ROI.
        """
        pass

    def GetROIY1(self):
        """
        Gets the position of the top row of the ROI.

        Returns
        -------
        int
            Top y-coordinate of ROI.
        """
        pass

    def GetROIX2(self):
        """
        Gets the position of the bottom row of the ROI.

        Returns
        -------
        int
            Bottom y-coordinate of ROI.
        """
        pass

    def GetEMGain(self):
        """
        Return electromagnetic gain of Camera object.

        Returns
        -------
        float
            Camera object gain

        See Also
        ----------
        GetTrueEMGain, SetEMGain
        """
        return 1

    def GetTrueEMGain(self, true_gain=False):
        """
        Return true electromagnetic gain of Camera object.

        Returns
        -------
        float
            Camera object adjusted true gain.

        See Also
        ----------
        GetEMGain
        """
        pass

    def GetAcquisitionMode(self):
        """
        Get the Camera object readout mode.

        Returns
        -------
        int
            One of self.MODE_CONTINUOUS, self.MODE_SINGLE_SHOT

        See Also
        --------
        SetAcquisitionMode
        """
        if isinstance(self.CycleMode, int) or isinstance(self.CycleMode, bool):
            return self.CycleMode
        raise TypeError("Cycle mode must be one of MODE_CONTINUOUS, "
                        "MODE_SINGLE_SHOT.")

    def SetAcquisitionMode(self, mode):
        """
        Set the readout mode of the Camera object. PYME currently supports two
        modes: single shot, where the camera takes one image, and then a new
        exposure has to be manually triggered, or continuous / free running,
        where the camera runs as fast as it can until we tell it to stop.

        Parameters
        ----------
        mode : int
            One of self.MODE_CONTINUOUS, self.MODE_SINGLE_SHOT

        Returns
        -------
        None

        See Also
        --------
        GetAcquisitionMode
        """

        if isinstance(mode, int) or isinstance(mode, bool):
            self.CycleMode = mode
        raise TypeError("Mode must be one of One of MODE_CONTINUOUS, "
                        "MODE_SINGLE_SHOT")

    def SetActive(self, active=True):
        """
        Flag the Camera object as active (or inactive) to dictate whether or
        not it writes its metadata.

        Parameters
        ----------
        active : bool
            Write metadata?

        Returns
        -------
        None
        """

        if ~isinstance(active, bool):
            raise TypeError("Active must be set to True or False.")

        self.active = active

    def SetIntegTime(self, integration_time):
        """
        Sets the exposure time in s. Currently assumes that we will want to go
        as fast as possible at this exposure time and also sets the frame
        rate to match.

        Parameters
        ----------
        integration_time : float
            Exposure time in s.

        Returns
        -------
        None

        See Also
        --------
        GetIntegTime
        """

        pass

    def SetEMGain(self, gain):
        """
        Set the electromagnetic gain. For EMCCDs this is typically the
        uncalibrated, gain register setting. The calibrated gain is computed
        separately and saved in the metadata as RealEMGain.

        Parameters
        ----------
        gain : float
            EM gain of Camera object.

        Returns
        -------
        None

        See Also
        --------
        GetEMGain
        """
        pass

    def GetCCDTempSetPoint(self):
        """
        Get the target camera temperature. Only currently called in Ixon
        related code, but potentially generally useful.

        Returns
        -------
        float
            Target camera temperature (Celsius)
        """
        pass

    def SetCCDTemp(self, temp):
        """
        Set the target camera temperature.

        Parameters
        ----------
        temp : float
            The target camera temperature (Celsius)

        Returns
        -------
        None
        """
        pass

    def SetShutter(self, mode):
        """
        Set the camera shutter (if available).

        Parameters
        ----------
        mode : bool
            True (1) if open

        Returns
        -------
        None
        """
        pass

    def SetBaselineClamp(self, mode):
        """
        Set the camera baseline clamp (EMCCD). Only called from the Ixon
        settings panel, so not relevant for other cameras.

        Parameters
        ----------
        mode : int
            Clamp state

        Returns
        -------
        None
        """
        pass

    def GetFPS(self):
        """
        Get the camera frame rate in frames per second (float).

        Returns
        -------
        float
            Camera frame rate (frames per second)
        """
        return self._frameRate

    def GetNumImsBuffered(self):
        """
        Return the number of images in the buffer.

        Returns
        -------
        int
            Number of images in buffer
        """
        return self.nFull

    def GetBufferSize(self):
        """
        Return the total size of the buffer (in images).

        Returns
        -------
        int
            Number of images that can be stored in the buffer.
        """
        return self.nBuffers

    # Binning is not really supported in current software, making these commands
    # mostly superfluous. Being able to read out the binning (GetHorizBin,
    # GetVertBin) is however necessary and these should definitely be revisited
    def SetHorizBin(*args):
        raise Exception('Not implemented yet!!')

    def GetHorizBin(*args):
        return 0

    def GetHorzBinValue(*args):
        raise Exception('Not implemented yet!!')

    def SetVertBin(*args):
        raise Exception('Not implemented yet!!')

    def GetVertBin(*args):
        return 0

    def GetElectrTemp(*args):
        """
        Returns the temperature of the internal electronics. Legacy of PCO
        Sensicam support, which had separate sensors for CCD and electronics.
        Not actually used anywhere critical (might be recorded in metadata),
        can remove.

        Returns
        -------
        float
            Temperature of internal electronics (default is 25.0).

        """
        return 25.0

    def Shutdown(self):
        """
        Clean up the Camera object.

        Returns
        -------
        None
        """
        pass

    def __del__(self):
        self.Shutdown()
