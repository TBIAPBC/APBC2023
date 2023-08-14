#!/usr/bin/ruby -w
# Encoding: UTF-8
# frozen_string_literal: true
# =========================================================================== #
# === Helloworld
#
# The assignment task can be read here:
#
#   https://github.com/TBIAPBC/APBC2023/tree/main/A0
#
# =========================================================================== #
# require 'hello_world.rb'
# =========================================================================== #
class Helloworld

  alias e puts

  # ========================================================================= #
  # === NAMESPACE
  # ========================================================================= #
  NAMESPACE = inspect

  # ========================================================================= #
  # === TEXT_TO_ADD
  # ========================================================================= #
  TEXT_TO_ADD = 'Hello World!'

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
    # ======================================================================= #
    @namespace = NAMESPACE
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
  # === run                                                         (run tag)
  # ========================================================================= #
  def run
    # ======================================================================= #
    # Task: in this assignment, you should write - for warm up - a program
    # that accepts a single file name on the command line and prints
    # (to standard output)
    # ======================================================================= #
    _ = first_argument?
    if _
      e TEXT_TO_ADD #  adding a line break
      if File.file?(_)
        file_content = File.read(_)
        e file_content
      else
        e 'Is not a file.'
      end
    else
      e 'Please supply a filename to this class.'
    end
  end

  # ========================================================================= #
  # === Helloworld[]
  # ========================================================================= #
  def self.[](i = '')
    new(i)
  end

end

if __FILE__ == $PROGRAM_NAME
  Helloworld.new(ARGV)
end # HelloWorld.rb