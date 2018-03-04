#!/usr/bin/env python

from evernote.api.client import EvernoteClient
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.ttypes as NotesStore
import curses
from curses import wrapper
import time

import local

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

def list_notes(scr, ns, nb):
  #http://dev.evernote.com/doc/reference/NoteStore.html#Fn_NoteStore_findNotesMetadata 
  notefilter = NotesStore.NoteFilter()
  notefilter.notebookGuid = nb.guid
  resultspec = NotesStore.NotesMetadataResultSpec()
  resultspec.includeTitle = True
  notelist =  ns.findNotesMetadata(notefilter, 0, 10, resultspec)
  i = 1
  for note in notelist.notes:
    date_str = convert_epoch_to_date(note.created)
    scr.addstr(i-1, 0, "%4d %5s %-30s" % (i, date_str, note.title))
    i=i+1

  stats = {}
  stats['notes'] = len(notelist.notes)
  return stats

def main(stdscr):
  # Clear screen
  curses.curs_set(0)
  stdscr.clear()
  curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)

  client=login()

  noteStore = client.get_note_store()
  defaultNotebook = noteStore.getDefaultNotebook()
  stats = list_notes(stdscr, noteStore, defaultNotebook)
  update_status(stdscr, defaultNotebook, stats)
  stdscr.refresh()


  while True:
    # Store the key value in the variable `c`
    c = stdscr.getch()
    # Clear the terminal
    #stdscr.clear()
    if c == ord('q'):
      return
    elif c == curses.KEY_UP:
      stdscr.addstr("You pressed the up arrow.")
    else:
      stdscr.addstr("This program doesn't know that key.....")

wrapper(main)
