# Evermutt

[![Build Status](https://travis-ci.org/scootersmk/evermutt.svg?branch=master)](https://travis-ci.org/scootersmk/evermutt)

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
- view previous versions of notes
- config file to specify
  - disabling caching
  - override editor
  - specify cache directory
  - Default notebook
  - Change keybindings
  - Customize metadata to display
  - Change color scheme

## GUI design
- Note List
  - Change Notebook(c)
  - Sort Notes(s)
    - By date
    - By tags
    - By title
  - Sync(S)
  - View Note
    - Edit Note Content
    - Tag Note
    - Trash Note
  - Create Note(n)
  - Search(/)

## Editing Modes

Strategies to ensure we don't "corrupt" formatting of existing notes that are created with GUI/Web clients.

### Different Modes
- read-only: only read existing notes, don't make any changes to notes or create new notes
- read-create: read existing notes and create new notes
- read-create-delete: same as read-create, but also delete any existing note
- read-create-delete-modify-local: same as read-create-delete, but also modify notes created locally
- read-create-delete-modify-all: same as read-create-delete but also modify all notes

### Protection Mode
Mark notes that are created in other clients as "protected" and warn users before allowing them to modify protected notes

## Development Links
- http://dev.evernote.com/doc/start/python.php
- http://dev.evernote.com/doc/reference/
- https://github.com/evernote/evernote-sdk-python/
- https://sandbox.evernote.com/
- http://dev.evernote.com/doc/articles/enml.php
- https://dev.evernote.com/doc/articles/synchronization.php
