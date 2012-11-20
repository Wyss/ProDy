# -*- coding: utf-8 -*-
# ProDy: A Python Package for Protein Dynamics Analysis
# 
# Copyright (C) 2010-2012 Ahmet Bakan
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""This module defines MSA analysis functions."""

__author__ = 'Ahmet Bakan'
__copyright__ = 'Copyright (C) 2010-2012 Ahmet Bakan'

from numpy import arange

from .analysis import *

__all__ = ['showShannonEntropy', 'showMutualInfo']


def showShannonEntropy(entropy, indices=None, *args, **kwargs):
    """Show a bar plot of Shannon *entropy* array.  :class:`MSA` instances 
    or Numpy character arrays storing sequence alignment are also accepted 
    as *entropy* argument, in which case :func:`.calcShannonEntropy` will 
    be used for calculations.  *indices* may be residue numbers, if **None**
    is given numbers starting from 1 will be used.
    
    Entropy is plotted using :func:`~matplotlib.pyplot.bar` function."""
    
    try:
        ndim = entropy.ndim
    except AttributeError:
        entropy = calcShannonEntropy(entropy)
        ndim = entropy.ndim

    if ndim != 1:
        raise ValueError('entropy must be a 1D array')

    if indices is not None:    
        try:
            len(indices) == len(entropy)
        except:
            args = indices, + args
            indices = None

    if indices is None:
        indices = arange(1, len(entropy) + 1)

    import matplotlib.pyplot as plt
    show = plt.bar(indices, entropy, *args, **kwargs)
    return show


def showMutualInfo(mutinfo, *args, **kwargs):
    """Show a heatmap of mutual information array.  :class:`MSA` instances 
    or Numpy character arrays storing sequence alignment are also accepted 
    as *mutinfo* argument, in which case :func:`.buildMutinfoMatrix` will 
    be used for calculations.  Note that x, y axes contain indices of the
    matrix starting from 1.
    
    Mutual Information is plotted using :func:`~matplotlib.pyplot.imshow`
    function."""
    
    try:
        ndim = mutinfo.ndim
    except AttributeError:
        mutinfo = buildMutinfoMatrix(mutinfo)
        ndim = mutinfo.ndim

    if ndim != 2:
        raise ValueError('mutinfo must be a 2D matrix')
    
    x, y = mutinfo.shape
    if x != y:
        raise ValueError('mutinfo matrix must be a square matrix')
    
    if not kwargs.has_key('interpolation'):
        kwargs['interpolation'] = 'nearest'
    if not kwargs.has_key('origin'):
        kwargs['origin'] = 'lower'
    
    extent = [0.5, x+0.5, 0.5, y+0.5]
    
    import matplotlib.pyplot as plt
    show = plt.imshow(mutinfo, extent = extent, *args, **kwargs), plt.colorbar()
    plt.xlabel('Indices')
    plt.ylabel('Indices')
    return show
