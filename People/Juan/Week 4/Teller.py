#!/usr/bin/env python3

"""
Teller will interface with the user, serve as intermediary between the user and the bank
"""
import logging

from Bank import Bank
from Accounts import Account
from Transactions import DirectedTransaction


class Teller:
	"""
	Class to interact with the user, and bank.
	"""
	def __init__(self, bank: Bank):
		self._bank = Bank

	@property
	def _accounts(self):
		return self._bank.accounts

	def log_in(self):
		"""
		Prompt the user to create an account, log in to their account, then manage their account
		"""


	def manage_account(self):
		"""
		Prompt the user to manage their account: actions include:
			* Changing account name
			* Transferring money from another account (transaction from their account)
			* Accepting Pending transactions to their account
			* Deleting Their account
		"""
		pass


if __name__ == "__main__":
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	my_bank = Bank()
	logger.debug(my_bank.status)

	teller = Teller(my_bank)
	teller.log_in()