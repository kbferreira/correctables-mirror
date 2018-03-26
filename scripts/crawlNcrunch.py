#!/usr/bin/env python
#

import logging as log
import sys as sys
import os
import argparse as ap
import time as time
import re

data = {}
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
                                FREQ = match.group( 2 )
                                DELTA = match.group( 6 )
                                printf( "Match found: APP(%s) FREQ(%g) DELTA(%g)\n",
                                                APP,
                                                float( FREQ ),
                                                float( DELTA ) )
                                
                                log.debug( "Opening %s for searching\n" % f )

                                with open( f ) as search:
                                        for line in search:
                                                line = line.rstrip()
                                                if( re.search( refline, line )):
                                                        match = re.search(
                                                                        refline,
                                                                        line )
                                                        PROC = match.group( 1 )
                                                        MAX = match.group( 11 )
                                                        printf( "\tPROC(%d) MAX(%g)\n",
                                                                        int(
                                                                                PROC
                                                                                ),
                                                                        float(
                                                                                MAX
                                                                                )
                                                                        )
                                                        this_size = len( data )
                                                        print this_size
                                                        data[ this_size ] = {}
                                                        data[ this_size ]['freq'] = FREQ
                                                        data[ this_size ][ 'delta' ] = DELTA
                                                        data[ this_size ][ 'app' ] = APP
                                                        data[ this_size ][ 'p' ] = PROC
                                                        data[ this_size ][ 'max' ] = MAX
