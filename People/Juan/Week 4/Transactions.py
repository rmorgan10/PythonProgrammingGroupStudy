#!/usr/bin/env python3

"""
We're gonna put transaction classes here
"""

from datetime import datetime
import re


class Transaction:
	"""
	Class that tracks a potential transaction

	Should:
	* add money to a receiving account
	* remove money from a giving account
	* convert funds from account to account

	Attributes:
		amount (str): string in format {Whole_place}.{decimal places} with max 2 characters after
			the decimal
		transaction_date (datetime): date and time when the transaction took place. If unspecified,
			set to current date and time
		currency (str): currency in use, according to the common codification
		usd_conversion (float): conversion rate to USD
		description (str): string describing the nature of the transaction
	"""

	# TODO: Use custom, or elsewhere defined, data type for ammount, to avoid rounding errors
	# TODO: Have setter for currency look up the currency code given from a list of standard
	#  codifications
	def __init__(
			self,
			amount: str,
			transaction_date: datetime = None,
			currency: str = "USD",
			usd_conversion: float = 1.0,
			description: str = None
	):
		self.__amount = self.set_amount(amount)
		self.__transaction_date = self.set_transaction_date(transaction_date)
		self.__currency = self.set_currency(currency)
		self.__usd_conversion = self.set_usd_conversion(usd_conversion)
		self.__description = self.set_description(description)

# attribute getters --------------------------------------------------------------------------------
	@property
	def amount(self):
		return self.__amount

	@property
	def transaction_date(self):
		return self.__transaction_date

	@property
	def currency(self):
		return self.__currency

	@property
	def usd_conversion(self):
		return self.__usd_conversion

	@property
	def description(self):
		return self.__description

	@property
	def usd(self):
		return float(self.amount)*self.usd_conversion

# attribute setters --------------------------------------------------------------------------------
	@staticmethod
	def set_amount(amount):
		# Use a regular expression to match the input string
		pattern = r"(\d+)\.?(\d2)?"
		try:
			am_groups = re.match(pattern, amount).groups()
			return f"{am_groups[0]}.{am_groups[1]}"
		except (AttributeError, TypeError) as e:
			val_er_msg = f"amount: {amount} does not match the pattern <whole>.<decimal>"
			raise ValueError(val_er_msg) from e

	@staticmethod
	def set_transaction_date(transaction_date):
		return transaction_date if transaction_date is not None else datetime.now()

	@staticmethod
	def set_currency(currency):
		# TODO : write the list
		# if currency.upper() not in Transaction.CURRENCIES:
		# 	raise ValueError(f"{currency} is not a valid currency code")
		return currency

	@staticmethod
	def set_usd_conversion(usd_conversion):
		try:
			return float(usd_conversion)
		except ValueError as e:
			msg = f"invalid type {type(usd_conversion)} for usd_conversion. Numeric type required"
			raise TypeError(msg) from e

	@staticmethod
	def set_description(description):
		return description if description is not None else ""

