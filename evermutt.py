#!/usr/bin/env python

from evernote.api.client import EvernoteClient
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.ttypes as NotesStore
import evernote.edam.type.ttypes as Types
import curses
import time
import argparse
import local


KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_UP = (curses.KEY_UP, ord('k'))
KEYS_DOWN = (curses.KEY_DOWN, ord('j'))
KEYS_SELECT = (curses.KEY_RIGHT, ord(' '))

class NoteList:
  def __init__(self, screen, notes):
    if len(notes) == 0:
      raise ValueError('notes should not be an empty list')

    self.notes = notes
    self.screen = screen
    self.index = 0 

  def move_up(self):
    self.index -= 1
    if self.index < 0:
      self.index = len(self.notes) - 1

  def move_down(self):
    self.index += 1
    if self.index >= len(self.notes):
      self.index = 0

  def draw(self):
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

  def run_loop(self):
    while True:
      self.draw()
      c = self.screen.getch()
      if c in KEYS_UP:
        self.move_up()
      elif c in KEYS_DOWN:
        self.move_down()
      elif c in KEYS_ENTER:
        return self.index
      elif c == ord('q'):
        return


def login():
  client = EvernoteClient(token=local.dev_token)
  return client

def update_status(scr, stats):
  y,x = scr.getmaxyx()
  status_y = y - 2
  status_x = 0
  status_line = "Notebook: %s [Notes: %d]" % (stats['notebook'], stats['notes'])
  status_line_length = x - 1
  status_line_fmt = "%%-%ds" % status_line_length
  scr.addstr(status_y,status_x, status_line_fmt % status_line , curses.color_pair(1))
  scr.refresh()

def convert_epoch_to_date(epoch):
  #time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch))
  return time.strftime("%b %d", time.localtime(epoch))

def get_notes_metadata(ns, nb):
  #http://dev.evernote.com/doc/reference/NoteStore.html#Fn_NoteStore_findNotesMetadata 
  notefilter = NotesStore.NoteFilter()
  notefilter.notebookGuid = nb.guid
  resultspec = NotesStore.NotesMetadataResultSpec()
  resultspec.includeTitle = True
  notelist =  ns.findNotesMetadata(notefilter, 0, 10, resultspec)
  return notelist.notes

def create_note(ns, text):
  note = Types.Note()
  note.title = text
  note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
  note.content += '<en-note></en-note>'
  note = ns.createNote(note)

def gui(stdscr, notes, stats):
  # Clear screen
  curses.curs_set(0)
  stdscr.clear()
  curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)

  update_status(stdscr, stats)
  y,x = stdscr.getmaxyx()
  notes_screen_y = y - 2
  #FIXME: set to less than number of notes, to test/fix scrolling
  #notes_screen_y = 5
  notes_screen_x = x
  notes_screen = curses.newwin(notes_screen_y, notes_screen_x, 0, 0)
  nl = NoteList(notes_screen, notes)
  note_index = nl.run_loop()
  return note_index


def main():
  stats = {}

  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  #FIXME: customize create-note option help text to make it clearer how to use
  parser.add_argument('-c', '--create-note', help="Create a note in the default notebook")
  args = parser.parse_args()

  if args.verbose:
    print "verbosity turned on"

  if args.verbose:
    print "Logging into evernote server"
  client=login()
  userStore = client.get_user_store()
  user =  userStore.getUser()
  if args.verbose:
      print "Logged in as user: %s" % user.username

  if args.verbose:
    print "Retrieving note store"
  noteStore = client.get_note_store()

  defaultNotebook = noteStore.getDefaultNotebook()
  stats['notebook'] = defaultNotebook.name
  if args.verbose:
    print "Default notebook is: %s" % stats['notebook']

  if args.verbose:
    print "Retrieving note metadata from default notebook"
  notes = get_notes_metadata(noteStore, defaultNotebook)
  stats['notes'] = len(notes)
  if args.verbose:
    print "Retrieved metadata for %d notes" % stats['notes']
    time.sleep(10)
  
  if args.create_note:
    if args.verbose:
      print "Creating new note"
    create_note(noteStore, args.create_note)
  else:  
    index = curses.wrapper(gui, notes, stats)
    print index
    print notes[index].title
    print notes[index].guid
    #FIXME: replace getNote call with getNoteWithResultSpec
    note = noteStore.getNote(notes[index].guid, True, False, False, False)
    print note.content
    

if __name__ == '__main__':
  main()
