#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find Sphinx
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

import os, platform

from sysdevel.util import *

environment = dict()
sphinx_found = False


def null():
    pass


def is_installed(version=None):
    global sphinx_found
    try:
        import sphinx
        ver = sphinx.__version__
        if not version is None and ver < version:
            return sphinx_found
        sphinx_found = True
    except:
        pass
    return sphinx_found


def install(target='build', version=None):
    if not sphinx_found:
        website = 'https://pypi.python.org/packages/source/S/Sphinx/'
        if version is None:
            version = '1.1.3'
        archive ='Sphinx-' + str(version) + '.tar.gz' 
        install_pypkg_locally('Sphinx-' + str(version), website, archive, target)