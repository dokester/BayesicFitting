import numpy as numpy
from astropy import units
import math

from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt

from .LinearModel import LinearModel
from .Dynamic import Dynamic
from .Modifiable import Modifiable
from .ExponentialPrior import ExponentialPrior
from .UniformPrior import UniformPrior

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"


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
#  *    2019 - 2020 Do Kester


class DecisionTreeModel( Modifiable, Dynamic, LinearModel ):
    """
    A DecisionTree Model (DTM) is mostly defined on multiple input dimensions (axes).
    It splits the data in 2 parts, according low and high values on a certain input axis.
    The splitting can continue along other axes.

    The axes can contain float values, categorials (int) or booleans.
    The float axes can have Nans when data are unkown.
    Each category set one bit in an integer. The unknown category is a category
    by itself.
    Booleans that contain unknowns should be coded as categorial.

        f( x:p ) = DTM
                    \left => DTM (or None)
                    \rite => DTM (or None)
                    \dimension
                    \split or \mask

    The tree is searched left to right.

    The parameters are all initialized at 0.0

    Examples
    --------
    >>> dtm = DecisionTreeModel( )
    >>> print( dtm )
    DecisionTree: with 0 components and 1 parameters

    Attributes
    ----------
    left : None or DTM
        a None the tree stops otherwise there is a new split.
    rite : None or DTM
        a None the tree stops otherwise there is a new split.
    dimension : int
        split according to data values on this axes
    itype : char. Either 'f' (float), 'i' (integer), or 'b' (boolean)
        characterizes the input dimension as float, integer or boolean
    split : float between 0 and 1 (for float dimension)
        to the left normalized values < split; to the rite normvalues > split.
        Unknown values (NaNs to to the smallest faction).
    nsplit : int
        number of calls to random.rand() to be averaged. Prior on "split"
    mask : float between 0 and 1 (for float dimension)
        to the left normalized values < split; to the rite normvalues > split.
        Unknown values (NaNs to to the smallest faction.

    Attributes from Modifiable
    --------------------------
        modifiable

    Attributes from Dynamic
    -----------------------
        dynamic

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    """

    NSPLITPRIOR = 3


    def __init__( self, ndim=1, depth=0, split=0.5, kdim=0, itypes=[0], modifiable=True,
                        dynamic=True, code=None, growPrior=None, copy=None, **kwargs ):
        """
        DecisionTree model.

        The DTM standardly has a UniformPrior for all parameters, with limits [0,1]

        Parameters
        ----------
        ndim : int
            number of input dimensions
        depth : int
            depth of the tree
        kdim : None or list of ints
            input channel to be splitted.
        itypes : [list of] int
            indicating the type of input: 0 for float, 1 for boolean, >1 for categorial
            The last number is repeated for remaining inputs
        split : None or float or list of floats
            fraction (0<s<1) of the input kdim that falls on either side.
        growPrior : None or Prior
            Governing the growth
        modifiable : bool (True)
            Will the model modify dimension and/or split/mask
        dynamic : bool (True)
            Will the model grow/shrink

        """

        Modifiable.__init__( self, modifiable=modifiable )
        Dynamic.__init__( self, dynamic=dynamic )

        if depth == 0 or code is not None :
            nparams = 1
            setatt( self, "left", None )
            setatt( self, "rite", None )
            setatt( self, "split", None )
            setatt( self, "parent", None )

        else :
            d = depth - 1
            setatt( self, "dimension", kdim[0] )
            itype = Tools.getItem( itypes, self.dimension )

            klen = Tools.length( kdim )
            if not isinstance( split, list ) : split = [split]
            for k in range(  Tools.length( split ), klen ) :
                split += [Tools.getItem( split, k )]

            self.setSplitOrMask( itype, split[0] )

            kd1 = kdim[1:]
            sp1 = split[1:]
            left = DecisionTreeModel( ndim=ndim, depth=d, kdim=kd1, split=sp1,
                                      itypes=itypes, **kwargs )
            setatt( self, "left", left )
            setatt( self.left, "parent", self )

            ns = ( 0x1 << d ) - 1
            kd2 = kd1[ns:]
            sp2 = sp1[ns:]
            rite = DecisionTreeModel( ndim=ndim, depth=d, kdim=kd2, split=sp2,
                                      itypes=itypes, **kwargs )
            setatt( self, "rite", rite )
            setatt( self.rite, "parent", self )
            nparams = self.left.npars + self.rite.npars


        param = [0.0] * nparams

        LinearModel.__init__( self, nparams, ndim=ndim, copy=copy,
                    params=param, **kwargs )

        if copy is None :
            if growPrior is None :
                growPrior = ExponentialPrior( scale=2 )
            setatt( self, "growPrior", growPrior )
            setatt( self, "itypes", itypes )
            setatt( self, "ncomp", ( 0x1 << depth ) - 1 )
#            setatt( self, "nsplit", 3 )
#            self.setLimits( 0, 1 )
            setatt( self, "nsplit", self.NSPLITPRIOR )
            self.setLimits( lowLimits=0.0, highLimits=1.0 )
        else :
            setatt( self, "growPrior", copy.growPrior )
            setatt( self, "ncomp", copy.ncomp )
            setatt( self, "nsplit", copy.nsplit )
            setatt( self, "itypes", copy.itypes )

        gen = self.walk()
        child = next( gen )     # skip root
        while True :
            try :
                child = next( gen )
            except :
                break
            if child.itypes is not None :
                del( child.itypes )
                del( child.priors )

        if code is not None :
            self = self.decode( code, kdim, split, 0 )


    def copy( self ):
        """ Copy method.  """

        dtm = DecisionTreeModel( copy=self, modifiable=self.modifiable )

        if self.dimension is not None :
            setatt( dtm, "dimension", self.dimension )
            if self.split is not None :
                setatt( dtm, "split", self.split )
            else :
                setatt( dtm, "mask", self.mask )

            if hasattr( self, "itypes" ) :
                setatt( dtm, "itypes", self.itypes )

            setatt( dtm, "left", self.left.copy() )
            setatt( dtm.left, "parent", dtm )
            setatt( dtm, "rite", self.rite.copy() )
            setatt( dtm.rite, "parent", dtm )

        return dtm

    def __getattr__( self, name ) :
        """
        Return None when the named attribute has not been set.

        Parameters
        ----------
        name : string
            name of the attribute
        """
        if ( ( name == "split" ) or ( name == "mask" ) or ( name == "itypes" ) or
             ( name == "dimension" ) or ( name == "maxComp" ) or ( name == "minComp" ) or
             ( name == "parent" ) ) :
            return None
        else :
            return super().__getattr__( name )

    def setSplitOrMask( self, itype, split ) :
        """ For internal use only """

        if itype == 0 :         ## float
            setatt( self, "split", split )
        else :                  ## boolean (1) or categorial (>1)
            setatt( self, "mask", int( split * ( 0x1 << itype ) + 1 ) )

    def isLeaf( self ) :
        """
        Return true if self is a leaf
        """
        return self.dimension is None

    def partitionList( self, xdata, plist ) :
        """
        Partition the xdata in plist over 2 new lists according to the DTM-branch.

        Paramaters
        ----------
        xdata : array-like
            the xdata
        plist : array of ints
            indices in xdata

        Return
        ------
        pl1, pl2 : 2 lists
            together containing all indices in plist
        """
        if len( plist ) == 0 :
            return ( [], [] )

        xd = Tools.getColumnData( xdata, self.dimension )[plist]        ## working data

        if self.split is not None :
            mn = numpy.min( xd )
            mx = numpy.max( xd )

            split = mn + ( mx - mn ) * self.split
            ### add NAN values to the smallest fraction
            cmp = xd > split if self.split < 0.5 else numpy.logical_not( xd <= split )
        elif self.mask >= 2 :
            cmp = ( xd & self.mask ) != 0
        else :
            cmp = ( xd == self.mask )

        pl1 = plist[numpy.where( cmp )]
        pl2 = plist[numpy.where( numpy.logical_not( cmp ) )]

        return ( pl1, pl2 )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        ndata = Tools.length( xdata )
        plist = numpy.arange( ndata, dtype=int )

#        print( params )
        res = numpy.zeros( ndata, dtype=type( params[0] ) )

        kpar = 0
        if self.isLeaf() :
            return params[0]

        res, kpar = self.recursiveResult( xdata, params, kpar, plist, res )

        return res

    def recursiveResult( self, xdata, params, kpar, plist, res ) :
        """ For internal use only """

        pl1, pl2 = self.partitionList( xdata, plist )

        if self.left.isLeaf() :
            res[pl1] = params[kpar]
            kpar += 1
        else :
            res, kpar = self.left.recursiveResult( xdata, params, kpar, pl1, res )

        if self.rite.isLeaf() :
            res[pl2] = params[kpar]
            kpar += 1
        else :
            res, kpar = self.rite.recursiveResult( xdata, params, kpar, pl2, res )

        return res, kpar

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        ndata = Tools.length( xdata )
        plist = numpy.arange( ndata, dtype=int ) if parlist is None else parlist

        kpar = 0
        if self.isLeaf() :
            return numpy.ones( (ndata,1), dtype=float )

        part = numpy.zeros( (ndata, self.npbase), dtype=float )

        part, kpar = self.recursivePartial( xdata, kpar, plist, part )

        return part

    def recursivePartial( self, xdata, kpar, plist, part ) :
        """ For internal use only """

        pl1, pl2 = self.partitionList( xdata, plist )

        if self.left.isLeaf() :
            part[pl1,kpar] = 1.0
            kpar += 1
        else :
            part, kpar = self.left.recursivePartial( xdata, kpar, pl1, part )

        if self.rite.isLeaf() :
            part[pl2,kpar] = 1.0
            kpar += 1
        else :
            part, kpar = self.rite.recursivePartial( xdata, kpar, pl2, part )

        return part, kpar

    def sortXdata( self, xdata ):
        """
        Reorder the xdata according to the parameter ordering

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials

        """
        ndata = Tools.length( xdata )
        plist = numpy.arange( ndata, dtype=int )

        if self.isLeaf() :
            return plist

        return numpy.asarray( self.recursiveOrder( xdata, plist ), dtype=int )

    def recursiveOrder( self, xdata, plist ) :
        """ For internal use only """

        pl1, pl2 = self.partitionList( xdata, plist )

        if not self.left.isLeaf() :
            pl1 = self.left.recursiveOrder( xdata, pl1 )

        if not self.rite.isLeaf() :
            pl2 = self.rite.recursiveOrder( xdata, pl2 )

        return numpy.append( pl1, pl2 )


    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each xdata (=x).

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        return numpy.zeros( Tools.length( xdata ), dtype=float )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        cl, cb = self.count()
        name = str( "DecisionTree: with %d components and %d parameters" % ( cb, cl ) )
        return name

    def fullName( self, ids=False ):
        """
        Returns a string representation of the model.

        Parameters
        ----------
        ids : bool
            if True give the pointers of the links too.

        """

        name = str( "DecisionTree:" )

        indent = 4
        kpar = 0
        name, kpar = self.recursiveName( name, indent, kpar, ids=ids )
        return name


    def recursiveName( self, name, indent, kpar, ids=False ) :
        """ For internal use only """
        if ids :
            if self.parent is None :
                name += " (%d)" % id( self )
            else :
                name += " (%d %d)" % ( id( self ), id( self.parent ) )

        if self.isLeaf() :
            name += " parameter %d\n" % kpar
            kpar += 1
        else :
            if self.split is not None :
                name += " dim %d split at %.2f\n" % ( self.dimension, self.split )
            else :
                name += " dim %d mask " % ( self.dimension )
                name += "None" if self.mask is None else numpy.binary_repr( self.mask )
                name += "\n"
            sind = " " * indent
            indent += 4
            name += "%sLeft  :" % sind
            name, kpar = self.left.recursiveName( name, indent, kpar, ids=ids )
            name += "%sRight :" % sind
            name, kpar = self.rite.recursiveName( name, indent, kpar, ids=ids )
        return ( name, kpar )


    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        return self.yUnit


    def walk( self ):
        """
        Iterate tree in pre-order depth-first search order

        Found this piece of code on the internet. Fairly obscure.
        """
        yield self
        for child in [self.left, self.rite]:
            if child is not None :
                for chld in child.walk( ):
                    yield chld


    def encode( self ) :
        """
        Make a code tuple to be used by the constructor to resurrect the DTM
        The tuple consists of
        code : list of (list or 1 or 2), encoding the structure of DTM
        dims : list of dimensions at the branches
        splim : list of split/mask values at the branches

        """
        if self.isLeaf() :
            return ( 1, [], [] )

        if self.left.isLeaf() and self.rite.isLeaf() :
            sm = self.split if self.split is not None else self.mask
            return ( 2, [self.dimension], [sm] )

        if self.left.isLeaf() :
            ( c, d, s ) = self.rite.encode()
            sm = self.split if self.split is not None else self.mask
            return ( [1,c], [self.dimension] + d, [sm] + s )

        if self.rite.isLeaf() :
            ( c, d, s ) = self.left.encode()
            sm = self.split if self.split is not None else self.mask
            return ( [c,1], [self.dimension] + d, [sm] + s )

        (c1,d1,s1) = self.left.encode()
        (c2,d2,s2) = self.rite.encode()
        sm = self.split if self.split is not None else self.mask

        return ( [c1,c2], [self.dimension] + d1 + d2, [sm] + s1 + s2 )

    def decode( self, code, kdim, splim, kbr ) :
        """
        Resurrect the DTM from the code generated by encode().
        For internal use in the Constructor.

        Parameters
        ----------
        code : list
            of (list or 1 or 2), encoding the structure of DTM
        dims : list
            of dimensions at the branches
        splim : list
            of split/mask values at the branches
        kbr : int
            counter (start at 0)
        """

        if code == 1 :
            return self, kbr-1

        dtm = self
        if code == 2 :
            setatt( dtm, "left", DecisionTreeModel( ndim=self.ndim, depth=0 ) )
            setatt( dtm, "rite", DecisionTreeModel( ndim=self.ndim, depth=0 ) )
            setatt( dtm, "dimension", kdim[kbr] )
            sname = "mask" if isinstance( splim[kbr], int ) else "split"
            setatt( dtm, sname, splim[kbr] )
            setatt( dtm.left, "parent", dtm )
            setatt( dtm.rite, "parent", dtm )

            return dtm, kbr

        setatt( dtm, "dimension", kdim[kbr] )
        sname = "mask" if isinstance( splim[kbr], int ) else "split"
        setatt( dtm, sname, splim[kbr] )

        left = DecisionTreeModel( ndim=self.ndim, depth=0 )
        left, kbr = left.decode( code[0], kdim, splim, kbr+1 )
        setatt( dtm, "left", left )
        setatt( dtm.left, "parent", dtm )

        rite = DecisionTreeModel( ndim=self.ndim, depth=0 )
        rite, kbr = rite.decode( code[1], kdim, splim, kbr+1 )
        setatt( dtm, "rite", rite )
        setatt( dtm.rite, "parent", dtm )

        return dtm, kbr


    def findLeaf( self, kleaf ) :
        """
        Find a leaf in the tree, returning the leaf.

        Parameter
        ---------
        kleaf : int
            index of the leaf to be found
        """
        kl = -1
        gen = self.walk()
        child = None
        while kl < kleaf :
            child = next( gen )
            if child.isLeaf() :
                kl += 1

        return child

    def findBranch( self, kbranch ) :
        """
        Find a branch in the tree, returning the branch.

        Parameter
        ---------
        kbranch : int
            index of the branch to be found
        """
#        print( self.fullName() )

#        print( "kbr   ", kbranch, self.ncomp, self.npars, self.count() )
        kl = -1
        gen = self.walk()
        child = None
        while kl < kbranch :
#            print( "kl   ", kl )
            child = next( gen )
            if not child.isLeaf() :
                kl += 1

        return child

    def check( self ) :
        """
        Find a branch in the tree, returning the branch.

        Parameter
        ---------
        kbranch : int
            index of the branch to be found
        """
        kbranch = self.countBranch()

        kl = -1
        gen = self.walk()
        child = None
        ok = True
        while kl < kbranch :
            try :
                child = next( gen )
            except :
                break
            if not child.isLeaf() :
                kl += 1
                sp = child.split
                mk = child.mask
                kd = child.dimension
                tp = Tools.getItem( self.itypes, kd )
                if sp is not None :
                    ok = ok and tp == 0 and ( 0 < sp < 1 )
                elif mk is not None :
                    ok = ok and tp > 0 and ( 0 < mk < ( 0x1 << tp + 1 ) )
                else :
                    ok = False

        return ok

    def findRoot( self ) :
        """
        Return the root of the tree.

        """
        root = self
        while root.parent is not None :
            root = root.parent

        return root

    def count( self ) :
        """
        Return number of leafs and branches.
        """
        cleaf = 0
        cbran = 0
        gen = self.walk()
        while True :
            try :
                child = next( gen )
            except :
                break

            if child.isLeaf() :
                cleaf += 1
            else :
                cbran += 1
        return cleaf, cbran

    def countLeaf( self ) :
        """
        Return number of leafs.
        """
        return self.count()[0]

    def countBranch( self ) :
        """
        Return number of leafs.
        """
        return self.count()[1]


    def grow( self, offset=0, rng=None, location=0, split=0.5, kdim=0 ):
        """
        Increase the the number of components by 1 (if allowed by maxComp)

        Parameters
        ----------
        offset : int
            offset in the parameter list (pertaining to earlier models in the chain)
        rng : Random Number Generator
            to obtain random values for items below.
        location : int
            location where the new dtm-leaf should be inserted
        kdim : int (<self.ndim)
            dimension to split
        split : float (0<split<1)
            relative cut on this dimension

        Return
        ------
        bool :  succes

        """
        if not self.isDynamic() :
            return False

        if self.maxComp is not None and self.ncomp >= self.maxComp:
            return False

        if rng is not None :
            location = rng.randint( self.npbase )
            kdim = rng.randint( self.ndim )
            itype = Tools.getItem( self.itypes, kdim )
            split = numpy.mean( rng.rand( self.nsplit ) ) if itype == 0 else rng.rand()
        else :
            itype = Tools.getItem( self.itypes, kdim )

        ## Replace the leaf by a DTM at its parent
        leaf = self.findLeaf( location )
        setatt( leaf, "dimension", kdim )

        leaf.setSplitOrMask( itype, split )

#        print( "GROW   ", kdim, itype, split, leaf.split, leaf.mask )

        setatt( leaf, "left", DecisionTreeModel( ndim=self.ndim, depth=0 ) )
        setatt( leaf.left, "parent", leaf )
        setatt( leaf, "rite", DecisionTreeModel( ndim=self.ndim, depth=0 ) )
        setatt( leaf.rite, "parent", leaf )

        ## count leafs (parameters) and branches (components)
        cleaf, cbran = self.count()
        dnp = cleaf - self.npars

        ## duplicate the parameter
        value = self._head.parameters[offset+location]
        self.alterParameterSize( dnp, offset, location, value=value )

        head = self._head
        mdlpar = head.parameters
        k1 = location + offset
        value = numpy.zeros( dnp, dtype=float )
        if rng is not None :
            for k in range( dnp ) :
                value[k] = head.unit2Domain( rng.rand(), k + k1 )

        mdlpar = self.alterParameters( mdlpar, location, dnp, offset, value=value )

        setatt( self._head, "parameters", mdlpar )

        self.alterParameterNames( dnp )

        setatt( self, "ncomp", cbran )

        return True

    def shrink( self, offset=0, rng=None, location=0 ):
        """
        Decrease the the number of componenets by 1 (if allowed by minComp)
        Remove an arbitrary item.

        Parameters
        ----------
        offset : int
            location where the new params should be inserted

        Return
        ------
        bool : succes

        """
        if self.ncomp < 1 or ( self.minComp is not None and self.ncomp <= self.minComp ):
            return False

        if rng is not None :
            location = rng.randint( self.npbase )

        leaf = self.findLeaf( location )
        parent = leaf.parent
#       npp = parent.countLeaf()

        if parent is None :
            return False


        ## Erase the branch by putting the leafs to None
        setatt( parent, "left", None )
        setatt( parent, "rite", None )
        setatt( parent, "split", None )
        setatt( parent, "dimension", None )

        cleaf, cbran = self.count()
        dnp = cleaf - self.npars
        location = min( location - dnp, self.npars )
        self.alterParameterSize( dnp, offset, location=location )

        head = self._head
        mdlpar = head.parameters

        mdlpar = self.alterParameters( mdlpar, location, dnp, offset )
        setatt( self._head, "parameters", mdlpar )

        self.alterParameterNames( dnp )

        setatt( self, "ncomp", cbran )

        return True

    def vary( self, rng=None, location=0, split=0.5, kdim=0 ):
        """
        Vary the model structure by changing kdim and/or split at location

        Parameters
        ----------
        rng : Random Number Generator
            to obtain random values for items below.
        location : int
            location where the dtm-branch should be changed
        kdim : int (<self.ndim)
            dimension to split
        split : float (0<split<1)
            relative cut on this dimension

        Return
        ------
        bool :  succes

        """
        if self.ncomp < 1 :
            return False

        if rng is not None :
            location = rng.randint( self.ncomp )
            parent = self.findBranch( location )
            if rng.rand() < 0.5 :
                kdim = rng.randint( self.ndim )
            else :
                kdim = parent.dimension

            itype = Tools.getItem( self.itypes, kdim )
            if itype == 0 :
                if parent.split is None :               ## make new split
                    split = numpy.mean( rng.rand( self.nsplit ) )
                else :                                  ## shift nearby
                    split = ( self.nsplit * parent.split + rng.rand() ) / ( self.nsplit + 1 )
                setatt( parent, "split", split )
            elif itype == 1 :                           ## make new mask
                if parent.mask is None :
                    mask = rng.randint( 2 ) + 1
                else :                                  ## exchange bits
                    mask = 2 if parent.mask == 1 else 1
                setatt( parent, "mask", mask )
            else :
                if parent.mask is None :                ## make new mask
                    mask = rng.randint( 0x1 << itype ) + 1
                else :                                  ## change 1 bit
                    kr = rng.randint( itype )
                    mask = parent.mask ^ ( 0x1 << kr )
                setatt( parent, "mask", mask )

        else :
            parent = self.findBranch( location )
            itype = Tools.getItem( self.itypes, kdim )
            parent.setSplitOrMask( itype, split )

        setatt( parent, "dimension", kdim )

        return True



