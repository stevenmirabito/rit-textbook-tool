"""
course.py
================
Provides a class to represent courses.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


class Course:
    def __init__(self, course_id, course_name):
        self.id = course_id
        self.name = course_name
        self.sections = []

    def __repr__(self):
        return str(vars(self))
