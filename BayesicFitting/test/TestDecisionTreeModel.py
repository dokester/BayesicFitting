#run with: python3 -m unittest TestDecisionTreeModel

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import formatter as fmt

__author__ = "Do Kester"
__year__ = 2018
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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
#  *    2016 Do Kester

class TestDecisionTreeModel( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )
        self.dofull = ( "DOFULL" in os.environ and os.environ["DOFULL"] == "1" )

    def test1( self ):
        print( "  Test 1 DecisionTreeModel" )
        dtm = DecisionTreeModel( )


        print( dtm )
        print( dtm.npars )
        cdtm = dtm.copy()
        print( cdtm )
        print( cdtm.npars )

        dtm1 = DecisionTreeModel( ndim=9, kdim=[0], depth=1 )
        print( dtm1 )
        print( dtm1.npars )

        dtm2 = DecisionTreeModel( ndim=9, kdim=[0,1,2], depth=2 )
        print( dtm2 )
        print( dtm2.npars )

        dtm3 = DecisionTreeModel( ndim=20, kdim=[0,1,2,3,4,5,6],
                    split=[0.1*k for k in range(2,8)], depth=3 )
        print( dtm3 )
        print( dtm3.npars )
        cdtm = dtm3.copy()
        print( cdtm )
        print( cdtm.npars )

        print( "============================" )
        wk = dtm3.walk()
        while True :
            try :
                pm = next( wk )
                if pm is None :
                    print( "TEST0  ", pm )
                else :
                    print( "TEST1  ", pm.shortName(), pm.dimension )
            except :
                break

        print( dtm3.findLeaf( 0 ) )
        print( dtm3.findLeaf( 1 ) )
        print( dtm3.findLeaf( 2 ) )
        print( dtm3.findLeaf( 4 ) )
        print( dtm3.findLeaf( 6 ) )

        printclass( dtm3 )
        printclass( cdtm )

        printclass( dtm3.left )
        printclass( cdtm.left )

    def test1a( self ):
        print( "  Test 1a DecisionTreeModel" )
        dtm = DecisionTreeModel( )
        print( dtm, dtm.isModifiable(), dtm.isDynamic() )
        cdtm = dtm.copy()
        print( cdtm, cdtm.isModifiable(), cdtm.isDynamic() )

        self.assertTrue( dtm.isModifiable() )
        self.assertTrue( cdtm.isModifiable() )

        dtm = DecisionTreeModel( ndim=9, kdim=[0], depth=1, modifiable=False )
        print( dtm, dtm.isModifiable(), dtm.modifiable )
        cdtm = dtm.copy()
        print( cdtm, cdtm.isModifiable(), cdtm.modifiable )

        self.assertFalse( dtm.isModifiable() )
        self.assertFalse( cdtm.isModifiable() )

    def test2( self ):
        print( "  Test 2 DecisionTreeModel" )
        ND = 10
        NP = 100
        m = DecisionTreeModel( ndim=ND, kdim=[0,1,2,3,4,5,6], depth=3 )
        print( m )

        numpy.random.seed( 12345 )
        xdata = numpy.random.rand( NP, ND )
        print( fmt( xdata ) )
        par0 = numpy.arange( m.npars, dtype=float ) + 1

        res = m.result( xdata, par0 )
        part = m.partial( xdata, par0 )

        for k in range( NP ) :
            print( fmt( res[k] ), fmt( part[k,:], max=None ) )
            self.assertTrue( part[k,int(res[k]-0.99)] == 1 )
            self.assertTrue( numpy.sum( part[k,:] ) == 1 )


    def test3( self ):
        print( "  Test 3 DecisionTreeModel" )

        for k in range( 4 ) :
            print( "==== depth : %d ============" % k )
            dtm = DecisionTreeModel( ndim=20, kdim=[0,1,2,3,4,5,6,7,8,9],
                    split=0.3+0.1*k, itypes=[0,1,3,7]*5, depth=k )
            print( dtm.fullName() )

            print( "CODE  ", dtm.encode() )

        dtm = DecisionTreeModel( ndim=20, kdim=[0,1,2,3,4,5,6,7,8,9],
                    split=0.5, depth=0, itypes=[0,1,3,5]*5 )
        for k in range( 4 ) :
            print( "==== grow  : %d ============" % k )
            dtm.grow( location=0, kdim=2+k, split=0.2+0.1*k )
            print( dtm.fullName() )
            print( "CODE  ", dtm.encode() )

#        dtm = DecisionTreeModel( ndim=20, kdim=[0,1,2,3,4,5,6,7,8,9],
#                    split=0.5, depth=0, itypes=[0,1,3,5]*5 )
        for k in range( 4 ) :
            print( "==== grow  : %d ============" % k )
            loc = dtm.npars - 1
            dtm.grow( location=loc, kdim=2+k, split=0.2+0.1*k )
            print( dtm.fullName() )
            print( "CODE  ", dtm.encode() )

        code, dims, splim = dtm.encode()
        dt2 = DecisionTreeModel( code=code, kdim=dims, split=splim )
        print( "CODE  ", dt2.encode() )
        print( dt2.fullName( ids=True ) )



    def test4( self ):
        print( "  Test 4 DecisionTreeModel: rencode" )

        for dep in range( 4 ) :
            dtm = DecisionTreeModel( ndim=20, kdim=[0,1,2,3,4,5,6,7,8,9],
                    split=0.5, depth=dep, itypes=[0,1,3,5]*5 )
            code, dims, splim = dtm.encode()
            print( "DEPTH  ", dep, " CODE  ", code, dims, splim )
            print( dtm.fullName( ids=True ) )


            dt2 = DecisionTreeModel( code=code, kdim=dims, split=splim )
            print( "CODE  ", dt2.encode() )
            print( dt2.fullName( ids=True ) )

        dtm = DecisionTreeModel( ndim=20, kdim=[0,1,2,3,4,5,6,7,8,9],
                    split=0.5, depth=0, itypes=[0,1,3,5]*5 )
        dtm.grow( location=0, kdim=2, split=0.2 )
        dtm.grow( location=1, kdim=3, split=0.3 )
        code, dims, splim = dtm.encode()
        print( "CODE  ", code, dims, splim )
        print( dtm.fullName( ids=True ) )

        dt2 = DecisionTreeModel( code=code, kdim=dims, split=splim )
        print( "CODE  ", dt2.encode() )
        print( dt2.fullName( ids=True ) )




    def test5( self ):
        print( "  Test 5 DecisionTreeModel" )
        dtm = DecisionTreeModel( ndim=20, kdim=[0],
                    split=0.5, depth=0 )
        dtm.parameters = numpy.arange( dtm.npars, dtype=float ) + 1

        print( dtm.fullName( ids=True ) )
        print( dtm.encode() )
        print( dtm.copy().fullName( ids=True ) )
        print( fmt( dtm.parameters, max=None ) )

        Tools.printclass( dtm )

        print( "GROW    at location 0 dim 1 split 0.34" )
        dtm.grow( offset=0, location=0, kdim=1, split=0.44 )
        print( dtm.fullName() )
        print( dtm.encode() )
        print( dtm.copy().fullName() )
        print( fmt( dtm.parameters, max=None ) )

        print( "GROW    at location 1 dim 1 split 0.44" )
        dtm.grow( offset=0, location=1, kdim=1, split=0.44 )
        print( dtm.fullName( ids=True ) )
        print( dtm.encode() )
        print( dtm.copy().fullName( ids=True ) )
        print( fmt( dtm.parameters, max=None ) )

        print( "GROW    at location 1 dim 2 split 0.54" )
        dtm.grow( offset=0, location=1, kdim=2, split=0.54 )
        print( dtm.fullName() )
        print( dtm.encode() )
        print( dtm.copy().fullName() )
        print( fmt( dtm.parameters, max=None ) )

        print( "GROW    at location 3 dim 3 split 0.64" )
        dtm.grow( offset=0, location=3, kdim=3, split=0.64 )
        print( dtm.fullName() )
        print( dtm.encode() )
        print( dtm.copy().fullName() )
        print( fmt( dtm.parameters, max=None ) )

        dtm.parameters = numpy.arange( dtm.npars, dtype=float ) + 1
        print( fmt( dtm.parameters, max=None ) )

        print( "SHRINK  at location 4" )
        dtm.shrink( offset=0, location=4 )
        print( dtm.fullName( ids=True ) )
        print( dtm.encode() )
        print( dtm.copy().fullName( ids=True ) )
        print( fmt( dtm.parameters, max=None ) )

        print( "SHRINK  at location 0" )
        dtm.shrink( offset=0, location=0 )
        print( dtm.fullName() )
        print( dtm.encode() )
        print( dtm.copy().fullName() )
        print( dtm.copy().encode() )
        print( fmt( dtm.parameters, max=None ) )






    def test6( self ):
        print( "  Test 6 DecisionTreeModel" )
        dtm = DecisionTreeModel( ndim=20, kdim=[0,1,2,3,4,5,6],
                    split=[0.1*k for k in range(2,8)], depth=3 )
        dtm.parameters = numpy.arange( dtm.npars, dtype=float ) + 1

        print( dtm.fullName() )
        print( fmt( dtm.parameters, max=None ) )
        self.assertTrue( dtm.npbase == dtm.npars )
        self.assertTrue( dtm.npars == dtm.countLeaf() )
        self.assertTrue( dtm.ncomp == dtm.countBranch() )


        print( "GROW    at location 2 dim 3 split 0.44" )
        dtm.grow( offset=0, location=2, kdim=3, split=0.44 )
        print( dtm )
        print( fmt( dtm.parameters, max=None ) )
        self.assertTrue( dtm.npbase == dtm.npars )
        self.assertTrue( dtm.npars == dtm.countLeaf() )
        self.assertTrue( dtm.ncomp == dtm.countBranch() )

        print( "VARY    at location 4, dim=5, split=0.55" )
        dtm.vary( location=4, kdim=5, split=0.55 )
        print( dtm )
        print( fmt( dtm.parameters, max=None ) )
        self.assertTrue( dtm.npbase == dtm.npars )
        self.assertTrue( dtm.npars == dtm.countLeaf() )
        self.assertTrue( dtm.ncomp == dtm.countBranch() )

        print( "GROW    at location 8" )
        dtm.grow( offset=0, location=8 )
        print( dtm )
        print( fmt( dtm.parameters, max=None ) )
        self.assertTrue( dtm.npbase == dtm.npars )
        self.assertTrue( dtm.npars == dtm.countLeaf() )
        self.assertTrue( dtm.ncomp == dtm.countBranch() )
        self.assertTrue( len( dtm.parNames ) == dtm.npars )

        print( "SHRINK  at location 7" )
        dtm.shrink( offset=0, location=7 )
        print( dtm )
        print( fmt( dtm.parameters, max=None ) )
        self.assertTrue( dtm.npbase == dtm.npars )
        self.assertTrue( dtm.npars == dtm.countLeaf() )
        self.assertTrue( dtm.ncomp == dtm.countBranch() )

        print( "SHRINK  at location 3" )
        dtm.shrink( offset=0, location=3 )
        print( dtm )
        print( fmt( dtm.parameters, max=None ) )
        self.assertTrue( dtm.npbase == dtm.npars )
        self.assertTrue( dtm.npars == dtm.countLeaf() )
        self.assertTrue( dtm.ncomp == dtm.countBranch() )

        print( "SHRINK  at location 0" )
        dtm.shrink( offset=0, location=0 )
        print( dtm.fullName() )
        print( fmt( dtm.parameters, max=None ) )
        self.assertTrue( dtm.npbase == dtm.npars )
        self.assertTrue( dtm.npars == dtm.countLeaf() )
        self.assertTrue( dtm.ncomp == dtm.countBranch() )

        printclass( dtm )

    def test7( self ):
        print( "  Test 7 DecisionTreeModel" )
        ND = 10
        NP = 100

        dtm = DecisionTreeModel( ndim=ND, kdim=[4,1,1,3,1,4,5],
                    split=0.5, depth=3 )
        print( dtm )

        numpy.random.seed( 12345 )
        xdata = numpy.random.rand( NP, ND )

        ydata = numpy.zeros( NP, dtype=float )
        ydata += 1.4 + 0.3 * xdata[:,4] - 0.1 * xdata[:,1] * xdata[:,6]

        ftr = Fitter( xdata, dtm )

        pars = ftr.fit( ydata )

        print( fmt( pars, max=None ) )

        yfit = dtm( xdata )

        ksrt = numpy.argsort( yfit )
        xxx = numpy.arange( NP, dtype=float )

        if not self.doplot : return

        plt.plot( xxx, ydata[ksrt], 'k.' )
        plt.plot( xxx, yfit[ksrt], 'r-' )

        plt.show()

    def testNestedSampler( self ) :
        print( "========================" )
        print( "  Test Nested Sampler" )
        print( "========================" )

        ND = 10
        NP = 100

        numpy.random.seed( 12345 )
        xdata = numpy.random.rand( NP, ND ) * 10
        print( fmt( xdata ) )

        y = 0.5 * xdata[:,1]
        print( xdata.shape, y.shape )
        y += numpy.where( xdata[:,4] > 3, 5, 0 )
        y += numpy.where( xdata[:,6] > 8, 0, 3 )
        y += numpy.where( xdata[:,4] > 7, 2, 0 )

        noise = numpy.random.randn( NP )
        y += 0.02 * noise

        pm = DecisionTreeModel( ndim=ND, kdim=[0], depth=0 )
        print( pm )

        lolim = [-10]
        hilim = [+10]
        pm.setLimits( lowLimits=lolim, highLimits=hilim )
        Tools.printclass( pm )

        ns = NestedSampler( xdata, pm, y, ensemble=100, seed=2031967 )

        ns.verbose = 2
        ns.weed = 10000
        ns.distribution.setLimits( [0.01, 100] )
        if not self.dofull :
            ns.ensemble = 10

        logE = ns.sample( )

        sl = ns.samples

        yfit = sl.average( xdata )

#        ksrt = numpy.argsort( yfit )
        xxx = numpy.arange( NP, dtype=float )

        mi = sl.medianIndex

        print( mi, sl.modusIndex, len( sl ) )

        if not self.doplot : return

        mdl = sl[mi].model
        ksrt = mdl.sortXdata( xdata )
        plt.plot( xxx, y[ksrt], 'k.' )
        plt.plot( xxx, yfit[ksrt], 'r-' )

        for k in range( mi-3, mi+4 ) :
            mdl = sl[k].model
            print( mdl.fullName() )
            ymod = mdl.result( xdata, sl[k].parameters )

            plt.plot( xxx, ymod[ksrt], 'g-' )

        print( ymod )
        print( ksrt )
        print( ymod[ksrt] )

        plt.show()

### TBD

    def XXXtestNestedSampler2( self ) :
        print( "========================" )
        print( "  Test Nested Sampler 2" )
        print( "========================" )

        ND = 10
        NP = 100

        numpy.random.seed( 12345 )
        xdata = numpy.random.rand( NP, ND ) * 10
        print( fmt( xdata ) )

        y = 0.5 * xdata[:,1]
        print( xdata.shape, y.shape )
        y += numpy.where( xdata[:,4] > 3, 5, 0 )
        y += numpy.where( xdata[:,6] > 8, 0, 3 )
        y += numpy.where( xdata[:,4] > 7, 2, 0 )

        noise = numpy.random.randn( NP )
        y += 0.02 * noise

        pm = DecisionTreeModel( ndim=ND, kdim=[0], depth=0 )
        print( pm )

        lolim = [-10]
        hilim = [+10]
        pm.setLimits( lowLimits=lolim, highLimits=hilim )
        Tools.printclass( pm )

        ed = ModelLikelihood( limits=[0.01,100] )

        engs = ["birth", "death", "struct"]
#        engs = ["birth", "struct"]
        ns = NestedSampler( xdata, pm, y, ensemble=100, distribution=ed,
                            engines=engs, seed=2031967 )

#        ns.minimumIterations = 4000
        ns.verbose = 2
#        ns.weed = 10000

        logE = ns.sample( )

        sl = ns.samples

        yfit = sl.average( xdata )

        ksrt = numpy.argsort( yfit )
        xxx = numpy.arange( NP, dtype=float )

        mi = sl.medianIndex

        print( mi, sl.modusIndex, len( sl ) )

        if not self.doplot : return

        plt.plot( xxx, y[ksrt], 'k.' )
        plt.plot( xxx, yfit[ksrt], 'r-' )

        for k in range( mi-3, mi+4 ) :
            mdl = sl[k].model
            print( mdl.fullName() )
            ymod = mdl.result( xdata, sl[k].parameters )

            plt.plot( xxx, ymod[ksrt], 'g-' )

        print( ymod )
        print( ksrt )

        plt.show()

        print( ymod[ksrt] )

    def suite( cls ):
        return unittest.TestCase.suite( TestDynamicModel.__class__ )


if __name__ == '__main__':
    unittest.main()

