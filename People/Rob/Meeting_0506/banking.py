# A module to define the banking classes

from collections import defaultdict
import os
from random import randint
import sqlite3

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
        return
    
class Teller(Bank):
    """
    The Teller class inherits the attributes of the bank class
    and provides additional functionalities for making transactions.
    """
    def __init__(self, bank=None, ledger=None):
        """
        Create a Teller instance. If a Bank object is passed as an
        argument, its attributes are inherited.
        
        :param bank: Bank, an existing bank instance.
        :param ledger: list, a list of Transactions made in the bank
        """
        if bank is not None:
            # Store the attributes of an existing Bank
            self.accounts = bank.accounts
            self.pins = bank.pins
            self.ledger = bank.ledger
            self.conn = bank.conn
        else:
            # Make an and inherit an empty Bank
            super().__init__()

        return

    def open_account(self):
        """
        Create a new account. Generate a new account number and PIN. 
        Add the account to the database.

        :return: account: An Account instance for the object just created
        """
        # Make a new account
        account = Account()
        account_pin = account._generate_pin()

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
        if amount < account.balance:
            raise YaBrokeException

        # Make a negative transaction
        self._make_transaction(account, -1.0 * account.balance)
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

    def _make_transaction(self, account, amount):
        """
        Document the transaction, adjust the account balance, and 
        update the ledger database.

        :param account: Account, the account to make the transaction with
        :param amount: float, the amount of the transaction
        """
        self.ledger.append(Transaction(account, amount))
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
        return

    def __str__(self):
        """
        Reimplement the str method for accounts. I doubt I'll actually use
        this in the code but why not.
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
    def __init__(self, account, amount):
        """
        Store the account and amount.
        """
        self.__account = account
        self.__amount = amount
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
        assert amount > 0, "Amount must be positive"
        self.__amount = amount
        return
        

# Custom Exceptions
class YaBrokeException(Exception): pass
class YaHackinException(Exception): pass

# Main body
if __name__ == "__main__":
    b = Bank()
    teller = Teller(b)

    acct = teller.open_account()
    teller.make_deposit(acct, 100.0)

    print(b.accounts.keys())
    print(list(b.accounts.values())[0].balance)
    print(b.pins)
    print(b.ledger)

    print(teller.accounts.keys())
    print(list(teller.accounts.values())[0].balance)
    print(teller.pins)
    print(teller.ledger)
