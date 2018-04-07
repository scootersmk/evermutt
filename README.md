# Evermutt

## Development Status
### What works
- Create a simple note from the command line
- Viewing list of notes in default notebook
- Viewing note metadata(tags, created/modified date, etc)
- Viewing basic note content

### What does *not* work or is untested
- creating new notes from the gui
- deleting existing notes from the gui(moving them to the EN trash)
- scrolling note list, handling more notes than can fit on the screen at once
- scrolling note content, handling more content than can fit on the screen at once
- displaying all curses compatible note content
- editing the title and content of existing notes
- adding/removing tags of existing notes
- searching: by tags, by text, by date, etc
- sorting: by date, by tags
- saved searches
- working with notes in other notebooks
- sending updates to the server, new/updated/deleted notes
- handling updates from the server, new/update/deleted notes
- handling conflicts from the server
- view raw note content(in XML)
- config file to specify
  - disabling caching
  - override editor
  - specify cache directory
  - Default notebook
  - Change keybindings
  - Customize metadata to display

## Development Links
- http://dev.evernote.com/doc/start/python.php
- http://dev.evernote.com/doc/reference/
- https://github.com/evernote/evernote-sdk-python/
- https://sandbox.evernote.com/
- http://dev.evernote.com/doc/articles/enml.php
