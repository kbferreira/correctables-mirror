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

base =  os.path.join( indir, "5Hz_1.5e-07sec.scale" )

baseline = np.genfromtxt( base, names=True, dtype=None,
                deletechars=set("""~!@#$%^&*()=+~\|]}[{';: /?.>,<"""),
                autostrip=True, missing_values='-', )


while mydata:

        el = mydata.pop( 0 )

        try:
                config = re.search(r"(([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)Hz_([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)sec)\.scale", el ).group( 1 )
        except AttributeError:
                continue

        printf( "Generating scaling plot for %s\n", el )

        data = np.genfromtxt( el, names=True, dtype=None,
                        deletechars=set("""~!@#$%^&*()=+~\|]}[{';: /?.>,<"""),
                        autostrip=True, missing_values='-', )

        fig, ax = plt.subplots()
        ax.set_xscale( 'log', basex = 2 )

        for i, a in enumerate( apps ):
                mask = np.isfinite( baseline[ a ] )
                the_min = min( baseline[ a ][ mask ] )

                mask = np.isfinite( data[ a ] )
                
                if  not the_min:
                        printf( "Min not found: %s\n", a )
                        continue
                percent = [ ( x - the_min ) / the_min * 100.0
                                for x in data[ a ][ mask ] ]
                plt.plot( data[ "Nodes" ][ mask ],
                        percent, 
                        lw = 1,
                        label = a )
        ymin, ymax = plt.ylim()
        plt.ylim( ymax = 100 )

        plt.legend( loc = 'best' )
        plt.xlabel( "Nodes" )
        plt.ylabel( "Pecent Slowdown" )
        plt.savefig( dest + config + "-apps-scale.pdf" );
        plt.close()
