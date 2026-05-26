import numpy as numpy
from astropy import units
import math

from . import Tools
from .Tools import setAttribute as setatt
from .NonLinearModel import NonLinearModel
from .StellarOrbitModel import StellarOrbitModel
from .Formatter import fma
from .Formatter import formatter as fmt

from numpy.testing import assert_allclose as assertAC

__author__ = "Do Kester"
__year__ = 2026
__license__ = "GPL3"
__version__ = "3.3.0"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"

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
#  *    2018 - 2026 Do Kester

class EclipsingStarModel( NonLinearModel ) :
    """
    Model for the light curve of an eclipsing double star, as a function of time, t. 

    | par | symbol | name         | description               | limits     | comment      |
    |-----|--------|--------------|---------------------------|------------|--------------|
    | p_0 |   e    | eccentricity | of the elliptic orbit     | 0<e<1      | 0 is circular |
    | p_1 |   P    | period       | of the velocity variation |   P>0      |  |
    | p_2 |   T    | phase        | phase until t = 0         | 0<T<2&pi;  |  |
    | p_3 |   i    | inclination  | of orbit (close to 90)    | 0<i<&pi;   |  |
    | p_4 | &omega;| longitude    | from north to periastron  | 0<&omega;<2&pi; |  |
    | p_5 |   r1   | radius_1     | radius of star 1          | 0<r1<1     |  |
    | p_6 |   r2   | radius_2     | radius of star 2          | 0<r2<1     |  |
    | p_7 |   f1   | lumen_1      | luminosity of star 1      |            |  |
    | p_8 |   f2   | lumen_2      | luminosity of star 2      |            |  |
    | p_9 |   fs   | spot         | spot illumination         | fs >= 0    | 0 is no spot |
    | p_10|   m1   | mass_1       | relative mass of star 1   | 0 < m1 < 1 | m2 = 1 - m1 |

    The amplitude (semimajor axis) is set to 1.0. Both stellar radii are given 
    as a fraction of the amplitude. The mass of star 2 is ( 1 - m1 ). The mass ratio
    is used in calculating the tidal distortion.

    When the sum of the radii, p_5 + p_6, is larger than the periastron distance,
    1 - p_0, the stars clash.

    When the model is constructed as circular, the parameter p_0 becomes 0 by 
    definition and p_4 looses its meaning. They are removed from the model.

    This class uses @StellarOrbitModel to find the true orbit

    The parameters are initialized at 
        [0.0, 1.0, 0.0, pi/2, 0.0, 0.1, 0.1, 1.0, 1.0, 0.0, 0.5].
    It is a non-linear model.

    For the mathematics of this model and further explanation see @EclipsingStars.html.

    (Partial) derivatives were obtained with the help of  
    @www.derivative-calculator.net
    Muchas Gracias


    Attributes
    ----------
    storbit : StellarOrbitModel
        to calculate the true stellar orbit
    circular : bool
        whether the orbit is circular (eccentricity == phase == longitude == 0)
    spot : bool
        apply spot illumination and tidal distortion
    tides : bool
        apply tidal distortion
    occultation : bool
        True: eclipses stricty enforced
    fixpar : lambda function
        to provide parameters for StellarOrbitModel

    Examples
    --------
    >>> esm = EclipsingStarModel( spot=True, tides=True )
    >>> print( esm.npars )
    >>> 10


    """
    TWOPI = 2 * math.pi

    def __init__( self, circular=False, spot=False, tides=False, occultation=True, 
                  copy=None, **kwargs ):
        """
        Radial velocity model.

        Number of parameters depends on the settings of ( False or True ) of 
         circular       spot        tides
        ( 9 or 6 ) + ( 0 or 1 ) + ( 0 or 1 )

        Parameters
        ----------
        circular : bool
            stellar orbit is circular: eccentricity = 0 ==> lonod = 0
        spot : bool or number
            apply spot illumination; more pronounced when spot > 1
        tides : bool
            apply tidal distortion
        occultation : bool (True)
            eclipses are stricty enforced
        copy : EclipsingStarModel
            model to copy
        """

        if circular :
            npar = 7
            param = [1.0, math.pi/2, 0, 0, 0, 1, 1]
            names = ["period", "phase", "inclination",  
                     "radius_1", "radius_2", "lumen_1", "lumen_2"]
            # fix parameters for StellarOrbitModel
            setatt( self, "fixpar", ( lambda x : [0.0, 1.0, x[0], x[1], x[2], 0.0, 0.0] ) )

        else :
            npar = 9
            param = [0.0, 1.0, 0.0, math.pi/2, 0.0, 0, 0, 1, 1]
            names = ["eccentricity", "period", "phase", "inclination", "longitude", 
                     "radius_1", "radius_2", "lumen_1", "lumen_2"]
            # fix parameters for StellarOrbitModel
            setatt( self, "fixpar", ( lambda x : [x[0], 1.0, x[1], x[2], x[3], 0.0, x[4]] ) )

        if spot :
            param += [0.0]
            names += ["spot"]
            npar += 1

        if tides :
            param += [1.0]
            names += ["mass_1"]
            npar += 1

        setatt( self, "circular", circular )
        setatt( self, "tides", tides )        ## tides same as spot
        ## force spot to be a number
        setatt( self, "spot", spot + 0 )

        setatt( self, "occultation", occultation )

        if "debug" in kwargs and kwargs["debug"] :          ## present and True
            from .Formatter import formatter_init 
            formatter_init( linelength=100 )
            setatt( self, "_assertDeriv", self._debugDeriv ) 
            setatt( self, "_assertParts", self._debugParts ) 
        else :                                              ## default
            setatt( self, "_assertDeriv", self._nodebug )
            setatt( self, "_assertParts", self._nodebug )

        super().__init__( npar, copy=copy, params=param, names=names, **kwargs )

        setatt( self, "storbit", StellarOrbitModel( spherical=False ) )


    def copy( self ):
        """ 
        Copy method.  
        """
        return EclipsingStarModel( circular=self.circular, spot=self.spot, 
                                   tides=self.tides, copy=self )

    def distanceConstraint( self, logL, problem, allpars, lowLhood ) :
        """
        Constrain the sizes of the stars for use in NestedSampling to avoid collapse.
        and the inclination to ensure eclipses

        Parameters
        ----------
        logL : float
            log Likelihood obtained with allpars
        problem : Problem
            to solve
        allpars : array
            all parameters involved in the problem
        lowLhood : float
            present value of the likelihood constraint
        """
        return self.logCombiPrior( allpars )


    def logCombiPrior( self, allpars ) :
        """
        Get extra prior for this combination of parameters.

        Parameters
        ----------
        allpars : array
            all parameters involved in the problem
        """
        eccen  = self.getParameterValue( allpars, "eccentricity", default=0 )
        inclin = self.getParameterValue( allpars, "inclination" )
        lonod  = self.getParameterValue( allpars, "longitude", default=0 )

        perdis = 1 - eccen

        r1 = self.getParameterValue( allpars, "radius_1" )
        r2 = self.getParameterValue( allpars, "radius_2" )

        if self.tides :
            m1 = self.getParameterValue( allpars, "mass_1" )
            mr = ( 1 - m1 ) / m1

            ## eps : flattening of the sphere
            eps1 = 3.75 * mr * ( r1 / perdis )**3
            eps2 = 3.75 / mr * ( r2 / perdis )**3
            if ( eps1 > 0.6 ) or ( eps2 > 0.6 ) :
                return -math.inf
        else :
            if ( 1.4 * ( r1 + r2 ) ) > perdis :
                return -math.inf 

        if not self.occultation :
            return 0

        ## calculate distance between stars at eclipse (= lonod+90)
        m  = 1 / math.tan( lonod - math.pi / 2 )    # co-tangus
        m2 = m ** 2
        e2 = eccen ** 2
        a = 1 - e2 + m2
        b = 2 * m2 * eccen
        c = m2 * e2 - 1 + e2
        det = math.sqrt( b*b - 4 * a * c )
        x1 = ( -b + det ) / ( 2 * a )
        y1 = ( x1 + eccen ) * m
        d1 = math.sqrt( y1 ** 2 + ( x1 + eccen ) ** 2 )
        x2 = ( -b - det ) / ( 2 * a )
        y2 = ( x2 + eccen ) * m 
        d2 = math.sqrt( y2 ** 2 + ( x2 + eccen ) ** 2 )
        if d1 > d2 :
            d1,d2 = d2,d1

        ci = abs( math.cos( inclin ) )

        if r2 > r1 :
            r1,r2 = r2,r1

        rp = ( r1 + r2 ) / d2
        rm = ( r1 - r2 ) / d1

        if ( perdis < 1.4 * rp ) :             ## avoid collapse
            logPrior = -math.inf
        elif ci > rp :                         ## no eclipse
            logPrior = -math.inf
        elif ci < rm :                         ## eclipse
            logPrior = 0
        else :                                 ## partial eclipse
            logPrior = math.log( ( rp - ci ) / ( rp - rm ) ) 

        return logPrior

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
        x, y, z = self.storbit.getOrbit( xdata, self.fixpar( params ), d3=True )

        xy = numpy.sqrt( x*x + y*y )
        result = self.lightCurve( xy, z, params ) 

        return result

    def lightCurve( self, xy, z, params, debug=0 ):
        """
        Return the visible area of two eclipsing stars, multiplied by their luminicities.

        Adapted from 
            https://scipython.com/books/book2/chapter-8-scipy/problems/overlapping-circles/

        Parameters
        ----------
        xy : arrey
            distance between the stars in the sky plane
        z : array
            distance of star 2 to the sky plane
        params : array
            of the model
        debug : int
            debug partial derivativesin stages

        """
        ## radii and luminosities of both stars
        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )
        f1 = self.getParameterValue( params, "lumen_1" )
        f2 = self.getParameterValue( params, "lumen_2" )

        ## Calculate tidal distortion: normalized apparent major and minor axis
        ## Need to be scaled with r1 or r2. 
        a1, b1, a2, b2 = self.tidalDistortion( xy, z, params )

        if debug == 1 :
            return ( a1, b1, a2, b2 )

        ## Find the fraction of each star, visible during the orbit
        vf1, vf2 = self.visibleFraction( xy, z, r1*a1, r2*a2 )
        if debug == 2 :
            return ( vf1, vf2 )

        ## spot illumination for close binaries.
        ## results in an array for f1 and f2 scaled with the normalized star surface
        f1, f2 = self.spotIllumination( xy, z, params )

        if debug == 3 :
            return ( f1, f2 )

        f1 *= a1 * b1
        f2 *= a2 * b2

        if debug == 4 :
            return ( f1, f2 )

        lc = vf1 * f1 + vf2 * f2

        return lc

    def visibleFraction( self, xy, z, r1, r2 ) :
        """
        Calculate the fraction of visibility for both stars.

        If z is positive, star 2 is in front of star 1    
        If z is negative, star 2 is behind star 1    

        Parameters
        ----------
        xy : array
            distance between overlapping circles
        z : array
            distance of star 2 to the sky plane
        r1 : float or array
            radius of star 1
        r2 : float or array
            radius of star 2
        """
        overlap = self.overlap( xy, r1, r2 )

        area1 = math.pi * r1 * r1
        area2 = math.pi * r2 * r2

        vf1 = numpy.where( z < 0, 1, 1 - overlap / area1 )
        vf2 = numpy.where( z > 0, 1, 1 - overlap / area2 )

        return ( vf1, vf2 )

    def VFderivative( self, xy, z, r1, r2 ) :
        """
        Calculate the derivatives for the visible fraction to xy and z
 
        Parameters
        ----------
        xy : array
            distance between overlapping circles
        z : array
            distance of star 2 to the sky plane
        r1 : float or array
            radius of star 1
        r2 : float or array
            radius of star 2

        Returns
        ------- 
        ( dV1dx, dV2dx, dV1dz, dV2dz )
            derivatives of the visibility to xy and z

        """
        dOdx = self.OVderivative( xy, r1, r2 )

        area1 = math.pi * r1 * r1
        area2 = math.pi * r2 * r2

        dV1dx = numpy.where( z < 0, 0, -dOdx / area1 )
        dV2dx = numpy.where( z > 0, 0, -dOdx / area2 )

        dV1dz = numpy.zeros_like( z )
        dV2dz = numpy.zeros_like( z )

        return ( dV1dx, dV2dx, dV1dz, dV2dz )


    def VFpartial( self, xy, z, r1, r2 ) :
        """
        Calculate the partial derivatives for the visible fraction to r1 and r2.
 
        Parameters
        ----------
        xy : array
            distance between overlapping circles
        z : array
            distance of star 2 to the sky plane
        r1 : float or array
            radius of star 1
        r2 : float or array
            radius of star 2

        Returns
        ------- 
        ( dV1dr1, dV2dr1, dV1dr2, dV2dr2 )
            partials of the visibility to r1 and r2

        """
        overlap = self.overlap( xy, r1, r2 )

        area1 = math.pi * r1 * r1
        area2 = math.pi * r2 * r2

        dA1dr1 = 2 * math.pi * r1
        dA2dr2 = 2 * math.pi * r2        

        dOdr1, dOdr2 = self.OVpartial( xy, r1, r2 )

        dV1dr1 = numpy.zeros_like( z ) 
        dV1dr2 = numpy.zeros_like( z ) 
        dV2dr1 = numpy.zeros_like( z ) 
        dV2dr2 = numpy.zeros_like( z ) 

        q = numpy.where( ( z > 0 ) & ( overlap > 0 ) )
        a1q = area1[q]
        a2q = area2[q]
        dV1dr1[q] = -( dOdr1[q] * a1q - dA1dr1[q] * overlap[q] ) / ( a1q * a1q )
        dV1dr2[q] = -( dOdr2[q] / a1q )

        q = numpy.where( ( z < 0 ) & ( overlap > 0 ) )
        a1q = area1[q]
        a2q = area2[q]
        dV2dr1[q] = -( dOdr1[q] / a2q )
        dV2dr2[q] = -( dOdr2[q] * a2q - dA2dr2[q] * overlap[q] ) / ( a2q * a2q )

        return ( dV1dr1, dV2dr1, dV1dr2, dV2dr2 )

 
    def overlap( self, xy, r1, r2 ) :
        """
        Calculate the overlap area between two partially overlapping circles

        From: https://scipython.com/books/book2/chapter-8-scipy/problems/overlapping-circles/
    
        Parameters
        ----------
        xy : array
            distance between overlapping circles
        r1 : float or array
            radius of circle 1
        r2 : float or array
            radius of circle 2
        """
        ## When completely behind each other, the overlap is the minimum area
        ## set rest to 0 for no overlap at all
        minarea = math.pi * numpy.minimum( r1, r2 )**2 
        overlap = numpy.where( xy < abs( r1 - r2 ), minarea, 0 )

        ## Partial overlap
        q = numpy.where( ( xy > abs( r1 - r2 ) ) & ( xy < r1 + r2 ) )[0]

        r1q = r1 if isinstance( r1, float ) else r1[q]
        r2q = r2 if isinstance( r2, float ) else r2[q]
        xyq = xy[q]
        d2 = xyq * xyq
        r1sq = r1q * r1q
        r2sq = r2q * r2q

        alfa = numpy.arccos( ( d2 + r2sq - r1sq ) / ( 2 * xyq * r2q ) )
        beta = numpy.arccos( ( d2 + r1sq - r2sq ) / ( 2 * xyq * r1q ) )
        overlap[q] = ( r2sq * alfa + r1sq * beta - 0.5 * 
                 ( r2sq * numpy.sin( 2 * alfa ) + r1sq * numpy.sin( 2 * beta ) ) )

        return overlap


    def spotIllumination( self, xy, z, params ) :
        """
        Illumination of the stars on each other.
        Depending on distance between stars and aspect angle

        The algoritm is taken from DOI: 10.5817/OEJV2025-0258

        Parameters
        ----------
        xy : array
            distance between the stars in the sky plane
        z : array
            distance of star 2 to the sky plane
        params : array
            parameters of the model

        """
        f1 = self.getParameterValue( params, "lumen_1" )
        f2 = self.getParameterValue( params, "lumen_2" )

        ## no spot --> return just the luminosities.
        if not self.spot :
            return ( f1, f2 )

        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )
        fs = self.getParameterValue( params, "spot" ) 
  
        rho2 = ( xy * xy + z * z )
        sp2 = fs * f1 * ( r1 * r1 / rho2 ) ** self.spot
        sp1 = fs * f2 * ( r2 * r2 / rho2 ) ** self.spot

        ## cosine defining the aspect angle
        aspect = z / numpy.sqrt( rho2 )

        ## illumination of star 2 by s 1 is most visible when z < 0
        sp2 *= 1 - aspect

        ## illumination of star 1 by s 2 is most visible when z > 0
        sp1 *= 1 + aspect

        return ( f1 + sp1, f2 + sp2 )

    def tidalDistortion( self, xy, z, params ) :
        """
        Calculate the tidal distortion of the stars in a binary system
        as elongated, prolate spheroids (cigars).

        from: https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node69.html
        Equation. (1.468) (for as long as it lasts)

        Parameters
        ----------
        xy : array
            distance between the stars in the sky plane
        z : array
            distance of star 2 to the sky plane
        params : array
            parameters of the model

        Returns
        -------
        ( a1, b1, a2, b2 )
            apparent stretch and squeeze of both stars
        """
        if not self.tides :
            ones = numpy.ones_like( xy )
            return ( ones, ones, ones, ones )

        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )
        m1 = self.getParameterValue( params, "mass_1" )

        mr = ( 1 - m1 ) / m1

        rho = numpy.hypot( xy, z )
        rho3 = rho ** 3
        r1c = r1 ** 3
        r2c = r2 ** 3

        ## eps : flattening of the sphere
        eps1 = 15 / 4 * ( r1c / rho3 ) * mr
        eps2 = 15 / 4 * ( r2c / rho3 ) / mr

        ## b goes imaginary when eps > 1
        b1 = ( 1 - eps1 ) ** ( 1 / 3 )      ## minor axis for star 1
        b2 = ( 1 - eps2 ) ** ( 1 / 3 )      ## minor axis for star 2

        ## use approximation that cannot go negative when eps > 1
        # b1 = 1 / ( 1 + eps1 ) ** ( 1 / 3 )
        # b2 = 1 / ( 1 + eps2 ) ** ( 1 / 3 )
        
        t1 = 1 / (b1*b1)                    ## true major factor for star 1
        t2 = 1 / (b2*b2)                    ## true major factor for star 2

        ## Apparent major axis is the projection along theta
        a1 = numpy.hypot( t1 * xy, b1 * z ) / rho
        a2 = numpy.hypot( t2 * xy, b2 * z ) / rho

        setatt( self, "truemajor", (t1,t2) )

        return ( a1, b1, a2, b2 )


    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        x,y,z = SOM(t:p1)

        r = S(x,y,z) = ( SQRT( x*x + y*y ), z )

        F(t:p,q) = SOM(t:p) | R(x,y,z:) | LC(r,z:q)
                 = LC( R( SOM( t:p ) ):q )
                   H(G(x:p):q)

        dF/dq = dLC( R( SOM(t:p)))/dq

        dF/dp = dLC/drz * dRZ/dxyz * dSOM/dp

        Parameters
        ----------
        xdata : array
            values at which to calculate the result
        params : array
            values for the parameters.
        parlist : array
            list of indices active parameters (or None for all)

        """
        if self.circular :
            plist = [2, 3, 4]          ## period phase and inclination
        else :
            plist = [0, 2, 3, 4, 6]    ## also eccentricity and longitude
        plist = numpy.array( plist )

        fpar = self.fixpar( params )

        x, y, z = self.storbit.getOrbit( xdata, fpar, d3=True )
        xy = numpy.hypot( x, y )
 
        ## partials to p (params of StellarOrbitModel)
        dxdp, dydp, dzdp = self.storbit.basePartial( xdata, fpar, parlist=plist, d3=True )

        ## RZ(x,y,z) = ( sqrt( x*x + y*y ), z )
        ## dRZdp = ( dRZdx * dxdp + dRZdy * dydp, dRZdz * dzdp ) 
        dRdp = ( x * dxdp.T + y * dydp.T ) / xy
        dZdp = dzdp.T

        ## LC = LC(r,z:q)
        dLCdx, dLCdz = self.LCderivative( xy, z, params )

        ## dFdp = dLCdx * dRdp + dLCdz * dZdz 
        dFdp = dLCdx * dRdp + dLCdz * dZdp          ## for p in plist (SOM)

        ## for params in LC :
        dLCdq = self.LCpartial( xy, z, params )

        partial = numpy.append( dFdp.T, dLCdq, 1 )

        return partial

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative of f to t (dfdt) at the input values.

        Parameters
        ----------
        xdata : array
            times at which to calculate the result
        params : array
            values for the parameters.

        """
        fpar = self.fixpar( params )
        x, y, z = self.storbit.getOrbit( xdata, fpar, d3=True )
        xy = numpy.hypot( x, y )

        dfdt = self.storbit.baseDerivative( xdata, fpar, d3=True )
        dxdt = dfdt[:,0]
        dydt = dfdt[:,1]
        dzdt = dfdt[:,2]

        drdt = ( x * dxdt + y * dydt ) / xy

        dLCdx, dLCdz = self.LCderivative( xy, z, params )

        return dLCdx * drdt + dLCdz * dzdt


    def OVpartial( self, xy, r1, r2 ) :
        """
        calculate the partials of overlap to r1 and r2.

        Parameters
        ----------
        xy : array
            projected distance between stars
        r1 : array
            radius of star 1
        r2 : array
            radius of star 2

        """
        dOdr1 = numpy.where( r1 > r2, 0.0,  
                    numpy.where( xy < r1 + r2, 2 * math.pi * r1, 0.0 ) )
        dOdr2 = numpy.where( r1 < r2, 0.0,  
                    numpy.where( xy < r1 + r2, 2 * math.pi * r2, 0.0 ) )

        q = numpy.where( ( xy > abs( r1 - r2 ) ) & ( xy < r1 + r2 ) )[0]

        xyq = xy[q]
        r1 = r1[q]
        r2 = r2[q]

        d2 = xyq * xyq
        rr1 = r1 * r1
        rr2 = r2 * r2

        r2d = xyq * numpy.sqrt( 1 - ( d2 - rr1 + rr2 )**2 / ( 4 * rr2 * d2 ) )
        dAdr1 = r1 / ( r2 * r2d )
        dAdr2 = ( d2 - rr1 - rr2 ) / ( 2 * rr2 * r2d )

        r1d = xyq * numpy.sqrt( 1 - ( d2 - rr2 + rr1 )**2 / ( 4 * rr1 * d2 ) )
        dBdr1 = ( d2 - rr1 - rr2 ) / ( 2 * rr1 * r1d )
        dBdr2 = r2 / ( r1 * r1d )

        alfa = numpy.arccos( ( d2 + rr2 - rr1 ) / ( 2 * xyq * r2 ) )
        beta = numpy.arccos( ( d2 + rr1 - rr2 ) / ( 2 * xyq * r1 ) )

        dOdA = rr2 * ( 1 - numpy.cos( 2 * alfa ) )
        dOdB = rr1 * ( 1 - numpy.cos( 2 * beta ) )

        dr1 = ( 2 * beta - numpy.sin( 2 * beta ) ) * r1
        dr2 = ( 2 * alfa - numpy.sin( 2 * alfa ) ) * r2

        dr1 += dOdA * dAdr1 + dOdB * dBdr1
        dr2 += dOdA * dAdr2 + dOdB * dBdr2

        dOdr1[q] = dr1
        dOdr2[q] = dr2

        return ( dOdr1, dOdr2 )
        
    def SIpartial( self, xy, z, params, surface=(1,1) ) :
        """
        Returns partials of the SpotIllumination.
        Specificly of the modified f1 and f2 to params[-5:] 
        (radius_1, radius_2, lumen_1, lumen_2, spot) 

        If no spot illumination is requested, the dF*dfs are returned as zero.

        Parameters
        ----------
        xy : array
            distance between the stars in the sky plane
        z : array
            distance of star 2 to the sky plane
        params : array
            values for the parameters.
        surface : tuple of arrays
            normalized surface areas of the stars

        Returns
        -------
        ( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs,
          dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs )

        """
        ones = numpy.ones_like( z )
        zero = numpy.zeros_like( z )

        if not self.spot :
            return ( zero, zero, ones*surface[0], zero, zero,
                     zero, zero, zero, ones*surface[1], zero )
        
        spot = self.spot

        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )
        f1 = self.getParameterValue( params, "lumen_1" )
        f2 = self.getParameterValue( params, "lumen_2" )
        fs = self.getParameterValue( params, "spot" )

        rr1 = r1 * r1
        rr2 = r2 * r2

        d2 = xy * xy + z * z
        d = numpy.sqrt( d2 )

        ## F2 = f2 + fs * f1 * ( 1 - z / d ) * ( rr1 / d2 ) ** spot
        ## F1 = f1 + fs * f2 * ( 1 + z / d ) * ( rr2 / d2 ) ** spot

        sifrac = surface[1] * ( 1 - z / d ) / ( d2 ** spot )

        dF2dr1 = fs * f1 * sifrac * 2 * spot * r1 ** (2 * spot - 1)
        dF2dr2 = zero
        sifrac *= rr1 ** spot
        dF2df1 = fs * sifrac
        dF2df2 = ones * surface[1]
        dF2dfs = f1 * sifrac

        sifrac = surface[0] * ( 1 + z / d ) / ( d2 ** spot )

        dF1dr1 = zero
        dF1dr2 = fs * f2 * sifrac * 2 * spot * r2 ** ( 2 * spot - 1 ) 
        dF1df1 = ones * surface[0]
        sifrac *= rr2 ** spot
        dF1df2 = fs * sifrac
        dF1dfs = f2 * sifrac

        return ( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs, 
                 dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs )


    def LCpartial( self, xy, z, params ) :
        """
        Return partial derivatives of LightCurve to each of the parameters

        Parameters
        ----------
        xy : array
            distance between the stars in the sky plane
        z : array
            distance of star 2 to the sky plane
        params : array
            parameters of the model
        """
        ## radii and luminosities of both stars
        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )

        ## tidalDistortion : partials
        tdresult = self.tidalDistortion( xy, z, params )
        tdpart = self.TDpartial( xy, z, params, TDresult=tdresult )

        self._assertParts( xy, z, params, tdpart, debug=1 )

        a1, b1, a2, b2 = tdresult
        da1dm, db1dm, da2dm, db2dm, da1dr, db1dr, da2dr, db2dr = tdpart

        ra1 = a1 * r1
        ra2 = a2 * r2

        V1, V2 = self.visibleFraction( xy, z, ra1, ra2 )
        dV1dra1, dV2dra1, dV1dra2, dV2dra2 = self.VFpartial( xy, z, ra1, ra2 )
        

        ## partials to mass_1
        dV1dm1 = dV1dra1 * r1 * da1dm + dV1dra2 * r2 * da2dm
        dV2dm1 = dV2dra1 * r1 * da1dm + dV2dra2 * r2 * da2dm

        ## convert from partials to ra1,ra2 to partials to r1,r2
        dra1dr1 = a1 + r1 * da1dr
        dra2dr2 = a2 + r2 * da2dr

        dV1dr1 = dV1dra1 * dra1dr1 
        dV1dr2 = dV1dra2 * dra2dr2 
        dV2dr1 = dV2dra1 * dra1dr1 
        dV2dr2 = dV2dra2 * dra2dr2 

        self._assertParts( xy, z, params, 
            ( dV1dr1, dV2dr1, dV1dr2, dV2dr2, dV1dm1, dV2dm1 ), debug=2 )


        ## spotIllumination : partials with effects of tidalDistortion
        F1, F2 = self.spotIllumination( xy, z, params )
        surface1 = a1 * b1                            ## normalized star surface
        surface2 = a2 * b2                            ## normalized star surface

        sipart = self.SIpartial( xy, z, params )

        self._assertParts( xy, z, params, sipart, debug=3 )

        sipart = tuple( [df * surface1 for df in sipart[:5]] + 
                        [df * surface2 for df in sipart[5:]] )

        ( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs, 
          dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs ) = sipart

        dS1dr1 = a1 * db1dr + b1 * da1dr
        dS2dr2 = a2 * db2dr + b2 * da2dr

        dF1dr1 += F1 * dS1dr1
        dF2dr2 += F2 * dS2dr2

        dF1dm1 = F1 * ( a1 * db1dm + b1 * da1dm )
        dF2dm1 = F2 * ( a2 * db2dm + b2 * da2dm )

        self._assertParts( xy, z, params, 
            ( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs, dF1dm1, 
              dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs, dF2dm1 ), debug=4 )

        F1 *= surface1
        F2 *= surface2

        ## lightCurve : partials
        ## LC = V1 * F1 + V2 * F2
        ## dLCdp = dV1dp * F1 + V1 * dF1dp + dV2dp * F2 + V2 * dF2dp
        dLCdr1 = dV1dr1 * F1 + V1 * dF1dr1 + dV2dr1 * F2 + V2 * dF2dr1
        dLCdr2 = dV1dr2 * F1 + V1 * dF1dr2 + dV2dr2 * F2 + V2 * dF2dr2
        dLCdf1 = V1 * dF1df1 + V2 * dF2df1
        dLCdf2 = V1 * dF1df2 + V2 * dF2df2

        dLCdp = numpy.append( dLCdr1, dLCdr2 )
        dLCdp = numpy.append( dLCdp, dLCdf1 )
        dLCdp = numpy.append( dLCdp, dLCdf2 )
        ksh = 4

        if self.spot :
            dLCdfs = V1 * dF1dfs + V2 * dF2dfs
            dLCdp = numpy.append( dLCdp, dLCdfs )
            ksh += 1

        if self.tides :
            dLCdm1 = dV1dm1 * F1 + V1 * dF1dm1 + dV2dm1 * F2 + V2 * dF2dm1
            dLCdp = numpy.append( dLCdp, dLCdm1 )
            ksh += 1

        dLCdp = dLCdp.reshape( ( ksh, -1 ) ).T

        self._assertParts( xy, z, params, dLCdp, debug=5, doprint=False )

        return dLCdp


    def TDpartial( self, xy, z, params, TDresult=None ) :
        """
        Calculate partials of the tidal distortion to the distortion parameter

        Parameters
        ----------
        xy : array
            distance between the stars in the sky plane
        z : array
            distance of star 2 to the sky plane
        params : array
            parameters of the model
        TDresult : None or tuple
            result of a call to tidalDistortion

        Returns
        -------
        ( da1dm, db1dm, da2dm, db2dm,  da1dr, db1dr, da2dr, db2dr ) : 8 arrays
            Partials of the normalized projected axes to the parameters
        """
        if not self.tides :
            zr = numpy.zeros_like( z )
            return ( zr, zr, zr, zr, zr, zr, zr, zr )

        if TDresult is None :
            a1, b1, a2, b2 = self.tidalDistortion( xy, z, params )
        else :
            a1, b1, a2, b2 = TDresult
        t1, t2 = self.truemajor

        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )
        m1 = self.getParameterValue( params, "mass_1" )

        mr = ( 1 - m1 ) / m1
        dmrdm = - 1 / ( m1 * m1 )

        r1c = r1 * r1 * r1
        r2c = r2 * r2 * r2

        xy2 = xy * xy
        z2  = z * z
        rho2 = xy2 + z2
        rho = numpy.sqrt( rho2 )
        rho3 = rho * rho2

        ## eps : flattening of the sphere
        eps1 = 3.75 * mr * r1c / rho3
        eps2 = 3.75 / mr * r2c / rho3

        de1dr = 11.25 * mr * r1 * r1 / rho3 
        de2dr = 11.25 / mr * r2 * r2 / rho3
        de1dm =  3.75 * r1c * dmrdm / rho3
        de2dm = -3.75 * r2c * dmrdm / ( rho3 * mr * mr )

        ## use approximation that cannot go negative when eps > 1
        # b1 = ( 1 + eps1 ) ** ( -1 / 3 )
        # b2 = ( 1 + eps2 ) ** ( -1 / 3 )

        # db1de = -( 1 / 3 ) * ( 1 + eps1 ) ** ( -4/3 )
        # db2de = -( 1 / 3 ) * ( 1 + eps2 ) ** ( -4/3 )

        ## use flattening as b = a ( 1 - eps )
        ## and a * b * b = r**3
        # b1 = ( 1 - eps1 ) ** ( 1 / 3 )
        # b2 = ( 1 - eps2 ) ** ( 1 / 3 )
        
        db1de = -( 1 / 3 ) * ( 1 - eps1 ) ** ( -2/3 )
        db2de = -( 1 / 3 ) * ( 1 - eps2 ) ** ( -2/3 )
        db1dr = db1de * de1dr 
        db1dm = db1de * de1dm
        db2dr = db2de * de2dr
        db2dm = db2de * de2dm

        # t1 = 1 / (b1*b1)                    ## true major factor for star 1
        # t2 = 1 / (b2*b2)                    ## true major factor for star 2

        dt1db = -2 / b1**3
        dt2db = -2 / b2**3

        dt1dr = dt1db * db1dr
        dt1dm = dt1db * db1dm
        dt2dr = dt2db * db2dr
        dt2dm = dt2db * db2dm

        ## Apparent major axis is the projection along theta
        ## a1 = numpy.hypot( t1 * xy, b1 * z ) / rho
        ## a1 = sqrt( t1**2 * xy**2 + b1**2 * z**2 ) / rho
        ## dadp = ( xy**2 * t * dtdp + z**2 * b * dbdp ) / ( rho * sqrt() )

        rsr1 = rho * numpy.hypot( t1 * xy, b1 * z )
        rsr2 = rho * numpy.hypot( t2 * xy, b2 * z )

        da1dm = ( xy2 * t1 * dt1dm + z2 * b1 * db1dm ) / rsr1
        da1dr = ( xy2 * t1 * dt1dr + z2 * b1 * db1dr ) / rsr1
        da2dm = ( xy2 * t2 * dt2dm + z2 * b2 * db2dm ) / rsr2
        da2dr = ( xy2 * t2 * dt2dr + z2 * b2 * db2dr ) / rsr2

        return ( da1dm, db1dm, da2dm, db2dm, 
                 da1dr, db1dr, da2dr, db2dr )

    def OVderivative( self, xy, r1, r2 ) :
        """
        calculate the derivative of overlap to xy

        Parameters
        ----------
        xy : array
            projected distance between stars
        r1 : array
            radius of star 1
        r2 : array
            radius of star 2

        """
        dOdr = numpy.zeros_like( xy )

        q = numpy.where( ( xy >= abs( r1 - r2 ) ) & ( xy <= r1 + r2 ) )
        dov = xy[q]

        if isinstance( r1, numpy.ndarray ) :
            r1 = r1[q]
            r2 = r2[q]

        d2 = dov * dov
        rr1 = r1 * r1
        rr2 = r2 * r2
        dAdr =  -( d2 - rr2 + rr1 ) / ( 2 * r2 * d2 * 
                    numpy.sqrt( 1 - ( d2 + rr2 - rr1 )**2 / ( 4 * rr2 * d2 ) ) )
        dBdr =  -( d2 - rr1 + rr2 ) / ( 2 * r1 * d2 * 
                    numpy.sqrt( 1 - ( d2 + rr1 - rr2 )**2 / ( 4 * rr1 * d2 ) ) )
        dOdA = 2 * rr2 * ( 1 - ( (d2 + rr2 - rr1) / (2 * r2 * dov) )**2 )
        dOdB = 2 * rr1 * ( 1 - ( (d2 + rr1 - rr2) / (2 * r1 * dov) )**2 )

        dOdr[q] = dOdA * dAdr + dOdB * dBdr
        return dOdr

    def LCderivative( self, xy, z, params ) :
        """
        Return derivative of LightCurve to xy and z, as 

        Parameters
        ----------
        xy : array
            distance between the stars in the sky plane
        z : array
            distance of star 2 to the sky plane
        params : array
            parameters of the model

        """
        ## radii and luminosities of both stars
        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )

        ## Calculate tidal distortion: normalized apparent major and minor axis
        ## Need to be scaled with r1 or r2. 
        tdresult = self.tidalDistortion( xy, z, params )
        tdderiv  = self.TDderivative( xy, z, params, TDresult=tdresult )
        a1, b1, a2, b2 = tdresult

        self._assertDeriv(  xy, z, params, tdderiv, debug=1 )

        ## Find overlap area between two circles of radius r1 and r2
        ##  at distances xy; r1,r2 depend on distortion 
        ra1 = r1 * a1
        ra2 = r2 * a2

        ## Take in account the dependency of r1,r2 on xy in tidalDistortion
        ## now also in z
        da1dx, db1dx, da2dx, db2dx, da1dz, db1dz, da2dz, db2dz = tdderiv

        ## multiply by these to get true surfaces
        surface1 = a1 * b1
        surface2 = a2 * b2

        ## derivatives of surface
        ds1dx = b1 * da1dx + a1 * db1dx
        ds2dx = b2 * da2dx + a2 * db2dx
        ds1dz = b1 * da1dz + a1 * db1dz
        ds2dz = b2 * da2dz + a2 * db2dz

        f1, f2 = self.spotIllumination( xy, z, params )
        ( df1dx, df2dx, df1dz, df2dz ) = self.SIderivative( xy, z, params )

        self._assertDeriv(  xy, z, params, ( df1dx, df2dx, df1dz, df2dz ), debug=3 )

        F1 = f1 * surface1
        F2 = f2 * surface2

        ## Add dependency on surface to lumens: F1 = f1 * surface1
        dF1dx = surface1 * df1dx + f1 * ds1dx
        dF2dx = surface2 * df2dx + f2 * ds2dx
        dF1dz = surface1 * df1dz + f1 * ds1dz
        dF2dz = surface2 * df2dz + f2 * ds2dz

        self._assertDeriv(  xy, z, params, ( dF1dx, dF2dx, dF1dz, dF2dz ), debug=4 )

        V1, V2 = self.visibleFraction( xy, z, ra1, ra2 )
        dV1dx, dV2dx, dV1dz, dV2dz = self.VFderivative( xy, z, ra1, ra2 )
        dV1dra1, dV2dra1, dV1dra2, dV2dra2 = self.VFpartial( xy, z, ra1, ra2 )

        q = numpy.where( z > 0 )
        dV1dx[q] += dV1dra1[q] * r1 * da1dx[q] + dV1dra2[q] * r2 * da2dx[q]
        dV1dz[q] += dV1dra1[q] * r1 * da1dz[q] + dV1dra2[q] * r2 * da2dz[q]

        q = numpy.where( z < 0 )
        dV2dx[q] += dV2dra1[q] * r1 * da1dx[q] + dV2dra2[q] * r2 * da2dx[q]
        dV2dz[q] += dV2dra1[q] * r1 * da1dz[q] + dV2dra2[q] * r2 * da2dz[q]

        self._assertDeriv(  xy, z, params, ( dV1dx, dV2dx, dV1dz, dV2dz ), 
                           debug=2, doprint=False )

        ## LC = V1 * F1 + V2 * F2
        dLCdx = V1 * dF1dx + F1 * dV1dx + V2 * dF2dx + F2 * dV2dx
        dLCdz = V1 * dF1dz + F1 * dV1dz + V2 * dF2dz + F2 * dV2dz

        self._assertDeriv(  xy, z, params, ( dLCdx, dLCdz ), debug=5 )

        return ( dLCdx, dLCdz )

    def SIderivative( self, xy, z, params, surface=(1,1) ) :
        """
        Returns derivatives of the SpotIllimunation.
        Specificly of the modified f1 and f2 to xy and z 

        Parameters
        ----------
        xy : float
            distance between the stars in the sky plane
        z : float
            distance of star 2 to the sky plane
        params : array_like
            values for the parameters.
        surface : tuple of 2 array
            normalized surface areas of the stars

        Returns
        -------
        ( dF1dx, dF2dx, dF1dz, dF2dz )

        """
        if not self.spot :
            zeros = numpy.zeros_like( z )
            return ( zeros, zeros, zeros, zeros )

        ## radii and luminosities of both stars
        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )
        f1 = self.getParameterValue( params, "lumen_1" )
        f2 = self.getParameterValue( params, "lumen_2" )
        fs = self.getParameterValue( params, "spot" )

        rr1 = r1 * r1
        rr2 = r2 * r2

        s = self.spot
        fr1s = surface[0] * fs * f1 * rr1 ** s
        fr2s = surface[1] * fs * f2 * rr2 ** s
        s2 = 2 * s
        sp1 = s2 + 1
        sp2 = s2 + 2

        R2 = xy * xy + z * z
        R = numpy.sqrt( R2 )
        dRdx = xy / R
        dRdz = z / R

        ## F2 = f2 + ( fs * f1 * ( rr1 / d2 ) ** s ) * ( 1 - z / d )
        ##    = f2 + ( fs * f1 * rr1 ** s ) * ( 1 / d**(2*s) - z / d**(2*s+1) )
        ##    = f2 + fr1s * ( d**(-2s) - z * d**(-2s-1) )
        ## F1 = f1 + fr2s * ( d**(-2s) + z * d**(-2s-1) )

        ## FD2 = d**(-2s) - z * d**(-2s-1)
        ## dFD2dR = -2s * d**(-2s-1) + z * (2s+1) * d**(-2s-2)
        ## dFD2dz = -d**(-2s-1) + dFZdd * dddz
        ## FD1 = d**(-2s) + z * d**(-2s-1)
        ## dFD1dR = -2s * d**(-2s-1) - z * (2s+1) * d**(-2s-2)
        ## dFD1dz =  d**(-2s-1) + dF1dd * dddz

        ## dF2dx = dF2dR * dRdx
        ## dF2dz = dF2dz + dF2dR * dRdz

        ds  = -R**(-sp1)
        dzs2 = ( s2 * ds + z * sp1 * R**(-sp2) )
        dzs1 = ( s2 * ds - z * sp1 * R**(-sp2) )

        dF2dx = fr1s * dzs2 * dRdx
        dF1dx = fr2s * dzs1 * dRdx
        dF2dz = fr1s * ( ds + dzs2 * dRdz )
        dF1dz = fr2s * (-ds + dzs1 * dRdz )

        return ( dF1dx, dF2dx, dF1dz, dF2dz )

    def TDderivative( self, xy, z, params, TDresult=None ) :
        """
        Calculate the derivative of the tidal distortion to xy and z

        Parameters
        ----------
        xy : array
            distance between the stars in the sky plane
        z : array
            distance of star 2 to the sky plane
        params : array
            parameters of the model
        TDresult : tuple
            result of call tp tidalDostortion

        Returns
        -------
        ( da1dx, db1dx, da2dx, db2dx, da1dz, db1dz, da2dz, db2dz )
            derivatives of apparent major and minor axes to xy and z
        """
        if not self.tides :
            zeros = numpy.zeros_like( z )
            return ( zeros, zeros, zeros, zeros, zeros, zeros, zeros, zeros )

        if TDresult is None :
            a1, b1, a2, b2 = self.tidalDistortion( xy, z, params )
        else :
            a1, b1, a2, b2 = TDresult
        t1,t2 = self.truemajor

        r1 = self.getParameterValue( params, "radius_1" )
        r2 = self.getParameterValue( params, "radius_2" )
        m1 = self.getParameterValue( params, "mass_1" )
        mr = ( 1 - m1 ) / m1

        r1c = r1**3
        r2c = r2**3
        xy2 = xy * xy
        z2 = z * z
        rho2 = xy2 + z2
        rho = numpy.sqrt( rho2 )
        dRhodx = xy / rho
        dRhodz = z / rho

        rho3 = rho2 * rho
        rho4 = rho2 * rho2

        ## eps : flattening of the sphere
        eps1 = 3.75 * mr * r1c / rho3
        eps2 = 3.75 / mr * r2c / rho3

        de1drho = -11.25 * mr * r1c / rho4
        de2drho = -11.25 / mr * r2c / rho4 

        ## use b = a ( 1 - eps ) and a * b * b = r**3
        ## b = ( 1 - eps ) ** ( 1 / 3 )

        db1drho = ( -1 / 3 ) * ( 1 - eps1 ) ** ( -2/3 ) * de1drho
        db2drho = ( -1 / 3 ) * ( 1 - eps2 ) ** ( -2/3 ) * de2drho

        db1dx = db1drho * dRhodx
        db1dz = db1drho * dRhodz
        db2dx = db2drho * dRhodx
        db2dz = db2drho * dRhodz

        ## t = 1 / (b*b)
        ## dtdb = -2 / b**3
        dt1db = -2 / b1**3
        dt2db = -2 / b2**3
        dt1dx = dt1db * db1dx 
        dt2dx = dt2db * db2dx
        dt1dz = dt1db * db1dz 
        dt2dz = dt2db * db2dz

        ## Apparent major axis is the projection along theta
        ##   a1 = numpy.sqrt( t1**2 * xy**2 + b1**2 * z**2 ) / rho
        ##      = Hyp / rho
        ## dHdx = ( xy**2 * t1 * dtdx + xy * t1**2 + z**2 * b1 * dbdx ) / Hyp

        h1 = numpy.hypot( t1 * xy, b1 * z )
        h2 = numpy.hypot( t2 * xy, b2 * z )

        dH1dx = ( xy2 * t1 * dt1dx + xy * t1 * t1 + z2 * b1 * db1dx ) / h1
        dH2dx = ( xy2 * t2 * dt2dx + xy * t2 * t2 + z2 * b2 * db2dx ) / h2
        dH1dz = ( xy2 * t1 * dt1dz + z  * b1 * b1 + z2 * b1 * db1dz ) / h1
        dH2dz = ( xy2 * t2 * dt2dz + z  * b2 * b2 + z2 * b2 * db2dz ) / h2

        da1dx = ( dH1dx * rho - h1 * dRhodx ) / rho2
        da1dz = ( dH1dz * rho - h1 * dRhodz ) / rho2
        da2dx = ( dH2dx * rho - h2 * dRhodx ) / rho2
        da2dz = ( dH2dz * rho - h2 * dRhodz ) / rho2

        return ( da1dx, db1dx, da2dx, db2dx, da1dz, db1dz, da2dz, db2dz )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "EclipsingStar " )

    def _XXXbaseParameterUnit( self, k ):
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

    def reportParameters( self, param, stdevs=None, toMags=False ) :
        """
        Print parameters and stdevs (if present)

        Parameters
        ----------
        param : array
            to be converted and printed
        stdevs : array 
            to be converted and printed
        toMags : bool or float (False)
            true    convert luminosities to magnitudes
            float   true and use number as scaling factor
        """
        TWOPI = 2 * math.pi
        f360 = 360
        tp10 = TWOPI * 10

        ## multiply with factor, f, and keep within [0,f]
        mp = lambda x, f : ( x * f / TWOPI ) % f
        if toMags :
            fm = float( toMags )
            fc = lambda x, f : -2.512 * math.log10( x * f )
            funit = "magnitude"
        else :
            fm = 1.0
            fc = lambda x, f : x
            funit = ""

        if stdevs is None :
            p0 = lambda k : ( "%10.3f" % param[k] ) 
            ps = lambda k,f : ( "%10.3f" % mp( param[k], f ) ) 
            pf = lambda k,f : ( "%10.3f" % fc( param[k], f ) ) 
        else :
            p0 = lambda k : ( "%10.3f +- %.3f" % ( param[k], stdevs[k] ) ) 
            ps = lambda k,f : ( ( "%10.3f +- %.3f" if stdevs[k] < tp10/f else "%10.3f +- %.2f" )
                                  % ( mp( param[k], f ), mp( stdevs[k], f ) ) ) 
            pf = lambda k,f : ( "%10.3f +- %.3f" % ( fc( param[k], f ),abs( fc( stdevs[k]+1, 1 ) ) ) ) 


        if self.circular :

            fper = param[0]
            print( "%-12.12s :" % self.getParameterName( 0 ), p0( 0 ), "days" )
            print( "%-12.12s :" % self.getParameterName( 1 ), ps( 1, fper ), "days since 2010.0" )
            print( "%-12.12s :" % self.getParameterName( 2 ), ps( 2, f360 ), "degrees" )
            k = 3
        else :        
            fper = param[1]
            print( "%-12.12s :" % self.getParameterName( 0 ), p0( 0 ) )
            print( "%-12.12s :" % self.getParameterName( 1 ), p0( 1 ), "days" )
            print( "%-12.12s :" % self.getParameterName( 2 ), ps( 2, fper ), "days since 2010.0" )
            print( "%-12.12s :" % self.getParameterName( 3 ), ps( 3, f360 ), "degrees" )
            print( "%-12.12s :" % self.getParameterName( 4 ), ps( 4, f360 ), "degrees" )
            k = 5

        print( "%-12.12s :" % self.getParameterName( k ), p0( k ) )
        k += 1
        print( "%-12.12s :" % self.getParameterName( k ), p0( k ) )
        k += 1
        print( "%-12.12s :" % self.getParameterName( k ), pf( k, fm ), funit )
        k += 1
        print( "%-12.12s :" % self.getParameterName( k ), pf( k, fm ), funit )
        k += 1

        if self.spot :
            print( "%-12.12s :" % self.getParameterName( k ), p0( k ) )
            k += 1
        if self.tides :
            print( "%-12.12s :" % self.getParameterName( k ), p0( k ) )

        return


    def _nodebug( self, xy, z, pars, dfs, debug=0, doprint=False ) :
        pass

    def _debugParts( self, xy, z, pars, dfs, debug=0, doprint=False ) :

        if doprint:
            print( "debug  Parts :", debug, len( dfs ) )

        np = self.npbase
        km = ks = []
        zs = numpy.zeros_like( dfs[0] )
        tol = 0.001
        if self.tides :
            np -= 1
            km = [np]
        elif debug == 1 :
            for k, df in enumerate( dfs ) :
                msg = ( "tides %d %s" % 
                      ( k, fma( df, indent=8 ) ) )
                self._assertPrint( df, zs, tol, msg, doprint=doprint )
            return

        if self.spot :
            np -= 1
            ks = [np]
        elif debug == 3 :
#            ons = numpy.ones_like( z )
#            for k, df in enumerate( dfs ) :
#                msg = ( "spot  %d %s" % 
#                      ( k, fma( df, indent=8 ) ) )
#                self._assertPrint( df, ons, tol, msg, doprint=doprint )
            return
        
        kf2 = [np - 1]
        kf1 = [np - 2]
        kr2 = [np - 3]
        kr1 = [np - 4]

        if debug == 1 :
            plist = km + kr1 + kr2
            pn = ["mr", "r1", "r2"]
            rn = ["a1", "b1", "a2", "b2"]
            dfr = ( dfs[0], dfs[1], dfs[2], dfs[3], dfs[4], dfs[5], 
                    zs, zs, zs, zs,  dfs[6], dfs[7] )
            dfs = dfr
        elif debug == 2 :
            plist = kr1 + kr2 + km
            rn = ["V1", "V2"]
            pn = ["r1", "r2", "mr"]
        elif debug == 12 :
            plist = kr1 + kr2 + km
            rn = ["Ov"]
            pn = ["r1", "r2", "mr"]
        elif debug == 3 :
            plist = kr1 + kr2 + kf1 + kf2 + ks
            rn = ["F1", "F2"]
            pn = ["r1", "r2", "f1", "f2", "fs"]
        elif debug == 4 :
            plist = kr1 + kr2 + kf1 + kf2 + ks + km
            rn = ["F1", "F2"]
            pn = ["r1", "r2", "f1", "f2", "fs", "mr"]
        else :
            plist = kr1 + kr2 + kf1 + kf2 + ks + km
            rn = ["LC"]
            pn = ["r1", "r2", "f1", "f2", "fs", "mr"]
            ln = dfs.shape[1]
            df = [dfs[:,k] for k in range( ln )]
            dfs = tuple( df )

        if doprint :
            for df in dfs :
                print( fmt( df, tail=5 ) )

        n = 0
        nk = len( rn )

        np = len( dfs ) // 2 if debug > 2 else 1
        for k, kp in enumerate( plist ) :
            msp = "====%s==par %d===\n" % ( self.getParameterName( kp ), kp ) 

            p = pars.copy()
            p[kp] += 0.0001
            yp = self.lightCurve( xy, z, p, debug=debug )
            p[kp] -= 0.0002
            ym = self.lightCurve( xy, z, p, debug=debug )

            if isinstance( yp, numpy.ndarray ) :
                nmdr = ( yp - ym ) / 0.0002
                msg = ( "%sd%sd%s  %s\nnumer   %s" % 
                      ( msp, rn[0], pn[k], fma( dfs[k], indent=8 ), fma( nmdr, indent=8 ) ) )
                self._assertPrint( dfs[k], nmdr, tol, msg, doprint=doprint )
                continue

            if debug > 2 :
                n = k
            # print( k, kp, nk, np )
            for i in range( nk ) :
                nmdr = ( yp[i] - ym[i] ) / 0.0002
                dfr = dfs[n]
                msg1 = ( "%sd%sd%s  %s\nnumer   %s" % 
                       ( msp, rn[i], pn[k], fma( dfr, indent=8 ), fma( nmdr, indent=8 ) ) )
#                print( msg1 )
                self._assertPrint( dfr, nmdr, tol, msg1, doprint=doprint )
                n += np

        return

    def _assertPrint( self, df, nm, tol, msg, doprint=False ) :
        if doprint :
            print( msg )
            q = numpy.where( abs( df - nm ) > ( tol + tol * abs( nm ) ) )
            if len( q ) > 0 :
                print( "errors at  ", fma( q[0], indent=12 ) )

        else :
            assertAC( df, nm, tol, tol, err_msg=msg )


    def _debugDeriv( self, xy, z, pars, dfs, debug=0, doprint=False ) :
        
        if doprint :
            print( "debug  Deriv :", debug, len( dfs ) )

        if debug == 1 :
            rn = ["a1", "b1", "a2", "b2"]
        elif debug == 2 :
            rn = ["V1", "V2"]
        elif debug == 3 :
            rn = ["F1", "F2"]
        elif debug == 4 :
            rn = ["F1", "F2"]
        else :
            rn = ["LC"]

        xp = xy + 0.0001
        xm = xy - 0.0001

        ypr = self.lightCurve( xp, z, pars, debug=debug )
        ymr = self.lightCurve( xm, z, pars, debug=debug )

        zp = z + 0.0001
        zm = z - 0.0001

        ypz = self.lightCurve( xy, zp, pars, debug=debug )
        ymz = self.lightCurve( xy, zm, pars, debug=debug )

        tol = 0.001
        if isinstance( ypr, numpy.ndarray ) :
            nmdr = ( ypr - ymr ) / 0.0002
            nmdz = ( ypz - ymz ) / 0.0002

            msg1 = "d%sdx   %s\nnmdx    %s" % ( rn[0], 
                    fma( dfs[0], indent=8 ), fma( nmdr, indent=8 ) )
            self._assertPrint( dfs[0], nmdr, tol, msg1, doprint=doprint )

            msg2 = "d%sdz   %s\nnmdz    %s" % ( rn[0], 
                    fma( dfs[1], indent=8 ), fma( nmdz, indent=8 ) )
            self._assertPrint( dfs[1], nmdz, tol, msg2, doprint=doprint )
            return

        nk = len( ypr )
        for k in range( nk ) :
            nmdr = ( ypr[k] - ymr[k] ) / 0.0002
            nmdz = ( ypz[k] - ymz[k] ) / 0.0002

            dfr = dfs[k]
            dfz = dfs[k+nk]

            msg1 = "d%sdx   %s\nnmdx    %s" % ( rn[k], 
                    fma( dfr, indent=8 ), fma( nmdr, indent=8 ) )
            self._assertPrint( dfr, nmdr, tol, msg1, doprint=doprint )

            msg2 = "d%sdz   %s\nnmdz    %s" % ( rn[k], 
                    fma( dfz, indent=8 ), fma( nmdz, indent=8 ) )
            self._assertPrint( dfz, nmdz, tol, msg2, doprint=doprint )


        return

