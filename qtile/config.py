import os
import subprocess
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
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.VerticalTile(),
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
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = 'LG3D'


@hook.subscribe.startup_once
def startup_once():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])