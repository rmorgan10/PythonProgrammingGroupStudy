# OOP

## Concepts and Terminology
* _class_, _data type_, and _type_ are interchangeable (in this book)
* _object_, _instance_ instance of a particular class
* _special methods_ methods with syntax **\_\_method_name__** and are pre-defined
* attributes are implemented as _instance variables_, variables unique to a particular object.
    * defined as **self.variable_name** within the body of a method
* _properties_ item of object data that is accessed like an _attribute_ but methods handle the access behind the scenes
    * Data validation
* _Class variables_ or _static variables_ variables that are properties of a class. Often defined before **\_\_init__**
* _subclass_ and _specialize_, V, to make a sub-version of an existing class
* _super class_ or _base class_ is a class that is inherited
* _sub class_, _derived class_, _derived_, a specialized version of an existing class
* calling an method overwritten in a subclass: Python's use of the overwritten method is: _dynamic method binding_ or _polmorphism_
* _duck typing_ : if it walks like a duck and quacks...
* No overloading in python: methods with same name but different arguments (types, number-of) are called depending on arguments passed
* No good access control (No true private methods or attributes)

## Custom Classes:
* Syntax
*       class className(base_class):
            suite

### Attributes and Methods
* When a class is instantiated
    * first **\_\_new__()** is called
    * then **\-\_init__()** is called
    * normally the base object **\_\_new__()** is good enough, and doesn't need to be overwritten like **\_\_init__**
* By default, all instances of custom classes are hashable
    * replacing **\_\_eq()__** makes them no longer hashable
    * this can be fixed (see FuzzyBool)
* Special comparison methods (eg **\_\_eq()__**) will try to compare anything that doesn't raise an error in the body. To fix:
    1.      Assert isintance(other, type(self))
    2.      if not isintance(other, type(self)):
                raise TypeError()
    3.      if not isintance(other, type(self)):
                return NotImplemented
    * third option is most "pythonic" makes use of python's built-in functionality to look for suitable method in the *other* type, raising type error on a failure
    
### Inheritance and polymorphism


### Using Properties to control attribute access
* Can implement simple methods to act like (read-only) attributes eg:
    *   @property
        def distance(self,origin=None):
            if origin == None:
                origin = Point(0,0)
            return math.sqrt((self.x-origin.x)**2+(self.y-origin.y)**2)
    can be called
    * Point(x,y).distance(Point(xp,yp))
* @property can be used for getter, setter, deleter functions and a docstring eg:
    *       @property
            def radius(self):
                """
                the docstring goes here
                """
                return self.__radius
             
            @property.setter(self, radius):
                assert radius > 0, "radius must be > 0"
                self.__radius = radius
   * without the setter or deleter functions the attribute in question cannot be modified or deleted, respectively

### Creating Complete Fully Integrated Data Types (from scratch)
* instead of inheriting from **object** inherit from an existing data type that is similar to what we want
* We have to re-implement methods we want to behave slightly differenetly, and Un-implement those we dont want
* To make a class with overwritten **\_\_eq()__** method hashable, provide a **\_\_hash()__** special method
    * you should probably give it the object's unique id (*id(self)*). Or something else unique to the *object* that won't change as the object is used
* You gotta make it hashable
* Page 246 of pdf for reference
### Creating data types from other data types
* When creating an immutable type, gotta overwrite the **\_\_new()__** method since, once created, an immutable object can't be changed
* **\_\_new()__** is a class method
* other class methods can be defined using @classmethod
    * syntax:
    *       @classmethod
            def method_name(cls,*args):
                suite
    * cls is the default first variable, provided by python. Like self, but the class is passed instead of the object
    * to unimplement we can:
        *       def __add__(self,other):
                    raise NotImplementedError()
        * More pythonic
        *       def __add__(self, other):
                    raise TypeError("unsupported operand tyoe(s) for +:"
                                    "'{0}' and '{1}'".format(
                                self.__class__.__name__,other.__class__.__name__))
        * For unary operations
        *       def __neg__(self):
                    raise TypeError("bad operand type for unary -: '{0}'".format(
                        self.__class__.__name__))
        * for comparisons
        *       def __eq__(self,other):
                    return NotImplemented
* to unimplement more systematically, look at pdf pg 256

## Custom Collection Classes