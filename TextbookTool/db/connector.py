"""
connector.py
================
Provides a connection interface to the SQLite database engine via SQLAlchemy.

This file is a part of RIT Textbook Tool.
Copyright (C) 2015 Steven Mirabito.

Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import TextbookTool.utilities.config


class DatabaseConnector:
    def __init__(self):
        config = TextbookTool.utilities.config.Config()
        db_type = config.ini.get('Database', 'type', fallback=None)
        db_driver = config.ini.get('Database', 'driver', fallback=None)

        if db_driver is None:
            # Use the default driver if one is not specified
            db_driver = ''
        else:
            db_driver = '+' + db_driver

        if db_type is None:
            print("You must specify a database type in the configuration file.")
            sys.exit()
        elif db_type == 'sqlite':
            db_path = config.ini.get('Database', 'path', fallback=None)
            if not os.path.isabs(db_path):
                db_path = config.basedir + '/' + db_path

            if db_path is None:
                print("You must specify a path to the SQLite database.")
                sys.exit()
            else:
                self.engine_uri = db_type + db_driver + '://' + db_path
                print(self.engine_uri)
                self.engine = create_engine(self.engine_uri)
                session = sessionmaker(bind=self.engine)
                self.session = session()
        else:
            db_user = config.ini.get('Database', 'username', fallback=None)
            db_pass = config.ini.get('Database', 'password', fallback=None)
            db_host = config.ini.get('Database', 'host', fallback=None)
            db_port = config.ini.get('Database', 'port', fallback=None)
            db_name = config.ini.get('Database', 'name', fallback=None)

            if db_user or db_pass or db_host or db_port or db_name is None:
                print("You must provide all required database connection details in the configuration file.")
                sys.exit()
            else:
                self.engine_uri = db_type + db_driver + '://' + db_user + ':' + db_pass + '@' + db_host + ':' + db_port + '/' + db_name
                self.engine = create_engine(self.engine_uri)
                session = sessionmaker(bind=self.engine)
                self.session = session()
