# -*- coding: utf-8 -*-
"""
Custom extensions and setup
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
import shutil
import os
import platform
import subprocess

from numpy.distutils import extension
from numpy.distutils.numpy_distribution import NumpyDistribution
from numpy.distutils.command.build import build as old_build
from numpy.distutils.command.config_compiler import config_cc as old_config_cc
from numpy.distutils.command.config_compiler import config_fc as old_config_fc
from numpy.distutils.core import Extension
from distutils.command.install import install as old_install
from distutils.command.clean import clean as old_clean

import util


class WebExtension(extension.Extension):
    def __init__(self, name, sources, source_dir,
                 public_subdir='', extra_support_files=[],
                 extra_public_files=[], extra_compile_args=[],
                 compiler=None):
        extension.Extension.__init__(self, name, sources)
        self.source_directory = source_dir
        self.public_subdir = public_subdir
        self.extra_support_files = extra_support_files
        self.extra_public_files = extra_public_files
        self.compiler = compiler
        self.extra_compile_args = extra_compile_args


class DocExtension(extension.Extension):
    def __init__(self, name, source_dir, sphinx_cfg=None,
                 doxy_cfg=None, doxy_srcs=[], extra_docs = [],
                 extra_directories=[], no_sphinx=False,
                 style=util.DEFAULT_STYLE):
        extension.Extension.__init__(self, name, [])
        self.source_directory = source_dir
        self.sphinx_config = sphinx_cfg
        self.doxygen_cfg = doxy_cfg
        self.doxygen_srcs = doxy_srcs
        self.extra_docs = extra_docs
        self.extra_directories = extra_directories
        self.without_sphinx = no_sphinx
        self.style = style


class AntlrGrammar(extension.Extension):
    def __init__(self, name, directory, sources):
        extension.Extension.__init__(self, name, sources)
        self.directory = directory


class PyPlusPlusExtension(extension.Extension):
    def __init__(self, name, sources,
                 pypp_file, binding_file,
                 include_dirs=None,
                 define_macros=None,
                 undef_macros=None,
                 library_dirs=None,
                 libraries=None,
                 runtime_library_dirs=None,
                 extra_objects=None,
                 extra_compile_args=None,
                 extra_link_args=None,
                 export_symbols=None,
                 swig_opts=None,
                 depends=None,
                 language=None,
                 f2py_options=None,
                 module_dirs=None,):
        extension.Extension.__init__(self, name, sources,
                                     include_dirs, define_macros, undef_macros,
                                     library_dirs, libraries,
                                     runtime_library_dirs, extra_objects,
                                     extra_compile_args, extra_link_args,
                                     export_symbols, swig_opts, depends,
                                     language, f2py_options, module_dirs,)
        self.pyppdef = pypp_file
        self.binding_file = binding_file
        self.builder = ''


class Executable(extension.Extension):
    ## make sure it matches numpy extension signature
    def __init__(self, name, sources,
                 include_dirs=None,
                 define_macros=None,
                 undef_macros=None,
                 library_dirs=None,
                 libraries=None,
                 runtime_library_dirs=None,
                 extra_objects=None,
                 extra_compile_args=None,
                 extra_link_args=None,
                 export_symbols=None,
                 swig_opts=None,
                 depends=None,
                 language=None,
                 f2py_options=None,
                 module_dirs=None,):
        extension.Extension.__init__(self, name, sources,
                                     include_dirs, define_macros, undef_macros,
                                     library_dirs, libraries,
                                     runtime_library_dirs, extra_objects,
                                     extra_compile_args, extra_link_args,
                                     export_symbols, swig_opts, depends,
                                     language, f2py_options, module_dirs,)



############################################################

class CustomDistribution(NumpyDistribution):
    '''
    Subclass NumpyDistribution to support new commands
    '''
    def __init__(self, attrs=None):
        old_attrs = attrs
        ## setup the environment for custom commands
        self.environment = attrs.get('environment')
        if self.environment != None:
            del old_attrs['environment']
        else:
            self.environment = dict()
        ## PYJS web extensions
        self.web_ext_modules = attrs.get('web_ext_modules')
        if self.web_ext_modules != None:
            del old_attrs['web_ext_modules']
        ## Sphinx documentation
        self.doc_modules = attrs.get('doc_modules')
        if self.doc_modules != None:
            del old_attrs['doc_modules']
        ## Py++ extensions
        self.pypp_ext_modules = attrs.get('pypp_ext_modules')
        if self.pypp_ext_modules != None:
            del old_attrs['pypp_ext_modules']
        ## Shared libraries
        self.sh_libraries = attrs.get('sh_libraries')
        if self.sh_libraries != None:
            del old_attrs['sh_libraries']
        ## ANTLR parser/lexers
        self.antlr_modules = attrs.get('antlr_modules')
        if self.antlr_modules != None:
            del old_attrs['antlr_modules']
        ## Native executables
        self.native_executables = attrs.get('native_executables')
        if self.native_executables != None:
            del old_attrs['native_executables']
        ## Data to install to 'share'
        self.data_dirs = attrs.get('data_dirs')
        if self.data_dirs != None:
            del old_attrs['data_dirs']
        ## Non-stock libraries to install to 'lib' or 'lib64'
        self.extra_install_libraries = attrs.get('extra_install_libraries')
        if self.extra_install_libraries != None:
            del old_attrs['extra_install_libraries']
        ## Non-stock python packages to co-install
        self.extra_install_modules = attrs.get('extra_install_modules')
        if self.extra_install_modules != None:
            del old_attrs['extra_install_modules']
        ## Boilerplate scripts to create
        self.create_scripts = attrs.get('create_scripts')
        if self.create_scripts != None:
            del old_attrs['create_scripts']
        ## SysDevel support modules
        self.devel_support = attrs.get('devel_support')
        if self.devel_support != None:
            del old_attrs['devel_support']
        ## Files to delete upon 'clean'
        self.generated_files = attrs.get('generated_files')
        if self.generated_files != None:
            del old_attrs['generated_files']
        ## Separate packages with their own setup.py
        self.subpackages = attrs.get('subpackages')
        if self.subpackages != None:
            del old_attrs['subpackages']
        ## Whether to quit if a subpackage build fails
        self.quit_on_error = attrs.get('quit_on_error')
        if self.quit_on_error != None:
            del old_attrs['quit_on_error']
        ## Enable parallel building
        self.parallel_build = attrs.get('parallel_build')
        if self.parallel_build != None:
            del old_attrs['parallel_build']

        ## py2exe options
        self.ctypes_com_server = attrs.pop("ctypes_com_server", [])
        self.com_server = attrs.pop("com_server", [])
        self.service = attrs.pop("service", [])
        self.windows = attrs.pop("windows", [])
        self.console = attrs.pop("console", [])
        self.isapi = attrs.pop("isapi", [])
        self.zipfile = attrs.pop("zipfile", util.default_py2exe_library)

        NumpyDistribution.__init__(self, old_attrs)

    def has_scripts(self):
        return NumpyDistribution.has_scripts(self) or \
            (self.create_scripts != None and len(self.create_scripts) > 0)

    def has_c_libraries(self):
        return NumpyDistribution.has_c_libraries(self) or self.has_shared_libs()

    def has_shared_libs(self):
        return (self.sh_libraries != None and len(self.sh_libraries) > 0) or \
            (self.extra_install_libraries != None and
             len(self.extra_install_libraries) > 0)

    def has_antlr_extensions(self):
        return self.antlr_modules != None and len(self.antlr_modules) > 0

    def has_sysdevel_support(self):
        return self.devel_support != None and len(self.devel_support) > 0

    def has_pypp_extensions(self):
        return self.pypp_ext_modules != None and \
            len(self.pypp_ext_modules) > 0

    def has_web_extensions(self):
        return self.web_ext_modules != None and len(self.web_ext_modules) > 0

    def has_documents(self):
        return self.doc_modules != None and len(self.doc_modules) > 0

    def has_executables(self):
        return self.native_executables != None and \
            len(self.native_executables) > 0

    def has_data_directories(self):
        return self.data_dirs != None and len(self.data_dirs) > 0




def process_package(fnctn, build_base, progress, pyexe, argv,
                    pkg_name, pkg_dir, addtnl_args=[]):
    sys.stdout.write(fnctn.upper() + 'ING ' + pkg_name + ' in ' + pkg_dir + ' ')
    logging = True
    if 'clean' in fnctn:
        logging = False
    log_file = os.path.join(build_base, pkg_name + '_' + fnctn + '.log')
    if logging:
        log = open(log_file, 'w')
    else:
        log = open(os.devnull, 'w')
    try:
        p = subprocess.Popen([pyexe, os.path.join(pkg_dir, 'setup.py'),
                              ] + argv + addtnl_args,
                             stdout=log, stderr=log)
        status = progress(p)
        log.close()
    except KeyboardInterrupt:
        p.terminate()
        log.close()
        status = 1
    if status != 0:
        sys.stdout.write(' failed')
        if logging:
            sys.stdout.write('; See ' + log_file)
    else:
        sys.stdout.write(' done')
    sys.stdout.write('\n')           
    return pkg_name, status


def process_subpackages(parallel, fnctn, build_base, subpackages,
                        argv, quit_on_error):
    try:
        if not parallel:
            raise ImportError
        ## parallel
        import pp
        job_server = pp.Server()
        results = [job_server.submit(process_package,
                                     (fnctn, build_base, util.process_progress,
                                      sys.executable, argv,) + sub,
                                     (), ('os', 'subprocess',))
                   for sub in subpackages]
        has_failed = False
        for result in results:
            res_tpl = result()
            if res_tpl is None:
                raise Exception("Parallel build failed.")
            pkg_name, status = res_tpl
            if status != 0 and quit_on_error:
                has_failed = True
            if has_failed:
                sys.exit(status)
    except ImportError: ## serial
        for sub in subpackages:
            args = (fnctn, build_base, util.process_progress,
                    sys.executable, argv,) + sub
            pkg_name, status = process_package(*args)
            if status != 0 and quit_on_error:
                sys.exit(status)



class build(old_build):
    '''
    Subclass numpy build command to support new commands.
    Order is important: numpy, distutils, the rest.
    build_doc MUST be last.
    Assumes commands from build.build: build_py, build_clib, build_ext,
      build_scripts
    '''
    def has_pure_modules(self):
        return self.distribution.has_pure_modules() or \
            self.distribution.has_antlr_extensions() or \
            self.distribution.has_sysdevel_support()

    def has_scripts(self):
        return self.distribution.has_scripts()

    def has_c_libraries(self):
        return self.distribution.has_c_libraries()

    def has_shared_libraries(self):
        return self.distribution.has_shared_libs()

    def has_pypp_extensions(self):
        return self.distribution.has_pypp_extensions()

    def has_web_extensions(self):
        return self.distribution.has_web_extensions()

    def has_documents(self):
        return self.distribution.has_documents()

    def has_executables(self):
        return self.distribution.has_executables()

    def has_data(self):
        return self.distribution.has_data_files() or \
            self.distribution.has_data_directories()


    ## Order is important
    sub_commands = [
        ('config_cc',      lambda *args: True),
        ('config_fc',      lambda *args: True),
        ('build_src',      old_build.has_ext_modules),
        ('build_py',       has_pure_modules),
        ('build_js',       has_web_extensions),
        ('build_clib',     has_c_libraries),
        ('build_shlib',    has_shared_libraries),
        ('build_ext',      old_build.has_ext_modules),
        ('build_pypp_ext', has_pypp_extensions),
        ('build_scripts',  has_scripts),
        ('build_doc',      has_documents),
        ('build_exe',      has_executables),
        ]


    def run(self):
        if self.distribution.subpackages != None:
            if self.get_finalized_command('install').ran:
                return  ## avoid build after install
            try:
                os.makedirs(self.build_base)
            except:
                pass
            for idx in range(len(sys.argv)):
                if 'setup.py' in sys.argv[idx]:
                    break
            argv = list(sys.argv[idx+1:])
            if 'install' in argv:
                argv.remove('install')
            if 'clean' in argv:
                argv.remove('clean')

            process_subpackages(self.distribution.parallel_build, 'build',
                                self.build_base, self.distribution.subpackages,
                                argv, self.distribution.quit_on_error)

            if self.has_pure_modules() or self.has_c_libraries() or \
                    self.has_ext_modules() or self.has_shared_libraries() or \
                    self.has_pypp_extensions() or self.has_web_extensions() or \
                    self.has_documents() or self.has_executables() or \
                    self.has_scripts() or self.has_data():
                old_build.run(self)
        else:
            old_build.run(self)


class install(old_install):
    '''
    Subclass numpy build command to support new commands.
    Order is important: numpy, my build_shlib, distutils, the rest.
    build_doc MUST be last.
    '''
    def initialize_options (self):
        old_install.initialize_options(self)
        self.ran = False

    def has_lib(self):
        return old_install.has_lib(self) or self.distribution.has_shared_libs()

    def has_exe(self):
        return self.distribution.has_executables()

    def has_data(self):
        return self.distribution.has_data_files() or \
            self.distribution.has_data_directories()

    sub_commands = [('install_exe', has_exe),
                    ('install_data', has_data),
                    ('install_lib', has_lib),
                    ] + old_install.sub_commands  ## includes install_lib

    def run(self):
        if self.distribution.subpackages != None:
            self.ran = True
            build = self.get_finalized_command('build')
            try:
                os.makedirs(build.build_base)
            except:
                pass
            for idx in range(len(sys.argv)):
                if 'setup.py' in sys.argv[idx]:
                    break
            argv = list(sys.argv[idx+1:])
            if 'build' in argv:
                argv.remove('build')
            if 'clean' in argv:
                argv.remove('clean')

            process_subpackages(build.distribution.parallel_build, 'install',
                                build.build_base, self.distribution.subpackages,
                                argv, build.distribution.quit_on_error)

            if build.has_pure_modules() or build.has_c_libraries() or \
                    build.has_ext_modules() or build.has_shared_libraries() or \
                    build.has_pypp_extensions() or \
                    build.has_web_extensions() or \
                    build.has_documents() or build.has_executables() or \
                    build.has_scripts() or build.has_data():
                old_install.run(self)
        else:
            old_install.run(self)


class config_cc(old_config_cc):
    def finalize_options(self):
        ## force specific compiler
        if 'windows' in platform.system().lower():
            self.compiler = 'mingw32'
        old_config_cc.finalize_options(self)


class config_fc(old_config_fc):
    def initialize_options(self):
        old_config_fc.initialize_options(self)
        try:
            old_ldflags = os.environ['LDFLAGS']
        except:
            old_ldflags = ''
        if 'darwin' in platform.system().lower():
            ## force 32-bit (for wxWidgets compatibility)
            os.environ['CFLAGS'] = '-m32 -arch i386'
            os.environ['FFLAGS'] = '-m32 -arch i386'
            os.environ['LDFLAGS'] = old_ldflags + ' -m32 -arch i386'
        else:
            os.environ['LDFLAGS'] = old_ldflags + ' -shared'

    def finalize_options(self):
        if 'windows' in platform.system().lower():
            self.noopt = True
            self.debug = True
        old_config_fc.finalize_options(self)


class clean(old_clean):
    def run(self):
        # Remove .pyc files
        if hasattr(os, 'walk'):
            for root, dirs, files in os.walk('.'):
                for f in files:
                    if f.endswith('.pyc'):
                        try:
                            os.unlink(f)
                        except:
                            pass

        # Remove generated directories
        build = self.get_finalized_command('build')
        build_dir = build.build_base
        if os.path.exists(build_dir):
            try:
                shutil.rmtree(build_dir, ignore_errors=True)
            except:
                pass
        if self.distribution.subpackages != None:
            for idx in range(len(sys.argv)):
                if 'setup.py' in sys.argv[idx]:
                    break
            argv = list(sys.argv[idx+1:])
            process_subpackages(build.distribution.parallel_build, 'clean',
                                build.build_base, self.distribution.subpackages,
                                argv, False)

        # Remove user-specified generated files
        if self.distribution.generated_files != None:
            for path in self.distribution.generated_files:
                if os.path.isfile(path) or os.path.islink(path):
                    try:
                        os.unlink(path)
                    except:
                        pass
                elif os.path.isdir(path):
                    try:
                        shutil.rmtree(path, ignore_errors=True)
                    except:
                        pass

        old_clean.run(self)
        util.delete_cache()



##################################################
## Almost verbatim from numpy.disutils.core

if 'setuptools' in sys.modules:
    raise NotImplementedError('SysDevel is incompatible with setuptools')

    have_setuptools = True
    from setuptools import setup as old_setup
    # easy_install imports math, it may be picked up from cwd
    from setuptools.command import easy_install
    try:
        # very old versions of setuptools don't have this
        from setuptools.command import bdist_egg
    except ImportError:
        have_setuptools = False
else:
    from distutils.core import setup as old_setup
    have_setuptools = False

import warnings
import distutils.core
import distutils.dist
from numpy.distutils.misc_util import get_data_files, is_sequence, is_string
from numpy.distutils.command import config, build_ext, sdist, \
    install_headers, bdist_rpm, scons
from numpy.distutils.core import _exit_interactive_session, _command_line_ok, \
    _dict_append

import build_doc
import build_js
import build_py
import build_scripts
import build_pypp_ext
import build_src
import build_clib
import build_shlib
import build_exe
import install_data
import install_lib
import install_exe

my_cmdclass = {'build':            build,
               'build_src':        build_src.build_src,
               'build_scripts':    build_scripts.build_scripts,
               'config_cc':        config_cc,
               'config_fc':        config_fc,
               'config':           config.config,
               'build_ext':        build_ext.build_ext,
               'build_py':         build_py.build_py,
               'build_clib':       build_clib.build_clib,
               'build_shlib':      build_shlib.build_shlib,
               'build_js':         build_js.build_js,
               'build_doc':        build_doc.build_doc,
               'build_pypp_ext':   build_pypp_ext.build_pypp_ext,
               'build_exe':        build_exe.build_exe,
               'sdist':            sdist.sdist,
               'scons':            scons.scons,
               'install_exe':      install_exe.install_exe,
               'install_lib':      install_lib.install_lib,
               'install_data':     install_data.install_data,
               'install_headers':  install_headers.install_headers,
               'install':          install,
               'bdist_rpm':        bdist_rpm.bdist_rpm,
               'clean':            clean,
               }
if have_setuptools:
    # Use our own versions of develop and egg_info to ensure that build_src is
    # handled appropriately.
    from numpy.distutils.command import develop, egg_info
    my_cmdclass['bdist_egg'] = bdist_egg.bdist_egg
    my_cmdclass['develop'] = develop.develop
    my_cmdclass['easy_install'] = easy_install.easy_install
    my_cmdclass['egg_info'] = egg_info.egg_info


def get_distribution(always=False):
    dist = distutils.core._setup_distribution
    # XXX Hack to get numpy installable with easy_install.
    # The problem is easy_install runs it's own setup(), which
    # sets up distutils.core._setup_distribution. However,
    # when our setup() runs, that gets overwritten and lost.
    # We can't use isinstance, as the DistributionWithoutHelpCommands
    # class is local to a function in setuptools.command.easy_install
    if dist is not None and \
            'DistributionWithoutHelpCommands' in repr(dist):
        #raise NotImplementedError("setuptools not supported yet for numpy.scons branch")
        dist = None
    if always and dist is None:
        dist = CustomDistribution()
    return dist


def setup(**attr):
    if len(sys.argv)<=1 and not attr.get('script_args',[]):
        from numpy.distutils.interactive import interactive_sys_argv
        import atexit
        atexit.register(_exit_interactive_session)
        sys.argv[:] = interactive_sys_argv(sys.argv)
        if len(sys.argv)>1:
            return setup(**attr)

    cmdclass = my_cmdclass.copy()

    new_attr = attr.copy()
    if 'cmdclass' in new_attr:
        cmdclass.update(new_attr['cmdclass'])
    new_attr['cmdclass'] = cmdclass

    if 'configuration' in new_attr:
        # To avoid calling configuration if there are any errors
        # or help request in command in the line.
        configuration = new_attr.pop('configuration')

        old_dist = distutils.core._setup_distribution
        old_stop = distutils.core._setup_stop_after
        distutils.core._setup_distribution = None
        distutils.core._setup_stop_after = "commandline"
        try:
            dist = setup(**new_attr)
        finally:
            distutils.core._setup_distribution = old_dist
            distutils.core._setup_stop_after = old_stop
        if dist.help or not _command_line_ok():
            # probably displayed help, skip running any commands
            return dist

        # create setup dictionary and append to new_attr
        config = configuration()
        if hasattr(config,'todict'):
            config = config.todict()
        _dict_append(new_attr, **config)

    # Move extension source libraries to libraries
    libraries = []
    for ext in new_attr.get('ext_modules',[]):
        new_libraries = []
        for item in ext.libraries:
            #if isinstance(item, unicode): ## unicode here screws up, convert it
            #    item = ''.join(chr(ord(c)) for c in item.decode('ascii'))
            if is_sequence(item):
                lib_name, build_info = item
                _check_append_ext_library(libraries, item)
                new_libraries.append(lib_name)
            elif is_string(item):
                new_libraries.append(item)
            else:
                raise TypeError("invalid description of extension module "
                                "library %r" % (item,))
        ext.libraries = new_libraries
    if libraries:
        if 'libraries' not in new_attr:
            new_attr['libraries'] = []
        for item in libraries:
            _check_append_library(new_attr['libraries'], item)

    # sources in ext_modules or libraries may contain header files
    if ('ext_modules' in new_attr or 'libraries' in new_attr) \
       and 'headers' not in new_attr:
        new_attr['headers'] = []

    # Use our custom NumpyDistribution class instead of distutils' one
    new_attr['distclass'] = CustomDistribution

    return old_setup(**new_attr)
