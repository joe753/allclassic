from helloflask.init_db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey, PrimaryKeyConstraint, func, Date
from sqlalchemy.orm import relationship, backref

class Users(Base):
    __tablename__ = 'Users'

    user_no = Column(Integer, primary_key = True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    phone_number = Column(String)
    nickname = Column(String)
    address = Column(String)
    premium = Column(Integer)
    profile_img = Column(String)
    user_video = Column(String)
    user_account = Column(String)
    qualification = Column(Integer)
    reward = Column(String)
    user_detail = Column(String)
    # premium, profile_img, user_video, user_account, qualification, reward, user_detail,
    def __init__ (self, email, password, name, phone_number, nickname, address,  makesha=False):

        if makesha:
            self.password = password
        else :
            self.password = func.sha2(password, 256)

        
        self.email = email
        self.phone_number = phone_number
        self.name = name
        self.nickname = nickname
        self.address = address
        # self.premium = premium
        # self.profile_img = profile_img
        # self.user_video = user_video
        # self.user_account = user_account
        # self.qualification = qualification
        # self.reward = reward
        # self.user_detail = user_detail

    def __repr__(self):
        return '%s, %s, %s, %s, %s, %s' %( self.email , self.password, self.name , self.phone_number, self.nickname, self.address)


class Board(Base):
    __tablename__ = 'Board'

    def __init__ (self, board_title, due_date, qualification , gender, money, practice_time, perform_time,  costume, practice_address, practice_mapx,  practice_mapy, perform_address, area_number, perform_mapx, perform_mapy,  detail_info, song_info, user_id) :
        self.board_title = board_title
        self.due_date = due_date
        self.qualification = qualification
        self.gen = gender
        self.money = money
        self.practice_time = practice_time
        self.perform_time = perform_time
        self.costume = costume
        self.practice_address = practice_address
        self.practice_mapx = practice_mapx
        self.practice_mapy = practice_mapy
        self.perform_address = perform_address
        self.area_number = area_number
        self.perform_mapx = perform_mapx
        self.perform_mapy = perform_mapy
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
    practice_mapx = Column(String)
    practice_mapy = Column(String)
    perform_address = Column(String)
    area_number = Column(Integer)
    perform_mapx = Column(String)
    perform_mapy = Column(String)
    detail_info = Column(String)
    song_info = Column(String)
    user_id = Column(Integer, ForeignKey('Users.user_no') , nullable=False)
    upload_time = Column(TIMESTAMP)
    users = relationship("Users" )

   


    def json(self):
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        j["user_nickname"] = self.users.nickname
        # j["user_img"] = self.users.profile_img
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

class BoardInstrument(Base):
    __tablename__ = "BoardInstrument"

    def __init__ (self, board_id, instrument_id, person):
        self.board_id = board_id
        self.instrument_id = instrument_id
        self.person = person

    id = Column(Integer, primary_key = True)
    board_id = Column(Integer, ForeignKey('Board.board_id'), nullable=False)
    instrument_id = Column(Integer,  ForeignKey('Instrument.instrument_id'), nullable=False)
    person = Column(Integer)
    board = relationship("Board")
    instrument = relationship('Instrument')
    # board = relationship("Board", lazy = "joined")
    # instrument = relationship('Instrument', lazy="joined")

    def json(self):
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        j['instrument_name'] = self.instrument.instrument_name
        j['user_id'] = self.board.user_id   

        return j