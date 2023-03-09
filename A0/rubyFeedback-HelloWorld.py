# =========================================================================== #
# === Helloworld
#
# The assignment task can be read here:
#
#   https://github.com/TBIAPBC/APBC2023/tree/main/A0
#
# =========================================================================== #
import sys
from pathlib import Path

class HelloWorld:

  # ========================================================================= #
  # === TEXT_TO_ADD
  # ========================================================================= #
  TEXT_TO_ADD = 'Hello World!'

  # ========================================================================= #
  # === __init__
  #
  # Task: in this assignment, you should write - for warm up - a program
  # that accepts a single file name on the command line and prints
  # (to standard output)
  # ========================================================================= #
  def __init__(self, use_this_file = None):
    if use_this_file:
      path = Path(use_this_file)
      if path.is_file(): # Check whether the given argument is an existing file.
        print(self.TEXT_TO_ADD)
        # =================================================================== #
        # Next, read in the file content:
        # =================================================================== #
        with open(use_this_file) as f:
          contents = f.read()
          print(contents.rstrip())
      else:
        print("Is not a file.")
    else:
      print("Please provide an existing file as argument to this class.")

program_name = sys.argv[0]
if len(sys.argv) > 1:
  arguments    = sys.argv[1:]
  # count = len(arguments)
  _ = HelloWorld(arguments[0])
else:
  print("Please provide at the least one argument to this class.")
