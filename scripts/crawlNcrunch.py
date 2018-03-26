#!/usr/bin/env python
#

import logging as log
import sys as sys
import os
import argparse as ap
import time as time
import re

simpledata = {}

seen_freqs = set()
seen_apps = set()
seen_deltas = set()

def printf(format, *args):
                sys.stdout.write(format % args)

if __name__ == '__main__':

        parser = ap.ArgumentParser( description = 'Simple correctable memory data collection' )

        parser.add_argument( '-i', '--input', nargs='+', default = [ "." ],
                help = 'List directories and address to search (default ./)' )
        
        args = parser.parse_args()

        log.basicConfig( level = log.DEBUG,
                        format = '%(levelname)s (%(threadName)-9s): %(message)s',
                        filename = ( 'correctable_crunch-time_%f.log' ) % ( time.time() )
        )

        mypath = args.input

        while mypath:

                element = mypath.pop( 0 )

                log.debug( "Considering %s\n" % ( element ) )

                if( os.path.isdir( element ) ):
                        files = [ f for f in os.listdir( element )
                                        if os.path.isfile( os.path.join( element, f ) ) ]

                        dirs = [ d for d in os.listdir( element )
                                        if os.path.isdir( os.path.join( element, d ) ) ]

                        dirs = map( lambda x: os.path.join( element, x ), dirs )

                        files = filter( lambda x: x.endswith( '.out'),
                                        map( lambda x: os.path.join( element, x ), files ) )

                        mypath.extend( dirs )

                        if not files:
                                continue

                else:
                        files = [ element ]

                refile = r"([a-zA-Z-_0-9]+)-([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)Hz-([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)delta.(\d+).out"
                
                refline = r"^\(\d+ processes\) Procs and min mean max time: (\d+)\s+([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)"
                for f in files:
                        ( path, file ) = os.path.split( f )
                        log.debug( "[%s] Searching file: %s\n" % ( path, file ) )

                        if( re.search( refile, file ) ):
                                match = re.search( refile, file )
                                APP = match.group( 1 )
                                seen_apps.add( APP )
                                FREQ = match.group( 2 )
                                seen_freqs.add(FREQ)
                                DELTA = match.group( 6 )
                                seen_deltas.add(DELTA)
                                log.debug( "Match found: APP(%s) FREQ(%g) DELTA(%g)\n" % 
                                        ( APP, float( FREQ ), float( DELTA ) ) )
                                
                                log.debug( "Opening %s for searching\n" % f )

                                with open( f ) as search:
                                        for line in search:
                                                line = line.rstrip()
                                                if( re.search( refline, line )):
                                                        match = re.search(
                                                                        refline,
                                                                        line )
                                                        PROC = match.group( 1 )
                                                        MIN = match.group( 2 )
                                                        MEAN = match.group( 6 )
                                                        MAX = match.group( 10 )
                                                        log.debug( "\tPROC(%d) MAX(%g)\n"
                                                                        % (
                                                                        int(
                                                                                PROC
                                                                                ),
                                                                        float(
                                                                                MAX
                                                                                )
                                                                        ) )
                                                        simpledata[ "%s-%s-%s-%s" % ( FREQ, DELTA, APP, PROC ) ] = MAX

        printf( "Found %d data entries\n", len( simpledata ) )

#        print simpledata

        apps = sorted( seen_apps )
        delta = sorted( seen_deltas, key=float )
        freqs = sorted( seen_freqs )
        for freq in freqs:
                for nodes in [ "65536", "32768", "16384" ]:
                        with open( freq + "_" + nodes + ".delta",
                                        "w" ) as out:
                                out.write( "Delta\t " + "\t ".join( apps ) + "\n" )
                                for d in delta:
                                        out.write( d + "\t " )
                                        for a in apps:
                                                try:
                                                        value = simpledata[ "%s-%s-%s-%s" % ( freq, d, a, nodes ) ] 
                                                except KeyError, e:
                                                        value = '-'
                                                out.write( str( value ) + "\t " )
                                        out.write( "\n" )

