
class __OneTimeCustomException(Exception):
    pass


try:
    try:
        import pyjd
        if not pyjd.is_desktop:
            raise __OneTimeCustomException('Compiling with pyjs.')
    except ImportError:
        pass

    ## WxPython
    # FIXME wx ui objects

    from datetime.datetime import strptime
    from flex_ui import FlexUI, multiline_text
    UserInterface = FlexUI

except __OneTimeCustomException, e:
    ## Pyjamas
    from pyjamas import Window
    from pyjamas.ui.RootPanel import RootPanel
    from pyjamas.ui.SimplePanel import SimplePanel
    from pyjamas.ui.DecoratorPanel import DecoratedTabPanel
    from pyjamas.ui.DecoratorPanel import DecoratorPanel
    from pyjamas.ui.DecoratorPanel import DecoratorTitledPanel
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.VerticalPanel import VerticalPanel
    from pyjamas.ui.HTML import HTML
    from pyjamas.ui.Button import Button
    from pyjamas.ui.RadioButton import RadioButton
    from pyjamas.ui.FlexTable import FlexTable
    from pyjamas.ui.Label import Label
    from pyjamas.ui.Image import Image
    from pyjamas.ui.CheckBox import CheckBox
    from pyjamas.ui.TextArea import TextArea
    from pyjamas.ui.TextBox import TextBox
    from pyjamas.ui.Calendar import DateField
    from pyjamas.ui.Calendar import Calendar
    from pyjamas.ui import HasAlignment

    try:
        import gchartplot as plotter
    except:
        try:
            import raphaelplot as plotter
        except:
            raise ImportError('No plotting modules available')

    from web_ui import WebUI, strptime, multiline_text
    UserInterface = WebUI
