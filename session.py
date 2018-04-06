#!/usr/bin/env python
#FIXME: Test python3 in seperate branch

from evernote.api.client import EvernoteClient
import evernote.edam.notestore.ttypes as NotesStore
import evernote.edam.type.ttypes as Types
import local

#Local modules
from note import *
from config import EmConfig
from cache import EmCache

class EnSession:
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
    self.client = EvernoteClient(token=local.dev_token)
    self.userStore = self.client.get_user_store()
    self.noteStore = self.client.get_note_store()
    self.defaultNotebook = self.noteStore.getDefaultNotebook()
    self.notebook = self.defaultNotebook
    self.notebook_name = self.defaultNotebook.name

  def create_note(self, title):
    note = Types.Note()
    note.title = title
    note.content = '<?xml version="1.0" encoding="UTF-8"?>\
                   <!DOCTYPE en-note SYSTEM \
                   "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note></en-note>'
    note = self.noteStore.createNote(note)
    if note is not None:
      return True
    else:
      return False

  def _get_note_metadata(self):
    notefilter = NotesStore.NoteFilter()
    notefilter.notebookGuid = self.defaultNotebook.guid
    resultspec = NotesStore.NotesMetadataResultSpec()
    resultspec.includeTitle = True
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

    return tags,content_lines

  def get_note_content(self, note_guid, raw=False):
    note = self.noteStore.getNote(note_guid, True, False, False, False)
    if raw:
      return note.content
    else:
      return parse_note_content(note.content)

  def get_note_tags(self, note_guid):
    tags = self.noteStore.getNoteTagNames(note_guid)
    return tags
