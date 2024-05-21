from pathlib import Path
from magicgui import widgets, magicgui


def show_io_win():
    gui = widgets.Dialog(
        widgets=[
            widgets.VBox(),
        ]
    )
    gui.show(run=True)
