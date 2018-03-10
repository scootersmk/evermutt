#!/usr/bin/env python

from evernote.api.client import EvernoteClient
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.ttypes as NotesStore
import curses
from curses import wrapper
import time

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
    self.index = 1 

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

    x, y = 1, 1  # start point
    max_y, max_x = self.screen.getmaxyx()
    max_rows = max_y - y  # the max rows we can draw

    for note in self.notes:
      date_str = convert_epoch_to_date(note.created)
      if y == self.index:
        self.screen.addstr(y-1, 0, "%4d %5s %-30s" % (y, date_str, note.title), curses.color_pair(1))
      else:
        self.screen.addstr(y-1, 0, "%4d %5s %-30s" % (y, date_str, note.title))
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


def login():
  client = EvernoteClient(token=local.dev_token)
  return client

def update_status(scr, nb, stats):
  y,x = scr.getmaxyx()
  status_y = y - 2
  status_x = 0
  scr.addstr(status_y,status_x, "Notebook: %s [Notes: %d]" % (nb.name, stats['notes']), curses.color_pair(1))
  scr.refresh()

def convert_epoch_to_date(epoch):
  #time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch))
  return time.strftime("%b %d", time.localtime(epoch))

def get_notes(ns, nb):
  #http://dev.evernote.com/doc/reference/NoteStore.html#Fn_NoteStore_findNotesMetadata 
  notefilter = NotesStore.NoteFilter()
  notefilter.notebookGuid = nb.guid
  resultspec = NotesStore.NotesMetadataResultSpec()
  resultspec.includeTitle = True
  notelist =  ns.findNotesMetadata(notefilter, 0, 10, resultspec)
  return notelist.notes

def main(stdscr):
  # Clear screen
  curses.curs_set(0)
  stdscr.clear()
  curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
  stats = {}

  client=login()

  noteStore = client.get_note_store()
  defaultNotebook = noteStore.getDefaultNotebook()
  notes = get_notes(noteStore, defaultNotebook)
  stats['notes'] = len(notes)
  update_status(stdscr, defaultNotebook, stats)
  y,x = stdscr.getmaxyx()
  notes_screen_y = y - 2
  notes_screen_x = x
  notes_screen = curses.newwin(notes_screen_y, notes_screen_x, 0, 0)
  nl = NoteList(notes_screen, notes)
  note_index = nl.run_loop()
  print note_index

#  while True:
#    # Store the key value in the variable `c`
#    c = stdscr.getch()
#    # Clear the terminal
#    #stdscr.clear()
#    if c == ord('q'):
#      return
#    elif c == curses.KEY_UP:
#      stdscr.addstr("You pressed the up arrow.")
#    else:
#      stdscr.addstr("This program doesn't know that key.....")

wrapper(main)
