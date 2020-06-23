# A module to demo python's built-in logging package

import inspect
import logging
import logging.config

def basic():
    """
    Shows how to utilize the basic functions of logging.
    -- using basicConfig for straightforward logging
    """
    # For demo, print function body to terminal
    print(inspect.getsource(inspect.currentframe().f_code))
    
    # Start by setting the logging.basicConfig() parameters
    logging.basicConfig(filename="demo_logging.log",
                        filemode="w+",
                        format="|%(levelname)s:%(name)s\t| %(asctime)s -- %(message)s",
                        datefmt="%I:%M:%S %p",
                        level=logging.DEBUG)

    # As the program runs, you add to the log by specifying
    # the level of the entry
    logging.debug("debug messages are the most detailed information")
    logging.debug("debug messages are only of interest when diagnosing problems")
    logging.info("info messages are used to mark that the program has reached a certain point")
    logging.warning("warning messages are used when an action could be problematic later")
    logging.error("error messages are used when the software failed to perform a task")
    logging.error("error messages are typically contained in except blocks of code")
    logging.critical("critical messages mark when the program will terminate")

    # An additional level (excpetion) should only be used in an except block
    try:
        assert False
    except:
        logging.exception("exception messages will log the traceback too!")
    
    # Signal the end of logging and write the log file
    logging.shutdown()

    # We can check the contents of the log file
    print("> getting_started LOGFILE")
    with open('demo_logging.log', 'r') as logfile:
        for line in logfile:
            print(line, end='')
    
    return

def advanced():
    """
    Shows advanced features of the logging module.
    -- We'll now do the basicConfig operations manually, 
       which enable much more freedom
    """
    # For demo, print function body to terminal
    print(inspect.getsource(inspect.currentframe().f_code))

    # Create a logger and name it after the module
    logger = logging.getLogger(__name__.replace('__', ''))

    # Set the level of the logging
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set its level
    handler = logging.FileHandler("demo_logging_advanced.log", mode='w+')
    handler.setLevel(logging.DEBUG)

    # Create a formatter and attach it to the handler
    formatter = logging.Formatter(fmt="|%(levelname)s:%(name)s\t| %(asctime)s -- %(message)s",
                                  datefmt="%I:%M:%S %p")
    handler.setFormatter(formatter)

    # Now connect the formatted handler to the logger
    logger.addHandler(handler)

    # Add messages to the log just like before
    logger.debug("This is a debug level message")
    logger.info("This is an info level message")
    logger.warning("This is a warning level message")
    logger.error("This is an error level message")
    logger.critical("This is a critical level message")

    # Signal the end of logging and write the log file
    logging.shutdown()
            
    # We can check the contents of the log file
    print("> advanced LOGFILE")
    with open('demo_logging_advanced.log', 'r') as logfile:
        for line in logfile:
            print(line, end='')

    return

def config():
    """
    Use a config file to initialize all logging
    """
    # For demo, print function body to terminal
    print(inspect.getsource(inspect.currentframe().f_code))
    
    # Specify the logger parameters using a config file
    logging.config.fileConfig('demo_logging.conf')
    logger = logging.getLogger('main')

    # Display the contents of the config file
    print("> config file")
    with open('demo_logging.conf', 'r') as config_file:
        for line in config_file:
            print(line, end='')

    # Add messages to the log just like before
    logger.debug("This is a debug level message")
    logger.info("This is an info level message")
    logger.warning("This is a warning level message")
    logger.error("This is an error level message")
    logger.critical("This is a critical level message")

    # Signal the end of logging and write the log file
    logging.shutdown()

    # We can check the contents of the log file
    print("> config LOGFILE")
    with open('demo_logging_advanced.log', 'r') as logfile:
        for line in logfile:
            print(line, end='')
    
    return

# Main body
if __name__ == "__main__":
    # Automatic testing of code examples in docstrings
    import doctest
    doctest.testmod()
    
    # Run the getting_started function
    basic()

    # Run the advnaced function
    advanced()

    # Run the config function
    config()
