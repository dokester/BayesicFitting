import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt
from .NonLinearModel import NonLinearModel
from .Kepplers2ndLaw import Kepplers2ndLaw

__author__ = "Do Kester"
__year__ = 2019
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

class StellarOrbitModel( NonLinearModel ):
    """
    Model for the radial velocity variations of a star caused by a orbiting planet.
.
    The algorithm was taken from
        Cory Boule etal. (2017) J. of Double Star Observations Vol 13 p.189.


    p_0 : e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
    p_1 : a     semi major axis (>0)
    p_2 : P     period of the orbit (>0)
    p_3 : T     time since periastron passage (0<p_3<period)
    p_4 : i     inclination of the orbit wrt sky (0<i<pi; 0 = pi = in sky plane)
    p_5 : Omega position angle of the ascending node (0<Omega<2pi; 0 = north )
    p_6 : omega longitude of periastron (0<omega<2pi; 0 = periastrom in ascending node )

    The parameters are initialized at [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0].
    It is a non-linear model.

    Examples
    --------
    >>> sm = StellarOrbitModel( )
    >>> print( sm.npars )
    7


    """
    TWOPI = 2 * math.pi

    def __init__( self, copy=None, **kwargs ):
        """
        Radial velocity model.

        Number of parameters is 5:

        Parameters
        ----------
        copy : StellarOrbitModel
            model to copy
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]
        names = ["eccentricity", "semimajoraxis", "period", "periastron phase",
                  "inclination", "ascending node", "ascending long"]

        setatt( self, "noutput", 2 )

        super( StellarOrbitModel, self ).__init__( 7, copy=copy, params=param,
                        names=names, **kwargs )

        setatt( self, "keppler", Kepplers2ndLaw() )

    def copy( self ):
        """ Copy method.  """
        return StellarOrbitModel( copy=self )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        p_0 : e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
        p_1 : a     semi major axis
        p_2 : P     period of the orbit (>0)
        p_3 : T     phase since periastron passage (0<p_3<2pi)
        p_4 : i     inclination of the orbit wrt sky (0<i<pi; 0 = orbit in sky plane)
        p_5 : Omega position angle of the ascending node
        p_6 : omega longitude of periastron

        """
        inclin = params[4]
        ascpos = params[5]
        asclon = params[6]

        ( r, v ) = self.keppler.radiusAndTrueAnomaly( xdata, params[:4] )

        vp = v + asclon
        svp = numpy.sin( vp ) * math.cos( inclin )
        cvp = numpy.cos( vp )

        ## theta = angle on sky of stars wrt each other
        theta = numpy.arctan2( svp, cvp ) + ascpos
        ## rho = distance between stars
        rho = r * numpy.sqrt( svp * svp + cvp * cvp )

        result = numpy.zeros( ( len( xdata ), 2 ), dtype=float )

        ## x-position on sky
        result[:,0] = rho * numpy.cos( theta )
        ## y-position on sky
        result[:,1] = rho * numpy.sin( theta )

        return result

    def derivative( self, xdata, params ):
        return self.baseDerivative( xdata, params )

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative (df/dx) of the model function.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        p_0 : e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
        p_1 : a     semi major axis
        p_2 : P     period of the orbit (>0)
        p_3 : p     phase since periastron passage (0<p<2pi)
        p_4 : i     inclination of the orbit wrt sky (0<i<pi; 0 = orbit in sky plane)
        p_5 : O(mega) position angle of the ascending node (0<Omega<2pi)
        p_6 : o(mega) longitude of periastron (0<omega<2pi)

        """
        inclin = params[4]
        ascpos = params[5]
        asclon = params[6]

        dfdx = numpy.zeros( ( len( xdata ), 2 ), dtype=float )

        KL = Kepplers2ndLaw()
        p = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, p )

        cosE = self.keppler.cosE
        sinE = self.keppler.sinE
        drdx, dvdx = self.keppler.drvdx( xdata, p, cosE, sinE )

        vp = v + asclon
        svp = numpy.sin( vp )
        cvp = numpy.cos( vp )
        ci = math.cos( inclin )
        svp2 = svp * svp
        cvp2 = cvp * cvp
        ci2 = ci * ci

        ## theta = angle on sky of stars wrt each other
        theta = numpy.arctan2( svp * ci, cvp ) + ascpos
        dtdv = ci * ( svp2 + cvp2 ) / ( ci2 * svp2 + cvp2 )
        dtdx = dtdv * dvdx

        ## rho = distance between stars
        ssc = numpy.sqrt( svp2 * ci2 + cvp2 )
        rho = r * ssc
        dRdr = ssc
        dRdv = r / ssc * ( svp * cvp * ( ci2 - 1 ) )
        dRdx = dRdr * drdx + dRdv * dvdx

        ct = numpy.cos( theta )
        st = numpy.sin( theta )
        dfdx[:,0] = ct * dRdx - rho * st * dtdx
        dfdx[:,1] = st * dRdx + rho * ct * dtdx

        return dfdx

    def partial( self, xdata, params, parlist=None ) :
        return self.basePartial( xdata, params, parlist=parlist )

    def basePartial( self, xdata, params, parlist=None ) :
        """
        Returns the partials at the xdata value.
        <br>
        The partials are x ( xdata ) to degree-th power.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters. (not used for linear models)
        parlist : array_like
            list of indices active parameters (or None for all)

        p_0 : e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
        p_1 : a     semi major axis
        p_2 : P     period of the orbit (>0)
        p_3 : p     phase since periastron passage (0<p<2pi)
        p_4 : i     inclination of the orbit wrt sky (0<i<pi; 0 = orbit in sky plane)
        p_5 : O     position angle of the ascending node
        p_6 : o     longitude of periastron

        """
        inclin = params[4]
        ascpos = params[5]
        asclon = params[6]

        p = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, p )

        cosE = self.keppler.cosE
        sinE = self.keppler.sinE
        E = self.keppler.eccAnomaly
        drde, drda, drdP, drdp, dvde, dvdP, dvdp = self.keppler.drvdpar( xdata, p,
                                                   E, cosE, sinE )

        vp = v + asclon
        svp = numpy.sin( vp )
        cvp = numpy.cos( vp )
        ci = math.cos( inclin )
        si = math.sin( inclin )
        svp2 = svp * svp
        cvp2 = cvp * cvp
        ci2 = ci * ci

        ## theta = angle on sky of stars wrt each other
        theta = numpy.arctan2( svp * ci, cvp ) + ascpos
        dTdv = ci * ( svp2 + cvp2 ) / ( ci2 * svp2 + cvp2 )

        dTde = dTdv * dvde
        dTda = 0
        dTdP = dTdv * dvdP
        dTdp = dTdv * dvdp
        dTdi = - cvp * svp * si / ( cvp2 + svp2 * ci2 )
        dTdO = 1
        dTdo = dTdv

        ## rho = distance between stars
        ssc = numpy.sqrt( svp2 * ci2 + cvp2 )
        rho = r * ssc
        dRdr = ssc
        dRdv = r / ssc * ( ci2 - 1 ) * svp * cvp

        dRde = dRdr * drde + dRdv * dvde
        dRda = dRdr * drda
        dRdP = dRdr * drdP + dRdv * dvdP
        dRdp = dRdr * drdp + dRdv * dvdp
        dRdi = -r / ssc * svp2 * ci * si
        dRdO = 0
        dRdo = dRdv


        ct = numpy.cos( theta )
        st = numpy.sin( theta )

        rst = rho * st
        rct = rho * ct

        partial0 = numpy.zeros( ( Tools.length( xdata ), self.npbase ), dtype=float )
        partial1 = numpy.zeros( ( Tools.length( xdata ), self.npbase ), dtype=float )

        part0 = { 0 : ( lambda: ct * dRde - rst * dTde ),
                  1 : ( lambda: ct * dRda - rst * dTda ),
                  2 : ( lambda: ct * dRdP - rst * dTdP ),
                  3 : ( lambda: ct * dRdp - rst * dTdp ),
                  4 : ( lambda: ct * dRdi - rst * dTdi ),
                  5 : ( lambda: ct * dRdO - rst * dTdO ),
                  6 : ( lambda: ct * dRdo - rst * dTdo ) }

        part1 = { 0 : ( lambda: st * dRde + rct * dTde ),
                  1 : ( lambda: st * dRda + rct * dTda ),
                  2 : ( lambda: st * dRdP + rct * dTdP ),
                  3 : ( lambda: st * dRdp + rct * dTdp ),
                  4 : ( lambda: st * dRdi + rct * dTdi ),
                  5 : ( lambda: st * dRdO + rct * dTdO ),
                  6 : ( lambda: st * dRdo + rct * dTdo ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial0[:,k] = part0[kp]()
            partial1[:,k] = part1[kp]()

        return ( partial0, partial1 )


    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "StellarOrbit " )

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


