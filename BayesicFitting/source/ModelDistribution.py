import numpy as numpy
import math
import sys

#from .ErrorDistribution import ErrorDistribution
from .ScaledErrorDistribution import ScaledErrorDistribution
from .LinearModel import LinearModel
from .Fitter import Fitter
from .BaseFitter import BaseFitter
from .CurveFitter import CurveFitter
from .AmoebaFitter import AmoebaFitter
from .LevenbergMarquardtFitter import LevenbergMarquardtFitter
from .Tools import setAttribute as setatt


__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.5"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"


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
#  *    2019 - 2025 Do Kester


class ModelDistribution( ScaledErrorDistribution ):
    """
    To calculate the probability of a model M from a set of models S,
    given some data D, use Bayes rule:

        P( M|DS ) = P( M|S ) * P( D|MS ) / P( D|S )
        posterior = prior   * likelihood / evidence

    This class calculates the likelihood P( D|MS ).
    On another level where we calculate the probability of the
    parameters p, we see this likelhood appear as evidence P( D|M ).

    Again using Bayes :

        P( p|DM ) = P( p|M ) * P( D|pM ) / P( D|M )

    The evidence here is calculated as the integral over a Gausian
    approximation of the posterior.

    Author       Do Kester.

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, arbiter=None, scale=1.0, limits=None, 
                  copy=None, **kwargs ):
        """
        Default Constructor.

        Parameters
        ----------
        arbiter : None or BaseFitter or str
            to provide the evidence
            None    select fitter automatically
            BaseFiter   Use this fitter
            str     "fitter", "levenberg", "curve", "amoeba", "NestedSampler"

        scale : float
            noise scale
        limits : None or list of 2 floats [low,high]
            None : no limits implying fixed scale
            low     low limit on scale (needs to be >0)
            high    high limit on scale
            when limits are set, the scale is *not* fixed.

        copy : ModelDistribution
            distribution to be copied.

        kwargs : dict
            to be applied to arbiter

        """
        setatt( self, "arbiter", arbiter )
        setatt( self, "kwarbs", kwargs )

        super( ).__init__( limits=limits, scale=scale, copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return ModelDistribution( copy=self, arbiter=self.arbiter )

    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        Always true for this distribution.
        """
        return True


    #  *********LIKELIHOODS***************************************************
    def logLikelihood_alt( self, problem, allpars ) :
        """
        Return the log( likelihood ) for a Gaussian distribution.

        Alternate calculation

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            list of all parameters in the problem
            Return optimal parameters of the fit

        """
        mdl = problem.model

        if allpars is None :
            allpars = self.rng.rand( mdl.npars + self.nhypar )
            allpars = problem.unit2Domain( allpars )

        try :
            noiselim = self.hyperpar[0].getLimits()
            fscale = None
        except Exception :
            noiselim = None
            fscale = self.scale

        if noiselim is None and mdl.npars < len( allpars ) :
            allpars[-1] = self.hyperpar[0].hypar

        kwarbs = self.kwarbs

        if self.arbiter is None :
            if isinstance( mdl, LinearModel ) :
                ftr = Fitter( problem.xdata, mdl, fixedScale=fscale, **kwarbs )
            else :
                ftr = LevenbergMarquardtFitter( problem.xdata, mdl, fixedScale=fscale,
                            **kwarbs )
        elif isinstance( self.arbiter, BaseFitter ) :
            ftr = self.arbiter

        elif not isinstance( self.arbiter, str ) :
            raise ValueError( "Cannot interpret %s as string or fitter" % self.arbiter )

        else :
            name = str.lower( self.arbiter )

            if name == "fitter" :
                ftr = Fitter( problem.xdata, mdl, fixedScale=fscale, **kwarbs )
            elif name.startswith( "leven" ) :
                ftr = LevenbergMarquardtFitter( problem.xdata, mdl, fixedScale=fscale, 
                            **kwarbs )
            elif name.startswith( "curve" ) :
                ftr = CurveFitter( problem.xdata, mdl, fixedScale=fscale, **kwarbs )
            elif name.startswith( "amoeba" ) :
                ftr = AmoebaFitter( problem.xdata, mdl, fixedScale=fscale, **kwarbs )

            else :
                ## we need a static version of the model
                model = mdl.copy( modifiable=False, dynamic=False )

                ## add items to kwarbs if not already present
                if "ensemble" not in kwarbs :
                    kwarbs["ensemble"] = 10
                if "verbose" not in kwarbs :
                    kwarbs["verbose"] = 0
                if "engines" not in kwarbs :
                    kwarbs["engines"] = ["chord", "galilean"]

                if name.startswith( "nested" ) :
                    ## Import NestedSampler here to avoid circular imports
                    from .NestedSampler import NestedSampler
                    ######################################################
                    ns = NestedSampler( model=model, xdata=problem.xdata, ydata=problem.ydata,
                        weights=problem.weights, limits=noiselim, **kwarbs )
                elif name.startswith( "phantom" ) :
                    ## Import PhantomSampler here to avoid circular imports
                    from .PhantomSampler import PhantomSampler
                    ######################################################
                    ns = PhantomSampler( model=model, xdata=problem.xdata, ydata=problem.ydata,
                        weights=problem.weights, limits=noiselim, **kwarbs )
                else :
                    raise ValueError( "Cannot interpret %s" % self.arbiter )

                try :
                    evidence = ns.sample()
                    allpars[:mdl.npars] = ns.parameters
                    if noiselim is not None :
                        allpars[-1] = ns.scale
                except RuntimeError :
                    evidence = -math.inf

                return evidence


        ## Run the fitters
        try :
            pars = ftr.fit( problem.ydata )

            for k,p in enumerate( pars ) :
                mdl.getPrior( k ).checkLimit( p )

            evidence = ftr.getLogZ( limits=mdl.getLimits(), noiseLimits=noiselim )

            allpars[:mdl.npars] = pars
            if noiselim is not None :
                allpars[-1] = ftr.scale

#            print( problem.npars, mdl.npars, noiselim, ftr.scale, allpars )

        except numpy.linalg.LinAlgError :
            evidence = -sys.float_info.max
        except ValueError :                         # math domain error or OOL
            evidence = -sys.float_info.max


        return evidence

    def logLdata( self, problem, allpars, mockdata=None ) :
        """
        Return the log( likelihood ) for each residual
           
        logL = sum( logLdata )

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            list of all parameters in the problem   
        mockdata : array_like
            as calculated by the model
        
        """
        return self.logLikelihood_alt( problem, allpars )


    def __str__( self ) :
        return "ModelDistribution"
