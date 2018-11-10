#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import sys
import argparse as ap
import re
from matplotlib.lines import Line2D
import matplotlib.patches as patches

def printf(format, *args):
        sys.stdout.write(format % args)

dest = "../figs/"

indir = "../data/bursty-5Hz"

files = [ f for f in os.listdir( indir )
                if os.path.isfile( os.path.join( indir, f ) ) ]

mydata = map( lambda x: os.path.join( indir, x ), files )

apps = [ "cth-st", "hpcg", "lmps-lj", "lmps-snap", "lmps-crack", "miniFE",
                "sparc", "milc" ]

while mydata:

        el = mydata.pop( 0 )

        try:
                config = re.search(r"(([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)Hz_([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)nodes)\.delta", el ).group( 1 )
        except AttributeError:
                continue

        printf( "Generating scaling plot for %s\n", el )

        data = np.genfromtxt( el, names=True, dtype=None,
                        deletechars=set("""~!@#$%^&*()=+~\|]}[{';: /?.>,<"""),
                        autostrip=True, missing_values='-', )

        fig, ax = plt.subplots()
        ax.set_xscale( 'log', basex = 10 )

        for i, a in enumerate( apps ):

                mask = np.isfinite( data[ a ] )
                the_min = min( data[ a ][ mask ] )

                if  not the_min:
                        printf( "Min not found: %s\n", a )
                        continue

                percent = [ ( x - the_min ) / the_min * 100.0
                                for x in data[ a ][ mask ] ]
                plt.plot( data[ "Delta" ][ mask ],
                        percent, 
                        lw = 1,
                        label = a )
        ymin, ymax = plt.ylim()

        plt.legend( loc = 'best' )
        plt.xlabel( "Duration of Error (sec)" )
        plt.ylabel( "Pecent Slowdown" )
        plt.savefig( dest + config + "-apps-delta.pdf" );
        plt.close()
