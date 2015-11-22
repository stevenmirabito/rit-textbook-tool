"""
data_helper.py
================
Provides functions for loading and saving data files.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


from barnesandnoble.model import course, department, section, textbook
import os
import pickle


class DataHelper:
    def __init__(self, filename):
        self.data = None
        self.filename = filename

    def save(self):
        """
        Saves the passed data tree to the passed filename
        :param filename: Filename to write data to
        :param data: Data tree to write to file
        :return: Boolean
        """
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.filename), 'wb') as file:
                pickle.dump(self.data, file)
                return True
        except OSError as e:
            print("Unable to open file " + e.filename + ": " + e.strerror)
            return False
        except pickle.PicklingError as e:
            print("Unable to save data: " + str(e))
            return False

    def load(self):
        """
        Loads and returns the data tree from the passed filename
        :param filename: Filename to open and load the data tree from
        :return: Boolean
        """
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.filename), 'rb') as file:
                data = pickle.load(file)
                if self._check_data(data):
                    self.data = data
                    return True
        except OSError as e:
            print("Unable to open file " + e.filename + ": " + e.strerror)
            return False
        except pickle.UnpicklingError as e:
            print("Unable to load data: " + str(e))
            return False
        except TypeError as e:
            print("Data file is corrupted or not of the correct type: " + str(e))
            return False

    def _check_data(self, data):
        """
        Checks a loaded data tree for the correct object types
        :param data: Data tree to check
        :return: Boolean
        """
        if isinstance(data, list):
            if self._check_list_type(data, department.Department):
                for d in data:
                    if self._check_list_type(d.courses, course.Course):
                        for c in d.courses:
                            if self._check_list_type(c.sections, section.Section):
                                for s in c.sections:
                                    if self._check_list_type(s.textbooks, textbook.Textbook):
                                        return True

    @staticmethod
    def _check_list_type(list, type):
        """
        Iterates through the passed list to determine if all items are of the passed type
        :param list: List to check
        :param type: Type to check against
        :return: Boolean
        """
        for item in list:
            if not isinstance(item, type):
                raise TypeError(str(item) + ' is not of type: ' + str(type.__class__.__name__))

        # If we get here, no exceptions were raised, so all items were of the prescribed type
        return True
