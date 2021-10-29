# run with : python3 -m unittest TestPrior2
# or :       python3 -m unittest TestPrior2.Test.test1

import unittest
import numpy as numpy
import math

from BayesicFitting import Prior, UniformPrior, JeffreysPrior, ExponentialPrior
from BayesicFitting import LaplacePrior, CauchyPrior, GaussPrior
from BayesicFitting import CircularUniformPrior
from BayesicFitting import PolynomialModel, NestedSampler

__author__ = "Do Kester"
__year__ = 2017
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *  2006-2015 Do Kester (JAVA CODE)

class Test( unittest.TestCase ) :
    """
    Test for Priors
    """

    def test1( self ) :

        print( "===========Gauss Prior Limitation ===========" )

        NP = 100
        x = numpy.zeros( NP, dtype=float )
        y = numpy.random.randn( NP )

        print( numpy.mean( numpy.append( y, [5.0] ) ) )

        mdl = PolynomialModel( 0 )

        mdl.setPrior( 0, GaussPrior( center=4.0, scale=1.0 ) )

        ns = NestedSampler( x, mdl, y, verbose=2 )

        logE = ns.sample()

        print( ns.parameters, logE )

        lim = math.exp( 4 )
        mdl.setPrior( 0, UniformPrior( limits=[-lim,lim] ) )

        ns = NestedSampler( x, mdl, y, verbose=2 )

        logE = ns.sample()

        print( ns.parameters, logE )



    @classmethod
    def suite( cls ):
        return ConfiguredTestCase.suite( PriorTest.__class__ )

if __name__ == '__main__':
    unittest.main( )


