#!/usr/bin/env python
#FIXME: Test python3 in seperate branch

from evernote.api.client import EvernoteClient
import evernote.edam.notestore.ttypes as NotesStore
import evernote.edam.type.ttypes as Types

#Local modules
from evermutt.note import *
from evermutt.config import EmConfig
from evermutt.cache import EmCache

class EnSession(object):
  def __init__(self, args):
    #if len(notes) == 0:
    #  raise ValueError('notes should not be an empty list')

    self.cache_enabled = not args.no_cache
    self.offline = args.offline
    self.client = None
    self.userStore = None
    self.noteStore = None
    self.defaultNotebook = None
    self.cache = None
    self.config = None
    self.notebook_list = None

    #FIXME: Currently written to only operate on defaultNotebook
    self.notebook = None
    self.notebook_name = None
    self.note_metadata = None

    self.config = EmConfig(args)

    if not self.offline:
      self.login()

    self.note_metadata = self._get_note_metadata()

    if self.cache_enabled:
      self.cache = EmCache(self.config.cache_dir)

  def login(self):
    dev_token = "S=s1:U=94719:E=1694a2fc3bc:C=161f27e9730:P=1cd:A=en-devtoken:V=2:H=8fb990d19b11965244f062dbb9ca06ec"
    self.client = EvernoteClient(token=dev_token)
    self.userStore = self.client.get_user_store()
    self.noteStore = self.client.get_note_store()
    self.defaultNotebook = self.noteStore.getDefaultNotebook()
    self.notebook = self.defaultNotebook
    self.notebook_name = self.defaultNotebook.name
    self.notebook_list = self.noteStore.listNotebooks()

  def create_note(self, title):
    note = Types.Note()
    note.title = title
    note.content = '<?xml version="1.0" encoding="UTF-8"?>\
                   <!DOCTYPE en-note SYSTEM \
                   "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note></en-note>'
    note = self.noteStore.createNote(note)
    return bool(note)

  def _get_note_metadata(self):
    notefilter = NotesStore.NoteFilter()
    notefilter.notebookGuid = self.notebook.guid
    resultspec = NotesStore.NotesMetadataResultSpec()
    resultspec.includeTitle = True
    resultspec.includeCreated = True
    resultspec.includeUpdated = True
    notelist = self.noteStore.findNotesMetadata(notefilter, 0, 10, resultspec)
    return notelist.notes

  def get_note_metadata(self):
    return self.note_metadata

  def get_note(self, note_guid):
    tags = []
    content_lines = []

    if self.cache_enabled:
      tags, content_lines = self.cache.get_note(note_guid, self)
    else:
      tags = self.get_note_tags(note_guid)
      content_lines = self.get_note_content(note_guid)

    return tags, content_lines

  def get_note_content(self, note_guid, raw=False):
    note = self.noteStore.getNote(note_guid, True, False, False, False)
    if raw:
      content = note.content
    else:
      content = parse_note_content(note.content)
    return content

  def get_note_tags(self, note_guid):
    tags = self.noteStore.getNoteTagNames(note_guid)
    return tags

  def get_notebooks(self):
    return self.notebook_list

  def change_notebook(self, notebook):
    self.notebook = notebook
    self.note_metadata = self._get_note_metadata()
