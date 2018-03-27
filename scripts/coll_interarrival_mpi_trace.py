#!/usr/bin/env python

import re
import math

# This is a primitive one-off script.  Apologies.  --sll
# NOTE: all of the <ARGUMENTS> need to be replaced by appropriate values
# NOTE: this script assumes a specific directory structure; it assumes that traces 
#       are located at: root_trace_dir/additional_path/process_count/
# NOTE: this script only analyzes the trace for Rank 0

mpi_op_re = re.compile("^(MPI\_(Bcast|Allreduce|Reduce|Barrier|Scan|Reduce_scatter|Alltoall|Allgather|Allgatherv|Exscan)):(\d+):")

root_trace_dir = "./"

workloads = {}
# EXAMPLE : workloads["MCCK"] = ("mcck/traces", 216)
workloads["lmps-lj" ] = ("lmps-lj", 128)

for (appname, (directory,process_count)) in sorted(workloads.items()):
  coll_inter = {}

  # Number of zeros in Rank 0 filename is based on process count
  zeros = int(math.floor(math.log(process_count, 10)) + 1) * "0"
  filename = root_trace_dir + directory + ("/%d/rank-%s.txt" % (process_count, zeros))
  last_time = None
  with open(filename, "r") as f:
    outfile = open(appname + "-interarrival.txt", "w")
    outfile.write( "# " + filename + "\n")

    for i, line in enumerate( f ):
      mpi_op_match = mpi_op_re.match( line )
      if mpi_op_match == None:
#       assert "MPI_" not in line or "//" in line
        continue

      mpi_op = mpi_op_match.group( 1 )
      mpi_op_time = int( mpi_op_match.group( 3 ) )

      if last_time == None:
              last_time = mpi_op_time
              continue

      outfile.write( "%d\t %d\n" % (
              ( mpi_op_time - last_time ),
              mpi_op_time ) )
      last_time = mpi_op_time
