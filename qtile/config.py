# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#please install python-xlib rofi alacritty maim

import os
import subprocess

from typing import List
from libqtile import bar, layout, widget, hook
from libqtile.config import Match, Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from Xlib import display as xdisplay

def cycle_workspaces(direction, move_window):
    def _inner(qtile):
        current = qtile.groups.index(qtile.current_group)
        destination = (current + direction) % len(groups)
        if move_window:
            qtile.current_window.togroup(qtile.groups[destination].name)
        qtile.groups[destination].cmd_toscreen()
    return _inner

    
mod = "mod4"
terminal = "alacritty"

next_workspace = lazy.function(cycle_workspaces(direction=1, move_window=False))
previous_workspace = lazy.function(cycle_workspaces(direction=-1, move_window=False))
to_next_workspace = lazy.function(cycle_workspaces(direction=1, move_window=True))
to_previous_workspace = lazy.function(cycle_workspaces(direction=-1, move_window=True))

keys = [
    #My settings
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="App Launcher"),
    Key([mod], "r", lazy.spawn("rofi -show run"),  desc="run"),

    #Enable Audio Keys
    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

    #Enable Screen capture 
    Key(["mod4"], "Print",          lazy.spawn("maim -u ~/Pictures/screenshot/screen_$(date +%Y-%m-%d-%T).png")),
    Key(["mod4", "shift"], "Print", lazy.spawn("maim -s ~/Pictures/screenshot/area_$(date +%Y-%m-%d-%T).png")),


    #Workspaces support

    Key(["control", "mod1"], "Right", next_workspace),
    Key(["control", "mod1"], "Left", previous_workspace),
    Key(["control", "mod1", "shift"], "Right", to_next_workspace),
    Key(["control", "mod1", "shift"], "Left", to_previous_workspace),


    #Base settings
    Key([mod], "Tab", lazy.next_layout(),       desc="Toggle between layouts"),

    Key([mod], "Down", lazy.layout.down(), desc="Move focus down in stack pane"),
    Key([mod], "Up", lazy.layout.up(),   desc="Move focus up in stack pane"),

    Key([mod, "control"], "k", lazy.layout.shuffle_down(),    desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),      desc="Move window up in current stack "),
    Key([mod], "space", lazy.layout.next(),                   desc="Switch window focus to other pane(s) of stack"),
    Key([mod, "shift"], "space", lazy.layout.rotate(),        desc="Swap panes of split stack"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal),             desc="Launch terminal"),

    Key([mod], "w", lazy.window.kill(),         desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(),  desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
]

group_names = [("DEV", {'layout': 'monadtall'}),
               ("TERM", {'layout': 'monadtall'}),
               ("CHAT", {'layout': 'monadtall'}),
               ("WWW", {'layout': 'monadtall'}),
               ("DB", {'layout': 'monadtall'}),
            ]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))


layout_theme = {
    "border_width": 2,
    "margin": 6,
    "border_focus": "e1acff",
    "border_normal": "1D2330"
}


layouts = [
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    #layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(num_stacks=2),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def get_num_monitors():
    num_monitors = 0
    try:
        display = xdisplay.Display()
        screen = display.screen()
        resources = screen.root.xrandr_get_screen_resources()

        for output in resources.outputs:
            monitor = display.xrandr_get_output_info(output, resources.config_timestamp)
            preferred = False
            
            if hasattr(monitor, "preferred"):
                preferred = monitor.preferred
            elif hasattr(monitor, "num_preferred"):
                preferred = monitor.num_preferred
            if prefeerred:
                num_monitors += 1
    except Exception as e:
        return 1
    else:
        return num_monitors

num_of_monitors = get_num_monitors()
screens= [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Memory(
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e htop')},
                       padding = 5
                ),
                widget.Volume(
                       padding = 5
                ),
                widget.Clock(format='%d/%m/%Y %I:%M %p'),
                widget.QuickExit(),
            ],
            24,
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.WindowName(),
                widget.Clock(format='%d/%m/%Y %I:%M %p'),
                widget.QuickExit(),
            ], 
            24,
        )
    )
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = [] 
main = None 
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
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
    {'wname': 'File Operations'},  # mate-desktop filer
    
    
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

wmname = "LG3D"