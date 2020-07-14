#!/usr/bin/env python3

"""
Teller will interface with the user, serve as intermediary between the user and the bank
"""
import logging
import os
from decimal import Decimal, InvalidOperation
from typing import Dict

from Bank import Bank
from Accounts import Account
from Transactions import DirectedTransaction as Transaction
import Currency


class QuitError(Exception):
	pass


class LogOutError(Exception):
	pass


class Teller:
	"""
	Class to interact with the user, and bank.
	"""

	QUIT = "quit"
	TO_QUIT = f"Type {QUIT} to exit any time"

	def __init__(self, bank: Bank):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.setLevel(logging.DEBUG)
		self._bank = bank

		if not len(self._bank):
			for i in range(20):
				nm = f"ac_{i}"
				success, ac_no = bank.create_account(nm)
				print(bank.status)
				if ac_no > 0:
					bank.complete_transaction(
						Transaction(Decimal("100.00"), 0, ac_no)
					)
					print(bank.status)
			input()
		self.clr()

	@property
	def _accounts(self) -> Dict[int, Account]:
		return self._bank.accounts

	def clr(self):
		"""
		Clears the bank's status flag and gives us debugging info
		"""
		self.logger.debug(f"Logger info : {self._bank.status}")

	def input(self, msg: str):
		"""
		wraps repetitive boilerplate around input()
		Args:
			msg : message for the user

		Returns:

		"""
		self.clr()
		os.system('cls')
		new_msg = f"{self.TO_QUIT}\n\n{msg}"
		usr_in = input(new_msg)
		if usr_in.lower() == self.QUIT.lower():
			raise QuitError
		else:
			return usr_in

	def begin(self):
		"""
		Prompt the user to create an account, log in to their account, then manage their account
		"""
		log_in = "L"
		create = "C"

		msg = f"""
Welcome to {self._bank}.\nWhat would you like to do?
{log_in} to log in to you existing account
{create} to create an account
: """
		while True:
			usr_choice = self.input(msg)[0].upper()
			if usr_choice in [log_in, create]:
				break

		if usr_choice == log_in:
			return self.log_in()
		elif usr_choice == create:
			return self.create_account()

	def log_in(self) -> int:
		"""
		Prompts the user to log in to an existing account
		Returns:
			account number of account user logs into.
		"""
		while True:
			ac_name = self.input("To log into your account, input the account name : ")
			account_no = self._bank.find_account(ac_name)
			if account_no > 0:
				print(f"Logging you in to your account! {self._accounts[account_no]}")
				return account_no
			else:
				print(f"{self._bank.status}\n")

	def create_account(self) -> int:
		"""
		Prompts the user through creating an account
		Returns:
			account number of account user creates
		"""
		base_message = "To create an account, input your desired name for the account : "
		message = base_message
		while True:
			ac_name = self.input(message)
			success, account_no = self._bank.create_account(ac_name)
			if success:
				print(f"{self._bank.status}\nLogging you into your new account!")
				deal = Transaction(
					Decimal("100.00"),
					0,
					account_no,
					description="A SUPER good deal!"
				)
				self._bank.complete_transaction(deal)
				input(self._bank.status)
				return account_no
			else:
				message = f"{self._bank.status}\n\n{base_message}"

	def manage_account(self, account_number: int):
		"""
		Prompt the user to manage their account
		Args:
			account_number : number of account being managed
		"""
		# Actions:
		check_balance = "C"
		transfer_to = "P"
		transfer_from = "G"
		delete = "D"
		log_out = "E"
		actions = [
			check_balance,
			transfer_to,
			transfer_from,
			delete,
			log_out
		]
		account = self._accounts[account_number]
		msg = f"""
Welcome to {account}! What would you like to do?
{check_balance} to check your current balance
{transfer_to} to transfer money from your account to another account
{transfer_from} to transfer money to your account from another account
{delete} to delete your account
{log_out} to log out
"""
		while True:
			usr_choice = self.input(msg)[0].upper()
			if usr_choice in actions:
				break

		if usr_choice == check_balance:
			input(f"Your current balance is : ${account.balance} (USD)")
		if usr_choice == transfer_to:
			self.pay(account_number)
		if usr_choice == transfer_from:
			self.receive(account_number)
		if usr_choice == delete:
			self.delete(account_number)
		if usr_choice == log_out:
			account.save()
			raise LogOutError

	def get_account(self, base_message) -> int:
		"""
		Get a valid account number from the user
		Args:
			base_message : message to prompt the user

		Returns:
			valid account number
		"""
		message = base_message
		while True:
			try:
				user_account = int(self.input(message))
			except ValueError:
				message = \
					"That was not a valid account number. Account numbers are 10 digit integers\n"
				message += base_message
				continue
			if user_account in self._accounts.keys():
				return user_account
			else:
				message = f"Account {user_account} cannot be found at our bank\n{base_message}"
				continue

	def get_amount(self, base_message: str, sender: int, conversion: float) -> Decimal:
		"""
		Prompts user to input a valid amount of cash to be transfered by sender
		Args:
			base_message : message to prompt the user
			sender : account number of account sending cash
			conversion : conversion of transaction's currency to USD

		Returns:
			amount of cash
		"""
		message = base_message
		while True:
			try:
				quantity = Decimal(self.input(message))
			except InvalidOperation:
				message = f"That was not a valid amount. Please input a valid float\n{base_message}"
				continue
			if quantity > 0:
				if quantity*conversion > self._accounts[sender].balance:
					message = \
						f"account {sender} does not have sufficient funds to complete this transaction\n{base_message}"
					continue
				else:
					return quantity
			else:
				message = f"Negative or zero cash does not make sense.\n{base_message}"
				continue

	def get_currency(self, base_message: str) -> str:
		"""
		prompts the user to input a valid currency and it's conversion to USD
		Args:
			base_message : message to prompt the user
		Returns:
			3 letter code corresponding to the transaction's currency
				conversion : conversion to USD such that the amount in USD = (amount in
					currency_code)*conversion
		"""
		message = base_message
		while True:
			usr_code = self.input(message).upper()
			if usr_code in Currency.currency_codes():
				return usr_code
			else:
				message = f"{usr_code} is not a valid currency code\n{base_message}"

	def get_conversion(self, base_message: str) -> float:
		"""
		prompts the user to input a conversion from the given currency to USD
		Args:
			base_message : message to prompt the user
		Returns:
			conversion to USD such that the amount in USD = (amount in currency_code)*conversion
		"""
		message = base_message
		while True:
			try:
				conversion = float(self.input(message))
			except ValueError:
				message = f"Not a valid conversion. Please input a float.\n{base_message}"
			else:
				return conversion

	def pay(self, account_number):
		"""
		Transfer money from user's account to another account specified by the user
		Args:
			account_number : number of the user's account
		"""
		# first get the account number
		base_message = "Enter the account number of the account that will receive your transfer : "
		receiver = self.get_account(base_message)

		# get the currency
		user_choice = self.input(f"Will this transaction be in USD? Y/n :").upper()
		if user_choice == "n":
			currency = self.get_currency("What currency will this transaction be in? : ")
			conversion = self.get_conversion(f"What is {currency}'s conversion to USD? :")
		else:
			currency, conversion = ("USD", 1)

		# now get the quantity
		base_message = \
			f"Enter the amount (in {currency}) you would like to transfer to account {receiver} : "
		quantity = self.get_amount(base_message, account_number, conversion)

		# and the description
		description = self.input("How would you like to describe this transaction?\n : ")
		transaction = Transaction(
			quantity,
			account_number,
			receiver,
			currency=currency,
			usd_conversion=conversion,
			description=description
		)

		self._bank.complete_transaction(transaction)
		input(self._bank.status)

	def receive(self, account_number: int):
		"""
		Transfer money from another account, specified by the user, to user's account
		Args:
			account_number : number of the user's account
		"""
		# first get the account number
		base_message = "Enter the account number of the account that will be transferring you money : "
		sender = self.get_account(base_message)

		# get the currency
		user_choice = self.input(f"Will this transaction be in USD? Y/n : ").upper()
		if user_choice == "n":
			currency = self.get_currency("What currency will this transaction be in? : ")
			conversion = self.get_conversion(f"What is {currency}'s conversion to USD? : ")
		else:
			currency, conversion = ("USD", 1)

		# now get the quantity
		base_message = \
			f"Enter the amount (in {currency}) you would like to have transferred from {sender} : "
		quantity = self.get_amount(base_message, sender, conversion)

		# and the description
		description = self.input("How would you like to describe this transaction?\n : ")
		transaction = Transaction(
			quantity,
			sender,
			account_number,
			currency=currency,
			usd_conversion=conversion,
			description=description
		)

		self._bank.complete_transaction(transaction)
		input(self._bank.status)

	def delete(self, account_number: int):
		"""
		deletes the account associated with account_number
		Args:
			account_number : user's account number
		"""
		last_chance = self.input(
			f"Are you sure you wish to delete account {account_number}? y/N :"
		)[0].upper()
		if last_chance == "Y":
			self._bank.delete_account(account_number)
			input(self._bank.status)
		else:
			input("Deletion aborted.")
			return


if __name__ == "__main__":
	my_bank = Bank()
	teller = Teller(my_bank)

	try:
		while True:
			acc_no = teller.begin()
			try:
				while True:
					teller.manage_account(acc_no)
			except LogOutError:
				continue
	except QuitError:
		my_bank.close()
		print(my_bank.status)