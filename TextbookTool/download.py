"""
download.py
================
Provides a utility to download class and textbook data from Barnes & Noble.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

import TextbookTool.barnesandnoble.downloader
import TextbookTool.utilities.progressbar
import TextbookTool.db.connector
import TextbookTool.db.schema


def download():
    # Connect to the database
    db_connector = TextbookTool.db.connector.DatabaseConnector()
    db = db_connector.session

    # Prompt the user for the term ID to download
    term_id = int(input("Term ID to download: "))  # Fall 2015 Term ID => 66316366

    # Create a Downloader instance
    downloader = TextbookTool.barnesandnoble.downloader.Downloader(term_id)

    print("Downloading departments...", end='')

    departments = downloader.get_departments()
    db.add_all(departments)
    db.commit()

    print("\rDownloading departments... Done!")

    # Set up courses progress bar
    progress_params = {
        'end': len(departments),
        'width': 30,
        'fill': '#',
        'format': '%(current)s/%(end)s [%(fill)s%(blank)s] %(progress)s%%'
    }
    progress = TextbookTool.utilities.progressbar.ProgressBar(**progress_params)
    print("Downloading courses for each department... " + str(progress), end='')

    num_courses = 0
    courses = []

    for department in departments:
        courses.append(downloader.get_courses(department.id))
        num_courses += len(department.courses)
        progress + 1
        print("\rDownloading courses for each department... " + str(progress), end='')

    db.add_all(courses)
    db.commit()

    print("\rDownloading courses for each department... Done!")

    # Set up sections progress bar
    progress_params = {
        'end': num_courses,
        'width': 30,
        'fill': '#',
        'format': '%(current)s/%(end)s [%(fill)s%(blank)s] %(progress)s%%'
    }
    progress = TextbookTool.utilities.progressbar.ProgressBar(**progress_params)
    print("Downloading sections for each course... " + str(progress), end='')

    num_sections = 0
    sections = []

    for course in courses:
        sections.append(downloader.get_sections(course.id, course.department_id))
        num_sections += len(course.sections)
        progress + 1
        print("\rDownloading sections for each course... " + str(progress), end='')

    db.add_all(sections)
    db.commit()

    print("\rDownloading sections for each course... Done!")

    # Set up textbooks progress bar
    progress_params = {
        'end': num_sections,
        'width': 30,
        'fill': '#',
        'format': '%(current)s/%(end)s [%(fill)s%(blank)s] %(progress)s%%'
    }
    progress = TextbookTool.utilities.progressbar.ProgressBar(**progress_params)
    print("Downloading textbooks for each section... " + str(progress), end='')

    textbooks = []

    for section in sections:
        textbooks.append(downloader.get_textbooks(section.id))
        progress + 1
        print("\rDownloading textbooks for each section... " + str(progress), end='')

    db.add_all(textbooks)
    db.commit()

    print("\rDownloading textbooks for each section... Done!")


if __name__ == "__main__":
    # Display the welcome banner
    print("RIT Textbook Tool Downloader")
    print("-----------------------------------------------------------", end='\n\n')

    # Invoke the downloader
    download()
