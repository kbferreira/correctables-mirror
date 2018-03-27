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

HW_lower = 90e-9
HW_upper = 110e-9

OS_lower = 700e-6
OS_upper = 780e-6

FW_lower = 130e-3
FW_upper = 0.5

dest = "../figs/"

indir = "../data/correctables/delta"
files = [ f for f in os.listdir( indir )
                if os.path.isfile( os.path.join( indir, f ) ) ]

mydata = map( lambda x: os.path.join( indir, x ), files )

apps = [ "cth-st", "hpcg", "lmps-lj", "lmps-snap", "sparc" ]
micro = [ "allreduce", "reduce", "broadcast", "stencil_27pt" ]

while mydata:

        el = mydata.pop( 0 )

        try:
                config = re.search(r"(([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)_(\d+))\.delta", el ).group( 1 )
        except AttributeError:
                printf( "Cannot find match ...\n" );
                exit( 1 )

        printf( "Generating delta plot for %s\n", el )

        data = np.genfromtxt( el, names=True, dtype=None,
                        deletechars=set("""~!@#$%^&*()=+~\|]}[{';: /?.>,<"""),
                        autostrip=True, missing_values='-', )

        fig, ax = plt.subplots()
        ax.set_xscale( 'log', basex = 10 )

        for i, a in enumerate( apps ):
                mask = np.isfinite( data[ a ] )
                the_min = min( data[ a ][ mask ] )
                if  not the_min:
                        continue
                percent = [ ( x - the_min ) / the_min * 100.0
                                for x in data[ a ][ mask ] ]
                plt.plot( data[ "Delta" ][ mask ],
                        percent, 
                        lw = 1,
                        label = a )
        ymin, ymax = plt.ylim()
        for p in [
                        patches.Rectangle(
                                ( HW_lower, ymin ), HW_upper - HW_lower,
                                  ymax - ymin, 
                                  linestyle='dotted',
                                  alpha=0.3,
                                  edgecolor = "#000000",
                                  facecolor = "#000000",
                        ),
                        patches.Rectangle(
                                ( OS_lower, ymin ), OS_upper - OS_lower,
                                  ymax - ymin, 
                                  linestyle='dotted',
                                  alpha=0.3,
                                  edgecolor = "#000000",
                                  facecolor = "#000000",
                        ),
                        patches.Rectangle(
                                ( FW_lower, ymin ), FW_upper - FW_lower,
                                  ymax - ymin, 
                                  linestyle='dotted',
                                  alpha=0.3,
                                  edgecolor = "#000000",
                                  facecolor = "#000000",
                        )
        ]:
                ax.add_patch( p )

        plt.legend( loc = 'best' )
        plt.xlabel( "Duration (sec.)" )
        plt.ylabel( "Pecent Slowdown" )
        plt.savefig( dest + config + "apps-delta.pdf" );
        plt.close()


        fig, ax = plt.subplots()
        ax.set_xscale( 'log', basex = 10 )

        for i, a in enumerate( micro ):
                mask = np.isfinite( data[ a ] )
                the_min = min( data[ a ][ mask ] )
                if  not the_min:
                        continue
                percent = [ ( x - the_min ) / the_min * 100.0
                                for x in data[ a ][ mask ] ]
                plt.plot( data[ "Delta" ][ mask ],
                        percent, 
                        lw = 1,
                        label = a )
        ymin, ymax = plt.ylim()
        for p in [
                        patches.Rectangle(
                                ( HW_lower, ymin ), HW_upper - HW_lower,
                                  ymax - ymin, 
                                  linestyle='dotted',
                                  alpha=0.3,
                                  edgecolor = "#000000",
                                  facecolor = "#000000",
                        ),
                        patches.Rectangle(
                                ( OS_lower, ymin ), OS_upper - OS_lower,
                                  ymax - ymin, 
                                  linestyle='dotted',
                                  alpha=0.3,
                                  edgecolor = "#000000",
                                  facecolor = "#000000",
                        ),
                        patches.Rectangle(
                                ( FW_lower, ymin ), FW_upper - FW_lower,
                                  ymax - ymin, 
                                  linestyle='dotted',
                                  alpha=0.3,
                                  edgecolor = "#000000",
                                  facecolor = "#000000",
                        )
        ]:
                ax.add_patch( p )

        plt.legend( loc = 'best' )
        plt.xlabel( "Duration (sec.)" )
        plt.ylabel( "Pecent Slowdown" )
        plt.savefig( dest + config + "micro-delta.pdf" );
        plt.close()



