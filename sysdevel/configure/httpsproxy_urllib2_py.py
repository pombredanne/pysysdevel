#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
If we're running Python 2.4/5, pull this patched urllib2. 
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

import sys

from sysdevel.util import *

environment = dict()
urllib_patch_found = False


def null():
    pass


def is_installed(environ, version):
    global urllib_patch_found
    if sys.version_info < (2, 6):
        ## Cannot detect if this is already present
        urllib_patch_found = False
    else:
        ## Not needed for Python 2.6+
        urllib_patch_found = True
    return urllib_patch_found


def install(environ, version, locally=True):
    global urllib_patch_found
    if not urllib_patch_found:
        website = 'http://pypi.python.org/packages/source/h/httpsproxy_urllib2/'
        if version is None:
            version = '1.0'
        src_dir = 'httpsproxy_urllib2-' + str(version)
        archive = src_dir + '.tar.gz' 
        install_pypkg(src_dir, website, archive, locally=locally)
        urllib_patch_found = True
        reload(urllib2)
        reload(httplib)
        ## Don't check / can't detect
        ## Also need to update setuptools, if present
        """
        try:
            import setuptools
        except:
            pass
        if 'setuptools' in sys.modules:
            website = 'http://pypi.python.org/packages/source/s/setuptools/'
            version = '0.6c11'
            src_dir = 'setuptools-' + str(version)
            archive = src_dir + '.tar.gz' 
            install_pypkg(src_dir, website, archive, locally=locally)
            reload(setuptools)
            """