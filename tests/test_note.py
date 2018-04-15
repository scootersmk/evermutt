import unittest

from evermutt.note import *

class TestNote(unittest.TestCase):

    def test_parse_note_content_blank(self):
        en_xml = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note></en-note>'
        content = parse_note_content(en_xml)
        assert content == []

    def test_parse_note_content_simple(self):
        en_xml = '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>Test 1 2 3</en-note>'
        content = parse_note_content(en_xml)
        assert content == ['Test 1 2 3']

if __name__ == '__main__':
    unittest.main()
