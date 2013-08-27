"""
Copyright 2013.  Los Alamos National Security, LLC.
This material was produced under U.S. Government contract
DE-AC52-06NA25396 for Los Alamos National Laboratory (LANL), which is
operated by Los Alamos National Security, LLC for the U.S. Department
of Energy. The U.S. Government has rights to use, reproduce, and
distribute this software.  NEITHER THE GOVERNMENT NOR LOS ALAMOS
NATIONAL SECURITY, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR
ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is
modified to produce derivative works, such modified software should be
clearly marked, so as not to confuse it with the version available
from LANL.

Licensed under the Mozilla Public License, Version 2.0 (the
"License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at
http://www.mozilla.org/MPL/2.0/

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.
"""

"""
'build_docbook' command using emacs on org-mode files
"""


import os
import sys
import glob
import subprocess

try:
    from numpy.distutils.command.build_ext import build_ext
except:
    from distutils.command.build_ext import build_ext

import util


def make_doc(src_file, target_dir=None, resource_dir=None, stylesheet=None):
    src_file = os.path.abspath(src_file)
    if target_dir is None:
        target_dir = os.path.dirname(src_file)
    else:
        target_dir = os.path.abspath(target_dir)
    if resource_dir is None:
        resource_dir = os.path.abspath(os.path.dirname(src_file))
    if stylesheet is None:
        stylesheet = util.find_file(os.path.join('fo', 'docbook.xsl'))
    else:
        stylesheet = os.path.abspath(stylesheet)

    fop_exe = util.find_program('fop')
    java_exe = util.find_program('java')
    try:
        saxon_exe = [util.find_program('saxon')]
    except:
        classpaths = []
        try:
            for path in os.environ['CLASSPATH'].split(os.pathsep):
                classpaths.append(os.path.dirname(path))
        except:
            pass
        try:
            classpaths.append(os.path.join(os.environ['JAVA_HOME'], 'lib'))
        except:
            pass
        saxon_jar = util.find_file('saxon*.jar',
                                   ['/usr/share/java', '/usr/local/share/java',
                                    '/opt/local/share/java',] + classpaths)
        saxon_exe = [java_exe, '-classpath', saxon_jar]
    if not os.path.exists(target_dir):
        util.mkdir(target_dir)

    # FIXME Need xsl-stylesheets dir?
    
    ## Need to respect relative paths
    here = os.getcwd()
    os.chdir(resource_dir)
    src_base = os.path.basename(src_file)
    fo_src = os.path.join(target_dir, os.path.splitext(src_base)[0] + '.fo')
    pdf_dst = os.path.join(target_dir, os.path.splitext(src_base)[0] + '.pdf')

    cmd_line = saxon_exe + ['com.icl.saxon.StyleSheet',
                            '-o', fo_src, src_file, stylesheet]
    subprocess.check_call(" ".join(cmd_line), shell=True)

    cmd_line = [fop_exe, '-fo', fo_src, '-pdf', pdf_dst]
    subprocess.check_call(" ".join(cmd_line), shell=True)
    os.chdir(here)


class build_docbook(build_ext):
    '''
    Build pdfs from docbook xml
    '''
    def run(self):
        if not self.distribution.doc_dir:
            return

        build = self.get_finalized_command('build')
        target = os.path.abspath(os.path.join(build.build_base, 'docs'))

        # FIXME filename or (filename, stylesheet) from self.distribution
        xml_files = glob.glob(os.path.join(self.distribution.doc_dir, '*.xml'))
        for xfile in xml_files:
            make_docs(xfile, target)