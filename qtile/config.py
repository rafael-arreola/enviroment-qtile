# PLEASE INSTALL python-xlib rofi alacritty ponymix deepin-screenshot
import os

from libqtile import layout, hook
from libqtile.config import Group

from keys import keys 
from groups import groups 
from screens import screens 


layout_theme = {
    "border_width": 2,
    "margin": 6,
    "border_focus": "e1acff",
    "border_normal": "1D2330"
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
]


widget_defaults = {
    'font': 'Sans', 
    'fontsize': 16, 
    'padding': 3
}



dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = 'focus'

wmname = 'qtile'