#!/usr/bin/ruby -w
# Encoding: UTF-8
# frozen_string_literal: true
# =========================================================================== #
# === WordCount
#
# Write a program that reads in a text (file name given on the command
# line) and counts the total number of words and the number of different
# words. On request, the program should print a list of the words.
#
# The program should accept the name of the text file as command line
# argument.
#
# If option -I (for 'Ignore') is given, case shall be ignored
# (by converting all upper case to lower case, see below).
#
# If option -l (for 'list') is present, the program must print
# a list of words instead only counts. This list must be sorted
# by word frequency, starting with the most common words. ( per
# line print one word and its frequency, separated by a tab
# symbol; in case of equal frequencies, the words must be sorted
# alphabetically.). Please have a look at the example inputs
# and outputs; your program should produce outputs in exactly
# the same format.
#
# Usage example:
#
#   WordCount.new(ARGV)
#
# =========================================================================== #
# https://github.com/TBIAPBC/APBC2023/tree/main/A1
# =========================================================================== #
import argparse
import collections
import itertools
import operator
import os.path
import pprint
import re
import shlex
import sys
import string
from collections import Counter

class WordCount:

  # ========================================================================= #
  # === USE_THIS_REGEX
  #
  # Something is wrong with this regex.
  # ========================================================================= #
  USE_THIS_REGEX = " |;|,|-|!|'|\.|\"" # ",| |!|%|\(|\)|-|_|\+|\"|;|:" # |. # ? # \^

  # ========================================================================= #
  # === __init__()
  # ========================================================================= #
  def __init__(self, commandline_arguments = sys.argv):
    self.reset()
    # ======================================================================= #
    # Define our instance variables next:
    # ======================================================================= #
    self.commandline_arguments = commandline_arguments
    self.run()

  # ========================================================================= #
  # === reset()
  # ========================================================================= #
  def reset(self):
    # ======================================================================= #
    # === @internal_hash
    # ======================================================================= #
    self.internal_hash = {}
    # ======================================================================= #
    # Next set some default values for the internal Hash. This hash will
    # keep the dataset that may be useful after having parsed the existing
    # content of the given file(s) to this class.
    # ======================================================================= #
    # ======================================================================= #
    # === :ignore_case
    #
    # This setting will allow the user to ignore the case of the words in
    # the file.
    # ======================================================================= #
    self.internal_hash['ignore_case'] = False
    # ======================================================================= #
    # === :print_list_of_words
    # ======================================================================= #
    self.internal_hash['print_list_of_words'] = False
    # ======================================================================= #
    # === :array_work_on_these_files
    #
    # Keep track of which files to work on/with here, as an Array.
    # ======================================================================= #
    self.internal_hash['array_work_on_these_files'] = []
    # ======================================================================= #
    # === :results
    #
    # The following Hash will store all results. The key will be the
    # filename; then the two integer values are the total number of words
    # and then the number of different words.
    # ======================================================================= #
    self.internal_hash['results'] = {}

  # ========================================================================= #
  # === menu                                                       (menu tag)
  #
  # This method will only work if a list is passed into it, as argument.
  # ========================================================================= #
  def menu(self, i):
    # ======================================================================= #
    # Check for list given next:
    # ======================================================================= #
    if isinstance(i, list):
      for entry in i:
        if entry.startswith('-'):
          # ================================================================= #
          # === Ignore the case
          #
          # Entry via:
          #
          #   py rubyFeedback-WordCount.py WordCount-test1.in -I
          #   
          # ================================================================= #
          if (entry == '-I') or (entry == '--ignore-case'):
            self.internal_hash['ignore_case'] = True
          # ================================================================= #
          # === Enable listed reporting next
          #
          #   py rubyFeedback-WordCount.py WordCount-test1.in -I -l
          #
          # ================================================================= #
          if (entry == '-l') or (entry == '--list'):
            self.internal_hash['print_list_of_words'] = True

  # ========================================================================= #
  # === print_list_of_words()
  #
  # Simple query-method.
  # ========================================================================= #
  def print_list_of_words(self):
    return self.internal_hash['print_list_of_words']

  # ========================================================================= #
  # === run                                                         (run tag)
  # ========================================================================= #
  def run(self):
    x = self.commandline_arguments
    # ======================================================================= #
    # Next parse the commandline arguments that were given to this class.
    # We do this on an ad-hoc basis though.
    # ======================================================================= #
    self.menu(x)
    # ======================================================================= #
    # Find the first entry that does NOT start with "-".
    # ======================================================================= #
    x = list(filter(lambda a: not a.startswith('-'), x))
    x = x[1] # Assume the second entry is the filename.
    if os.path.isfile(x):
      with open(x) as file:
        file_content = file.read()
        # =================================================================== #
        # Replace newlines with ' ' next:
        # =================================================================== #
        file_content = file_content.replace("\n", ' ')
        # =================================================================== #
        # Honour the ignore-case setting next:
        #
        # Invocation example:
        #
        #   py rubyFeedback-WordCount.py WordCount-test1.in -I
        #
        # =================================================================== #
        if (self.internal_hash['ignore_case']):
          file_content = file_content.lower()

        # =================================================================== #
        # Next we will split via the regex defined on top of the file. This
        # currently does not work perfectly well, though.
        # =================================================================== #
        result = re.split(self.USE_THIS_REGEX, file_content)
        # result = [word.strip(string.punctuation) for word in file_content.split()]
        # result = file_content.split()
        stripped_result = [i for i in result if i] # Ignore empty Strings here via list comprehension.

        if (self.print_list_of_words()):
          self.do_print_the_list_of_words_in_a_detailed_manner(stripped_result)
        else:
          # =================================================================== #
          # Get the unique entries next:
          # =================================================================== #
          set_unique_entries = set(stripped_result)
          # =================================================================== #
          # Finally we will print our findings:
          # =================================================================== #
          print(
            len(set_unique_entries), '/', len(stripped_result)
          )
    else:
      print(x+" is not a file. This class requires the path to a local,\n"\
      "existing file, as its input.")

  # ========================================================================= #
  # === do_print_the_list_of_words_in_a_detailed_manner()
  #
  # The task of this method is to do this:
  #
  # "The program must print a list of words instead only counts. This
  # list must be sorted by word frequency, starting with the most
  # common words. ( per line print one word and its frequency,
  # separated by a tab symbol; in case of equal frequencies, the
  # words must be sorted alphabetically.).
  #
  # Please have a look at the example inputs and outputs; your
  # program should produce outputs in exactly the same format.
  # ========================================================================= #
  def do_print_the_list_of_words_in_a_detailed_manner(
      self,
      i # stripped_result
    ):
    word_frequencies = Counter(i).most_common()
    # ======================================================================= #
    # We want a dictionary/Hash, though.
    # ======================================================================= #
    hash_word_frequencies = dict(word_frequencies)
    # self.p(hash_word_frequencies.items()) # For debugging.
    sorted_hash = sorted(hash_word_frequencies.items(), key=operator.itemgetter(1))
    sorted_dict = collections.OrderedDict(reversed(sorted_hash))
    # self.p(sorted_dict)
    values = sorted_dict.values()
    # self.p(values)
    unique_values = list(set([i for i in values]))
    unique_values = unique_values[::-1] # Reverse it here.
    for entry in unique_values:
      self.print_alphabeticalcally(entry, sorted_dict)

  # ========================================================================= #
  # === print_alphabeticalcally
  # ========================================================================= #
  def print_alphabeticalcally(self, entry, sorted_hash):
    # this_hash = sorted_dict
    array = []

    for key, value in sorted_hash.items():
      if value == entry:
        array.append(key)
    array = sorted(array)

    for inner_entry in array:
      print(inner_entry, "\t", entry)

  # ========================================================================= #
  # === e
  # ========================================================================= #
  def e(self, i = ''):
    print(i)

  # ========================================================================= #
  # === p
  # ========================================================================= #
  def p(self, i):
    pprint.PrettyPrinter(width=41, compact=True).pprint(i)
  
  # ========================================================================= #
  # === debug
  # ========================================================================= #
  def debug(self):
    p(self.commandline_arguments)
    p(self.internal_hash)

word_count = WordCount(sys.argv)
# word_count.debug()