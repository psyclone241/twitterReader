# Installation
* Requires the Twitter Libs found here
  https://github.com/sixohsix/twitter/tree/master

# Basic Usage
* Make a copy of config.py.example to config.py
* Edit your new config.py to your own configuration settings
* Run `python twitterReader.py`

# Advanced Usage
* For a specific feed
    * Default count: `python twitterReader.py -f feedname`
    * Custom count: `python twitterReader.py -f feedname -c 10`
* For configured or specific feeds
    * Save configured to json data: `python twitterReader.py -o json -s file.json`
    * Save specific feed to json data: `python twitterReader.py -f feedname -o json -f file.json`
