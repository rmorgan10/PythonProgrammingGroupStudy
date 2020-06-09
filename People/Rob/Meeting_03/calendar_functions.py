# Objects used in calendar.py

from benedict import benedict
import os
import pandas as pd

class Event():
    """
    The Event Class. Stores event info as attributes.
    """
    def __init__(self, name, date, time, duration, location, description):
        """
        Store event properties as attributes.
        
        :param name: str, title of event
        :param date: datetime, date of event
        :param time: datetime, time of event in US Central Time
        :param duration: timedelta, a length of time for the event to last
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

            elif event_year _ '.' + event.month + '.' event.day not in self.event_db.keypaths():
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
                del event_db[event.year + '.' + event.month + '.' event.day]

        return

    def edit_event(self, event, name=None, date=None, time=None, duration=None, location=None description=None):
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
        for year in event_db.keys():
            for month in event_db[year].keys():
                for day in event_db[year + '.' + month].keys():
                    for event in event_db[year + '.' + month + '.' + day]:
                        out_data.append([event.name,
                                         event.date,
                                         event.time,
                                         event.duration,
                                         event.location,
                                         event.description])

        out_df = pd.DateFrame(data=out_data, columns=out_cols)
        out_df.to_csv('calendar_db.csv')

        return


