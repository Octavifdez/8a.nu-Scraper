from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    city = Column(String)
    country = Column(String)
    sex = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    started = Column(Integer)
    competitions = Column(String)
    occupation = Column(String)
    sponsor1 = Column(String)
    sponsor2 = Column(String)
    sponsor3 = Column(String)
    best_area = Column(String)
    worst_area = Column(String)
    guide_area = Column(String)
    interests = Column(String)
    birth = Column(Date)
    presentation = Column(String)
    deactivated = Column(Integer)
    anonymous = Column(Integer)


class Method(Base):
    __tablename__ = 'method'

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    shorthand = Column(String)
    name = Column(String)


class Grade(Base):
    __tablename__ = 'grade'

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    fra_routes = Column(String)
    fra_routes_input = Column(Boolean)
    fra_routes_selector = Column(Boolean)
    fra_boulders = Column(String)
    fra_boulders_input = Column(Boolean)
    fra_boulders_selector = Column(Boolean)
    usa_routes = Column(String)
    usa_routes_input = Column(Boolean)
    usa_routes_selector = Column(Boolean)
    usa_boulders = Column(String)
    usa_boulders_input = Column(Boolean)
    usa_boulders_selector = Column(Boolean)


class Ascent(Base):
    __tablename__ = 'ascent'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    grade_id = Column(Integer, ForeignKey('grade.id'))
    grade = relationship(Grade)

    notes = Column(String)
    raw_notes = Column(Integer)

    method_id = Column(Integer, ForeignKey('method.id'))
    method = relationship(Method)

    climb_type = Column(Integer)
    total_score = Column(Integer)
    date = Column(Integer)
    year = Column(Integer)
    last_year = Column(Boolean)
    rec_date = Column(Integer)
    project_ascent_date = Column(Integer)
    name = Column(String)
    crag_id = Column(Integer)
    crag = Column(String)
    sector_id = Column(Integer)
    sector = Column(String)
    country = Column(String)
    comment = Column(String)
    rating = Column(Integer)
    description = Column(String)
    yellow_id = Column(Integer)
    climb_try = Column(Boolean)
    repeat = Column(Boolean)
    exclude_from_ranking = Column(Boolean)
    user_recommended = Column(Boolean)
    chipped = Column(Boolean)


engine = create_engine('sqlite:///8adata.db')

Base.metadata.create_all(engine)