from helloflask.init_db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey, PrimaryKeyConstraint, func, Date
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

    def __init__ (self, board_title, due_date, qualification , gender, money, practice_time, perform_time, costume, practice_address,perform_address, detail_info, song_info, user_id) :
        self.board_title = board_title
        self.due_date = due_date
        self.qualification = qualification
        self.gen = gender
        self.money = money
        self.practice_time = practice_time
        self.perform_time = perform_time
        self.costume = costume
        self.practice_address = practice_address
        self.perform_address = perform_address
        self.detail_info = detail_info
        self.song_info = song_info
        self.user_id = user_id




    board_id = Column(Integer, primary_key = True)
    board_title = Column(String)
    due_date = Column(Date)
    qualification = Column(Integer)
    gen = Column(Integer)
    money = Column(Integer)
    practice_time = Column(Integer)
    perform_time = Column(Integer)
    costume = Column(Integer)
    practice_address = Column(String)
    perform_address = Column(String)
    detail_info = Column(String)
    song_info = Column(String)
    user_id = Column(Integer)
    upload_time = Column(TIMESTAMP)

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


