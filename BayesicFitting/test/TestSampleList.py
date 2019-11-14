# run with : python3 -m unittest TestSampleList

import unittest
import numpy as numpy
import sys
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import math

from BayesicFitting import *
from BayesicFitting import formatter as fmt

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
#  *  2002 Do Kester

class TestSampleList( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """

    # Define x independent variable
    x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0], dtype=float )

    # Define noise: random Gaussian noise sig=0.3
    noise = numpy.asarray( [ -0.000996, -0.046035,  0.013656,  0.418449,  0.0295155,  0.273705,
    -0.204794,  0.275843, -0.415945, -0.373516, -0.158084], dtype=float )
    wgt = numpy.asarray( [1,2,3,4,5,6,7,4,3,2,1], dtype=float )                 #  total 38
    par = numpy.asarray( [3,2,1,0.3], dtype=float )
    len = 11


    #  **************************************************************
    def testSampleList( self ):
        print( "=========  SampleListTest  =======================" )
        gm = GaussModel( )
        gm += PolynomialModel( 0 )

        problem = ClassicProblem( gm, xdata=self.x, ydata=self.noise )
#        errdis = GaussErrorDistribution( )

        lnZ = 1.234
        sl0 = SampleList( gm, self.len )
        k = 0
        for s in sl0 :
            self.assertTrue( s.id == k )
            self.assertTrue( s.parent == -1 )
            self.assertTrue( isinstance( s.model, GaussModel ) )
            self.assertTrue( s.logW == 0 )
            self.assertTrue( s.logL == 0 )
            self.assertTrue( s.parameters[0] == 1 )
            self.assertTrue( s.parameters[1] == 0 )
            self.assertTrue( s.parameters[2] == 1 )
            self.assertTrue( s.parameters[3] == 0 )

            self.assertTrue( len( s.fitIndex ) == 4 )
            k += 1

        ap = numpy.append( gm.parameters, [0.5] )
        fi = numpy.asarray( [0,1,2,3,-1] )

        sl = SampleList( gm, self.len, parameters=ap, fitIndex=fi )
        k = 0
        for s in sl:
            s.id = k + 1
            s.parent = ( k + 2 ) % self.len + 1
            sup = 0.3 + 0.01 * self.noise[k]
            s.hyper = sup
            pars = self.par + 0.01 * self.noise[k]
            s.parameters = pars
            s.logL = -1213.0 + self.x[k]
            s.logW = math.log( self.wgt[k] / 38.0 ) + lnZ
            print( s )
            print( "    allpars ", fmt( s.allpars ) )
            print( "    par sup ", fmt( s.parameters ), fmt( s.hypars ) )
            print( "    fitindx ", fmt( s.fitIndex ) )
            k += 1
        sl.logZ = lnZ
        sl.info = 30
        self.assertTrue( sl.evidence == sl.logZ / math.log( 10) )
        self.assertTrue( sl.info == 30 )

        sumw = 0
        for s in sl :
            sumw += s.weight

        print( "wgt evo ", sl.getWeightEvolution( ) )
        print( "sum wgt ", sumw )
        self.assertFalse( abs(sumw - 1.0 ) < 1e-8 )

        sl.normalize()
        sumw = 0
        for s in sl :
            sumw += s.weight
        print( sl.getWeightEvolution( ) )
        print( sumw )
        self.assertTrue( abs(sumw - 1.0 ) < 1e-8 )

        for s in sl0 :
            s.logW = -sys.float_info.max

        sl0.sample( 4, sl.sample( 4 ) )
        sl0[5] = sl[5]
        sl0.logZ = sl.logZ

        print( sl0.sample( 4 ) )
        print( sl0[4].parameters )
        print( sl0[4].hypars )

        print( sl.sample( 4 ) )
        print( sl[4].parameters )
        print( sl[4].hypars )

        print( sl0.sample( 5 ) )
        print( sl.sample( 5 ) )

        self.assertTrue( sl0[4].id == sl[4].id )
        self.assertTrue( sl0[4].parent == sl[4].parent )
        self.assertTrue( sl0[4].hypars == sl[4].hypars )
        self.assertTrue( sl0[4].logW == sl[4].logW )
        self.assertTrue( sl0.sample( 4 ).logL == sl[4].logL )

        print( "sl0 Id   ", sl0.getGeneration( ) )
        print( "sl0 par  ", sl0.getParentEvolution( ) )
        print( "sl  Id   ", sl.getGeneration( ) )
        print( "sl  par  ", sl.getParentEvolution( ) )

        sl0.add( sl[10] )
#        print( "sl0 Id   ", sl0.getGeneration( ) )
        self.assertTrue( len( sl0 ) == 12 )
        sl0.copy( 11, 0 )
#        print( "sl0 Id   ", sl0.getGeneration( ) )
        self.assertTrue( sl0[0].id == 0 )
        self.assertTrue( sl0[11].id == 11 )
        self.assertTrue( sl0[0].logW == sl0[11].logW )
        self.assertTrue( sl0.sample( 0 ).logL == sl0.sample( 11 ).logL )

        for s,t in zip( sl0, sl ) :
            s.logL = t.logL
            s.logW = t.logW

        print( "SL   ", len( sl0 ) )
#        Tools.printclass( sl0[0] )
#        Tools.printclass( sl0[7] )
        for s in sl0 :
            print( s.id, s.logW, s.logL )

        k = 1
        while k < 3:
            sl0.weed( maxsize=8 )
            print( "SL0  ", k, len( sl0 ) )
            for s in sl0 :
                print( s.id, s.logW, s.logL )
#            Tools.printclass( sl0[0] )
#            Tools.printclass( sl0[7] )
            self.assertTrue( len( sl0 ) == 8 )
#            self.assertTrue( sl0[0].logL == sl0[5].logL )
            k += 1

        print( "SL   ", k, len( sl ) )
        for s in sl :
            print( s.id, s.logW, s.logL )

        print( "par    ", sl.parameters )
        print( "stdev  ", sl.stdevs )
        print( "hypars ", sl.hypars )
        print( "stdscl ", sl.stdevHypars )

        print( sl.medianIndex, sl.modusIndex, sl.maxLikelihoodIndex )

        sss = numpy.zeros( gm.npchain, dtype=float ) + 0.003

        assertAAE( sl.parameters, self.par, 2 )
        assertAAE( sl.standardDeviations, sss, 1 )
        assertAAE( sl.scale, 0.3, 2 )
        assertAAE( sl.stdevScale, 0.003, 1 )
        self.assertTrue( sl.medianIndex == 5 )
        self.assertTrue( sl.modusIndex == 6 )
        self.assertTrue( sl.maxLikelihoodIndex == -1 )
        assertAAE( sl.maxLikelihoodParameters, sl[10].parameters )
        self.assertTrue( sl.maxLikelihoodScale == sl[10].hypars[0] )
        assertAAE( sl.medianParameters, sl[5].parameters )
        self.assertTrue( sl.medianScale == sl[5].hypars[0] )
        assertAAE( sl.modusParameters, sl[6].parameters )
        self.assertTrue( sl.modusScale == sl[6].hypars[0] )

        param = sl.getParameterEvolution( )
        print( param.shape )
        self.assertTrue( param.shape[0] == 11 )
        self.assertTrue( param.shape[1] == 4 )
        par0 = sl.getParameterEvolution( 0 )
        par1 = sl.getParameterEvolution( 1 )
        par2 = sl.getParameterEvolution( 2 )
        par3 = sl.getParameterEvolution( 3 )
        nrp = sl.getNumberOfParametersEvolution( )

        for i in range( self.len ):
            assertAAE( param[i], self.par + 0.01 * self.noise[i] )
            assertAAE( param[i, 0], par0[i] )
            assertAAE( param[i, 1], par1[i] )
            assertAAE( param[i, 2], par2[i] )
            assertAAE( param[i, 3], par3[i] )
            self.assertTrue( nrp[i] == 4 )

        xx = numpy.arange( 10, dtype=float ) * 0.2
        yf1 = sl.average( xx )
        yf2 = gm.result( xx, sl.getParameters( ) )
        assertAAE( yf1, yf2, 5 )
        err = sl.monteCarloError( xx )
        assertAAE( err, numpy.zeros( 10, dtype=float ), 2 )
        zz = numpy.arange( 20, dtype=float ) * 0.2
        assertAAE( sl.monteCarloError( zz ), numpy.zeros( 20, dtype=float ), 2 )

    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestSampleList.__class__ )



if __name__ == '__main__':
    unittest.main()


