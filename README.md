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

## loader.py

This utility will load up all types.xml files referenced in your Profiles directory; validate them against an XML schema, and ensure all classes loaded are unique across all files.

```
usage: loader.py [-h] [-d DIR]

Loads all the types.xml from the DayZ profiles directory and validates them against a schema, and ensures there is only one instance of every class in all types.xml files.

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Specify the root Profiles directory of DayZ to search for files to validate.
```