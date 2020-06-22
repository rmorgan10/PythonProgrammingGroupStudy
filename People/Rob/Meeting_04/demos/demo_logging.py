# A module to demo python's built-in logging package

import inspect
import logging

def getting_started():
    """
    Shows how to utilize the basic functions of logging.
    """
    # For demo, print function body to terminal
    print(inspect.getsource(inspect.currentframe().f_code))
    
    # Start by setting the logging.basicConfig() parameters
    logging.basicConfig(filename="demo_logging.log",
                        filemode="w+",
                        format="%(asctime)s %(levelname)s: %(message)s",
                        level=logging.DEBUG
    )

    # As the program runs, you add to the log by specifying
    # the level of the entry
    logging.debug("debug messages are the most detailed information")
    logging.debug("debug messages are only of interest when diagnosing problems")
    logging.info("info messages are used to mark that the program has reached a certain point")
    logging.warning("warning messages are used when an action could be problematic later")
    logging.error("error messages are used when the software failed to perform a task")
    logging.error("error messages are typically contained in except blocks of code")
    logging.critical("critical messages mark when the program will terminate")

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
    """
    # For demo, print function body to terminal
    print(inspect.getsource(inspect.currentframe().f_code))



    return



# Main body
if __name__ == "__main__":
    # Automatic testing of code examples in docstrings
    import doctest
    doctest.testmod()
    
    # Run the getting_started function
    getting_started()

    # Run the advnaced function
    advanced()
