#!/usr/bin/env python

import xml.etree.ElementTree as ET

def parse(filename):
  lines = []
  tree = ET.parse(filename)
  root = tree.getroot()

  if root is not None and root.tag == 'en-note':
    print root
    #handle simple notes blank and oneliners
    if root.text is not None:
      lines.append(root.text)
    else:
      for e in root.iter('*'):
        print e.tag
        if e.text:
          lines.append(e.text)
        elif e.tag == 'br':
          lines.append("")
  
  return lines
  
#files = ['blank.xml', 'simple.xml', 'sample.xml']
files = ['sample.xml']
for f in files:
  print f 
  print parse(f)
