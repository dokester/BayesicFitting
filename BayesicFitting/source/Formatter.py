from __future__ import print_function

import numpy as numpy
from numpy import ndarray

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.5"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

#  * This file is part of the BayesicFitting package.
#  *
#  * BayesicFitting is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU Lesser General Public License as
#  * published by the Free Software Foundation, either version 3 of
#  * the License, or ( at your option ) any later version.
#  *
#  * BayesicFitting is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  * GNU Lesser General Public License for more details.
#  *
#  * The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  *    2017 - 2025 Do Kester


# Module Formatter
"""
This module contains methods to format numbers, especially in arrays.

"""


gllen = 110
gindent = 0
gmax = 5
fmt = { "float64" : " %8.3f", 
        "int64" : " %8d", 
        "uint8" : " %8d", 
        "bool" : " %d", 
        "object" : "%s" }


def formatter_init( format={}, indent=None, linelength=None, max=-1 ):
    """
    Initialize the formatter with new default values.

    Parameters
    ----------
    format : dict {namestring : formatstring }
        name : "float64" or "int64"
        fmt  : " %fmt"
    indent : None or int
        number of spaces to indent *after* the first line
        Default is 0
    linelength : None or int
        length of the lines produced
        Default is 120
    max : None or int
        maximum number of items displayed followed by ... if there are more
        None displays all
        Default is 5
    """

    global gllen, gindent, gmax

    for k in format.keys() :
        fmt[k] = format[k]

    if indent is not None :
        gindent = indent
    if linelength is not None :
        gllen = linelength
    if max is None or max >= 0 :
        gmax = max
#    print( "init  ", gindent, gllen, gmax, fmt )

def fma( erray, **kwargs ) :
    """
    Syntactic sugar for
        formatter( ..., max=None, ... )
    """
    return formatter( erray, max=None, **kwargs )

def formatter( erray, format=None, indent=None, linelength=None, max=-1, tail=0 ) :
    """
    Format a number or an array nicely into a string

    Parameters override defaults given earlier with init().

    Parameters
    ----------
    array : array_like or number
        number or list of numbers or n-dim array of numbers
    format : None or string
        format applying to one item of array
        Default is "8.3f" for float and "8d" for int
    indent : None or int
        number of spaces to indent *after* the first line
        Default is 0
    linelength : None or int
        length of the lines produced
        Default is 120
    max : None or int
        maximum number of items displayed followed by ... if there are more
        None displays all
        Default is 5
    tail : int
        print the last items in the array, preceeded by ...
        Only if the number of items is larger than max.
        Default is 0

    Returns
    -------
    string : containing the formatted array

    """
    global count, nwl, sp, llen, fmtlen, mx, fmt

    if indent is None :
        indent = gindent
    if linelength is None :
        linelength = gllen
    if max is not None and max <= 0 :
        max = gmax
    count = indent
    llen = linelength
    mx = max
    nwl = False
    sp = 0
#    print( count, nwl, sp, llen, indent, mx, fmt )

    if not isinstance( erray, ndarray ) :
        erray = numpy.asarray( erray )

    if format is None :
        format = fmt[str(erray.dtype)]

    fmtlen = len( format % 1 )

    result = ""
    result = recursive_format( result, erray, format=format, indent=indent, tail=tail )
    return result

def recursive_format( result, erray, format=None, indent=0, tail=0 ) :
    global count, nwl, sp, llen, fmtlen, mx, fmt

    if erray.size == 1 :
        if count + fmtlen > llen :
            result += ( "\n%s" % spaces( sp + indent ) )
            count = indent
        if format is None :
            format = fmt[erray.__class__]

        ## Avoid DeprecationError from numpy.
        erray = erray.item( 0 )

        result += ( format % erray )

        count += fmtlen
        return result

    shp = erray.shape
    if sp > 0 and nwl :
        result += ( "\n%s" % spaces( sp + indent ) )
    result += ( "[" )
    nwl = False
    sp += 1
    shp0 = shp[0] if mx is None else min( shp[0], mx )
    for k in range( shp0 ) :
        result = recursive_format( result, erray[k], format=format,
                                   indent=indent, tail=tail )
        nwl = True
    if mx is not None and shp[0] > mx :
        if shp[0] > mx + tail :
            lens = len( shp )
            if lens > 1 :
                result += "\n%s..." % spaces( lens + indent )
            else :
                result += " ..."
        t = min( tail, shp[0] - mx )
        for k in range( -t, 0 ) :
            result = recursive_format( result, erray[k], format=format,
                                       indent=indent, tail=tail )

    result += ( "]"  )
    count = 0
    sp -=1
    return result

def spaces( ksp ) :
    """
    Return ksp spaces.
    """
    return ( " " * ksp )

