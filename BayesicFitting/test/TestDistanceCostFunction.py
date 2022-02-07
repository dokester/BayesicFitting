# run with : python3 -m unittest TestDistanceCostFunction

import unittest
import os
import numpy as numpy
from astropy import units
from numpy.testing import assert_array_equal as assertAE
from numpy.testing import assert_array_almost_equal as assertAAE
import math
import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from BayesicFitting import fma


__author__ = "Do Kester"
__year__ = 2021
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
        print( "\n   DistanceCostFunction\n" )

        problem = self.initProblem( random=True )

        pars = numpy.random.permutation( problem.npars )

        print( fmt( problem.xdata, tail=3 ) )
        print( fmt( pars, tail=3 ) )

        swt = problem.sumweight
        dist = problem.result( pars )
        sd1  = numpy.sum( dist )

        print( fmt( dist, tail=3 ) )
        print( fmt( swt ), fmt( sd1 ) )
        self.assertTrue( swt == 100 )
#        assertAAE( sd1, 502.303, 3 )

        dcf = DistanceCostFunction()
        lh = dcf.logLikelihood( problem, pars )
        la = dcf.logLikelihood_alt( problem, pars )
        print( "logL  ", fmt( lh ), fmt(la ) )

        problem.xdata *= 100
        swt = problem.sumweight
        dist = problem.result( pars )
        sd2  = numpy.sum( dist )
        dcf = DistanceCostFunction()

        print( fmt( swt ), fmt( sd2 ) )
        lh = dcf.logLikelihood( problem, pars )
        la = dcf.logLikelihood_alt( problem, pars )
        print( "logL  ", fmt( lh ), fmt(la ) )

        self.assertTrue( swt == 100 )
        assertAAE( sd2, ( 100 * sd1 ) )

        problem.xdata /= 100
        problem.weights = numpy.array( [2.0] * 100 )

        swt = problem.sumweight
        dist = problem.result( pars )
        sd3  = numpy.sum( dist )
        dcc = dcf.copy()

        print( fmt( swt ), fmt( sd3 ) )
        lh = dcc.logLikelihood( problem, pars )
        la = dcc.logLikelihood_alt( problem, pars )
        print( "logL  ", fmt( lh ), fmt(la ) )

        self.assertTrue( dcc.acceptWeight() )
        self.assertTrue( swt == 200 )
        assertAAE( sd3, ( 2 * sd1 ) )

        problem.weights = numpy.array( [1.0,2.0] * 50 )

        swt = problem.sumweight
        dist = problem.result( pars )
        sd3  = numpy.sum( dist )
        dcc = dcf.copy()

        print( fmt( swt ), fmt( sd3 ) )
        lh = dcc.logLikelihood( problem, pars )
        la = dcc.logLikelihood_alt( problem, pars )
        print( "logL  ", fmt( lh ), fmt(la ) )

        self.assertTrue( dcc.acceptWeight() )
        self.assertTrue( swt == 150 )
#        assertAAE( sd3, ( 1.5 * sd1 ) )


    def suite( cls ):
        return unittest.TestCase.suite( TestDistanceCostFunction.__class__ )


if __name__ == '__main__':
    unittest.main( )


