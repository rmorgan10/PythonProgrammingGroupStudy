#!/usr/bin/env python3

"""
This file stores account classes
"""

from typing import List
import random
import pickle
from decimal import Decimal
import os
# This is filthy, BUT we only use Transaction here to it's ok. I promise.
from Transactions import DirectedTransaction as Transaction


class Account:

	MIN_NAME = 4  # Minimum name length
	EXTENSION = ".acc"
	BANK = "Bank"

	def __init__(self, name):
		self.name = name
		self.__number = self.create_account_number()
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
		balance = 0
		for transaction in self.transactions:
			sign = 1 if transaction.receiving_account == self.__number else -1
			balance += sign*transaction.usd*transaction.completed
		# The bank has infinite money
		if self.name == Account.BANK:
			balance = Decimal('Infinity')
		return balance

	@property
	def all_usd(self) -> bool:
		return all(transaction.currency == "USD" for transaction in self.transactions)

	@property
	def account_file(self):
		return f"{self.account_number}{Account.EXTENSION}"

	def create_account_number(self) -> int:
		"""
		Should generate a 10 digit account number.
		Returns:
			int : the account number
		"""
		if self.name == Account.BANK:
			return 0
		random.seed(self.name)
		return 10**10 + random.randint(0, 10**9-1)

	def apply(self, new_transaction: Transaction):
		"""
		Applies new_transaction to this account
		"""
		if self.__number in [new_transaction.receiving_account, new_transaction.sending_account]:
			self.transactions.append(new_transaction)
		else:
			raise ValueError(
				"This account is not involved in the desired transaction. Transaction Cancelled"
			)

	def save(self):
		"""
		Saves this account to a .acc file
		Returns:
			The filename for the file this class was saved to
		"""
		with open(self.account_file, "wb") as file:
			pickle.dump(self, file)

	def destroy(self):
		"""
		Destroys this account's file.
		Only call this function if account is also being deleted
		"""
		os.remove(self.account_file)

	@staticmethod
	def load(account_number: int):
		"""
		Loads an account from the text_file account_filename
		Args:
			account_number : number associated with the account
		Returns:
			Account loaded from file
		"""
		account_filename = f"{account_number}{Account.EXTENSION}"
		with open(account_filename, "rb") as account_file:
			loaded_account = pickle.load(account_file)
		return loaded_account

	def __len__(self):
		return len(self.transactions)

	def __repr__(self):
		return f"Account {self.account_number} ; {self.name}"