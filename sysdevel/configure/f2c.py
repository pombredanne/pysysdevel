#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find F2C
"""
#**************************************************************************
# 
# This material was prepared by the Los Alamos National Security, LLC 
# (LANS), under Contract DE-AC52-06NA25396 with the U.S. Department of 
# Energy (DOE). All rights in the material are reserved by DOE on behalf 
# of the Government and LANS pursuant to the contract. You are authorized 
# to use the material for Government purposes but it is not to be released 
# or distributed to the public. NEITHER THE UNITED STATES NOR THE UNITED 
# STATES DEPARTMENT OF ENERGY, NOR LOS ALAMOS NATIONAL SECURITY, LLC, NOR 
# ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR 
# ASSUMES ANY LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY, 
# COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, APPARATUS, PRODUCT, OR 
# PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE 
# PRIVATELY OWNED RIGHTS.
# 
#**************************************************************************

import os

from sysdevel.util import *

environment = dict()
f2c_found = False

def null():
    global environment
    environment['F2C_INCLUDE_DIR'] = None


def is_installed(version=None):
    global environment, f2c_found
    try:
        incl_dir = find_header('f2c.h')
        environment['F2C_INCLUDE_DIR'] = find_header('f2c.h')
        ## f2c lib is built into libgfortran
        f2c_found = True
    except Exception,e:
        f2c_found = False
    return f2c_found


def install(target='build', version=None):
    global environment
    if not f2c_found:
        website = 'http://www.netlib.org/f2c/'
        header_file = 'f2c.h'        
        fetch(''.join(website), header_file, header_file)
        shutil.copy(os.path.join(download_dir, header_file), target)
        environment['F2C_INCLUDE_DIR'] = target