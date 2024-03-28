from __future__ import print_function
import pytest
from ipdb import set_trace
from sqlalchemy import create_engine, text, Integer, String, Column, func
from sqlalchemy.orm import sessionmaker, declarative_base
from tabulate import tabulate

Base = declarative_base()
# CREATE TABLE half_time(id INT, name VARCHAR, abv FLOAT NULL, color_rating INT, hop_rating INT NULL, brewery VARCHAR, state VARCHAR, style VARCHAR, food_pairing VARCHAR NULL);
class half_time(Base):
    __tablename__ = 'half_time'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abv = Column(Integer)
    color_rating = Column(Integer)
    hope_rating = Column(Integer)
    brewery = Column(String)
    state = Column(String)
    style = Column(String) 
    food_pairing = Column(String)

    def __repr__(self):
        return "<half_time(id=%s, name='%s', abv=%s, color_rating=%s, hope_rating=%s, brewery='%s', state='%s', style='%s', food_pairing='%s')>" % (self.id, self.name, self.abv, self.color_rating, self.hope_rating, self.brewery, self.state, self.style, self.food_pairing)

engine = create_engine(
    "postgresql://alizameller:@localhost:5432/hw2")
Session = sessionmaker(bind=engine)
s = Session()

# Query shows beers where the abv is higher than 7 -- useful when looking for boozy beers
def test_question1():
    output = s.query(
        half_time.name, 
        half_time.abv,).where(half_time.abv > 7).all()

    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT name, abv " + 
                                                  "FROM half_time "
                                                  "WHERE abv > 7;"))
    
    print(tabulate(output, headers=("name","abv"), tablefmt='psql'))
    
    assert expected_output.fetchall() == output

# Query shows beers that contain "meat" in the food pairing -- useful when looking for beers that pair well with meat 
def test_question2():
    output = s.query(
        half_time.name, 
        half_time.food_pairing,).where(half_time.food_pairing.like("%meat%")).all()

    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT name, food_pairing " + 
                                                  "FROM half_time " + 
                                                  "WHERE food_pairing like '%meat%';"))
    
    print(tabulate(output, headers=("name","food_pairing"), tablefmt='psql'))
    
    assert expected_output.fetchall() == output

# Query shows count of IPAs from each brewery and the state of the brewery (ordered by state) -- just an interesting statistic
def test_question3():
    output = s.query(
        half_time.brewery,
        half_time.state,
        func.count(half_time.style)).where(half_time.style.like("%IPA%")).group_by(half_time.brewery, half_time.state).order_by(half_time.state).all()

    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT brewery, state, COUNT(style) " + 
                                                  "FROM half_time " + 
                                                  "WHERE style LIKE '%IPA%' " + 
                                                  "GROUP BY brewery, state " +
                                                  "ORDER BY state;"))
    
    print(tabulate(output, headers=("brewery","state", "count"), tablefmt='psql'))
    
    assert expected_output.fetchall() == output
    