import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt
from .NonLinearModel import NonLinearModel
from .Kepplers2ndLaw import Kepplers2ndLaw
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2018 - 2022 Do Kester

class StellarOrbitModel( NonLinearModel ):
    """
    Model for the radial velocity variations of a star caused by a orbiting planet.
.
    The algorithm was taken from
        Cory Boule etal. (2017) J. of Double Star Observations Vol 13 p.189.
        http://www.jdso.org/volume13/number2/Harfenist_189-199.pdf

    p_0 : e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
    p_1 : a     semi major axis (>0)
    p_2 : P     period of the orbit (>0)
    p_3 : T     phase since periastron passage (0<p_3<2pi)
    p_4 : i     inclination of the orbit wrt sky (0<i<pi; 0 = pi = in sky plane)
    p_5 : Omega position angle from North to the line of nodes (0<Omega<pi; 0 = north )
    p_6 : omega longitude from the node (in p_5) to the periastron (0<omega<2pi; 0 = periastron in node )

    Due to the fact that the orbit can be mirrored in the sky plane, one of p_5 or p_6
    has to be limited to [0,pi] and the other to [0,2pi].

    The parameters are initialized at [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0].
    It is a non-linear model.

    This class uses @Kepplers2ndLaw to find the radius and anomaly.

    Attributes
    ----------
    keppler : Kepplers2ndLaw()
        to calculate the radius and true anomaly
    ndout : int
        The number of outputs is 2. Use @MultipleOutputProblem.
    spherical : bool
        if True return the results in spherical coordinates.
    cyclic : { 1 : 2*pi }
        Only if spherical, indicating that result[:,1] is cyclic.

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Examples
    --------
    >>> sm = StellarOrbitModel( )
    >>> print( sm.npars )
    7


    """
    def __init__( self, copy=None, spherical=True, **kwargs ):
        """
        Radial velocity model.

        Number of parameters is 5:

        Parameters
        ----------
        copy : StellarOrbitModel
            model to copy
        spherical : bool (True)
            produce output in sperical coordinates (rho,phi)
            otherwise in rectilinear coordinates (x,y)
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]
        names = ["eccentricity", "semimajoraxis", "period", "phase since periastron",
                  "inclination", "north2nodes", "nodes2periastron"]

        setatt( self, "ndout", 2 )
        setatt( self, "spherical", spherical )

        super( StellarOrbitModel, self ).__init__( 7, copy=copy, params=param,
                        names=names, **kwargs )

        setatt( self, "keppler", Kepplers2ndLaw() )

        if spherical :
            setatt( self, "cyclic", {1:2*math.pi} )

    def copy( self ):
        """ Copy method.  """
        return StellarOrbitModel( spherical=self.spherical, copy=self )

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
        p_1 : a     semi major axis (>0)
        p_2 : P     period of the orbit (>0)
        p_3 : p     phase since periastron passage (0<p<2pi)
        p_4 : i     inclination of the orbit wrt sky (0<i<pi; 0 = orbit in sky plane)
        p_5 : Omega position angle of the line of nodes
        p_6 : omega longitude of periastron from lines of nodes

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
        result[:,0] = rho       ## distance
        result[:,1] = theta     ## positional angle from north counterclock

        if not self.spherical :
            result = self.toRect( result )

        return result

    def toRect( self, rp ):
        """
        Return (x,y) coordinates from (rho,phi)

        Parameters
        ----------
        rp : array
            rp[:,0] : separation of the stars
            rp[:,1] : angle from north (down) CCW to east (right)
        """
        xy = numpy.empty_like( rp )
        xy[:,0] = rp[:,0] * numpy.sin( rp[:,1] )
        xy[:,1] =-rp[:,0] * numpy.cos( rp[:,1] )
        return xy


    def toSpher( self, xy ) :
        """
        Return (rho,phi) coordinates from (x,y)

        Parameters
        ----------
        xy : array
            xy[:,0] : x position
            xy[:,1] : y position
        """
        rp = numpy.empty_like( xy )
        rp[:,0] = numpy.hypot( xy[:,0], xy[:,1] )
        rp[:,1] = numpy.arctan2( xy[:,0], -xy[:,1] )
        return rp

    def XXXderivative( self, xdata, params ):
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
        p_1 : a     semi major axis (>0)
        p_2 : P     period of the orbit (>0)
        p_3 : p     phase since periastron passage (0<p<2pi)
        p_4 : i     inclination of the orbit wrt sky (0<i<pi; 0 = orbit in sky plane)
        p_5 : O(mega) position angle of the line of nodes (0<Omega<pi)
        p_6 : o(mega) longitude of periastron (0<omega<2pi)

        """
        inclin = params[4]
        ascpos = params[5]
        asclon = params[6]

        dfdx = numpy.zeros( ( len( xdata ), 2 ), dtype=float )

        p = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, p )

        cosE = self.keppler.cosE
        cosE = numpy.where( cosE == -1, -0.99999, cosE )
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

        if self.spherical :
            dfdx[:,0] = dRdx
            dfdx[:,1] = dtdx
        else :
            ct = numpy.cos( theta )
            st = numpy.sin( theta )
            dfdx[:,0] = +st * dRdx + rho * ct * dtdx
            dfdx[:,1] = -ct * dRdx + rho * st * dtdx

        return dfdx


    def XXXpartial( self, xdata, params, parlist=None ) :
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
        p_5 : O     position angle of the line of nodes
        p_6 : o     longitude of periastron

        """
        inclin = params[4]
        ascpos = params[5]
        asclon = params[6]

        p = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, p )

        cosE = self.keppler.cosE
        cosE = numpy.where( cosE == -1, -0.99999, cosE )
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

        partial0 = numpy.zeros( ( Tools.length( xdata ), self.npbase ), dtype=float )
        partial1 = numpy.zeros( ( Tools.length( xdata ), self.npbase ), dtype=float )

        ## theta = angle on sky of stars wrt each other
        theta = numpy.arctan2( svp * ci, cvp ) + ascpos
        dTdv = ci * ( svp2 + cvp2 ) / ( ci2 * svp2 + cvp2 )

        ## rho = distance between stars
        ssc = numpy.sqrt( svp2 * ci2 + cvp2 )
        rho = r * ssc
        dRdr = ssc
        dRdv = r / ssc * ( ci2 - 1 ) * svp * cvp


        part0 = { 0 : ( lambda: dRdr * drde + dRdv * dvde ),
                  1 : ( lambda: dRdr * drda ),
                  2 : ( lambda: dRdr * drdP + dRdv * dvdP ),
                  3 : ( lambda: dRdr * drdp + dRdv * dvdp ),
                  4 : ( lambda: -r / ssc * svp2 * ci * si ),
                  5 : ( lambda: 0 ),
                  6 : ( lambda: dRdv ) }

        part1 = { 0 : ( lambda: dTdv * dvde ),
                  1 : ( lambda: 0 ),
                  2 : ( lambda: dTdv * dvdP ),
                  3 : ( lambda: dTdv * dvdp ),
                  4 : ( lambda: -cvp * svp * si / ( cvp2 + svp2 * ci2 ) ),
                  5 : ( lambda: 1 ),
                  6 : ( lambda: dTdv ) }

        if not self.spherical :
            dRde = part0[0]()
            dRda = part0[1]()
            dRdP = part0[2]()
            dRdp = part0[3]()
            dRdi = part0[4]()
            dRdO = 0
            dRdo = part0[6]()

            dTde = part1[0]()
            dTda = 0
            dTdP = part1[2]()
            dTdp = part1[3]()
            dTdi = part1[4]()
            dTdO = 1
            dTdo = part1[6]()

            ct = numpy.cos( theta )
            st = numpy.sin( theta )
            rst = rho * st
            rct = rho * ct
            ct *= -1

            part0 = { 0 : ( lambda: st * dRde + rct * dTde ),
                      1 : ( lambda: st * dRda + rct * dTda ),
                      2 : ( lambda: st * dRdP + rct * dTdP ),
                      3 : ( lambda: st * dRdp + rct * dTdp ),
                      4 : ( lambda: st * dRdi + rct * dTdi ),
                      5 : ( lambda: st * dRdO + rct * dTdO ),
                      6 : ( lambda: st * dRdo + rct * dTdo ) }
            part1 = { 0 : ( lambda: ct * dRde + rst * dTde ),
                      1 : ( lambda: ct * dRda + rst * dTda ),
                      2 : ( lambda: ct * dRdP + rst * dTdP ),
                      3 : ( lambda: ct * dRdp + rst * dTdp ),
                      4 : ( lambda: ct * dRdi + rst * dTdi ),
                      5 : ( lambda: ct * dRdO + rst * dTdO ),
                      6 : ( lambda: ct * dRdo + rst * dTdo ) }


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
        Return the unit of a parameter. (TBC)

        Parameters
        ----------
        k : int
            the kth parameter.

        """

        if k == 0:
            return units.Unit( )
        elif k == 1 :
            return self.yUnit
        elif k == 2 :
            return 1.0 / self.xUnit
        return units.Unit( units.si.rad )


