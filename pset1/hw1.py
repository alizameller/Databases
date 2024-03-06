'''
Sailors and Boats lecture script
@eugsokolov
Modified for PSET1
@alizameller

Invoke using:
$ pytest -s hw1.py
'''
from __future__ import print_function
import pytest
from ipdb import set_trace
from sqlalchemy import create_engine, text, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, select
from sqlalchemy.orm import sessionmaker, declarative_base, backref, relationship

Base = declarative_base()

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s)>" % (self.sid, self.sname, self.age)

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color)

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor')

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day)

# This is for part 3
class Employee(Base):
    __tablename__ = 'employees'

    eid = Column(Integer, primary_key=True)
    ename = Column(String)
    salary = Column(Integer)
    role = Column(String)
    bid = Column(Integer, ForeignKey('boats.bid'))

    def __repr__(self):
        return "<Employee(id=%s, name='%s', salary='%s', role=%s, bid='%s')>" % (self.eid, self.ename, self.salary, self.role, self.bid)

'''
- I made a class for the table employees which keeps track of the employees who work with the boats
- Every employee has a unique eid and works as some role on a specific boat 
- I made the above class as a table with the following command:

CREATE TABLE employees(eid int PRIMARY KEY, 
                       ename varchar(30), 
                       salary int, 
                       role varchar(30), 
                       bid int);

I populated it with the following data using the following commands:
insert into employees values (51,'david',30000,'cleaner', 110);
insert into employees values (86,'serene',190000,'deckhand', 101);
insert into employees values (23,'yuri',20000,'deckhand', 105);
insert into employees values (78,'faith',8,'cleaner', 105);
insert into employees values (69,'aliza',100,'deckhand', 107);
insert into employees values (12,'john',35000,'operator', 104);
insert into employees values (2,'david',170000,'operator', 106);
insert into employees values (43,'brian',400,'operator', 110);
insert into employees values (41,'evan',100000,'cleaner', 108);
insert into employees values (27,'jakey',45000,'engineer', 101);
insert into employees values (9,'lizelle',9000,'repairman', 102);
insert into employees values (17,'jacob',15,'operator', 103);
'''

engine = create_engine(
    "postgresql://alizameller:@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
s = Session()

def test_question1():
    output = s.query(
        Boat.bname, 
        Boat.bid, 
        func.count()).join(Reservation).group_by(Boat.bid).order_by(Boat.bid.asc()).all()
    
    bnames = [] 
    bids = []
    count = []
    for row in output:
        bnames.append(row[0].replace('\t', ' ').strip())
        bids.append(row[1])
        count.append(row[2])

    expected_bname = ['Interlake', 'Interlake', 'Clipper', 'Clipper', 'Marine', 'Marine', 'Marine', 'Driftwood', 'Driftwood', 'Klasper', 'Sooney', 'Sooney']
    expected_bid = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]
    expected_count = [2, 3, 3, 5, 3, 3, 1, 1, 4, 3, 1, 1]

    assert (bnames.sort(), bids.sort(), count.sort()) == (expected_bname.sort(), expected_bid.sort(), expected_count.sort())

def test_question2():
    count = (s.query(func.count()).where(Boat.color == 'red').all())[0][0]
    output = s.query(
        Reservation.sid, 
        Sailor.sname).join(Boat).join(Sailor).where(Boat.color == 'red').group_by(Reservation.sid, Sailor.sname).having(func.count(Reservation.bid) == count).all()

    assert output == []

def test_question3():
    sct = s.query(
    Reservation.sid,
    Sailor.sname, 
    Boat.color).join(Boat).join(Sailor).cte("sct")
    
    src = s.query(
        sct.c.sid, 
        sct.c.sname, 
        func.count()).where(sct.c.color == 'red').group_by(sct.c.sid, 
                                                        sct.c.sname).cte("src")

    output = s.query(sct.c.sname, sct.c.sid).select_from(src).join(sct, src.c.sid == sct.c.sid).group_by(sct.c.sid, sct.c.sname, src.c.count).having(func.count(sct.c.sname) == src.c.count).all()
    
    snames = [] 
    sids = []
    for row in output:
        snames.append(row[0].replace('\t', ' ').strip())
        sids.append(row[1])

    expected_sname = ['shaun', 'emilio', 'ossola', 'scruntus', 'figaro']
    expected_sid = [62, 23, 61, 24, 35]
    
    assert (snames.sort(), sids.sort()) == (expected_sname.sort(), expected_sid.sort())

def test_question4():
    output = s.query(Boat.bname, 
                     Boat.bid, 
                     func.count(Reservation.bid)).join(Reservation).group_by(Boat.bname, Boat.bid).order_by((func.count(Reservation.bid)).desc()).limit(1).all()
    
    bnames = []
    bids = []
    count = []
    for row in output:
        bnames.append(row[0].replace('\t', ' ').strip())
        bids.append(row[1])
        bids.count(row[2])

    expected_bname = ['Clipper']
    expected_bid = [104]
    expected_count = [5]

    assert (bnames.sort(), bids.sort(), count.sort()) == (expected_bname.sort(), expected_bid.sort(), expected_count.sort())

def test_question5():
    total_reserves = s.query(Reservation.sid)
    reserved_red = s.query(Reservation.sid).join(Boat).where(Boat.color == 'red')
    exception = s.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.in_(reserved_red))
    output = s.query(Sailor.sid, Sailor.sname).join(Reservation).filter(Sailor.sid.in_(total_reserves)).except_(exception).all()
    
    snames = []
    sids = []
    for row in output:
        snames.append(row[1].replace('\t', ' ').strip())
        sids.append(row[0])

    expected_sname = ['horatio', 'vin', 'jit']
    expected_sid = [74, 90, 60]

    assert (snames.sort(), sids.sort()) == (expected_sname.sort(), expected_sid.sort())

def test_question6():
    sailors_rated_10 = s.query(Sailor.sid, Sailor.sname, Sailor.age).where(Sailor.rating == 10).cte("sailors_rated_10")
    output = s.query(func.avg(sailors_rated_10.c.age)).all()
    
    assert output[0][0] == 35.0000000000000000

def test_question7():
    youngest = s.query(
        Sailor.sid,
        Sailor.sname, 
        Sailor.age,
        Sailor.rating,
        func.min(Sailor.age).over(
            partition_by=Sailor.rating).label('youngestsailor')).subquery()
    
    output = s.query(
        youngest.c.sname,
        youngest.c.sid,
        youngest.c.rating,
        youngest.c.age).where(youngest.c.age == youngest.c.youngestsailor).all()
    
    snames = []
    sids = []
    ages = []
    ratings = []
    for row in output:
        snames.append(row[0].replace('\t', ' ').strip())
        sids.append(row[1])
        ratings.append(row[2])
        ages.append(row[3])

    expected_sname = ['scruntus', 'brutus', 'art', 'dye', 'horatio', 'ossola', 'andy', 'stum', 'dan', 'horatio', 'jit', 'zorba', 'shaun', 'rusty']
    expected_sid = [24, 29, 85, 89, 64, 61, 32, 59, 88, 74, 60, 71, 62, 58]
    expected_ratings = [1, 1, 3, 3, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10]
    expected_ages = [33, 33, 25, 25, 16, 16, 25, 25, 25, 25, 35, 35, 35, 35]

    assert (snames.sort(), sids.sort(), ages.sort(), ratings.sort()) == (expected_sname.sort(), expected_sid.sort(), expected_ratings.sort(), expected_ages.sort())

def test_question8():
    num_reserves_per_boat = s.query(
    Reservation.bid,
    Sailor.sid, 
    Sailor.sname, 
    func.count()).join(Reservation).group_by(Reservation.bid, Sailor.sid, Sailor.sname).order_by(Reservation.bid).cte("num_reserves_per_boat")
    
    highest_num_res = s.query(
        num_reserves_per_boat.c.bid,
        num_reserves_per_boat.c.sid,
        num_reserves_per_boat.c.sname, 
        num_reserves_per_boat.c.count.label('count'),
        func.max(num_reserves_per_boat.c.count).over(
            partition_by=num_reserves_per_boat.c.bid).label('maximum')).subquery()

    output = s.query(highest_num_res.c.bid, 
                     highest_num_res.c.sid, 
                     highest_num_res.c.sname, 
                     highest_num_res.c.count).where(highest_num_res.c.maximum == highest_num_res.c.count).all()
    
    bids = []
    sids = []
    snames = []
    counts = []
    for row in output:
        bids.append(row[0])
        sids.append(row[1])
        snames.append(row[2].replace('\t', ' ').strip())
        counts.append(row[3])

    expected_bids = [101, 101, 102, 102, 102, 103, 103, 103, 104, 104, 104, 104, 104, 105, 105, 105, 106, 107, 108, 109, 109, 109, 109, 110, 111, 112]
    expected_sids = [22, 64, 22, 31, 64, 22, 31, 74, 22, 23, 24, 31, 35, 23, 35, 59, 60, 88, 89, 59, 60, 89, 90, 88, 88, 61]
    expected_snames = ['dusting', 'horatio', 'dusting', 'lubber', 'horatio', 'dusting', 'lubber', 'horatio', 'dusting', 'emilio', 'scruntus', 'lubber', 'figaro', 'emilio', 'figaro', 'stum', 'jit', 'dan', 'dye', 'stum', 'jit', 'dye', 'vin', 'dan', 'dan', 'ossola']
    expected_counts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1]
    
    assert (bids.sort(), sids.sort(), snames.sort(), counts.sort()) == (expected_bids.sort(), expected_sids.sort(), expected_snames.sort(), expected_counts.sort())

# I use this test to find all employees (id, name, role) that work on red boats
def test_employees():
    output = s.query(
        Employee.eid,
        Employee.ename, 
        Employee.role).join(Boat).where(Boat.color == 'red').all()
    
    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT * FROM employees INNER JOIN boats ON employees.bid = boats.bid WHERE boats.color = 'red'"))
    
    assert expected_output.fetchall().sort() == output.sort()