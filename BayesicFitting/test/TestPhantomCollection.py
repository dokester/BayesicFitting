# run with : python3 -m unittest TestPhantomCollection

import unittest
import numpy as np
import math
import os

from numpy.testing import assert_array_equal as assertAE
from numpy.testing import assert_array_almost_equal as assertAAE

import matplotlib.pyplot as plt
from BayesicFitting import *
from BayesicFitting import formatter as fmt


class Test( unittest.TestCase  ) :

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def test1( self ) :
        print( "====test 1 Static====================" )

        m = PolynomialModel( 3 )
        m.setPrior( 0, UniformPrior( limits=[-5,5] ) )
        problem = ClassicProblem( model=m )

        numpy.random.seed( 12345 )

        phc = PhantomCollection( )
        for k in range( 10 ) :
            pars = numpy.random.randn( 4 ) / ( k + 1 )
            logL = -numpy.sum( numpy.square( pars ) )

            walker = Walker( k, problem, pars, None, logL=logL )
            phc.storeItems( walker )

        for k, ph in enumerate( phc.phantoms ) :
            print( fmt( k ), fmt( ph.logL ), fmt( ph.allpars ) )

        for k in range( 10, 20 ) :
            lowL = numpy.amin( phc.phantoms[0].logL )
            while True :
                pars = numpy.random.randn( 4 ) / ( k + 1 )
                logL = -numpy.sum( numpy.square( pars ) )
                if logL > lowL : break

            walker = Walker( k, problem, pars, None, logL=logL )
            phc.storeItems( walker )

            ur, um = phc.getParamMinmax( lowL )
            print( fmt( k ), fmt( ur ), fmt( um ), phc.length(), fmt( phc.phantoms[0].logL ) )


        for k, ph in enumerate( phc.phantoms ) :
            print( fmt( k ), fmt( phc.phantoms._count ), fmt( ph.logL ), fmt( ph.allpars ) )
        

    def test2( self ) :
        print( "====test 2 Dynamic====================" )

        N = 30
        numpy.random.seed( 12345 )

        phc = PhantomCollection( dynamic=True )
        for k in range( N ) :
            np = numpy.random.randint( 3, high=6 )

            m = PolynomialDynamicModel( np-1 )
            m.setPrior( 0, UniformPrior( limits=[-5,5] ) )
            problem = ClassicProblem( model=m )

            pars = numpy.random.randn( np ) * 30 / ( k + 1 )
            logL = -numpy.sum( numpy.square( pars ) )
            print( fmt( np ), fmt( logL ), fmt( pars ) )
            walker = Walker( k, problem, pars, None, logL=logL )
            phc.storeItems( walker )
            self.assertTrue( np == phc.phantoms[np][0].problem.npars )

        printclass( phc )

        for n in range( 3, 6 ) :
            for k, ph in enumerate( phc.phantoms[n] ) :
                print( fmt( n ), fmt( k ), fmt( ph.logL ), fmt( ph.allpars ) )

#        lowL = min( [numpy.amin( ph.logL ) for ph in phc.phantoms] )
        lowL = min( [numpy.amin( phc.phantoms[k].getLogL() ) for k in phc.phantoms.keys()] )
        low0 = min( [phc.phantoms[k][0].logL for k in phc.phantoms.keys()] )

        print( "low   ", lowL, low0 )
        self.assertTrue( lowL == low0 )

        np = 5
        ur, um = phc.getParamMinmax( lowL, np=np )
        print( "parange  ", fmt( ur ) )
        print( "parmin   ", fmt( um ) )

        for k in range( N, 2*N ) :
            lowL = min( [phc.phantoms[k][0].logL for k in phc.phantoms.keys()] )
            np = numpy.random.randint( 3, high=6 )
            while True :
                pars = numpy.random.randn( np ) * 30 / ( k + 1 )
                logL = -numpy.sum( numpy.square( pars ) )
                if logL > lowL : break
            walker = Walker( k, problem, pars, None, logL=logL )
            phc.storeItems( walker )

            ur, um = phc.getParamMinmax( lowL, np=np )

            print( fmt( k ), fmt( np ), fmt( phc.length( np ) ), fmt( lowL ) )
            print( "parange  ", fmt( ur ) )
            print( "parmin   ", fmt( um ) )

            if phc.length( np ) <= phc.minpars :
                self.assertTrue( ur is None )
            else :
                self.assertFalse( um is None )

        for n in range( 3, 6 ) :
            for k, ph in enumerate( phc.phantoms[n] ) :
                print( fmt( n ), fmt( phc.phantoms[n]._count ), fmt( k ), fmt( ph.logL ), fmt( ph.allpars ) )

        s = 0
        for np in phc.phantoms :
            s += phc.length( np )
            print( np, phc.length( np ) )
        print( phc.length() )        
        self.assertTrue( s == phc.length() )

if __name__ == '__main__':
    unittest.main( )

