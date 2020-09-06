from libqtile import bar, widget

soft_sep = {
    'linewidth': 2, 
    'size_percent': 70,
    'foreground': '393939', 
    'padding': 7
}


main_bar = bar.Bar([
    widget.GroupBox(
        visible_groups=["DEV","TERM", "CHAT"]
    ),
    widget.Sep(linewidth=2, size_percent=100, padding=12),
    widget.Memory(
        mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e htop')},
        padding = 5
    ),
    widget.Sep(linewidth=2, size_percent=100, padding=12),
    widget.WindowName(),
    widget.Systray(),
    widget.Volume(
        padding = 5
    ),
    widget.Sep(**soft_sep),
    widget.Clock(format='%d/%m/%Y %I:%M %p'),
    widget.Sep(**soft_sep),
    widget.QuickExit(),
], 30)


secondary_bar = bar.Bar([
    widget.GroupBox(
        visible_groups=["WWW","DB"]
    ),
    widget.WindowName(),
    widget.Clock(format='%d/%m/%Y %I:%M %p'),
    widget.QuickExit(),
], 24,)