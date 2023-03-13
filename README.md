# dayz-admin
Author: 
    DarthJedi

Initial Release Date: 
    02/2023

A collection of utilities and scripts I've written to help in my DayZ Management

## app/app.py

This will load a GUI to set the directory structure, and upon closing, will validate the DayZ Profile XML Files, and optionally the well-formedness of the JSON and XML files in various directories.

### app-config.json

Delete this file to recreate the config file upon next app.py run.

## validator.py

This will load up and validate that your JSON and XML files are well-formed.  No more accidental commas!  

```
usage: validator.py [-h] [-t {JSON,XML,BOTH}] [-d DIR]

Quick file validator for JSON and XML files

options:
  -h, --help            show this help message and exit
  -t {JSON,XML,BOTH}, --type {JSON,XML,BOTH}
                        Specify whether you want to validate JSON or XML(Default)
  -d DIR, --dir DIR     Specify a directory to search for files to validate.Multiple directories can be added using spaces between them
```
## items_loader.py

This utility will load up all the Market files in the Markets directory from the Root Profiles directory, it will validate them against a JSON schema, and then ensure all the Items are unique across all the Market files.

```
usage: items_loader.py [-h] [-d DIR]

Loads all the Market Items JSON files from the Markets directory and validates them against a schema, and ensures there is only one instance of every class in all Market files.

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Specify the Markets directory of Expansion Market folder to search for files to validate.

```
## types_loader.py

This utility will load up all types.xml files referenced in your Profiles directory; validate them against an XML schema, and ensure all classes loaded are unique across all files.

```
usage: types_loader.py [-h] [-d DIR]

Loads all the types.xml from the DayZ profiles directory and validates them against a schema, and ensures there is only one instance of every class in all types.xml files.

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Specify the root Profiles directory of DayZ to search for files to validate.
```

## airdrop_loader.py

```
usage: airdrop_loader.py [-h] [-d DIR] [-i ITEM] [-f FILE] [-s {d,default,m,medical,b,basebuilding,m,military}]

Searches for objects in a specified market file, adds those objects and all their variants to the airdropsettings, given each variant equal spawn chances.

options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Specify the root Expansion configuration directory to search for files to update.
  -i ITEM, --item ITEM  Specify the fragment of the item to search for, e.g. Diesel_TortillaBag
  -f FILE, --file FILE  Specify the specific Market file to examine
  -s {d,default,m,medical,b,basebuilding,m,military}, --section {d,default,m,medical,b,basebuilding,m,military}
                        Identifies the section of the airdrop settings file

```