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
# require 'rubyFeedback-WordCount.rb'
# =========================================================================== #
class WordCount

  alias e puts

  # ========================================================================= #
  # === NAMESPACE
  # ========================================================================= #
  NAMESPACE = inspect

  # ========================================================================= #
  # === REGEX_FOR_CHARACTERS_TO_BE_RECOGNIZED_AS_SPECIAL
  # ========================================================================= #
  REGEX_FOR_CHARACTERS_TO_BE_RECOGNIZED_AS_SPECIAL =
    /,| |!|\.|\?|%|\^|\(|\)|-|_|'|\+|"|;|:/ # These characters are to be used.

  # ========================================================================= #
  # === initialize
  # ========================================================================= #
  def initialize(
      commandline_arguments = nil,
      run_already           = true
    )
    reset
    set_commandline_arguments(
      commandline_arguments
    )
    run if run_already
  end

  # ========================================================================= #
  # === reset                                                     (reset tag)
  # ========================================================================= #
  def reset
    # ======================================================================= #
    # === @namespace
    #
    # Not in use for this class; just defined in case we need more specific
    # debug output at a later time.
    # ======================================================================= #
    @namespace = NAMESPACE
    # ======================================================================= #
    # === @internal_hash
    # ======================================================================= #
    @internal_hash = {}
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
    @internal_hash[:ignore_case] = false
    # ======================================================================= #
    # === :print_list_of_words
    # ======================================================================= #
    @internal_hash[:print_list_of_words] = false
    # ======================================================================= #
    # === :array_work_on_these_files
    #
    # Keep track of which files to work on/with here, as an Array.
    # ======================================================================= #
    @internal_hash[:array_work_on_these_files] = []
    # ======================================================================= #
    # === :results
    #
    # The following Hash will store all results. The key will be the
    # filename; then the two integer values are the total number of words
    # and then the number of different words.
    # ======================================================================= #
    @internal_hash[:results] = {}
  end

  # ========================================================================= #
  # === set_commandline_arguments
  # ========================================================================= #
  def set_commandline_arguments(i = '')
    i = [i].flatten.compact
    @commandline_arguments = i
  end

  # ========================================================================= #
  # === commandline_arguments?
  # ========================================================================= #
  def commandline_arguments?
    @commandline_arguments
  end

  # ========================================================================= #
  # === first_argument?
  # ========================================================================= #
  def first_argument?
    @commandline_arguments.first
  end; alias first? first_argument? # === first?

  # ========================================================================= #
  # === menu                                                       (menu tag)
  # ========================================================================= #
  def menu(
      i = commandline_arguments?
    )
    if i.is_a? Array
      i.each {|entry| menu(entry) }
    else
      case i
      # ===================================================================== #
      # === --ignore-case
      # ===================================================================== #
      when /-I/,
           /--ignore(-|_)?case$/i
        @internal_hash[:ignore_case] = true
      # ===================================================================== #
      # === --list
      # ===================================================================== # 
      when /-l/,
           /--list/
        @internal_hash[:print_list_of_words] = true
      else
        if i and File.file?(i)
          # ================================================================= #
          # Handle existing local files here, by appending them onto the
          # correct Array.
          # ================================================================= #
          @internal_hash[:array_work_on_these_files] << i
        end
      end
    end
  end

  # ========================================================================= #
  # === print_list_of_words?
  # ========================================================================= #
  def print_list_of_words?
    @internal_hash[:print_list_of_words]
  end

  # ========================================================================= #
  # === ignore_case?
  # ========================================================================= #
  def ignore_case?
    @internal_hash[:ignore_case]
  end

  # ========================================================================= #
  # === work_on_which_files?
  # ========================================================================= #
  def work_on_which_files?
    @internal_hash[:array_work_on_these_files]
  end

  # ========================================================================= #
  # === no_files_were_given?
  # ========================================================================= #
  def no_files_were_given?
    work_on_which_files?.empty?
  end

  # ========================================================================= #
  # === do_work_on_these_files
  # ========================================================================= #
  def do_work_on_these_files(i = work_on_which_files?)
    i.each {|this_file|
      file_content = File.read(this_file).dup
      if ignore_case?
        # =================================================================== #
        # For this purpose just convert upper case to lower case.
        # =================================================================== #
        file_content.downcase!
      end
      without_newlines = file_content.tr("\n",' ').squeeze(' ') # Simplify things.
      splitted_into_words = without_newlines.split(
        # =================================================================== #
        # Note that ' also appears to be in the list of characters to
        # be used for splitting.
        # =================================================================== #
        REGEX_FOR_CHARACTERS_TO_BE_RECOGNIZED_AS_SPECIAL
      ).reject {|entry| entry.empty? }
      tallied = splitted_into_words.tally
      sum = tallied.values.sum
      uniq_keys = tallied.keys.uniq
      n_uniq = uniq_keys.size
      @internal_hash[:results][this_file] = [
        n_uniq, sum
      ]
      if print_list_of_words?
        do_print_the_list_of_words_from_this_dataset(tallied)
      else
        pointer = @internal_hash[:results][this_file]
        e "#{pointer.first} / #{pointer.last}"
      end
    }
  end

  # ========================================================================= #
  # === do_print_the_list_of_words_from_this_dataset
  #
  # If option -l (for 'list') is present, the program must print a list
  # of words instead only counts. This list must be sorted by word
  # frequency, starting with the most common words. ( per line print
  # one word and its frequency, separated by a tab symbol; in case of
  # equal frequencies, the words must be sorted alphabetically.).
  #
  # Please have a look at the example inputs and outputs; your
  # program should produce outputs in exactly the same format.
  # ========================================================================= #
  def do_print_the_list_of_words_from_this_dataset(i)
    hash = {}
    sorted = i.sort_by {|key, value| value }.reverse
    unsorted_hash = Hash[*sorted.flatten]
    sorted.each {|word, number|
      correct_entries = unsorted_hash.select {|key, value| value == number }
      sorted_entries  = correct_entries.sort_by {|key, value| key }
      new_hash        = Hash[*sorted_entries.flatten]
      hash.update(new_hash)
    }
    hash.each_pair {|a, b| e a+"\t"+b.to_s }
  end

  # ========================================================================= #
  # === run                                                         (run tag)
  # ========================================================================= #
  def run
    menu
    if no_files_were_given?
      e 'Please provide a filename to this program. The file has to exist'
      e 'locally, in order for this class to process it.'
      e
      e 'Examples:'
      e
      e '  ruby rubyFeedback-WordCount.rb WordCount-test1.in'
      e '  ruby rubyFeedback-WordCount.rb WordCount-test2.in'
      e '  ruby rubyFeedback-WordCount.rb WordCount-test3.in'
      e
    else
      do_work_on_these_files(work_on_which_files?)
    end
  end

  # ========================================================================= #
  # === WordCount[]
  # ========================================================================= #
  def self.[](i = '')
    new(i)
  end

end

if __FILE__ == $PROGRAM_NAME
  WordCount.new(ARGV)
end # ruby rubyFeedback-WordCount.rb WordCount-test1.in
    # ruby rubyFeedback-WordCount.rb -l -I WordCount-test1.in
    # ruby rubyFeedback-WordCount.rb -l -I WordCount-test2.in
    # ruby rubyFeedback-WordCount.rb -l -I WordCount-test3.in