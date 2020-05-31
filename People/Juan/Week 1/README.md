# Week 1 - Rapid Intro and Data Types

## Notes
### Rapid Intro to Procedural Programing

* both *str* and basic numeric types (e.g _int_) are **immutable** - Once set, their values cannot 
be changed.
    * the following code raises a TypeError:
    * Look at **immutable**
> st = "sfsdfesaf"\
> st[-1] = 'a'
>> TypeError: 'str' object does not support item assignment

#### Object References
* No such thing as variables, just references to immutable objects (e.g _int_ and _str_)
* Variable and object reference used interchangably in text
* Sample code
> x = "blue"
> z = x
* First creates str("blue") object, then creates reference to said object, called x. Second 
statement creates a new reference that points to the same object
* objects are auto-garbage collected when no references to them remain
#### Collection data types
* Lists and Tuples don't hold data items, they hold object references.
#### Identity operator
* _is_ operator tells if two references refer to the same object
* _==_ operator compares **value** of objects being referred to
* Should take care when comparing values of string containing non-ACSII characters
* Can use _in_ operator to check for sub-phrases in strings
#### Arithmetic Operators
* / produces floats
* // produces ints 
* += creates new (int,float,str) object, doesn't change value of existing one
#### I/O
* input(prompt: str); Reads str from standard input. prompt is printed to std out to prompt user
* >\>> python _pyfile.py_ < _textfile_
* runs _pyfile.py_ with contents of _textfile_ as input to std_in

### Data Types
* Bitwise operators can be written as 
> i op= j $\equiv$ i = i op j
* Operators
    * i | j     : bitwise OR (negative numbers are assumed to be using 2's complement)
    * i ^ j     : bitwise XOR
    * i & j     : bitwise AND
    * i << j    : shits i left by j bits; like i*(2**j) w/o overflow checking
    * i >> j    : shifts i right by j bits; like i//(2**j) w/o overflow checking
    * ~i        : Inverts i's bits
* Floats are approximations due to base 2. decimal.Decimal get around this at the cost of 
performance
* Complex numbers can't use //, %, or divmod() operations
* cmath module provides complex number versions of trig and log functions, plus more!
* Get around regex issues when "\\" is needed by usuing r"", raw strings
* Comparison operators compare strings byte-by-byte


## Python Quizmaster
Develop an interactive multiple choice quiz matching python built in keywords to a one-sentence 
definition you write for them. All keywords can be found by typing dir(\_\_builtins__)  into
an interactive python session. Research each one and construct a mapping of keywords to 
definitions. Then develop functionality to prompt the user with the correct answer and three 
wrong answers (perhaps chosen randomly from your bank of definitions). Collect the response for
each question and output a quiz summary at the end. Be as extra as you please.

###Builtins
>\_\_class__\
>\_\_contains__\
>\_\_delattr__\
>\_\_delitem__\
>\_\_dir__\
>\_\_doc__\
>\_\_eq__\
>\_\_format__\
>\_\_ge__\
>\_\_getattribute__\
>\_\_getitem__\
>\_\_gt__\
>\_\_hash__\
>\_\_init__\
>\_\_init_subclass__\
>\_\_iter__\
>\_\_le__\
>\_\_len__\
>\_\_lt__\
>\_\_ne__\
>\_\_new__\
>\_\_reduce__\
>\_\_reduce_ex__\
>\_\_repr__\
>\_\_reversed__\
>\_\_setattr__\
>\_\_setitem__\
>\_\_sizeof__\
>\_\_str__\
>\_\_subclasshook__\
>clear\
>copy\
>fromkeys\
>get\
>items\
>keys\
>pop\
>popitem\
>setdefault\
>update\
>values

## Pi Writing Contest
Write a script to print as many digits of pi as possible. You will have to address the concepts of 
float precision and memory allocation (and perhaps even string formatting) to get lots of digits. 
Convert your result to a string and compare element-wise to a string of pi copied from the internet.
Output the number of decimal places you get correct. Bonus points for a fun visualization.