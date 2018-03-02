
import unittest
import numpy as np
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from BayesicFitting import ExponentialPrior
from BayesicFitting import LaplacePrior
from BayesicFitting import JeffreysPrior
from BayesicFitting import UniformPrior
from BayesicFitting import GaussPrior
from BayesicFitting import CauchyPrior

from BayesicFitting import Prior
from BayesicFitting import Formatter
from Formatter import formatter as fmt

class PlotTestPrior( unittest.TestCase  ) :

    def testPlotUniform( self ) :
        # example data
        u = np.random.rand( 10000 )
        pr = UniformPrior( limits=[-10,10] )
        d = [pr.unit2Domain( v ) for v in u]
        x = np.asarray( [-12,-10,-10,10,10,12], dtype=float )
        a = 1.0 / pr._range
        y = np.asarray( [0,0,a,a,0,0], dtype=float )
        self.histo( d, pr, fun=(x,y) )

    def testPlotJeffreys( self ) :
        # example data
        u = np.random.rand( 10000 )
        pr = JeffreysPrior( limits=[0.2,9] )
        d = [pr.unit2Domain( v ) for v in u]
        x = np.arange( 51 ) / 5
        y = np.zeros( 51, dtype=float )
        y[1:46] = 1.0 / ( ( math.log( pr.highLimit ) - math.log( pr.lowLimit ) ) * x[1:46] )
        self.histo( d, pr, fun=(x,y) )

    def testPlotExponential( self ) :
        # example data
        u = np.random.rand( 10000 )
        pr = ExponentialPrior( scale=3 )
        d = [pr.unit2Domain( v ) for v in u]
        x = np.arange( 51 ) * pr.scale / 5
        y = np.exp( - x / pr.scale ) / pr.scale
        self.histo( d, pr, fun=(x,y) )

    def testPlotLaplace( self ) :
        # example data
        u = np.random.rand( 10000 )
        pr = LaplacePrior( scale=4 )
        d = [pr.unit2Domain( v ) for v in u]
        x = ( np.arange( 101 ) - 50 ) * pr.scale / 5
        y = np.exp( - np.abs( x ) / pr.scale ) / ( 2 * pr.scale )
        self.histo( d, pr, fun=(x,y) )

    def testPlotGauss( self ) :
        # example data
        u = np.random.rand( 10000 )
        pr = GaussPrior( scale=4 )
        d = [pr.unit2Domain( v ) for v in u]
        x = ( np.arange( 101 ) - 50 ) * pr.scale / 5
        y = [pr.result( v )/4 for v in x]
        self.histo( d, pr, fun=(x,y) )

    """
    def testPlotGaussLut( self ) :
        # example data
        u = np.random.rand( 10000 )
        pr = GaussLutPrior( scale=4, nl=128 )
#        print( fmt( pr.u2d, max=None ) )
#        print( fmt( pr.d2u, max=None ) )
        d = [pr.unit2Domain( v ) for v in u]
        x = ( np.arange( 101 ) - 50 ) * pr.scale / 5
        y = [pr.result( v )/4 for v in x]
        self.histo( d, pr, fun=(x,y) )
    """
    def testPlotCauchy( self ) :
        # example data
        u = np.random.rand( 10000 )
        pr = CauchyPrior( scale=4 )
        d = np.asarray( [pr.unit2Domain( v ) for v in u] )
        # There are too many far outliers in a Cauchy
        q = np.where( d < -50 )
        d[q] = -50
        q = np.where( d > 50 )
        d[q] = 50
        x = ( np.arange( 101 ) - 50 ) * pr.scale / 5
        y = [pr.result( v ) for v in x]
        self.histo( d, pr, fun=(x,y) )


    def histo( self, x, pr, fun=None ) :
        print( pr )
        print( fmt( x ) )
        print( fmt( fun[0] ) )
        print( fmt( fun[0] ) )

        num_bins = 50
        # the histogram of the data
        n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
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

