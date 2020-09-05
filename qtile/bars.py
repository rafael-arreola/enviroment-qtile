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
    widget.Mpris2(background='253253', name='spotify',
                    stop_pause_text='▶', scroll_chars=None,
                    display_metadata=['xesam:title', 'xesam:artist'],
                    objname="org.mpris.MediaPlayer2.spotify"),
    widget.Sep(linewidth=2, size_percent=100, padding=12),
    widget.Prompt(),
    widget.Memory(
        mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e htop')},
        padding = 5
    ),
    widget.Volume(
        padding = 5
    ),
    widget.WindowName(),
    widget.Systray(),
    widget.Sep(**soft_sep),
    widget.Sep(**soft_sep),
    widget.Clock(format='%d/%m/%Y %I:%M %p'),
], 30)


secondary_bar = bar.Bar([
    widget.GroupBox(
        visible_groups=["WWWW","DB"]
    ),
    widget.WindowName(),
    widget.Clock(format='%d/%m/%Y %I:%M %p'),
    widget.QuickExit(),
], 24,)