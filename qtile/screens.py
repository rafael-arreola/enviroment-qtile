from libqtile.config import Screen

from bars import main_bar, secondary_bar

main_screen   = Screen(top=main_bar)
second_screen = Screen(top=secondary_bar)

screens = [
    main_screen, 
    second_screen
]