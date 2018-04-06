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
