#!/usr/bin/env python

from evernote.api.client import EvernoteClient
import evernote.edam.notestore.ttypes as NotesStore
import evernote.edam.type.ttypes as Types
import xml.etree.ElementTree as ET

#Local modules
from misc import *


def get_notes_metadata(ns, nb):
  notefilter = NotesStore.NoteFilter()
  notefilter.notebookGuid = nb.guid
  resultspec = NotesStore.NotesMetadataResultSpec()
  resultspec.includeTitle = True
  notelist = ns.findNotesMetadata(notefilter, 0, 10, resultspec)
  return notelist.notes

def create_note(session, text):
  ns = session['noteStore']
  note = Types.Note()
  note.title = text
  note.content = '<?xml version="1.0" encoding="UTF-8"?>\
                 <!DOCTYPE en-note SYSTEM \
                 "http://xml.evernote.com/pub/enml2.dtd">'
  note.content += '<en-note></en-note>'
  note = ns.createNote(note)

def parse_note_content(en_xml):
  lines = []
  root = ET.fromstring(en_xml)

  if root is not None and root.tag == 'en-note':
    #handle simple notes blank and oneliners
    if root.text is not None:
      lines.append(root.text)
    else:
      for e in root.iter('*'):
        if e.text:
          lines.append(e.text)
        elif e.tag == 'br':
          lines.append("")

  return lines

def get_note_content(index, session, raw=False):
  ns = session['noteStore']
  notes = session['noteMetadata']
  #FIXME: replace getNote call with getNoteWithResultSpec
  note = ns.getNote(notes[index].guid, True, False, False, False)
  if raw:
    return note.content
  else:
    return parse_note_content(note.content)

def get_note_tags(index, session):
  ns = session['noteStore']
  notes = session['noteMetadata']
  tags = ns.getNoteTagNames(notes[index].guid)
  return tags

