import sys

import numpy as numpy
from astropy import units
from scipy.signal import lombscargle
import math
from . import Tools
from .Tools import setAttribute as setatt

from .BasicSplinesModel import BasicSplinesModel
from .Fitter import Fitter
from .Formatter import formatter as fmt
from .Formatter import fma

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
#  *    2025 - 2026 Do Kester

class PeriodicScout( object ) :
    """
    Investigating scout for periodic models

    """
    def __init__( self ) :

        self.plotter = DummyPlotter()

    def findPeriod( self, days, flux, pmin=1, pmax=2, grid=1000, clip=2, 
                    verbose=0 ) :
        """
        Find period in  eclipsing star data.

        The search periods are defined as a geometric series, from pmin to pmax with
        NP points, where NP = int( grid * log10( pmax / pmin ) / math.log10( 2 ) )
        That is grid points per octave from pmin to pmax.

        Select eclipsing parts and find the minimum distance

        Parameters
        ----------
        days : array
            Julian days of observation
        flux : array
            measured flux
        pmin : float (1)
            smallest period to be considered
        pmax : float (2)
            largest period to be considered
        grid : int (1000) 
            number of points per octave in pmin to pmax
        clip : float (2)
            select data below median flux minus clip * median abs deviants        
        verbose : int
            0 : silent
            1 : not
        """
        NP = int( 1000 * math.log10( pmax / pmin ) / math.log10( 2 ) )

        pers = numpy.geomspace( pmin, pmax, NP )
        NK = 20
        knots = numpy.linspace( 0, 1, NK )
        bsm = BasicSplinesModel( knots=knots, border=1 )

        prs = numpy.zeros( NP, dtype=float )
        scl = numpy.zeros( NP, dtype=float )

        k = 0
        for ptry in pers :
            dtry = ( days % ptry ) / ptry
            ftr = Fitter( dtry, bsm )

            try :
                ftr.fit( flux )
                prs[k] = ptry
                scl[k] = ftr.scale
                k += 1
            except Exception :
                pass

        ## only k trials are valid
        scl = scl[:k]
        prs = prs[:k]
        km = numpy.argmin( scl[1:k-1] ) + 1

        if verbose :
            print( "Between %8.2f and %8.2f" % ( prs[0], prs[-1] ), 
                   "; minimum at %10.4f scale %8.3f" % ( prs[km], scl[km] ) )

        self.plotter.plotSearch( prs, flux, scl )

        ks = [km-1, km, km+1]
        period, scale = self.downhill( days, flux, prs[ks], scl[ks], verbose=verbose )

        # print( "Period  ", fmt( period ), fmt( scale ) ) 

        km -= grid          ## half the period
        if km > 0 :
            ks = [km-1, km, km+1] 
            per, sca = self.downhill( days, flux, prs[ks], scl[ks], verbose=verbose )
            # print( "Half    ", fmt( per ), fmt( sca ) ) 
            if sca < scale :
                period = per
                scale = sca

        km += 2 * grid      ## double the period
        if km < NP-1 :
            ks = [km-1, km, km+1] 
            per, sca = self.downhill( days, flux, prs[ks], scl[ks], verbose=verbose )
            # print( "Double  ", fmt( per ), fmt( sca ) ) 
            if sca < scale :
                period = per
                scale = sca

        # print( "Period   ", fmt( period ), fmt( scale ) ) 

        self.plotter.close()

        return period, scale


    def downhill( self, days, flux, prs, scl, nrknots=20, tol=0.01, verbose=0 ) :
        """
        Search minimum chisq in a range of periods

        Parameters
        ----------
        days : array
            Julian days of observation
        flux : array
            measured flux
        prs : array 
            list of periods
        scl : array
            pertaining scale of fit
        nrknots : int (20)
            number of knots in BasicSplinesModel
        tol : float (0.001)
            tolerance, stop criterion
        """

        p0 = prs[1]
        c0 = scl[1]
        p1 = prs[0]
        p2 = prs[2]
        c1 = scl[0]
        c2 = scl[2]
        if scl[0] > scl[2] :
            p1, p2 = p2, p1
            c1, c2 = c2, c1

        if verbose :
            print(fmt( prs[1] ), fmt( scl[1] ) )
            print( fmt( c2 - c0 ), fmt( (c0,c1,c2) ), fmt( (p0, p1, p2)) )

        k = 0
        while ( k < 3 ) or ( ( (c2 - c0) > ( tol * c0 ) ) and ( k < 20 ) ) :
            ptry = ( p0 + p2 ) / 2

            knots = numpy.linspace( 0, ptry, nrknots, dtype=float )
            bsm = BasicSplinesModel( knots=knots, border=1 )
            dtry = days % ptry
            ftr = Fitter( dtry, bsm )
            ftr.fit( flux )
            sc = ftr.scale
#            if verbose :
#                print( "Iter %3d  period %10.5f   scale %10.5f" % (k, ptry, sc ), 
#                         fmt( [c0, c1, c2] ), fmt( [p0, p1, p2] ) )

            if sc < c0 :
                c1, p1 = c0, p0
                c0, p0 = sc, ptry
            elif sc < c1 :
                c2, p2 = c1, p1
                c1, p1 = sc, ptry
            else :
                c2, p2 = sc, ptry

            self.plotter.fine( [p0,p2], [c0,c2] )

            k += 1

        if verbose :
            print( "Iter %3d  period %10.5f   scale %10.5f" % (k, p0, c0 ) )

        return p0, c0


    def findParameters( self, days, flux, period, verbose=False, plot=0 ) :
        """
        Return a first guess for the parameters
        eccentricity, phase, longitude

        Parameters
        ----------
        days : array
            time of observations
        flux : array
            flux of observations
        period : float
            the period (from findPeriod() )
        verbose : bool
            print some things
        plot : int
            0   dont plot
            1   plot and show the results
            2   plot but dont show the results
        """
        PI = numpy.pi
        TWOPI = 2 * PI

        ## Lookup table for orbiting times from one latus rectum point to the next
        ## for 20 values of eccentricity [0, 0.05, 0.10, ... 0.95]
        lot = numpy.array( [0.500, 0.468, 0.437, 0.405, 0.373, 0.343, 0.312, 0.282, 
                            0.252, 0.223, 0.196, 0.168, 0.142, 0.118, 0.094, 0.072, 
                            0.052, 0.034, 0.019, 0.007] )
        nlot = 20

        ## Make Splines model for the eclipsing binary
        nrk = 40
        knots = numpy.linspace( 0, period, nrk, dtype=float )
        bsm = BasicSplinesModel( knots=knots, border=1 )
        dtry = days % period

        NP = 500
        xx = numpy.linspace( 0, period, NP )
#        xr = numpy.linspace( 0, TWOPI, NP )

        ftr = Fitter( dtry, bsm )
        par = ftr.fit( flux )
        yfit = bsm.result( xx, par )

        ks = numpy.argsort( yfit )
        kp = km = kmin = ks[0]
       
        ## Find location of primary and secundary minimum
        for kk in ks :
#            print( kk, kp, km )
            if kp <= kk <= ( kp + 1 ) :
                kp = kk
            elif ( km-1 ) <= kk <= km :
                km = kk
            elif abs( kk - kmin ) < 50 :
                continue
            else :
                knxt = kk
                break

        ## relative times (0..1) for 1st and 2nd minimum
        pmin = kmin / NP
        smin = knxt / NP
        
        ## calculate a mimimum for eccentricity
        dt = abs( pmin - smin )
        if dt > 0.5 :
            dt = 1 - dt
        for k in range( 1, nlot ) :
            if dt > lot[k] : 
                break
        ecc = ( k - ( lot[k] - dt ) / ( lot[k] - lot[k-1] ) ) / 20 
    
        ## Phase is the midpoint between the minima
        phas = ( pmin + smin ) * PI
        if abs( pmin - smin ) > 0.5 :
            phas = ( phas + numpy.pi ) % TWOPI


        ## inclination: either 0.5*pi or 1.5*pi
        incl = PI / 2
        prad = pmin * TWOPI         ## primary min in radial
        if prad < phas :
            prad += TWOPI
        if prad - phas < PI / 2 :
            incl += PI 
 
        #if knxt < NP/2 :
        #    incl += numpy.pi

        ymed = numpy.median( yfit )

        ## Find luminosities from minima
        ## At the minimum we have full eclipse. We see 1 star
        f1 = yfit[kmin]  
        f2 = ymed - yfit[kmin]

        ## Find radii from width of minima
        r1 = self.findRadius( xx, yfit, kmin, ymed )
        r2 = self.findRadius( xx, yfit, knxt, ymed )

        ## 
        long = 0.0

        # knxt = ( NP + knxt - kmin ) % NP

        r1 /= period
        r2 /= period

        if verbose :
            print( "InitPars  ", fma( ( ecc, period, phas, incl, long, r1, r2, f1, f2 ) ) )

        return ( ecc, period, phas, incl, long, r1, r2, f1, f2 )


    def findRadius( self, time, yfit, kmin, ymed ) :
        """
        Find the radius of a star from the eclips duration

        Parameters
        ----------
        time : array
            time values of yfit
        yfit : array
            splines fit to the clipsing data
        kmin : int
            index of (local) minimum in yfit
        ymed : float
            median value of yfit
        """
        NP = len( yfit )
        kk = NP // 2
        yf = numpy.roll( yfit, kk - kmin )
        tm = numpy.roll( time, kk - kmin )
        f1 = yf[kk] 
        h1 = ( f1 + ymed ) / 2

        ff = f1
        kp = kk
        while ff < h1 :
            kp += 1
            ff = yf[kp]
        xp = tm[kp]

        km = kk
        ff = f1
        while ff < h1 :
            km -= 1
            ff = yf[km]
        xm = tm[km]

        return xp - xm
                 


class DummyPlotter( object ) :

    def plotSearch( self, prs, flux, scl ) :
        pass

    def fine( self, p, s ) :
        pass

    def close( self ) :
        pass
