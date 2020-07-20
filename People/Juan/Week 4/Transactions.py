#!/usr/bin/env python3

"""
We're gonna put transaction classes here
"""

from datetime import datetime
from decimal import Decimal

from Currency import Money


class Transaction(Money):
	"""
	Class that tracks an attempted transaction

	Attributes:
		amount (Decimal): amount to be transferred to two decimal places
		transaction_date (datetime): date and time when the transaction took place. If unspecified,
			set to current date and time
		currency (str): currency in use, according to the ISO 4217:2015(en) codification
		usd_conversion (float): conversion rate to USD
		description (str): string describing the nature of the transaction
	"""

	def __init__(
			self,
			amount: Decimal,
			transaction_date: datetime = None,
			currency: str = "USD",
			usd_conversion: float = 1.0,
			description: str = None
	):

		super().__init__(amount, currency)
		self.completed = False
		self.__transaction_date = transaction_date if transaction_date is not None else datetime.now()

		try:
			self.__usd_conversion = float(usd_conversion)
		except ValueError as e:
			msg = f"invalid type {type(usd_conversion)} for usd_conversion. Numeric type required"
			raise TypeError(msg) from e

		self.__description = description if description is not None else ""

# attribute getters --------------------------------------------------------------------------------
	@property
	def transaction_date(self):
		return self.__transaction_date

	@property
	def usd_conversion(self):
		return self.__usd_conversion

	@property
	def description(self):
		return self.__description

	@property
	def usd(self):
		return Decimal(float(self.amount)*self.usd_conversion).quantize(Decimal(self.quantizer))

	def __repr__(self):
		return f"Transaction {self.amount} {self.currency} on {self.transaction_date}"


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
			amount: Decimal,
			sending_account: int,
			receiving_account: int,
			transaction_date: datetime = None,
			currency: str = "USD",
			usd_conversion: float = 1.0,
			description: str = None,
	):
		super().__init__(amount, transaction_date, currency, usd_conversion, description)
		self.__sending = sending_account
		self.__receiving = receiving_account

	@property
	def sending_account(self):
		return self.__sending

	@property
	def receiving_account(self):
		return self.__receiving

	def __repr__(self):
		ms = super(DirectedTransaction, self).__repr__()
		ms += f"\nFrom Account {self.sending_account}\nTo Account {self.receiving_account}\n"
		return ms




