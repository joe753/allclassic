from flask import Flask, g, request, Response, make_response, flash, redirect, jsonify
import json
from flask import session, render_template, Markup
from datetime import date, datetime, timedelta
from helloflask.db_tables import Users, Board, Instrument, BoardInstrument
from helloflask.init_db import db_session
from sqlalchemy.orm import subqueryload, joinedload, relationship, backref
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import ForeignKey, func



app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
# app.jinja_env.trim_blocks = True


app.config.update(
	SECRET_KEY='ABCDEFG!@#$%^&',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

##### function #######################3\


#######################3 route ######################33
@app.route('/lesson')
def lesson():
    return render_template('lesson.html')


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

@app.route('/signup_nick', methods=['GET', 'POST'])
def checknick () :
    nick = request.json
    result = Users.query.filter(Users.nickname == nick).all()
    print (len(result))

    return str(len(result))

@app.route('/signup', methods=['GET', 'POST'])
def signup_modal():
    form_data = request.json

    email = form_data['email']
    password = form_data['password']
    cfpassword = form_data['cfpassword']
    name = form_data['name']
    phone_number = form_data['phone']
    nickname = form_data['nickname']
    address = form_data['address']

    u = Users( email, password, name, phone_number, nickname, address)
    print (u)
    try:
        db_session.add(u)
        db_session.commit()
    
    except Exception as err:
        print (err)
        db_session.rollback()
        if "Duplicate" in str(err) :
            data = {}
            data['error'] = 'error'
            data['email'] = u.email
            print (data)
            return jsonify(data)

    print (u.email)
    return jsonify(u.email)




@app.route('/sendboard', methods=['POST'])
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
    boardtb = Board.query.order_by(Board.board_id.desc()).all()
    
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


@app.route('/login', methods=['POST'])
def login_post():
    login_data = request.json
    
    email = login_data['email']
    passwd = login_data['password']
    print ("PPPPPP", passwd, func.sha2(passwd, 256))
    # u = Users.query.filter('email = :email and `password` = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
    # u = Users.query.filter(Users.email == email and Users.password == func.sha2(passwd, 256)).first()
    u = Users.query.filter(Users.email == email).filter(Users.password == func.sha2(passwd, 256)).first()
    print (">>>>>>", u)
    if u is not None:
        session['loginUser'] = { 'userid': u.user_no, 'name': u.nickname, 'premium' : u.premium}
        if session.get('next'):
            next = session.get('next')
            del session['next']
            print ("OOOOOOOOOKKKKKKKKKKKK")
            return redirect(next)
        print ("YEEESSS")
        return jsonify ('ok')
    else:
        return jsonify('error')



@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']

    return redirect('/perform')


@app.route('/test')
def test():
    data = {}
    boardinst = json_boardinst()
    instruments = json_instruments()
    boardtb = json_boards()    
    bjson = jsonify([b.json() for b in boardinst])
    ijson = jsonify([i.json() for i in instruments])
    tjson = jsonify([t.json() for t in boardtb])
    data['bjson'] = bjson
    print(">>>>",bjson, ijson, tjson)
    return jsonify(data)

def json_boardinst() :
    boardinst = BoardInstrument.query.order_by(BoardInstrument.instrument_id).all()
    return boardinst

def json_instruments() :
    instruments = Instrument.query.all()
    return instruments

def json_boards () : 
    # boardtb = Board.query.filter(Board.board_id == boardid).all()
    boardtb = Board.query.order_by(Board.board_id.desc()).all()
    
    return boardtb


    # return jsonify([s.json() for s in boardtb])
