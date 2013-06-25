"""
GTK-based Graphical User Interface classes that extend the virtual classes
loaded from a Glade file and provide functionality to the GUI layout
"""

import sys
import os

import gui

try:
    import warnings
    ## Eliminate "PendingDeprecationWarning: The CObject type is marked Pending Deprecation in Python 2.7.  Please use capsule objects instead."
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
    import pygtk
    pygtk.require('2.0')
    import gtk
    import gobject
    warnings.resetwarnings()


    class SplashScreen(gtk.Window):
        def __init__(self, image_file, timeout=gui.SPLASH_DURATION):
            gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
            self.set_decorated(False)
            self.set_position(gtk.WIN_POS_CENTER)
            self.set_modal(True)
            image = gtk.Image()
            image.set_from_file(image_file)
            box = gtk.VBox()
            box.pack_start(image, False, False, 0)
            self.add(box)
            image.show()
            box.show()
            self.show()
            while gtk.events_pending():
                gtk.main_iteration()
            gobject.timeout_add(timeout, self.hide)
        

    ##############################

    class GTK_GUI(gui.GUI):
        def __init__(self, impl_mod, parent, resfile=None, has_log=True):
            gui.GUI.__init__(self, impl_mod, parent)

            self.resource_file = None
            if resfile:
                self.resource_file = resfile + '.glade'

            xpm_icon = os.path.join(self.app.IMAGE_DIR, self.app.key + '.xpm')
            try:
                __import__(self.implementation)
                impl = sys.modules[self.implementation]
                impl.gtkSetup(self, xpm_icon)
            except Exception, e:
                sys.stderr.write('Application ' + self.implementation +
                                 ' not enabled/available\n' + str(e) + '\n')
                sys.exit(1)
            splash = SplashScreen(os.path.join(self.app.IMAGE_DIR,
                                               'itar_warning.xpm'))

        def Run(self):
            gtk.main()

        def onExit(self, widget=None, data=None):
            gtk.main_quit()

        def onHelp(self, widget=None, data=None):
            self.helper_frame.show_all()

        def onAbout(self, widget=None, data=None):
            dialog = gtk.AboutDialog()
            dialog.set_name(self.app.name)
            dialog.set_version(self.app.version)
            dialog.set_copyright(u'Copyright © ' + self.app.copyright)
            dialog.run()
            dialog.destroy()

        def onNotice(self, txt):
            pass

        def onMessage(self, txt, tpl):
            #gtk.MessageDialog(parent, flags, type, buttons)
            pass


    ## end GTK_GUI
    ##############################

except Exception, e:
    print e
