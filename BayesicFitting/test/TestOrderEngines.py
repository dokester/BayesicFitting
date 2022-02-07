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


    def initProblem( self, np=10, random=False ):

        n2 = np * np
        if random :
            numpy.random.seed( 12345 )
            x0 = numpy.random.rand( n2 ) * np
            x1 = numpy.random.rand( n2 ) * np
        else :
            x0 = numpy.arange( n2, dtype=int ) % np
            x1 = numpy.arange( n2, dtype=int ) // np
        xdata = numpy.append( x0, x1 ).reshape( 2, n2 ).transpose()
        xdata = numpy.array( xdata, dtype=float )

        problem = SalesmanProblem( xdata )

#        numpy.set_printoptions( precision=3, suppress=True )
        return problem

    def test1( self ):
        print( "\n   SalesmanProblem Test MoveEngine\n" )
        self.stdenginetest( MoveEngine, np=4, plot=self.doplot, random=True )

    def test2( self ):
        print( "\n   SalesmanProblem Test ReverseEngine\n" )
        self.stdenginetest( ReverseEngine, np=5, plot=self.doplot )

    def test3( self ):
        print( "\n   SalesmanProblem Test ShuffleEngine\n" )
        self.stdenginetest( ShuffleEngine, np=5, plot=self.doplot )

    def test4( self ):
        print( "\n   SalesmanProblem Test SwitchEngine\n" )
        self.stdenginetest( SwitchEngine, np=5, plot=self.doplot )

    def test5( self ):
        print( "\n   SalesmanProblem Test LoopEngine\n" )
        self.stdenginetest( LoopEngine, np=5, plot=self.doplot, random=True )

    def test6( self ):
        print( "\n   SalesmanProblem Test NearEngine\n" )
        self.stdenginetest( NearEngine, np=5, plot=self.doplot, random=True )

    def teststart1( self ) :
        print( "\n   SalesmanProblem Test StartOrderEngine\n" )
        self.stdstarttest( StartOrderEngine, np=4, nwalker=10 )

    def XXXteststart2( self ) :
        print( "\n   SalesmanProblem Test StartNearEngine\n" )
        self.stdstarttest( StartNearEngine, np=4, nwalker=10 )


    def stdstarttest( self, mystarteng, np=4, nwalker=10 ) :

        problem = self.initProblem( np=np )

        errdis = DistanceCostFunction( )

        n2 = np * np
        pars = numpy.arange( n2, dtype=int )
        fi = numpy.arange( n2, dtype=int )
        sl = WalkerList( problem, nwalker, pars, fi )

        steng = mystarteng( sl, errdis, verbose=5 )
        for wlkr in steng.walkers :
            logL = errdis.logLikelihood( problem, wlkr.allpars )
            wid = wlkr.id
            print( "Walker :", wid, wlkr.allpars, fmt( logL ) )
            steng.execute( wid, -math.inf )

            nwlk = steng.walkers[wid]
            print( "          ", nwlk.allpars, fmt( nwlk.logL ) )


            psort = numpy.sort( nwlk.allpars )
            assertAE( psort, pars )


    def stdenginetest( self, myengine, nwalker=4, np=10, plot=False, random=False ) :
        problem = self.initProblem( np=np, random=random )

        errdis = DistanceCostFunction( )
#        print( problem.xdata )

        n2 = np * np
        pars = numpy.arange( n2, dtype=int )
        fi = numpy.arange( n2, dtype=int )
        sl = WalkerList( problem, nwalker, pars, fi )

        if not random :
            n1 = np - 1
            m = n1 * n1
            s = np * n1
            s += math.sqrt( m + 1 ) * ( np - 1 )
            s += math.sqrt( m + m )

            logL = numpy.sum( problem.result( pars ) )
            print( s, logL, abs( s - logL ) )
            self.assertTrue( abs( s - logL ) < 1.0e-10 )

        steng = StartOrderEngine( sl, errdis, verbose=5 )
        myeng = myengine( sl, errdis, verbose=5 )

        for wlkr in steng.walkers :
            print( "=========", wlkr )

            pars = wlkr.allpars
#            print( "Before ", wlkr.allpars )

            wid = wlkr.id
            myeng.execute( wid, -math.inf )

            neww = steng.walkers[wid]
#            print( "After  ", neww.allpars )
            newp = neww.allpars

            psort = numpy.sort( neww.allpars )
            assertAE( psort, pars )

            if plot :
                xy0 = problem.xdata[pars]
                plt.plot( xy0[:,0], xy0[:,1], 'k-' )
                plt.plot( [xy0[-1,0], xy0[0,0]], [xy0[-1,1], xy0[0,1]], 'b-' )
                xy1 = problem.xdata[newp]
                plt.plot( xy1[:,0], xy1[:,1], 'r-.' )
                plt.plot( [xy1[-1,0], xy1[0,0]], [xy1[-1,1], xy1[0,1]], 'g-.' )
                for kp in range( n2 ) :
                    plt.text( xy0[kp,0], xy0[kp,1], "%d"%kp,
                               {'color': 'black', 'ha': 'right'} )
                    plt.text( xy1[kp,0], xy1[kp,1], "%d"%kp,
                               {'color': 'red', 'ha': 'left'} )


                plt.show()

        myeng.verbose = 0
        wid = wlkr.id
        for k in range( 1000 ) :
            myeng.execute( wid, -math.inf )
            psort = numpy.sort( steng.walkers[wid].allpars )
            assertAE( psort, pars )

    def suite( cls ):
        return unittest.TestCase.suite( TestOrderEngines.__class__ )


if __name__ == '__main__':
    unittest.main( )


