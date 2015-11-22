"""
section.py
================
Provides a class to represent a section of a course.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


class Section:
    def __init__(self, section_id, section_number):
        self.id = section_id
        self.number = section_number
        self.textbooks = []

    def __repr__(self):
        return str(vars(self))
