import datetime
import os

class Money:
    """ Class for Money
    
    """
    def __init__(self, amt, currency):
        self.amt = amt                    # Amount
        self.currency = currency          # Currency
        return 
     
    """
    def currency_conv(self.currency, original, new):
        # Converting money within currency
        # For example: in USD, from Cents to Dollars
        rates = {
            "USD": {"dollar": 1, "cent": 100},
            "Swiss Francs": {"dollar": 1, "cent": 100},
            "HP": {"Galleon": 1, "Sickle": 17, "Knut": 493}
                }
        return rates
    """
            
    def conv_rates(self, original, new):
        # Converting money between currencies
        # For example, converting USD to 
        originals = ["USD", "Swiss Francs", "Euros", "Republic Credits", "Yen", "HP"]
        rates = {
            originals[0]: [1, 1.2, 0.8, 2.5, 0.01, 1.1]
        }
        return rates[original][originals.index(new)], self

class Tr(Money):
    """ Class for money transactions.
    
      Initialize the transaction object, then call the function that
      performs the desired transaction
    """
    
    def __init__(self, amt, date, currency='USD', conv_rate=1, desc=''):
        super().__init__(amt, currency)   # Amount and Currency
        self.date = date                  # Date
        self.conv_rate = conv_rate        # Conversion Rate
        self.desc = desc                  # Description
        return
        
    def tfr_in(self):
        self.amt = self.amt
        self.desc = "TfrIn:  " + self.desc
        return self
        
    def tfr_out(self):
        self.amt = -1 * self.amt
        self.desc = "TfrOut: " + self.desc
        return self
             
    def convert(self, new): 
        rate = self.conv_rates(self.currency, new)
        self.amt = self.amt*rate
        self.currency = new
        self.desc = "Conv:   " + self.desc
        return self
    
    def as_str(self):
        output = f"{self.date}: {self.amt} {self.currency} \n"
        output += f"\t{self.desc}"
        return output
        
    def printout(self):
        print(self.as_str())
        return 
        
class Acct:
    """ Class for Accounts
    
      ;lasdkjf
      a;lskdfja
    """
    
    def __init__(self, bal, name, num, usr, typ, hist):
        self.bal = bal     # current balance, 
                           #       dictionary of balances, keys = currencies
        self.name = name   # account name
        self.num = num     # account number
        self.typ = typ     # account type (checking or savings)
        self.usr = usr     # account holder name
        self.hist = hist   # transaction history (list)
        return 
       
    def display(self):
        out = "~  ~~  ~  ~~  ~  ~~  ~  ~~  ~  ~~  ~\n"
        out += f"{self.name} - {self.num}\n"
        out += f"\tAccount Type:   {self.typ}\n"
        out += f"\tAccount Holder: {self.usr}\n"
        out += "~  ~~  ~  ~~  ~  ~~  ~  ~~  ~  ~~  ~\n"
        out += "  Current Balance: \n"
        for currency in self.bal: 
            out += f"    {currency} {self.bal[currency]}\n"
        out += "~  ~~  ~  ~~  ~  ~~  ~  ~~  ~  ~~  ~\n"
        out += "  Recent History: \n"
        tmp_list = self.hist
        tmp_list.reverse()    # Print 3 most recent entries
        for h in tmp_list[:3]:
            out += f"    {h.as_str()}\n"
        out += "~  ~~  ~  ~~  ~  ~~  ~  ~~  ~  ~~  ~\n"
        print(out)
        return 
        
    def transaction(self, in_Tr):
        if in_Tr.desc[:5] == 'Conv:': 
            for update in in_Tr:
                if update.currency in bal.keys():
                    bal[update.currency] += update.amt
                    self.hist.append(update)
                elif update.currency not in bal.keys() and update.amt < 0: 
                    print("Cannot compute. No money to withdraw.")
                    break
                else: 
                    bal[update.currency] = update.amt
                    self.hist.append(update)
        else: 
            if in_Tr.currency in self.bal.keys():
                self.bal[in_Tr.currency] += in_Tr.amt
                self.hist.append(in_Tr)
            elif in_Tr.currency not in self.bal.keys() and in_Tr.amt < 0: 
                print("Cannot compute. No money to withdraw.")
            else: 
                self.bal[in_Tr.currency] = in_Tr.amt
                #self.update_history(in_Tr)
                self.hist.append(in_Tr)
        return self
        