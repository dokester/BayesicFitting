# run with : python3 -m unittest TestStartEngine

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

from TestEngine import TestEngine
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

class TestStartEngine( TestEngine ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def testStartEngine( self ):
        print( "\n   Start Engine Test 1\n" )
        m, xdata, data = self.initEngine()

        print( m )

        problem = ClassicProblem( m, xdata=xdata, ydata=data )

        errdis = GaussErrorDistribution( )
        errdis.setLimits( [0.1, 10.0] )
        ap = [1.0, 0.0, 0.3, 0.2]
        fi = [0,1,2,-1]

        wl = WalkerList( problem, 100, ap, fi )

        engine = StartEngine( wl, errdis )
        self.startenginetest( engine )

        print( "    make copy of engine" )
        copeng = engine.copy()
        self.startenginetest( copeng )

        if self.doplot :
            parevo = wl.getParameterEvolution()
            sclevo = wl.getScaleEvolution()
            print( parevo.shape, sclevo.shape )
            plt.subplot( 2, 2, 1 )
            plt.plot( parevo[:,0], parevo[:,1], 'k.' )
            plt.subplot( 2, 2, 2 )
            plt.plot( parevo[:,0], parevo[:,2], 'k.' )
            plt.subplot( 2, 2, 3 )
            plt.plot( parevo[:,1], parevo[:,2], 'k.' )
            plt.subplot( 2, 2, 4 )
            plt.plot( parevo[:,0], sclevo, 'k.' )
            plt.show()

    def startenginetest( self, engine ) :
        print( engine )
        minv = [ math.inf] * len( engine.walkers[0].allpars )
        maxv = [-math.inf] * len( engine.walkers[0].allpars )
        for kw in range( len( engine.walkers ) ) :
            engine.execute( kw, -math.inf )
            samp = engine.walkers[kw]
            minv = numpy.fmin( minv, samp.allpars )
            maxv = numpy.fmax( maxv, samp.allpars )
            if samp.id <= 1 or samp.id >= 98 :
                print( samp )
                print( "  ", samp.allpars, "  ", samp.fitIndex )
        print( "minv  ", minv )
        print( "maxv  ", maxv )


    def suite( cls ):
        return unittest.TestCase.suite( TestStartEngine.__class__ )


if __name__ == '__main__':
    unittest.main( )


