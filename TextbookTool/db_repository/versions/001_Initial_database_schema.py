from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(10))
    courses = relationship('Course', backref='department')

    def __repr__(self):
        return "<Department(id='%s', name='%s')>" % (self.id, self.name)


class Course(Base):
    __tablename__ = 'course'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(40))
    department_id = Column(Integer, ForeignKey('department.id'))
    sections = relationship('Section', backref='course')

    def __repr__(self):
        return "<Course(id='%s', name='%s', department_id='%s', sections='%s')>" % (
            self.id, self.name, self.department_id, self.sections)


class Section(Base):
    __tablename__ = 'section'
    id = Column('id', Integer, primary_key=True)
    number = Column('number', String(2))
    course_id = Column(Integer, ForeignKey('course.id'))
    textbooks = relationship('Textbook', backref='section')

    def __repr__(self):
        return "<Section(id='%s', number='%s', course_id='%s', textbooks='%s')>" % (
            self.id, self.number, self.course_id, self.textbooks)


class Textbook(Base):
    __tablename__ = 'textbook'
    isbn = Column('isbn', Integer, primary_key=True)
    title = Column('title', String(40))
    author = Column('author', String(40))
    edition = Column('edition', String(10))
    publisher = Column('publisher', String(40))
    required = Column('required', Boolean)
    buyback_price = Column('buyback_price', Numeric(12, 2))
    section_id = Column(Integer, ForeignKey('section.id'))

    def __repr__(self):
        return "<Textbook(isbn='%s', title='%s', author='%s', edition='%s', publisher='%s', required='%s', buyback_price='%s')>" % (
            self.isbn, self.title, self.author, self.edition, self.publisher, self.required, self.buyback_price)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    Base.metadata.create_all(migrate_engine)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    Base.metadata.drop_all(migrate_engine)
