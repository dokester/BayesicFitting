import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt
from .NonLinearModel import NonLinearModel
from .Kepplers2ndLaw import Kepplers2ndLaw

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

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
#  *    2018 - 2020 Do Kester

class RadialVelocityModel( NonLinearModel ) :
    """
    Model for the radial velocity variations of a star caused by a orbiting planet.

    p_0 : eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
    p_1 : amplitude    of the velocity variation (>0)
    p_2 : period       of the velocity variation (>0)
    p_3 : phase        phase of periastron (0<p<2pi)
    p_4 : periastron   longitude of periastron (0<p<2pi)

    This class uses @Kepplers2ndLaw to find radius and true anomaly.

    Note:
    The velocity of the star system is not included in this model. See example.

    The parameters are initialized at {0.0, 1.0, 1.0, 0.0, 0.0}.
    It is a non-linear model.

    Attributes
    ----------
    keppler : Kepplers2ndLaw()
        to calculate the radius and true anomaly

    Examples
    --------
    >>> rv = RadialVelocityModel( )
    >>> print( rv.npars )
    5
    >>> rv += PolynomialModel( 0 )          # add a constant system velocity

    """
    TWOPI = 2 * math.pi

    def __init__( self, copy=None, **kwargs ):
        """
        Radial velocity model.

        Number of parameters is 5:

        Parameters
        ----------
        copy : RadialVelocityModel
            model to copy
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [0.0, 1.0, 1.0, 0.0, 0.0]
        names = ["eccentricity", "amplitude", "period", "phase", "longitude"]

        super( RadialVelocityModel, self ).__init__( 5, copy=copy, params=param,
                        names=names, **kwargs )

        setatt( self, "keppler", Kepplers2ndLaw() )

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

        f(x:p) = p_1 * ( cos( v + p_4 ) + p_0 * cos( p_4 ) )

        where v is the true anomaly

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        pars = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, pars )

        x = v + params[4]

        result = params[1] * ( numpy.cos( x ) + params[0] * math.cos( params[4] ) )
        return result


    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        f(x:p) = p_1 * ( cos( v + p_4 ) + p_0 * cos( p_4 ) )

        df/dp_0 = p_1 * ( - sin( v + p_4 ) dv/dp_0 + cos( p_4 ) )
        df/dp_1 = cos( v + p_4 ) + p_0 * cos( p_4 )
        df/dp_2 = - p_1 * sin( v + p_4 ) dv/dp_2
        df/dp_3 = - p_1 * sin( v + p_4 ) dv/dp_3
        df/dp_4 = - p_1 * ( sin( v + p_4 ) + p_0 * sin( p_4 ) )

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        ecc = params[0]
        amp = params[1]
        lon = params[4]

        np = self.npbase if parlist is None else len( parlist )

        pars = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, pars )

        E = self.keppler.eccAnomaly
        sinE = self.keppler.sinE
        cosE = self.keppler.cosE

        drde, drda, drdP, drdp, dvde, dvdP, dvdp = self.keppler.drvdpar( xdata, pars,
                                       E, cosE, sinE )

        vp4 = v + lon
        sinvp4 = numpy.sin( vp4 )


        part = { 0 : ( lambda : amp * ( math.cos( lon ) - sinvp4 * dvde ) ),
                 1 : ( lambda : numpy.cos( vp4 ) + ecc * math.cos( lon ) ),
                 2 : ( lambda : -amp * sinvp4 * dvdP ),
                 3 : ( lambda : -amp * sinvp4 * dvdp ),
                 4 : ( lambda : -amp * ( sinvp4 + ecc * math.sin( lon ) ) ) }

        partial = numpy.ndarray( ( Tools.length( xdata ), np ) )

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = part[kp]()


        return partial

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative of f to x (df/dx) at the input values.

        dfdx = - p_1 * sin( v + p_4 ) * dvdx

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        pars = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, pars )

        sinE = self.keppler.sinE
        cosE = self.keppler.cosE
        drdx, dvdx = self.keppler.drvdx( xdata, pars, cosE, sinE )

        return - params[1] * numpy.sin( v + params[4] ) * dvdx

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

