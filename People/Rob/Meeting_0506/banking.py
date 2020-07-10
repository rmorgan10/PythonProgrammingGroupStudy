# A module to define the banking classes

from collections import defaultdict
import copy
import datetime
import os
from random import randint
import sqlite3
import sys

class Bank:
    def __init__(self):
        """
        Create a bank to store the accounts, pins, and a 
        ledger of transactions.
        """
        self.accounts = defaultdict(lambda: Account())
        self.pins = {}
        self.ledger = []
        self.load_ledger()
        return

    def load_ledger(self):
        """
        Read the sqlite3 database into the bank data structures.
        If no database exists, make one.
        """
        if not os.path.exists('bank_ledger.db'):
            # Establish connection to database
            self.conn = sqlite3.connect('bank_ledger.db')
            c = self.conn.cursor()

            # Create tables
            c.execute("""CREATE TABLE accounts
                         (number text, pin text)""")
            c.execute("""CREATE TABLE transactions
                         (number text, amount real)""")
            self.conn.commit()
            
        else:
            # Read in an existing database
            self.conn = sqlite3.connect('bank_ledger.db')
            self.update_accounts()

            return

    def update_ledger(self):
        """
        For a transaction in the ledger, write it to the database.
        """
        while len(self.ledger) > 0:
            transaction = self.ledger.pop()
            c = self.conn.cursor()
            c.execute("""INSERT INTO transactions 
                         VALUES ({0}, {1})""".format(transaction.account,
                                                     transaction.amount))
            self.conn.commit()
            
        return

    def update_accounts(self):
        """
        Read from the database and update update the accounts and pins
        in memory that are attached to the Bank.
        """
        # Get account numbers and pins
        c = self.conn.cursor()
        c.execute("""SELECT * FROM accounts""")
        for num, pin in c.fetchall():
            self.pins[num] = pin

        # Get the record of all transactions and execute them
        c.execute("""SELECT * FROM transactions""")
        for num, amount in c.fetchall():
            self.accounts[num].balance += amount

        return

    def close_bank(self):
        """
        Close the connection to the database. All transactions are 
        written at the time of execution, so nothing else is 
        needed here.
        """
        self.conn.close()
        sys.exit()
        return
    
    def open_account(self, number=None):
        """
        Create a new account. Generate a new account number and PIN. 
        Add the account to the database.

        :param number: str, the account number to open
        :return: account: An Account instance for the object just created
        """
        # Make a new account
        account = Account(number)
        account_pin = account._generate_pin()
        account.pin = account_pin

        # Store the account in the Bank data structures
        self.accounts[account.number] = account
        self.pins[account.number] = account_pin

        # Add the account to the database
        self.conn.execute("""INSERT INTO accounts
                             VALUES ({0}, {1})""".format(account.number, account_pin))
        self.conn.commit()
        
        return account

    def close_account(self, account):
        """
        Withdraw the entire balance and remove the account.

        :param account: An Account instance
        """
        # Don't let someone close an account with a debt
        if account.balance < 0.0:
            raise YaBrokeException

        # Withdraw all money and delete the account 
        self.make_withdrawal(account, account.balance)
        del self.accounts[account.number]
        del self.pins[account.number]
        
        return

    def login(self, number, pin):
        """
        Verify if a supplied PIN matches the account's PIN

        :param number: str, the account number to login access
        :param pin: str, the user-supplied PIN
        :return: account: the account instance if the PIN is correct
        """
        if self.pins[number] != pin:
            raise YaHackinException
        return self.accounts[number]
    
    def make_deposit(self, account, amount):
        """
        Increase the balance of an account.

        :param account: Account, the account to deposit into
        :param amount: float, the (positive) amount to deposit
        """
        self._make_transaction(account, amount)
        return

    def make_withdrawal(self, account, amount):
        """
        Reduce the balance of an account.

        :param account: Account, the account to withdraw from 
        :param amount: float, the (positive) amount to withdrawal
        """
        # Don't let people withdrawal more than they have
        if amount > account.balance:
            raise YaBrokeException

        # Make a negative transaction
        self._make_transaction(account, -1.0 * amount, how='subtract')
        return

    def make_wire(self, from_account, to_account, amount):
        """
        Move money from one account to another.
        
        :param from_account: Account, the account to withdraw from
        :param to_account: Account, the account to deposit into 
        :param amount: float, the (positive) amount to transfer
        """
        self.make_withdrawal(from_account, amount)
        self.make_deposit(to_account, amount)
        return

    def _make_transaction(self, account, amount, how='add'):
        """
        Document the transaction, adjust the account balance, and 
        update the ledger database.

        :param account: Account, the account to make the transaction with
        :param amount: float, the amount of the transaction
        :param how: str, (add or subtract) the type of transaction
        """
        t = Transaction(account, how=how)
        t.amount = amount
        self.ledger.append(t)
        self.accounts[account.number].balance += amount
        self.update_ledger()
        return

class Account:
    def __init__(self, number=None, balance=0.0):
        """
        Create an Account to with an account number, a PIN,
        and a balance.
        
        :param number: str, the account number. If no number is supplied
                            a new unique number is generated
        :param balance: float, the starting balance of the account. If no
                               balance is supplied then it is set to 0.0
        """
        if number is None:
            number = self._generate_number()
        self.number = number
        self.balance = balance
        self.pin = '' # overwritten by Teller during account creation
        return

    def __str__(self):
        """
        Reimplement the str method for accounts. I doubt I'll actually use
        this in the code but why not. Fun fact: I did!
        """
        return str(self.number)

    @staticmethod
    def _generate_number():
        """
        Generate a unique number for the account. Track all existing
        account numbers in a text file. This is totally secure.

        :return: num: str, a unique account number
        """
        # Check for existing accounts
        try:
            f = open('existing_accounts.txt', 'r')
            existing_accounts = f.readlines()
            f.close()
        except FileNotFoundError:
            existing_accounts = []

        # Generate an unused account number
        num = str(randint(1000000, 9999999))
        while num in existing_accounts:
            num = str(randint(1000000, 9999999))

        # Document the use of the new account number
        f = open('existing_accounts.txt', 'w+')
        f.writelines(existing_accounts + [num])
        f.close()
        
        return num

    @staticmethod
    def _generate_pin():
        """
        Generate a random PIN.

        :return: pin: str, a pin for the account
        """
        return str(randint(1000, 9999))

class Transaction:
    """
    A class to collect the attributes defining a transaction.
    """
    def __init__(self, account, how='add'):
        """
        Store the account and amount.
        """
        self.__account = account
        self.__amount = 0.0
        self.how = how
        return

    @property
    def account(self):
        """
        Make the account a read-only attribute
        """
        return self.__account

    @property
    def amount(self):
        """
        Make the amount a read-only attribute
        """
        return self.__amount

    @amount.setter
    def amount(self, amount):
        """
        When setting the amount, check that it is a positive float
        """
        assert isinstance(amount, float), "Amount must be a float"
        if self.how == 'add':
            assert amount >= 0, "Amount must be positive"
        elif self.how == 'subtract':
            assert amount <= 0, "Amount must be negative"
        else:
            raise YaSuckAtCodingError
        
        self.__amount = amount
        return
        
# Custom Exceptions
class YaBrokeException(Exception): pass
class YaHackinException(Exception): pass
class YaSuckAtCodingError(Exception): pass

# Functions for user interaction
def menu():
    """
    Prompt the user with a set of possible actions and return
    the choice.

    :return: choice: the user's selected action
    """
    print("What would you like to do?\n")
    print("  a) Make a deposit")
    print("  b) Make a withdrawal")
    print("  c) View balance")
    print("  d) Transfer funds to another account")
    print("  e) Close your account")
    print("  f) Log out")
    print("  q) Quit\n")
    choice = input("Your choice: ").strip().lower()
    while choice not in ['a', 'b', 'c', 'd', 'e', 'f', 'q']:
        print("You must choose from ['a', 'b', 'c', 'd', 'e', 'f', 'q'].")
        choice = input("Your choice: ").strip().lower()

    return choice

def connect(bank):
    """
    Ask the user to open a new account or log in to an 
    existing account.

    :param teller: Teller, the Teller instance of the program
    :return: account: Account, the opened or logged-into account
    """
    print("What would you like to do?\n")
    print("  a) Login")
    print("  b) Open a new account")
    print("  q) Quit\n")
    choice = input("Your choice: ").strip().lower()
    while choice not in ['a', 'b', 'q']:
        print("\nYou need to choose from ['a', 'b', 'q']")
        choice = input("Your choice: ").strip().lower()

    if choice == 'a':
        # Attempt to login to an existing account
        number = input("Please type your account number: ").strip()
        if number in bank.pins.keys():
            login_attempts = 0
            while login_attempts < 5:
                pin = input("Please type your PIN: ").strip()
                try:
                    account = bank.login(number, pin)
                    return account
                
                except YaHackinException:
                    print("Incorrect PIN. {} attempts remaining.".format(4 - login_attempts))
                    login_attempts += 1
            else:
                # Maximum attempts reached. Force quit.
                print("Login failed. Get out hacker.")
                choice = 'q'
        else:
            print("There is no account number {} on record. Please try again.\n".format(number))
            return connect(bank)

    if choice == 'b':
        # Open a new account
        account = bank.open_account()
        print("\nWelcome to your new account!")
        print("  - Account Number: {}".format(str(account)))
        print("  - PIN: {}\n".format(account.pin))
        return account

    if choice == 'q':
        # Donezo
        quit_session(bank)
              
    return

def welcome():
    """
    Welcome the user to the bank, but only if it is currently in
    operating hours.
    """

    time = datetime.datetime.now()
    if time.weekday() in (5, 6):
        print("The bank is closed on weekends.")
        sys.exit()
    elif time.hour < 9 or time.hour >= 17:
        print("The bank is only open from 9am to 5pm.")
        sys.exit()

    print("\n\n\t\tWelcome to the Bank!\n\n")
    return

def quit_session(bank):
    """
    The user is done, close the bank.

    :param bank: a Bank object
    """
    print("Goodbye!")
    bank.close_bank()
    return

# Main body
if __name__ == "__main__":
    # Welcome the user to the bank
    welcome()
    
    # Open the bank
    bank = Bank()

    # Have the user connect to a bank account
    account = connect(bank)

    # Prompt the user for an action
    choice = menu()
    while choice != 'q':

        # Make a deposit
        if choice == 'a':
            # Get the amount to deposit
            while True:
                try:
                    amount = float(input("Please enter the amount of the deposit: $"))
                    break
                except ValueError:
                    print("You must enter a numeric value, goofball.")

            # Execute the deposit
            try:
                bank.make_deposit(account, amount)
                print("Deposit was successful. New balance is ${0:.2f}\n".format(account.balance))
            except AssertionError:
                print("You must specify a positive numeric value to deposit.")
                print("Deposit attempt failed becasue ya dumb.")

        # Make a withdrawal
        elif choice == 'b':
            # Get the amount to withdraw
            while True:
                try:
                    amount = float(input("Please enter the amount of the withdrawal: $"))
                    break
                except ValueError:
                    print("You must enter a numeric value, goofball.")

            # Execute the withdrawal
            try:
                bank.make_withdrawal(account, amount)
                print("Withdrawal was successful. New balance is ${0:.2f}\n".format(account.balance))
            except AssertionError:
                print("You must specify a positive numeric value to withdraw.")
                print("Withdrawal attempt failed becasue ya dumb.\n")
            except YaBrokeException:
                print("You do not have enough money in your account for that withdrawal.")
                print("Withdrawal attempt failed becasue ya broke.\n")
        
        # View balance
        elif choice == 'c':
            print("\nYour balance is ${0:.2f}\n".format(account.balance))

        # Wire transfer
        elif choice == 'd':
            # Get account to transfer funds to
            to_account_number = input("Enter the account you would like to send funds to: ").strip()
            while not to_account_number.isnumeric() or len(to_account_number) != 7:
                print("You have to enter a 7-digit number, goofball")
                to_account_number = input("Enter the account you would like to send funds to: ").strip()

            # Determine if the account exists
            if to_account_number not in bank.accounts.keys():
                new_choice = input("There is no account found with that number. Would you like to open one? (y/n) ").strip().lower()
                while new_choice not in ['yes', 'no', 'y', 'n']:
                    new_choice = input("Please enter 'yes' or 'no': ")

                # Make a new account if desired or give up on the transfer
                if new_choice in ['yes', 'y']:
                    to_account = bank.open_account(number=to_account_number)
                    print("\nWelcome to your new account!")
                    print("  - Account Number: {}".format(str(to_account)))
                    print("  - PIN: {}\n".format(to_account.pin))
                
                # Give up on the fool
                elif new_choice in ['no', 'n']:
                    print("Idk where you want me to send this money then fam.")
                    print("Wire transer failed becasue ya dumb.\n")
                    choice = menu()
                    continue
                    
                # The code should never get here
                else:
                    raise YaSuckAtCodingError
            
            # Get amount to transfer
            while True:
                try:
                    amount = float(input("Please enter the amount of the transfer: $"))
                    break
                except ValueError:
                    print("You must enter a numeric value, goofball.")

            # Execute transfer
            try:
                bank.make_wire(account, bank.accounts[to_account_number], amount)
                print("Transfer successful. New balance is ${0:.2f}\n".format(account.balance))
            except AssertionError:
                print("You must specify a positive numeric value to transfer.")
                print("Transfer attempt failed becasue ya dumb.\n")
            except YaBrokeException:
                print("You do not have enough money in your account for that transfer.")
                print("Transfer attempt failed becasue ya broke.\n")

        # Close account and log out
        elif choice == 'e':
            try:
                bank.close_account(account)
                account = connect(bank)
            except YaBrokeException:
                print("You cannot close an account with a negative balance.\n")

        # Log out
        elif choice == 'f':
            account = connect(bank)
            
        # The code should never get here
        else:
            raise YaSuckAtCodingError

        # Figure out what the user wants to do next
        choice = menu()

    else:
        # The user has chosen to quit
        quit_session(bank)
        
