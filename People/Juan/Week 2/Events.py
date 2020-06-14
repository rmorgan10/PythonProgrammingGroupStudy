"""
File to hold different kinds of event classes
"""
from datetime import date, datetime, time
from typing import TypeVar
import os
from CalendarErrors import MainError
from Calendar import Calendar
DateTypes = TypeVar("DateTypes", date, datetime)


class Event:
	"""
	Base class for all events

	Attributes:
		date_of_event : date or datetime object holding information about when the event is
			happening
		name : brief, descriptive name for the event
		description : more detailed description of the event, if desired
		time : time the event will occur if not specified by date_of_event and if desired
	"""
	def __init__(
			self,
			date_of_event: DateTypes,
			name: str,
			description: str = None,
			time_of_event: time = None
	):

		self.date_of_event = date_of_event
		self.name = name
		self.description = "" if description is None else description

		# This bit is to keep pycharm from underlining things for me
		self.year = None
		self.month = None
		self.day = None
		self.update_date(date_of_event)
		# set the time of the event based on what is passed to the constructor
		if isinstance(date_of_event, datetime):
			self.time = self.date_of_event.time()
		elif isinstance(date_of_event, date):  # This is true for the above case
			if time_of_event is not None:
				if isinstance(time_of_event, time):
					self.time = time_of_event
				else:
					self.time = self.prompt_user_time()
			else:
				self.time = time(0)  # Assume it lasts all day, therefore time of event is midnight
		else:
			raise ValueError(f"{type(date_of_event)} is not a valid type for date_of_event")

	def modify(self):
		"""
		Modifies this event by prompting the user to enter a command indicating which part of the
		event is to be modified and what value should replace that
		"""

		info_str = f"""
Let's modify the event below.
{self}		
To return to the main menu enter Q,
To change the name enter N,
To change the description enter L
To change date enter D,
To change the time enter T, 
What would you like to do?:
"""
		commands = [
			"Q",
			"N",
			"L",
			"D",
			"T"
		]
		# TODO make this function work inside event class
		# TODO: Implement T
		# Get the user's command
		cmd = ""
		while True:
			mod_input = input(info_str)
			try:
				cmd = mod_input[0].upper()
				assert cmd in commands
			except (IndexError, AssertionError):
				print(f"""{mod_input} is not a valid command, should lead with one
of the following (case insensitive): {commands}""")
				continue
			else:
				break

		# Break out the user's command
		if cmd == "Q":
			raise MainError
		elif cmd == "N":
			self.name = input(f"What is {self.name}'s new name?")
		elif cmd == "L":
			self.description = input(f"What is {self.name}'s new description?")
		elif cmd == "D":
			self.update_date(Calendar.prompt_date(f"What is {self.name}'s new date?"))
		elif cmd == "T":
			self.update_time(self.prompt_user_time(f"What is {self.name}'s new time?"))
		else:
			print("You really shouldn't be here")

	def update_time(self, new_time: time):
		"""
		Excessively simple function but one that can be overwritten
		Args:
			new_time : new time for this event
		"""
		self.time = new_time

	def update_date(self, new_date: DateTypes):
		"""
		Sets important class parameters based on the new_date provided.
		Args:
			new_date : new date for this event
		"""
		self.date_of_event = new_date
		self.year = self.date_of_event.year
		self.month = self.date_of_event.month
		self.day = self.date_of_event.day


	def __repr__(self):  # TODO: overwrite this method to provide nice description of event
		pass