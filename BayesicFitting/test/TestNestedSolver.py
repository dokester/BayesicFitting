# run with : python3 -m unittest TestSalesmanProblem

import unittest
import os
import numpy as numpy
from astropy import units
from numpy.testing import assert_array_equal as assertAE
import math
import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from BayesicFitting import fma


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
#  *  2006 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for solving the SalesmanProblem with NestedSampler.

    Author       Do Kester

    """
    def __init__( self, name ):
        super( ).__init__( name )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def makeData( self, np ) :
        n2 = np * np
        x0 = numpy.arange( n2, dtype=int ) % np
        x1 = numpy.arange( n2, dtype=int ) // np
        xdata = numpy.append( x0, x1 ).reshape( 2, n2 ).transpose()
        return numpy.array( xdata, dtype=float )
        
    def testSolve1( self, plot=False ):
        print( "\n   NestedSolver Test1 \n" )
        np = 6

        xdata = self.makeData( np )

        problem = SalesmanProblem( xdata )
        print( "mindis  ", problem.scale )

        print( problem )


        ns = NestedSolver( problem, verbose=2, seed=130105 )
#        ns.minimumIterations = 20000
#        ns.end = 4
#        ns.ensemble = 10

        sl = ns.solve()


        if self.doplot :
            pars = sl[-1].allpars

            x = problem.xdata[pars,0]
            y = problem.xdata[pars,1]
            print( x )
            print( y )

            plt.plot( x, y, 'k-' )
            plt.show()


    def testSolve2( self, plot=False ):
        print( "\n   NestedSolver Test2 \n" )
        np = 6

        n2 = np * np
        numpy.random.seed( 123456 )
        x1 = ( numpy.random.rand( n2 ) - 0.5 ) * 180
        x0 = numpy.random.rand( n2 ) * 360 - 180

#        x0 = numpy.arange( n2, dtype=int ) % np
#        x1 = numpy.arange( n2, dtype=int ) // np
#        x0 = ( x0 - hp ) * 180 / ( hp + 1 )
#        x1 = ( x1 - hp ) * 90 / ( hp + 1 )

        print( x0 )
        print( x1 )

        xdata = numpy.append( x0, x1 ).reshape( 2, n2 ).transpose()
        xdata = numpy.array( xdata, dtype=float )

        problem = SalesmanProblem( xdata, distance="spheric" )
        print( "mindis  ", problem.scale )

        engs = ["move", "reverse", "switch"]

        ns = NestedSolver( problem, engines=engs, verbose=2, seed=80409 )

        sample = ns.solve()

#        print( fmt( problem.xdata, max=None ) )
        pars = sample.allpars
#        print( fmt( problem.xdata[pars], max=None ) )


        if self.doplot :

            d2r = math.pi / 180
            y = problem.xdata[pars,1]
            t = problem.xdata[pars,0]
            x = t * numpy.cos ( y * d2r )

#            print( x )
#            print( y )

            yy = numpy.linspace( -90, 90, 181 )
            cy = numpy.cos( yy * d2r )
            for k in range( -180, 181, 30 ) :
                plt.plot( k * cy, yy, 'g-' )

            for k in range( -90, 90, 30 ) :
                xx = 180 * math.cos( k * d2r )
                plt.plot( [-xx, xx], [k, k], 'g-' )

            rt = numpy.roll( t, -1 )
            rx = numpy.roll( x, -1 )
            ry = numpy.roll( y, -1 )

            for k in range( n2 ) :
                if x[k] < rx[k] :
                    x0,x1,t0,t1,y0,y1 = (x[k],rx[k],t[k],rt[k],y[k],ry[k]) 
                else :
                    x0,x1,t0,t1,y0,y1 = (rx[k],x[k],rt[k],t[k],ry[k],y[k])

                tm = 180
                if ( t1 - t0 ) < tm :
                    plt.plot( [x0,x1], [y0,y1], 'k-' )
                else :
                    ym = y0 + ( y1 - y0 ) * ( tm - t1 ) / ( 360 - ( t1 - t0 ) )
                    xm = tm * math.cos( d2r * ym )
                    print( fmt( [x0, xm, x1] ), fmt( [y0,ym,y1] ) ) 
                    plt.plot( [x1,xm], [y1,ym], 'r-' )
                    plt.plot( [x0,-xm], [y0,ym], 'b-' )

#            plt.plot( x, y, 'k-' )
            plt.show()



    def suite( cls ):
        return unittest.TestCase.suite( TestNestedSolver.__class__ )


if __name__ == '__main__':
    unittest.main( )


