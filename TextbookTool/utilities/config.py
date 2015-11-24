"""
config.py
================
Configuration parser utility

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


import os
import sys
import configparser


class Config:
    def __init__(self):
        self.basedir = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.ini = configparser.ConfigParser()

        try:
            with open(self.basedir + '/settings.ini') as config_file:
                self.ini.read_file(config_file)
        except OSError as e:
            print("Unable to open configuration file " + e.filename + ": " + e.strerror)
            sys.exit(1)
        except configparser.ParsingError as e:
            print("Unable to parse configuration file: " + str(e))
            sys.exit(1)
