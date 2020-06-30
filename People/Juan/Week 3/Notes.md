# Modules

* Module - Collection of functions
* Package - Collection of modules that are grouped together because they're either related or interdependent

## Modules and Packages
* A module is a .py file designed to be imported and used by other programs
* Not all modules are associated with .py files. eg sys
* syntax
*       import importable
        import importable1, importable2 ...
        import importable as prefered_name
* importable can be a module, package or module within a package
    * In the last case syntax is  
    *       import package.module
* Common practice is imports go after shebang line and module documentation
* Standard library import first, then third-party modules, then our own
* other syntaxes
*       from importable import object as preferred_name
        from importable import object1, object2, ...
        from importable import (object1, object2, ..., objectN)
        from importable import *
* can cause name conflicts!
* The last syntax imports all non-private objects
    * practically, all items not prepended by __
    * Or, if a global __all__ variable is defined, all objects names in the __all__ list are imported
    * importable is a package, it imports all modules
* sys.path holds list of directories that make the python path
    * first is program directory (even if invoked from other directory)
    * Then PYTHONPATH if specified
    * Then path needed for standard library (set on python install)
* Imported modules are looked for in sys.path
* If we write a module with the same name as a standard module our module will overwrite the standard one
    * Use only if purposely overwriting the module in question

## Packages
* package: a directory that contains a set of modules and a file called *\_\_init__.py*
* To be able to import all modules in a package at once, (from package import *) add this line to *\_\_init__.py*
*       __all__ = ["module1","module2",...]
* Packages can be nested to arbitrary depth

## Custom Modules
* Making a custom module is as easy as defining a bunch of functions within a .py file
* To make it available to all our python programs we can
    * Put the module in the _site-packages_ directory
        * Windows(usually) : C:\Python31\Lib\site-packages
        * Unix : varies
    * Create a directory for our custom modules and have PYTHONPATH set to that directory
    * Put it in the **local** _site-packages_ sub-directory
        * %APPDATA%\Python\Python3x\site-packages
* To test examples in docstring use
*       if __name__ == "__main__":
            import doctest
            doctest.testmod()
* When a module is imported _\_\_name___ is that module's filename without the .py extension

## Overview of standard library
