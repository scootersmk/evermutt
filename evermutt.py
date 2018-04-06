#!/usr/bin/env python
#FIXME: Test python3 in seperate branch

from evernote.api.client import EvernoteClient
#import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.ttypes as NotesStore
import evernote.edam.type.ttypes as Types
import curses
import argparse
import local
import xml.etree.ElementTree as ET
import os
import sys

#Local modules
from misc import *
from note import *


KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_UP = (curses.KEY_UP, ord('k'))
KEYS_DOWN = (curses.KEY_DOWN, ord('j'))
KEYS_SELECT = (curses.KEY_RIGHT, ord(' '))

class NoteList:
  def __init__(self, screen, session):
    #if len(notes) == 0:
    #  raise ValueError('notes should not be an empty list')

    self.session = session
    self.notes = session['noteMetadata']
    self.screen = screen
    self.index = 0
    self.in_note = False

  def move_up(self):
    self.index -= 1
    if self.index < 0:
      self.index = len(self.notes) - 1

  def move_down(self):
    self.index += 1
    if self.index >= len(self.notes):
      self.index = 0

  def draw(self, draw_note_index=None):
    """draw the curses ui on the screen, handle scroll if needed"""
    self.screen.clear()

    x, y = 0, 0  # start point
    max_y, max_x = self.screen.getmaxyx()
    max_rows = max_y - 1  # the max rows we can draw

    index_length = 4
    date_length = 5
    title_length = max_x - index_length - date_length - 3
    line_str_fmt = "%%%dd %%%ds %%-%ds" % (index_length, date_length, title_length)

    for note in self.notes:
      if y < max_rows:
        date_str = convert_epoch_to_date(note.created)
        if y == self.index:
          self.screen.addstr(y, 0, line_str_fmt % (y+1, date_str, note.title), curses.color_pair(1))
        else:
          self.screen.addstr(y, 0, line_str_fmt % (y+1, date_str, note.title))
        y += 1

    self.screen.refresh()

    if draw_note_index is not None:
      self.draw_note(draw_note_index)

  def draw_note(self, note_index):
    note = self.notes[note_index]
    y, x = self.screen.getmaxyx()
    note_screen_x = x
    note_screen_y = y - 10
    note_screen = curses.newwin(note_screen_y, note_screen_x, 10, 0)
    status_y = 0
    status_x = 0
    status_line = "Title: %s" % (note.title)
    status_line_length = x - 1
    status_line_fmt = "%%-%ds" % status_line_length
    note_screen.addstr(status_y,
                       status_x,
                       status_line_fmt % status_line,
                       curses.color_pair(1))
    note_screen.addstr(1, 0, "Title: %s" % note.title)
    created_date_str = convert_epoch_to_date(note.created, False)
    updated_date_str = convert_epoch_to_date(note.updated, False)
    content_lines = get_note_content(note_index, self.session)
    tags = get_note_tags(note_index, self.session)
    #FIXME: Be smarter about what metadata to display
    note_screen.addstr(2, 0, "Created: %s" % created_date_str)
    note_screen.addstr(3, 0, "Updated: %s" % updated_date_str)
    note_screen.addstr(4, 0, "Guid: %s" % note.guid)
    note_screen.addstr(5, 0, "Notebook Guid: %s" % note.notebookGuid)
    note_screen.addstr(6, 0, "Tags: %s" % str(tags))
    note_screen.addstr(7, 0, "Lines: %d" % len(content_lines))

    #FIXME: Test notes longer than display
    i = 9
    for content in content_lines:
      note_screen.addstr(i, 0, "%s" % content)
      i = i + 1
      if i >= y - 1:
        break

    note_screen.refresh()
    return

  def run_loop(self):
    while True:
      if self.in_note:
        self.draw(self.index)
      else:
        self.draw()
      c = self.screen.getch()
      if c in KEYS_UP:
        self.move_up()
      elif c in KEYS_DOWN:
        self.move_down()
      elif c in KEYS_ENTER:
        self.in_note = True
      elif c == ord('q'):
        if self.in_note:
          self.in_note = False
        else:
          return


def login(args):
  session = {}
  session['client'] = EvernoteClient(token=local.dev_token)
  session['userStore'] = session['client'].get_user_store()
  session['noteStore'] = session['client'].get_note_store()
  session['defaultNotebook'] = session['noteStore'].getDefaultNotebook()
  session['noteMetadata'] = get_notes_metadata(session['noteStore'],
                                               session['defaultNotebook'])
  session['noteCount'] = len(session['noteMetadata'])
  if args.verbose:
    print "NoteCount = %d" % session['noteCount']
  return session

def cache(session, offline=False):
  cached_session = {}
  create_cache_dir = False
  new_cache = False

  #Verify/Create local storage
  home_env = 'HOME'
  evermutt_dirname = ".evermutt"
  try:
    homedir = os.environ[home_env]
  except KeyError:
    print "Error, no such environment variable: %s" % home_env
    sys.exit(1)
  evermutt_dir = "%s%s%s" % (homedir, os.sep, evermutt_dirname)

  try:
    os.stat(homedir)
  except OSError:
    print "Error, HOME directory(%s) does not exist \n \
          Please set HOME to a writeable directory or \
          disable cacheing with --no-cache option"
    sys.exit(1)

  try:
    os.stat(evermutt_dir)
  except OSError:
    create_cache_dir = True

  if create_cache_dir:
    try:
      os.mkdir(evermutt_dir, 0o700)
      new_cache = True
    except OSError:
      print "Error, cache directory creation failed"
      sys.exit(1)

  #FIXME: Read in local cache
  #if not new_cache:
  #  print "Read cache"

  #Get note content
  if not offline:
    for idx, note in enumerate(session['noteMetadata']):
      content_fname = "%s%s%s.xml" % (evermutt_dir, os.sep, note.guid)
      #print "Cacheing note %s in %s" % (note.guid, content_fname)
      content = get_note_content(idx, session, True)
      #print content
      fdesc = open(content_fname, "w")
      fdesc.write(content)
      fdesc.close()
      #print "Created file %s" % fname
      metadata_fname = "%s%s%s.metadata.xml" % (evermutt_dir, os.sep, note.guid)
      #print "Cacheing note %s in %s" % (note.guid, content_fname)
      #FIXME: Add cache attributes to root element: guid, version/timestamp, etc
      note_cache_xml = ET.Element('note')
      tags = get_note_tags(idx, session)
      if len(tags):
        tags_xml = ET.SubElement(note_cache_xml, 'tags')
        for t in tags:
          attribs = {}
          attribs['text'] = t
          tag_xml = ET.SubElement(tags_xml, 'tag', attribs)
      #print content
      fdesc = open(metadata_fname, "w")
      metadata_content = ET.tostring(note_cache_xml)
      fdesc.write(metadata_content)
      fdesc.close()
      #print "Created file %s" % fname

  #FIXME: Download resources

  #FIXME: Handle conflicts
  #if not new_cache:
  #  print "Merge cache with server data"

  #Write cache to disk
  return cached_session


def update_status(scr, session):
  notebook = session['defaultNotebook'].name
  noteCount = session['noteCount']
  y, x = scr.getmaxyx()
  status_y = y - 2
  status_x = 0
  status_line = "Notebook: %s [Notes: %d]" % (notebook, noteCount)
  status_line_length = x - 1
  status_line_fmt = "%%-%ds" % status_line_length
  scr.addstr(status_y,
             status_x,
             status_line_fmt % status_line,
             curses.color_pair(1))
  scr.refresh()

def gui(stdscr, session):
  # Clear screen
  curses.curs_set(0)
  stdscr.clear()
  curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)

  update_status(stdscr, session)
  y, x = stdscr.getmaxyx()
  notes_screen_y = y - 2
  #FIXME: set to less than number of notes, to test/fix scrolling
  #notes_screen_y = 5
  notes_screen_x = x
  notes_screen = curses.newwin(notes_screen_y, notes_screen_x, 0, 0)
  nl = NoteList(notes_screen, session)
  note_index = nl.run_loop()

  return note_index

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

  if args.offline:
    session = None
  else:
    session = login(args)

  if args.create_note:
    if args.verbose:
      print "Creating new note"
    create_note(session, args.create_note)
  else:
    if args.no_cache:
      curses.wrapper(gui, session)
    else:
      cached_session = cache(session)
      return
      curses.wrapper(gui, cached_session)

if __name__ == '__main__':
  main()
