#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find/install ffnet package
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

from pydevel.util import *

environment = dict()
ffnet_found = False


def is_installed():
    global environment, ffnet_found
    try:
        import serial
        environment['FFNET_VERSION'] = serial.VERSION
        ffnet_found = True
    except:
        pass
    return ffnet_found


def install(target='build'):
    global environment
    if not ffnet_found:
        try:
            from setuptools.command import easy_install
            easy_install.main(["-U","ffnet"])
            import ffnet
            environment['FFNET_VERSION'] = ffnet.version
        except:
            try:
                import urllib, tarfile, subprocess
                website = 'http://prdownloads.sourceforge.net/ffnet/'
                ver = '0.7.1'
                environment['FFNET_VERSION'] = ver
                here = os.path.abspath(os.getcwd())
                download_file = 'ffnet-' + ver + '.tar.gz'
                set_downloading_file(website + download_file)
                if not os.path.exists(target):
                    os.makedirs(target)
                os.chdir(target)
                if not os.path.exists(download_file):
                    urllib.urlretrieve(website + download_file,
                                       os.path.join(target, download_file),
                                       download_progress)
                z = tarfile.open(download_file, 'r:gz')
                z.extractall()                
                os.chdir('ffnet-' + ver)
                cmd_line = ['python', 'setup.py', 'install']
                ##TODO installing package will fail
                status = subprocess.call(cmd_line)
                if status != 0:
                    raise Exception("Command '" + str(cmd_line) +
                                    "' returned non-zero exit status "
                                    + str(status))
                os.chdir(here)
            except Exception,e:
                raise Exception('Unable to install ffnet: ' + str(e))
