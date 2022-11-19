# run with : python3 -m unittest TestPrior2
# or :       python3 -m unittest TestPrior2.Test.test1

import unittest
import numpy as numpy
import math
import os
import matplotlib.pyplot as plt

from BayesicFitting import Prior, UniformPrior, JeffreysPrior, ExponentialPrior
from BayesicFitting import LaplacePrior, CauchyPrior, GaussPrior
from BayesicFitting import UniformPrior
from BayesicFitting import PolynomialModel, NestedSampler
from BayesicFitting import GaussErrorDistribution

from BayesicFitting import GaussPriorNew
from BayesicFitting import ClassicProblem
from BayesicFitting import Fitter
from BayesicFitting import NestedSampler
from BayesicFitting import formatter as fmt

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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
#  *  2006-2015 Do Kester (JAVA CODE)

class Test( unittest.TestCase ) :
    """
    Test for Priors
    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def addPrior( self, logL, problem, allpars, logLlow ):
        return logL + GaussPrior( center=0.5, scale=0.5/6 ).logResult( allpars[0] )

    def test1( self ) :

        print( "===========Gauss Prior Limitation ===========" )

        NP = 100
        x = numpy.zeros( NP, dtype=float )
        y = 0.4  + 0.2 * numpy.random.randn( NP )

#        print( numpy.mean( numpy.append( y, [5.0] ) ) )

        mdl = PolynomialModel( 0 )

        mdl.setPrior( 0, GaussPrior( center=0.5, scale=0.5/6 ) )

        ed = GaussErrorDistribution( scale=0.2 )
        ns = NestedSampler( x, mdl, y, verbose=2, distribution=ed )
        ns.ensemble = 500

        logE = ns.sample()

        pars = ns.parameters
        stdv = ns.stdevs
        print( pars, stdv, logE )
        maxL = ns.samples[-1].logL
        print( maxL + math.log( stdv ) )

#        lim = math.exp( 4 )
        mdl.setPrior( 0, UniformPrior( limits=[0.0,1.0] ) )

        
        ed = GaussErrorDistribution( scale=0.2 )
        ed.constrain = self.addPrior
        ns = NestedSampler( x, mdl, y, verbose=2, distribution=ed )
        ns.ensemble = 500
        logE = ns.sample()

        pars = ns.parameters
        stdv = ns.stdevs
        print( pars, stdv, logE )
        maxL = ns.samples[-1].logL
        print( maxL + math.log( stdv ) )

    def test2( self ) :

        print( "=============Plot Gauss Prior==============" )
        
        NP = 171
        x = numpy.linspace( -8.5, 8.5, NP, dtype=float )
        u = numpy.linspace( 0, 1, NP, dtype=float )

        gp = GaussPrior( )
        res = gp.result( x )
        print( numpy.sum( res ) / 10 ) 

        if not self.doplot :
            return

        plt.plot( x, res, 'k-' )

        d = []
        for xx in x :
            d += [gp.domain2Unit( xx )]
        d = numpy.array( d )

        plt.plot( x[1:-1], d[1:-1], 'r-' )


        dd = ( d - numpy.roll( d, -2 ) ) / ( x - numpy.roll( x, -2 ) )
        plt.plot( x[3:-1], dd[2:-2], 'g-' )

        gn = GaussPriorNew( )
        res = gp.result( x )
        print( numpy.sum( res ) / 10 ) 

        plt.plot( x, res, 'b-' )

        d = []
        for xx in x :
            d += [gn.domain2Unit( xx )]
        d = numpy.array( d )

        plt.plot( x[1:-1], d[1:-1], 'c-' )


        dd = ( d - numpy.roll( d, -2 ) ) / ( x - numpy.roll( x, -2 ) )
        plt.plot( x[3:-1], dd[2:-2], 'm-' )

        plt.show()

    def testlogL( self ) :

        s = 1 / math.sqrt( 2.0 )
        x = numpy.asarray( [0.0] )      # [2014., 2015., 2016., 2017., 2018., 2019.] )
        y = numpy.asarray( [0.0] )      # [150., 145., 140., 150., 160., 154.] )
        w = numpy.zeros( 1, dtype=float ) + 1 / ( s *s )

        print( w )

        mdl0 = PolynomialModel( 0 )

        prob1 = ClassicProblem( model=mdl0, xdata=x, ydata=y )
        prob2 = ClassicProblem( model=mdl0, xdata=x, ydata=y, weights=w )

        pp = numpy.linspace( -10, 10, 201, dtype=float )

        ed = GaussErrorDistribution( )

        logL1 = numpy.asarray( [ed.logLikelihood( prob1, [p, 1.0] ) for p in pp] )
        logL2 = logL1 + logL1
        logLE = [ed.logLikelihood( prob1, [p, s] ) for p in pp]
        logLW = [ed.logLikelihood( prob2, [p, 1.0] ) for p in pp]

        if not self.doplot :
            return

        plt.plot( pp, numpy.exp( logL1 ), 'k-' )
#        plt.plot( pp, 0.1 + numpy.exp( logL2 ), 'k-' )
#        plt.plot( pp, 0.2 + numpy.exp( logL1 ) ** 2, 'k-' )
        plt.plot( pp, numpy.exp( logLE ), 'r-' )
        plt.plot( pp, numpy.exp( logLW ), 'g-' )

#        plt.plot( pp, ( logL1 ), 'k-' )
#        plt.plot( pp, ( logLE ), 'r-' )
#        plt.plot( pp, ( logLW ), 'g-' )

        plt.xlabel( "residual" )
        plt.ylabel( "likelihood" )

        plt.show()


    def testm0( self ) :
        x = numpy.asarray( [2014., 2015., 2016., 2017., 2018., 2019.] )
        y = numpy.asarray( [155., 145., 140., 150., 160., 154.] )

        x -= 2013

        mdl0 = PolynomialModel( 0 )

        gp = GaussPrior( center=150, scale=20 )
        gn = GaussPriorNew( center=150, scale=20 )
        up = UniformPrior( limits=[130,170] )

        problem = ClassicProblem( model=mdl0, xdata=x, ydata=y )

        w = numpy.zeros( 6, dtype=float ) + 2
        prob2 = ClassicProblem( model=mdl0, xdata=x, ydata=y, weights=w )

        dp = 0.1
        pp = numpy.linspace( 130, 170, 401, dtype=float )

        ed = GaussErrorDistribution( )

        su = 0
        sg = 0.0
        sn = 0.0
        logU = up.logResult( 150 )
        ll = []
        for p in pp :
            logL = ed.logLikelihood( problem, [p, 5.0] )
            logG = gp.logResult( p )
            logN = gn.logResult( p )
            su += math.exp( logL + logU )
            sg += math.exp( logL + logG )
            sn += math.exp( logL + logN )
            ll += [logL]

        plt.plot( pp, numpy.exp( ll ), 'k-' )

        su *= dp
        sg *= dp
        sn *= dp

        print( "1  LogZold  ", fmt( math.log( sg ) ), "  LogZnew  ", fmt( math.log( sn ) ), " LogZuni  ", fmt( math.log( su ) ) )

        mdl0.setPrior( 0, up )
        ftr = Fitter( x, mdl0 )
        par = ftr.fit( y )
        ftr.fixedScale = 5.0        

        print( fmt( par ), fmt( ftr.logZ ), fmt( ftr.getLogZ( limits=[130,170] ) ) )

        ed.scale = 5.0
        engs = ["gibbs", "chord"]

        ns = NestedSampler( problem=prob2, engines=engs, distribution=ed, verbose=1 )
        ev2 = ns.sample()
       
        ns = NestedSampler( problem=problem, engines=engs, distribution=ed, verbose=1 )

        ev = ns.sample()
        print( fmt( ev ), fmt( ev2 ) )

        sl = ns.samples
        pml = numpy.average( [sl[k].parameters for k in range( -100, 0 )] )

        pev = sl.getParameterEvolution( kpar=0 )
        lev = sl.getLogLikelihoodEvolution()

        if self.doplot :
            plt.plot( pev, numpy.exp( lev ), 'r.' )

        print( fmt( ns.parameters ), fmt( pml ), fmt( ns.logZ ), " +- ", fmt( ns.logZprecision ) )

        print( fmt( math.log( su ) / ns.logZ ) )

        indx = numpy.argsort( pev )

        ip = pev[indx]
        il = lev[indx]

        print( fmt( ip ), fmt( numpy.roll( ip, -1 ) ) )

        dip = numpy.roll( ip, -1 )[:-1] - ip[:-1]
        print( fmt( dip ) )

        print( fmt( numpy.sum( dip ) ) )
        lin = numpy.sum( dip * numpy.exp( il[:-1] + logU ) )
        print( fmt( math.log( lin ) ) )
        print( fmt( math.log( numpy.sum( numpy.exp( sl.getLogWeightEvolution() ) ) ) ) )

#        lz = -sys.float_info.max

        if self.doplot :
            plt.show()

    def testm1( self ) :
        x = numpy.asarray( [2014., 2015., 2016., 2017., 2018., 2019.] )
        y = numpy.asarray( [155., 145., 140., 150., 160., 154.] )

        x -= 2013

        mdl = PolynomialModel( 1 )

        gp0 = GaussPrior( center=150, scale=20 )
        gn0 = GaussPriorNew( center=150, scale=20 )
        gp1 = GaussPrior( center=0, scale=20 )
        gn1 = GaussPriorNew( center=0, scale=20 )
        up0 = UniformPrior( limits=[130,170] )
        up1 = UniformPrior( limits=[-20,20] )

        problem = ClassicProblem( model=mdl, xdata=x, ydata=y )

        NPP = 71
        nh = NPP // 2

        pp0 = numpy.linspace( 150 - nh, 150 + nh, NPP, dtype=float )
        pp1 = numpy.linspace( -nh, nh, NPP, dtype=float )

        ed = GaussErrorDistribution( )

        sg = 0.0
        sn = 0.0
        su = 0.0
        logU0 = up0.logResult( 150 )
        logU1 = up1.logResult( 0 )
        for p0 in pp0 :
            logG0 = gp0.logResult( p0 )
            logN0 = gn0.logResult( p0 )
            for p1 in pp1 :
                logL = ed.logLikelihood( problem, [p0, p1, 5.0] )
                logG1 = gp1.logResult( p1 )
                logN1 = gn1.logResult( p1 )
                sg += math.exp( logL + logG0 + logG1 )
                sn += math.exp( logL + logN0 + logN1 )
                su += math.exp( logL + logU0 + logU1 )


        print( "2  LogZold  ", fmt( math.log( sg) ), "  LogZnew  ", fmt( math.log( sn ) ), " LogZuni  ", fmt( math.log( su ) ) )

        mdl.setPrior( 0, up0 )
        mdl.setPrior( 1, up1 )

        ftr = Fitter( x, mdl )
        par = ftr.fit( y )
        ftr.fixedScale = 5.0        

        print( fmt( par ), fmt( ftr.logZ ), fmt( ftr.getLogZ( limits=[[130,-20],[170,20]] ) ) )

        ed.scale = 5.0
        engs = ["gibbs", "chord"]
        ns = NestedSampler( problem=problem, distribution=ed, verbose=1, ensemble=400, engines=engs )
        ns.minimumIterations = 1000

        ev = ns.sample()

        print( fmt( ns.parameters ), fmt( ns.logZ ), " +- ", fmt( ns.logZprecision ) )


    def testm2( self ) :
        x = numpy.asarray( [2014., 2015., 2016., 2017., 2018., 2019.] )
        y = numpy.asarray( [155., 145., 140., 150., 160., 154.] )

        x -= 2013

        mdl = PolynomialModel( 2 )

        gp0 = GaussPrior( center=150, scale=20 )
        gn0 = GaussPriorNew( center=150, scale=20 )
        gp1 = GaussPrior( center=0, scale=20 )
        gn1 = GaussPriorNew( center=0, scale=20 )

#        mdl0.setPrior( 0, GaussPrior( center=150, scale=20 ) )

        problem = ClassicProblem( model=mdl, xdata=x, ydata=y )

        NPP = 71
        nh = NPP // 2

        pp0 = numpy.linspace( 150 - nh, 150 + nh, NPP, dtype=float )
        pp1 = numpy.linspace( -nh, nh, NPP, dtype=float )
        pp2 = numpy.linspace( -nh, nh, NPP, dtype=float )

        ed = GaussErrorDistribution( )

        sg = 0.0
        sn = 0.0
        for p0 in pp0 :
            for p1 in pp1 :
                for p2 in pp2 :
                    logL = ed.logLikelihood( problem, [p0, p1, p2, 5.0] )
                    logG0 = gp0.logResult( p0 )
                    logN0 = gn0.logResult( p0 )
                    logG1 = gp1.logResult( p1 )
                    logN1 = gn1.logResult( p1 )
                    logG2 = gp1.logResult( p2 )
                    logN2 = gn1.logResult( p2 )
                    sg += math.exp( logL + logG0 + logG1 + logG2 )
                    sn += math.exp( logL + logN0 + logN1 + logN2 )

        print( "3  LogZold  ", fmt( math.log( sg) ), "  LogZnew  ", fmt( math.log( sn ) ) )

    def testm3( self ) :
        x = numpy.asarray( [2014., 2015., 2016., 2017., 2018., 2019.] )
        y = numpy.asarray( [155., 145., 140., 150., 160., 154.] )

        x -= 2013

        mdl = PolynomialModel( 3 )

        gp0 = GaussPrior( center=150, scale=20 )
        gn0 = GaussPriorNew( center=150, scale=20 )
        gp1 = GaussPrior( center=0, scale=20 )
        gn1 = GaussPriorNew( center=0, scale=20 )

#        mdl0.setPrior( 0, GaussPrior( center=150, scale=20 ) )

        problem = ClassicProblem( model=mdl, xdata=x, ydata=y )

        NPP = 71
        nh = NPP // 2

        pp0 = numpy.linspace( 150 - nh, 150 + nh, NPP, dtype=float )
        pp1 = numpy.linspace( -nh, nh, NPP, dtype=float )
        pp2 = numpy.linspace( -nh, nh, NPP, dtype=float )
        pp3 = numpy.linspace( -nh, nh, NPP, dtype=float )

        ed = GaussErrorDistribution( )

        sg = 0.0
        sn = 0.0
        for p0 in pp0 :
            logG0 = gp0.logResult( p0 )
            logN0 = gn0.logResult( p0 )
            for p1 in pp1 :
                logG1 = gp1.logResult( p1 )
                logN1 = gn1.logResult( p1 )
                for p2 in pp2 :
                    logG2 = gp1.logResult( p2 )
                    logN2 = gn1.logResult( p2 )
                    for p3 in pp3 :
                        logL = ed.logLikelihood( problem, [p0, p1, p2, p3, 5.0] )
                        logG3 = gp1.logResult( p3 )
                        logN3 = gn1.logResult( p3 )
                        sg += math.exp( logL + logG0 + logG1 + logG2 + logG3 )
                        sn += math.exp( logL + logN0 + logN1 + logN2 + logN3 )

        print( "4  LogZold  ", fmt( math.log( sg) ), "  LogZnew  ", fmt( math.log( sn ) ) )


    @classmethod
    def suite( cls ):
        return ConfiguredTestCase.suite( TestPrior2.__class__ )

if __name__ == '__main__':
    unittest.main( )


