#!/usr/bin/env python3

"""
This file stores account classes
"""

from Transactions import Transaction
from typing import List


class Account:

	MIN_NAME = 4  # Minimum name length

	def __init__(self, name):
		self.__number = self.create_account_number()
		self.name = name
		self.transactions: List[Transaction] = []

	@property
	def account_number(self):
		return self.__number

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, new_name):
		if not isinstance(new_name, str):
			raise TypeError(f"{new_name} is not a string.")
		assert len(new_name) >= Account.MIN_NAME, \
			f"Name to be set {new_name} must be at least {Account.MIN_NAME} characters long"
		self.__name = new_name

	@property
	def balance(self) -> float:
		"""
		Calculate the current account balance and provide it to the user
		Returns:
			Current account balance in USD
		"""
		raise NotImplementedError

	@property
	def all_usd(self) -> bool:
		return all(transaction.currency == "USD" for transaction in self.transactions)

	def create_account_number(self):
		"""
		Should generate a 10 digit account number.
		Returns:
			int : the account number
		"""
		raise NotImplementedError

	def apply(self, new_transaction: Transaction):
		"""
		Applies new_transaction to this account
		Args:
			new_transaction ():
		"""
		raise NotImplementedError

	def save(self) -> str:
		"""
		Saves this account to a .acc file
		Returns:
			The filename for the file this class was saved to
		"""
		raise NotImplementedError

	@staticmethod
	def load(account_filename: str) -> Account:
		"""
		Loads an account from the text_file account_filename
		Args:
			account_filename : filename of account to be loaded
		Returns:
			Account loaded from file
		"""
		raise NotImplementedError

	def __len__(self):
		return len(self.transactions)