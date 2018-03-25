#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pylab
import os
import sys

def printf(format, *args):
            sys.stdout.write(format % args)

mypath = ["../data/correctables"]

dest = "../figs/"

while mypath:
        element = mypath.pop( 0 )

#        printf( "considering %s\n", element )

        if( os.path.isdir( element ) ):
                files = [f for f in os.listdir( element )
                                if os.path.isfile( os.path.join( element, f ) ) ]
                dirs = [d for d in os.listdir( element ) 
                                if os.path.isdir( os.path.join( element, d ) ) ]

                dirs = map( lambda x: os.path.join( element, x ), dirs )

                # I am sure Scott is thinking about how this is not very 'pythonic'
                files = filter( lambda x: x.endswith( '.data'), 
                                map( lambda x: os.path.join( element, x ), files ) )

                mypath.extend( dirs );

                if not files:
                        continue

                fprefix = os.path.basename( element )

                printf( "Generating figure for %s noise signature\n", fprefix )

                # For each noise signature, plot all apps

                only_f = map( lambda x: os.path.splitext( x ), 
                                map( lambda x: os.path.basename( x ), files ) )

                labels = [ seq[ 0 ] for seq in only_f ]

                datalist = [ ( np.genfromtxt( filename, autostrip=True ) )
                        for filename in files ]

                fig, ax = plt.subplots()
                ax.set_xscale( 'log', basex=2 )

                for data in datalist:
                        l = labels.pop( 0 )
                        mask = np.isfinite( data[ :,3 ] )
                        per =     abs( ( data[ : , 3 ] - data[ :, 1 ] ) / 
                                        data[ :, 1 ] * 100 )
                        per_min = per - abs( ( data[ : , 2 ] - data[ :, 1 ] ) / 
                                        data[ :, 1 ] * 100 )
                        per_max = abs( ( data[ : , 4 ] - data[ :, 1 ] ) / 
                                        data[ :, 1 ] * 100 ) - per
                        ax.errorbar( data[:,0][ mask ], per[ mask ], label = l,
                                        yerr=[ per_min[ mask ], per_max[ mask] ],
                                        capsize = 5 )

                plt.legend()
                plt.xlabel( "Nodes" )
                plt.ylabel( "Percent Slowdown" )
                plt.savefig( dest + fprefix + '.eps' );
                plt.close()
