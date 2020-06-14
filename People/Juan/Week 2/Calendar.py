#!/usr/bin/env python3

from typing import List, Dict
from datetime import date
from calendar import monthrange
import os
from CalendarErrors import BreakoutError, MainError
from Prompt import prompt_user_date, parse_user_date

"""
Should print a calendar to the terminal/console output and prompt the user to
input some number of possible commands to:
* scroll from month to month
* make, read, and modify events on certain days
"""


class Calendar:
	"""
	Calendar class to hold info on all events in our calendar
	"""
	WEEKDAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

	# calendar commands ============================================================================
	# scroll ---------------------------------------------------------------------------------------
	SCROLL = "S"
	FORWARD = "F"
	BACKWARD = "B"
	SCROLLING = [SCROLL, FORWARD, BACKWARD]
	# Event ----------------------------------------------------------------------------------------
	NEW = "N"
	MODIFY = "C"
	READ = "R"
	EVENTS = [NEW, MODIFY, READ]
	VERB = {
		NEW : "Made",
		MODIFY : "Modified",
		READ : "Read"
	}
	# utility --------------------------------------------------------------------------------------
	QUIT = "Q"
	HELP = "H"
	UTIL = [QUIT, HELP]
	COMMANDS = SCROLLING + EVENTS + UTIL
	# indicators -----------------------------------------------------------------------------------
	DAY = "D"
	MONTH = "M"
	YEAR = "Y"
	EVENT = "E"
	INDICATORS = [DAY, MONTH, YEAR, EVENT]

	MONTHS = {
		1: "January",
		2: "February",
		3: "March",
		4: "April",
		5: "May",
		6: "June",
		7: "July",
		8: "August",
		9: "September",
		10: "October",
		11: "November",
		12: "December"
	}

	MENU_STRING = f"""
	Here's how to use the calendar!
	To scroll to the next day enter         : {FORWARD}{DAY}
	TO scroll to the previous day enter     : {BACKWARD}{DAY}
	To scroll to the the next month enter   : {FORWARD}{MONTH}
	To scroll to the previous month enter   : {BACKWARD}{MONTH}
	To scroll to the next year enter        : {FORWARD}{YEAR}
	To scroll to the previous year enter    : {BACKWARD}{YEAR}
	To scroll to a date enter               : {SCROLL} <date in yyyy/mm/dd format>
	To create an event enter                : {NEW} <date in yyyy/mm/dd format> - <name>
	To modify an event enter                : {MODIFY} <date in yyyy/mm/dd format> - <name>
	To read an event enter                  : {READ} <date in yyyy/mm/dd format> - <name>
	(To continue Press enter)
	"""

	def __init__(self):
		# Store events as a dict of names and dates
		self.events = {}  # TODO : Modify to work like Rob's code
		self.today = date.today()

	def command_loop(self):
		"""
		Main loop of the calendar. Prompts the user to input commands to modify the calendar or
		scroll around in time
		"""

		command_ms = "Welcome to the calendar, what would you like to do? \n"
		command_ms += "(Q to quit, H for help) : "
		ignores = [" ", "\n"]

		while True:
			self.print_calendar()
			user_input = input(command_ms)
			for ignore in ignores:
				user_input = user_input.replace(ignore, "")
			try:
				cmd = user_input[0].upper()
			except IndexError:
				continue
			try:
				if cmd == self.QUIT:
					break
				elif cmd == self.HELP:
					input(self.MENU_STRING)
				elif cmd in self.SCROLLING:
					self.scroll(user_input)
				elif cmd in self.EVENTS:
					self.eventing(user_input)
				else:
					input(f"{cmd} is not a valid command, please input a valid command\
					{self.MENU_STRING}")
			# MainError is just an indicator that user wants to try and input again
			except MainError:
				continue

	def scroll(self, usr_input: str):
		"""
		parse scroll commands from the user and make the correct call to print_calendar()
		Args:
			usr_input : string input by the user. Should be led by a valid scroll based command
		"""

		cmd = usr_input[0]
		if len(usr_input) > 1:
			usr_args = usr_input[1:]
		else:
			usr_args = None
		if cmd == self.SCROLL:
			calendar_date = parse_user_date(usr_args)
			self.today = calendar_date
		elif cmd == self.FORWARD or cmd == self.BACKWARD:
			# Move forward of backward
			if cmd == self.FORWARD:
				sgn = 1
			else:
				sgn = -1
			if usr_args is not None:
				usr_ind = usr_args[0].upper()
			else:
				usr_ind = usr_args
			if usr_ind == self.YEAR:
				self.today = date(self.today.year+sgn, self.today.month, self.today.day)
			elif usr_ind == self.DAY:
				self.today = date(self.today.year, self.today.month, self.today.day+sgn)
			else:  # Scroll by month is default
				self.today = date(self.today.year, self.today.month+sgn, self.today.day)

	def eventing(self, usr_input: str):
		"""
		parse event commands from the user and edit self.events dict
		Args:
			usr_input : string input by the user. Should be led by a valid event based command
		"""
		cmd = usr_input[0]
		if len(usr_input) > 1:
			usr_args = usr_input[1:]
		else:
			usr_args = None
		if usr_args is None:
			calendar_date = prompt_user_date("Lets get a date for the event")
			name = input("Give us a name for the event : ")
		else:
			usr_args = usr_args.split("-")[:2]
			calendar_date = parse_user_date(usr_args[0])
			if len(usr_args) >= 2:
				name = usr_args[2]
			else:
				name = input(f"What is the name of the event to be {Calendar.VERB[cmd]}")
		if cmd == self.NEW:
			self.events.update({name: calendar_date})
			input(f"new event created {self.print_event(name)}")
		if cmd == self.MODIFY or cmd == self.READ:
			if name in self.events.keys():  # and calendar_date == self.events[name]:
				if cmd == self.MODIFY:
					self.modify_event(name)
				else:
					input(self.print_event(name))
			else:
				input("The event you described does not exist. Back to main menu ")
				raise MainError

	# TODO : Move following two functions to Events.py
	def print_event(self, name: str):
		"""
		Returns a string describing the event in question
		"""
		ev_date = self.events[name]
		yr, mn, dy = (ev_date.year, ev_date.month, ev_date.day)
		return f"{name} : {yr} / {mn:2} / {dy:2}"

	def modify_event(self, name: str):
		"""
		Prompt user and get their input to modify the event passed in
		Args:
			name : name of event to be modified
		"""
		info_str = f"""
Let's modify the event below.
{self.print_event(name)}		
To return to the main menu enter Q,
To change date enter D,
To change name enter N,
What would you like to do?:
"""
		# Get the user's command
		cmd = ""
		while True:
			mod_input = input(info_str)
			try:
				cmd = mod_input[0]
			except IndexError:
				continue
			if cmd in ["Q", "D", "N"]:
				break
			else:
				print("Invalid command, try again.")
				continue
		if cmd == "Q":
			raise MainError
		elif cmd == "D":
			print("Lets get the new date")
			new_date = self.prompt_date()
			self.events[name] = new_date
		elif cmd == "N":
			new_name = input("What is the event's new name?")
			self.events[new_name] = self.events.pop(name)

	def print_calendar(self):
		"""
		Prints a calendar to the terminal or command for the month which contains day.
		"""
		def color_entry(message: str, txt: str = "normal", bg: str = "normal") -> str:
			"""
			turns message into a colorful version of itself
			Args:
				message : message to be beautified
				txt : string indicating color of text
				bg : string indicating color of background

			Returns:
				beautified message
			"""
			txt_colors = {
				"black": "30",
				"red": "31",
				"green": "32",
				"yellow": "33",
				"blue": "34",
				"purple": "35",
				"cyan": "36",
				"white": "37",
				"normal": 1
			}
			bg_colors = {
				"black": f"{37+10}",
				"red": f"{31 + 10}",
				"green": f"{32 + 10}",
				"yellow": f"{33 + 10}",
				"blue": f"{34 + 10}",
				"purple": f"{35 + 10}",
				"cyan": f"{36 + 10}",
				"white": f"{30 + 10}",
				"normal": 1
			}
			return f"\033[1;{txt_colors[txt]};{bg_colors[bg]}m{message}\033[0m"

		os.system('cls')
		# Find which day of the week the month started on
		first_day = date(self.today.year, self.today.month, 1).weekday()

		# Find number of days in month
		num_days = monthrange(self.today.year, self.today.month)[1]

		# find all dates this month with events
		first = date(self.today.year, self.today.month, 1)
		last = date(self.today.year, self.today.month, num_days)
		monthly_events = list(filter(lambda x: first <= x <= last, self.events.values()))
		# turn it into a list of ints
		monthly_events = [eventful_day.day for eventful_day in monthly_events]

		cal_string = ""
		# Print month and year
		cal_string += color_entry(
			f"{self.MONTHS[self.today.month]} : {self.today.year}\n",
			txt="cyan"
		)
		# Print the days of the week
		for day in self.WEEKDAYS:
			cal_string += f"{day} "
		cal_string += "\n"
		days = 0
		while days < num_days:
			for i, day in enumerate(self.WEEKDAYS):
				if days == 0 and i < first_day:
					entry = "   "
				else:
					days += 1
					entry = f"{days:2} "
					if days in monthly_events and not days == self.today.day:
						entry = color_entry(entry, txt="green")
					if days == self.today.day and days not in monthly_events:
						entry = color_entry(entry, bg="red")
					if days == self.today.day and days in monthly_events:
						entry = color_entry(entry, txt="green", bg="red")
				if days > num_days:
					entry = "   "
				cal_string += entry
			cal_string += "\n"
		print(cal_string)


if __name__ == '__main__':
	cal = Calendar()
	cal.command_loop()
