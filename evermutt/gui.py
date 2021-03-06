#!/usr/bin/env python

import curses

#Local modules
from evermutt.misc import *

KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_UP = (curses.KEY_UP, ord('k'))
KEYS_DOWN = (curses.KEY_DOWN, ord('j'))
KEYS_SELECT = (curses.KEY_RIGHT, ord(' '))

class GuiSelectableList(object):
  def __init__(self, items, title, screen):
    self.index = 0
    self.items = items
    self.title = title
    self.screen = screen

  def move_up(self):
    self.index -= 1
    if self.index < 0:
      self.index = len(self.items) - 1

  def move_down(self):
    self.index += 1
    if self.index >= len(self.items):
      self.index = 0

  def draw_list(self):
    self.screen.clear()

    max_y, max_x = self.screen.getmaxyx()
    max_rows = max_y - 1  # the max rows we can draw
    max_length = max_x - 1

    self.screen.addstr(0, 0, self.title)

    for idx, item in enumerate(self.items, 0):
      if idx < max_rows:
        if idx == self.index:
          self.screen.addstr(idx + 1, 0, item[:max_length], curses.color_pair(1))
        else:
          self.screen.addstr(idx + 1, 0, item[:max_length])

    self.screen.refresh()

  def run_loop(self):
    while True:
      self.draw_list()
      c = self.screen.getch()
      if c in KEYS_UP:
        self.move_up()
      elif c in KEYS_DOWN:
        self.move_down()
      elif c in KEYS_ENTER:
        return self.index
      elif c == ord('q'):
        return self.index

class EmGui(GuiSelectableList):
  def __init__(self, items, title, screen, session):
    #if len(notes) == 0:
    #  raise ValueError('notes should not be an empty list')

    GuiSelectableList.__init__(self, items, title, screen)

    self.session = session
    self.notes_screen = None
    self.status_screen = None
    self.draw_note = False

    #Valid gui contexts
    # NoteList
    # NoteView
    self.context = 'NoteList'

  def start(self):
    curses.curs_set(0)
    self.screen.clear()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    #Create window that will contain the note list
    y, x = self.screen.getmaxyx()
    notes_screen_y = y - 2
    #FIXME: set to less than number of notes, to test/fix scrolling
    #notes_screen_y = 5
    notes_screen_x = x
    self.notes_screen = curses.newwin(notes_screen_y, notes_screen_x, 0, 0)

    #Create window that will contain the status bar
    status_y = y - 2
    status_x = 0
    self.status_screen = curses.newwin(1, x, status_y, status_x)

    self.run_loop()


  def draw_list(self):
    """draw the curses ui on the screen, handle scroll if needed"""
    self.notes_screen.clear()

    max_y, max_x = self.notes_screen.getmaxyx()
    max_rows = max_y - 1  # the max rows we can draw

    #FIXME: Check to make sure we will fit in the screen
    index_length = 5
    date_length = 8
    title_length = 40
    tags_length = 30

    line_str_fmt = "%%-%ds %%-%ds %%-%ds %%-%ds" % (index_length,
                                                    date_length,
                                                    title_length,
                                                    tags_length)

    header_y = 0
    header_x = 0
    header_line = line_str_fmt % ("#", "Date", "Title", "Tags")
    header_line_length = max_x - 1
    header_line_fmt = "%%-%ds" % header_line_length
    self.notes_screen.addstr(header_y,
                             header_x,
                             header_line_fmt % header_line,
                             curses.color_pair(1))

    for idx, note in enumerate(self.items, 0):
      if idx < max_rows:
        date_str = convert_epoch_to_date(note.created)
        tags = self.session.get_note(note.guid)[0]
        tags_str = ", ".join(tags)
        note_line = line_str_fmt % (str(idx+1), date_str, note.title, tags_str)
        note_line_length = max_x - 1
        note_line_fmt = "%%-%ds" % note_line_length
        if idx == self.index:
          self.notes_screen.addstr(idx + 1, 0, note_line_fmt % note_line, curses.color_pair(1))
        else:
          self.notes_screen.addstr(idx + 1, 0, note_line_fmt % note_line)

    self.notes_screen.refresh()

    if self.draw_note:
      self.draw_note_screen()

  def draw_help(self):
    options = {}
    options['view_note'] = {}
    options['view_note']['description'] = 'View selected note'
    options['view_note']['keys'] = '<enter>'
    options['view_note']['status'] = None
    options['search_note'] = {}
    options['search_note']['description'] = 'Search notes'
    options['search_note']['keys'] = '<enter>'
    options['search_note']['status'] = 'not_implemented'
    options['change_notebook'] = {}
    options['change_notebook']['description'] = 'Change current notebook'
    options['change_notebook']['keys'] = 'c'
    options['change_notebook']['status'] = None
    options['trash_note'] = {}
    options['trash_note']['description'] = 'Move currently selected note to trash'
    options['trash_note']['keys'] = 'd'
    options['trash_note']['status'] = 'not_implemented'
    options['edit_note'] = {}
    options['edit_note']['description'] = 'Edit content of currently selected note'
    options['edit_note']['keys'] = 'e'
    options['edit_note']['status'] = 'not_implemented'
    options['create_note'] = {}
    options['create_note']['description'] = 'Create new note'
    options['create_note']['keys'] = 'n'
    options['create_note']['status'] = 'not_implemented'
    options['create_notebook'] = {}
    options['create_notebook']['description'] = 'Create new notebook'
    options['create_notebook']['keys'] = 'N'
    options['create_notebook']['status'] = 'not_implemented'
    options['sort_notes'] = {}
    options['sort_notes']['description'] = 'Sort note list'
    options['sort_notes']['keys'] = 's'
    options['sort_notes']['status'] = 'not_implemented'
    options['sync_notes'] = {}
    options['sync_notes']['description'] = 'Sync notes with Evernote Server'
    options['sync_notes']['keys'] = 'S'
    options['sync_notes']['status'] = 'not_implemented'
    options['tag_note'] = {}
    options['tag_note']['description'] = 'Manage tags on currently selected note'
    options['tag_note']['keys'] = 't'
    options['tag_note']['status'] = 'not_implemented'


    y, x = self.notes_screen.getmaxyx()
    help_screen = curses.newwin(y, x, 0, 0)
    help_screen.box()

    help_screen.addstr(0, 5, "| Help |")
    help_screen.addstr(1, 2, "%-10s %s" % ('Keys', 'Description'))

    for i, k in enumerate(options.keys()):
      if options[k]['status']:
        desc = "%s(%s)" % (options[k]['description'], options[k]['status'])
      else:
        desc = options[k]['description']
      keys = options[k]['keys']
      help_screen.addstr(i + 2, 2, "%-10s %s" % (keys, desc))

    help_screen.refresh()

    while True:
      c = help_screen.getch()
      if c is not None:
        return

  def draw_note_screen(self):
    note = self.items[self.index]
    guid = note.guid
    y, x = self.notes_screen.getmaxyx()
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
    #content_lines = self.session.get_note_content(guid)
    #tags = self.session.get_note_tags(guid)
    tags, content_lines = self.session.get_note(guid)
    tags_str = ", ".join(tags)
    #FIXME: Be smarter about what metadata to display
    note_screen.addstr(2, 0, "Created: %s" % created_date_str)
    note_screen.addstr(3, 0, "Updated: %s" % updated_date_str)
    note_screen.addstr(4, 0, "Guid: %s" % note.guid)
    note_screen.addstr(5, 0, "Notebook Guid: %s" % note.notebookGuid)
    note_screen.addstr(6, 0, "Tags: %s" % tags_str)
    note_screen.addstr(7, 0, "Lines: %d" % len(content_lines))

    #FIXME: Test notes longer than display
    i = 9
    for content in content_lines:
      note_screen.addstr(i, 2, "%s" % content)
      i = i + 1
      if i >= y - 1:
        break

    note_screen.refresh()
    return

  def run_loop(self):
    while True:
      self.update_status()
      self.draw_list()
      c = self.notes_screen.getch()
      if c in KEYS_UP:
        self.move_up()
      elif c in KEYS_DOWN:
        self.move_down()
      elif c in KEYS_ENTER:
        self.draw_note = True
      elif c == ord('q'):
        if self.draw_note:
          self.draw_note = False
        else:
          return
      elif c == ord('c'):
        if not self.draw_note:
          self.change_notebook()
      elif c == ord('h'):
        self.draw_help()

  def update_status(self):
    notebook = self.session.notebook_name
    metadata = self.session.get_note_metadata()
    noteCount = len(metadata)
    x = self.status_screen.getmaxyx()[1]
    status_line = "Notebook: %s [Notes: %d]" % (notebook, noteCount)
    status_line_length = x - 1
    status_line_fmt = "%%-%ds" % status_line_length
    self.status_screen.addstr(0,
                              0,
                              status_line_fmt % status_line,
                              curses.color_pair(1))
    self.status_screen.refresh()

  def change_notebook(self):
    notebooks = self.session.get_notebooks()
    notebook_names = []
    for nb in notebooks:
      notebook_names.append(nb.name)
    NoteBookSelector = GuiSelectableList(notebook_names, "Select a notebook:", self.notes_screen)
    new_notebook = NoteBookSelector.run_loop()
    self.session.change_notebook(notebooks[new_notebook])
    self.items = self.session.get_note_metadata()
