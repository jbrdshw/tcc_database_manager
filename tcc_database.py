#!/usr/bin/python
# encoding: utf-8

################################################################################
##                                                                            ##
## tcc_database.py                                                            ##
##                                                                            ##
## This script takes in a service name and a bundle ID and adds an entry to   ##
## the appropriate TCC.db file to allow access for that item.  This is to be  ##
## used to reduce the amount of dialogs users in our computer labs get.       ##
##                                                                            ##
################################################################################
##                                                                            ##
## COPYRIGHT (c) 2014 Marriott Library IT Services.  All Rights Reserved.     ##
##                                                                            ##
## Author:          Pierce Darragh - pierce.darragh@utah.edu                  ##
## Creation Date:   February 07, 2014                                         ##
## Last Updated:    February 07, 2014                                         ##
##                                                                            ##
## Permission to use, copy, modify, and distribute this software and its      ##
## documentation for any purpose and without fee is hereby granted, provided  ##
## that the above copyright notice appears in all copies and that both that   ##
## copyright notice and this permission notice appear in supporting           ##
## documentation, and that the name of The Marriott Library not be used in    ##
## advertising or publicity pertaining to distribution of the software        ##
## without specific, written prior permission. This software is supplied as-  ##
## is without expressed or implied warranties of any kind.                    ##
##                                                                            ##
################################################################################
##                                                                            ##
## Much of this code has been copy/pasted and adapted from the tccmanager.py  ##
## script written by Tim Sutton and published to his GitHub repository at:    ##
##     https://github.com/timsutton/scripts/tree/master/tccmanager            ##
## Many thanks to Tim for posting his code online like that; it has been very ##
## helpful to us.                                                             ##
##                                                                            ##
################################################################################
