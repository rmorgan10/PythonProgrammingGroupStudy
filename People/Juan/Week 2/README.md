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
    *     namedtuple(\
               name: str,
              names: str, 
          )
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
* **for** and **while** loops have an **else** clause
*     for ... in : 
            <code>
      else: '
    * **else** is not executed if a **break**, **return** or error terminates the loop
### Exception Handling
#### Catching and Raising Exceptions
*Full Syntax (**else** and **finally** are optional)
*       try:
            try_suite
        except exception_group1 as variable1:
            except_suite1
        ...
        except exception_groupN as variableN:
            except_suiteN
        else:
            else_suite
        finally:
            finally_suite
* **else** is executed if **try** suite is executed normally, but not if any exception is raised.
* **finally**  is *always* executed at the end. 
    * Even if an uncaught exception is thrown.
    * Even if a try_suite or except_suite includes a **return** statement (it's called right before the **return** is executed?)
* the except_groups are single exception classes or tuples of exception classes
* Exceptions are caught by the first except block where the thrown exception (or any of its "parent" classes) are in the except_group
* A **try**..**finally** suite is also available
*       try:
            try_suite
        finally:
            finally_suite
##### Raising Exceptions
* Syntax
*       raise exception(args)
*       raise exception(args) from original_exception
*       raise
* Last two should only be used inside except suites
* Second one raises exception as a chained exception (Chp 9) that includes the original.
* **Typo>??** book says empty **raise** statement should cause a **TypeError**. Causes a **RuntimeError** in my jupyter notebook.
#### Custom Exceptions
* Can define a bare exception with:
*       class ExceptionName(baseException): pass

### Custom Functions
* Global Functions: Functions accessible anywhere in the module and anywhere that inherits the module
* Local Functions: Functions within a function (Chp 7)
* Lambda Functions: expressions, can be created at their point of use
* Methods: Functions associated with a particular data type (Object/class?)
*       def func(var=class()):
* is bad form. class is instantiated when the function is *created* and not again. If function is called multiple times, var will still refer to the same object
*

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