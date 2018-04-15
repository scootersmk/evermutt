#!/usr/bin/env python

import os
import xml.etree.ElementTree as ET

#local modules
from evermutt.misc import *
from evermutt.note import *

class EmCache(object):
  def __init__(self, directory):

    #Defaults
    self.cache_dir = directory

    self.initialize()

  def initialize(self):
    if not dir_exists(self.cache_dir):
      dir_create(self.cache_dir)

  def get_note(self, note_guid, session):
    metadata_fname = os.path.join(self.cache_dir,
                                  "%s.metadata.xml" % (note_guid))
    content_fname = os.path.join(self.cache_dir,
                                 "%s.xml" % note_guid)

    if file_exists(metadata_fname):
      tags = self.read_metadata(metadata_fname)
    else:
      tags = session.get_note_tags(note_guid)
      self.write_metadata(metadata_fname, tags)

    if file_exists(content_fname):
      content_lines = self.read_content(content_fname)
    else:
      content = session.get_note_content(note_guid, True)
      self.write_content(content_fname, content)
      content_lines = parse_note_content(content)

    return tags, content_lines

  @staticmethod
  def read_metadata(fname):
    #FIXME: support other metadata
    tags = []
    xml = ET.parse(fname)
    root_xml = xml.getroot()
    tags_xml = root_xml.find('tags')
    if tags_xml is not None:
      for tag in tags_xml.findall('tag'):
        tags.append(tag.get('name'))

    return tags


  @staticmethod
  def write_metadata(fname, tags):
    note_cache_xml = ET.Element('note')
    if tags:
      tags_xml = ET.SubElement(note_cache_xml, 'tags')
      for t in tags:
        attribs = {}
        attribs['name'] = t
        ET.SubElement(tags_xml, 'tag', attribs)
    #print content
    fdesc = open(fname, "w")
    metadata_content = ET.tostring(note_cache_xml)
    fdesc.write(metadata_content)
    fdesc.close()

  @staticmethod
  def read_content(fname):
    with open(fname, 'r') as xmlfile:
      enxml = xmlfile.read()
    content_lines = parse_note_content(enxml)
    return content_lines

  @staticmethod
  def write_content(fname, content):
    fdesc = open(fname, "w")
    fdesc.write(content)
    fdesc.close()
