"""
department.py
================
Provides a class to represent academic departments.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


class Department:
    def __init__(self, department_id, department_name):
        self.id = department_id
        self.name = department_name
        self.courses = []

    def __repr__(self):
        return str(vars(self))
