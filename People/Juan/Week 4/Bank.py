#!/usr/bin/env python3

"""
Stores accounts, verifies transactions
"""

from typing import List, Dict, Tuple
import csv
import os

from Accounts import Account
from Transactions import Transaction, DirectedTransaction


class Bank:
	"""
	Class that stores accounts, verifies internal transactions
	"""

	BANK = Account.BANK
	BANK_PATH = os.getcwd()
	BANK_FILE = os.path.join(BANK_PATH, "Bank.bk")
	BANK_CATEGORIES = ["account_number", "name", "balance"]

	def __init__(self, default_currency="USD"):
		self._status = ""  # Status message of bank

		self.__accounts: Dict[int, Account] = {}
		self.load_accounts()

	@property
	def accounts(self):
		return {ac_n: ac for ac_n, ac in self.__accounts.items() if ac_n}

	@property
	def secret_accounts(self):
		return self.__accounts

	@property
	def status(self) -> str:
		"""
		Attribute to store status of last operation.
		"""
		stat = self._status
		self._status = ""
		return stat

	def verify_transaction(
			self,
			transaction: Transaction,
			sending_account: int = None,
			receiving_account: int = None
	) -> bool:
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
		success = f"{transaction} completed successfully."
		failure = f"{transaction} could not be completed."

		if receiving_account is None:
			self._status += failure + " No receiving account was provided."
			return False
		if receiving_account not in self.__accounts.keys():
			self._status += failure + " Receiving account was not found in this bank"
			return False
		if sending_account not in self.__accounts.keys():
			self._status += failure + " Sending account was not found in this bank"
			return False

		if self.__accounts[sending_account].balance >= transaction.usd:
			self._status += success
			return True
		else:
			self._status += failure + f" Balance of account {sending_account} is not sufficient"
			return False

	def complete_transaction(
			self,
			transaction: Transaction,
			sending_account: int = None,
			receiving_account: int = None
	) -> bool:
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

		if self.verify_transaction(transaction, sending_account, receiving_account):
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
			self.__accounts[transaction.sending_account].apply(transaction)
			self.__accounts[transaction.receiving_account].apply(transaction)
			transaction.completed = True
			return True
		return False

	def _add_account(self, account: Account) -> bool:
		"""
		Creates an account at this bank
		Args:
			account : valid account to be added to the bank
		Returns:
			verified
		"""
		# Boilerplate
		success = f"{account} successfully added."
		failure = f"{account} could not be added."

		try:
			self.__accounts.update({account.account_number: account})
		except Exception as e:
			self._status += f"{type(e)} : {e}\n" + failure
			return False

		self._status += success
		return True

	def create_account(self, name: str) -> Tuple[bool, int]:
		"""
		Creates an account and adds it to this banks list of accounts.
		Args:
			name : name for the bank account

		Returns:
			(verified, account_number)
				verified : was the account successfully added
				account_number : number off account added. -1 if addition is unsuccessful
		"""
		failure = f"Account {name} could not be created."

		if name == Bank.BANK:
			self._status += failure + f" {Bank.BANK} is not an allowed account name"
			return False, -1
		if self.find_account(name) > 0:
			self._status += f"\n{failure} Another account is already using the name {name}"
			return False, -1
		self._status += "\n"

		while True:
			try:
				account = Account(name)
			except AssertionError as e:
				self._status = f"{e}"
				return False, -1
			if account.account_number not in self.accounts.keys():
				verified = self._add_account(account)
				if verified:
					return True, account.account_number
				else:
					return False, -1
			else:
				print(f"{account.account_number} is in {self.accounts.keys()}")

	def load_accounts(self):
		"""
		Loads all accounts detailed in the bank file
		"""
		try:
			with open(self.BANK_FILE, "r", newline="") as bank_file:
				bank_accounts = list(csv.reader(bank_file))
		except FileNotFoundError:
			bank_account = Account(Bank.BANK)
			self._add_account(bank_account)
			return

		for account_attributes in bank_accounts[1:]:
			atr_dict = dict(zip(bank_accounts[0], account_attributes))
			try:
				account = Account.load(int(atr_dict["account_number"]))
			except FileNotFoundError:
				self._status += "Account file not found. Account not loaded"
				continue
			loaded_attributes = [
				str(getattr(account, category)) for category in Bank.BANK_CATEGORIES]
			if account_attributes == loaded_attributes:
				self._add_account(account)
				self._status += "\n"
			else:
				self._status += f"Someone Has messed with {account}. Account Not loaded.\n" \
									f"loaded : {loaded_attributes}\n" \
									f"expected : {account_attributes}"

		if 0 not in self.__accounts.keys():
			self._add_account(Account(self.BANK))

	def delete_account(self, account_number: int):
		"""
		Deletes an account given the account number
		Args:
			account_number : number  of account to be deleted
		"""
		account = self.accounts.pop(account_number)
		account.destroy()
		self._status += f"{account} successfully deleted."
		del account

	def close(self):
		"""
		Closes the bank and saves all accounts in self.accounts, as well as the list of accounts
		to be loaded on the next startup
		"""
		if len(self):
			with open(self.BANK_FILE, "w", newline="") as bank_file:
				bank_writer = csv.writer(bank_file, delimiter=",")
				bank_writer.writerow(Bank.BANK_CATEGORIES)
				for account in self.accounts.values():
					bank_writer.writerow(
						[getattr(account, category) for category in Bank.BANK_CATEGORIES]
					)
					account.save()
					self._status += f"{account} successfully saved\n"

	def find_account(self, account_name: str) -> int:
		"""
		Args:
			account_name : name of account to be returned
		Returns:
			Account number of specified account. -1 if account was not found
		"""
		for account_number, account in self.accounts.items():
			if account_name == account.name:
				self._status += f"{account} found."
				return account_number
		self._status += f"No account with name {account_name} was found"
		return -1

	def __len__(self):
		return len(self.accounts)

	def __repr__(self):
		return "Juan's super cool bank. Today's exclusive offer is $100 for opening an account today!"

