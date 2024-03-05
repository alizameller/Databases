'''
Sailors and Boats lecture script
@eugsokolov
Modified for PSET1
@alizameller
'''
from __future__ import print_function
import pytest
from ipdb import set_trace
from sqlalchemy import create_engine, text, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func
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

engine = create_engine(
    "postgresql://alizameller:@localhost:5432/postgres_copy")
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
        func.count()).group_by(sct.c.sid, 
                               sct.c.sname, 
                               sct.c.color).having(sct.c.color == 'red').cte("src")

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