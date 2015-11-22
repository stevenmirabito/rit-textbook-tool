"""
view.py
================
Provides a utility to load and display saved data from a file.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


import barnesandnoble.data_helper
from pprint import pprint


if __name__ == "__main__":
    # Display the welcome banner
    print("RIT Textbook Tool Data Viewer")
    print("Copyright (C) 2015 Steven Mirabito. All rights reserved.")
    print("-----------------------------------------------------------", end='\n\n')

    # Prompt the user for a filename
    filename = str(input("Data file name: "))

    data_helper = barnesandnoble.data_helper.DataHelper(filename)
    data_helper.load()
    pprint(data_helper.data)
