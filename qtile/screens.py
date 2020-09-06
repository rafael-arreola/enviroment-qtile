from libqtile.config import Screen

from bars import main_bar, secondary_bar

main_screen   = Screen(bottom=main_bar)
second_screen = Screen(bottom=secondary_bar)

screens = [
    main_screen, 
    second_screen
]