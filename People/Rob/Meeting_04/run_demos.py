# A module to use the demos package

import pyfiglet

import demos.demo_logging as demo_logging

# Instantiate Figlets for pretty text
speed = pyfiglet.Figlet(font='speed')
print_speed = lambda s: print(speed.renderText(s))
invita = pyfiglet.Figlet(font='invita')
print_invita = lambda s: print(invita.renderText(s))

def run_logging_demo():
    """
    Execute functions in demos.demo_logging
    with some extra annotations
    """
    # Display a header
    print_speed("Logging Demo")

    # Execute tutorial functions
    print_invita("The Basics")
    print("\n\nHere's what the demo is doing:\n\n")
    demo_logging.basic()
    print("\n\n")
    print_invita("Advanced")
    print("\n\nHere's what the demo is doing:\n\n")
    demo_logging.advanced()
    print("\n\n")
    print_invita("Config File")
    print("\n\nHere's what the demo is doing:\n\n")
    demo_logging.config()
    
    return

run_logging_demo()
