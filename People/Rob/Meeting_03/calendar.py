# The outer shell for PyCalendar

from calendar_functions import Display, Calendar
import os

# Create a calendar
calendar = Calendar()

# Create a display
display = Display(calendar)

# Start by displaying the month view
os.system('clear')
display.action_view_month()

# Interact with user in a while loop
while True:

    # Show the user the menu
    """
    a) view next year  b) view previous year  c) view current month 
    d) view next month  e) view previous month  f) view current day
    g) view next day  h) view previoius day  i) view current week
    j) view next week  k) view previous week 
    l) add an event  m) remove an event  n) edit an event
    o) view event details  q) quit
    """
    user_action = menu()

    # Act based on the user choice
    if user_action == 'a':
        display.action_increment_year()
        display.action_view_month()

    elif user_action == 'b':
        display.action_deincrement_year()
        display.action_view_month()

    elif user_action == 'c':
        display.action_view_month()

    elif user_action == 'd':
        display.action_increment_month()
        display.action_view_month()

    elif user_action == 'e':
        display.action_deincrement_month()
        display.action_view_month()

    elif user_action == 'f':
        display.action_view_day()

    elif user_action == 'g':
        display.action_increment_day()
        display.action_view_day()

    elif user_action == 'h':
        display.action_deincrement_day()
        display.action_view_day()

    elif user_action == 'i':
        display.action_view_week()

    elif user_action == 'j':
        display.action_increment_week()
        display.action_view_week()

    elif user_action == 'k':
        display.action_deincrement_week()
        display.action_view_week()

    elif user_action == 'l':
        display.action_add_event()
        display.action_view_day()

    elif user_action == 'm':
        display.action_remove_event()
        display.action_view_day()

    elif user_action == 'n':
        display.action_edit_event()
        display.action_view_day()

    elif user_action == 'o':
        display.action_print_event_details()

    elif user_action == 'q':
        display.action_quit()
        
