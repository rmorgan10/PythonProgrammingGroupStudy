# A module to define the banking classes

from collections import defaultdict
import os
from random import randint
import sqlite3

class Bank:
    def __init__(self):
        self.accounts = defaultdict(lambda: Account())
        self.pins = {}
        self.ledger = []
        self.load_ledger()
        return

    def load_ledger(self):
        if not os.path.exists('bank_ledger.db'):
            self.conn = sqlite3.connect('bank_ledger.db')
            c = self.conn.cursor()
            c.execute("""CREATE TABLE accounts
                         (number text, pin text)""")
            c.execute("""CREATE TABLE transactions
                         (number text, amount real)""")
            self.conn.commit()
        else:
            self.conn = sqlite3.connect('bank_ledger.db')
            self.update_accounts()
        return

    def update_ledger(self):
        while len(self.ledger) > 0:
            transaction = self.ledger.pop()
            c = self.conn.cursor()
            c.execute("""INSERT INTO transactions 
                         VALUES ({0}, {1})""".format(transaction.account,
                                                     transaction.amount))
            self.conn.commit()
        return

    def update_accounts(self):
        c = self.conn.cursor()
        c.execute("""SELECT * FROM accounts""")
        for num, pin in c.fetchall():
            self.pins[num] = pin
            
        c.execute("""SELECT * FROM transactions""")
        for num, amount in c.fetchall():
            self.accounts[num].balance += amount

        return

    def close_bank(self):
        self.conn.close()
        return
    
class Teller(Bank):
    def __init__(self, bank=None, ledger=None):
        if bank is not None:
            self.accounts = bank.accounts
            self.pins = bank.pins
            self.ledger = bank.ledger
            self.conn = bank.conn
        else:
            super().__init__()

        return

    def open_account(self):
        account = Account()
        account_pin = account._generate_pin()
        self.accounts[account.number] = account
        self.pins[account.number] = account_pin

        self.conn.execute("""INSERT INTO accounts
                             VALUES ({0}, {1})""".format(account.number, account_pin))
        self.conn.commit()
        return account

    def close_account(self, account):
        if account.balance < 0.0:
            raise YaBrokeException
        self.make_withdrawal(account, account.balance)
        del self.accounts[account.number]
        del self.pins[account.number]
        return

    def login(self, number, pin):
        if self.pins[number] != pin:
            raise YaHackingException
        return self.accounts[number]
    
    def make_deposit(self, account, amount):
        self._make_transaction(account, amount)
        return

    def make_withdrawal(self, account, amount):
        if amount < account.balance:
            raise YaBrokeException

        self._make_transaction(account, -1.0 * account.balance)
        return

    def make_wire(self, from_account, to_account, amount):
        self.make_withdrawal(from_account, amount)
        self.make_deposit(to_account, amount)
        return

    def _make_transaction(self, account, amount):
        self.ledger.append(Transaction(account, amount))
        self.accounts[account.number].balance += amount
        self.update_ledger()
        return

class Account:
    def __init__(self, number=None, balance=0.0):
        if number is None:
            number = self._generate_number()
        self.number = number
        self.balance = balance
        return

    def __str__(self):
        return str(self.number)

    @staticmethod
    def _generate_number():
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
        return str(randint(1000, 9999))

class Transaction:
    def __init__(self, account, amount):
        self.__account = account
        self.__amount = amount
        return

    @property
    def account(self):
        return self.__account

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, amount):
        assert isinstance(amount, float), "Amount must be a float"
        assert amount > 0, "Amount must be positive"
        self.__amount = amount
        return
        

class YaBrokeException(Exception): pass
class YaHackinException(Exception): pass


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
