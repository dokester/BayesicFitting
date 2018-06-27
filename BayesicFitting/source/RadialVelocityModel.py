import numpy as numpy
from astropy import units
import math
from . import Tools
from .NonLinearModel import NonLinearModel

__author__ = "Do Kester"
__year__ = 2018
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
#  *    2018        Do Kester

class RadialVelocityModel( NonLinearModel ):
    """
    Model for the radial velocity variations of a star caused by a orbiting planet.
.
    .. math::
        f( x:p ) = p_1 * \cos( 2 * \pi * p_0 * x ) + p_2 * \sin( 2 * \pi * p_0 * x )

    amplitude   : of the velocity variation (>0)
    eriod       : of the velocity variation (>0)
    eccentricity: of the elliptic orbit (0<e<1; 0 = circular orbit)
    phase       : time shift since periastron (0<p<2pi)
    periastron  : longitude of periastron (0<p<2pi)

    Note:
    The velocity of the star system is not included in this model. See example.

    The parameters are initialized at {1.0, 1.0, 0.0, 0.0, 0.0}.
    It is a non-linear model.

    Examples
    --------
    >>> rv = RadialVelocityModel( )
    >>> print( rv.npchain )
    3
    >>> rv += PolynomialModel( 0 )          # add a constant system velocity

    """
    TWOPI = 2 * math.pi

    def __init__( self, copy=None, **kwargs ):
        """
        Radial velocity model.

        Number of parameters is 5:

        Parameters
        ----------
        copy : SineModel
            model to copy
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [1.0, 1.0, 0.0, 0.0, 0.0]
        names = ["amplitude", "period", "eccentricity", "phase", "periastron"]

        super( RadialVelocityModel, self ).__init__( 5, copy=copy, params=param,
                        names=names, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return RadialVelocityModel( copy=self )

    def __getattr__( self, name ) :
        """
        Return value belonging to attribute with name.

        Parameters
        ----------
        name : string
            name of the attribute
        """
        if name == "semimajoraxis" :
            p = self.parameters
            return p[0] * p[1] * math.sqrt ( 1 - p[2] * p[2] ) / self.TWOPI
        else :
            return super( RadialVelocityModel, self ).__getattr__( name )

    def getMsini( self, stellarmass ) :
        """
        Return the mass of the exoplanet in Jupiter masses.

        Parameters
        ----------
        stellarmass : float
            mass of the host star in solar masses.
        """
        p = self.parameters
        return ( 4.91e-3 * math.pow( stellarmass, 2.0 / 3.0 ) * p[0] *
                 math.pow( p[1], 1.0 / 3.0 ) * math.sqrt( 1 - p[2] * p[2] ) )



    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        x = self.TWOPI * self.anomaly( xdata, params ) + params[4]
        result = params[0] * ( numpy.cos( x ) + params[2] * math.cos( params[4] ) )
        return result

    def anomaly( self, xdata, params ) :
        """
        Returns the true anomaly at times xdata

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        period = params[1]
        eccen = params[2]
        phase = params[3] / self.TWOPI

#        otime = ( ( xdata + phase ) % period ) / period
        otime = ( ( xdata / period ) + phase ) % 1.0

        npt = 361
        phi = numpy.linspace( 0.0, 1.0, npt, dtype=float )
        r = ( 1 - eccen * eccen ) / ( 1 - eccen * numpy.cos( self.TWOPI * phi ) )

        sectors = 0.5 * r[1:] * r[:-1] * math.sin( self.TWOPI * phi[1] )
        anom = numpy.cumsum( sectors )
#        print( anom )
        anom /= anom[-1]
#        anom *= ( period / anom[-1] )

        k = 0
        res = numpy.zeros_like( xdata )
        for i,t in enumerate( otime ) :
            while k < npt and anom[k] < t :
                k += 1
            while k > 0 and anom[k] > t :
                k -= 1
            res[i] = phi[k] + phi[1] * ( t - anom[k] ) / ( anom[k+1] - anom[k] )

        return res


    def TBWbasePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        np = self.npbase if parlist is None else len( parlist )
        partial = numpy.ndarray( ( Tools.length( xdata ), np ) )

        #  disregard count
        x = self.TWOPI * xdata
        xf = x * params[0]
        cxf = numpy.cos( xf )
        sxf = numpy.sin( xf )

        parts = { 0 : ( lambda: x * params[2] * cxf - x * params[1] * sxf ),
                  1 : ( lambda: cxf ),
                  2 : ( lambda: sxf ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def TBWbaseDerivative( self, xdata, params ):
        """
        Returns the derivative of f to x (df/dx) at the input values.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        x = self.TWOPI * xdata * params[0]
        df = self.TWOPI * params[0] * ( params[2] * numpy.cos( x ) - params[1] * numpy.sin( x ) )
        return df

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "RadialVelocity " )

    def baseParameterUnit( self, k ):
        """
        Return the unit of a parameter.

        Parameters
        ----------
        k : int
            the kth parameter.

        """
        if k == 0:
            return units.Unit( units.si.rad ) / self.xUnit
        return self.yUnit

