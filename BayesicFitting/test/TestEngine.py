# run with : python3 -m unittest TestEngine

import unittest
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt
from numpy.testing import assert_array_almost_equal as assertAAE

from BayesicFitting import *

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
#  *  2006 Do Kester

class TestEngine( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """
    def __init__( self, name ):
        super( TestEngine, self ).__init__( name )


    def initEngine( self ):
        m = GaussModel()

        ep1 = ExponentialPrior( scale=2.0 )
        up = UniformPrior( limits=[-10,10] )
        ep2 = ExponentialPrior()
        m.priors = [ep1, up, ep2]

        xdata = numpy.linspace( 0.0, 10.0, 101 )
        data = numpy.zeros( 101, dtype=float )
        data[30:71] = 1.0
        data[40:61] = 2.0
        data[45:56] = 3.0
        data[48:53] = 4.0
        data[50] = 5.0

        numpy.set_printoptions( precision=3, suppress=True )
        return ( m, xdata, data )

    def testEngine( self ):
        print( "\n   Engine Test 1\n" )
        m, xdata, data = self.initEngine()

        errdis = GaussErrorDistribution( )
        errdis.setLimits( [0.1, 10.0] )

        print( errdis.hyperpar[0].prior )
        print( errdis.hyperpar[0].prior.lowLimit )
        print( errdis.hyperpar[0].prior.highLimit )
        print( errdis.hyperpar[0].prior._umin )
        print( errdis.hyperpar[0].prior._urng )

        fi = [0,1,2,-1]
        problem = ClassicProblem( m, xdata, data )

        Tools.printclass( problem )

        allpars = numpy.append( m.parameters, 1.0 )
        wl = WalkerList( problem, 100, allpars, fi )

        engine = Engine( wl, errdis )

        self.enginetest( engine )

        print( "    make copy of engine" )
        copeng = engine.copy()
        self.enginetest( copeng )


    def enginetest( self, engine ) :
        walkers = engine.walkers
        fi = [0,1,2,-1]
        for kw in range( len( walkers ) ) :
            problem = walkers[kw].problem
            p = engine.unit2Domain( problem, engine.rng.rand( 4 ) )
            logL = engine.errdis.logLikelihood( problem, p )
            engine.setWalker( kw, problem, p, logL, fitIndex=fi )
            engine.reportSuccess()
            engine.reportCall()

        engine.reportReject()
        engine.reportFailed()

        self.assertTrue( engine.maxtrials == 5 )
        self.assertTrue( isinstance( engine.rng, numpy.random.RandomState ) )

        print( engine.walkers[0] )
        print( engine.walkers[0].allpars )

        engine.calculateUnitRange()

        print( "UnitR ", engine.unitRange )

        print( "DomR  ", engine.unit2Domain( problem, engine.unitRange ) )
        engine.printReport()



    def suite( cls ):
        return unittest.TestCase.suite( TestEngine.__class__ )


if __name__ == '__main__':
    unittest.main( )


