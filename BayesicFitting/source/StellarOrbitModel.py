import numpy as numpy
from astropy import units
import math

from . import Tools
from .Tools import setAttribute as setatt
from .NonLinearModel import NonLinearModel
from .Kepplers2ndLaw import Kepplers2ndLaw

## import matplotlib.pyplot as plt

__author__ = "Do Kester"
__year__ = 2026
__license__ = "GPL3"
__version__ = "3.3.0"
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
#  *    2018 - 2026 Do Kester

class StellarOrbitModel( NonLinearModel ):
    """
    Model for the radial velocity variations of a star caused by a orbiting planet.
.
     The algorithm was taken from [Boule](../references.md#boule)
        Cory Boule etal. (2017) J. of Double Star Observations Vol 13 p.189.
        http://www.jdso.org/volume13/number2/Harfenist_189-199.pdf

    | par |symbol | description                        | limits  | comment |
    |-----|-------|------------------------------------|---------|---------|
    | p_0 |   e   | eccentricity of the elliptic orbit | 0<e<1   | 0 = circular orbit |
    | p_1 |   a   | semi major axis                    |   a>0   |                      |
    | p_2 |   P   | period of the orbit                |   P>0   |                      |
    | p_3 |   T   | phase since periastron passage     |0<T<2&pi;|                      |
    | p_4 |   i   | inclination of the orbit wrt sky   |0<i<&pi; | 0 = pi = in sky plane|
    | p_5 |&Omega;| position angle from North          |         |                      |
    |     |       |     to the line of nodes         |0<&Omega;<&pi;| 0 = north         |
    | p_6 |&omega;| longitude from the node (in p_5) |              |                   |
    |     |       |     to the periastron         |0<&omega;<2&pi;| 0 = periastron in node|

    Due to the fact that the orbit can be mirrored in the sky plane, one of p_5 or p_6
    has to be limited to [0,pi] and the other to [0,2pi]. However it could be preferred to
    keep the inclination between [0,pi] as it keeps the ascending node at the same place.
    All parameter from 3 on, are cyclic and would profit from a circular prior. 

    The parameters are initialized at [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0].
    It is a non-linear model.

    This class uses @Kepplers2ndLaw to find the radius and anomaly.

    Attributes
    ----------
    keppler : Kepplers2ndLaw()
        to calculate the radius and true anomaly
    ndout : int
        The number of outputs is 2. Use @MultipleOutputProblem.
    spherical : bool
        if True return the results in spherical coordinates, as [rho,phi]
        otherwise return euclidian coordinates [x,y]
        Angles are measured counterclockwise from north to east
        North is Down (-y) and East is to the Right (+x)
    cyclic : { 1 : 2*pi }
        Only if spherical, indicating that result[:,1] is cyclic.
    toRect : Tools.toRect
        Return (x,y) coordinates from (rho,phi). See @Tools#toRect
    toSpher : Tools.toSpher
        Return (rho,phi) coordinates from (x,y). See @Tools#toSpher

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Examples
    --------
    >>> sm = StellarOrbitModel( )
    >>> print( sm.npars )
    >>> 7


    """
    def __init__( self, copy=None, spherical=True, **kwargs ):
        """
        Radial velocity model.

        Number of parameters is 5:

        Parameters
        ----------
        copy : StellarOrbitModel
            model to copy
        spherical : bool (True)
            produce output in sperical coordinates (rho,phi)
            otherwise in rectilinear coordinates (x,y)
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]
        names = ["eccentricity", "semimajoraxis", "period", "phase since periastron",
                  "inclination", "north2nodes", "nodes2periastron"]

        setatt( self, "ndout", 2 )
        setatt( self, "spherical", spherical )

        super( StellarOrbitModel, self ).__init__( 7, copy=copy, params=param,
                        names=names, **kwargs )

        setatt( self, "keppler", Kepplers2ndLaw() )

        setatt( self, "toRect", Tools.toRect )
        setatt( self, "toSpher", Tools.toSpher )

        if spherical :
            setatt( self, "cyclic", {1:2*math.pi} )

    def copy( self, spherical=None ):
        """ 
        Copy method.  
    
        Parameters
        ----------
        spherical : None or bool
            return spherical (True) or rectangular (False) coordinates

        """
        if spherical is None :
            spherical = self.spherical

        return StellarOrbitModel( spherical=spherical, copy=self )

    def baseResult( self, xdata, params ):
        """
        Returns
        ------- 
        the result of the model function as a 2-d array containing 
        [rho,phi] when spherical is true else [x,y]

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        The parameters are explained in the @#StellarOrbitModel constructor.

        """
        xr, yp = self.getOrbit( xdata, params )
        
        result = numpy.zeros( ( len( xdata ), 2 ), dtype=float )
        result[:,0] = xr       ## distance
        result[:,1] = yp       ## positional angle from north counterclock

        return result


    def getOrbit( self, xdata, params, d3=False ) :
        """
        Calculate the 2 (or 3)-dim result of the model function as a tuple of arrays 

        The pertaining rho, phi, (theta) are available from self.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.
        d3 : bool (False)
            return 3 dim result if true else 2 dim

        The parameters are explained in the @#StellarOrbitModel constructor.

        Returns
        ------- 
        x, y(, z) : tuple of arrays
            containing the rectangular coordinates
        """

        inclin = params[4]
        ascpos = params[5]
        asclon = params[6]

        ## rho = distance between stars
        if math.isnan( params[0] ) :
            from .Formatter import fma
            print( "pars   ", fma( params ) )

        ( rho, v ) = self.keppler.radiusAndTrueAnomaly( xdata, params[:4] )

        ## add the longitude (along the orbit) from the ascending node to the periastron
        vp = v + asclon

        ## project on the xy plane 
        svp = numpy.sin( vp )
        svi = svp * math.cos( inclin )
        cvp = numpy.cos( vp )

        ## phi = angle on sky (xy-plane) of stars wrt each other
        ## add angle (in xy plane) from north to ascending node
        phi = numpy.arctan2( svi, cvp ) + ascpos
        rxy = rho * numpy.sqrt( svi * svi + cvp * cvp )

        if not d3 :
            return ( ( rxy, phi ) if self.spherical else 
                     Tools.toRect( rxy, phi ) )
        
        x, y = Tools.toRect( rxy, phi )
        z = rho * svp * math.sin( inclin )

        return ( x, y, z )

    def baseDerivative( self, xdata, params, d3=False ):
        """
        Returns the derivative [df1/dt, df2/dt] of the model function.
        Where f1 = rho if spherical else x
              f2 = phi if spherical else y
        and t is time, input data, here aliased to 'xdata' 

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.
        d3 : boolean
            when True also return df3/dt in the array
            f3 is theta if spherical else z 

        The parameters are explained in the @#StellarOrbitModel constructor.

        """
        inclin = params[4]
        ascpos = params[5]
        asclon = params[6]

        dfdt = numpy.zeros( ( len( xdata ), 2 ), dtype=float )

        p = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, p )

        cosE = self.keppler.cosE
        cosE = numpy.where( cosE == -1, -0.99999, cosE )
        sinE = self.keppler.sinE
        drdt, dvdt = self.keppler.drvdx( xdata, p, cosE, sinE )

        vp = v + asclon
        svp = numpy.sin( vp )
        cvp = numpy.cos( vp )
        ci = math.cos( inclin )
        svp2 = svp * svp
        cvp2 = cvp * cvp
        ci2 = ci * ci

        ## phi = angle on sky of stars wrt each other
        phi = numpy.arctan2( svp * ci, cvp ) + ascpos
        dFdv = ci * ( svp2 + cvp2 ) / ( ci2 * svp2 + cvp2 )
        dFdt = dFdv * dvdt

        ## rho = distance between stars
        ssc = numpy.sqrt( svp2 * ci2 + cvp2 )
        rho = r * ssc
        dRdr = ssc
        dRdv = r / ssc * ( svp * cvp * ( ci2 - 1 ) )
        dRdt = dRdr * drdt + dRdv * dvdt

        if self.spherical :
            dfdt[:,0] = dRdt
            dfdt[:,1] = dFdt
        else :
            cf = numpy.cos( phi )
            sf = numpy.sin( phi )
            dfdt[:,0] = +sf * dRdt + rho * cf * dFdt
            dfdt[:,1] = -cf * dRdt + rho * sf * dFdt

        if not d3 :
            return dfdt

        ## theta is angle between z-axis and star 2
        ## theta = numpy.arccos( svp * math.sin( inclin ) )

        ## if not spherical:
        ## z = r * svp * math.sin( inclin )

        si = math.sin( inclin )

        if self.spherical :
            ## coordinate_0 is now r, not rho (= r projected on the sky)
            dfdt[:,0] = drdt 
            dTdv =  -( si * cvp ) / numpy.sqrt( 1 - si * si * svp2 )
            dTdt = dTdv * dvdt
            dfdt = numpy.append( dfdt, dTdt.reshape( (-1,1) ), 1 )
        else :
            dzdt = svp * si * drdt + r * si * cvp * dvdt
#            dTdt = numpy.cos( theta ) * drdt - numpy.sin( theta ) * dTdt
            dfdt = numpy.append( dfdt, dzdt.reshape( (-1,1) ), 1 )

        return dfdt


    def basePartial( self, xdata, params, parlist=None, d3=False ) :
        """
        Returns the partials at the xdata value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters. (not used for linear models)
        parlist : array_like
            list of indices active parameters (or None for all)
        d3 : bool
            if True also return derivatives of theta cq z

        The parameters are explained in the @#StellarOrbitModel constructor.

        """
        inclin = params[4]
        ascpos = params[5]
        asclon = params[6]

        p = params[:4]
        r, v = self.keppler.radiusAndTrueAnomaly( xdata, p )

        cosE = self.keppler.cosE
        cosE = numpy.where( cosE == -1, -0.99999, cosE )
        sinE = self.keppler.sinE
        E = self.keppler.eccAnomaly

        ## dr.., dv.. derivatives of r and v to each op the parameters
        ##   e : eccentricity, a : semimajor axis, P : period, and p : phase
        drde, drda, drdP, drdp, dvde, dvdP, dvdp = self.keppler.drvdpar( xdata, p,
                                                   E, cosE, sinE )

        #######################################################
        ##  2-D parts                                        ##
        #######################################################

        vp = v + asclon
        svp = numpy.sin( vp )
        cvp = numpy.cos( vp )
        ci = math.cos( inclin )
        si = math.sin( inclin )
        svp2 = svp * svp
        cvp2 = cvp * cvp
        ci2 = ci * ci

        ## phi = angle on sky of stars wrt each other
        ## dF.. derivative to phi
        phi = numpy.arctan2( svp * ci, cvp ) + ascpos
        dFdv = ci * ( svp2 + cvp2 ) / ( ci2 * svp2 + cvp2 )

        ## rho = distance between stars
        ssc = numpy.sqrt( svp2 * ci2 + cvp2 )
        rho = r * ssc
        dRdr = ssc
        dRdv = r * ( ci2 - 1 ) * svp * cvp / ssc


        part0 = { 0 : ( lambda: dRdr * drde + dRdv * dvde ),
                  1 : ( lambda: dRdr * drda ),
                  2 : ( lambda: dRdr * drdP + dRdv * dvdP ),
                  3 : ( lambda: dRdr * drdp + dRdv * dvdp ),
                  4 : ( lambda: -r / ssc * svp2 * ci * si ),
                  5 : ( lambda: 0 ),
                  6 : ( lambda: dRdv ) }

        part1 = { 0 : ( lambda: dFdv * dvde ),
                  1 : ( lambda: 0 ),
                  2 : ( lambda: dFdv * dvdP ),
                  3 : ( lambda: dFdv * dvdp ),
                  4 : ( lambda: -cvp * svp * si / ( cvp2 + svp2 * ci2 ) ),
                  5 : ( lambda: 1 ),
                  6 : ( lambda: dFdv ) }

        if self.spherical :
            rhorx = lambda p0, p1 : p0()
            phory = lambda p0, p1 : p1()

        else :
            ct = numpy.cos( phi )
            st = numpy.sin( phi )
            rst = rho * st
            rct = rho * ct
            ct *= -1

            rhorx = lambda p0, p1 : st * p0() + rct * p1()
            phory = lambda p0, p1 : ct * p0() + rst * p1()

        if parlist is None :
            parlist = range( self.npmax )

        npl = len( parlist )
        partial0 = numpy.zeros( ( Tools.length( xdata ), npl ), dtype=float )
        partial1 = numpy.zeros( ( Tools.length( xdata ), npl ), dtype=float )

        for k,kp in enumerate( parlist ) :
            partial0[:,k] = rhorx( part0[kp], part1[kp] )
            partial1[:,k] = phory( part0[kp], part1[kp] )

        if not d3 :
            return ( partial0, partial1 )


        #######################################################
        ##  3-D parts                                        ##
        #######################################################


        si = math.sin( inclin )
        partial2 = numpy.zeros( ( Tools.length( xdata ), npl ), dtype=float )

        if self.spherical :

            ## r is just the distance to star 2 (unprojected)
            ## phi si the same as above

            ## theta is angle between z-axis and star 2
            ## theta = numpy.arccos( svp * math.sin( inclin ) )
            ## dTdp = -cvp * sin( inclin)  / sqrt( 1 - svp^2 * sin^2( inclin ) ) 

            si2 = si * si
            sss = numpy.sqrt( 1 - svp2 * si2 )
            dTdv =  -( si * cvp ) / sss

            part0 = { 0 : ( lambda: drde ),
                      1 : ( lambda: drda ),
                      2 : ( lambda: drdP ),
                      3 : ( lambda: drdp ),
                      4 : ( lambda: 0 ),
                      5 : ( lambda: 0 ),
                      6 : ( lambda: 0 ) }

            part2 = { 0 : ( lambda: dTdv * dvde ),
                      1 : ( lambda: 0 ),
                      2 : ( lambda: dTdv * dvdP ),
                      3 : ( lambda: dTdv * dvdp ),
                      4 : ( lambda: -svp * ci / sss ),  
                      5 : ( lambda: 0 ),
                      6 : ( lambda: -cvp * si / sss ) }

            for k,kp in enumerate( parlist ) :
                partial0[:,k] = part0[kp]()
                partial2[:,k] = part2[kp]()


        else :

            ## rectangular (x,y,z)
            ## z = r * sin( v - p[6] ) * math.sin( inclin )
            ## dzdp = svp * si * drdp + r * si * cvp * dvdp + r * svp * ci * didp

            svps = svp * si
            cvps = cvp * si * r
            svpc = svp * ci
            part2 = { 0 : ( lambda: svps * drde + cvps * dvde ),
                      1 : ( lambda: svps * drda ),
                      2 : ( lambda: svps * drdP + cvps * dvdP ),
                      3 : ( lambda: svps * drdp + cvps * dvdp ),
                      4 : ( lambda: svpc * r ),
                      5 : ( lambda: 0 ),
                      6 : ( lambda: cvps ) }


#            thorz = lambda p0, p2 : ( ct * p0() - st * p2() )

            for k,kp in enumerate( parlist ) :
                partial2[:,k] = part2[kp]()

        return ( partial0, partial1, partial2 )


    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "StellarOrbit " )

    def baseParameterUnit( self, k ):
        """
        Return the unit of a parameter. (TBC)

        Parameters
        ----------
        k : int
            the kth parameter.

        """

        if k == 0:
            return units.Unit( )
        elif k == 1 :
            return self.yUnit
        elif k == 2 :
            return 1.0 / self.xUnit
        return units.Unit( units.si.rad )

    def convertParameters( self, param, stdevs=None, year=2000 ) :
        """
        Return time of periastron (p_3) in years after year and inclination (p_4), 
            the position angle from North to the line of nodes (p_5) and
            the longitude from line of nodes to periastron (p_6) in degrees

        Parameters
        ----------
        param : array
            parameters to be converted
        stdevs : array
            standard deviations to be converted
        year : float
            return the first periastron passage after year

        Returns
        -------
        converted parameters if stdevs is None
        converted (parameters, stdevs) else 
        """
        r2d = 180 / math.pi

        pp = param.copy()
        pp[3] *= param[2] / ( 2 * math.pi )
        while pp[3] < year :
            pp[3] += pp[2]
        pp[4] *= r2d
        pp[5] *= r2d
        pp[6] *= r2d
        if stdevs is None :
            return pp

        sd = stdevs.copy()
        sd[3] *= param[2] / ( 2 * math.pi )
        sd[4] *= r2d
        sd[5] *= r2d
        sd[6] *= r2d

        return ( pp, sd )


    def plotOrbit( self, par, npoint=361, xdata=None, ydata=None, 
                plot=None, color='k', ls='-' ) :
        """
        Plot the orbit in N points, a forward pointing arrow at T = 0, 
        the line to the periastron and an extended line of nodes. 

        if ydata is present, plot the datapoints. If also xdata is present, 
        plot the connecting lines too.

        Parameters
        ----------
        par :  array
            parameter of the model
        npoint : int
            number of points in the orbit
        xdata : array 
            array of times at which the data are measured
        ydata : 2d array 
            array of [x,y] pairs representing the data
        plot : None or pyplot
            None    make a self standing plot and show it
            pyplot  operate within thid plot; do not show
        color, ls : color and linestyle
            for the plot

        """
        from . import Plotter

        Plotter.plotOrbit( self, par, npoint=npoint, xdata=xdata, ydata=ydata,
                plot=plot, color=color, ls=ls )

