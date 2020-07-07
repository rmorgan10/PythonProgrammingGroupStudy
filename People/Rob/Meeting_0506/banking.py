# A module to define the banking classes

class Bank:
    def __init__(self):
        self.accounts = {}
        self.pins = {}
        return

class Teller(Bank):
    def __init__(self):
        super().__init__()
        return

    def open_account(self):
        return

    def close_account(self):
        return

    def login(self):
        return
    
    def make_deposit(self):
        return

    def make_withdrawal(self):
        return

class Account:
    def __init__(self, number):
        self.number = number
        return

    def __str__(self):
        return str(self.number)

    def withdrawal(self):
        return

    def deposit(self):
        return


