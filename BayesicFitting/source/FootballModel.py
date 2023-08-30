import numpy as numpy
from astropy import units
from .NonLinearModel import NonLinearModel
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2023
__license__ = "GPL3"
__version__ = "3.2.0"
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
#  *    2016 - 2023 Do Kester


class FootballModel( NonLinearModel ):
    """
    More or less complex model for the outcome of football marches.

    The input values are a (nteams,2) list of integers. They represent 
    teams that play a match, the first at home the other away.

    For each team the complexity lists parameters

       name                    limits    default    comment
    0. Number of trials      0 < a         n/a     trials on the goal of the opponent
    1. Defensive strength    0 < b < 1      0      fraction of the trials that is stopped
    2. Midfield strength     0 < c < 2      1      relative strength of the team
    3. Home advantage        0 < d < 2      1      advantage of playing at home
    4. Strategy              0 < e < 2      1      

    Note: Computational runtime errors/warnings occur when (some of) the parameters are at 
          their limits. 

    The default values are chosen such that they dont have effect on the results.
    I.e. a model with complexity=5 and all parameters at the defaults except for 
    "trials", has the same result as a model with complexity 1 with the same "trials"
    value.

    Let p1 denote the parameters of the home team and p2 those of the away team,
    then the equations for calculating the strengths, S1 and S2, are

        S1 = a1 * sqrt( c1 * d1 / c2 ) * ( 1 - b2 ^ ( c1 * d1 / c2 ) )

        S2 = a2 * sqrt( c2 / ( c1 * d1 ) ) * ( 1 - b1 ^ ( c2 / ( c1 * d1 ) )


    Note:
    This is about the game that most of the world calls football.

    Examples
    --------
    >>> fm = FootballModel( 18 ) 
    >>> print( fm.npars )
    90

    Author : Do Kester

    Attributes
    ----------
    nteams : int
        number of teams
    complexity : int
        degree of complexity, default = 5.

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
    PARNAMES = ["trials", "defense", "midfield", "home", "strategy"]

    def __init__( self, nteams, complexity=5, copy=None, **kwargs ):
        """
        Calculate the score of football matches

        The number of parameters is ( nteams * complexity )

        Parameters
        ----------
        nteams : int
            number of teams
        complexity : 1 <= int <= 5
            of the model
        copy : FootballModel
            model to copy
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        if complexity < 1 or complexity > 5 :
            raise ValueError( "Complexity must be between 1 and 5, inclusive." )

        super( ).__init__( complexity * nteams, ndim=2, copy=copy, **kwargs )

        self.ndout = 2
        self.complexity = complexity
        self.nteams = nteams

    def copy( self ):
        """ Copy method.  """
        return FootballModel( self.nteams, complexity=self.complexity, copy=self )

    def getPrior( self, k ) :
        """
        Return the prior of the parameter, indicated by k modulo the complexity

        Parameters
        ---------
        k : int
            parameter number.
        """
        return self.basePrior( k % self.complexity )
        

    def __setattr__( self, name, value ):
        """
        Set attributes: degree
        """
        if name == 'complexity' :
            if value == 5 :
                setatt( self, "goals", self.goals5 )
                setatt( self, "parts", self.part5 )
            elif value == 4 :
                setatt( self, "goals", self.goals4 )
                setatt( self, "parts", self.part4 )
            elif value == 3 :
                setatt( self, "goals", self.goals3 )
                setatt( self, "parts", self.part3 )
            elif value == 2 :
                setatt( self, "goals", self.goals2 )
                setatt( self, "parts", self.part2 )
            elif value == 1 :
                setatt( self, "goals", self.goals1 )
                setatt( self, "parts", self.part1 )
            else :
                raise ValueError( "Complexity must be between 1 and 5, inclusive" )

            setatt( self, name, value, type=int )

        elif name == 'nteams' :
            setatt( self, name, value, type=int )
        elif name == 'ndout' :
            setatt( self, name, value, type=int )
        else :
            super( ).__setattr__( name, value )


    def goals1( self, xdata, par ) :
        """ attack """
        return numpy.asarray( [par[xdata[:,0]], par[xdata[:,1]]] ).transpose()

    def goals2( self, xdata, par ) :
        """ attack, defense """
        k0 = xdata[:,0] * 2
        k1 = xdata[:,1] * 2
        return numpy.asarray( [par[k0] * ( 1 - par[k1+1] ), 
                               par[k1] * ( 1 - par[k0+1] )] ).transpose()

    def goals3( self, xdata, par ) :
        """ attack, defense, midfield """
        k0 = xdata[:,0] * 3
        k1 = xdata[:,1] * 3
        ma0 = md1 = par[k0+2] / par[k1+2]
        ma1 = md0 = 1 / ma0
#        print( "3 m0  ", fmt( m0 ) )
#        print( "3 m1  ", fmt( m1 ) )

        sc0 = par[k0] * numpy.sqrt( ma0 ) * ( 1 - numpy.power( par[k1+1], md1 ) )
        sc1 = par[k1] * numpy.sqrt( ma1 ) * ( 1 - numpy.power( par[k0+1], md0 ) )
        return numpy.asarray( [sc0, sc1] ).transpose()

    def goals4( self, xdata, par ) :
        """ attack, defense, midfield, home """
        k0 = xdata[:,0] * 4
        k1 = xdata[:,1] * 4
        ma0 = md1 = ( par[k0+2] * par[k0+3] ) / par[k1+2]
        ma1 = md0 = 1 / ma0
#        print( "4 m0  ", fmt( m0 ) )
#        print( "4 m1  ", fmt( m1 ) )

        sc0 = par[k0] * numpy.sqrt( ma0 ) * ( 1 - numpy.power( par[k1+1], md1 ) )
        sc1 = par[k1] * numpy.sqrt( ma1 ) * ( 1 - numpy.power( par[k0+1], md0 ) )
        return numpy.asarray( [sc0, sc1] ).transpose()

    def goals5( self, xdata, par ) :
        """
        attack, defense, midfield, home, strategy 

        """
        k0 = xdata[:,0] * 5
        k1 = xdata[:,1] * 5

        m0 = ( par[k0+2] * par[k0+3] ) / par[k1+2]
        m1 = 1 / m0
        ma0 = m0 * par[k0+4]
        md0 = m1 * par[k0+4]
        ma1 = m1 * par[k1+4]
        md1 = m0 * par[k1+4]

#        print( "5 m0  ", fmt( m0 ), fmt( ma0 ), fmt( md0 ) )
#        print( "5 m1  ", fmt( m1 ), fmt( ma1 ), fmt( md1 ) )

        sc0 = par[k0] * numpy.sqrt( ma0 ) * ( 1 - numpy.power( par[k1+1], md1 ) )
        sc1 = par[k1] * numpy.sqrt( ma1 ) * ( 1 - numpy.power( par[k0+1], md0 ) )
        return numpy.asarray( [sc0, sc1] ).transpose()


    def baseResult( self, xdata, params ):
        """
        Returns the partials at the input value.

        The partials are the powers of x ( xdata ) from 0 to degree.

        Parameters
        ----------
        xdata : array_like [2:nteams]
            list of team ids playing against each other.
        params : array_like
            parameters for the model 

        """
        return self.goals( xdata, params )



    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        The partials are the powers of x ( xdata ) from 0 to degree.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters for the model (ignored for LinearModels).
        parlist : array_like
            list of indices of active parameters

        to a1
        (1-b_2^((c_1*d_1)/(c_2*f_2)))*sqrt((c_1*d_1)/c_2)
        to b2
        -(a_1*c_1*d_1*sqrt((c_1*d_1)/c_2)*b_2^((c_1*d_1)/(c_2*f_2)-1))/(c_2*f_2)
        to c1
        -(a_1*d_1*(2*b_2^((d_1*c_1)/(c_2*f_2))*log(b_2)*d_1*c_1+(b_2^((d_1*c_1)/(c_2*f_2))-1)
            *c_2*f_2))/(2*c_2^2*f_2*sqrt((d_1*c_1)/c_2))
        to c2
        (a_1*c_1*d_1*((b_2^((c_1*d_1)/(f_2*c_2))-1)*f_2*c_2+2*b_2^((c_1*d_1)/(f_2*c_2))*
            log(b_2)*c_1*d_1))/(2*f_2*sqrt((c_1*d_1)/c_2)*c_2^3)
        to d1
        -(a_1*c_1*(2*b_2^((c_1*d_1)/(c_2*f_2))*log(b_2)*c_1*d_1+(b_2^((c_1*d_1)/(c_2*f_2))-1)*
            c_2*f_2))/(2*c_2^2*f_2*sqrt((c_1*d_1)/c_2))
        to f2
        (a_1*b_2^((c_1*d_1)/(c_2*f_2))*log(b_2)*c_1*d_1*sqrt((c_1*d_1)/c_2))/(c_2*f_2^2)
        """
        return self.parts( xdata, params )



    def part1( self, xdata, par ) :
        k0 = xdata[:,0]
        k1 = xdata[:,1]
        lenk = len( k0 )
        kr = range( lenk )
        phome = numpy.zeros( (lenk, self.npbase), dtype=float )
        paway = numpy.zeros( (lenk, self.npbase), dtype=float )

        phome[kr,k0] = 1.0
        paway[kr,k1] = 1.0
        return [phome,paway]    
    
    def part2( self, xdata, par ) :
        k0 = xdata[:,0] * 2
        k1 = xdata[:,1] * 2
        lenk = len( k0 )
        kr = range( lenk )
        phome = numpy.zeros( (lenk, self.npbase), dtype=float )
        paway = numpy.zeros( (lenk, self.npbase), dtype=float )

        phome[kr,k0] = 1.0 - par[k1+1]  
        paway[kr,k1] = 1.0 - par[k0+1]

        phome[kr,k1+1] = -par[k0]
        paway[kr,k0+1] = -par[k1]

        return [phome,paway]    

    def part3( self, xdata, par ) :
        k0 = xdata[:,0] * 3
        k1 = xdata[:,1] * 3
        lenk = len( k0 )
        kr = range( lenk )
        phome = numpy.zeros( (lenk, self.npbase), dtype=float )
        paway = numpy.zeros( (lenk, self.npbase), dtype=float )

        a0 = par[k0]
        a1 = par[k1]
        b0 = par[k0+1]
        b1 = par[k1+1]
        c0 = par[k0+2]
        c1 = par[k1+2]

        m0 = c0 / c1
        m1 = 1 / m0
        sm0 = numpy.sqrt( m0 )
        sm1 = numpy.sqrt( m1 )
        pp0 = numpy.power( b0, m1 )
        pp1 = numpy.power( b1, m0 )
        lb0 = numpy.log( b0 )
        lb1 = numpy.log( b1 )
        pc0 = ( pp0 - 1 ) * c0
        pc1 = ( pp1 - 1 ) * c1
        pl0 = 2 * pp0 * lb0 * c1
        pl1 = 2 * pp1 * lb1 * c0
        sc0 = 2 * sm0 * c1 * c1
        sc1 = 2 * sm1 * c0 * c0

        phome[kr,k0] += sm0 * ( 1 - pp1 )                        # df0/da0
        paway[kr,k1] += sm1 * ( 1 - pp0 )                        # df1/da1
        # df0/da1 = df1/da0 = 0 

        phome[kr,k1+1] += -a0 * sm0 * m0 * pp1 / b1              # df0/db1
        paway[kr,k0+1] += -a1 * sm1 * m1 * pp0 / b0              # df1/db0
        # df0/db0 = df1/db1 = 0 

        apps0 = a0 * ( pc1 + pl1 ) / sc0
        apps1 = a1 * ( pc0 + pl0 ) / sc1

        phome[kr,k0+2] += -apps0                                 # df0/dc0
        phome[kr,k1+2] +=  apps0 * m0                            # df0/dc1
        paway[kr,k1+2] += -apps1                                # df1/dc1
        paway[kr,k0+2] +=  apps1 * m1                            # df1/dc0

        return [phome,paway]    

    def part4( self, xdata, par ) :
        k0 = xdata[:,0] * 4
        k1 = xdata[:,1] * 4
        lenk = len( k0 )
        kr = range( lenk )
        phome = numpy.zeros( (lenk, self.npbase), dtype=float )
        paway = numpy.zeros( (lenk, self.npbase), dtype=float )

        a0 = par[k0]
        a1 = par[k1]
        b0 = par[k0+1]
        b1 = par[k1+1]
        c0 = par[k0+2]
        c1 = par[k1+2]
        d0 = par[k0+3]
#        d1 = par[k1+3]

        m0 = c0 * d0 / c1
        m1 = 1 / m0
        sm0 = numpy.sqrt( m0 )
        sm1 = numpy.sqrt( m1 )
        pp0 = numpy.power( b0, m1 )
        pp1 = numpy.power( b1, m0 )
        lb0 = numpy.log( b0 )
        lb1 = numpy.log( b1 )
        pc0 = ( pp0 - 1 ) * c0
        pc1 = ( pp1 - 1 ) * c1
        pl0 = 2 * pp0 * lb0 * c1
        pl1 = 2 * pp1 * lb1 * c0 * d0
        sc0 = 2 * sm0 * c1 * c1
        sc1 = 2 * sm1 * c0 * c0
        d02 = d0 * d0

        phome[kr,k0] = sm0 * ( 1 - pp1 )                        # df0/da0
        paway[kr,k1] = sm1 * ( 1 - pp0 )                        # df1/da1
        # df0/da1 = df1/da0 = 0 

        phome[kr,k1+1] = -a0 * sm0 * m0 * pp1 / b1              # df0/db1
        paway[kr,k0+1] = -a1 * sm1 * m1 * pp0 / b0              # df1/db0
        # df0/db0 = df1/db1 = 0 

        apps0 = a0 * ( pc1 + pl1 ) / sc0
        apps1 = a1 * ( pc0 * d0 + pl0 ) / sc1

        phome[kr,k0+2] = -apps0 * d0                            # df0/dc0
        phome[kr,k1+2] =  apps0 * m0                            # df0/dc1
        paway[kr,k1+2] = -apps1 / d02                           # df1/dc1
        paway[kr,k0+2] =  apps1 * m1 / d0                       # df1/dc0

        phome[kr,k0+3] = -apps0 * c0                             # df0/dd0
        paway[kr,k0+3] =  apps1 * c1 / ( d02 * d0 )              # df1/dd0
        # df0/dd1 = df1/dd1 = 0

        return [phome,paway]    


    def part5( self, xdata, par ) :
        """
        Derivatives copies from https://www.derivative-calculator.net

        Fh = a0*sqrt((d0*f0*c0)/c1) * (1-b1**((d0*f1*c0)/c1))
        Fa = a1*sqrt((c1*f1)/(c0*d0)) * (1-b0**((c1*f0)/(c0*d0)))

        dFh/da0 = (1-b1**((d0*f1*c0)/c1))*sqrt((d0*f0*c0)/c1)
        dFh/da1 = 0
        dFh/db0 = 0
        dFh/db1 = -(a0*c0*d0* sqrt((c0*d0*f0)/c1) *f1* b1**((c0*d0*f1)/c1-1)) / c1
        dFh/dc0 = -(a0*d0*f0*(2*b1**((d0*f1*c0)/c1)*log(b1)*d0*f1*c0+
                    (b1**((d0*f1*c0)/c1)-1)*c1))/(2*c1**2*sqrt((d0*f0*c0)/c1))
        dFh/dc1 = (a0*c0*d0*f0*((b1**((c0*d0*f1)/c1)-1)*c1+2*b1**((c0*d0*f1)/c1)
                   *log(b1)*c0*d0*f1))/(2*sqrt((c0*d0*f0)/c1)*c1**3)
        dFh/dd0 = -(a0*c0*f0*(2*b1**((c0*f1*d0)/c1)*log(b1)*c0*f1*d0+
                    (b1**((c0*f1*d0)/c1)-1)*c1))/(2*c1**2*sqrt((c0*f0*d0)/c1))
        dFh/dd1 = 0
        dFh/df0 = (a0*(1-b1**((c0*d0*f1)/c1))*c0*d0)/(2*c1*sqrt((c0*d0*f0)/c1))
        dFh/df1 = -(a0*b1**((c0*d0*f1)/c1)*log(b1)*c0*d0*sqrt((c0*d0*f0)/c1))/c1

        dFa/da0 = 0
        dFa/da1 = (1-b0**((c1*f0)/(c0*d0)))*sqrt((c1*f1)/(c0*d0))
        dFa/db0 = -(a1*c1*f0*sqrt((c1*f1)/(c0*d0))*b0**((c1*f0)/
                    (c0*d0)-1))/(c0*d0)
        dFa/db1 = 0
        dFa/dc0 = (a1*c1*f1*((b0**((c1*f0)/(d0*c0))-1)*d0*c0+2*
                    b0**((c1*f0)/(d0*c0))*log(b0)*c1*f0))/(2*d0**2*
                    sqrt((c1*f1)/(d0*c0))*c0**3)
        dFa/dc1 = -(a1*f1*(2*b0**((f0*c1)/(c0*d0))*log(b0)*f0*c1+
                    (b0**((f0*c1)/(c0*d0))-1)*c0*d0))/(2*c0**2*d0**2*
                    sqrt((f1*c1)/(c0*d0)))
        dFa/dd0 = (a1*c1*f1*((b0**((c1*f0)/(c0*d0))-1)*c0*d0+2*
                    b0**((c1*f0)/(c0*d0))*log(b0)*c1*f0))/(2*c0**2*
                    sqrt((c1*f1)/(c0*d0))*d0**3)
        dFa/dd1 = 0
        dFa/df0 = -(a1*b0**((c1*f0)/(c0*d0))*log(b0)*c1*
                    sqrt((c1*f1)/(c0*d0)))/(c0*d0)
        dFa/df1 = (a1*(1-b0**((c1*f0)/(c0*d0)))*c1)/(2*c0*d0*
                    sqrt((c1*f1)/(c0*d0)))

        """
        k0 = xdata[:,0] * 5
        k1 = xdata[:,1] * 5
        lenk = len( k0 )
        kr = range( lenk )
        phome = numpy.zeros( (lenk, self.npbase), dtype=float )
        paway = numpy.zeros( (lenk, self.npbase), dtype=float )

        a0 = par[k0]
        a1 = par[k1]
        b0 = par[k0+1]
        b1 = par[k1+1]
        c0 = par[k0+2]
        c1 = par[k1+2]
        d0 = par[k0+3]
#        d1 = par[k1+3]
        f0 = par[k0+4]
        f1 = par[k1+4]


        cd0 = c0 * d0
        ma0 = cd0 * f0 / c1
        ma1 = c1 * f1 / cd0
        sm0 = numpy.sqrt( ma0 )
        sm1 = numpy.sqrt( ma1 )
        md0 = c1 * f0 / cd0
        md1 = cd0 * f1 / c1
        pp0 = numpy.power( b0, md0 )
        pp1 = numpy.power( b1, md1 )
        lb0 = numpy.log( b0 )
        lb1 = numpy.log( b1 )
        pb0 = pp0 - 1
        pb1 = pp1 - 1

        phome[kr,k0] = -sm0 * pb1                                # df0/da0
        paway[kr,k1] = -sm1 * pb0                                # df1/da1
        # df0/da1 = df1/da0 = 0 

        phome[kr,k1+1] = -a0 * sm0 * md1 * pp1 / b1              # df0/db1
        paway[kr,k0+1] = -a1 * sm1 * md0 * pp0 / b0              # df1/db0
        # df0/db0 = df1/db1 = 0 

        phome[kr,k0+2] = -(a0*d0*f0*(2* pp1 * lb1 *cd0*f1 + pb1 *c1))/(2*c1**2* sm0 )  # df0dc0
        phome[kr,k1+2] = (a0*cd0*f0*( pb1 *c1 + 2*pp1 * lb1 *cd0*f1))/(2* sm0 *c1**3)  # df0dc1
        paway[kr,k1+2] = -(a1*f1*(2* pp0 * lb0 * f0*c1 + pb0 *cd0))/(2*cd0**2* sm1 )   # df1dc1
        paway[kr,k0+2] = (a1*c1*f1*(pb0 * cd0 + 2*pp0 * lb0 *c1*f0))/(2*cd0**2* sm1 * c0) # df1dc0

        phome[kr,k0+3] = -(a0*c0*f0*( 2* pp1 * lb1 *cd0*f1 + pb1*c1 )) /( 2*c1**2 * sm0 ) # df0dd0
        paway[kr,k0+3] = (a1*c1*f1*(pb0*cd0 + 2*pp0 * lb0 * c1*f0))/( 2*cd0**2* sm1 * d0) # df1dd0
        # df0/dd1 = df1/dd1 = 0

        phome[kr,k0+4] = -(a0* pb1 * cd0) / ( 2*c1 * sm0 )          # df0df0
        phome[kr,k1+4] = -(a0* pp1 * lb1 * cd0 * sm0 ) / c1         # df0df1
        paway[kr,k1+4] = -(a1* pb0 * c1 ) / ( 2*cd0 * sm1 )         # df1df1
        paway[kr,k0+4] = -(a1* pp0 * lb0 * c1 * sm1 ) / cd0         # df1df0

        return [phome,paway]    


    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each input (=x).

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters for the model.

        """
        raise NotImplementedError( "Impossible. Integer values in xdata." )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return "Foolball"

    def baseParameterName( self, k ):
        """
        Return the name of the indicated parameter.
        Parameters
        ----------
        k : int
            parameter number.

        """
        return "%s_team_%d" % ( self.PARNAMES[k % self.complexity], k / self.complexity )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.

        """
        return units.Unit ( 1 )


