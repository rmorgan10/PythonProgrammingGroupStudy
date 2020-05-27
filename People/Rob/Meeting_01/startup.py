# python startup file
import readline
import rlcompleter
import atexit
import os
import sys
import datetime
import colorama

# tab completion
readline.parse_and_bind('tab: complete')

# history file
histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
try:
    readline.read_history_file(histfile)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

# add time and color
colorama.init(autoreset=True)

class Prompt:
  def __str__(self):
    print(self.prompt, end='')
    return ''

class PS1(Prompt):

  @property
  def prompt(self):
    return '{brace_c}[{time_c}{time}{brace_c}]{prompt_c}>>> '.format(
              brace_c  = colorama.Fore.BLACK + colorama.Style.BRIGHT,
              # style is preserved, so the following are also bright:
              prompt_c = colorama.Fore.LIGHTGREEN_EX,
              time_c   = colorama.Fore.BLACK,
              time     = datetime.datetime.now().strftime('%H:%M'),
            )

sys.ps1 = PS1()

# clean up imports
del os, histfile, readline, rlcompleter