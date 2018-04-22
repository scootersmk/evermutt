#!/usr/bin/env python

import curses
import argparse
import sys
#Local modules
from evermutt.gui import EmGui
from evermutt.session import EnSession

def gui_setup(stdscr, session):
  items = session.get_note_metadata()
  gui = EmGui(items, None, stdscr, session)
  gui.start()

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")
  #FIXME: customize create-note option help text to make it clearer how to use
  parser.add_argument('-c',
                      '--create-note',
                      help="Create a note in the default notebook")
  parser.add_argument('-o',
                      '--offline',
                      help="Work within local cache, don't talk to server",
                      action="store_true")
  parser.add_argument('--no-cache',
                      help="Disable creating or using local cache directory",
                      action="store_true")
  #FIXME: -F option to specify different cache/config directory
  #FIXME: -f option to specify different config file
  args = parser.parse_args()

  if args.offline and args.no_cache:
    print "Invalid options, can't set both --offline and --no-cache"
    sys.exit(1)

  if args.verbose:
    print "verbosity turned on"

  session = EnSession(args)

  if args.create_note:
    if args.verbose:
      print "Creating new note"
    session.create_note(args.create_note)
  else:
    curses.wrapper(gui_setup, session)

if __name__ == '__main__':
  main()
