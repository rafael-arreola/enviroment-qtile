from libqtile.config import Group, Match

group_names = [
    ("DEV", {'layout': 'max', 'matches': [Match(wm_class=["code", "vscode"])] }),
    ("TERM", {'layout': 'monadtall', 'matches': [Match(wm_class=["Alacritty"])] }),
    ("CHAT", {'layout': 'max', 'matches': [Match(wm_class=["Rambox"])] }),
    ("WWW", {'layout': 'max', 'matches': [Match(wm_class=["Firefox", "firefox"])] }),
    ("DB", {'layout': 'max', 'matches': [Match(wm_class=["datagrip"])] }),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]