# run with : python3 -m unittest TestPhantomCollection

import unittest
import os


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

        printclass( phc )

        for k, ph in enumerate( phc.phantoms ) :
            print( fmt( k ), fmt( ph.logL ), fmt( ph.allpars ) )

        for k in range( N-1 ) :
            self.assertTrue( phc.phantoms[k].logL < phc.phantoms[k+1].logL )

        np = 5
        lowL = phc.phantoms[0].logL
        ur, um = phc.getParamMinmax( lowL, np=np )
        print( "parange  ", fmt( ur ) )
        print( "parmin   ", fmt( um ) )

        for k in range( N, 2*N ) :
            lowL = min( [ph.logL for ph in phc.phantoms] )
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

        printclass( phc.phantoms[0] )

        for k, ph in enumerate( phc.phantoms ) :
            print( fmt( k ), fmt( ph.id ), fmt( ph.logL ), fmt( ph.allpars ) )


if __name__ == '__main__':
    unittest.main( )

