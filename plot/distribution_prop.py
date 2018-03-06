#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import sys

def printf(format, *args):
        sys.stdout.write(format % args)

mypath = [ "../data/correctables" ]

dest = "../figs/"

N = 200
bw_values = [ None, 'silverman' ]

while mypath:

        element = mypath.pop( 0 )

        printf( "considering %s\n", element )

        if( os.path.isdir( element ) ):
                files = [ f for f in os.listdir( element )
                                if os.path.isfile( os.path.join( element, f ) ) ]

                dirs = [ d for d in os.listdir( element )
                                if os.path.isdir( os.path.join( element, d ) ) ]

                dirs = map( lambda x: os.path.join( element, x ), dirs )

                # I am sure Scott is thinking about how this is not very 'pythonic'
                files = filter( lambda x: x.endswith( '.dtr'),
                                map( lambda x: os.path.join( element, x ), files ) )

                mypath.extend( dirs );

                if not files:
                        continue

                fprefix = os.path.basename( element )

                printf( "Generating figures for %s noise signature\n", fprefix )

                only_f = map( lambda x: os.path.splitext( x ),
                                map( lambda x: os.path.basename( x ), files ) )

                labels = [ seq[ 0 ] for seq in only_f ]

                for file in files:
                        
                        printf( "\tDistribution info for %s\n", file )

                        this_name = labels.pop( 0 )

                        data = ( np.genfromtxt( file, autostrip=True ) )
                        
                        kurtosis = stats.kurtosis( data[ :, 1 ], fisher = True,
                                        bias = True );
                        skew = stats.skew( data[ :, 1 ], bias = True,
                                        nan_policy = 'omit' )

                        sorted = np.sort( data[ :, 1 ] )
                        cdf = np.arange( len( sorted ) ) / float( len( sorted ) )

                        kde = [ stats.gaussian_kde( data[ :, 1 ], bw_method = bw )
                                        for bw in bw_values ]

                        fig, ax = plt.subplots()
                        ax.set_yscale( 'log' )
                        ax.set_ylim( [ 1*10**2, 1*10**8 ] )
                        plt.plot( data[ :, 0 ] * 1.0e-9,
                                        data[ :, 1 ],
                                        label = 'detour', lw = 1 )
                        plt.xlabel( "Timestamp (sec)" )
                        plt.ylabel( "Detour (ns)" )
                        plt.savefig( dest + this_name + '_' + fprefix +
                                        '_dtr.eps' )
                        plt.close()

                        fig, ax = plt.subplots()

                        ax.set_yscale( 'log' )

                        #p, x = np.histogram( delta, bins = ( len( delta ) / N ),
                        #                normed = True )
                        #x = x[ : -1 ] + ( x[ 1 ] - x[ 0 ] ) / 2   # convert bin edges to centers
                        #ax.step( x, p )

                        plt.hist( data[ :, 1 ], N, normed=1, facecolor='blue',
                                        alpha=0.5 )

                        range = np.linspace( min( data[ :, 1 ] ), max( data[ :, 1] ),
                                        N )

                        for i, bw in enumerate( bw_values ):
                                plt.plot( range, kde[ i ]( range ), lw = 1,
                                                label = 'bw = ' + str( bw ) )

                        printf( "\t\t%s kurtosis: %g, skew: %g\n", this_name,
                                        kurtosis, skew )

                        plt.text( 0.6, 0.75,
                                        "kurtosis = " + '{:.2}'.format( kurtosis ) + 
                                        "\nskew = " + '{:.2}'.format( skew ),
                                        horizontalalignment = 'left',
                                        verticalalignment = 'center',
                                        transform = ax.transAxes,
                                        bbox = dict( facecolor = 'white', 
                                                alpha = 0.5 ),
                                        fontsize = 10 
                        )

                        plt.legend( loc = 'best' )
                        plt.xlabel( "Detour (ns)" )
                        plt.ylabel( "Probability ($P(x = X)$)" )
                        plt.savefig( dest + this_name + '_' + fprefix +
                                        '_pdf.eps' )
                        plt.close()

                        fig, ax = plt.subplots()

                        plt.plot( sorted, cdf, label = '$CDF( x )$', lw = 1 )
                        plt.legend( loc = 'best' )
                        plt.xlabel( "Detour (ns)" )
                        plt.ylabel( 'Cummulative Probability ($P(x \leq X)$)' )
                        plt.savefig( dest + this_name + '_' + fprefix +
                                        '_cdf.eps' )
                        plt.close()
                        

