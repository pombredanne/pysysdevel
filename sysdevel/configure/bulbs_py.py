
import glob
import os

from sysdevel.util import *
from sysdevel.configuration import py_config

class configuration(py_config):
    """
    Find/install Bulbs
    """
    def __init__(self):
        py_config.__init__(self, 'bulbs', '0.2.2', debug=False)


    def install(self, environ, version, locally=True):
        if not self.found:
            if version is None:
                version = self.version
            website = 'https://github.com/espeed/bulbs/tarball/'
            src_dir = 'bulbs-' + str(version)
            archive = src_dir + '.tar.gz' 
            fetch(website, 'master', archive)
            unarchive(archive, src_dir)
            try:
                ext = glob.glob(os.path.join(target_build_dir, '*bulbs*'))[0]
                os.rename(ext, os.path.join(target_build_dir, src_dir))
            except:
                pass
            install_pypkg(src_dir, website, archive, locally=locally)
            if not self.is_installed(environ, version):
                raise Exception('Bulbs installation failed.')
