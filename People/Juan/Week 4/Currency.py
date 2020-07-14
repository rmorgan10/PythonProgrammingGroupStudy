from typing import List
import csv
from decimal import Decimal


class Money:
	"""
	Class that holds currency of a particular type

	"""

	CURRENCIES_FILENAME = \
		r"C:\Users\Juan\Repos\PythonProgrammingGroupStudy\People\Juan\Week 4\currency_codes.csv"

	def __init__(self, amount: Decimal, currency_code: str = "USD"):
		if currency_code.upper() not in self._currency_codes:
			raise ValueError(f"{currency_code} is not a valid currency code")
		self.__currency_code = currency_code
		self.__amount = amount.quantize(self.quantizer)

	@property
	def _currency_codes(self) -> List[str]:
		return currency_codes(Money.CURRENCIES_FILENAME)

	@property
	def amount(self):
		return self.__amount

	@property
	def quantizer(self):
		return Decimal("1."+"0"*get_minor_unit(self.__currency_code, Money.CURRENCIES_FILENAME))

	@property
	def currency(self):
		return self.__currency_code


def currency_codes(currencies_filename: str = "currency_codes.csv") -> List[str]:
	"""
	Returns all valid currency codes as specified in the currencies .csv file
	Args:
		currencies_filename : name of the file containing information on global currencies
		Returns:
			list of all valid currency codes
	"""
	with open(currencies_filename, newline="") as f:
		currency_info = list(csv.reader(f))
	return [cur[2] for cur in currency_info]


def get_minor_unit(currency_code: str, currencies_filename: str = "currency_codes.csv") -> int:
	"""
	Returns the minor unit (how many decimal places are needed to store info about this currency)
	from the currencies file
	Args:
		currency_code : valid country currency
		currencies_filename :  name of the file containing information on global currencies
	Returns:
		minor unit
	"""
	if currency_code not in currency_codes(currencies_filename):
		raise ValueError(f"{currency_code} is not a valid currency code!")

	with open(currencies_filename, newline="") as f:
		currency_info = dict(zip(currency_codes(currencies_filename), list(csv.reader(f) )))

	minor_unit = currency_info[currency_code][4]
	try:
		minor_unit = int(minor_unit)
	except ValueError:
		"""
		Not all "currencies" are just currencies. Those don't have a valid minor unit. Assume
		storage to arbitrary precision, then realize arbitrary precision past 10 decimal places is
		fake
		"""
		minor_unit = 10
	return minor_unit
