# The Standard Library on Parade

Chapter 5 describes how to make your code into an importable package, and then details a handful of packages that come pre-installed with python.
There are hundreds more packages that constitute the Standard Library (SL) of pre-installed packages (https://docs.python.org/3/library/index.html).

**Your task:** create a demos module that demonstrates important properties of 3 (or more if you want) Standard Library packages that you think you may use at some point in your research. 

_Example:_ With your demos module (and assuming you selected glob as one of your SL packages), you should be able to use the interactive python prompt like this:

```python
>>> from demos.demo_glob import run_demo
>>> run_demo()
```

And the run_demo() method will begin a demonstration of some of the utilities of glob (which can be interactive if you so choose / see fit)

- Bonus points: do more than 3 SL packages
- Super bonus points: make your package pip-installable (just build the wheel, no need to upload to PyPi)