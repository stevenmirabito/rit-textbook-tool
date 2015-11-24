#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(debug='False', repository='db_repository', url='sqlite:///textbooktool.db')
