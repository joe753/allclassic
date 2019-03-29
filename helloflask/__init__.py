from flask import Flask, g, request, Response, make_response, flash, redirect, jsonify
import json
from flask import session, render_template, Markup
from datetime import date, datetime
from helloflask.db_tables import User, Board, Instrument, BoardInstrument
from helloflask.init_db import db_session
from sqlalchemy.orm import subqueryload, joinedload, relationship, backref
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey



app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
# app.jinja_env.trim_blocks = True


@app.route('/lesson')
def lesson():
    return render_template('lesson.html')

@app.route('/perform/detail/board01')
def p_bbs01():
    row = ["title","기간","user0222"]
    return render_template('board01.html', lst=row)

@app.route('/add/perform/pboard01')
def add_pboard():
    return render_template('add_board.html')

@app.route('/perform')
def perform():
    return render_template('perform.html')


@app.route('/perform/detail/board<boardid>', methods=["GET"])
def board (boardid) : 
    
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",boardid)
    return render_template('board01.html', boardid=boardid)



@app.route('/signup', methods=['GET', 'POST'])
def signup_modal():
    email = request.form.get('email')
    password = request.form.get('password')
    cfpassword = request.form.get('cfpassword')
    name = request.form.get('name')
    phone_number = request.form.get('phone')
    nickname = request.form.get('nickname')
    address = request.form.get('address')

    if password != cfpassword :
        flash("암호를 입력주세요!!!")

    else :
        u = User( email, password, name, phone_number, nickname, address)
        print (u)
        try:
            db_session.add(u)
            db_session.commit()
        
        except Exception as err:
            print (err)
            db_session.rollback()

        return redirect('/perform')





@app.route('/sendboard', methods=['GET', 'POST'])
def sendboard():
    all_data = request.json

    title = all_data['title']
    duedate = all_data['duedate']
    money = all_data['money']
    practice = all_data['practice_time']
    perform = all_data['perform_time']
    prac_address = all_data['practice_address']
    perf_address = all_data['perform_address']
    detail_textarea = all_data['detail_info']
    song_textarea = all_data['song_info']
    costume = all_data['costume']
    qualification =all_data["qualification"]
    gender = all_data["gen"]
    instruments = all_data["instruments"]
    practice_mapx = all_data["practice_mapx"]
    practice_mapy = all_data["practice_mapy"]
    perform_mapx = all_data["perform_mapx"]
    perform_mapy = all_data["perform_mapy"]

    print (title, "\n", duedate, money, practice, perform, prac_address, perf_address, detail_textarea, song_textarea, costume, qualification, gender, instruments, practice_mapx, practice_mapy, perform_mapx, perform_mapy)
    
    b = Board( title, duedate, qualification , gender, money, practice, perform, costume, prac_address, practice_mapx, practice_mapy, perf_address, perform_mapx, perform_mapy, detail_textarea, song_textarea, '2')
        
    try:
        db_session.add(b)
        db_session.commit()
        
        for j in instruments:
            iid = j['iid']
            person = j['person']

            inst = BoardInstrument(b.board_id, iid, person)
            db_session.add(inst)
            db_session.commit()
        # inst = BoardInstrument(b.board_id, instruments.in)
    
    except Exception as err:
        print (err)
        db_session.rollback()

    
    print ("-=======>>>>>>>>>>>>>>>>>>>>>>>>>>>",b.board_id)
    return str(b.board_id)


#### DB API ########################################3

@app.route('/boards', methods=["GET"])
def boards_json () : 
    # boardtb = Board.query.filter(Board.board_id == boardid).all()
    boardtb = Board.query.all()
        
    for s in boardtb:
        print (">>>>>>>>>>>>>>>>", s.json()['upload_time'])
    
    return jsonify([s.json() for s in boardtb])

@app.route('/boards/<boardid>', methods=["GET"])
def board_json (boardid) : 
    boardtb = Board.query.filter(Board.board_id == boardid).all()
        
    for s in boardtb:
        print (">>>>>>>>>>>>>>>>", s.json())
    
    return jsonify([s.json() for s in boardtb])

@app.route('/instrument', methods=["GET"])
def get_instrument () : 
    instruments = Instrument.query.all()
    return jsonify([inst.json() for inst in instruments])

@app.route('/boardinstruments/<boardid>', methods=["GET"])
def get_boardinst(boardid) :
    boardinst = BoardInstrument.query.filter(BoardInstrument.board_id == boardid).order_by(BoardInstrument.instrument_id).all()

    return jsonify([s.json() for s in boardinst])
