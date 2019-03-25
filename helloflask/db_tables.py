from helloflask.init_db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship, backref

class User(Base):
    __tablename__ = 'User'

    user_no = Column(Integer, primary_key = True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    phone_number = Column(String)
    nickname = Column(String)
    address = Column(String)

    def __init__ (self, email, password, name, phone_number, nickname, address, makesha=False):

        if makesha:
            self.password = password
        else :
            self.password = func.sha2(password, 256)

        
        self.email = email
        self.phone_number = phone_number
        self.name = name
        self.nickname = nickname
        self.address = address


    def __repr__(self):
        return '%s, %s, %s, %s, %s, %s' %( self.email , self.password, self.name , self.phone_number, self.nickname, self.address)


class Board(Base):
    __tablename__ = 'Board'

    def __init__ (self, board_id, user_id, user_img, instrument, money) :
        self.board_id = board_id
        self.user_id = user_id
        self.user_img = user_img
        self.instrument = instrument
        self.money = money


    board_id = Column(Integer, primary_key = True)
    user_id = Column(Integer)
    user_img = Column(String)
    instrument = Column(String)
    money = Column(Integer)
    up_time = Column(TIMESTAMP)

    def json(self):
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return j
    #    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Instrument(Base):
    __tablename__ = 'Instrument'

    def __init__ (self, instrument_id, instrument_name) :
        self.instrument_id = instrument_id
        self.instrument_name = instrument_name
        

    instrument_id = Column(Integer, primary_key = True)
    instrument_name = Column(String)


    def json(self):
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return j
    #    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


