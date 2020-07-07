#!/usr/bin/env python3

"""
We're gonna put transaction classes here
"""

from datetime import datetime
from decimal import Decimal
from typing import List
import csv


class Transaction:
	"""
	Class that tracks an attempted transaction

	Attributes:
		amount (Decimal): amount to be transferred to two decimal places
		transaction_date (datetime): date and time when the transaction took place. If unspecified,
			set to current date and time
		currency (str): currency in use, according to the common codification
		usd_conversion (float): conversion rate to USD
		description (str): string describing the nature of the transaction
	"""

	QUANTIZER = Decimal('1.00')
	CURRENCIES_FILENAME = "currency_codes.csv"

	def __init__(
			self,
			amount: str,
			transaction_date: datetime = None,
			currency: str = "USD",
			usd_conversion: float = 1.0,
			description: str = None
	):

		self.completed = False
		self.__amount = Decimal(amount).quantize(Transaction.QUANTIZER)
		self.__transaction_date = transaction_date if transaction_date is not None else datetime.now()

		if currency.upper() not in self._currency_codes:
			raise ValueError(f"{currency} is not a valid currency code")
		self.__currency = currency

		try:
			self.__usd_conversion = float(usd_conversion)
		except ValueError as e:
			msg = f"invalid type {type(usd_conversion)} for usd_conversion. Numeric type required"
			raise TypeError(msg) from e

		self.__description = description if description is not None else ""

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
		return Decimal(float(self.amount)*self.usd_conversion).quantize(Transaction.QUANTIZER)

	@property
	def _currency_codes(self) -> List[str]:
		with open(Transaction.CURRENCIES_FILENAME, newline="") as f:
			currency_info = list(csv.reader(f))
		return [cur[2] for cur in currency_info]


class DirectedTransaction(Transaction):
	"""
	Class to hold information on an attempted transaction between two accounts

	Attributes:
		amount (Decimal): amount to be transferred to two decimal places
		sending_account (int) : account number of account that is sending the money
		receiving_account (int) : account number of account that is receiving the money
		transaction_date (datetime): date and time when the transaction took place. If unspecified,
			set to current date and time
		currency (str): currency in use, according to the common codification
		usd_conversion (float): conversion rate to USD
		description (str): string describing the nature of the transaction
	"""
	def __init__(
			self,
			amount: str,
			sending_account: int,
			receiving_account: int,
			transaction_date: datetime = None,
			currency: str = "USD",
			usd_conversion: float = 1.0,
			description: str = None,
	):
		super().__init__(amount, transaction_date, currency, usd_conversion, description)
		self.__sending = self._validate(sending_account)
		self.__receiving = self._validate(receiving_account)

	@property
	def sending_account(self):
		return self.__sending

	@property
	def receiving_account(self):
		return self.__receiving

	def _validate(self, account_no):
		"""
		Validates the provided account number. Raises a ValueError if the number is not valid
		Returns:
			the account number
		"""
		# TODO : Implement this
		return account_no



