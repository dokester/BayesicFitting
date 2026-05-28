import numpy as numpy
import math as math
import numbers
import re
import inspect

from astropy.table import Table

__author__ = "Do Kester"
__year__ = 2026
__license__ = "GPL3"
__version__ = "3.3.0"
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
#  *    2016 - 2026 Do Kester

# Module Tools
"""
    This module contains a mixed bag of "usefull" methods.

"""

def getItem( ilist, k ) :
    """
    Return the k-th item of the ilist
        or the last when not enough
        or the ilist itself when it is not a list

    Parameters
    ----------
    ilist : an item or a list of items
        List to obtain an item from
    k : int
        item to be returned

    """
    return ( ilist if not isinstance( ilist, list ) else
             ilist[-1] if k >= len( ilist ) else ilist[k] )


def firstIndex( iterable, condition=lambda x: True ) :
    """
    Returns the index of first item in the `iterable` that
    satisfies the `condition`.

    If the condition is not given, it returns 0

    Parameters
    ----------
    iterable : iterable
        to find the first item in
    condition : lambda function
        the condition

    Raises
    ------
     StopIteration: if no item satysfing the condition is found.

    Examples
    --------
    >>> firstIndex( (1,2,3), condition=lambda x: x % 2 == 0)
    >>> 2
    >>> firstIndex( range( 3, 100 ) )
    >>> 3
    >>> firstIndex( () )
    >>> Traceback (most recent call last):
    >>> ...
    >>> StopIteration

    """
    return next( k for k,x in enumerate( iterable ) if condition( x ) )


def getColumnData( xdata, kcol ) :
    """
    Return the kcol-th column from xdata

    Parameters
    ----------
    xdata   2D array_like or Table
        the data array
    kcol    int
        column index
    """
    if isinstance( xdata, Table ) :
        return xdata.columns[kcol].data
    elif xdata.ndim == 2 :
        return xdata[:,kcol]
    else :
        return xdata

def isBetween( xs, x, xe ) :
    """
    Return True when x falls between xs and xe or on xs or xe.
        where the order of xs, xe is unknown.
    """
    return ( xs <= x <= xe ) or ( xe <= x <= xs )

def getKwargs( **kwargs ) :
    """
    Return kwargs as dictionary
    """
    return kwargs

def setAttribute( obj, name, value, type=None, islist=False, isnone=False ) :

    if type is None :                       ## no check on type
        object.__setattr__( obj, name, value )
        return True

    if isnone and value is None :           ## could be None
        object.__setattr__( obj, name, value )
        return True

    if islist :                             ## should be list of type
        isl = isList( value, type )
#        print( "TS  ", name, value, type, isl )
        if ( isl[0] ) :
            if type is not int and type is not float :
                array = value if isl[1] else [value]
            elif ( isl[1] ) : array = numpy.asarray( value, dtype=type )
            else : array = numpy.asarray( [value], dtype=type )
            object.__setattr__( obj, name, array )
            return True
        else :
            raise TypeError( name + ' has not the proper type: (list of) ' + str( type ) )
            return False

    if isInstance( value, type ) :          ## should be singular type
        object.__setattr__( obj, name, value )
        return True
    else :
        raise TypeError( name + ' has not the proper type: ' + str( type ) )
    return False


def setNoneAttributes( obj, name, value, listNone ) :
    """
    Set an attribute to an object.

    Parameters
    ----------
    obj : object
        to set the attribute to
    name : str
        of the attribute
    value : any
        of the attribute
    type : class
        check class of the object
    islist : boolean
        check if it is a list of type
    isnone : boolean
        value could be a None

    Raises
    ------
    TypeError : if any  checks fails
    """
    if name in listNone and value is None :
        object.__setattr__( obj, name, value )
        return True
    return False


def setListOfAttributes( obj, name, value, dictList ) :
    """
    Set attribute contained in dictionary dictList into the attr-list.
    A list is a native list or a numpy.ndarray. It also checks the type.
    if values is a singular item of the proper type it will be inserted as [value].

    Parameters
    ----------
    obj : object
        to place the attribute in
    name : str
        of the attribute
    value : any
        of the attribute
    listNone : list of names
        that could have a None value

    Returns
    -------
     True on succesful insertion. False otherwise.

    Raises
    ------
     TypeError   if the type is not as in the dictionary
     """
    if name in dictList :
        _type = dictList[name]
        isl = isList( value, _type )
#        print( name, isl )
        if ( isl[0] ) :
            if _type is not int and _type is not float :
                _array = value if isl[1] else [value]
            elif ( isl[1] ) : _array = numpy.asarray( value, dtype=_type )
            else : _array = numpy.asarray( [value], dtype=_type )
            object.__setattr__( obj, name, _array )
            return True
        else :
            raise TypeError( name + ' has not the proper type: (list of) ' + str( dictList[name] ) )
    return False


def setSingleAttributes( obj, name, value, dictSingle ) :
    """
    Set attribute contained in dictionary dictList into the attr-list.
    A list is a native list or a numpy.ndarray. It also checks the type.
    if values is a singular item of the proper type it will be inserted as [value].

    Parameters
    ----------
    obj : object
        to place the attribute in
    name : str
        of the attribute
    value : any
        of the attribute
    dictList : dictionary
        of possible attributes {"name": type}

    Returns
    -------
     True on succesful insertion. False otherwise.

    Raises
    ------
     TypeError   if the type is not as in the dictionary

    """
    if name in dictSingle :
        if isInstance( value, dictSingle[name] ) :
            object.__setattr__( obj, name, value )
            return True
        else :
            raise TypeError( name + ' has not the proper type: ' + str( dictSingle[name] ) )
    return False

def makeNext( x, k ) :
    """
    Set a singular attribute contained in dictionary dictSingle into the attr-list.
    It also checks the type.

    Parameters
    ----------
    obj : object
        to place the attribute in
    name : str
        of the attribute
    value : any
        of the attribute
    dictSingle : dictionary
        of possible attributes {"name": type}

    Returns
    -------
     True on succesful insertion. False otherwise.

    Raises
    ------
     TypeError   if the type is not as in the dictionary
     """
    try :
        _xnext = x[-1]
    except Exception :
        _xnext = x
    while True :
        try :
            _xnext = x[k]
            yield _xnext
            k += 1
        except Exception :
            yield _xnext


def length( x ) :
    """
    Return next item of x, and last item if x is exhausted.
    Or x itself if x is singular.
    """
    if x is None :
        return 0
    try :
        return len( x )
    except Exception :
        return 1

def toArray( x, ndim=1, dtype=None ) :
    """
    Return the length of any item. Singletons have length 1; None has length 0..
    """
    if isinstance( x, Table ) :
        return x
    return numpy.array( x, dtype=dtype, ndmin=min( ndim, 2 ) )

def isList( item, cls ) :
    """
    Return a array of x when x is a number

    Parameters
    ----------
    x : any number, list/array of numbers or []
        to be converted to numpy.ndarray
    ndim : int
        minimum number of dimensions present
    dtype : type
        conversion to type (None : as is)

    """
#    print( item, cls, item.__class__ )
    if isInstance( item, cls ) : return (True,False)
    islst = isinstance( item, list ) or isinstance( item, numpy.ndarray )
    if islst :
        for i in numpy.asarray( item ).flat :
            islst = islst and isInstance( i, cls )
    return (islst,islst)

def isInstance( item, cls ) :
    """
    Return (True,False) if item is a instance of cls
           (True,True)  if item is a (list|ndarray) of instances of cls
           (False,False) if not
    """
    if cls is int :
        return isinstance( item, int ) or isinstance( item, numpy.integer )
    elif cls is float :
        return isinstance( item, float ) or isInstance( item, int )
    else :
        return isinstance( item, cls )

def subclassof( sub, cls ) :
    """
    Transfer attributes from src to des.
    If copy is True try to copy the attributes, otherwise link it.

    Parameters
    ----------
    src : object
        source of the attributes
    des : object
        destiny for the attributes
    copy : bool
        if True: copy
    """
    if not inspect.isclass( sub ) : 
        return False

    while sub != cls and sub is not object :
        tre = inspect.getclasstree( [sub], unique=True )   
        sub = tre[0][0]

    return sub is cls

def printclass( cls, nitems=8, printId=False ) :
    """
    Determine if sub inherits from the class cls
    
    Parameters
    ----------
    sub : class object
        supposed sub class
    cls : class object
        supposed parent class
    """
    numpy.set_printoptions( precision=3, threshold=10, edgeitems=4 )

    ###  Import Model here to avoid circular imports ###
    from .Model import Model
    from .Problem import Problem

    print( "+++++++++++++++++++++++++++++++++++++++++++++++++++++++" )
    print( cls, " at ", id( cls ) ) if printId else  print( cls )
    print( "+++++++++++++++++++++++++++++++++++++++++++++++++++++++" )
    atr = vars( cls )
    ld = list( atr.keys() )
    ld.sort()
    for key in ld :
        print( "%-15.15s "%key, end="" )
        val = atr[key]
        if isinstance( val, (list,numpy.ndarray) ) :
            printlist( val, nitems=nitems )
        elif isinstance( val, str ) :
            print( shortName( val ) )
        elif isinstance( val, ( Model, Problem ) ) :
            print( val._toString( indent="                " ) )
        elif key == "model" :
            print( val.shortName( ) )
        elif inspect.ismethod( val ) :
            print( "-->", val.__name__ )
        else :
            try :
                valstr = val.__str__()
                if valstr.startswith( '<BayesicFitting' ) :
                    print( valstr.split()[0].split( '.' )[-1] )
                else : 
                    print( valstr )
            except Exception :
                print( val )
    print( "+++++++++++++++++++++++++++++++++++++++++++++++++++++++" )
            

def printlist( val, nitems=8 ) :
    nv = length( val )
    if nv == 0 or isinstance( val[0], numbers.Number ) :
        if nv <= nitems :
            print( val )
        else :
            print( val, nv )
        return

#    if val.dimensions > 1 :
#        print( "array of shape", val.shape )
#        return

    sep = "["
    for k in range( min( nv, nitems ) ) :
        try :
            print( "%s%s"%(sep, val[k].__name__ ), end="" )
        except Exception :
            print( "%s%s"%(sep, shortName( str( val[k] ) ) ), end="" )
        sep = " "
    print( "%s" % ( ( "... ] %d" % nv ) if nitems < nv else "]" ) )

def shortName( val ):
    """
    Print the attributes of a class.
    """
    m = re.match( "^[0-9a-zA-Z_]*", val )
    return m[0]


def nicenumber( x ) :
    """
    Return a short version the string representation: upto first non-letter.
    """
    if x == 0 :
        return x
    if x < 0 :
        sgn = -1
        x = abs( x )
    else :
        sgn = 1

    n = 1.0
    while x > 10 :
        x /= 10
        n *= 10
    while x < 1 :
        x *= 10
        n /= 10
    return sgn * int( x ) * n


def average( xx, weights=None, circular=None ) :
    """

    Parameters
    ----------
    statement : str
        statement to be traced

    """
    if circular is None :
        if weights is None :
            weights = numpy.ones_like( xx )
        sw = numpy.sum( weights )
        xw = xx * weights
        sx = numpy.sum( xw )
        averx = sx / sw

        rr = xx - averx
        stdvx = math.sqrt( numpy.average( rr * rr, weights=weights ) )

    else :
        range = circular[1] - circular[0]
        d2r = 2 * math.pi / range
        rr = ( xx - circular[0] ) * d2r
        asx = numpy.average( numpy.sin( rr ), weights=weights )
        acx = numpy.average( numpy.cos( rr ), weights=weights )
        averx = math.atan2( asx, acx )

        ## make rr relative to average and put 0.0 in mid of range.
        rr = ( rr - averx + math.pi ) % ( 2 * math.pi ) - math.pi
        stdvx = math.sqrt( numpy.average( rr * rr, weights=weights ) ) / d2r

        ## put the average inside the circular domain
        averx = averx / d2r + circular[0]
        while averx < circular[0] : averx += range
        while averx > circular[1] : averx -= range

    return( averx, stdvx )

def toRect( rp, phi=None ):
    """
    Return (x,y) coordinates from (rho,phi)

    Angles are measured counterclockwise from north to east
    North is Down (-y) and East is to the Right (+x)

    Parameters
    ----------
    rp : array of pairs [rho,phi] or tuple of (rhos,phis)
        rp[:,0] : separation of the stars
        rp[:,1] : angle from north (down) CCW to east (right)
    phi : array
        When phi is given, rp is interpeted as rho.

    Returns
    -------
    2d-array if the input is a 2d-array  or
    tuple of 2 arrays if the input is a tuple of 2 arrays or phi is given

    """
    if phi is not None :
        x =  rp * numpy.sin( phi )
        y = -rp * numpy.cos( phi )
        return ( x, y )

    if isinstance( rp, tuple ) :
        x =  rp[0] * numpy.sin( rp[1] )
        y = -rp[0] * numpy.cos( rp[1] )
        return ( x, y )

    xy = numpy.empty_like( rp )
    xy[:,0] = rp[:,0] * numpy.sin( rp[:,1] )
    xy[:,1] =-rp[:,0] * numpy.cos( rp[:,1] )

    return xy

def toRect3D( rho, phi, theta ):
    """
    Return (x,y,z) coordinates from (rho,phi,theta)

    The angle phi is measured counterclockwise from north to east
    North is Down (-y) and East is to the Right (+x)
    The angle theta is measured form the (x,y) plane. 
    Up is positive (+) and down is negative (-)

    Parameters
    ----------
    rho : array of float
        Separation between the stars
    phi : array of float
        angle in (x,y) plane from -y (North,down) to +x (East,right)
    theta : array of float 
        angle between z and star 2
 
    Returns
    -------
    (x,y,z) : tuple of 3 arrays 

    """
    # x, y = toRect( rho * numpy.sin( theta ), phi )
    rxy = rho * numpy.sin( theta )
    y = -rxy * numpy.cos( phi )
    x =  rxy * numpy.sin( phi )
    z = rho * numpy.cos( theta )

    return ( x, y, z )


def toSpher3D( x, y, z ) :
    """
    Return (rho,phi,theta) coordinates from (x,y,z)

    See toRect3D()

    Parameters
    ----------
    x : array of float
        x position
    y : array of float
        y position
    z : array of float
        z position

    Returns
    -------
    (rho,phi,theta) : tuple of 3 arrays 

    """
    rho = numpy.sqrt( x * x + y * y + z * z )
    numpy.seterr( divide="ignore" )
    theta = numpy.where( rho == 0, 0, numpy.arccos( z / rho ) )
    phi = numpy.arctan2( x, -y )

    return ( rho, phi, theta )
    
def toSpher( xy, y=None ) :
    """
    Return (rho,phi) coordinates from (x,y)

    Angles are measured counterclockwise from north to east
    North is Down (-y) and East is to the Right (+x)

    Parameters
    ----------
    xy : array of pairs [x,y] or tuple of (x array,y array)
        xy[:,0] : x position
        xy[:,1] : y position
    y : array
        when given xy is interpreted as x

    Returns
    -------
    2d-array if the input is a 2d-array  or
    tuple of 2 arrays if the input is a tuple of 2 arrays or when y is given

    """
    if y is not None :
        r = numpy.hypot( xy, y )
        p = numpy.arctan2( xy, -y )
        return ( r, p )

    if isinstance( xy, tuple ) :
        r = numpy.hypot( xy[0], xy[1] )
        p = numpy.arctan2( xy[0], -xy[1] )
        return ( r, p )

    rp = numpy.empty_like( xy )
    rp[:,0] = numpy.hypot( xy[:,0], xy[:,1] )
    rp[:,1] = numpy.arctan2( xy[:,0], -xy[:,1] )

    return rp

def arrow( x, y, z=None, scale=1.0 ) :
    """
    Return the coordinates of an arrow point from (xyz[0]) to (xyz[1])

    The returned 2-d coordinates are at
        tail, top, left-head, right-head, top 

    the returned 3-d coordinates are at 
        tail, top, left-head, right-head, top, read-head, near-head, top

    Parameters
    ----------
    x : array of length 2 (at least)
        x-coordinates
    y : array of length 2 (at least)
        y-coordinates
    z : array of length 2 or None
	when None return 2D array else 3D
    scale : float
        scale factor. End point stays in place
    """
    dx = ( x[1] - x[0] ) * scale
    dy = ( y[1] - y[0] ) * scale

    xb = x[1] - dx 
    yb = y[1] - dy

    dx /= 2
    dy /= 2

    xarrow = numpy.array( [x[0], x[1], xb + dy, xb - dy, x[1]] )
    yarrow = numpy.array( [y[0], y[1], yb - dx, yb + dx, y[1]] )

    if z is None :
        return ( xarrow, yarrow )

    dx = x[0] - x[1]
    dy = y[0] - y[1]
    dz = z[0] - z[1]

    rho, phi, theta = toSpher3D( dx, dy, dz )

    ## make arrow along x-axis of length rho 
    hd = scale * rho / 2
    tl = hd - rho
    wd = hd / 2
    ya = numpy.array( [tl, hd,  0,  0, hd,  0,  0, hd] )
    za = numpy.array( [ 0,  0, wd,-wd,  0,  0,  0,  0] )
    xa = numpy.array( [ 0,  0,  0,  0,  0, wd,-wd,  0] )

    ## transform arrow to spherical
    ra, pa, ta = toSpher3D( xa, ya, za )

    ## rotate over theta and phi
    ta += ( theta - numpy.pi / 2 ) * numpy.cos( pa )
    pa += phi

    ## transform back and add starting point.
    x1, y1, z1 = toRect3D( ra, pa, ta )

    ## shift in place
    ba = hd / rho
    bb = 1 - ba
    xar = x1 + ba * x[0] + bb * x[1]
    yar = y1 + ba * y[0] + bb * y[1]
    zar = z1 + ba * z[0] + bb * z[1]

    return ( xar, yar, zar )


def minmax( x, range=False, mid=False ) :
    """
    Return minimum, maximum, range and midpoint of an array

    Parameters
    ----------
    x : array
        the array
    range : bool (False)
        return range (max - min) too
    mid : bool (False)
        return midpoint (max + min) / 2 too
    """
    mn = min( x )
    mx = max( x )
    if not ( range or mid ) :
        return ( mn, mx )
    if range & mid :
        return ( mn, mx, mx-mn, (mx+mn)/2 )
    if range :
        return ( mn, mx, mx-mn )

    return ( mn, mx, (mx+mn)/2 )

