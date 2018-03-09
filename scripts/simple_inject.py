#!/usr/bin/env python
#

import threading as thread
import time as time
import logging as log
from subprocess import call
import sys as sys
import argparse as ap

address = 0x12345000

def setup_config():

        global inject_value

        log.debug( 'Initializing memory injection config' )

        return_code = call( ( "echo 0x%x > /sys/kernel/debug/apei/einj/param1" ) % address,
                        shell = True )

        if( return_code != 0 ):
                sys.exit( 'Problem writing injection address' )

        return_code = call( 'echo $((-1 << 12)) > /sys/kernel/debug/apei/einj/param2',
                        shell = True )

        if( return_code != 0 ):
                sys.exit( 'Problem writing injection mask' )

        return_code = call( 'echo 0x%x > /sys/kernel/debug/apei/einj/error_type' % inject_value,
                        shell = True )

        if( return_code != 0 ):
                sys.exit( 'Problem writing error type (correctable DRAM)' )

        return 0

def inject_now():

        global inject_cnt
        global inject_value
        global do_inject

        if( do_inject ):
                log.debug( 'Inject error now (0x%x)' % inject_value)
                return_code = call( 'echo 1 > /sys/kernel/debug/apei/einj/error_inject',
                        shell = True )
        else:
                log.debug( 'Inject dry-run' )
                return_code = call( 'echo 0x%x > /sys/kernel/debug/apei/einj/error_type' % inject_value,
                        shell = True )
        
        if( return_code != 0 ):
                sys.exit( 'Problem writing error type (correctable DRAM)' )

        inject_cnt += 1

        return 0

if __name__ == '__main__':

        inject_cnt = 0
        inject_value = 0x0
        do_inject = True

        parser = ap.ArgumentParser( description = 'Simple memory error injection utility' )
        parser.add_argument( '-i', '--interval', default = 60, type = int,
                        help = 'Interval in seconds to inject memory errors' )
        parser.add_argument( '-l', '--length', default = 1000, type = int,
                        help = 'Length in seconds to run application' )
        parser.add_argument( '-c', '--dram-correctable', default = True,
                        action = 'store_true',
                        help = 'inject DRAM correctable error (default on)' )
        parser.add_argument( '-u', '--dram-uncorrectable', default = False,
                        action = 'store_true',
                        help = 'inject DRAM uncorrectable error non-fatal (default off)' )
        parser.add_argument( '-d', '--dry-run', default = False,
                        action = 'store_true',
                        help = 'Dry-run, so not actually inject the error (default off)' )
        parser.add_argument( '-v', '--version', action = 'version', 
                        version = '%(prog)s 1.0' )

        args = parser.parse_args()

        log.basicConfig( level = log.DEBUG,
                format = '%(levelname)s (%(threadName)-9s): %(message)s', 
                filename = ( 'correctable_interval-%d_length-%d_time-%f.log' ) % 
                                ( args.interval, args.length, time.time() )
        )

        if( args.dram_uncorrectable ):
                inject_value = 0x10
        else:
                inject_value = 0x8

        if( args.dry_run ):
                do_inject = False

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
