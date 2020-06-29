import numpy as numpy
from astropy import units
import math
from . import Tools
from .Sample import Sample

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2008 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester


class SampleList( list ):
    """
    SampleList is a list of Samples, see @Sample

    SampleList is the main result of the NestedSampler. It contains all
    information to calculate averages, medians, modi or maximum likihood solutions
    of the parameters, or of any function of the parameters; in particular of the
    Model.

    To make averages one has to take into account the weights. Each Sample has a weight
    and all weights sum to 1.0. So the average of any function, f, of the parameters p is

        E( f(p) ) = &sum; w_k f( p_k )

    where the sum is over all samples k.

    A large set of utility functions is provided to extract the information from the
    SampleList.


    Attributes
    ----------
    parameters : numpy.array (read-only)
        The average over the parameters. Not for dynamic models.
    stdevs, standardDeviations : numpy.array (read-only)
        The standard deviations for the parameters. Not for dynamic models
    scale : float
        The average of the noise scale
    stdevScale : float
        the standard deviation of the scale.

    logZ : float (read-only)
        Natural log of evidence
    evidence : float (read-only)
        log10( Z ). Evidence * 10 is interpretable as dB.
    info : float (read-only)
        The information H. The compression factor ( the ratio of the prior space
        available to the model parameters over the posterior space ) is equal to the exp( H ).

    maxLikelihoodIndex : int (read-only)
        The index at which the max likelihood can be found: always the last in the list
    maxLikelihoodParameters : numpy.array (read-only)
        The maximum likelihood parameters at the maxLikelihoodIndex.
    maxLikelihoodScale : float (read-only)
        The maximum likelihood noise scale at the maxLikelihoodIndex.
    medianIndex : int (read-only)
        The index at which the median can be found: the middle of the cumulative weights.
        It is calculated once and then kept.
    medianParameters : numpy.array (read-only)
        The median of the parameters at the medianIndex
    medianScale : float (read-only)
        The median of the noise scale at the medianIndex
    modusIndex : int (read-only)
        The index at which the modus can be found: the largest weight
        It is calculated once and then kept.
    modusParameters : numpy.array (read-only)
        The modus of the parameters at the modusIndex
    modusScale : float (read-only)
        The modus of the noise scale at the modusIndex.

    normalized : bool
        True when the weights are normalized to SUM( weights ) = 1


    Author       Do Kester

    """
    def __init__( self, model, nsamples, parameters=None, fitIndex=None, ndata=1 ):
        """
        Constructor.

        Parameters
        ----------
        nsamples : int
            number of samples created.
        model : Model
            to be used in the samples
        parameters : array_like
            list of model parameters
        fitIndex : array of int
            indicating which parameters need fitting
        ndata : int
            length of the data vector; to be used in stdev calculations

        """
        super( SampleList, self ).__init__( )
        self._count = 0
        self.iteration = 0
        self.logZ = 0.0
        self.info = 0.0
        self.addSamples( model, nsamples, parameters, fitIndex=fitIndex )
        self.maxLikelihoodIndex = -1            # always the last one
        self.normalized = False
        self.ndata = ndata

    def addSamples( self, model, nSamples, parameters, fitIndex=None ):
        for i in range( nSamples ) :
            if model.isDynamic() :
                model = model.copy()
                if fitIndex is not None :
                    fitIndex = fitIndex.copy()
            sample = Sample( self._count, -1, self.iteration, model,
                             parameters=parameters, fitIndex=fitIndex )
            self.append( sample )
            self._count += 1

    def __getattr__( self, name ) :
        if name == "parameters" :
            return self.getParameters()
        elif name == "stdevs" or name == "standardDeviations" :
            self.getParameters()
            return self.stdevs
        elif name == "hypars" :
            return self.getHypars()
        elif name == "stdevHypar" :
            self.getHypars()
            return self.stdevHypar
        elif name == "nuisance" :
            return self.getNuisance()
        elif name == "stdevNuis" :
            self.getNuisance()
            return self.stdevNuis
        elif name == "scale" :
            return self.hypars[0]
        elif name == "stdevScale" :
            return self.stdevHypars[0]

        elif name == "evidence" :
            return self.logZ / math.log( 10.0 )
        elif name == "maxLikelihoodParameters" :
            return self[self.maxLikelihoodIndex].parameters
        elif name == "maxLikelihoodScale" :
            return self[self.maxLikelihoodIndex].hypars[0]
        elif name == "medianIndex" :
            return self.getMedianIndex()
        elif name == "medianParameters" :
            return self[self.medianIndex].parameters
        elif name == "medianScale" :
            return self[self.medianIndex].hypars[0]
        elif name == "modusIndex" :
            we = list( self.getLogWeightEvolution() )
            self.modusIndex = we.index( max( we ) )
            return self.modusIndex
        elif name == "modusParameters" :
            return self[self.modusIndex].parameters
        elif name == "modusScale" :
            return self[self.modusIndex].hypars[0]


        else :
            raise AttributeError( "Unknown attribute " + name )

        return None

    # ===========================================================================
    def sample( self, k, sample=None ) :
        """
        Set or return the k-th sample from the list.

        Parameters
        ----------
        k : int
            the index of the sample
        sample : Sample
            if present, set the kth sample with sample
        """
        if sample is not None :
            self[k] = sample

        return self[k]


    def normalize( self ):
        """
        Normalize the samplelist.
        make Sum( weight ) = 1

        """
        self.normalized = True
        lwev = self.getLogWeightEvolution()

        lmax = numpy.max( lwev )
        lwev -= lmax

        lswt = math.log( numpy.sum( numpy.exp( lwev ) ) )

        for sample in self :
            sample.logW -= ( lmax + lswt )


    def add( self, sample ):
        """
        Add a Sample to the list

        Parameters
        ----------
        sample : Sample
            the sample to be added

        """
        sample.parent = sample.id       ## where it is from
        sample.id = self._count
        self._count += 1
        self.append( sample )
        self.normalized = False

    def copy( self, src, des ):
        """
        Copy one item of the list onto another.

        Parameters
        ----------
        src : int
            the source item
        des : int
            the destination item

        """
        id = self[des].id
        self[des] = self[src].copy()
        self[des].id = id


    def weed( self, maxsize=None ):
        """
        Weed superfluous samples.

        If MaxSamples has been set, it is checked whether the size of the
        SampleList exceeds the maximum. If so the Sample with the smallest
        log( Weight ) is removed.
        weed( ) is called recursively until the size has the required length.

        """
        if maxsize is None :
            return

        while len( self ) > maxsize :
            if self[0].logW < self[-1].logW :
                self.remove( self[0] )
            else :
                self.remove( self[-1] )
        return


    def logPlus( self, x, y ):
        """
        Return  log( exp(x) + exp(y) )
        """
        return numpy.logaddexp( x, y )

    # ===== AVERAGES and STDEVS ===================================================
    def getParameters( self ):
        """
        Calculate the average of the parameters and the standard deviations.

        Return
        ------
            The average values of the parameters.
        Raises
        ------
            ValueError when using Dynamic Models

        """
        mdl = self[0].model
        if not ( mdl.hasPriors() and any( [mdl.getPrior( k ).isCircular() for k in range( mdl.npchain )] ) ) :
            ( a, s ) = self.averstd( "parameters" )
            self.stdevs = s
            return a

        par, wgt = self.getParAndWgtEvolution()
        np = self[0].model.npchain
        param = numpy.zeros( np, dtype=float )
        stdev = numpy.zeros( np, dtype=float )
        for k in range( np ) :
            pr = mdl.getPrior( k )
            clh = None if not pr.isCircular() else pr.getLimits()
            param[k], stdev[k] = Tools.average( par[:,k], weights=wgt, circular=clh )

        self.parameters = param
        self.stdevs = stdev

        return self.parameters

        """
        np = self[0].model.npchain
        param = numpy.zeros( np, dtype=float )
        stdev = numpy.zeros( np, dtype=float )
        sumwt = 0.0
        for sample in self :
            if sample.model.npchain != np :
                raise ValueError( "Models with different " + "numbers of parameters: Cannot average" )
            wt = math.exp( sample.logW )
            sumwt += wt
            wp = wt * sample.parameters
            param = param + wp
            stdev = stdev + wp * sample.parameters

        stdev = numpy.sqrt( stdev - param * param )
        self.parameters = param
        self.stdevs = stdev

        return self.parameters
        """

    def getHypars( self ) :
        """
        Return the hyper parameters
        """
        nhp = len( self[0].hyper )

        hypar = numpy.zeros( nhp, dtype=float )
        hydev = numpy.zeros( nhp, dtype=float )
        sw = 0.0
        for sample in self :
            wt = math.exp( sample.logW )
            sw += wt
            ws = wt * sample.hyper
            hypar = hypar + ws
            hydev = hydev + ws * sample.hyper
        self.stdevHypars = numpy.sqrt( hydev - hypar * hypar )
        self.hypars = hypar
        return self.hypars

    def getNuisance( self ) :
        """
        Return the average of the nuisance parameters (if present)
        """
        ( a, s ) = self.averstd( "nuisance" )
        self.stdevNuis = s
        return a

    def averstd( self, name ) :
        """
        Return the average and the stddevs of the named attribute from Sample

        Parameters
        ----------
        name : str
            name of an attribute from Sample
        """
        np = len( getattr( self[0], name ) )

        aver = numpy.zeros( np, dtype=float )
        stdv = numpy.zeros( np, dtype=float )
        sw = 0.0
        for sample in self :
            wt = math.exp( sample.logW )
            sw += wt
            ss = getattr( sample, name )
            ws = wt * ss
            aver = aver + ws
            stdv = stdv + ws * ss
        stdv = numpy.sqrt( stdv - aver * aver )

        return ( aver, stdv )

    # ===== MEDIAN ===========================================================
    def getMedianIndex( self ) :
        """
        Return the index at which the median can be found.
        """
        sum = 0.0
        k = 0
        for sample in self :
            sum += math.exp( sample.logW )
            if sum < 0.5 :
                k += 1
            else :
                break
        self.medianIndex = k
        return self.medianIndex

     # ===== EVOLUTIONS ========================================================
    def getMaximumNumberOfParameters( self ):
        """
        Return the maximum number of parameters (for Dynamic Models)
        """
        if self[0].model.isDynamic( ) :
            return numpy.max( self.getNumberOfParametersEvolution() )

        return self[0].model.npchain

    def getParameterEvolution( self, kpar=None ):
        """
        Return the evolution of one or all parameters.

        In case of dynamic models the number of parameters may vary.
        They are zero-padded. Use `getNumberOfParametersEvolution`
        to get the actual number.

        Parameters
        ----------
        kpar : int or tuple of ints
            the parameter to be selected. Default: all

        """
        pe = []
        for sample in self :
            pe += [sample.parameters]
        if kpar is None :
            return numpy.asarray( pe )
        else :
            return numpy.asarray( pe )[:,kpar]

    def getParAndWgtEvolution( self ):
        """
        Return the evolution of parameters and weights.

        In case of dynamic models the number of parameters may vary.
        They are zero-padded. Use `getNumberOfParametersEvolution`
        to get the actual number.

        """
        pe = []
        we = []
        for sample in self :
            pe += [sample.parameters]
            we += [sample.logW]
        return ( numpy.asarray( pe ), numpy.exp( numpy.asarray( we ) ) )


    def getNumberOfParametersEvolution( self ):
        """ Return the evolution of the number of parameters.  """
        pe = [sample.model.npchain for sample in self]
        return numpy.asarray( pe )

    def getScaleEvolution( self ):
        """ Return the evolution of the scale.  """
        pe = [sample.hypars for sample in self]
        return numpy.asarray( pe )

    def getLogLikelihoodEvolution( self ):
        """ Return the evolution of the log( Likelihood ).  """
        pe = [sample.logL for sample in self]
        return numpy.asarray( pe )

    def getLogWeightEvolution( self ):
        """
        Return the evolution of the log( weight ).

        The weights itself sum up to 1.
        See #getWeightEvolution( ).

        """
        pe = [sample.logW for sample in self]
        return numpy.asarray( pe )

    def getWeightEvolution( self ):
        """
        Return the evolution of the weight.

        The weights sum to 1.

        """
        return numpy.exp( self.getLogWeightEvolution( ) )

    def getParentEvolution( self ):
        """ Return the evolution of the parentage.  """
        pe = []
        for sample in self :
            pe += [sample.parent]
        return numpy.asarray( pe )

    def getStartEvolution( self ):
        """ Return the evolution of the start generation.  """
        pe = []
        for sample in self :
            pe += [sample.start]
        return numpy.asarray( pe )

    def getGeneration( self ):
        """ Return the generation number pertaining to the evolution.  """
        pe = []
        for sample in self :
            pe += [sample.id]
        return numpy.asarray( pe )

    def getLowLogL( self ):
        """
        Return the lowest value of logL in the samplelist, plus its index.
        """
        low = self[0].logL
        klo = 0
        k = 0
        for sample in self :
            if sample.logL < low :
                klo = k
                low = sample.logL
            k += 1
        return ( low, klo )


    # ===== AVERAGE RESULTS ===================================================
    def average( self, xdata ):
        """
        Return the (weighted) average result of the model(s) over the samples.

        Parameters
        ----------
        xdata : array_like
            the input

        """
        ndata = Tools.length( xdata )
        result = numpy.zeros( ndata, dtype=float )
        error = numpy.zeros( ndata, dtype=float )
        sumwgt = 0
        for sample in self :
            yfit = sample.model.result( xdata, sample.parameters )
            wgt = math.exp( sample.logW )
            yw = yfit * wgt
            result += yw
            error  += yw * yfit
            sumwgt += wgt

#        self.error = numpy.sqrt( ( error - result * result ) / self.ndata )
        self.error = numpy.sqrt( error - result * result )
        self.result = result

        return self.result

    # ===== MONTE CARLO ERRORS ===================================================
    def monteCarloError( self, xdata ):
        """
        Calculates 1-\sigma-confidence regions on the model given some inputs.

        The model is run with the input for the parameters in each of the
        samples. Appropiately weighted standard deviations are calculated
        and returned at each input value.

        Parameters
        ----------
        xdata : array_like
           the input vectors.

        Returns
        -------
        error : array_like
            standard deviations at each input point

        """
        if Tools.length( xdata ) != len( self.result ):
            self.average( xdata )
        return self.error

