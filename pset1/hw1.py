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
- I made a class for the table employees which keeps track of the employees who work with the boats.
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

    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT B.bname, B.bid, COUNT(*) " + 
                                                  "FROM boats as B " +
                                                  "INNER JOIN reserves as R ON R.bid = B.bid " +
                                                  "GROUP BY B.bid " +
                                                  "ORDER BY B.bid ASC"))
    
    assert expected_output.fetchall() == output
    
def test_question2():
    count = (s.query(func.count()).where(Boat.color == 'red').all())[0][0]
    output = s.query(
        Reservation.sid, 
        Sailor.sname).join(Boat).join(Sailor).where(Boat.color == 'red').group_by(Reservation.sid, Sailor.sname).having(func.count(Reservation.bid) == count).all()

    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT R.sid, S.sname " +
                                                  "FROM reserves R " +
                                                  "INNER JOIN boats B ON R.bid = B.bid " +
                                                  "INNER JOIN sailors S on R.sid = S.sid " +
                                                  "WHERE B.color = 'red' " +
                                                  "GROUP BY R.sid, S.sname " +
                                                  "HAVING COUNT(DISTINCT R.bid) = (SELECT COUNT(*) " +
                                                                                   "FROM boats B " +
                                                                                   "WHERE B.color = 'red')"))
    
    assert expected_output.fetchall() == output

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
    
    with engine.connect() as connection:
        expected_output = connection.execute(text("WITH sailor_color_table AS (SELECT R.sid, S.sname, B.color " +
                                                                                "FROM reserves R " +
                                                                                "INNER JOIN boats B ON R.bid = B.bid " +
                                                                                "INNER JOIN sailors S on R.sid = S.sid), " + 
                                                    "sailors_red_count AS (SELECT sailor_color_table.sid, sailor_color_table.sname, COUNT(*) " +
                                                                           "FROM sailor_color_table " +
                                                                           "WHERE sailor_color_table.color = 'red' " +
                                                                           "GROUP BY sailor_color_table.sid, sailor_color_table.sname) " +
                                                    "SELECT SCT.sname, SCT.sid " +
                                                    "FROM sailors_red_count SRC " +
                                                    "INNER JOIN sailor_color_table SCT on SCT.sid = SRC.sid " +
                                                    "GROUP BY SCT.sid, SCT.sname, SRC.count " +
                                                    "HAVING COUNT(SCT.sname) = SRC.count "))
    
    assert expected_output.fetchall() == output

def test_question4():
    output = s.query(Boat.bname, 
                     Boat.bid, 
                     func.count(Reservation.bid)).join(Reservation).group_by(Boat.bname, Boat.bid).order_by((func.count(Reservation.bid)).desc()).limit(1).all()
    
    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT B.bname, B.bid, COUNT(R.bid) " +
                                                  "FROM boats B " +
                                                  "INNER JOIN reserves R ON R.bid = B.bid " +
                                                  "GROUP BY B.bname, B.bid " +
                                                  "ORDER BY COUNT(R.bid) DESC " +
                                                  "LIMIT 1"))
    
    assert expected_output.fetchall() == output

def test_question5():
    reserved_red = s.query(Reservation.sid).join(Boat).where(Boat.color == 'red')
    exception = s.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.in_(reserved_red))
    output = s.query(Sailor.sid, Sailor.sname).except_(exception).all()

    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT S.sid, S.sname " +
                                                  "FROM sailors S " +
                                                  "EXCEPT " +
                                                  "SELECT S.sid, S.sname " +
                                                  "FROM sailors S " +
                                                  "WHERE S.sid IN (SELECT R.sid " +
                                                                  "FROM reserves R " +
                                                                  "INNER JOIN boats B ON R.bid = B.bid " +
                                                                  "WHERE B.color = 'red')"))

    assert output == expected_output.fetchall()

def test_question6():
    sailors_rated_10 = s.query(Sailor.sid, Sailor.sname, Sailor.age).where(Sailor.rating == 10).cte("sailors_rated_10")
    output = s.query(func.avg(sailors_rated_10.c.age)).all()
    
    with engine.connect() as connection:
        expected_output = connection.execute(text("WITH sailors_rated10 AS (SELECT S.sid, S.sname, S.age " +
                                                                            "FROM sailors S " +
                                                                            "WHERE S.rating = 10) " +
                                                    "SELECT AVG(S.age) " +
                                                    "FROM sailors_rated10 S"))

    assert output == expected_output.fetchall()

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
    
    with engine.connect() as connection:
        expected_output = connection.execute(text("WITH youngest AS (SELECT S.sid, S.sname, S.age, S.rating, MIN(S.age) " +
                                                                    "OVER (PARTITION BY S.rating) " +
                                                                    "AS YoungestSailor FROM sailors S) " +
                                                 "SELECT Y.sname, Y.sid, Y.rating, Y.age " +
                                                 "FROM youngest Y " +
                                                 "WHERE Y.age = Y.youngestsailor"))

    assert output == expected_output.fetchall()

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
    
    with engine.connect() as connection:
        expected_output = connection.execute(text("WITH num_reserves_per_boat AS (SELECT R.bid, S.sid, S.sname, COUNT(*) " +
                                                                                 "FROM sailors S " +
                                                                                 "INNER JOIN reserves R ON S.sid = R.sid " +
                                                                                 "GROUP BY R.bid, S.sid, S.sname) " +
                                                 "SELECT bid, sid, sname, count " +
                                                 "FROM " +
                                                    "(SELECT N.bid, N.sid, N.sname, N.count, MAX(N.count) " +
                                                    "OVER (PARTITION BY N.bid) " +
                                                    "AS maximum FROM num_reserves_per_boat N) AS temp " +
                                                 "WHERE temp.maximum = temp.count"))

    assert output == expected_output.fetchall()

# I use this test to find all employees (id, name, role) that work on red boats
def test_employees():
    output = s.query(
        Employee.eid,
        Employee.ename, 
        Employee.role).join(Boat).where(Boat.color == 'red').all()
    
    with engine.connect() as connection:
        expected_output = connection.execute(text("SELECT eid, ename, role FROM employees " +
                                                  "INNER JOIN boats ON employees.bid = boats.bid " +
                                                  "WHERE boats.color = 'red'"))
    
    assert expected_output.fetchall() == output