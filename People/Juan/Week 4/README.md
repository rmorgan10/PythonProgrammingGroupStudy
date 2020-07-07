# Banking Assignment

Based on problems 3 and 4 in the book (chapter 6: OOP)

## Part 1
Make a class that processes transactions:
* adding money to your account
* removing money
* converting your funds from one currency to another (bonus points for neat currency options)).

It’s recommended that your class takes in an :
* amount
* date
* currency (specifying a default)
* a conversion rate (default 1)
* a description (default None).

## Part 2
Make an account class that stores account info :
* account number
    * Read only property
* name
    * read-write property, with assertion to enusre it is at least 4 characters long
* a list of transactions

* class should support len(), returning the number of transactions

Should provide the calculated, read-only properties:
* balance.
    * Returns balance in USD
* all_usd
    * Returns True if all transactions are in USD, False otherwise

Three other methods should be provided:
* apply()
    * to apply (add) a transaction
* save() and load()
    * should use a binary pickle with the filename being the account number with extension .acc
    * They should save and load the account number, name, and all transactions.
    
Can be implemented in about 90 lines.

The prompt asks you to be able to save and load data from a file. We can get so extra as to have it :
* output your account balance in all sorts of fun ways
* allow the user to transfer money from one account to another
* calculate returns from dividends.  

As extra as you want.