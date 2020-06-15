# The outer shell for PyCalendar

from calendar_functions import Display, Calendar, Spot
import curses
import datetime
import os

# Create a calendar
calendar = Calendar()

# Create a display
display = Display(calendar)

def main_wrapper(screen, display):
    screen.border(0)
    
    display.main(screen)

    current_spot = display.spots[str(display.date.day)]
    
    while True:
        # set the current spot to blink
        screen.addstr(current_spot.curses_locs[0][0],
                      current_spot.curses_locs[0][1],
                      current_spot.name,
                      current_spot.fmt + curses.A_BLINK)

        # save the previous spot information
        prev_spot = Spot(current_spot.name,
                         current_spot.curses_locs,
                         current_spot.choose,
                         current_spot.up,
                         current_spot.down,
                         current_spot.left,
                         current_spot.right,
                         current_spot.fmt)

        # stay in this loop till the user presses 'q'
        ch = screen.getch()
        if ch == ord('q'):
            break

        #down: 258 up: 259 left: 260 right: 261
        elif ch == 258:
            if current_spot.down is not None:
                current_spot = current_spot.down
                screen.addstr(prev_spot.curses_locs[0][0],
                              prev_spot.curses_locs[0][1],
                              prev_spot.name,
                              prev_spot.fmt)
        elif ch == 259:
            if current_spot.up is not None:
                current_spot = current_spot.up
                screen.addstr(prev_spot.curses_locs[0][0],
                              prev_spot.curses_locs[0][1],
                              prev_spot.name,
                              prev_spot.fmt)
        elif ch == 260:
            if current_spot.left is not None:
                current_spot = current_spot.left
                screen.addstr(prev_spot.curses_locs[0][0],
                              prev_spot.curses_locs[0][1],
                              prev_spot.name,
                              prev_spot.fmt)
        elif ch == 261:
            if current_spot.right is not None:
                current_spot = current_spot.right
                screen.addstr(prev_spot.curses_locs[0][0],
                              prev_spot.curses_locs[0][1],
                              prev_spot.name,
                              prev_spot.fmt)

        # enter button pressed
        elif ch == 10:
            if current_spot.choose is not None:
                exec("display." + current_spot.choose)
            else:
                pass

        # Update the date to reflect the new spot
        if current_spot.name.strip().isdigit():
            display.update_date(datetime.date(display.date.year,
                                              display.date.month,
                                              int(current_spot.name.strip())))
            display.refresh()
            
    # After ending, save events
    display.action_quit()

    return

curses.wrapper(main_wrapper, display)


        
