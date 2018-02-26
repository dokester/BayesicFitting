import numpy as numpy
from . import Tools
from .Model import Model
from .LinearModel import LinearModel
from .SplinesModel import SplinesModel

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

#  *
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester

class SurfaceSplinesModel( LinearModel ):
    """
    Surface splines model of arbitrary order and knot settings.

    It is a linear model.

    Surface splines are direct product of a splines model in the x-direction with
    a splines model in the y-direction.

    The number of parameters is
    ( xknotlength + xorder - 1 ) * ( yknotlength + yorder - 1 )

    The SplinesModel has more information about order and knots.

    Examples
    --------
    >>> nxk = 17
    >>> nyk = 11
    >>> xknots = numpy.arange(  nxk , dtype=float ) * 10      # make knots from 0 to 160
    >>> yknots = numpy.arange(  nyk , dtype=float ) * 10      # make knots from 0 to 100
    >>> csm = SurfaceSplinesModel( xknots, yknots, 2 )
    >>> print csm.getNumberOfParameters( )      # ( nxk + order - 1 )*( nyk + order - 1 )
    216
    # ... fitter etc. see Fitter

    Category     mathematics/Fitting

    Attributes
    ----------

    """

    def __init__( self, knots, order=3, copy=None, fixed=None, **kwargs ):
        """
        Splines on a given set of knots and a given order.

        The number of parameters is ( length( knots ) + order - 1 )

        Parameters
        ----------
        knots : list of array_like
            positions of the knots in all dimensions
        order : int or list of ints
            order of the splines in all dimensions
        copy : SurfaceSplinesModel
            model to be copied
        fixed : dict
            If not None raise AttributeError.

        Raises
        ------
        AttributeErrr : When fixed is not None

        """
        if fixed is not None :
            raise AttributeError( "SurfaceSplinesModel cannot have fixed parameters" )

        super( SurfaceSplinesModel, self ).__init__( self.calcNp( knots, order ),
                    ndim=len( knots ), copy=copy )
        self.order = order if Tools.length( order ) > 1 else [order] * len( knots )
        self.knots = knots
        models = []
        for (kn,dr) in zip( self.knots, self.order ) :
            models = models + [SplinesModel( knots=kn, order=dr )]
        self.models = models

    def copy( self ):
        """ Copy method.  """
        return SurfaceSplinesModel( self.knots, order=self.order, copy=self )

    def calcNp( self, knots, order ) :
        if Tools.length( order ) == 1 :
            order = [order] * len( knots )
        np = 1
        for (kn,dr) in zip( knots, order ) :
            np *= ( len( kn ) + dr - 1 )

        if isinstance( np, numpy.int64 ) :
            np = np.item()

        return np

    def __setattr__( self, name, value ):
        """
        Set attributes: knots, order, models

        """
        dlst = {'order': int, 'models': Model }
        done = {'knots': list }
        if ( Tools.setListOfAttributes( self, name, value, dlst ) or
             Tools.setSingleAttributes( self, name, value, done ) ) :
            pass
        else :
            super( SurfaceSplinesModel, self ).__setattr__( name, value )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        The partials are the powers of x (input) from 0 to degree.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters to the model (ignored in LinearModels)
        parlist : array_like
            not used in this model
        """
        ndata = Tools.length( xdata[:,0] )
        partial = numpy.ones( ( ndata, 1 ), dtype=float )
        np = 1
        n = 0
        for mdl in self.models :
            nw = numpy.zeros( ( ndata, np * mdl.npbase ), dtype= float )
            mpart = mdl.basePartial( xdata[:,n], params )
            k = 0
            for i in range( np ) :
                for j in range( mdl.npbase ) :
                    nw[:,k] = partial[:,i] * mpart[:,j]
                    k += 1

            partial = nw
            n += 1
            np *= mdl.npbase

        return partial

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        strkn = "["
        stror = "["
        for k,o in zip( self.knots, self.order ) :
            strkn += ( "%d,"%len( k ) )
            stror += ( "%d,"%o )
        strkn = strkn[:-1] + "]"
        stror = stror[:-1] + "]"
        return str( "SurfaceSplines %dd of order "%self.ndim + stror + " with " + strkn + " knots" )

    def baseParameterName( self, k ):
        """
        Return the name of a parameter.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        strpar = "param"
        for mdl in self.models :
            nx = mdl.npbase
            strpar = strpar + "_%d"%(k%nx)
            k = k // nx
        return strpar

    def baseParameterUnit( self, k ):
        """
        Return the unit of a parameter.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        u = self.yUnit
        n = 0
        for mdl in self.models :
            nx = mdl.npbase
            j = k % nx
            if j > 3 : j = 3
            k = k // nx
            u = u / ( self.xUnit[n] ** j )
            n += 1
        return u


