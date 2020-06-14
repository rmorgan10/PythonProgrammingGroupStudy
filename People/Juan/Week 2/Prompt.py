import os
from datetime import date, time, datetime
from calendar import monthrange
from Calendar import Calendar
from CalendarErrors import MainError, BreakoutError

"""
Module to hold generally useful functions that prompt the user for information
"""


def parse_user_date(usr_date: str) -> date:
	"""
	Parses a user's date input, prompts the user to input useful date data if user's date was
	invalid
	Args:
		usr_date : str, user input of date info. Should be in <yyyy/mm/dd> format

	Returns:
		valid datetime.date() object
	"""
	expected_len = len("yyyy/mm/dd")
	if usr_date is None:
		return prompt_user_date()
	try:
		dt_list = usr_date[0:expected_len].split("/")
		# Ensure right number of fields
		if len(dt_list) >= 3:
			try:
				# Ensure year is long enough to be useful
				if len(dt_list[0]) == 4:
					year = int(dt_list[0])
				else:
					raise BreakoutError()
				# set rest of info
				month = int(dt_list[1])
				day = int(dt_list[2])
			# deal with bad user characters
			except ValueError:
				raise BreakoutError()
			# create date if user isn't a dingus
			calendar_date = date(year, month, day)
		else:
			raise BreakoutError()
	except BreakoutError:
		# Make user give us a useful date if they are a dingus
		calendar_date = prompt_user_date()
	return calendar_date


def prompt_user_date(prompting_msg=None) -> date:
	"""
	Prompts the user for a valid date to draw out on the calendar
	Args:
		prompting_msg : message to prompt user for info on the time
	Returns:
		date object indicating the user's desired date
	"""

	os.system('cls')
	if prompting_msg is not None:
		print(prompting_msg)
	print(f"(input {Calendar.QUIT} to return to the main menu at any time)")

	yr = get_info("Which year? (In <yyyy> format please) :", 1, ln=4)
	mn = get_info("What month? (as an int please) :", 1, 12)
	dy = get_info("What day? :", 1, monthrange(yr, mn)[1])

	return date(yr, mn, dy)


def prompt_user_time(prompting_msg: str = None) -> time:
	"""
	Prompts the user to import time info for hours and minutes
	Args:
		prompting_msg : message to prompt the user for info on the time in hours and minutes

	Returns:
		time object with user's desired time
	"""

	os.system('cls')
	if prompting_msg is not None:
		print(prompting_msg)
	print(f"(input {Calendar.QUIT} to return to the main menu at any time)")

	hr = get_info("What hour? (0 to 23)", 0, 24)
	mn = get_info("What minute?", 0, 60)
	return time(hr, mn)


def prompt_user_datetime(prompting_msg: str = None) -> datetime:
	"""
	Prompts the user to input info about a particular date and time
	Args:
		prompting_msg : message to prompt the user

	Returns:
		datetime object with user's desired date and time
	"""
	os.system('cls')
	if prompting_msg is not None:
		print(prompting_msg)

	usr_date = prompt_user_date("Lets start with the day")
	usr_time = prompt_user_time("Now lets get the time")

	# return relevant datetime object
	return datetime(
		usr_date.year,
		usr_date.month,
		usr_date.day,
		usr_time.hour,
		usr_time.minute
	)


def get_info(msg: str, low: int, high: int = None, ln: int = 2) -> int:
	"""
	Uses msg to prompt user to provide useful time info
	Args:
		msg : message prompting the user to provide the desired info
		low : lower limit for input
		high : higher limit for input
		ln : how long is the expected user input
	Returns:
		int input by the user
	"""
	# deal with this funky assertion message to make sure input is in range
	if high is None:
		as_msg = "{0} is not a valid input, must be greater than {1}. Try Again"
	else:
		as_msg = "{0} is not a valid input, must be between {1} and {2}. Try Again"

	while True:
		usr_inp = input(msg)
		try:
			# Deal with the quitting case (always available)
			if usr_inp[0].upper() == Calendar.QUIT:
				raise MainError
			# store user data
			val = int(usr_inp[:ln])
			# make sure user data is usable
			if high is None:
				assert val >= low
			else:
				assert val in range(low, high)
			# Exit the loop
			break

		# Deal with bad user inputs
		except (IndexError, ValueError):
			print(f"{usr_inp} is not a valid input. Try again")
			continue
		except AssertionError:
			print(as_msg.format(usr_inp, low, high))
			continue
	return val