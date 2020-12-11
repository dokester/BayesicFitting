# run with : python3 -m unittest TestBaseFitter

import unittest
import math
import numpy as np
from numpy.testing import assert_array_almost_equal as assertAAE

import matplotlib.pyplot as plt

from BayesicFitting import *

class TestBaseFitter( unittest.TestCase  ) :

    def testExceptions( self ) :
        print( "====testExceptions======================" )
        x1 = np.arange( 10, dtype=float )
        x2 = np.ndarray( [10,2] )
        pm = PolynomialModel( 1 )
        gm = GaussModel()
        pm += gm

        self.assertRaises( ValueError, BaseFitter, x1, gm )
        self.assertRaises( ValueError, BaseFitter, x2, pm )

        bf = BaseFitter( x1, pm )
        y = np.arange( 10, dtype=float )
        self.assertRaises( NotImplementedError, bf.fit, y )

        self.assertTrue( bf.sumwgt == bf.nxdata )

#        self.assertRaises( AttributeError, bf.__getattr__, 'sumwgt' )
        self.assertRaises( AttributeError, bf.__getattr__, 'chisq' )
        self.assertRaises( AttributeError, bf.__getattr__, 'logOccam' )
        self.assertRaises( AttributeError, bf.__getattr__, 'logLikelihood' )
        self.assertRaises( AttributeError, bf.__getattr__, 'xyz' )
        bf.chisq = -1.0
        print( 'chisq', bf.chisq )

        y[2] = -np.inf
        w = np.ones( 10, dtype=float )
        self.assertRaises( ValueError, bf.checkNan, y, weights=w )
        w[8] = np.nan
        y[2] = 0
        self.assertRaises( ValueError, bf.checkNan, y, weights=w )

        x1[3] = np.nan
        self.assertRaises( ValueError, BaseFitter, x1, pm )

    def testInit( self ) :
        print( "====testInit======================" )
        x1 = np.arange( 10, dtype=float )
        pm = PolynomialModel( 1 )
        bf = BaseFitter( x1, pm )
        print( bf )
        print( bf.model )
        print( bf.xdata )
        print( bf.nxdata, bf.ndim )

    def testVector( self ) :
        print( "====testVector======================" )
        np.random.seed( 12345 )
        x = np.arange( 10, dtype=float )
        y = np.random.rand( 10 )
        w = np.ones( 10, dtype=float )
        pm = PolynomialModel( 1 )
        bf = BaseFitter( x, pm )
        v1 = bf.getVector( y )
        print( v1 )
        v2 = bf.getVector( y, index=[0] )
        print( v2 )
        v3 = bf.getVector( y, index=[1] )
        print( v3 )

        assertAAE( v1, np.append( v2, v3 ) )

    def testHessian( self ) :
        print( "====testHessian======================" )
        x = np.arange( 10, dtype=float )
        pm = PolynomialModel( 1 )
        bf = BaseFitter( x, pm )
        y = np.ones( 10, dtype=float )
        w = np.ones( 10, dtype=float )
        p = np.asarray( [1.0,1.0] )

        h0 = bf.hessian
        print( h0 )
        h1 = bf.getHessian( )
        print( h1 )
        h2 = bf.getHessian( params=p )
        print( h2 )
        h3 = bf.getHessian( weights=w, params=p )
        print( h3 )
        assertAAE( h0, h1 )
        assertAAE( h1, h2 )
        assertAAE( h1, h3 )
        index = 0
        h4 = bf.getHessian( weights=w, params=p, index=index )
        print( h4 )
        index = 1
        h4 = bf.getHessian( weights=w, params=p, index=index )
        print( h4 )
        index = [0,1]
        w /= 2
        h4 = bf.getHessian( weights=w, params=p, index=index )
        print( h4 )
        print( bf.sumwgt )

        ih = bf.getInverseHessian()
        print( ih )

        dia = np.inner( h1, ih )
        print( dia )
        assertAAE( dia, np.eye( 2 ) )

    def testChiSquared( self ) :
        print( "====testChiSquared======================" )
        x = np.arange( 10, dtype=float )
        pm = PolynomialModel( 1 )
        bf = BaseFitter( x, pm )
        y = np.ones( 10, dtype=float )
        w = np.ones( 10, dtype=float )

        print( bf.model.parameters )
        c1 = bf.chiSquared( y )
        print( c1, bf.sumwgt )
        self.assertTrue( c1 == bf.chisq )
        self.assertTrue( bf.sumwgt == 10 )

        w /= 2
        c2 = bf.chiSquared( y, weights=w )
        print( c2, bf.sumwgt )

        cov = bf.covariance
        print( cov )

        s1 = bf.stdevs
        print( s1 )

    def testEvidence( self ) :
        print( "====testEvidence======================" )
        x = np.arange( 11, dtype=float ) - 5
        pm = PolynomialModel( 1 )
        bf = Fitter( x, pm )
        np.random.seed( 12345 )
        y = 0.2 + 0.3 * x + np.random.randn( 11 ) * 0.1
        w = np.ones( 11, dtype=float )

        par = bf.fit( y, w )
        print( "chisq %f  scale %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.sumwgt ) )

        lolim = [-10.0,-10.0]
        hilim = [+10.0,+10.0]


        print( "= 0 ====== Parameters only" )

        evi0 = bf.getLogZ( limits=[lolim,hilim] )
        occ0 = bf.logOccam
        lhd0 = bf.logLikelihood
        print( "evid %f  occam %f  lhood %f" % ( evi0, occ0, lhd0 ) )
        self.assertTrue( bf.getEvidence( limits=[-10.0,10.0] ) == evi0 / math.log( 10.0 ) )

        nslim = [0.01,10.0]
        print( "= 1 ====== Parameters and scale" )
        evi1 = bf.getLogZ( limits=[-10.0,10.0], noiseLimits=nslim )
        occ1 = bf.logOccam
        lhd1 = bf.logLikelihood
        print( "evid %f  occam %f  lhood %f" % ( evi1, occ1, lhd1 ) )
        self.assertTrue( bf.fixedScale is None  )
        self.assertRaises( AttributeError, bf.__getattr__, "minimumScale" )

        print( "= 2 ====== Parameters and fixed scale = 0.01" )
        bf.fixedScale = 0.01
        evi2 = bf.getLogZ( limits=[lolim,hilim] )
        occ2 = bf.logOccam
        lhd2 = bf.logLikelihood
        print( "evid %f  occam %f  lhood %f" % ( evi2, occ2, lhd2 ) )
        self.assertFalse( bf.fixedScale is None )
        self.assertRaises( AttributeError, bf.__getattr__, "minimumScale" )

        print( "= 3 ====== Parameters and fixed scale = 0.1" )
        bf.fixedScale = 0.1
        evi3 = bf.getLogZ( limits=[lolim,hilim] )
        occ3 = bf.logOccam
        lhd3 = bf.logLikelihood
        print( "evid %f  occam %f  lhood %f" % ( evi3, occ3, lhd3 ) )

        print( "= 4 ====== Parameters and fixed scale = 1.0" )
        bf.fixedScale = 1.0
        evi4 = bf.getLogZ( limits=[lolim,hilim] )
        occ4 = bf.logOccam
        lhd4 = bf.logLikelihood
        print( "evid %f  occam %f  lhood %f" % ( evi4, occ4, lhd4 ) )

        print( "= 5 ====== Parameters and fixed scale = 10.0" )
        bf.fixedScale = 10.0
        evi5 = bf.getLogZ( limits=[lolim,hilim] )
        occ5 = bf.logOccam
        lhd5 = bf.logLikelihood
        print( "evid %f  occam %f  lhood %f" % ( evi5, occ5, lhd5 ) )
        self.assertFalse( bf.fixedScale is None )

        # no noiseLimit is the same as fixedScale=1.0
        self.assertTrue( evi0 == evi4 )
        self.assertTrue( occ0 == occ4 )
        self.assertTrue( lhd0 == lhd4 )

        # evidence with the `right' fixed scale is the best; better than auto scale
        self.assertTrue( evi3 > evi1 )      # auto scaling
        self.assertTrue( evi3 > evi2 )      # scale = 0.01
        self.assertTrue( evi3 > evi4 )      # scale = 1.0
        self.assertTrue( evi3 > evi5 )      # scale = 10.0

        print( "======= limits inside the model " )
        pm.setLimits( lolim, hilim )
        print( "limits par[0]  ", pm.priors[0].lowLimit, pm.priors[0].highLimit )
        print( "limits par[1]  ", pm.priors[1].lowLimit, pm.priors[1].highLimit )
        print( "umin           ", pm.priors[0]._umin, pm.priors[1]._umin )
        print( "ranges         ", pm.priors[0]._urng, pm.priors[1]._urng )
        self.assertTrue( pm.priors[0]._urng == 20.0 )
        self.assertTrue( pm.priors[1]._urng == 20.0 )

        bf.fixedScale = None
        evi6 = bf.getLogZ( )
        occ6 = bf.logOccam
        lhd6 = bf.logLikelihood
        print( "evid %f  occam %f  lhood %f" % ( evi0, occ0, lhd0 ) )
        self.assertTrue( bf.getEvidence( ) == evi0 / math.log( 10.0 ) )

        # no noiseLimit is the same as fixedScale=1.0
        self.assertTrue( evi0 == evi6 )
        self.assertTrue( occ0 == occ6 )
        self.assertTrue( lhd0 == lhd6 )


#    def testNullModel( self ) :
#        print( "====testNullModel======================  TBD" )


if __name__ == '__main__':
    unittest.main( )

