# Grid Engine Scripts

These are small scripts I've developed to assist in day to day Grid Engine
support for the Speech Group.

## Getting Started

Download them and put them in your path.  They need to be run on an administration host.

## gpuacct.py

Python script for working out monthly CPU and GPU usage for grant application purposes.

## overloads

Lists the hosts where the system load is greater than the number of cores.

## qdels

Obsolete.

## qdhosts

List hosts with disabled queues.

## qerrors

**Useful:** Find queues with error states and clear them.

## reserve

Script for reserving a host (or hosts) for a particular user group.  If you want to reserve it for 
an individual, just create a user group consisting of only them (use their login name to make it obvious).

## staticsp

Use ipmitool to set the server's service processor to use a static IP address rather than configure itself with DHCP.

## Dependencies

* Python
* Bash
* Need to be run on an admin host

## Author

* **Anna Langley** - *Initial work* - [mrscasper](https://github.com/mrscasper)
