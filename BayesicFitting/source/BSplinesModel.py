import numpy as numpy
from . import Tools
from .Tools import setAttribute as setatt
import math
# import (modified) bspline from Juha Jeronen
from . import bspline
from . import splinelab

from .LinearModel import LinearModel

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2017 - 2022 Do Kester

class BSplinesModel( LinearModel ):
    """
    General b-splines model of arbitrary order and with arbitrary knot settings.

    It encapsulates the bspline package of John Foster and Juha Jeronen,
    at http://github.com/johnfoster/bspline.

    B-splines have some advantages over natural splines as implemented in
    SplinesModel. Specificly the parameters are much more easily
    interpreted as the amplitudes of spline-like blobs. The disadvantage of
    BSplinesModel is that the x-values need to fall strictly within the range
    spanned by the knots.

    It is a linear model.

    order   behaviour between knots     continuity at knots
      0     piecewise constant          not continuous at all
      1     piecewise linear            lines are continuous
      2     parabolic pieces            1st derivatives are also continuous
      3     cubic pieces                2nd derivatives are also continuous
     n>3    n-th order polynomials      (n-1)-th derivatives are also continuous

    The user lays out a number ( << datapoints ) of knots on the x-axis at
    arbitrary position, generally more knots where the curvature is higher.
    The knots need to be monotonuously increasing in x.
    Alternatively one can ask this class to do the lay-out which is then
    equidistant in x over the user-provided range.
    Through these knots a splines function is obtained which best
    fits the datapoints. One needs at least 2 knots, one smaller and one
    larger than the x-values in the dataset.

    Contrary to the SplinesModel here the xdata need to be strictly inside the range
    spanned by the knots: knots[0] <= xdata < knots[-1]

    This model is NOT for (cubic) spline interpolation.

    Examples
    --------
    >>> knots = numpy.arange( 17, dtype=float ) * 10    # make equidistant knots from 0 to 160
    >>> csm = BSplinesModel( knots=knots, order=2 )
    >>> print csm.getNumberOfParameters( )
    18
    # or alternatively:
    >>> csm = BSplinesModel( nrknots=17, order=2, min=0, max=160 )    # automatic layout of knots
    >>> print csm.getNumberOfParameters( )
    18
    # or alternatively:
    >>> npt = 161                                               # to include both 0 and 160.
    >>> x = numpy.arange( npt, dtype=float )                    # x-values
    >>> csm = BSplinesModel( nrknots=17, order=2, xrange=x )     # automatic layout of knots
    >>> print csm.getNumberOfParameters( )
    18

    Attributes
    ----------
    knots : array_like
        a array of arbitrarily positioned knots
    order : int
        order of the spline. Default 3 (cubic splines)
    eps : float
        small number to enable inclusion of endpoints. Default 0.0.


    Attributes from Model
    --------------------------
        parameters, stdevs, xUnit, yUnit, npchain

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames



    Limitations
    -----------
    Dont put the knots too closely so that there are no datapoints in between.

    """
    def __init__( self, knots=None, order=3, nrknots=None, min=None, max=None, xrange=None,
                        copy=None, fixed=None, **kwargs ):
        """
        Splines on a given set of knots and a given order.

        The number of parameters is ( length( knots ) + order - 1 )

        Parameters
        ----------
        knots : array_like
            a array of arbitrarily positioned knots
        order : int
            order of the spline. Default 3 (cubic splines)
        nrknots : int
            number of knots, equidistantly posited over xrange or [min,max]
        min : float
            minimum of the knot range
        max : float
            maximum of the knot range
        xrange : array_like
            range of the xdata
        copy : BSplinesModel
            model to be copied.
        fixed : dict
            If not None, raise AttributeError.


        Raises
        ------
        ValueError : At least either ('knots') or ('nrnkots', 'min', 'max') or
                ('nrknots', 'xrange') must be provided to define a valid model.
        AttributeErrr : When fixed is not None

        Notes
        -----
        The BSplinesModel is only strictly valid inside the domain defined by the
        minmax of knots. It does not exist outside that domain.

        """
        if fixed is not None :
            raise AttributeError( "BSplinesModel cannot have fixed parameters" )

        if copy is not None :
            knots = copy.knots
            order = copy.order
        if knots is not None : nrknots = len( knots )
        elif nrknots is None :
            raise ValueError( "Need either knots or (nrknots,min,max) or (nrknots,xrange)" )

        super( BSplinesModel, self ).__init__( order + nrknots - 1, copy=copy, **kwargs )
        setatt( self, "order", order )
        if knots is None :
            if xrange is not None :
                min = numpy.min( xrange )
                max = numpy.max( xrange )
            knots = numpy.linspace( min, max, nrknots, dtype=float )
        self.knots = knots

        augknots = splinelab.augknt( knots, order )
        setatt( self, "_bspline", bspline.Bspline( augknots, self.order, last=True ) )
        self.eps = 0.0

    def copy( self ):
        return BSplinesModel( copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: knots, order

        """
        rerun = False
        if name == "knots" :
            setatt( self, name, value, type=float, islist=True )
            rerun = True
        elif name == "order" :
            setatt( self, name, value, type=int )
            rerun = True
        elif name == "eps" :
            setatt( self, name, value, type=float )

        else :
            super( BSplinesModel, self ).__setattr__( name, value )

        if rerun :
            augknots = splinelab.augknt( self.knots, self.order )
            setatt( self, "_bspline", bspline.Bspline( augknots, self.order, last=True ) )


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
            list of indices active parameters (or None for all)

        Raises
        ------
        ValueError when xdata < knots[0] or xdata > knots[1]

        """
        if numpy.any( xdata < self.knots[0] ) or numpy.any( xdata > self.knots[-1] ) :
            print( "Min max data : ", numpy.min( xdata ), numpy.max( xdata ),
                   "  knots : ", self.knots[0], self.knots[-1] )
            raise ValueError( "Input data need to fall strictly in the domain spanned by knots" )

        partial = Tools.toArray( self._bspline.collmat( xdata ), ndim=2 )

        return partial

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each xdata (=x).

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters to the model

        """
        xd = numpy.where( xdata == self.knots[-1], ( 1.0 - self.eps ) * self.knots[-1], xdata )

        partial = Tools.toArray( self._bspline.collmat( xd, deriv_order=1 ), ndim=2 )

        return numpy.inner( params, partial )

    def baseName( self ):
        """ Returns a string representation of the model. """
        return "BSplines of order %d with %d knots."%( self.order, len( self.knots) )

    def baseParameterUnit( self, k ):
        """
        Return the units of the parameter.

        Parameters
        ----------
        k : int
            index of the parameter.
        """
        return self.yUnit


