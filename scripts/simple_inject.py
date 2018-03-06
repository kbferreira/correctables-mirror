#!/usr/bin/env python
#

import threading as thread
import time as time
import logging as log
from subprocess import call
import sys as sys
import argparse as ap

log.basicConfig( level = log.DEBUG,
                format = '%(levelname)s (%(threadName)-9s): %(message)s', 
                filename = 'correctable.log' )

address = 0x12345000

def setup_config():
        log.debug( 'Initializing memory injection config' )

        return_code = call( ( "echo 0x%x > /sys/kernel/debug/apei/einj/param1" ) % address,
                        shell = True )

        if( return_code != 0 ):
                sys.exit( 'Problem writing injection address' )

        return_code = call( 'echo $((-1 << 12)) > /sys/kernel/debug/apei/einj/param2',
                        shell = True )

        if( return_code != 0 ):
                sys.exit( 'Problem writing injection mask' )

        return_code = call( 'echo 0x8 > /sys/kernel/debug/apei/einj/error_type',
                        shell = True )

        if( return_code != 0 ):
                sys.exit( 'Problem writing error type (correctable DRAM)' )

        return 0

def inject_now():

        global inject_cnt

        log.debug( 'Inject error now' )

        return_code = call( 'echo 1 > /sys/kernel/debug/apei/einj/error_inject',
                        shell = True )
        
        if( return_code != 0 ):
                sys.exit( 'Problem writing error type (correctable DRAM)' )

        inject_cnt += 1

        return 0

if __name__ == '__main__':

        inject_cnt = 0

        parser = ap.ArgumentParser( description = 'Simple memory error injection utility' )
        parser.add_argument( '-i', '--interval', default = 60, type = int,
                        help = 'Interval in seconds to inject memory errors' )
        parser.add_argument( '-l', '--length', default = 1000, type = int,
                        help = 'Length in seconds to run application' )
        parser.add_argument( '-v', '--version', action = 'version', 
                        version = '%(prog)s 1.0' )

        args = parser.parse_args()

        setup_config()

        inject = thread.Timer( 0, inject_now )
        inject.setName( 'inject' )

        log.info( 'Start it up ...' )

        start_time = time.time()

        log.debug( 'Start the timers' )
        inject.start()
        inject.join()

        while ( time.time() - start_time ) < args.length:

                inject = thread.Timer( args.interval, inject_now )
                inject.setName( 'inject' )

                log.debug( 'Start the timers' )

                inject.start()
                inject.join()

        log.info( ( 'Done: Injection count -- %d' ) % inject_cnt )
