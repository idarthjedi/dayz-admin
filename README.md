# dayz-admin
Author: 
    DarthJedi

Initial Release Date: 
    02/2023

A collection of utilities and scripts I've written to help in my DayZ Management
## src/main.py

This loads the main application (WIP) that brings a GUI interface to all the different utilities written within this toolset.

![image_mainUI.jpg](src%2Fconfig%2Fresources%2Fimage_mainUI.jpg)

## src/validatorUI.py (Validator quicktest)

This will load a GUI to set the directory structure, and upon closing, will validate the DayZ Profile XML Files, and optionally the well-formedness of the JSON and XML files in various directories.

![image_configUI.jpg](src%2Fconfig%2Fresources%2Fimage_configUI.jpg)

### src/config/app-config.json

This file is created the first time the application requests configuration information and stored locally.  Delete this file to recreate the config file upon next config run.

## standalone/validator.py

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
## standalone/items_loader.py

This utility will load up all the Market files in the Markets directory from the Root Profiles directory, it will validate them against a JSON schema, and then ensure all the Items are unique across all the Market files.

```
usage: items_loader.py [-h] [-d DIR]

Loads all the Market Items JSON files from the Markets directory and validates them against a schema, and ensures there is only one instance of every class in all Market files.

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Specify the Markets directory of Expansion Market folder to search for files to validate.

```
## standalone/types_loader.py

This utility will load up all types.xml files referenced in your Profiles directory; validate them against an XML schema, and ensure all classes loaded are unique across all files.

```
usage: types_loader.py [-h] [-d DIR]

Loads all the types.xml from the DayZ profiles directory and validates them against a schema, and ensures there is only one instance of every class in all types.xml files.

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Specify the root Profiles directory of DayZ to search for files to validate.
```

## standalone/airdrop_loader.py

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
## standalone/trader_to_expansion.py

```
usage: traderplus_to_expansion.py [-h] -f FILE [-m MULTIPLIER]

Takes as input the name of a traderplus file, and will output an Expansion trader file of the same name with category extensions (e.g.) FILE=geb_trader, output=geb_trader_fish.json, geb_trader_fishmeat.json, etc. Code
optionally takes a multiplier (float) to apply against the priceses listed in the traderplus file e.g. 1.5 multiper will make the prices 1.5 times higher than in the original traderplus file.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Specify the TraderPlus file name to convert.
  -m MULTIPLIER, --multiplier MULTIPLIER
                        Specify the optional price multiplier for the TraderPlus to Expansion conversion

```

## standalone/types_to_market.py
```
usage: types_to_market.py [-h] [-f FILE] [-p PRICE] [-c CATEGORY]

Loads the type file specified, and converts it into a market file, using pre-defined defaults.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Specify the types file to convert.
  -p PRICE, --price PRICE
                        Specify the default price for the imported items.
  -c CATEGORY, --category CATEGORY
                        Specify the Category name for the imported items.
```
## Attribution

Some icons by [Yusuke Kamiyamane](http://p.yusukekamiyamane.com/). Licensed under a [Creative Commons Attribution 3.0 License](http://creativecommons.org/licenses/by/3.0/).
