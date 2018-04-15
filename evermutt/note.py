#!/usr/bin/env python

import xml.etree.ElementTree as ET

def parse_note_content(en_xml):
  lines = []
  root = ET.fromstring(en_xml)

  if root is not None and root.tag == 'en-note':
    #handle simple notes blank and oneliners
    if root.text is not None:
      lines.append(root.text)
    else:
      for e in root.findall('*'):
        if e.text:
          lines.append(e.text)
        elif e.tag == 'br':
          lines.append("")

  return lines
