#!/usr/bin/python

##################
# piecewiseMapping.py
#
# Copyright David Baddeley, 2009
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
##################

from numpy import *
import numpy as np
import sys
import six

def timeToFrames(t, events, mdh):
    cycTime = mdh.getEntry('Camera.CycleTime')
    startTime = mdh.getEntry('StartTime')

    #se = array([('0', 'start', startTime)], dtype=events.dtype)
    se = np.empty(1, dtype=events.dtype)
    se['EventName'] = 'start'
    se['EventDescr'] = '0'
    se['Time'] = startTime

    #sf = array([('%d' % iinfo(int32).max, 'end', startTime + 60*60*24*7)], dtype=events.dtype)
    sf = np.empty(1, dtype=events.dtype)
    sf['EventName'] = 'end'
    sf['EventDescr'] = '%d' % iinfo(int32).max
    sf['Time'] = startTime + 60*60*24*7

    #get events corresponding to aquisition starts
    startEvents = hstack((se, events[events['EventName'] == b'StartAq'], sf))

    #print startEvents

    sfr = array([int(e['EventDescr'].decode('ascii')) for e in startEvents])

    si = startEvents['Time'].searchsorted(t, side='right')
    
    #print t    
    #print((si, startEvents, sfr))
    
    #try:
    #    if len(si) > 1:
    #        si = si[-1]
    #except:
    #    pass
    
    #fr = np.zeros_like(t)
    
    
    fr = sfr[si-1] + ((t - startEvents['Time'][si-1]) / cycTime)
    
    if np.isscalar(fr):
        if si < len(sfr):
            return minimum(fr, sfr[si])
    else:
        M = (si < len(sfr))
        fr[M] = minimum(fr[M], sfr[si[M]]) 

        return fr

def framesToTime(fr, events, mdh):
    cycTime = mdh.getEntry('Camera.CycleTime')
    startTime = mdh.getEntry('StartTime')

    #se = array([('0', 'start', startTime)], dtype=events.dtype)
    se = np.empty(1, dtype=events.dtype)
    se['EventName'] = 'start'
    se['EventDescr'] = '0'
    se['Time'] = startTime

    #get events corresponding to aquisition starts
    startEvents = hstack((se, events[events['EventName'] == b'StartAq']))
    #print(events)
    #print(startEvents)

    sfr = array([int(e['EventDescr'].decode()) for e in startEvents])

    si = sfr.searchsorted(fr, side = 'right')
    return startEvents['Time'][si-1] + (fr - sfr[si-1]) * cycTime
    

class piecewiseMap:
    def __init__(self, y0, xvals, yvals, secsPerFrame=1, xIsSecs=True):
        self.y0 = y0

        if xIsSecs: #store in frame numbers
            self.xvals = xvals / secsPerFrame
        else:
            self.xvals = xvals
        self.yvals = yvals

        self.secsPerFrame = secsPerFrame
        self.xIsSecs = xIsSecs

    def __call__(self, xp, xpInFrames=True):
        xp = xp.astype('f') #fast to float in case we get passed an int
        yp = 0 * xp

        if not xpInFrames:
            xp = xp / self.secsPerFrame
        
#        y0 = self.y0
#        x0 = -inf
#
#        for x, y in zip(self.xvals, self.yvals):
#            yp += y0 * (xp >= x0) * (xp < x)
#            x0, y0 = x, y
#
#        x  = +inf
#        yp += y0 * (xp >= x0) * (xp < x)

        inds = self.xvals.searchsorted(xp, side='right')
        yp  = self.yvals[maximum(inds-1, 0)]
        yp[inds == 0] = self.y0

        return yp

def GeneratePMFromProtocolEvents(events, metadata, x0, y0, id='setPos', idPos = 1, dataPos=2):
    x = []
    y = []

    secsPerFrame = metadata.getEntry('Camera.CycleTime')

    for e in events[events['EventName'] == b'ProtocolTask']:
        #if e['EventName'] == eventName:
        ed = e['EventDescr'].decode('ascii').split(', ')
        if ed[idPos] == id:
            x.append(e['Time'])
            y.append(float(ed[dataPos]))
            
    x = array(x)
    y = array(y)
    
    I = np.argsort(x)
    
    x = x[I]
    y = y[I]

    return piecewiseMap(y0, timeToFrames(x, events, metadata), y, secsPerFrame, xIsSecs=False)


def GeneratePMFromEventList(events, metadata, x0, y0, eventName=b'ProtocolFocus', dataPos=1):
    x = []
    y = []

    secsPerFrame = metadata.getEntry('Camera.CycleTime')

    for e in events[events['EventName'] == eventName]:
        #if e['EventName'] == eventName:
        #print(e)
        x.append(e['Time'])
        y.append(float(e['EventDescr'].decode('ascii').split(', ')[dataPos]))
        
    x = array(x)
    y = array(y)
        
    I = np.argsort(x)
    
    x = x[I]
    y = y[I]

    #print array(x) - metadata.getEntry('StartTime'), timeToFrames(array(x), events, metadata)

    return piecewiseMap(y0, timeToFrames(x, events, metadata), y, secsPerFrame, xIsSecs=False)

def GenerateBacklashCorrPMFromEventList(events, metadata, x0, y0, eventName=b'ProtocolFocus', dataPos=1, backlash=0):
    x = []
    y = []

    secsPerFrame = metadata.getEntry('Camera.CycleTime')

    for e in events[events['EventName'] == eventName]:
        #if e['EventName'] == eventName:
        x.append(e['Time'])
        y.append(float(e['EventDescr'].decode('ascii').split(', ')[dataPos]))

    x = array(x)
    y = array(y)

    dy = diff(hstack(([y0], y)))

    for i in range(1, len(dy)):
        if dy[i] == 0:
            dy[i] = dy[i-1]

    y += backlash*(dy < 0)


    return piecewiseMap(y0, timeToFrames(x, events, metadata), y, secsPerFrame, xIsSecs=False)

