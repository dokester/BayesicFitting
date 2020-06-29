import numpy as numpy
import math
import warnings

from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt

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

class Kepplers2ndLaw( object ):
    """
    Class for calculating Kepplers second law for planetary motion.

    The projection of the orbit on the sky is not included in this class.
.
    The algorithm was taken from
        Cory Boule etal. (2017) J. of Double Star Observations Vol 13 p.189.

        http://www.jdso.org/volume13/number2/Harfenist_189-199.pdf

    p_0 : e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
    p_1 : a     semi major axis (>0)
    p_2 : P     period of the orbit (>0)
    p_3 : T     phase since periastron passage (0<p_3<2 pi)

    The parameters are initialized at [0.0, 1.0, 1.0, 0.0].

    """
    TWOPI = 2 * math.pi
    MAXITER = 100

    def meanAnomaly( self, xdata, params ) :
        """
        Return the mean anomaly.

        P = params[2] = period
        p = params[3] = periastron passage

        M = 2 * pi * xdata / P - p

        Parameters
        ----------
        xdata : array_like
            times in the orbit
        params : array_like
            parameters: eccentr, semimajor, period, ppass
        """
        period = params[2]
        phase = params[3]

        ## return mean anomaly
        return self.TWOPI * xdata / period - phase

    def dMdx( self, xdata, params ) :
        """
        Return derivatives of M (mean anomaly) to xdata

        Returns
        -------
        dMdx : array_like
            derivatives of M to x (xdata)
        """
        period = params[2]
        return numpy.zeros_like( xdata ) + self.TWOPI / period


    def dMdpar( self, xdata, params ) :
        """
        Return derivatives of M (mean anomaly) to relevant parameters.

        Returns
        -------
        dMdP : array_like
            derivatives of M to P (period)
        dMdp : array_like
            derivatives of M to p (phase of periastron)
        """
        period = params[2]

        dMdP = - self.TWOPI * xdata / ( period * period )
        dMdp = -1
        return ( dMdP, dMdp )


    def eccentricAnomaly( self, xdata, params, Estart=None ) :
        """
        Take the best one : Halleys method

        It converges in a few iterations for e <= 0.999999999
        """
        return self.eccentricAnomaly2( xdata, params, Estart=Estart )


    def eccentricAnomaly0( self, xdata, params ) :
        """
        Return the eccentric anomaly, i.e. the solution for E of

        Standard method by Jean Meuss :
            Astronomical Algorithms, 2nd ed.,
            Willmann-Bell, Inc, Virginia, 193-196, 397-399

        e = params[0] = eccentricity
        M = mean anomaly

        E = M + e * sin( E )

        Parameters
        ----------
        xdata : array_like
            times in the orbit
        params : array_like
            parameters: eccentr, semimajor, period, ppass
        """
        M = self.meanAnomaly( xdata, params )
        eccen = params[0]

        Ep = M[:]
        iter = 0
        ## calculate the eccentric anomaly E
        while iter < self.MAXITER :
            sinE = numpy.sin( Ep )
            E = M - eccen * sinE
            iter += 1
            if all( numpy.abs( E - Ep ) < 1e-8 ) : break
            Ep = E
        else :
            print( "EA0: No convergence at iter %d for eccentricity %8.4f" % ( iter, eccen ) )

        setatt( self, "iter", iter )
        return E

    def eccentricAnomaly1( self, xdata, params ) :
        """
        Newtons method.

        Return the eccentric anomaly, i.e. the solution for E of

        e = params[0] = eccentricity
        M = mean anomaly

        E = M + e * sin( E )

        Parameters
        ----------
        xdata : array_like
            times in the orbit
        params : array_like
            parameters: eccentr, semimajor, period, ppass
        """
        M = self.meanAnomaly( xdata, params )
        eccen = params[0]

        Ep = M[:]
        iter = 0
        ## calculate the eccentric anomaly E
        while iter < self.MAXITER :
            sinE = numpy.sin( Ep )
            cosE = numpy.cos( Ep )
            E = Ep - ( M + eccen * sinE - Ep ) / ( eccen * cosE - 1 )
            iter += 1
            if all( numpy.abs( E - Ep ) < 1e-8 ) : break
            Ep = E
        else :
            print( "EA1: No convergence at iter %d for eccentricity %8.4f" % ( iter, eccen ) )

        setatt( self, "iter", iter )
        return E

    def eccentricAnomaly2( self, xdata, params, Estart=None ) :
        """
        Halleys method.

        Return the eccentric anomaly, i.e. the solution for E of

        e = params[0] = eccentricity
        M = mean anomaly

        E = M + e * sin( E )

        Parameters
        ----------
        xdata : array_like
            times in the orbit
        params : array_like
            parameters: eccentr, semimajor, period, phase
        Estart : array_like
            starting values for E
        """
        M = self.meanAnomaly( xdata, params )
        eccen = params[0]


        E = M[:] if Estart is None else Estart

        iter = 0
        ## calculate the eccentric anomaly E
        while iter < self.MAXITER :
            Ep = E
            sinE = numpy.sin( Ep )
            cosE = numpy.cos( Ep )
            es = eccen * sinE
            fx = M + es - Ep
            fp = eccen * cosE - 1

            E = Ep - 2 * fx * fp / ( 2 * fp * fp + fx * es )
            iter += 1
            if all( numpy.abs( E - Ep ) < 1e-8 ) : break
        else :
#            # uncomment for more diagnostics
#            q = numpy.where( numpy.abs( E - Ep ) > 1e-8 )
#            print( "\n" )
#            print( "params  ", fmt( params, max=None ) )
#            print( "Ep      ", fmt( Ep[q] ) )
#            print( "E       ", fmt( E[q] ) )
#            print( "sinE    ", fmt( sinE[q] ) )
#            print( "cosE    ", fmt( cosE[q] ) )

            print( "EA2: No convergence at iter %d for eccentricity %8.4f" % ( iter, eccen ) )

        setatt( self, "iter", iter )
        setatt( self, "sinE", sinE )
        setatt( self, "cosE", cosE )

        return E

    def dEdM( self, xdata, params, cosE ) :
        """
        Return derivatives of E (eccentric anomaly) to mean anomaly

        Returns
        -------
        dEdM : array_like
            derivatives of E to M (mean anomaly)
        """
        eccen = params[0]
        dE = 1.0 / ( 1.0 - eccen * cosE )
        return dE

    def dEdx( self, xdata, params, cosE ) :
        """
        Return derivatives of E (eccentric anomaly) to xdata

        Returns
        -------
        dEdx : array_like
            derivatives of E to x (xdata)
        """
        return self.dEdM( xdata, params, cosE ) * self.dMdx( xdata, params )

    def dEdpar( self, xdata, params, cosE, sinE ) :
        """
        Return derivatives of E (eccentric anomaly) to relevant parameters.

        Returns
        -------
        dEde : array_like
            derivatives of E to e (eccentricity)
        dEdP : array_like
            derivatives of E to P (period)
        dEdp : array_like
            derivatives of E to p (phase of periastron)
        """
        dEdM = self.dEdM( xdata, params, cosE )
        dMdP, dMdp = self.dMdpar( xdata, params )
        dEdp = dEdM * dMdp
        dEdP = dEdM * dMdP
        dEde = dEdM * sinE
        return ( dEde, dEdP, dEdp )


    def radiusAndTrueAnomaly( self, xdata, params ) :
        """
        Return the radius and the true anomaly.

        e = params[0] = eccentricity
        a = params[1] = semimajor axis
        E = eccentric anomaly

        r = a * ( 1 - e * cos( E ) )

        v = 2 * arctan( sqrt( (1+e)/(1-e) ) * tan( E / 2 ) )

        from Wikepedia => Trigoniometic Identities :
        tan( E / 2 ) = sqrt( ( 1 - cos( E ) ) / ( 1 + cos( E ) ) )
                     = sqrt( ( 1 - c ) * ( 1 + c ) / ( 1 + c )^2 )
                     = sqrt( s^2 / ( 1 + c )^2 )
                     = s / ( 1 + c )
                     = sin( E ) / ( 1 + cos( E ) )
        Avoid cases where cos( E ) is too close to -1

        Parameters
        ----------
        xdata : array_like
            times in the orbit
        params : array_like
            parameters: eccentr, semimajor, inclin, ascpos, asclon, period, ppass

        Returns
        -------
        r : array_like
            radius
        v : array_like
            true anomaly

        """
        E = self.eccentricAnomaly( xdata, params )

        eccen = params[0]
        semimaj = params[1]

        ## r = radius
        cosE = self.cosE
        r = semimaj * ( 1 - eccen * cosE )

        ## v = true anomaly
        ef = math.sqrt( ( 1 + eccen ) / ( 1 - eccen ) )

        v = 2 * numpy.arctan2( ef * self.sinE, 1 + cosE )

        setatt( self, "eccAnomaly", E )
        ## return radius and true anomaly
        return ( r, v )

    def drvdE( self, xdata, params, cosE, sinE ) :
        """
        Return derivatives of r (radius) and v (true anomaly) to eccentric anomaly

        Parameters
        ----------
        xdata : array_like
            times in the orbit
        params : array_like
            parameters: eccentr, semimajor, period, ppass
        cosE : array_like
            cosine of E
        sinE : array_like
            sine of E

        Returns
        -------
        drdE : array_like
            derivatives of r to E (eccentric anomaly)
        dvdE : array_like
            derivatives of v to E (eccentric anomaly)
        """

        eccen = params[0]
        semimaj = params[1]

        dr = semimaj * eccen * sinE

        ef = ( 1 + eccen ) / ( 1 - eccen )
        c2 = numpy.where( cosE <= -0.9999999999, 1e10, 1 / ( 1 + cosE ) )
        t2 = ( 1 - cosE ) * c2          ## = tan^2( E/2 )       from Wiki:
        c2 *= 2                         ## = 1 / cos^2( E/2 )   trig identities
        dv = math.sqrt ( ef ) * c2
        dv /= ( ef * t2 + 1 )

        return ( dr, dv )

    def drvdx( self, xdata, params, cosE, sinE ) :
        """
        Return derivatives of r (radius) and v (true anomaly) to xdata

        Returns
        -------
        drdx : array_like
            derivatives of r to x (xdata)
        dvdx : array_like
            derivatives of v to x (xdata)
        """

        drvdE = self.drvdE( xdata, params, cosE, sinE )
        dEdx = self.dEdx( xdata, params, cosE )
        return ( drvdE[0] * dEdx, drvdE[1] * dEdx )

    def drvdpar( self, xdata, params, E, cosE, sinE ) :
        """
        Return derivatives of r (radius) and v (true anomaly) to relevant parameters.

        Returns
        -------
        drde : array_like
            derivatives of r to e (eccentricity)
        drda : array_like
            derivatives of r to a (semimajor axis)
        drdP : array_like
            derivatives of r to P (period)
        drdp : array_like
            derivatives of r to p (phase of periastron)
        dvde : array_like
            derivatives of v to e (eccentricity)
        dvdP : array_like
            derivatives of v to P (period)
        dvdp : array_like
            derivatives of v to p (phase of periastron)
        """
        eccen = params[0]
        semimaj = params[1]

        ( dEde, dEdP, dEdp ) = self.dEdpar( xdata, params, cosE, sinE )
        ( drdE, dvdE ) = self.drvdE( xdata, params, cosE, sinE )

        # r = semimaj * ( 1 - eccen * cosE )
        drdP = drdE * dEdP
        drdp = drdE * dEdp
        drde = drdE * dEde
        drde -= semimaj * cosE
        drda = 1 - eccen * cosE

        dvdP = dvdE * dEdP
        dvdp = dvdE * dEdp

        ef = ( 1 + eccen ) / ( 1 - eccen )
        sef = math.sqrt( ef )
        e2 = ( 1 - eccen ) * ( 1 - eccen )

        c2 = numpy.where( cosE <= -0.9999999999, 1e10, 1 / ( 1 + cosE ) )

        tanE = sinE * c2                ## for tan( E/2 )

        dd1 = 2 * tanE / ( sef * e2 )
        dd2 = dd1 + 2 * sef * dEde * c2
        dvde = dd2 / ( 1 + ef * tanE * tanE )
        dvde = numpy.where( numpy.isnan( dvde ), 0.0, dvde )

        return ( drde, drda, drdP, drdp, dvde, dvdP, dvdp )


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



