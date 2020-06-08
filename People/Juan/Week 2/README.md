# Collection Data Types, Control Structures, and Functions


## Collection Data Types (pgs 107 - 158)
### Sequence Types
a _sequence_ is a type that supports the **in** operator, the **len()** function,
slices, and is iterable.
5 Builtin ones : *bytearray*, *bytes*, *list*, *str*, and *tuple*
When iterated, items are provided in order

#### Tuples
* Ordered sequence of 0 or more object references. Immutable like strings.
* some available Functions : 
    * *t.count(x)* : returns number of times object *x* appears in tuple t
    * *t.index(x)* : returns index of leftmost occurance of *x* in tuple t
* Operators (+, *, \[](slice), and in) act as with lists (and with strings)
* Comparison (<, <=, ==, !=, >=, >) compare item by item and recursively (as w/ lists)

#### Named Tuples
* Same as tuple but with ability to refere to items by name as well as index position
* Provided in collections.namedtuple
* syntax:
    * > namedtuple(
    * >     name: str,
    * >     names: str, 
    * >)
    * names should be a space separated string of names that items in the custom tuple should take 
    * e.g "A B C D" gives names A, B, C, D accessible as class attributes, t.A, t.B,...

#### Lists
* list(\<list object>) returns a shallow copy of the argument
* 
##### List Comprehensions

### Set types
#### Sets
#### Set Comprehensions
#### Frozen Sets

### Mapping Types
#### Dictionaries
##### Dictionary Comprehensions
#### Default Dictionaries 
* Look at this for instrument server
#### Ordered Dictionaries

### Iterating and Copying Collections
#### Iterators and Iterable Operations and Functions
#### Copying Collections


## Control Structures and Functions (pgs 159 - 194)

### Control Structures
#### Conditional Branching
#### Looping

### Exception Handling
#### Catching and Raising Exceptions
#### Custom Exceptions

### Custom Functions
#### Names and Docstrings
#### Arguments and Parameter Unpacking
#### Accessing Variables in the Global Scope
#### Lambda Functions
#### Assertions


## Assignment ideas

### Py Calendar
Build a functioning calendar. 
* It should print today's date, month and year and display
the days of the month in standard calendar format
* Allow the user to scroll through months and years with ease, 
* Allow the user to get, set and modify events on certain days using the command prompt/terminal.
* Allow user to exit without keyboard interrupts
* Be nice to the user!

### Error Madness
Create a custom Error class that raises a random builtin Warning in the constructor

### 