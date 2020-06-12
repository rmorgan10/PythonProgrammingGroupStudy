"""
File to hold different kinds of event classes
"""
from datetime import date, datetime

class Event:
	"""
	Base class for all events
	"""
	def __init__(self, date_of_event: date, name: str, description: str = None, time = None):
		self.date_of_event = date_of_event
		self.name = name
		self.description = description
		self.time = time

		self.year = self.date_of_event.year
		self.month = self.date_of_event.month
		self.day = self.date_of_event.day
