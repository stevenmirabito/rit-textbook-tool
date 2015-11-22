"""
download.py
================
Provides a utility to download class and textbook data from Barnes & Noble.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


import barnesandnoble.data_helper
import barnesandnoble.web_helper


if __name__ == "__main__":
    # Display the welcome banner
    print("RIT Textbook Tool Download Utility")
    print("-----------------------------------------------------------", end='\n\n')

    # Prompt the user for a filename
    filename = str(input("Output file name: "))

    # Prompt the user for the term ID to download
    term_id = int(input("Term ID to download: "))  # Fall 2015 Term ID => 66316366

    # Run the downloader
    web_helper = barnesandnoble.web_helper.WebHelper(term_id)
    data = web_helper.get_tree()

    # Output the results to the specified file
    print("Saving...", end='')
    data_helper = barnesandnoble.data_helper.DataHelper(filename)
    data_helper.data = data
    data_helper.save()
    print("\rSaving... Done!")
