"""
downloader.py
================
Provides functions for downloading data from Barnes & Noble.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

import json
import lxml.html
import requests
import TextbookTool.db.schema


class Downloader:
    def __init__(self, term_id):
        # B&N variables to use for each request
        self.campus_id = 31093371
        self.term_id = term_id
        self.store_id = 35554
        self.catalog_id = 10001
        self.lang_id = -1

        # Web request headers
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/42.0'}

    def get_departments(self):
        """
        Request the list of departments offering classes at RIT from B&N
        :return: List of Department objects (or an empty list if nothing is returned)
        """
        payload = {'campusId': self.campus_id,
                   'termId': self.term_id,
                   'storeId': self.store_id,
                   'catalogId': self.catalog_id,
                   'langId': self.lang_id,
                   'dropdown': 'term'}
        response = requests.get('http://rit.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd',
                                params=payload, headers=self.headers)

        # Add each department returned to the list
        departments = []
        for item in json.loads(response.text):
            departments.append(TextbookTool.db.schema.Department(id=item['categoryId'], name=item['title']))

        return departments

    def get_courses(self, department_id):
        """
        Constructs a list of Course objects for a department by requesting the list of
        courses for the passed department_id from Barnes & Noble.
        :param department_id: B&N ID of the department to search for
        :return: List of Course objects (or an empty list if the department does not offer any courses)
        """
        payload = {'campusId': self.campus_id,
                   'termId': self.term_id,
                   'deptId': department_id,
                   'storeId': self.store_id,
                   'catalogId': self.catalog_id,
                   'langId': self.lang_id,
                   'dropdown': 'dept'}
        response = requests.get('http://rit.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd',
                                params=payload, headers=self.headers)

        # Add each course returned to the department's list of courses
        courses = []
        for item in json.loads(response.text):
            courses.append(
                TextbookTool.db.schema.Course(id=item['categoryId'], name=item['title'], department_id=department_id))

        return courses

    def get_sections(self, course_id, department_id):
        """
        Constructs a list of Section objects for a course by requesting the list of sections
        for the passed course_id from Barnes & Noble.
        :param course_id: B&N ID of the course to search for
        :param department_id: Department ID for the course
        :return: List of Section objects (or an empty list if the course does not have any sections)
        """
        payload = {'campusId': self.campus_id,
                   'termId': self.term_id,
                   'deptId': department_id,
                   'courseId': course_id,
                   'storeId': self.store_id,
                   'catalogId': self.catalog_id,
                   'langId': self.lang_id,
                   'dropdown': 'course'}
        response = requests.get('http://rit.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd',
                                params=payload, headers=self.headers)

        # Add each section returned to a list
        sections = []
        for item in json.loads(response.text):
            sections.append(
                TextbookTool.db.schema.Section(id=item['categoryId'], number=item['categoryName'], course_id=course_id))

        return sections

    def get_textbooks(self, section_id):
        """
        Constructs a list of Textbook objects for a section by scraping the Barnes & Noble
        textbook results page for the passed section_id.
        :param section_id: B&N section ID to search for
        :return: List of Textbook objects (or an empty list if the section does not require a textbook)
        """
        payload = {'campus1': self.campus_id,
                   'firstTermId_31093371': self.term_id,
                   'section_1': section_id,
                   'storeId': self.store_id,
                   'catalogId': self.catalog_id,
                   'langId': self.lang_id,
                   'viewName': 'TBWizardView',
                   'mcEnabled': 'N',
                   'showCampus': 'false'}
        response = requests.get('http://rit.bncollege.com/webapp/wcs/stores/servlet/BNCBTBListView',
                                params=payload, headers=self.headers)

        # Parse the HTML into a tree
        tree = lxml.html.fromstring(response.content)

        # Scrape content from the page
        isbn = self._clean_xpath_list(
            tree.xpath('//*[@id="courseListForm"]/div[3]/div[2]/div/div/div[3]/ul/li[3]/text()'))
        title = self._clean_xpath_list(tree.xpath('//*[@id="courseListForm"]/div[3]/div[2]/div/div/div[1]/h1/text()'))
        author = self._clean_xpath_list(
            tree.xpath('//*[@id="courseListForm"]/div[3]/div[2]/div/div/div[3]/h2/span[3]/i/text()'))
        edition = self._clean_xpath_list(
            tree.xpath('//*[@id="courseListForm"]/div[3]/div[2]/div/div/div[3]/ul/li[1]/text()'))
        publisher = self._clean_xpath_list(
            tree.xpath('//*[@id="courseListForm"]/div[3]/div[2]/div/div/div[3]/ul/li[2]/text()'))
        required = self._clean_xpath_list(
            tree.xpath('//*[@id="courseListForm"]/div[3]/div[2]/div/div/div[3]/h2/span[1]/text()'))

        # Massage the data a bit
        author = [s.replace('By ', '') for s in author]

        # Create a list of Textbook objects with the data
        textbooks = []
        for book_index in range(0, len(isbn)):
            book_required = True if required[book_index] == 'REQUIRED' else False
            textbooks.append(
                TextbookTool.db.schema.Textbook(isbn=isbn[book_index],
                                                title=title[book_index],
                                                author=author[book_index],
                                                edition=edition[book_index],
                                                publisher=publisher[book_index],
                                                required=book_required,
                                                section_id=section_id))

        # Return the list
        return textbooks

    @staticmethod
    def _clean_xpath_list(xpath_list):
        return list(filter(None, map(str.strip, xpath_list)))
