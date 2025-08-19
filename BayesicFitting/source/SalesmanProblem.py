import numpy as numpy
from astropy import units
import math
import warnings
from . import Tools

from .OrderProblem import OrderProblem

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"


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
#  *    2018 - 2025 Do Kester


class SalesmanProblem( OrderProblem ):
    """
    Traveling Salesman Problem.

    The parameters give the order in which the nodes are visited.

    The result is a list of distances.

        [dist( x[p[k-1]], x[p[k]] ) for k in range( len( p ) )]

    The number of parameters is equal to the length of the xdata array
    The parameters are initialized at [k for k in range( npars )]

    Examples
    --------
    >>> tsm = SalesmanProblem( 100 )
    >>> print( tsm )
    >>> TravelingSalesman in 2 dimensions with 100 nodes.
    >>> print( tsm.npars )
    >>> 100


    """

    DISNAMES = ["User Defined", "Manhattan", "Euclidic", "Spherical", "Tabulated"]


    def __init__( self, xdata=None, weights=None, distance="euclid", scale=None, table=None,
                  oneway=False, copy=None ):
        """
        Traveling Salesman problem.


        Parameters
        ----------
        xdata : array_like of shape [np,ndim]
            the nodes to be visited
        weights : array_like
            weights on the arrival nodes
        distance : str or callable
            to calculate the distance between point1 and point2
            "manh"   : Manhattan distance (1 norm) (2 or more dimensions)
            "euclid" : Euclidic (2 norm) (2 or more dimensions) 
            "spher"  : spherical, distance over sphere (2 dimensions only) 
            "table"  : tabulated distance values
            callable of the form callable( xdata, pars )
        scale : None or float
            scale all distances by this number.
            None : take minimum distance as scale
        table : arraylike or None
            table of all distances, Only when distance is "tabulated"
        oneway : bool
            Don't close the loop; cut at position 0.
        copy : SalesmanProblem
            to be copied

        """
        super( ).__init__( xdata=xdata, weights=weights, copy=copy )

        if copy is not None :
            self.distance = copy.distance
            self.disname = copy.disname
            self.scale = copy.scale
            self.oneway = copy.oneway
            return

        self.oneway = oneway

        if callable( distance ) :
            self.distance = distance
            self.disname = self.DISNAMES[0]

        elif isinstance( distance, str ) :
            dis = distance.lower()[0]

            self.disname = self.DISNAMES[2]
            if dis == "e" :
                self.distance = self.euclidic
            elif dis == "m" :
                self.distance = self.manhattan
                self.disname = self.DISNAMES[1]
            elif dis == "s" :
                self.distance = self.spherical
                self.disname = self.DISNAMES[3]    
            elif dis == "t" :
                self.distance = self.tabulated
                self.disname = self.DISNAMES[4]
                self.table = table
            else :
                warnings.warn( "Unknown distance ", distance, " Using euclidic in stead" )
                self.distance = self.euclidic
        else :
            warnings.warn( "Unknown distance ", distance, " Using euclidic in stead" )
            self.distance = self.euclidic

        mindis = self.minimumDistance()
        if mindis < 1e-10 :
            print( "SalesmanProblem. minimumDistance less than 1.e-10" )
            mindis = 1.0

        self.scale = scale if scale is not None else mindis 


    def copy( self ):
        """ Copy method.  """
        return SalesmanProblem( xdata=self.xdata, weights=self.weights, copy=self )

    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        
        """
        return True

    def result( self, params ):
        """
        Calculates the distance between the nodes (xdata) in the order
        given by the parameters (params), multiplied by the weight at the 
        starting node (if present), divided by the scale

        Each result is 

            res[k] = dis[k] * weight[params[k]] / scale

        Parameters
        ----------
        params : array_like
            values for the parameters.

        Returns
        -------
        An array of distances

        """
        res = self.distance( self.xdata, params ) / self.scale

        if self.oneway :
            res[-1] = 0                     # dont return home.

        if self.weights is None :
            return res 
        else :
            return res * self.weights[params]

    def manhattan( self, xdata, pars, roll=1 ) :
        """
        Use Manhattan distances (1-norm)

        Each distance is 

            dis[k] = SUM_i ( abs( xdata[pars[k],i] - xdata[pars[k+roll],i] ) )

        Parameters
        ----------
        xdata : array-like of shape (ndata,ndim) 
            positional info in several dimensions
        pars : list of indices
            designating the order of the nodess
        roll : int
            number of positions to roll 
        """
        xd = xdata[pars]
        r = numpy.abs( xd - numpy.roll( xd, -roll, axis=0 ) )    ## leaving from xd
        return numpy.sum( r, 1 )

    def euclidic( self, xdata, pars, roll=1 ) :
        """
        Use Euclidic distances (2-norm)

        Each distance is 

            dis[k] = sqrt( SUM_i ( ( xdata[pars[k],i] - xdata[pars[k+roll],i] )^2 ) )

        Parameters
        ----------
        xdata : array-like of shape (ndata,ndim) 
            positional info in several dimensions
        pars : list of indices
            designating the order of the nodes
        roll : int
            number of positions to roll 
        """
        xd = xdata[pars]
        r = numpy.square( xd - numpy.roll( xd, -roll, axis=0 ) )        ## leaving from xd
        return numpy.sqrt( numpy.sum( r, 1 ) )

    def spherical( self, xdata, pars, roll=1 ) :
        """
        Use distances over a 2-d unit sphere.

        Each distance is calculated according to the Haversine formula.
 
        It is assumed that the xdata is in decimal degrees: [longitude, latitude]

        The results are in radian.

        Parameters
        ----------
        xdata : array-like of shape (ndata,2) 
            longitude, latitude info
        pars : list of indices
            designating the order of the nodes
        roll : int
            number of positions to roll 
        """
        if not hasattr( self, "coslat1" ) :

            xd = xdata * math.pi / 180
            xh = xd / 2

            self.coslat1 = numpy.cos( xd[:,1] )

            self.shlon1 = numpy.sin( xh[:,0] )
            self.chlon1 = numpy.cos( xh[:,0] )
            self.shlat1 = numpy.sin( xh[:,1] )
            self.chlat1 = numpy.cos( xh[:,1] )


        cslat1 = self.coslat1[pars]

        shlon1 = self.shlon1[pars]
        chlon1 = self.chlon1[pars]
        shlat1 = self.shlat1[pars]
        chlat1 = self.chlat1[pars]

        cslat2 = numpy.roll( cslat1, -roll )
        shlon2 = numpy.roll( shlon1, -roll )
        chlon2 = numpy.roll( chlon1, -roll )
        shlat2 = numpy.roll( shlat1, -roll )
        chlat2 = numpy.roll( chlat1, -roll )

        a = ( numpy.square( shlat2 * chlat1 - shlat1 * chlat2 ) + 
              cslat1 * cslat2 *
              numpy.square( shlon2 * chlon1 - shlon1 * chlon2 ) )

        # catch round-off error above 1.
        a = numpy.where( a > 1, 1.0, a )

        dis = 2 * numpy.arctan2( numpy.sqrt( a ), numpy.sqrt( 1 - a ) )

        return dis 

    def tabulated( self, xdata, pars, roll=1 ) :
        """
        Use tabulated distances from self.table

        Each distance is 

            dis[k] = table[ pars[k], pars[k+roll] ]

        Parameters
        ----------
        xdata : array-like of shape (ndata,ndim) 
            positional info in several dimensions
        pars : list of indices
            designating the order of the nodess
        roll : int
            number of positions to roll 
        """

        r = self.table[ pars, numpy.roll( pars, -roll ) ]
        return r

    def minimumDistance( self ) :
        """
        Return the smallest distance in the data.

        """        
        ndata = len( self.xdata[:,0] )
        pars = numpy.arange( ndata, dtype=int )
        md = self.distance( self.xdata, pars ).min()
        for roll in range( 2, ndata ) :
            md = self.distance( self.xdata, pars, roll=roll ).min( initial=md )

        return md

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "TravelingSalesman in %d dimensions with %d nodes. %s distance" %
                    ( self.ndim, self.npars, self.disname ) )



