#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find PROJ4 library
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

import os, glob

from sysdevel.util import *

environment = dict()
proj4_found = False


def null():
    global environment
    environment['PROJ4_INCLUDE_DIR'] = None
    environment['PROJ4_LIBRARY_DIR'] = None
    environment['PROJ4_LIBRARIES'] = []
    environment['PROJ4_LIBS'] = []


def is_installed(environ, version):
    global environment, proj4_found
    base_dirs = []
    try:
        base_dirs.append(os.environ['PROJ4_ROOT'])
    except:
        pass
    if 'windows' in platform.system().lower():
        base_dirs.append(os.path.join('C:', os.sep, 'OSGeo4W'))
        try:
            base_dirs.apeend(environ['MSYS_DIR'])
        except:
            pass
    try:
        proj4_inc_dir = find_header('proj_api.h', base_dirs)
        proj4_lib_dir, proj4_libs  = find_libraries('proj', base_dirs)
        proj4_found = True
    except:
        return proj4_found

    environment['PROJ4_INCLUDE_DIR'] = proj4_inc_dir
    environment['PROJ4_LIBRARY_DIR'] = proj4_lib_dir
    environment['PROJ4_LIBRARIES'] = proj4_libs
    environment['PROJ4_LIBS'] = ['proj',]
    return proj4_found


def install(environ, version, target='build'):
    if not proj4_found:
        if version is None:
            version = '4.8.0'
        website = ('http://trac.osgeo.org/proj/',)
        if 'windows' in platform.system().lower():
            ## assumes MinGW installed and detected
            website = ('http://download.osgeo.org/proj/',)
            here = os.path.abspath(os.getcwd())
            src_dir = 'proj-' + str(version)
            archive = src_dir + '.tar.gz'
            fetch(''.join(website), archive, archive)
            unarchive(os.path.join(here, download_dir, archive),
                      target, src_dir)
            build_dir = os.path.join(src_dir, '_build')
            mkdir(build_dir)
            os.chdir(build_dir)
            mingw_check_call(environ, ['../configure',
                                       '--prefix=' + environ['MSYS_PREFIX']])
            mingw_check_call(environ, ['make'])
            mingw_check_call(environ, ['make', 'install'])
            os.chdir(here)
        else:
            global_install('PROJ4', website,
                           None,
                           'libproj4',
                           'libproj-dev',
                           'proj-devel')
        is_installed()

