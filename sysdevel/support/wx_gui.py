"""
WX-based Graphical User Interface classes that extend the virtual classes
loaded from an XRC file and provide functionality to the GUI layout
"""

import sys
import os
import platform

import events
import gui

try:
    import warnings
    ## Eliminate "UserWarning: wxPython/wxWidgets release number mismatch"
    warnings.filterwarnings("ignore", category=UserWarning)
    import wx
    import wx.xrc as xrc
    warnings.resetwarnings()
    import wx_bmptoggle

    ##############################

    class XrcEvtHandler(wx.EvtHandler):
        """
        Wrapper for wxPython XRC objects
        See http://wiki.wxpython.org/UsingXmlResources
        """
        def __init__(self, other):
            self.this = other.this
            del other.this
            self.thisown = 1
            if hasattr(self, '_setOORInfo'):
                self._setOORInfo(self)
            if hasattr(self, '_setCallbackInfo'):
                self._setCallbackInfo(self, self.__class__)


    class XrcFrame(wx.Frame, XrcEvtHandler):
        def __init__(self, other):
            XrcEvtHandler.__init__(self, other)


    class XrcDialog(wx.Dialog, XrcEvtHandler):
        def __init__(self, other):
            XrcEvtHandler.__init__(self, other)


    ##############################
    ##############################

    class WX_GUI(gui.GUI, wx.App):
        def __init__(self, impl_mod, parent, resfile=None, has_log=True):
            gui.GUI.__init__(self)

            bmptoggle.initialize(self.app.IMAGE_DIR)
            self.resource_file = None
            if resfile:
                self.resource_file = resfile + '.xrc'
            wx.App.__init__(self, redirect=(not has_log))


        def OnInit(self):
            self.resource = xrc.XmlResource(self.resource_file)
            self.resource.InsertHandler(
                wx_bmptoggle.BitmapToggleButtonXmlHandler())
            wx.InitAllImageHandlers()
            xpm_icon = os.path.join(self.app.IMAGE_DIR, self.app.key + '.xpm')
            try:
                __import__(self.implementation)
                impl = sys.modules[self.implementation]
                impl.wxSetup(self, xpm_icon)
            except Exception, e:
                sys.stderr.write('Application ' + self.implementation +
                                 ' not enabled/available\n' + str(e) + '\n')
                sys.exit(1)

            image = wx.Image(os.path.join(self.app.IMAGE_DIR,
                                          "itar_warning.xpm"),
                             wx.BITMAP_TYPE_XPM)
            bitmap = image.ConvertToBitmap()
            splash = wx.SplashScreen(bitmap,
                                     wx.SPLASH_CENTRE_ON_PARENT |
                                     wx.SPLASH_TIMEOUT, gui.SPLASH_DURATION,
                                     self.main_frame, wx.ID_ANY)
            self.ShowAll()
            wx.YieldIfNeeded()
            return True

    
        def Beep(self):
            sys.stdout.write("Beep\n")
            if 'windows' in platform.system().lower():
                wx.Bell()
            else:
                sys.stdout.write(chr(7))
                sys.stdout.flush()


        def Run(self):
            self.app.InitGUI()
            self.MainLoop()


        def onExit(self):
            self.main_frame.Close()


        def onAbout(self, event):
            wx.MessageBox(self.app.name + ' version ' + self.app.version +
                          '\n' + u'Copyright © ' + self.app.copyright,
                          'About ' + self.app.short_name)


        def onNotice(self, txt):
            self.main_frame.statusbarOneLiner(txt)


        def onMessage(self, txt, tpl):
            result = False
            idx = txt.find('|')
            fn = tpl[0]
            general_style = tpl[1]
            specific_style = 0
            if general_style & events.OK:
                specific_style |= wx.OK
            elif general_style & events.CANCEL:
                specific_style |= wx.CANCEL
            elif general_style & events.INFORMATION:
                specific_style |= wx.ICON_INFORMATION
            elif general_style & events.WARNING:
                specific_style |= wx.ICON_EXCLAMATION
            elif general_style & events.QUESTION:
                specific_style |= wx.ICON_QUESTION
            elif general_style & events.ERROR:
                specific_style |= wx.ICON_ERROR
            dialog = wx.MessageDialog(self.main_frame,
                                      txt[idx + 1:], txt[:idx],
                                      style = specific_style)
            if dialog.ShowModal() == wx.ID_OK:
                result = True
            dialog.Destroy()
            if fn != None:
                fn(result)



        def SetText(self, textctl, txt):
            if textctl == None:
                raise Exception("Attempting to write to an unknown control")
            textctl.Clear()
            textctl.AppendText(txt)


        def AppendText(self, textctl, txt):
            if textctl == None:
                raise Exception("Attempting to append to an unknown control")
            textctl.AppendText(txt)


        def Toggle(self, btn):
            state = btn.GetValue()
            btn.SetValue(not state)


        def GetText(self, textctl):
            if textctl == None:
                raise Exception("Attempting to read from an unknown control")
            return textctl.GetValue()


    ## end WX_GUI
    ##############################

except Exception, e:
    print e
