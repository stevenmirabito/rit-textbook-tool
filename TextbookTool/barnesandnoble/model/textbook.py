"""
textbook.py
================
Provides a class to represent a textbook.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


class Textbook:
    def __init__(self, isbn, title, author, edition, publisher, required):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.edition = edition
        self.publisher = publisher
        self.required = required
        self.buyback_price = 0

    def __repr__(self):
        return str(vars(self))
