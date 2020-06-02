# run with : python3 -m unittest TestWeights

import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal as assertAAE

import matplotlib.pyplot as plt
from BayesicFitting import *


class TestWeights( unittest.TestCase  ) :


    def testWeights2( self ) :
        print( "====testWeights 2====================" )
        nn = 5
        x = np.arange( nn, dtype=float )
        y = x % 2
        y[2] = 0.5
        x4 = np.arange( 4*nn, dtype=float )
        y4 = x4 % 2
        y4[range(2,20,5)] = 0.5

        pm = PolynomialModel( 0 )
        bf = CurveFitter( x, pm )
        pars = bf.fit( y )
        pcov = bf.covariance
        var = bf.makeVariance()
        print( "======= 5 data points; no weights; no fixScale ===" )
        print( "pars  ", pars, "stdv  ", np.sqrt( np.diag( pcov ) ), bf.hessian, pcov )
        print( "pars  ", pm.parameters, "stdv  ", bf.stdevs, bf.hessian, bf.covariance, var )
        print( "chisq %f  scale %f %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.makeVariance(), bf.sumwgt ) )

        pm = PolynomialModel( 0 )
        bf = CurveFitter( x4, pm )
        pars = bf.fit( y4 )
        pcov = bf.covariance
        var = bf.makeVariance()
        print( "======= 20 data points; no weights; no fixScale ===" )
        print( "pars  ", pars, "stdv  ", np.sqrt( np.diag( pcov ) ), bf.hessian, pcov )
        print( "pars  ", pm.parameters, "stdv  ", bf.stdevs, bf.hessian, bf.covariance, var )
        print( "chisq %f  scale %f %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.makeVariance(), bf.sumwgt ) )


        print( "======= 5 data points; weights = 4; no fixScale ===" )
        pm = PolynomialModel( 0 )
        bf = CurveFitter( x, pm )
        w = np.zeros( nn, dtype=float ) + 4
        pars = bf.fit( y, w )
        pcov = bf.covariance
        var = bf.makeVariance()
        print( "pars  ", pars, "stdv  ", np.sqrt( np.diag( pcov ) ), bf.hessian, pcov )
        print( "pars  ", pm.parameters, "stdv  ", bf.stdevs, bf.hessian, bf.covariance, var )
        print( "chisq %f  scale %f %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.makeVariance(), bf.sumwgt ) )

        pm = PolynomialModel( 0 )
        bf = CurveFitter( x, pm )
        pars = bf.fit( y )
        pcov = bf.covariance
        var = bf.makeVariance()
        print( "======= 5 data points; no weights; fixScale ===" )
        print( "pars  ", pars, "stdv  ", np.sqrt( np.diag( pcov ) ), bf.hessian, pcov )
        print( "pars  ", pm.parameters, "stdv  ", bf.stdevs, bf.hessian, bf.covariance, var )
        print( "chisq %f  scale %f %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.makeVariance(), bf.sumwgt ) )
        print( "noise ", bf.scale, " +- ", bf.stdevScale, "  keep ", bf.keep )


    def testWeights1( self ) :
        print( "====testWeights 1====================" )
        nn = 5
        x = np.arange( nn, dtype=float )
        y = x % 2
        y[2] = 0.5
        x4 = np.arange( 4*nn, dtype=float )
        y4 = x4 % 2
        y4[range(2,20,5)] = 0.5

        pm = PolynomialModel( 0 )
        bf = Fitter( x, pm )
        pars = bf.fit( y )
        var = bf.makeVariance()
        print( "======= 5 data points; no weights; no noiseScale ===" )
        print( "pars  ", pm.parameters, "stdv  ", bf.stdevs, bf.hessian, bf.covariance, var )
        print( "chisq %f  scale %f %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.makeVariance(), bf.sumwgt ) )

        pm = PolynomialModel( 0 )
        bf = Fitter( x4, pm )
        pars = bf.fit( y4 )
        print( "======= 20 data points; no weights; no noiseScale ===" )
        print( "pars  ", pm.parameters, "stdv  ", bf.stdevs, bf.hessian, bf.covariance )
        print( "chisq %f  scale %f %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.makeVariance(), bf.sumwgt ) )


        print( "======= 5 data points; weights = 4; no noiseScale ===" )
        pm = PolynomialModel( 0 )
        bf = Fitter( x, pm )
        w = np.zeros( nn, dtype=float ) + 4
        pars = bf.fit( y, w )
        print( "pars  ", pm.parameters, "stdv  ", bf.stdevs, bf.hessian, bf.covariance )
        print( "chisq %f  scale %f %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.makeVariance(), bf.sumwgt ) )

        pm = PolynomialModel( 0 )
        bf = Fitter( x, pm )
        pars = bf.fit( y )
        print( "======= 5 data points; no weights; noiseScale ===" )
        print( "pars  ", pm.parameters, "stdv  ", bf.stdevs, bf.hessian, bf.covariance )
        print( "chisq %f  scale %f %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.makeVariance(), bf.sumwgt ) )
        print( "noise ", bf.scale, " +- ", bf.stdevScale, "  keep ", bf.keep )


if __name__ == '__main__':
    unittest.main( )

