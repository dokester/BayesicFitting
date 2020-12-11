
import unittest
import os
import numpy as np
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from BayesicFitting import *

from BayesicFitting import formatter as fmt

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
#  *  2020 Do Kester


class TestPrior2( unittest.TestCase  ) :

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )
        np.random.seed( 123456 )

    def testPlotUniform( self ) :
        # example data
        NP = 10000
        u = np.random.rand( NP )
        pr = UniformPrior( limits=[-10,10] )
        d = [pr.unit2Domain( v ) for v in u]

        fac = NP / 4
        x = np.asarray( [-12,-10,-10,10,10,12], dtype=float )
        a = fac / pr._range
        y = np.asarray( [0,0,a,a,0,0], dtype=float )
        self.histo( d, pr, fun=(x,y) )

    def testPlotJeffreys( self ) :
        # example data
        NP = 10000
        u = np.random.rand( NP )
        pr = JeffreysPrior( limits=[1.0,9.0] )
        d = [pr.unit2Domain( v ) for v in u]

        fac = NP / 7
        x = np.arange( 51 ) / 5
        y = np.zeros( 51, dtype=float )
        y[5:46] = fac / ( ( math.log( pr.highLimit ) - math.log( pr.lowLimit ) ) * x[5:46] )
        self.histo( d, pr, fun=(x,y) )

    def testPlotExponential( self ) :
        # example data
        NP = 10000
        u = np.random.rand( NP )
        pr = ExponentialPrior( scale=3 )
        d = [pr.unit2Domain( v ) for v in u]

        fac = NP / 3
        x = np.arange( 51 ) * pr.scale / 5
        y = fac * np.exp( - x / pr.scale ) / pr.scale
        self.histo( d, pr, fun=(x,y) )

    def testPlotLaplace( self ) :
        # example data
        NP = 10000
        u = np.random.rand( NP )
        pr = LaplacePrior( scale=4 )
        d = [pr.unit2Domain( v ) for v in u]

        Tools.printclass( pr )

        fac = math.sqrt( 2.0 ) * NP
        fac = NP
        x = ( np.arange( 101 ) - 50 ) * pr.scale / 5
        y = fac * np.exp( - np.abs( x ) / pr.scale ) / ( 2 * pr.scale )
        self.histo( d, pr, fun=(x,y) )

    def testPlotLaplace2( self ) :
        # example data
        NP = 10000
        u = np.random.rand( NP )
        pr = LaplacePrior( scale=4, limits=[-10,None] )
        d = [pr.unit2Domain( v ) for v in u]

        Tools.printclass( pr )

        fac = 0.7 * NP
        x = ( np.arange( 101 ) - 50 ) * pr.scale / 5
        y = fac * np.exp( - np.abs( x ) / pr.scale ) / ( 2 * pr.scale )
        self.histo( d, pr, fun=(x,y) )

    def testPlotGauss( self ) :
        # example data
        NP = 10000
        u = np.random.rand( NP )
        pr = GaussPrior( scale=4 )
        d = [pr.unit2Domain( v ) for v in u]
        x = ( np.arange( 101 ) - 50 ) * pr.scale / 5
        fac = NP / 4
        y = [fac * pr.result( v )/4 for v in x]
        self.histo( d, pr, fun=(x,y) )

    def testPlotCauchy( self ) :
        # example data
        NP = 10000
        u = np.random.rand( NP )
        pr = CauchyPrior( scale=4 )
        d = np.asarray( [pr.unit2Domain( v ) for v in u] )
        # There are too many far outliers in a Cauchy
        q = np.where( d < -50 )
        d[q] = -50
        q = np.where( d > 50 )
        d[q] = 50
        x = ( np.arange( 101 ) - 50 ) * pr.scale / 5
        fac = 1.2 * NP
        y = [fac * pr.result( v ) for v in x]
        self.histo( d, pr, fun=(x,y) )


    def histo( self, x, pr, fun=None ) :
        print( pr )
        print( fmt( x ) )
        print( fmt( fun[0] ) )
        print( fmt( fun[1] ) )

        if self.doplot :
            num_bins = 80
            # the histogram of the data
            n, bins, patches = plt.hist( x, num_bins, facecolor='green', alpha=0.5 )

            # add a 'best fit' line
            if fun is not None :
                plt.plot( fun[0], fun[1], 'r--')
            plt.xlabel('Error')
            plt.ylabel('Probability')
            plt.title('Histogram of ' + str( pr ) )

            # Tweak spacing to prevent clipping of ylabel
            plt.subplots_adjust(left=0.15)
            plt.show()

if __name__ == '__main__':
    unittest.main( )

