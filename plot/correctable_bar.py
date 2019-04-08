#!/usr/bin/env python

import re
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import sys
import random
import matplotlib.cm as cm
from collections import defaultdict

root_data_dir = "../data/configs"
dst = "../figs"

configs = {}
# EXAMPLE : workloads[ <name> ] = ( <mtbf>, <nodes> )
configs[ "Cielo" ] = ( 333, 8192 )
configs[ "Trinity" ] = ( 86.5, 16384 )
configs[ "Summit" ] = ( 17.3, 4096 )
configs[ "Exascale_Cielo" ] = ( 15.4, 16384 )
configs[ "Exascale_Cielo10" ] = ( 1.54, 16384 )
configs[ "Exascale_Facebook" ] = ( 0.12, 16384 )

for ( sys_name, ( mtbf, process_count ) ) in sorted( configs.items() ):
        data = np.genfromtxt( root_data_dir + "/" + sys_name + "_" + str( mtbf ) +
                        "MTBF_" + str( process_count ) + "nodes.delta",  
                        names = True, dtype = None, encoding = 'ascii',
                        deletechars= '~!@#$%^&*()=+~\|]}[{;: /?>,<' )
        
        deltas = [ 0.15, 775, 133000 ]
        delta_labels = [ "Hardware (No Logging)", "Software Logging",
                         "Firmware Logging" ]
        labels = data[ "App" ]
        
        slowdowns = {}
        bar_slow = defaultdict( list )

        for d in deltas:
                slowdowns[ d ] = ( ( data[ str( d ) ] - data[ "0" ] ) / 
                                     data[ "0" ] ) * 100

        for i, a in enumerate( labels ):
                for j, d in enumerate( deltas ):
                        bar_slow[ a ].append( slowdowns[ d ][ i ] )

        bar_width = 0.8

        # bar positions
        r1 = range( 0, len( deltas) * len( labels ), len( labels ) )
        r2 = [ x + bar_width for x in r1 ]
        r3 = [ x + bar_width for x in r2 ]
        r4 = [ x + bar_width for x in r3 ]
        r5 = [ x + bar_width for x in r4 ]
        r6 = [ x + bar_width for x in r5 ]
        r7 = [ x + bar_width for x in r6 ]
        r8 = [ x + bar_width for x in r7 ]
        r9 = [ x + bar_width for x in r8 ]
        r = [ r1, r2, r3, r4, r5, r6, r7, r8, r9 ]

        fig, ax = plt.subplots()
#        plt.yscale( 'log', basey = 10 )

        if "Exascale" not in sys_name:  
                plt.ylim( top = 10, bottom = -0.1 )
        else:
                plt.yscale( 'log', basey = 10 )
                plt.ylim( top = 2000, bottom = 0.01 )


        for i, l in enumerate( labels ):
                plt.bar( r[ i ], bar_slow[ l ], label = l, 
                         edgecolor = 'white', bottom = -0.1 )

        plt.xlabel( 'Logging Mechanism', fontweight = 'bold' ) 
        plt.ylabel( 'Percent Slowdown', fontweight = 'bold' ) 
        plt.xticks( [ t + ( bar_width * len( labels ) / 2 ) - ( bar_width / 2 ) for t in r1 ],
                    delta_labels )
        plt.legend( loc = 'best' )
        plt.savefig( dst + '/' + sys_name + '_' + str( mtbf ) + 'MTBF_' +
                                str( process_count ) + 'nodes.png' )
        plt.close()
