#!/usr/bin/env python

"""
    Script for collecting gpu usage data from gridengine between specified dates (at midnight)
    Anna Langley <jal58@cam.ac.uk> 30.11.2017

    This is a first pass at the problem, and Mark Gales may have a later and improved version.
"""

import argparse
import datetime
import subprocess
import sys

# Set the defaults
def ThisMonth():
    """
        This function returns the current month
        as a string in the form YYYYMM
    """
    return str(datetime.datetime.now().year) + str(datetime.datetime.now().month)

def LastMonth():
    """
        This function returns last month
        as a string in in the form YYYYMM
    """
    year  = datetime.datetime.now().year
    month = datetime.datetime.now().month - 1
    if month == 0:
        month  = 12
        year  -= 1
    return str(year) + str(month)

class defaults:
    """
        Object holding defaults, which can be overridden on the command line.
        This is the place to change the defaults, if you need to.
    """
    cpucost  = 414.99
    gpucost  = 414.99
    start    = LastMonth()
    end      = ThisMonth()
    projects = "material,nst,babel,babel-eval"
    users    = "ar527,mjfg"

# Parse command line
parser = argparse.ArgumentParser(
                   description="Script for calculating Gridengine usage costs",
                   epilog="Anna Langley <jal58@cam.ac.uk>, 30.11.2017")
parser.add_argument("-c", "--cpucost",
                   dest='cpucost', type=float,
                   default=defaults.cpucost,
                   help="Override default CPU cost (USD/Yr): " + str(defaults.cpucost))
parser.add_argument("-g", "--gpucost",
                    dest='gpucost', type=float,
                    default=defaults.gpucost,
                    help="Override default GPU cost (USD/Yr): " + str(defaults.gpucost))
parser.add_argument("-s", "--start",
                   dest='start', type=str,
                   default=defaults.start,
                   help="Override default start (YYYYMM): " + defaults.start)
parser.add_argument("-e", "--end",
                   dest='end', type=str,
                   default=defaults.end,
                   help="Override default end (YYYYMM): " + defaults.end)
parser.add_argument("-p", "--projects",
                    dest='projects', type=str,
                    default=defaults.projects,
                    help="Comma separated list of projects, default: " + defaults.projects)
parser.add_argument("-u", "--users",
                    dest='users', type=str,
                    default=defaults.users,
                    help="Comma separated list of users, default: " + defaults.users)
parser.add_argument("-f", "--file",
                    dest='outfile', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help="Optional output file.  Will write to stdout if absent")
args = parser.parse_args()

class params:
    """
        Object holding the paramaters for this run
    """
    cpucost  = args.cpucost
    gpucost  = args.gpucost
    start    = args.start + "010000"
    end      = args.end   + "010000"
    projects = args.projects.split(',')
    users    = args.users.split(',')
    outfile  = args.outfile
    cpuqueues = ['all-high.q', 'all-low.q', 'all-verlow.q', 'cuda-cpu.q']
    gpuqueues = ['cuda-fast-1.q', 'cuda-fast-2.q', 'cuda-fast-3.q', 'cuda-fast-4.q',
                 'cuda-low-1.q',  'cuda-low-2.q',  'cuda-low-3.q',  'cuda-low-4.q']

class outputs:
    CPUsecs  = 0.0
    CPUyears = 0.0
    CPUcost  = 0.0
    GPUsecs  = 0.0
    GPUyears = 0.0
    GPUcost  = 0.0


# CPU Seconds
for queue in params.cpuqueues:
    for project in params.projects:
        for user in params.users:
            params.outfile.write("\nCPU usage: Queue: {} Project: {} User: {}\n".format(queue, project, user))
            for line in subprocess.check_output(['qacct',
                             '-h',
                             '-q', queue,
                             '-P', project,
                             '-o', user,
                             '-b', params.start,
                             '-e', params.end]).splitlines()[2:]:
                outputs.CPUsecs += float(line.split()[6])
                params.outfile.write(line + '\n')


# GPU Seconds
for queue in params.gpuqueues:
    for project in params.projects:
        for user in params.users:
            params.outfile.write("\nGPU usage: Queue: {} Project: {} User: {}\n".format(queue, project, user))
            for line in subprocess.check_output(['qacct',
                             '-h',
                             '-q', queue,
                             '-P', project,
                             '-o', user,
                             '-b', params.start,
                             '-e', params.end]).splitlines()[2:]:
                outputs.GPUsecs += float(line.split()[6])
                params.outfile.write(line + '\n')

# Convert seconds to years and costs
# CPU cost is divide by two to account for hyperthreading
outputs.CPUyears = outputs.CPUsecs / (2 * 3600 * 24 * 365.0)
outputs.CPUcost  = outputs.CPUyears * params.cpucost
outputs.GPUyears = outputs.GPUsecs / (3600 * 24 * 365.0)
outputs.GPUcost  = outputs.GPUyears * params.gpucost


params.outfile.write("CPU Seconds: {:8.2f} Years: {:2.4f} Cost ${:.2f}\n".format(outputs.CPUsecs, outputs.CPUyears, outputs.CPUcost))
params.outfile.write("GPU Seconds: {:8.2f} Years: {:2.4f} Cost ${:.2f}\n".format(outputs.GPUsecs, outputs.GPUyears, outputs.GPUcost))

