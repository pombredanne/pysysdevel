
from ..prerequisites import *
from ..configuration import py_config

class configuration(py_config):
    """
    Find/install pytest-runner
    """
    def __init__(self):
        py_config.__init__(self, 'pytest-runner', '2.0',
                           dependencies=['hgtools',], debug=False)
        #FIXME setuptools dependency


    def is_installed(self, environ, version=None):
        try:
            import ptr
            self.found = True
        except Exception:
            if self.debug:
                e = sys.exc_info()[1]
                print('Exception: ' + str(e))
                print(traceback.print_exc())
        return self.found