# Objects used in my_calendar.py

import curses
import datetime
import os
import pandas as pd
import sys
from benedict import benedict

class Event():
    """
    The Event Class. Stores event info as attributes.
    """
    def __init__(self, name, date, time, duration, location, description):
        """
        Store event properties as attributes.
        
        :param name: str, title of event
        :param date: datetime.date, date of event
        :param time: datetime.time, time of event in US Central Time
        :param duration: datetime.timedelta, a length of time for the event to last
        :param location: str, location of event
        :param description: str, description of event
        """
        # Store main attributes
        self.name = name
        self.date = date
        self.time = time
        self.duration = duration
        self.location = location
        self.description = description

        # Store helper attributes
        self.year = str(date.year)
        self.month = str(date.month)
        self.day = str(date.day)
        self.hour = str(time.hour)
        self.minute = str(time.minute)
        self.end_date = date + duration
        self.end_time = time + duration

        return

class Calendar():
    """
    The Calendar Class. Tracks all events while sorting them by date.
    """
    def __init__(self):
        """
        Initialize the event storage data structure (nested dict).
        Year: dict of months
        └── Month: dict of days
            └── Day: list of events

        Also utilize the benedict module for faster searching.
        """
        # Start an empty calendar
        self.event_db = benedict({}, keypath_separator='.')
        
        # If existing events are in the database, load them in
        if os.path.exists('calendar_db.csv'):
            self._load_events()
        
        return

    def _has_event_on_date(self, year, month, day):
        """
        Check if the calendar has an event on the specified day.

        :param year: str, year of event (integer value)
        :param month: str, month of event (integer value)
        :param day: str, day of event (integer value)
        :return: has_event: bool, true if calendar has an event
        """
        if year in self.event_db.keys():
            if year + '.' + month in self.event_df.keypaths():
                if year + '.' + month + '.' + day in self.event_df.keypaths():
                    return True
        return False
    
    def add_event(self, event):
        """
        Add an event to the calendar.

        :param event: event, an instance of the Event class
        """
        if self._has_event_on_date(event.year, event.month, event.day):
            # If an entry for this day exists, just append to list
            self.event_db[event.year + '.' + event.month + '.' + event.day].append(event)

        else:
            if event.year not in self.event_db.keys():
                # No entries for year, so add event at year level
                self.event_db[event.year] = {event.month : {event.day : [event]}}

            elif event_year + '.' + event.month not in self.event_db.keypaths():
                # No entries for month, so add event at month level
                self.event_db[event.year + '.' + event.month] = {event.day : [event]}

            elif event_year + '.' + event.month + '.' + event.day not in self.event_db.keypaths():
                # No entries for day so add event at day level
                self.event_db[event.year + '.' + event.month + '.' + event.day] = [event]
        
        return

    def remove_event(self, event):
        """
        Remove an event from the calendar.

        :param event: event, an instance of the Event class 
        """
        # Find the index of the event in the list of events on that day
        for index, ev in self.event_db[event.year + '.' + event.month + '.' + event.day]:
            if ev.name == event.name:
                break

        # Delete the event
        del self.event_db[event.year + '.' + event.month + '.' + event.day][index]

        # clean up self.event_db if we are left with an empty list
        if len(self.event_db[event.year + '.' + event.month + '.' + event.day]) == 0:
            # if there are no more events that year, delete the whole year
            if len([x for x in event_db.keypaths() if x.find(event.year + '.') != -1]) < 2:
                del event_db[event.year]
            # if there are no more events that month, delete the whole month
            elif len([x for x in event_db.keypaths() if x.find(event.year + '.' + event.month + '.') != -1]) < 2:
                del event_db[event.year + '.' + event.month]
            # if there are no more events that day, delete the whole day
            elif len([x for x in event_db.keypaths() if x.find(event.year + '.' + event.month + '.' + event.day) != -1]) < 2:
                del event_db[event.year + '.' + event.month + '.' + event.day]

        return

    def edit_event(self, event, name=None, date=None, time=None, duration=None, location=None, description=None):
        """
        Edit an existing event. Delete existing event and add new one. If an 
        argument is not passed, the exiting value is used
        
        :param event: event, the existing event instance
        :param name: str, title of event
        :param date: datetime, date of event 
        :param time: datetime, time of event in US Central Time
        :param duration: timedelta, a length of time for the event to last  
        :param location: str, location of event 
        :param description: str, description of event  
        """
        # Get existing information if it will not be changed
        if name is None: name = event.name.copy()
        if date is None: date = event.date.copy()
        if time is None: time = event.time.copy()
        if duration is None: duration = event.duration.copy()
        if location is None: location = event.location.copy()
        if description is None: description = event.description.copy()

        # Delete old event
        self.remove_event(event)

        # Add new event
        new_event = Event(name, date, time, duration, location, description)
        self.add_event(new_event)

        return
                
    def _load_events(self):
        """
        Read events from calendar_db.csv, create Event instances, add
        them to self.event_db
        """
        df = pd.read_csv("calendar_db.csv")

        for index, row in df.iterrows():
            event = Event(row['NAME'],
                          row['DATE'],
                          row['TIME'],
                          row['DURATION'],
                          row['LOCATION'],
                          row['DESCRIPTION'])

            self.add_event(event)

        return

    def _save_events(self):
        """
        Write all events in event_db to calendar_db.csv.
        """
        out_data = []
        out_cols = ['NAME', 'DATE', 'TIME', 'DURATION', 'LOCATION', 'DESCRIPTION']
        for year in self.event_db.keys():
            for month in self.event_db[year].keys():
                for day in self.event_db[year + '.' + month].keys():
                    for event in self.event_db[year + '.' + month + '.' + day]:
                        out_data.append([event.name,
                                         event.date,
                                         event.time,
                                         event.duration,
                                         event.location,
                                         event.description])

        out_df = pd.DataFrame(data=out_data, columns=out_cols)
        out_df.to_csv('calendar_db.csv', index=False)

        return

class Spot():
    """
    A spot on the display grid.
    """
    def __init__(self, name, curses_locs, choose, up=None, down=None, left=None, right=None, fmt=curses.A_NORMAL):
        """
        Store attributes of a Spot

        :param name: str, identifier for the location
        :param curses_locs: list, elements of tuple coordinates for curses
        :param choose: str, what to do if the Spot is selected
        :param up: Spot, the Spot to move to if up is pressed
        :param down: Spot, the Spot to move to if down is pressed 
        :param left: Spot, the Spot to move to if left is pressed 
        :param right: Spot, the Spot to move to if right is pressed
        :param fmt: int, the curses bitmask for formatting
        """
        self.name = name
        self.curses_locs = curses_locs
        self.choose = choose
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.fmt = fmt

        return

    def set_up(self, spot):
        """
        Set the spot accessed by the up arrow from present spot
        
        :param spot: Spot, the Spot instance above self
        """
        self.up = spot
        spot.down = self
        return

    def set_down(self, spot):
        """
        Set the spot accessed by the down arrow from present spot

        :param spot: Spot, the Spot instance below self
        """
        self.down = spot
        spot.up = self
        return

    def set_left(self, spot):
        """
        Set the spot accessed by the left arrow from present spot
        
        :param spot: Spot, the Spot instance left of self
        """
        self.left = spot
        spot.right = self
        return

    def set_right(self, spot):
        """
        Set the spot accessed by the right arrow from present spot

        :param spot: Spot, the Spot instance left of self   
        """
        self.right = spot
        spot.left = self
        return
    
class Display():
    """
    The Display Class. Interacts with the user.
    """
    def __init__(self, calendar):
        """
        Instantiates a display.

        :param calendar: calendar, an instance of the Calendar class
        """
        self.calendar = calendar
        self.date = datetime.date.today()
        self.today = datetime.date.today()
        self._get_week()
        self._build_month_grid()

        self.month_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                          5: 'May', 6: 'June', 7: 'July', 8: 'August',
                          9: 'September', 10: 'October', 11: 'November',
                          12: 'December'}
        self.weekday_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday',
                            3: 'Wednesday', 4: 'Thursday', 5: 'Friday',
                            6: 'Saturday'}

        return

    def refresh(self):
        self._get_week()
        self._build_month_grid()
        self.main(self.screen)
        return
    
    def update_date(self, date):
        """
        Store the current date as a datetime object.

        :param date: datetime, the new date to set the calendar to.
        """
        self.date = date
        return
    
    def _get_week(self):
        """
        Determine the day of the previous sunday. If previous month,
        use negative numbers.
        """
        # Switch convention to have Sunday = 0
        self.weekday = 0 if self.date.weekday() == 6 else self.date.weekday() + 1

        return

    def main(self, screen):
        self.screen = screen

        """
        Run the display by handling user input
        """
        # Display a header
        self.screen.addstr(1, 20, '{weekday} {month} {day}, {year}           '.format(weekday=self.weekday_map[self.weekday],
                                                                      month=self.month_map[self.date.month],
                                                                      day=self.date.day,
                                                                      year=self.date.year), curses.A_BOLD)
        self.screen.addstr(2, 1, '-' * 65, curses.A_NORMAL)

        # Display a grid layout of the month on the left side
        self.screen.addstr(4, 8, '{month} {year}'.format(month=self.month_map[self.date.month][0:3],
                                                    year=self.date.year), curses.A_BOLD)
        self.screen.addstr(5, 3, 'S  M  T  W  T  F  S', curses.A_DIM)

        temp_date = self.date - datetime.timedelta(days=self.date.day) + datetime.timedelta(days=1)
        while temp_date.month == self.date.month:
            temp_day = str(temp_date.day)
            temp_y, temp_x = self.curses_locs[temp_date.day]
            fmt = curses.A_UNDERLINE if self.calendar._has_event_on_date(str(temp_date.year), str(temp_date.month), temp_day) else curses.A_NORMAL
            self.screen.addstr(temp_y, temp_x, ' ' + temp_day if len(temp_day) == 1 else temp_day, fmt)
            temp_date += datetime.timedelta(days=1)

        # Highlight today's day on calendar if it is the current month and year
        if self.date.month == self.today.month and self.date.year == self.today.year:
            current_y, current_x = self.curses_locs[self.today.day]
            current_idx1, current_idx2 = self.grid_locs[self.today.day]
            if self.calendar._has_event_on_date(str(self.today.year), str(self.today.month), str(self.today.day)):
                self.screen.addstr(current_y, current_x, self.grid[current_idx1][current_idx2], curses.A_BOLD + curses.A_UNDERLINE)
            else:
                self.screen.addstr(current_y, current_x, self.grid[current_idx1][current_idx2], curses.A_BOLD)

        # Display a vertical line between events and month panels
        for i in range(4, 12):
            self.screen.addstr(i, 23, '|', curses.A_NORMAL)
        
        # Display all events on that day on the right side
        self.screen.addstr(4, 27, 'Events', curses.A_UNDERLINE)
        if self.calendar._has_event_on_date(str(self.date.year), str(self.date.month), str(self.date.day)):
            # Display all events on that day
            events_y = 5
            events = self.calendar[str(self.date.year)][str(self.date.month)][str(self.date.day)]
            ordered_events = sorted(events, key=self._order_events)
            for event in ordered_events:
                self.screen.addstr(events_y, 25, str(event.hour) + ':' + str(event.minute) + '\t' + event.name, curses.A_NORMAL)
                events_y += 1
        else:
            self.screen.addstr(7, 25, 'No events to display.' , curses.A_NORMAL)    

        # Display menu
        self.screen.addstr(4, 2, '<<', curses.A_UNDERLINE)
        self.screen.addstr(4, 5, '<', curses.A_UNDERLINE)
        self.screen.addstr(4, 18, '>', curses.A_UNDERLINE)
        self.screen.addstr(4, 20, '>>', curses.A_UNDERLINE)

        # Make the current day standout
        current_y, current_x = self.curses_locs[self.date.day]
        current_idx1, current_idx2 = self.grid_locs[self.date.day]
        fmt = curses.A_STANDOUT
        if self.date == self.today:
            fmt += curses.A_BOLD
        self.screen.addstr(current_y, current_x, self.grid[current_idx1][current_idx2], fmt)

        # Hide the cursor
        curses.curs_set(0)
        
        # Determine Buttons
        self.spots = {}
        self.spots["<<"] = Spot("<<", [(4,2), (4,3)], "action_deincrement_year()", fmt=curses.A_UNDERLINE)
        self.spots["<"] = Spot("<", [(4,5)], "action_deincrement_month()", fmt=curses.A_UNDERLINE)
        self.spots[">"] = Spot(">", [(4,18)], "action_increment_month()", fmt=curses.A_UNDERLINE)
        self.spots[">>"] = Spot(">>", [(4,20), (4,21)], "action_increment_year()", fmt=curses.A_UNDERLINE)

        for day in range(1, 32):
            try:
                left_locs = self.curses_locs[day]
                str_day = ' ' + str(day) if len(str(day)) == 1 else str(day)
                self.spots[str_day] = Spot(str_day, [left_locs, (left_locs[0], left_locs[1] + 1)], "action_select()") 
            except KeyError:
                # Triggered when we run out of days in the month
                break

        # Determine Connections
        self.spots["<<"].set_right(self.spots["<"])
        self.spots["<"].set_right(self.spots[">"])
        self.spots[">"].set_right(self.spots[">>"])

        fmt_day = lambda d: ' ' + str(d) if len(str(d)) == 1 else str(d)
        for day in range(1, 32):
            ## set right for each
            try:
                self.spots[fmt_day(day)].set_right(self.spots[fmt_day(day + 1)])
            except KeyError:
                pass

            ## set down for as many as possible
            try:
                self.spots[fmt_day(day)].set_down(self.spots[fmt_day(day + 7)])
            except KeyError:
                pass

        ## connect month/year toggles to grid
        for day in range(1, 8):
            if self.curses_locs[day][0] == 6:
                str_day = ' ' + str(day) if len(str(day)) == 1 else str(day)
                self.spots[str_day].up = self.spots["<<"]

        for name in ["<<", "<", ">", ">>"]:
            self.spots[name].down = self.spots[' 1']
                
        # Set the current spot
        #self.current_spot = self.spots[self._fmt_str(self.date.day)]
               
                                            
        """
         | << <  Jun 2020  > >> |   Events     
         │  S  M  T  W  T  F  S |              
         │     1  2  3  4  5  6 |              
         │  7  8  9 10 11 12 13 | No events to display. 
         │ 14 15 16 17 18 19 20 |                       
         │ 21 22 23 24 25 26 27 |                       
         │ 28 29 30             |                       
         │                      |

        """
        return

    def _fmt_str(self, num):
        """
        Format a calendar date to be a string of length 2

        :param num: int, a calendar date
        :return: str_num: str, a length 2 string of num
        """
        str_num = ' ' + str(num) if len(str(num)) == 1 else str(num)
        return str_num
    
    def _order_events(self, event):
        """
        Used as key function of the python 'sorted' method.

        :param event: Event, and instance of the Event class
        :return: float_date: float, essentially float(HH.MM)
        """
        return float(str(event.hour) + '.' + str(event.minute))
                            

    def _build_month_grid(self):
        """
        Fill in a grid layout of the current month. 
        Save a 7x7 list of lists as self.grid. 
        Save a dict of day: (index, index) as self.grid_locs.
        Save a dict of day: (curses_index, curses_index) as self.curese_locs.
        """
        self.grid = [[], [], [], [], [], [], []]
        self.grid_locs, self.curses_locs = {}, {}
        grid_loc_start = 6

        # Start the grid on the first day of the month
        grid_date = self.date - datetime.timedelta(days=self.date.day)	+ datetime.timedelta(days=1)

        # Fill the trailing days of the previous month with whitespace
        week_start = grid_date.weekday() + 1
        for day_num in range(week_start):
            self.grid[0].append('  ')

        # Fill in the days of the current month and store locs
        finished_month = False
        for week_num  in range(len(self.grid)):
            # If finished, fill all remaining spaces with whitespace
            if finished_month:
                while len(self.grid[week_num]) < 7:
                    self.grid[week_num].append('  ')
                
                continue

            # This will only execute if the days are not exhausted
            while len(self.grid[week_num]) < 7:
                # Add the next day to the grid while forcing length to be 2
                str_day_num = ' ' + str(grid_date.day) if len(str(grid_date.day)) == 1 else str(grid_date.day)
                self.grid[week_num].append(str_day_num)

                # Save the location of the date in the grid
                self.grid_locs[grid_date.day] = (week_num, week_start)
                self.curses_locs[grid_date.day] = (grid_loc_start + week_num, len(' '.join(self.grid[week_num])))
                week_start += 1

                # Increment the date on the grid
                grid_date = grid_date + datetime.timedelta(days=1)

                # Fill the remaining grid spaces that week with whitespace
                if grid_date.day == 1:
                    finished_month = True
                    while len(self.grid[week_num]) < 7:
                        self.grid[week_num].append('  ')
            else:
                week_start = 0

        return

    def _select_event(self):
        #TODO
        # - prompt user for event info
        # - isolate event in calendar
        return
    
    def action_select(self):
        """
        Trigger a menu of options after enter has been pressed on a calendar date
        """
        self.screen.addstr(14, 2, "What would you like to do?", curses.A_NORMAL)
        self.screen.addstr(15, 4, "a) Add an event", curses.A_NORMAL)
        if self.calendar._has_event_on_date(str(self.date.year), str(self.date.month), str(self.date.day)):
            self.screen.addstr(16, 4, "b) Remove an event", curses.A_NORMAL)
            self.screen.addstr(17, 4, "c) Edit an event", curses.A_NORMAL)
            self.screen.addstr(18, 4, "d) Go back", curses.A_NORMAL)

            ch = self.screen.getch()
            while ch not in [ord("a"), ord("b"), ord("c"), ord("d")]:
                self.screen.addstr(20, 5, "Please select one of the above options", curses.A_BOLD)
                ch = self.screen.getch()

            if ch == ord("a"):
                self.action_add_event()
            elif ch == ord("b"):
                self.action_remove_event()
            elif ch == ord("c"):
                self.action_edit_event()
            elif ch == ord("d"):
                pass
        else:
            self.screen.addstr(16, 4, "b) Go back", curses.A_NORMAL)    

            ch = self.screen.getch()
            while ch not in [ord("a"), ord("b")]:
                self.screen.addstr(18, 5, "Please select one of the above options", curses.A_BOLD)
                ch = self.screen.getch()

            if ch == ord("a"):
                self.action_add_event()
            elif ch == ord("b"):
                pass
            
        return
        
    def action_quit(self):
        """
        User has chosen to quit. Save events and termintate program.
        """
        self.calendar._save_events()
        return

    def action_add_event(self):
        """
        User has chosen to add an event. Prompt user for information
        and create an Event in the Calendar.
        """
    
        #TODO
        # - promept user for all atributes of a new event
        # - add the new event to the calendar
        
        #change date to be the date of the new event
        
        return

    def action_remove_event(self):
        #TODO
        # - call _select_event to find the event in question
        # - delete the event from the calendar
        return

    def action_edit_event(self):
        #TODO
        # - call _select_event to find the event in question
        # - edit the event from the calendar 
        return

    def action_increment_year(self):
        """
        Add 1 to the current year.
        """
        self.update_date(self.date + datetime.timedelta(days=365))
        self.refresh()
        return

    def action_deincrement_year(self):
        """
        Subtract 1 from current year.
        """
        self.update_date(self.date - datetime.timedelta(days=365))
        self.refresh()
        return

    def action_increment_month(self):
        """
        Add 1 to the current month.
        """
        self.update_date(self.date + datetime.timedelta(days=30))
        self.refresh()
        return

    def action_deincrement_month(self):
        """
        Subtract 1 from current month.
        """
        self.update_date(self.date - datetime.timedelta(days=30))
        self.refresh()
        return

    def action_increment_day(self):
        """
        Add 1 to the current day.
        """
        self.update_date(self.date + datetime.timedelta(days=1))
        self.refresh()
        return

    def action_deincrement_day(self):
        """
        Subtract 1 from current day.
        """
        self.update_date(self.date - datetime.timedelta(days=1))
        self.refresh()
        return

    def action_increment_week(self):
        """
        Add 7 to the current day.
        """
        self.update_date(self.date + datetime.timedelta(weeks=1))
        self.refresh()
        return

    def action_deincrement_week(self):
        """
        Subtract 7 from current day.
        """
        self.update_date(self.date - datetime.timedelta(weeks=1))
        self.refresh()
        return
