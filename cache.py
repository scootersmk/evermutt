#!/usr/bin/env python

import os
import sys
import xml.etree.ElementTree as ET

#local modules
from misc import *
from note import *

class EmCache:
  def __init__(self, directory):

    #Defaults
    self.cache_dir = directory

    self.initialize()

  def initialize(self):
    if not dir_exists(self.cache_dir):
      dir_create(self.cache_dir)

  def get_note(self, note_guid, session):
    metadata_fname = os.path.join(self.cache_dir, "%s.metadata.xml" % (note_guid))
    content_fname = os.path.join(self.cache_dir, "%s.xml" % note_guid)

    if file_exists(metadata_fname):
      tags = self.read_metadata(metadata_fname)
    else:
      tags = session.get_note_tags(note_guid)
      self.write_metadata(metadata_fname, tags)

    if file_exists(content_fname):
      content = self.read_content(content_fname)
      content_lines = parse_note_content(content)
    else:
      content = session.get_note_content(note_guid, True)
      self.write_content(content_fname, content)
      content_lines = parse_note_content(content)

    return tags,content

  def read_metadata(self, fname):
    print "read_metadata is NOT yet implemented!" 
    sys.exit(1)

  def write_metadata(self, fname, tags):
    note_cache_xml = ET.Element('note')
    if len(tags):
      tags_xml = ET.SubElement(note_cache_xml, 'tags')
      for t in tags:
        attribs = {}
        attribs['text'] = t
        tag_xml = ET.SubElement(tags_xml, 'tag', attribs)
    #print content
    fdesc = open(fname, "w")
    metadata_content = ET.tostring(note_cache_xml)
    fdesc.write(metadata_content)
    fdesc.close()

  def read_content(self, fname):
    print "read_content is NOT yet implemented!" 
    sys.exit(1)

  def write_content(self, fname, content):
    fdesc = open(fname, "w")
    fdesc.write(content)
    fdesc.close()
