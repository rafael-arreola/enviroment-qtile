import subprocess
from time import time
from pathlib import Path

from libqtile.config import Key
from libqtile.command import lazy

from groups import group_names

mod = "mod4"
alt = 'mod1'
BROWSER = 'firefox'
TERM_EMULATOR = 'alacritty'

def screenshot(save=True, copy=True):
    def f(qtile):
        path = Path.home() / 'Pictures'
        path /= f'screenshot_{str(int(time() * 100))}.png'
        shot = subprocess.run(['maim'], stdout=subprocess.PIPE)

        if save:
            with open(path, 'wb') as sc:
                sc.write(shot.stdout)

        if copy:
            subprocess.run(['xclip', '-selection', 'clipboard', '-t',
                            'image/png'], input=shot.stdout)
    return f

def cycle_workspaces(direction, move_window):
    def _inner(qtile):
        current = qtile.groups.index(qtile.current_group)
        destination = (current + direction) % len(group_names)
        if move_window:
            qtile.current_window.togroup(qtile.groups[destination].name)
        qtile.groups[destination].cmd_toscreen()
    return _inner


next_workspace = lazy.function(cycle_workspaces(direction=1, move_window=False))
previous_workspace = lazy.function(cycle_workspaces(direction=-1, move_window=False))
to_next_workspace = lazy.function(cycle_workspaces(direction=1, move_window=True))
to_previous_workspace = lazy.function(cycle_workspaces(direction=-1, move_window=True))


keys = [
    Key([mod], 'k',     lazy.layout.down()),
    Key([mod], 'i',     lazy.layout.up()),
    Key([mod], 'space', lazy.layout.next()),
    Key([mod, 'control'], 'k',  lazy.layout.shuffle_down()),
    Key([mod, 'control'], 'i',  lazy.layout.shuffle_up()),
    Key([mod, 'shift'],   'j',  lazy.layout.client_to_previous()),
    Key([mod, 'shift'],   'l',  lazy.layout.client_to_next()),
    Key([mod, 'shift'], 'space', lazy.layout.rotate()),
    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),

    Key([mod, alt], 'Left',     lazy.to_screen(1)),
    Key([mod, alt], 'Right',     lazy.to_screen(2)),

    
    Key([mod], 'Tab',   lazy.next_layout()),
    Key([mod], 'w',     lazy.window.kill()),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="App Launcher"),
    Key([mod], "r", lazy.spawn("rofi -show run"),  desc="run"),

    #Workspaces support
    Key(["control", alt], "Right", next_workspace),
    Key(["control", alt], "Left", previous_workspace),
    Key(["control", alt, "shift"], "Right", to_next_workspace),
    Key(["control", alt, "shift"], "Left", to_previous_workspace),

    # Base 
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),

    # Screen
    Key([], 'F7', lazy.spawn('xset dpms force off')),

    # Audio
    Key([], 'XF86AudioMute', lazy.spawn('ponymix toggle')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('ponymix increase 5')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('ponymix decrease 5')),

    # Apps
    Key([mod], 'Return', lazy.spawn(TERM_EMULATOR)),
    Key([mod],  'b',     lazy.spawn(BROWSER)),

    # Screenshots
    Key([], 'Print', lazy.function(screenshot())),
    Key(['control'], 'Print', lazy.spawn('deepin-screenshot'))
]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))