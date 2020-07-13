#!/usr/bin/env python3

"""
Stores accounts, verifies transactions
"""

from typing import List, Dict, Tuple
from Accounts import Account
from Transactions import Transaction, DirectedTransaction


class Bank:
	"""
	Class that stores accounts, verifies internal transactions
	"""

	BANK = "Bank"

	def __init__(self, default_currency="USD"):
		self.__accounts: Dict[int, Account] = {0: Account(Bank.BANK)}

	@property
	def accounts(self):
		return self.__accounts

	def verify_transaction(
			self,
			transaction: Transaction,
			sending_account: int = None,
			receiving_account: int = None
	) -> Tuple[bool, str]:
		"""
		Verifies that a transaction can be completed.
		Args:
			transaction : transaction to be completed between accounts at this bank
			sending_account : account number of the account at this bank that will be sending
				money in this transaction
			receiving_account : account number of the account at this bank that will be receiving
				money in this transaction

		Returns:
			(verified, message)
				verified : can the transaction be completed successfully
				message : message detailing success or reason for failure
		"""
		if isinstance(transaction, DirectedTransaction):
			sending_account = transaction.sending_account
			receiving_account = transaction.receiving_account
		elif sending_account is None:
			sending_account = 0

		# Boilerplate
		success = "The transaction completed successfully."
		failure = "The transaction Could not be completed."

		if receiving_account is None:
			return False, failure + "No receiving account was provided."
		if receiving_account not in self.accounts.keys():
			return False, failure + "Receiving account was not found in this bank"
		if sending_account not in self.accounts.keys():
			return False, failure + "Sending account was not found in this bank"

		if self.accounts[sending_account].balance > transaction.usd:
			return True, success
		else:
			acc_name = self.accounts[sending_account].name
			return False, failure + f"Balance of account {acc_name} is not sufficient"

	def complete_transaction(
			self,
			transaction: Transaction,
			sending_account: int = None,
			receiving_account: int = None
	) -> Tuple[bool, str]:
		"""
		Verifies a transaction can be completed, then applies the transaction to the accounts
		involved
		Args:
			transaction : the transaction to take place
			sending_account : account sending the money
			receiving_account : account receiving the money
		Returns:
			(verified, message)
				verified : was the transaction completed successfully
				message : message detailing success or reason for failure
		"""

		verified, message = self.verify_transaction(transaction, sending_account, receiving_account)
		if verified:
			if not isinstance(transaction, DirectedTransaction):
				transaction = DirectedTransaction(
					amount=transaction.amount,
					sending_account=sending_account,
					receiving_account=receiving_account,
					transaction_date=transaction.transaction_date,
					currency=transaction.currency,
					usd_conversion=transaction.usd_conversion,
					description=transaction.description
				)
			self.accounts[transaction.sending_account].apply(transaction)
			self.accounts[transaction.receiving_account].apply(transaction)
		return verified, message

	def _add_account(self, account: Account) -> Tuple[bool, str]:
		"""
		Creates an account at this bank
		Args:
			account : valid account to be added to the bank
		Returns:
			(verified, message)
				verified : was the account successfully added
				message : message detailing success or reason for failure
		"""
		# Boilerplate
		success = f"Account {str(account)} successfully added."
		failure = f"Account {str(account)} could not be added."

		if account.name == Bank.BANK:
			return False, failure + f"{Bank.BANK} is not an allowed account name"
		else:
			self.__accounts.update({account.account_number, account})
			return True, success

	def create_account(self, name: str) -> Tuple[bool, str]:
		"""
		Creates an account and adds it to this banks list of accounts.
		Args:
			name : name for the bank account

		Returns:
			(verified, message)
				verified : was the account successfully added
				message : message detailing success or reason for failure
		"""
		# Boilerplate
		success = f"Account {name} successfully created."
		failure = f"Account {name} could not be created."

		if name == Bank.BANK:
			return False, failure + f"{Bank.BANK} is not an allowed account name"

		while True:
			account = Account(name)
			if account.account_number not in self.accounts.keys():
				verified, message = self._add_account(account)
				if verified:
					return True, success
				else:
					return False, message


