# run with : python3 -m unittest TestWalker

import unittest
import numpy as numpy

from BayesicFitting import *

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
#  *  2002 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness.

    Author       Do Kester

    """

    # Define x independent variable
    x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0], dtype=float )

    # Define noise: random Gaussian noise sig=0.3
    noise = numpy.asarray( [ -0.000996, -0.046035,  0.013656,  0.418449,  0.0295155,  0.273705,
    -0.204794,  0.275843, -0.415945, -0.373516, -0.158084], dtype=float )
    wgt = numpy.asarray( [1,2,3,4,5,6,7,4,3,2,1], dtype=float )                 #  total 38
    par = numpy.asarray( [3,2,1,0.3], dtype=float )
    fi  = [0,1,2,3]
    len = 11

    #  **************************************************************
    def test1( self ) :
        print( "========= test1 ===========================" )

        mdl = PolynomialModel( 1 )
        problem = ClassicProblem( xdata= self.x, ydata=self.noise, model=mdl )
        problem.npars = 3       ## 1 nuisance parameter

        self.assertTrue( mdl.npars == 2 )
        self.assertTrue( problem.npars == 3 )

        w1 = Walker( 1, problem, self.par, self.fi, start=99 )
        w1.logL = 1.0
        w1.logPrior = 0.3

        self.assertTrue( w1.id == 1 )
        self.assertTrue( w1.parent == -1 )
        self.assertTrue( w1.start == 99 )
        self.assertTrue( len( w1.allpars ) == 4 )
        self.assertTrue( w1.problem.model.npars == 2 )
        self.assertTrue( w1.problem.npars == 3 )


        wc = w1.copy()
        wc.problem.npars = w1.problem.npars

        self.assertTrue( wc.id == 1 )
        self.assertTrue( wc.parent == -1 )
        self.assertTrue( wc.start == 99 )
        self.assertTrue( wc.logPrior == 0.3 )
        self.assertTrue( wc.logL == 1 )
        self.assertTrue( wc.problem.model.npars == 2 )
        self.assertTrue( wc.problem.npars == 3 )


        samp = wc.toSample( 0.1 )

        self.assertTrue( samp.id == w1.id )
        self.assertTrue( samp.parent == w1.parent )
        self.assertTrue( samp.start == w1.start )
        self.assertTrue( samp.logL == 1.3 )

        print( samp.parameters )
        print( samp.hyper )
        print( samp.nuisance )
        self.assertTrue( len( samp.parameters ) == 2 ) 
        self.assertTrue( len( samp.hyper ) == 1 ) 
        self.assertTrue( len( samp.nuisance ) == 1 ) 

        print( w1 )
        print( wc )
        self.assertTrue( wc.nap == 4 )

    #  **************************************************************
    def test2( self ) :
        print( "========= test2 ===========================" )

        mdl = PolynomialModel( 3 )
        problem = ClassicProblem( xdata= self.x, ydata=self.noise, model=mdl )

        errdis = GaussErrorDistribution( )

        self.par[-1] = -1
        wlkr = Walker( 1, problem, self.par, self.fi, start=99 )
        logL = errdis.logLikelihood( problem, self.par )
        wlkr.logL = logL
        wlkr.logPrior = 0.3


        ## Too many parameters in model
        self.assertRaises( ValueError, wlkr.check, errdis )

        mdl = PolynomialModel( 2 )
        problem = ClassicProblem( xdata= self.x, ydata=self.noise, model=mdl )
        errdis = GaussErrorDistribution( )

        wlkr = Walker( 1, problem, self.par, self.fi, start=99 )
        logL = errdis.logLikelihood( problem, self.par )
        wlkr.logL = logL
        wlkr.logPrior = 0.3


        ## negative hypar.
        self.assertRaises( ValueError, wlkr.check, errdis )

        self.par[-1] = 1
        wlkr = Walker( 1, problem, self.par, self.fi, start=99 )

        ## No Prior provided.
        self.assertRaises( IndexError, wlkr.check, errdis )

        mdl.setPrior( 0, UniformPrior( limits=[0,3] ) )

        ## inconsistent logL.
        self.assertRaises( ValueError, wlkr.check, errdis )

        wlkr.logL = errdis.logLikelihood( problem, self.par )

        wlkr.check( errdis )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( Test.__class__ )



if __name__ == '__main__':
    unittest.main()


